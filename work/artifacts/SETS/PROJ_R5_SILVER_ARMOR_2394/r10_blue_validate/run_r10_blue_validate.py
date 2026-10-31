#!/usr/bin/env python3
"""
R10 · BLUE DETOX INDEPENDENT VALIDATION (memsafe · 1.9GB-class hosts)
Single runner closed loop: inputs/ → methods → PNG + ACCEPT + ROI + SHA256.

Formal metrics: ROI Lab a,b + luma-norm blue opponent · NOT HSV dark.
Nested: N1_DIRECT vs N2_REBASE explicit.
Large boards (>2048): full detox A/B/C still produced tiled; metrics FULL on 1/4 scale,
formal PASS only on fixed auto-ROI.
"""
from __future__ import annotations
import gc, hashlib, json, time
from datetime import datetime, timezone
from pathlib import Path
import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
IN, OUT, ROI_DIR = HERE / 'inputs', HERE / 'complete', HERE / 'roi'
OUT.mkdir(parents=True, exist_ok=True)
ROI_DIR.mkdir(parents=True, exist_ok=True)
EPS = 1e-3
TILE = 768

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()

def to_y(bgr):
    b = bgr.astype(np.float32)
    return 0.114 * b[..., 0] + 0.587 * b[..., 1] + 0.299 * b[..., 2]

def auto_roi(lp, poison, bs=256, step=64):
    d = np.abs(poison.astype(np.float32) - lp.astype(np.float32)).mean(axis=2)
    H, W = d.shape
    best, bx, by = -1.0, 0, 0
    for y in range(0, max(1, H - bs + 1), step):
        for x in range(0, max(1, W - bs + 1), step):
            m = float(d[y:y+bs, x:x+bs].mean())
            if m > best:
                best, bx, by = m, x, y
    return (bx, by, min(bs, W - bx), min(bs, H - by)), best

def tile_map(lp, sr, fn_core):
    H, W = lp.shape[:2]
    if H * W <= 2048 * 2048:
        return fn_core(lp, sr)
    out = np.empty_like(lp)
    for y in range(0, H, TILE):
        for x in range(0, W, TILE):
            y2, x2 = min(y + TILE, H), min(x + TILE, W)
            out[y:y2, x:x2] = fn_core(lp[y:y2, x:x2], sr[y:y2, x:x2])
        print(f'      tile y={y}/{H}', flush=True)
        gc.collect()
    return out

def core_luma(lp, sr):
    lp_f = lp.astype(np.float32)
    y_sr = to_y(sr)
    y_lp = to_y(lp_f)
    return np.clip((lp_f / (y_lp[..., None] + EPS)) * y_sr[..., None], 0, 255).astype(np.uint8)

def core_material(lp, sr, silver_sat_max=55.0, silver_v_min=40.0, chroma_allow=0.15):
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
    return np.clip(out, 0, 255).astype(np.uint8)

def core_adaptive(lp, sr, k=0.25, thr=3.0):
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
    mag_y = np.abs(res_y) + 1.0
    allow = (1.0 - poison) * np.clip(1.0 - mag_c / (mag_y * thr + thr), 0, 1) * k
    allow = cv2.GaussianBlur(allow.astype(np.float32), (0, 0), 1.0)
    return np.clip(base + res_c * allow[..., None], 0, 255).astype(np.uint8)

def silver_frac(lp, silver_sat_max=55.0, silver_v_min=40.0):
    hsv = cv2.cvtColor(lp, cv2.COLOR_BGR2HSV)
    S, V = hsv[..., 1].astype(np.float32), hsv[..., 2].astype(np.float32)
    return float(((S <= silver_sat_max) & (V >= silver_v_min)).mean())

def nested_n1(lp_n, sr8):
    return core_luma(lp_n, sr8)

def nested_n2(lp_n, lp_o, sr8):
    y_n, y_o, y_s = to_y(lp_n), to_y(lp_o), to_y(sr8)
    y_out = y_n + (y_s - y_o)
    ratio = lp_n.astype(np.float32) / (y_n[..., None] + EPS)
    return np.clip(ratio * y_out[..., None], 0, 255).astype(np.uint8)

def crop(img, roi):
    x, y, w, h = roi
    return img[y:y+h, x:x+w]

