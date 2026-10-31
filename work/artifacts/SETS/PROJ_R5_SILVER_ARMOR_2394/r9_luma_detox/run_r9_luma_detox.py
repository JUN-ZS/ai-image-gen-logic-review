#!/usr/bin/env python3
"""R9 FULL-CHAIN luma-only residual detox (E-BLUE-01..04).
Formula:
  Y_out = Y_LP + (Y_SR - Y_LP)
  RGB_out = chromaticity(LP) * Y_out
Primary: lossless PNG children · never full BGR residual.
"""
from __future__ import annotations
import json, time
from datetime import datetime, timezone
from pathlib import Path
import cv2
import numpy as np

ROOT = Path('/workspace/artifacts/SETS/PROJ_R5_SILVER_ARMOR_2394')
OUT = ROOT / 'r9_luma_detox'
COMPLETE = OUT / 'complete'
PEEP = OUT / 'peep'
for d in (OUT, COMPLETE, PEEP):
    d.mkdir(parents=True, exist_ok=True)

MOTHER = cv2.imread(str(ROOT / 'MOTHER_SRC.jpg'))
assert MOTHER is not None

EPS = 1e-3

def to_y(bgr: np.ndarray) -> np.ndarray:
    bgr = bgr.astype(np.float32)
    return 0.114 * bgr[..., 0] + 0.587 * bgr[..., 1] + 0.299 * bgr[..., 2]

def luma_only_detox(lp: np.ndarray, sr: np.ndarray) -> np.ndarray:
    """Inject only dY; lock LP chromaticity."""
    assert lp.shape == sr.shape, (lp.shape, sr.shape)
    lp_f = lp.astype(np.float32)
    sr_f = sr.astype(np.float32)
    y_lp = to_y(lp_f)
    y_sr = to_y(sr_f)
    dy = y_sr - y_lp
    # chromaticity from LP
    ratio = lp_f / (y_lp[..., None] + EPS)
    out = ratio * (y_lp + dy)[..., None]
    return np.clip(out, 0, 255).astype(np.uint8)

def ten(img: np.ndarray) -> float:
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
    gx = cv2.Sobel(g, cv2.CV_32F, 1, 0, 3)
    gy = cv2.Sobel(g, cv2.CV_32F, 0, 1, 3)
    return float((gx * gx + gy * gy).mean())

def sncc(a: np.ndarray, b: np.ndarray) -> float:
    """Structure NCC on lowpass gray."""
    ga = cv2.GaussianBlur(cv2.cvtColor(a, cv2.COLOR_BGR2GRAY).astype(np.float32), (0, 0), 2.0)
    gb = cv2.GaussianBlur(cv2.cvtColor(b, cv2.COLOR_BGR2GRAY).astype(np.float32), (0, 0), 2.0)
    ga = ga - ga.mean(); gb = gb - gb.mean()
    den = (np.linalg.norm(ga) * np.linalg.norm(gb) + 1e-8)
    return float((ga * gb).sum() / den)

def blue_stats(img: np.ndarray) -> dict:
    bgr = img.astype(np.float32)
    B, G, R = bgr[..., 0], bgr[..., 1], bgr[..., 2]
    be = np.clip(B - np.maximum(G, R), 0, None)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    H, S, V = hsv[..., 0].astype(np.float32), hsv[..., 1].astype(np.float32), hsv[..., 2].astype(np.float32)
    dark = ((H >= 95) & (H <= 135) & (S > 45) & (V < 160)).astype(np.float32)
    return dict(
        be_mean=float(be.mean()),
        be_p95=float(np.percentile(be, 95)),
        dark_blue_frac=float(dark.mean()),
        BminusG=float((B - G).mean()),
    )

def chroma_res_abs(lp: np.ndarray, sr: np.ndarray) -> dict:
    res = sr.astype(np.float32) - lp.astype(np.float32)
    ry = to_y(res)
    ch = res - ry[..., None]
    return dict(
        absB=float(np.abs(ch[..., 0]).mean()),
        absG=float(np.abs(ch[..., 1]).mean()),
        absR=float(np.abs(ch[..., 2]).mean()),
    )

