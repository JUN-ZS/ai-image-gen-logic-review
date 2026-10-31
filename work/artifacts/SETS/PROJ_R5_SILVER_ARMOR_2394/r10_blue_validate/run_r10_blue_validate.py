#!/usr/bin/env python3
"""R10 BLUE DETOX INDEPENDENT VALIDATION — memory-safe closed loop runner."""
from __future__ import annotations
import gc, hashlib, json, time
from datetime import datetime, timezone
from pathlib import Path
import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
IN, OUT, ROI_DIR = HERE / "inputs", HERE / "complete", HERE / "roi"
for d in (OUT, ROI_DIR):
    d.mkdir(parents=True, exist_ok=True)
EPS = 1e-3

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()

def to_y(bgr):
    b = bgr.astype(np.float32)
    return 0.114 * b[..., 0] + 0.587 * b[..., 1] + 0.299 * b[..., 2]

def luma_only_core(lp, sr):
    lp_f = lp.astype(np.float32)
    y_lp = to_y(lp_f)
    y_sr = to_y(sr.astype(np.float32))
    return np.clip((lp_f / (y_lp[..., None] + EPS)) * y_sr[..., None], 0, 255).astype(np.uint8)

def material_core(lp, sr, silver_sat_max=55.0, silver_v_min=40.0, chroma_allow=0.15):
    lp_f = lp.astype(np.float32)
    sr_f = sr.astype(np.float32)
    y_lp, y_sr = to_y(lp_f), to_y(sr_f)
    hsv = cv2.cvtColor(lp, cv2.COLOR_BGR2HSV)
    S, V = hsv[..., 1].astype(np.float32), hsv[..., 2].astype(np.float32)
    silver = cv2.GaussianBlur(((S <= silver_sat_max) & (V >= silver_v_min)).astype(np.float32), (0, 0), 1.2)
    base = (lp_f / (y_lp[..., None] + EPS)) * y_sr[..., None]
    res = sr_f - lp_f
    res_c = res - to_y(res)[..., None]
    out = base + res_c * ((1.0 - silver) * chroma_allow)[..., None]
    return np.clip(out, 0, 255).astype(np.uint8), float(silver.mean())

def adaptive_core(lp, sr, k=0.25, thr=3.0):
    lp_f = lp.astype(np.float32)
    sr_f = sr.astype(np.float32)
    y_lp, y_sr = to_y(lp_f), to_y(sr_f)
    base = (lp_f / (y_lp[..., None] + EPS)) * y_sr[..., None]
    res = sr_f - lp_f
    res_y = to_y(res)
    res_c = res - res_y[..., None]
    b_ex = res[..., 0] - np.maximum(res[..., 1], res[..., 2])
    poison = np.clip(b_ex / 8.0, 0, 1)
    mag_c = np.linalg.norm(res_c, axis=2)
    allow = (1.0 - poison) * np.clip(1.0 - mag_c / (np.abs(res_y) + 1.0) / thr, 0, 1) * k
    allow = cv2.GaussianBlur(allow.astype(np.float32), (0, 0), 1.0)
    return np.clip(base + res_c * allow[..., None], 0, 255).astype(np.uint8)

def apply_tiled(lp, sr, core, tile=512, **kw):
    H, W = lp.shape[:2]
    out = np.empty_like(lp)
    silver_acc, n = 0.0, 0
    for y in range(0, H, tile):
        for x in range(0, W, tile):
            y2, x2 = min(y + tile, H), min(x + tile, W)
            r = core(lp[y:y2, x:x2], sr[y:y2, x:x2], **kw) if kw else core(lp[y:y2, x:x2], sr[y:y2, x:x2])
            if isinstance(r, tuple):
                out[y:y2, x:x2], s = r
                silver_acc += s; n += 1
            else:
                out[y:y2, x:x2] = r
    if n:
        return out, silver_acc / n
    return out

def nested_n1(lp_n, sr8):
    return luma_only_core(lp_n, sr8)

def nested_n2(lp_n, lp_o, sr8):
    y_n, y_o, y_s = to_y(lp_n.astype(np.float32)), to_y(lp_o.astype(np.float32)), to_y(sr8.astype(np.float32))
    ratio = lp_n.astype(np.float32) / (y_n[..., None] + EPS)
    return np.clip(ratio * (y_n + (y_s - y_o))[..., None], 0, 255).astype(np.uint8)