def ten(img):
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
    gx = cv2.Sobel(g, cv2.CV_32F, 1, 0, 3)
    gy = cv2.Sobel(g, cv2.CV_32F, 0, 1, 3)
    return float((gx*gx + gy*gy).mean())

def sncc(a, b):
    ga = cv2.GaussianBlur(cv2.cvtColor(a, cv2.COLOR_BGR2GRAY).astype(np.float32), (0, 0), 2.0)
    gb = cv2.GaussianBlur(cv2.cvtColor(b, cv2.COLOR_BGR2GRAY).astype(np.float32), (0, 0), 2.0)
    ga -= ga.mean(); gb -= gb.mean()
    return float((ga*gb).sum() / (np.linalg.norm(ga)*np.linalg.norm(gb)+1e-8))

def legacy_dark(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    H, S, V = hsv[..., 0].astype(np.float32), hsv[..., 1].astype(np.float32), hsv[..., 2].astype(np.float32)
    return float(((H >= 95) & (H <= 135) & (S > 45) & (V < 160)).mean())

def luma_norm(img):
    f = img.astype(np.float32)
    return f / (to_y(f)[..., None] + EPS) * 100.0

def lab_ab_abs_mean(a, b):
    la = cv2.cvtColor(a, cv2.COLOR_BGR2LAB).astype(np.float32)
    lb = cv2.cvtColor(b, cv2.COLOR_BGR2LAB).astype(np.float32)
    return float(np.abs(la[..., 1:] - lb[..., 1:]).mean())

def blue_opp_mean(a, b):
    na, nb = luma_norm(a), luma_norm(b)
    d = nb - na
    return float((np.maximum(d[..., 0] - d[..., 1], 0) + np.maximum(d[..., 0] - d[..., 2], 0)).mean())

def metrics_roi(lp, poison, detox, roi):
    rlp, rpo, rde = crop(lp, roi), crop(poison, roi), crop(detox, roi)
    ab_p = lab_ab_abs_mean(rlp, rpo)
    ab_d = lab_ab_abs_mean(rlp, rde)
    bo_p = blue_opp_mean(rlp, rpo)
    bo_d = blue_opp_mean(rlp, rde)
    def improve(p, d):
        if p < 1e-6:
            return 0.0 if d < 1e-6 else -100.0
        return round((1 - d / p) * 100, 2)
    ten_p, ten_d = ten(poison), ten(detox)
    # for large boards ten on full is expensive; still do it but on downscale if huge
    H = poison.shape[0]
    if H > 2048:
        sc = 0.25
        small_p = cv2.resize(poison, None, fx=sc, fy=sc, interpolation=cv2.INTER_AREA)
        small_d = cv2.resize(detox, None, fx=sc, fy=sc, interpolation=cv2.INTER_AREA)
        small_l = cv2.resize(lp, None, fx=sc, fy=sc, interpolation=cv2.INTER_AREA)
        ten_p, ten_d = ten(small_p), ten(small_d)
        sn_d = sncc(small_l, small_d)
        sn_p = sncc(small_l, small_p)
    else:
        sn_d = sncc(lp, detox)
        sn_p = sncc(lp, poison)
    out = dict(
        roi_ab_poison=ab_p, roi_ab_detox=ab_d,
        roi_ab_improve_pct=improve(ab_p, ab_d),
        roi_blue_opp_poison=bo_p, roi_blue_opp_detox=bo_d,
        roi_blue_opp_improve_pct=improve(bo_p, bo_d),
        ten_poison=ten_p, ten_detox=ten_d,
        ten_keep_pct=round(ten_d / max(ten_p, 1e-9) * 100, 2),
        sn_poison=sn_p, sn_detox=sn_d,
        legacy_dark_blue_lp=legacy_dark(rlp),
        legacy_dark_blue_poison=legacy_dark(rpo),
        legacy_dark_blue_detox=legacy_dark(rde),
        legacy_dark_blue_delta_pp=round((legacy_dark(rde) - legacy_dark(rpo)) * 100, 3),
        metrics_scope='ROI formal; ten/sn on full if ≤2048 else 0.25x full',
    )
    out['PASS_roi_ab'] = (ab_d <= ab_p * 0.55) if ab_p >= 1e-6 else (ab_d <= 0.25)
    out['PASS_roi_blue_opp'] = (bo_d <= bo_p * 0.55) if bo_p >= 1e-6 else (bo_d <= 0.5)
    out['PASS_ten'] = out['ten_keep_pct'] >= 92.0
    out['PASS_sn'] = out['sn_detox'] >= 0.95
    out['PASS_FORMAL'] = all([out['PASS_roi_ab'], out['PASS_roi_blue_opp'], out['PASS_ten'], out['PASS_sn']])
    return out

def save_png(path: Path, img) -> dict:
    ok = cv2.imwrite(str(path), img, [cv2.IMWRITE_PNG_COMPRESSION, 3])
    assert ok, path
    return dict(path=str(path), bytes=path.stat().st_size, sha256=sha256_file(path), hw=list(img.shape[:2]))

def proof_roi(lp, poison, detox, roi, labels, out_jpg):
    tiles = [cv2.resize(crop(im, roi), (320, 320), interpolation=cv2.INTER_AREA) for im in (lp, poison, detox)]
    strip = np.hstack(tiles)
    ban = np.zeros((28, strip.shape[1], 3), np.uint8)
    for i, t in enumerate(labels):
        cv2.putText(ban, t, (i * 320 + 6, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 180), 1)
    cv2.imwrite(str(out_jpg), np.vstack([ban, strip]), [int(cv2.IMWRITE_JPEG_QUALITY), 92])

def run_method(tag, name, lp, poison, roi, extra=None):
    print(f'  {tag}/{name} computing…', flush=True)
    if name == 'B_material':
        # material needs silver_frac from full LP cheaply
        det = tile_map(lp, poison, core_material)
        extra = dict(silver_frac=silver_frac(lp))
    elif name == 'A_luma':
        det = tile_map(lp, poison, core_luma)
    elif name == 'C_adaptive':
        det = tile_map(lp, poison, core_adaptive)
    path = OUT / f'{tag}_{name}.png'
    meta_file = save_png(path, det)
    m = metrics_roi(lp, poison, det, roi)
    m.update(tag=tag, method=name, **meta_file, roi=list(roi))
    if extra:
        m.update(extra)
    proof_roi(lp, poison, det, roi, ['LP', 'poison', name], ROI_DIR / f'{tag}_{name}_ROI.jpg')
    print(f"  {tag}/{name} FORMAL={m['PASS_FORMAL']} roi_ab {m['roi_ab_poison']:.3f}→{m['roi_ab_detox']:.3f} "
          f"({m['roi_ab_improve_pct']}%) blue_opp {m['roi_blue_opp_improve_pct']}% ten {m['ten_keep_pct']}%",
          flush=True)
    del det
    gc.collect()
    return m

def process_board(tag, lp, poison, methods_order):
    bs = 256 if min(lp.shape[:2]) <= 2048 else 512
    roi, score = auto_roi(lp, poison, bs=bs)
    print(f'  auto_roi {tag} {roi} score={score:.3f}', flush=True)
    rows = []
    for name in methods_order:
        rows.append(run_method(tag, name, lp, poison, roi))
        gc.collect()
    return rows

def main():
    t0 = time.time()
    print('R10 BLUE DETOX INDEPENDENT VALIDATION (memsafe)', flush=True)
    required = [
        'P0_L0_512.png', 'P0_POISON_2048.png',
        'P1_L0_512.png', 'P1_POISON_2048.png',
        'PEEP2_LP_4096.png', 'PEEP2_POISON_R7b.png',
        'PEEP3_L0_512.jpg', 'PEEP3_POISON_R8.png',
    ]
    missing = [r for r in required if not (IN / r).exists()]
    if missing:
        raise SystemExit(f'MISSING inputs: {missing}')

    input_manifest = [dict(name=p.name, bytes=p.stat().st_size, sha256=sha256_file(p))
                      for p in sorted(IN.iterdir()) if p.is_file()]

    # clear prior complete for true single-shot closed loop
    for p in OUT.iterdir():
        if p.is_file():
            p.unlink()
    for p in ROI_DIR.iterdir():
        if p.is_file():
            p.unlink()

    all_jobs = []
    order = ['A_luma', 'B_material', 'C_adaptive']

    lp0 = cv2.resize(cv2.imread(str(IN / 'P0_L0_512.png')), (2048, 2048), interpolation=cv2.INTER_LANCZOS4)
    po0 = cv2.imread(str(IN / 'P0_POISON_2048.png'))
    save_png(OUT / 'P0_LP_2048.png', lp0)
    all_jobs += process_board('P0', lp0, po0, order)
    del lp0, po0; gc.collect()

    lp1 = cv2.resize(cv2.imread(str(IN / 'P1_L0_512.png')), (2048, 2048), interpolation=cv2.INTER_LANCZOS4)
    po1 = cv2.imread(str(IN / 'P1_POISON_2048.png'))
    save_png(OUT / 'P1_LP_2048.png', lp1)
    all_jobs += process_board('P1', lp1, po1, order)
    del lp1, po1; gc.collect()

    lp2 = cv2.imread(str(IN / 'PEEP2_LP_4096.png'))
    po2 = cv2.imread(str(IN / 'PEEP2_POISON_R7b.png'))
    all_jobs += process_board('PEEP2_R7b', lp2, po2, ['A_luma'])  # B/C full 4096 OOM-prone; A only fullres
    # nested parent from A_luma on disk
    det2_a = cv2.imread(str(OUT / 'PEEP2_R7b_A_luma.png'))
    wx, wy, ww, wh = 2276, 28, 512, 512
    lp3_nested = cv2.resize(det2_a[wy:wy+wh, wx:wx+ww], (2048, 2048), interpolation=cv2.INTER_LANCZOS4)
    del det2_a, lp2, po2; gc.collect()

    lp3_orig = cv2.resize(cv2.imread(str(IN / 'PEEP3_L0_512.jpg')), (2048, 2048), interpolation=cv2.INTER_LANCZOS4)
    sr8 = cv2.imread(str(IN / 'PEEP3_POISON_R8.png'))
    save_png(OUT / 'PEEP3_LP_nested_2048.png', lp3_nested)
    save_png(OUT / 'PEEP3_LP_orig_2048.png', lp3_orig)

    roi3, sc3 = auto_roi(lp3_nested, sr8)
    print(f'  auto_roi PEEP3_nested {roi3} score={sc3:.3f}', flush=True)
    for name, det in [
        ('N1_DIRECT', nested_n1(lp3_nested, sr8)),
        ('N2_REBASE', nested_n2(lp3_nested, lp3_orig, sr8)),
    ]:
        mf = save_png(OUT / f'PEEP3_{name}.png', det)
        m = metrics_roi(lp3_nested, sr8, det, roi3)
        m.update(tag='PEEP3', method=name, **mf, roi=list(roi3),
                 formula=('Y_out=Y_SR8; chrom(LP_nested)' if name == 'N1_DIRECT'
                          else 'Y_out=Y_LP_nested+(Y_SR8-Y_LP_orig); chrom(LP_nested)'))
        proof_roi(lp3_nested, sr8, det, roi3, ['LP_nested', 'poison', name], ROI_DIR / f'PEEP3_{name}_ROI.jpg')
        all_jobs.append(m)
        print(f"  PEEP3/{name} FORMAL={m['PASS_FORMAL']} ab↑{m['roi_ab_improve_pct']}% ten{m['ten_keep_pct']}%", flush=True)
        del det; gc.collect()

    all_jobs += process_board('PEEP3_origLP', lp3_orig, sr8, order)
    del lp3_orig, sr8, lp3_nested; gc.collect()

    out_manifest = []
    for p in sorted(OUT.iterdir()):
        if p.suffix.lower() == '.png':
            out_manifest.append(dict(name=p.name, bytes=p.stat().st_size, sha256=sha256_file(p)))

    n_formal = sum(1 for j in all_jobs if j.get('PASS_FORMAL'))
    champions = {}
    for j in all_jobs:
        tag = j['tag']
        key = (j['roi_ab_improve_pct'], j['ten_keep_pct'])
        if tag not in champions or key > (champions[tag]['roi_ab_improve_pct'], champions[tag]['ten_keep_pct']):
            champions[tag] = dict(method=j['method'], PASS_FORMAL=j['PASS_FORMAL'],
                                  roi_ab_improve_pct=j['roi_ab_improve_pct'],
                                  roi_blue_opp_improve_pct=j['roi_blue_opp_improve_pct'],
                                  ten_keep_pct=j['ten_keep_pct'], path=j.get('path'), sha256=j.get('sha256'))

    accept = dict(
        round='R10_BLUE_DETOX_INDEPENDENT_VALIDATION',
        variant='memsafe',
        constitution='single-runner closed loop · ROI Lab/opponent formal · no HSV formal · no post-hoc JSON edit',
        supersedes=['R9 full ACCEPT', 'R9b JSON honesty without matching runner'],
        runner=str(Path(__file__).resolve()),
        host_ram_note='tile=768; metrics ROI formal; ten/sn 0.25x if board>2048',
        formulas={
            'A_luma': 'Y_out=Y_SR; RGB=chrom(LP)*Y_SR',
            'B_material': 'A + (1-silver)*0.15*chroma_residual',
            'C_adaptive': 'A + allow*chroma; kill blue-excess residual',
            'N1_DIRECT': 'Y_out=Y_SR8; chrom(LP_nested)',
            'N2_REBASE': 'Y_out=Y_LP_nested+(Y_SR8-Y_LP_orig); chrom(LP_nested)',
        },
        metrics_formal=['roi_lab_ab_abs', 'roi_lumanorm_blue_opp', 'ten_keep', 'sn'],
        metrics_legacy_not_formal=['HSV dark_blue_frac'],
        input_manifest=input_manifest,
        output_manifest=out_manifest,
        jobs=all_jobs,
        champions=champions,
        n_jobs=len(all_jobs),
        n_pass_formal=n_formal,
        status='PARTIAL' if n_formal < len(all_jobs) else 'ALL_FORMAL',
        merge_main='NO',
        asof=datetime.now(timezone.utc).isoformat(),
        elapsed_s=round(time.time() - t0, 2),
    )
    (OUT / 'ACCEPT_R10.json').write_text(json.dumps(accept, indent=2, ensure_ascii=False))
    (OUT / 'MANIFEST_SHA256_R10.json').write_text(json.dumps(
        dict(inputs=input_manifest, outputs=out_manifest), indent=2))
    roi_report = [dict(
        tag=j['tag'], method=j['method'], PASS_FORMAL=j['PASS_FORMAL'],
        roi_ab_improve_pct=j['roi_ab_improve_pct'],
        roi_blue_opp_improve_pct=j['roi_blue_opp_improve_pct'],
        ten_keep_pct=j['ten_keep_pct'],
        legacy_dark_delta_pp=j['legacy_dark_blue_delta_pp'],
        path=j.get('path'), sha256=j.get('sha256'),
    ) for j in all_jobs]
    (OUT / 'ROI_REPORT_R10.json').write_text(json.dumps(roi_report, indent=2, ensure_ascii=False))
    (HERE / 'LOG_R10.md').write_text(
        f"# R10 BLUE DETOX INDEPENDENT VALIDATION\n\n"
        f"- status: **{accept['status']}** · formal {n_formal}/{len(all_jobs)}\n"
        f"- runner: single closed loop (memsafe)\n"
        f"- formal: ROI Lab ab + luma-norm blue opp · **not** HSV\n"
        f"- Nested: N1_DIRECT vs N2_REBASE separate\n"
        f"- merge main: **NO**\n"
        f"- elapsed: {accept['elapsed_s']}s\n\n## Champions\n" +
        '\n'.join(f"- **{k}**: {v['method']} FORMAL={v['PASS_FORMAL']} ab↑{v['roi_ab_improve_pct']}% "
                  f"blue↑{v['roi_blue_opp_improve_pct']}% ten{v['ten_keep_pct']}%"
                  for k, v in champions.items()) + '\n'
    )
    print(json.dumps({
        'status': accept['status'], 'n_pass_formal': n_formal, 'n_jobs': len(all_jobs),
        'champions': {k: v['method'] for k, v in champions.items()},
        'elapsed_s': accept['elapsed_s'],
    }, indent=2))
    print('DONE R10', OUT)

if __name__ == '__main__':
    main()
