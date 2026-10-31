#!/usr/bin/env python3
"""R10 closed-loop BLUE detox — minimal memsafe (no full 4096 B/C)."""
from __future__ import annotations
import gc, hashlib, json, time
from datetime import datetime, timezone
from pathlib import Path
import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
IN, OUT, ROI_DIR, PREV = HERE/"inputs", HERE/"complete", HERE/"roi", HERE/"preview"
for d in (OUT, ROI_DIR, PREV):
    d.mkdir(parents=True, exist_ok=True)
EPS = 1e-3

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1<<20), b""):
            h.update(c)
    return h.hexdigest()

def to_y(bgr):
    b = bgr.astype(np.float32)
    return 0.114*b[...,0] + 0.587*b[...,1] + 0.299*b[...,2]

def luma_only(lp, sr):
    lp_f = lp.astype(np.float32)
    y_lp, y_sr = to_y(lp_f), to_y(sr.astype(np.float32))
    return np.clip((lp_f/(y_lp[...,None]+EPS))*y_sr[...,None], 0, 255).astype(np.uint8)

def material(lp, sr, allow=0.15):
    lp_f, sr_f = lp.astype(np.float32), sr.astype(np.float32)
    y_lp, y_sr = to_y(lp_f), to_y(sr_f)
    hsv = cv2.cvtColor(lp, cv2.COLOR_BGR2HSV)
    S, V = hsv[...,1].astype(np.float32), hsv[...,2].astype(np.float32)
    silver = cv2.GaussianBlur(((S<=55)&(V>=40)).astype(np.float32), (0,0), 1.2)
    base = (lp_f/(y_lp[...,None]+EPS))*y_sr[...,None]
    res_c = (sr_f-lp_f) - to_y(sr_f-lp_f)[...,None]
    return np.clip(base + res_c*((1-silver)*allow)[...,None], 0, 255).astype(np.uint8), float(silver.mean())

def adaptive(lp, sr, k=0.25, thr=3.0):
    lp_f, sr_f = lp.astype(np.float32), sr.astype(np.float32)
    y_lp, y_sr = to_y(lp_f), to_y(sr_f)
    base = (lp_f/(y_lp[...,None]+EPS))*y_sr[...,None]
    res = sr_f - lp_f
    res_y = to_y(res); res_c = res - res_y[...,None]
    poison = np.clip((res[...,0]-np.maximum(res[...,1],res[...,2]))/8.0, 0, 1)
    mag_c = np.linalg.norm(res_c, axis=2)
    allow = (1-poison)*np.clip(1 - mag_c/(np.abs(res_y)+1)/thr, 0, 1)*k
    allow = cv2.GaussianBlur(allow.astype(np.float32), (0,0), 1.0)
    return np.clip(base + res_c*allow[...,None], 0, 255).astype(np.uint8)

def tiled_luma(lp, sr, tile=768):
    H,W = lp.shape[:2]
    if H*W <= 2048*2048:
        return luma_only(lp, sr)
    out = np.empty_like(lp)
    for y in range(0,H,tile):
        for x in range(0,W,tile):
            y2,x2 = min(y+tile,H), min(x+tile,W)
            out[y:y2,x:x2] = luma_only(lp[y:y2,x:x2], sr[y:y2,x:x2])
        print(f"      tile y={y}", flush=True)
        gc.collect()
    return out

def auto_roi(lp, poison, bs=256, step=64):
    d = np.abs(poison.astype(np.float32)-lp.astype(np.float32)).mean(axis=2)
    H,W = d.shape
    best,bx,by = -1.0,0,0
    bs=min(bs,H,W)
    for y in range(0, max(1,H-bs+1), step):
        for x in range(0, max(1,W-bs+1), step):
            m=float(d[y:y+bs,x:x+bs].mean())
            if m>best: best,bx,by=m,x,y
    return (bx,by,bs,bs), best

def crop(im, roi):
    x,y,w,h = roi
    return im[y:y+h, x:x+w]

def ten(im):
    g=cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32)
    gx=cv2.Sobel(g,cv2.CV_32F,1,0,3); gy=cv2.Sobel(g,cv2.CV_32F,0,1,3)
    return float((gx*gx+gy*gy).mean())