def auto_roi(lp, poison, bs=256, step=64):
    d = np.abs(poison.astype(np.float32) - lp.astype(np.float32)).mean(axis=2)
    H, W = d.shape
    best, bx, by = -1.0, 0, 0
    bs = min(bs, H, W)
    for y in range(0, max(1, H - bs + 1), step):
        for x in range(0, max(1, W - bs + 1), step):
            m = float(d[y:y+bs, x:x+bs].mean())
            if m > best:
                best, bx, by = m, x, y
    return (bx, by, bs, bs), best

def crop(img, roi):
    x, y, w, h = roi
    return img[y:y+h, x:x+w]

def ten(img):
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
    gx = cv2.Sobel(g, cv2.CV_32F, 1, 0, 3); gy = cv2.Sobel(g, cv2.CV_32F, 0, 1, 3)
    return float((gx*gx + gy*gy).mean())

def sncc(a, b):
    ga = cv2.GaussianBlur(cv2.cvtColor(a, cv2.COLOR_BGR2GRAY).astype(np.float32), (0, 0), 2.0)
    gb = cv2.GaussianBlur(cv2.cvtColor(b, cv2.COLOR_BGR2GRAY).astype(np.float32), (0, 0), 2.0)
    ga -= ga.mean(); gb -= gb.mean()
    return float((ga*gb).sum() / (np.linalg.norm(ga)*np.linalg.norm(gb) + 1e-8))