def save_png(path: Path, img: np.ndarray):
    path.parent.mkdir(parents=True, exist_ok=True)
    ok = cv2.imwrite(str(path), img, [cv2.IMWRITE_PNG_COMPRESSION, 3])
    assert ok, path
    return path.stat().st_size

def proof_strip(lp, poison, detox, labels, out_jpg, crop=None):
    h, w = lp.shape[:2]
    if crop is None:
        cy, cx = h // 2, w // 2
        s = min(400, h // 2, w // 2)
        crop = (cy - s // 2, cx - s // 2, s, s)
    y, x, sh, sw = crop
    tiles = []
    for im in (lp, poison, detox):
        t = im[y:y + sh, x:x + sw]
        tiles.append(cv2.resize(t, (360, 360), interpolation=cv2.INTER_AREA))
    strip = np.hstack(tiles)
    ban = np.zeros((28, strip.shape[1], 3), np.uint8)
    for i, t in enumerate(labels):
        cv2.putText(ban, t, (i * 360 + 8, 19), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 180), 1)
    cv2.imwrite(str(out_jpg), np.vstack([ban, strip]), [int(cv2.IMWRITE_JPEG_QUALITY), 92])

def process_job(tag, lp, sr, out_png, proof_jpg, crop=None) -> dict:
    t0 = time.time()
    print(f'  detox {tag} {sr.shape} …', flush=True)
    # tiled for large
    H, W = sr.shape[:2]
    if H * W > 2048 * 2048:
        out = np.zeros_like(sr)
        tile = 1024
        for y in range(0, H, tile):
            for x in range(0, W, tile):
                y2, x2 = min(y + tile, H), min(x + tile, W)
                out[y:y2, x:x2] = luma_only_detox(lp[y:y2, x:x2], sr[y:y2, x:x2])
            if y % 1024 == 0:
                print(f'    row y={y}', flush=True)
        detox = out
    else:
        detox = luma_only_detox(lp, sr)

    nbytes = save_png(out_png, detox)
    bs_lp = blue_stats(lp)
    bs_sr = blue_stats(sr)
    bs_dx = blue_stats(detox)
    cr_sr = chroma_res_abs(lp, sr)
    cr_dx = chroma_res_abs(lp, detox)
    meta = dict(
        tag=tag,
        child=str(out_png),
        child_bytes=nbytes,
        hw=list(detox.shape[:2]),
        ten_lp=ten(lp),
        ten_poison=ten(sr),
        ten_detox=ten(detox),
        sn_poison=sncc(lp, sr),
        sn_detox=sncc(lp, detox),
        blue_lp=bs_lp,
        blue_poison=bs_sr,
        blue_detox=bs_dx,
        chroma_abs_poison=cr_sr,
        chroma_abs_detox=cr_dx,
        dark_blue_delta_pp=round((bs_dx['dark_blue_frac'] - bs_sr['dark_blue_frac']) * 100, 3),
        elapsed_s=round(time.time() - t0, 2),
        formula='Y_out=Y_LP+(Y_SR-Y_LP); RGB=chrom(LP)*Y_out',
        iron='E-BLUE luma-only residual',
    )
    # PASS gates
    meta['PASS_blue_down'] = bs_dx['dark_blue_frac'] <= bs_sr['dark_blue_frac'] + 0.002
    meta['PASS_chroma_B'] = cr_dx['absB'] < cr_sr['absB'] * 0.35  # strong kill
    meta['PASS_ten_keep'] = meta['ten_detox'] >= meta['ten_poison'] * 0.92
    meta['PASS_sn'] = meta['sn_detox'] >= 0.95
    meta['PASS'] = all(meta[k] for k in ('PASS_blue_down', 'PASS_chroma_B', 'PASS_ten_keep', 'PASS_sn'))
    proof_strip(lp, sr, detox, ['LP', f'{tag} RGB-res', f'{tag} LUMA'], proof_jpg, crop=crop)
    print(f'  → {tag} PASS={meta["PASS"]} dark {bs_sr["dark_blue_frac"]:.3f}→{bs_dx["dark_blue_frac"]:.3f} '
          f'Babs {cr_sr["absB"]:.3f}→{cr_dx["absB"]:.3f} ten {meta["ten_poison"]:.0f}→{meta["ten_detox"]:.0f}', flush=True)
    return meta, detox

# ---------- jobs ----------
results = []
t_all = time.time()
print('R9 FULL-CHAIN luma-only detox', flush=True)

# P0
x0, y0, sz = 300, 693, 512
L0_p0 = MOTHER[y0:y0 + sz, x0:x0 + sz].copy()
cv2.imwrite(str(PEEP / 'P0_L0_512.jpg'), L0_p0, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
LP0 = cv2.resize(L0_p0, (2048, 2048), interpolation=cv2.INTER_LANCZOS4)
SR0 = cv2.imread(str(ROOT / 'r6c/complete/P0_CHILD_2048_NCNN_GENERAL_R6c.png'))
assert SR0 is not None and SR0.shape[:2] == (2048, 2048)
m0, DET0 = process_job(
    'P0', LP0, SR0,
    COMPLETE / 'P0_CHILD_2048_LUMA_R9.png',
    COMPLETE / 'PROOF_P0_LUMA_R9.jpg',
    crop=(1024 - 200, 1024 - 200, 400, 400),
)
results.append(m0)

# P1
x1, y1 = 318, 180
L0_p1 = MOTHER[y1:y1 + sz, x1:x1 + sz].copy()
cv2.imwrite(str(PEEP / 'P1_L0_512.jpg'), L0_p1, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
LP1 = cv2.resize(L0_p1, (2048, 2048), interpolation=cv2.INTER_LANCZOS4)
SR1 = cv2.imread(str(ROOT / 'r6c/complete/P1_CHILD_2048_NCNN_GENERAL_R6c.png'))
assert SR1 is not None
m1, DET1 = process_job(
    'P1', LP1, SR1,
    COMPLETE / 'P1_CHILD_2048_LUMA_R9.png',
    COMPLETE / 'PROOF_P1_LUMA_R9.jpg',
)
results.append(m1)

# PEEP2 from R7 (raw) + R7b (ridge) — LP from saved or rebuild
lp_path = ROOT / 'r7_peep2/peep/LP_4096.png'
if lp_path.exists():
    LP2 = cv2.imread(str(lp_path))
else:
    # rebuild: window on P0 LP 2048
    wx, wy, ww, wh = 708, 32, 1024, 1024
    peep2_l0 = LP0[wy:wy + wh, wx:wx + ww]
    LP2 = cv2.resize(peep2_l0, (4096, 4096), interpolation=cv2.INTER_LANCZOS4)
assert LP2 is not None and LP2.shape[0] == 4096
cv2.imwrite(str(PEEP / 'PEEP2_LP_4096_preview.jpg'),
            cv2.resize(LP2, (1024, 1024), interpolation=cv2.INTER_AREA),
            [int(cv2.IMWRITE_JPEG_QUALITY), 90])

SR7 = cv2.imread(str(ROOT / 'r7_peep2/complete/PEEP2_CHILD_4096_NCNN_FULLRES_R7.png'))
SR7b = cv2.imread(str(ROOT / 'r7_peep2/complete/PEEP2_CHILD_4096_NCNN_RIDGE_R7b.png'))
assert SR7 is not None and SR7b is not None

m7, DET7 = process_job(
    'PEEP2_R7', LP2, SR7,
    COMPLETE / 'PEEP2_CHILD_4096_LUMA_R9.png',
    COMPLETE / 'PROOF_PEEP2_R7_LUMA_R9.jpg',
    crop=(2048 - 256, 2048 - 256, 512, 512),
)
results.append(m7)

m7b, DET7b = process_job(
    'PEEP2_R7b', LP2, SR7b,
    COMPLETE / 'PEEP2_CHILD_4096_RIDGE_LUMA_R9.png',
    COMPLETE / 'PROOF_PEEP2_R7b_LUMA_R9.jpg',
    crop=(2048 - 256, 2048 - 256, 512, 512),
)
results.append(m7b)

# PEEP3 — parent is R7b 4096 window
wx3, wy3, ww3, wh3 = 2276, 28, 512, 512
# LP from original peep L0 or from R7b window Lanczos
l0_p3 = ROOT / 'r8_peep3/peep/PEEP3_L0_512.jpg'
if l0_p3.exists():
    L0_p3 = cv2.imread(str(l0_p3))
else:
    L0_p3 = SR7b[wy3:wy3 + wh3, wx3:wx3 + ww3]  # fallback poison parent — prefer LP path
# Prefer LP = Lanczos of peep L0 if available; else Lanczos of detox parent window
if l0_p3.exists() and L0_p3 is not None:
    LP3 = cv2.resize(L0_p3, (2048, 2048), interpolation=cv2.INTER_LANCZOS4)
else:
    LP3 = cv2.resize(LP2[wy3:wy3 + wh3, wx3:wx3 + ww3], (2048, 2048), interpolation=cv2.INTER_LANCZOS4)

SR8 = cv2.imread(str(ROOT / 'r8_peep3/complete/PEEP3_CHILD_2048_NCNN_FULLRES_R8.png'))
assert SR8 is not None
m8, DET8 = process_job(
    'PEEP3_R8', LP3, SR8,
    COMPLETE / 'PEEP3_CHILD_2048_LUMA_R9.png',
    COMPLETE / 'PROOF_PEEP3_LUMA_R9.jpg',
)
results.append(m8)

# Also detox PEEP3 using parent from DET7b (nested consistency) if L0 was from poisoned board
# Rebuild LP3 from detoxed R7b window for nested chain consistency
LP3_nested = cv2.resize(DET7b[wy3:wy3 + wh3, wx3:wx3 + ww3], (2048, 2048), interpolation=cv2.INTER_LANCZOS4)
# residual source still SR8 relative to original LP3 is wrong; for nested: re-express SR8 HF onto nested LP chrom
# Better: transfer only the luma residual of SR8 vs original LP3 onto nested LP chrom
y_lp3 = to_y(LP3.astype(np.float32))
y_sr8 = to_y(SR8.astype(np.float32))
dy8 = y_sr8 - y_lp3
ratio_n = LP3_nested.astype(np.float32) / (to_y(LP3_nested.astype(np.float32))[..., None] + EPS)
DET8n = np.clip(ratio_n * (to_y(LP3_nested.astype(np.float32)) + dy8)[..., None], 0, 255).astype(np.uint8)
nbytes_n = save_png(COMPLETE / 'PEEP3_CHILD_2048_LUMA_NESTED_R9.png', DET8n)
m8n = dict(
    tag='PEEP3_R8_NESTED',
    child=str(COMPLETE / 'PEEP3_CHILD_2048_LUMA_NESTED_R9.png'),
    child_bytes=nbytes_n,
    note='dY from (SR8−LP3_orig) on chromaticity of DET7b-window LP',
    ten_detox=ten(DET8n),
    blue_detox=blue_stats(DET8n),
    sn_detox=sncc(LP3_nested, DET8n),
)
proof_strip(LP3_nested, SR8, DET8n, ['LP nested', 'R8 poison', 'NESTED luma'],
            COMPLETE / 'PROOF_PEEP3_NESTED_LUMA_R9.jpg')
results.append(m8n)
print(f'  → PEEP3_NESTED ten={m8n["ten_detox"]:.0f} dark={m8n["blue_detox"]["dark_blue_frac"]:.3f}', flush=True)

# Master strip: user-ref style L/R for P0
vis = np.hstack([
    cv2.resize(LP0, (512, 512), interpolation=cv2.INTER_AREA),
    cv2.resize(SR0, (512, 512), interpolation=cv2.INTER_AREA),
    cv2.resize(DET0, (512, 512), interpolation=cv2.INTER_AREA),
])
ban = np.zeros((30, vis.shape[1], 3), np.uint8)
for i, t in enumerate(['LP P0', 'R6c RGB-res POISON', 'R9 LUMA DETOX']):
    cv2.putText(ban, t, (i * 512 + 10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 180), 1)
cv2.imwrite(str(COMPLETE / 'STRIP_P0_CHAIN_R9.jpg'), np.vstack([ban, vis]),
            [int(cv2.IMWRITE_JPEG_QUALITY), 92])

# zoom 400 mesh blotch zone (same as earlier audit)
y1, x1 = 1100, 900
z = np.hstack([
    cv2.resize(LP0[y1:y1 + 256, x1:x1 + 256], (400, 400)),
    cv2.resize(SR0[y1:y1 + 256, x1:x1 + 256], (400, 400)),
    cv2.resize(DET0[y1:y1 + 256, x1:x1 + 256], (400, 400)),
])
banz = np.zeros((26, z.shape[1], 3), np.uint8)
for i, t in enumerate(['LP', 'POISON blue', 'R9 luma']):
    cv2.putText(banz, t, (i * 400 + 10, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 180), 1)
cv2.imwrite(str(COMPLETE / 'ZOOM_P0_BLUE_FIXED_R9.jpg'), np.vstack([banz, z]),
            [int(cv2.IMWRITE_JPEG_QUALITY), 92])

# Accept
accept = dict(
    round='R9_FULLCHAIN_LUMA_ONLY_DETOX',
    constitution='E-BLUE-01..04 · §0.12.56 residual iron',
    formula='Y_out=Y_LP+(Y_SR-Y_LP); RGB=chromaticity(LP)*Y_out',
    iron=['4x residual luma-primary', 'lock LP chroma', 'no full BGR residual paste'],
    jobs=results,
    n_jobs=len(results),
    n_pass=sum(1 for r in results if r.get('PASS')),
    primary_children=[
        'P0_CHILD_2048_LUMA_R9.png',
        'P1_CHILD_2048_LUMA_R9.png',
        'PEEP2_CHILD_4096_RIDGE_LUMA_R9.png',
        'PEEP3_CHILD_2048_LUMA_NESTED_R9.png',
    ],
    status='ACCEPT' if all(r.get('PASS', True) for r in results if 'PASS' in r) else 'PARTIAL',
    asof=datetime.now(timezone.utc).isoformat(),
    elapsed_s=round(time.time() - t_all, 2),
)
(COMPLETE / 'ACCEPT_R9_LUMA.json').write_text(json.dumps(accept, indent=2, ensure_ascii=False))
(OUT / 'LOG_R9.md').write_text(
    '# R9 FULL-CHAIN luma-only detox\n\n'
    f"- status: **{accept['status']}**\n"
    f"- formula: `{accept['formula']}`\n"
    f"- elapsed: {accept['elapsed_s']}s\n"
    f"- jobs: {accept['n_jobs']} · PASS fields: {accept['n_pass']}\n\n"
    '## Jobs\n' +
    '\n'.join(
        f"- **{r.get('tag')}**: dark {r.get('blue_poison',{}).get('dark_blue_frac','—')}→"
        f"{r.get('blue_detox',{}).get('dark_blue_frac','—')} · "
        f"Babs {r.get('chroma_abs_poison',{}).get('absB','—')}→{r.get('chroma_abs_detox',{}).get('absB','—')} · "
        f"ten {r.get('ten_poison','—')}→{r.get('ten_detox','—')} · PASS={r.get('PASS','n/a')}"
        for r in results
    ) + '\n'
)
print(json.dumps({k: accept[k] for k in ('round', 'status', 'n_jobs', 'n_pass', 'elapsed_s', 'primary_children')}, indent=2))
print('DONE R9', COMPLETE)