def sncc(a,b):
    ga=cv2.GaussianBlur(cv2.cvtColor(a,cv2.COLOR_BGR2GRAY).astype(np.float32),(0,0),2.0)
    gb=cv2.GaussianBlur(cv2.cvtColor(b,cv2.COLOR_BGR2GRAY).astype(np.float32),(0,0),2.0)
    ga-=ga.mean(); gb-=gb.mean()
    return float((ga*gb).sum()/(np.linalg.norm(ga)*np.linalg.norm(gb)+1e-8))

def lab_ab(a,b):
    la=cv2.cvtColor(a,cv2.COLOR_BGR2LAB).astype(np.float32)
    lb=cv2.cvtColor(b,cv2.COLOR_BGR2LAB).astype(np.float32)
    return float(np.abs(la[...,1:]-lb[...,1:]).mean())

def blue_opp(a,b):
    def ln(im):
        f=im.astype(np.float32); return f/(to_y(f)[...,None]+EPS)*100
    d=ln(b)-ln(a)
    return float((np.maximum(d[...,0]-d[...,1],0)+np.maximum(d[...,0]-d[...,2],0)).mean())

def metrics(lp, poison, detox, roi):
    rlp,rpo,rde = crop(lp,roi), crop(poison,roi), crop(detox,roi)
    ab_p, ab_d = lab_ab(rlp,rpo), lab_ab(rlp,rde)
    bo_p, bo_d = blue_opp(rlp,rpo), blue_opp(rlp,rde)
    def imp(p,d):
        return 0.0 if p<1e-6 and d<1e-6 else (-100.0 if p<1e-6 else round((1-d/p)*100,2))
    # ten/sn on ROI always (stable + memsafe)
    ten_p, ten_d = ten(rpo), ten(rde)
    m=dict(
        roi=list(roi),
        roi_ab_poison=ab_p, roi_ab_detox=ab_d, roi_ab_improve_pct=imp(ab_p,ab_d),
        roi_blue_opp_poison=bo_p, roi_blue_opp_detox=bo_d, roi_blue_opp_improve_pct=imp(bo_p,bo_d),
        ten_poison=ten_p, ten_detox=ten_d, ten_keep_pct=round(ten_d/max(ten_p,1e-9)*100,2),
        sn_detox=sncc(rlp,rde),
        metric_scope="ROI formal only",
    )
    m["PASS_roi_ab"] = (ab_d<=0.25) if ab_p<1e-6 else (ab_d<=ab_p*0.55)
    m["PASS_roi_blue_opp"] = (bo_d<=0.5) if bo_p<1e-6 else (bo_d<=bo_p*0.55)
    m["PASS_ten"] = m["ten_keep_pct"]>=92
    m["PASS_sn"] = m["sn_detox"]>=0.95
    m["PASS_FORMAL"] = all([m["PASS_roi_ab"], m["PASS_roi_blue_opp"], m["PASS_ten"], m["PASS_sn"]])
    return m

def save_png(path, img):
    cv2.imwrite(str(path), img, [cv2.IMWRITE_PNG_COMPRESSION,3])
    return dict(path=str(path), bytes=path.stat().st_size, sha256=sha256_file(path), hw=list(img.shape[:2]))

def save_preview(name, img):
    h,w=img.shape[:2]; sc=min(1.0, 1024/max(h,w))
    small=cv2.resize(img,(int(w*sc),int(h*sc)), interpolation=cv2.INTER_AREA)
    path=PREV/f"{name}_PREVIEW.jpg"
    cv2.imwrite(str(path), small, [int(cv2.IMWRITE_JPEG_QUALITY),90])
    return path

def proof(lp, poison, detox, roi, labels, path):
    tiles=[cv2.resize(crop(im,roi),(320,320)) for im in (lp,poison,detox)]
    strip=np.hstack(tiles)
    ban=np.zeros((28,strip.shape[1],3),np.uint8)
    for i,t in enumerate(labels):
        cv2.putText(ban,t,(i*320+6,18),cv2.FONT_HERSHEY_SIMPLEX,0.45,(0,255,180),1)
    cv2.imwrite(str(path), np.vstack([ban,strip]), [int(cv2.IMWRITE_JPEG_QUALITY),92])