def legacy_dark(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    H, S, V = hsv[...,0].astype(np.float32), hsv[...,1].astype(np.float32), hsv[...,2].astype(np.float32)
    return float(((H>=95)&(H<=135)&(S>45)&(V<160)).mean())

def lab_ab_abs(a, b):
    la = cv2.cvtColor(a, cv2.COLOR_BGR2LAB).astype(np.float32)
    lb = cv2.cvtColor(b, cv2.COLOR_BGR2LAB).astype(np.float32)
    return float(np.abs(la[...,1:] - lb[...,1:]).mean())

def blue_opp_abs(a, b):
    def ln(im):
        f = im.astype(np.float32); y = to_y(f)[...,None] + EPS
        return f / y * 100.0
    d = ln(b) - ln(a)
    return float((np.maximum(d[...,0]-d[...,1],0) + np.maximum(d[...,0]-d[...,2],0)).mean())

def metrics_roi(lp, poison, detox, roi):
    rlp, rpo, rde = crop(lp, roi), crop(poison, roi), crop(detox, roi)
    ab_p, ab_d = lab_ab_abs(rlp, rpo), lab_ab_abs(rlp, rde)
    bo_p, bo_d = blue_opp_abs(rlp, rpo), blue_opp_abs(rlp, rde)
    def improve(p, d):
        if p < 1e-6: return 0.0 if d < 1e-6 else -100.0
        return round((1 - d/p)*100, 2)
    # ten/sn/legacy on ROI only (full 4096 OOM); document scope=roi
    ten_p, ten_d = ten(rpo), ten(rde)
    m = dict(
        roi=list(roi),
        metric_scope="ROI_only_for_ten_sn_legacy",
        roi_ab_poison=ab_p, roi_ab_detox=ab_d, roi_ab_improve_pct=improve(ab_p, ab_d),
        roi_blue_opp_poison=bo_p, roi_blue_opp_detox=bo_d, roi_blue_opp_improve_pct=improve(bo_p, bo_d),
        ten_poison=ten_p, ten_detox=ten_d,
        ten_keep_pct=round(ten_d/max(ten_p,1e-9)*100, 2),
        sn_detox=sncc(rlp, rde),
        legacy_dark_blue_poison=legacy_dark(rpo),
        legacy_dark_blue_detox=legacy_dark(rde),
        legacy_dark_delta_pp=round((legacy_dark(rde)-legacy_dark(rpo))*100, 3),
    )
    # FORMAL gates (ROI Lab/opponent; not HSV)
    if ab_p < 1e-6:
        m["PASS_roi_ab"] = ab_d <= 0.25
    else:
        m["PASS_roi_ab"] = ab_d <= ab_p * 0.55
    if bo_p < 1e-6:
        m["PASS_roi_blue_opp"] = bo_d <= 0.5
    else:
        m["PASS_roi_blue_opp"] = bo_d <= bo_p * 0.55
    m["PASS_ten"] = m["ten_keep_pct"] >= 92.0
    m["PASS_sn"] = m["sn_detox"] >= 0.95
    m["PASS_FORMAL"] = all([m["PASS_roi_ab"], m["PASS_roi_blue_opp"], m["PASS_ten"], m["PASS_sn"]])
    return m

def save_png(path, img):
    cv2.imwrite(str(path), img, [cv2.IMWRITE_PNG_COMPRESSION, 3])
    return dict(path=str(path), bytes=path.stat().st_size, sha256=sha256_file(path), hw=list(img.shape[:2]))

def proof(lp, poison, detox, roi, labels, path):
    tiles = [cv2.resize(crop(im, roi), (320, 320)) for im in (lp, poison, detox)]
    strip = np.hstack(tiles)
    ban = np.zeros((28, strip.shape[1], 3), np.uint8)
    for i, t in enumerate(labels):
        cv2.putText(ban, t, (i*320+6, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0,255,180), 1)
    cv2.imwrite(str(path), np.vstack([ban, strip]), [int(cv2.IMWRITE_JPEG_QUALITY), 92])

def run_methods(tag, lp, poison, methods, tile=512):
    roi, score = auto_roi(lp, poison, bs=256 if min(lp.shape[:2])<=2048 else 512)
    print(f"  auto_roi {tag} {roi} score={score:.3f}", flush=True)
    rows = []
    for name, kind in methods:
        if kind == "A":
            det = apply_tiled(lp, poison, luma_only_core, tile=tile)
            extra = {}
        elif kind == "B":
            det, sf = apply_tiled(lp, poison, material_core, tile=tile)
            extra = {"silver_frac": sf}
        elif kind == "C":
            det = apply_tiled(lp, poison, adaptive_core, tile=tile)
            extra = {}
        else:
            raise ValueError(kind)
        meta = save_png(OUT / f"{tag}_{name}.png", det)
        m = metrics_roi(lp, poison, det, roi)
        m.update(tag=tag, method=name, **meta, **extra)
        proof(lp, poison, det, roi, ["LP", "poison", name], ROI_DIR / f"{tag}_{name}_ROI.jpg")
        print(f"  {tag}/{name} FORMAL={m['PASS_FORMAL']} ab {m['roi_ab_poison']:.3f}→{m['roi_ab_detox']:.3f} ({m['roi_ab_improve_pct']}%) ten {m['ten_keep_pct']}%", flush=True)
        rows.append(m)
        del det
        gc.collect()
    return rows, roi

def main():
    t0 = time.time()
    print("R10 BLUE DETOX INDEPENDENT VALIDATION (memsafe)", flush=True)
    req = ["P0_L0_512.png","P0_POISON_2048.png","P1_L0_512.png","P1_POISON_2048.png",
           "PEEP2_LP_4096.png","PEEP2_POISON_R7b.png","PEEP3_L0_512.jpg","PEEP3_POISON_R8.png"]
    miss = [r for r in req if not (IN/r).exists()]
    if miss:
        raise SystemExit(f"MISSING {miss}")
    input_manifest = [dict(name=p.name, bytes=p.stat().st_size, sha256=sha256_file(p)) for p in sorted(IN.iterdir()) if p.is_file()]
    ABC = [("A_luma","A"),("B_material","B"),("C_adaptive","C")]
    jobs = []

    lp0 = cv2.resize(cv2.imread(str(IN/"P0_L0_512.png")), (2048,2048), interpolation=cv2.INTER_LANCZOS4)
    po0 = cv2.imread(str(IN/"P0_POISON_2048.png"))
    save_png(OUT/"P0_LP_2048.png", lp0)
    j, _ = run_methods("P0", lp0, po0, ABC, tile=1024); jobs += j
    del lp0, po0; gc.collect()

    lp1 = cv2.resize(cv2.imread(str(IN/"P1_L0_512.png")), (2048,2048), interpolation=cv2.INTER_LANCZOS4)
    po1 = cv2.imread(str(IN/"P1_POISON_2048.png"))
    save_png(OUT/"P1_LP_2048.png", lp1)
    j, _ = run_methods("P1", lp1, po1, ABC, tile=1024); jobs += j
    del lp1, po1; gc.collect()

    # PEEP2: only A_luma full (mem); B/C = A base + ROI local recompute paste
    lp2 = cv2.imread(str(IN/"PEEP2_LP_4096.png"))
    po2 = cv2.imread(str(IN/"PEEP2_POISON_R7b.png"))
    roi2, sc2 = auto_roi(lp2, po2, bs=512, step=128)
    print(f"  auto_roi PEEP2_R7b {roi2} score={sc2:.3f}", flush=True)
    det2 = apply_tiled(lp2, po2, luma_only_core, tile=512)
    meta = save_png(OUT/"PEEP2_R7b_A_luma.png", det2)
    m = metrics_roi(lp2, po2, det2, roi2)
    m.update(tag="PEEP2_R7b", method="A_luma", **meta)
    proof(lp2, po2, det2, roi2, ["LP","poison","A_luma"], ROI_DIR/"PEEP2_R7b_A_luma_ROI.jpg")
    print(f"  PEEP2_R7b/A_luma FORMAL={m['PASS_FORMAL']} ab↑{m['roi_ab_improve_pct']}%", flush=True)
    jobs.append(m)
    # B/C only on ROI crop (not full 4096)
    x,y,w,h = roi2
    for name, core, kind in [("B_material", material_core, "B"), ("C_adaptive", adaptive_core, "C")]:
        if kind=="B":
            local, sf = core(lp2[y:y+h, x:x+w], po2[y:y+h, x:x+w]); extra={"silver_frac":sf, "scope":"ROI_paste"}
        else:
            local = core(lp2[y:y+h, x:x+w], po2[y:y+h, x:x+w]); extra={"scope":"ROI_paste"}
        det = det2.copy()
        det[y:y+h, x:x+w] = local
        meta = save_png(OUT/f"PEEP2_R7b_{name}.png", det)
        m = metrics_roi(lp2, po2, det, roi2)
        m.update(tag="PEEP2_R7b", method=name, **meta, **extra)
        proof(lp2, po2, det, roi2, ["LP","poison",name], ROI_DIR/f"PEEP2_R7b_{name}_ROI.jpg")
        print(f"  PEEP2_R7b/{name} FORMAL={m['PASS_FORMAL']} ab↑{m['roi_ab_improve_pct']}% scope=ROI_paste", flush=True)
        jobs.append(m)
        del det, local
    save_png(OUT/"PEEP2_R7b_A_luma_for_nested.png", det2)
    del lp2, po2; gc.collect()

    wx, wy, ww, wh = 2276, 28, 512, 512
    lp3_orig = cv2.resize(cv2.imread(str(IN/"PEEP3_L0_512.jpg")), (2048,2048), interpolation=cv2.INTER_LANCZOS4)
    sr8 = cv2.imread(str(IN/"PEEP3_POISON_R8.png"))
    lp3_nested = cv2.resize(det2[wy:wy+wh, wx:wx+ww], (2048,2048), interpolation=cv2.INTER_LANCZOS4)
    del det2; gc.collect()
    save_png(OUT/"PEEP3_LP_nested_2048.png", lp3_nested)
    save_png(OUT/"PEEP3_LP_orig_2048.png", lp3_orig)

    for name, det, formula in [
        ("N1_DIRECT", nested_n1(lp3_nested, sr8), "Y_out=Y_SR8; chrom(LP_nested)"),
        ("N2_REBASE", nested_n2(lp3_nested, lp3_orig, sr8), "Y_out=Y_LP_nested+(Y_SR8-Y_LP_orig); chrom(LP_nested)"),
    ]:
        roi, sc = auto_roi(lp3_nested, sr8)
        meta = save_png(OUT / f"PEEP3_{name}.png", det)
        m = metrics_roi(lp3_nested, sr8, det, roi)
        m.update(tag="PEEP3", method=name, formula=formula, **meta)
        proof(lp3_nested, sr8, det, roi, ["LP_nested","poison",name], ROI_DIR/f"PEEP3_{name}_ROI.jpg")
        print(f"  PEEP3/{name} FORMAL={m['PASS_FORMAL']} ab↑{m['roi_ab_improve_pct']}%", flush=True)
        jobs.append(m)

    j, _ = run_methods("PEEP3_origLP", lp3_orig, sr8, ABC, tile=1024); jobs += j
    del lp3_orig, sr8, lp3_nested; gc.collect()

    out_manifest = []
    for p in sorted(OUT.iterdir()):
        if p.suffix.lower()==".png":
            out_manifest.append(dict(name=p.name, bytes=p.stat().st_size, sha256=sha256_file(p)))

    n_formal = sum(1 for j in jobs if j.get("PASS_FORMAL"))
    champions = {}
    for j in jobs:
        t = j["tag"]
        key = (j["roi_ab_improve_pct"], j["ten_keep_pct"])
        if t not in champions or key > (champions[t]["roi_ab_improve_pct"], champions[t]["ten_keep_pct"]):
            champions[t] = dict(method=j["method"], PASS_FORMAL=j["PASS_FORMAL"],
                                roi_ab_improve_pct=j["roi_ab_improve_pct"],
                                roi_blue_opp_improve_pct=j["roi_blue_opp_improve_pct"],
                                ten_keep_pct=j["ten_keep_pct"], path=j.get("path"), sha256=j.get("sha256"))

    accept = dict(
        round="R10_BLUE_DETOX_INDEPENDENT_VALIDATION",
        runner=str(Path(__file__).resolve()),
        supersedes=["R9 overclaim ACCEPT", "R9b JSON-only without runner"],
        formulas={
            "A_luma": "Y_out=Y_SR; RGB=chrom(LP)*Y_SR",
            "B_material": "A + (1-silver)*0.15*chroma_res",
            "C_adaptive": "A + allow*chroma_res; kill blue-excess",
            "N1_DIRECT": "Y_out=Y_SR8; chrom(LP_nested)",
            "N2_REBASE": "Y_out=Y_LP_nested+(Y_SR8-Y_LP_orig); chrom(LP_nested)",
        },
        metrics_formal=["roi_lab_ab", "roi_lumanorm_blue_opp", "ten_keep", "sn"],
        metrics_legacy_not_formal=["HSV dark_blue_frac"],
        roi_policy="auto max |poison-LP| block deterministic",
        input_manifest=input_manifest,
        output_manifest=out_manifest,
        jobs=jobs,
        champions=champions,
        n_jobs=len(jobs),
        n_pass_formal=n_formal,
        status="PARTIAL" if n_formal < len(jobs) else "ALL_FORMAL",
        merge_main="NO",
        asof=datetime.now(timezone.utc).isoformat(),
        elapsed_s=round(time.time()-t0, 2),
    )
    (OUT/"ACCEPT_R10.json").write_text(json.dumps(accept, indent=2, ensure_ascii=False))
    (OUT/"MANIFEST_SHA256_R10.json").write_text(json.dumps({"inputs":input_manifest,"outputs":out_manifest}, indent=2))
    (OUT/"ROI_REPORT_R10.json").write_text(json.dumps([
        {k:j[k] for k in ("tag","method","PASS_FORMAL","roi","roi_ab_poison","roi_ab_detox","roi_ab_improve_pct",
                          "roi_blue_opp_improve_pct","ten_keep_pct","legacy_dark_delta_pp","path","sha256") if k in j}
        for j in jobs
    ], indent=2))
    (HERE/"LOG_R10.md").write_text(
        f"# R10\n\nstatus **{accept['status']}** formal {n_formal}/{len(jobs)} · merge main **NO**\n\n"
        f"runner closed loop · ROI Lab/opponent formal · HSV legacy only\n\n## Champions\n" +
        "\n".join(f"- {k}: {v}" for k,v in champions.items())
    )
    print(json.dumps({"status":accept["status"],"n_pass_formal":n_formal,"n_jobs":len(jobs),
                      "champions":champions,"elapsed_s":accept["elapsed_s"]}, indent=2, ensure_ascii=False))
    print("DONE R10", OUT)

if __name__ == "__main__":
    main()