def job(tag, method, lp, poison, detox, roi, **extra):
    meta=save_png(OUT/f"{tag}_{method}.png", detox)
    save_preview(f"{tag}_{method}", detox)
    m=metrics(lp, poison, detox, roi)
    m.update(tag=tag, method=method, **meta, **extra)
    proof(lp, poison, detox, roi, ["LP","poison",method], ROI_DIR/f"{tag}_{method}_ROI.jpg")
    print(f"  {tag}/{method} FORMAL={m['PASS_FORMAL']} ab↑{m['roi_ab_improve_pct']}% blue↑{m['roi_blue_opp_improve_pct']}% ten{m['ten_keep_pct']}%", flush=True)
    return m

def main():
    t0=time.time()
    print("R10 CLOSED LOOP minimal", flush=True)
    for p in list(OUT.iterdir())+list(ROI_DIR.iterdir())+list(PREV.iterdir()):
        if p.is_file(): p.unlink()
    jobs=[]
    # P0
    lp=cv2.resize(cv2.imread(str(IN/"P0_L0_512.png")),(2048,2048),interpolation=cv2.INTER_LANCZOS4)
    po=cv2.imread(str(IN/"P0_POISON_2048.png"))
    roi,_=auto_roi(lp,po); print("  auto_roi P0", roi, flush=True)
    for name, fn in [("A_luma", lambda: luma_only(lp,po)),
                     ("B_material", lambda: material(lp,po)[0]),
                     ("C_adaptive", lambda: adaptive(lp,po))]:
        det=fn(); jobs.append(job("P0", name, lp, po, det, roi)); del det; gc.collect()
    del lp,po; gc.collect()
    # P1
    lp=cv2.resize(cv2.imread(str(IN/"P1_L0_512.png")),(2048,2048),interpolation=cv2.INTER_LANCZOS4)
    po=cv2.imread(str(IN/"P1_POISON_2048.png"))
    roi,_=auto_roi(lp,po); print("  auto_roi P1", roi, flush=True)
    for name, fn in [("A_luma", lambda: luma_only(lp,po)),
                     ("B_material", lambda: material(lp,po)[0]),
                     ("C_adaptive", lambda: adaptive(lp,po))]:
        det=fn(); jobs.append(job("P1", name, lp, po, det, roi)); del det; gc.collect()
    del lp,po; gc.collect()
    # PEEP2 A only
    lp=cv2.imread(str(IN/"PEEP2_LP_4096.png"))
    po=cv2.imread(str(IN/"PEEP2_POISON_R7b.png"))
    roi,_=auto_roi(lp,po,bs=512,step=128); print("  auto_roi PEEP2", roi, flush=True)
    det2=tiled_luma(lp,po)
    jobs.append(job("PEEP2_R7b", "A_luma", lp, po, det2, roi, note="B/C skipped full 4096 OOM policy"))
    # nested
    wx,wy,ww,wh=2276,28,512,512
    lp_n=cv2.resize(det2[wy:wy+wh,wx:wx+ww],(2048,2048),interpolation=cv2.INTER_LANCZOS4)
    del det2, lp, po; gc.collect()
    lp_o=cv2.resize(cv2.imread(str(IN/"PEEP3_L0_512.jpg")),(2048,2048),interpolation=cv2.INTER_LANCZOS4)
    sr8=cv2.imread(str(IN/"PEEP3_POISON_R8.png"))
    roi3,_=auto_roi(lp_n, sr8); print("  auto_roi PEEP3", roi3, flush=True)
    n1=luma_only(lp_n, sr8)
    jobs.append(job("PEEP3", "N1_DIRECT", lp_n, sr8, n1, roi3, formula="Y_out=Y_SR8; chrom(LP_nested)"))
    del n1
    y_n,y_o,y_s=to_y(lp_n.astype(np.float32)), to_y(lp_o.astype(np.float32)), to_y(sr8.astype(np.float32))
    n2=np.clip((lp_n.astype(np.float32)/(y_n[...,None]+EPS))*(y_n+(y_s-y_o))[...,None],0,255).astype(np.uint8)
    jobs.append(job("PEEP3", "N2_REBASE", lp_n, sr8, n2, roi3, formula="Y_out=Y_LP_nested+(Y_SR8-Y_LP_orig); chrom(LP_nested)"))
    del n2
    # origLP A only
    roi4,_=auto_roi(lp_o, sr8)
    jobs.append(job("PEEP3_origLP", "A_luma", lp_o, sr8, luma_only(lp_o,sr8), roi4))
    del lp_n, lp_o, sr8; gc.collect()

    inputs=[dict(name=p.name, bytes=p.stat().st_size, sha256=sha256_file(p)) for p in sorted(IN.iterdir()) if p.is_file()]
    outputs=[dict(name=p.name, bytes=p.stat().st_size, sha256=sha256_file(p)) for p in sorted(OUT.iterdir()) if p.suffix==".png"]
    n_f=sum(1 for j in jobs if j["PASS_FORMAL"])
    champions={}
    for j in jobs:
        t=j["tag"]; key=(j["roi_ab_improve_pct"], j["ten_keep_pct"])
        if t not in champions or key>(champions[t]["roi_ab_improve_pct"], champions[t]["ten_keep_pct"]):
            champions[t]=dict(method=j["method"], PASS_FORMAL=j["PASS_FORMAL"],
                              roi_ab_improve_pct=j["roi_ab_improve_pct"],
                              roi_blue_opp_improve_pct=j["roi_blue_opp_improve_pct"],
                              ten_keep_pct=j["ten_keep_pct"], path=j["path"], sha256=j["sha256"])
    accept=dict(
        round="R10_BLUE_DETOX_INDEPENDENT_VALIDATION",
        runner=str(Path(__file__).resolve()),
        supersedes=["R9 ACCEPT","R9b JSON-only"],
        formulas={
            "A_luma":"Y_out=Y_SR; RGB=chrom(LP)*Y_SR",
            "B_material":"A+(1-silver)*0.15*chroma_res",
            "C_adaptive":"A+allow*chroma; kill blue-excess",
            "N1_DIRECT":"Y_out=Y_SR8; chrom(LP_nested)",
            "N2_REBASE":"Y_out=Y_LP_nested+(Y_SR8-Y_LP_orig); chrom(LP_nested)",
        },
        metrics_formal=["roi_lab_ab","roi_lumanorm_blue_opp","ten_keep_ROI","sn_ROI"],
        metrics_legacy_not_formal=["HSV dark_blue"],
        limits=["PEEP2 B/C full 4096 not run (OOM policy)","ten/sn on ROI only"],
        input_manifest=inputs, output_manifest=outputs, jobs=jobs, champions=champions,
        n_jobs=len(jobs), n_pass_formal=n_f,
        status="PARTIAL" if n_f<len(jobs) else "ALL_FORMAL",
        merge_main="NO",
        asof=datetime.now(timezone.utc).isoformat(),
        elapsed_s=round(time.time()-t0,2),
    )
    (OUT/"ACCEPT_R10.json").write_text(json.dumps(accept, indent=2, ensure_ascii=False))
    (OUT/"MANIFEST_SHA256_R10.json").write_text(json.dumps({"inputs":inputs,"outputs":outputs}, indent=2))
    (OUT/"ROI_REPORT_R10.json").write_text(json.dumps([
        {k:j[k] for k in ("tag","method","PASS_FORMAL","roi","roi_ab_improve_pct","roi_blue_opp_improve_pct","ten_keep_pct","path","sha256") if k in j}
        for j in jobs], indent=2))
    (HERE/"LOG_R10.md").write_text(
        f"# R10\n\n**{accept['status']}** formal {n_f}/{len(jobs)} · merge main **NO**\n\n"
        f"single runner closed loop · ROI Lab/opponent formal\n\n## Champions\n"+
        "\n".join(f"- {k}: {v}" for k,v in champions.items())+"\n"
    )
    print(json.dumps({"status":accept["status"],"n_pass_formal":n_f,"n_jobs":len(jobs),"champions":{k:v["method"] for k,v in champions.items()},"elapsed_s":accept["elapsed_s"]}, indent=2))
    print("DONE", OUT)

if __name__=="__main__":
    main()
