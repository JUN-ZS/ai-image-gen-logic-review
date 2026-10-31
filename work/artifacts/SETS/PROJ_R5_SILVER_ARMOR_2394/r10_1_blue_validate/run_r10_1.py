#!/usr/bin/env python3
"""R10.1 · BLUE DETOX — atomic single-runner closed loop (audit-response).

IRON RULES
1. ONE process, ONE job list JOBS, ONE ACCEPT written once at end.
2. ACCEPT.jobs == ROI_REPORT == len(outputs for those jobs) — no post-hoc edit.
3. Dual ROI per board: FIXED_MESH (locked constants) + AUTO_WORST (max |poison-LP|).
4. Nested N1/N2 share the SAME dual ROIs; blue_opp is primary for blue detox ranking.
5. PEEP2 B/C: SKIPPED_OOM (documented job with PASS_FORMAL=null, not silently dropped).
6. Provenance: runner_sha256, input_sha256, output_sha256, all in MANIFEST.
7. merge_main = NO until clean re-download SHA verify passes.

Does NOT upload to GitHub (upload is outer shell after staging).
"""
from __future__ import annotations
import gc, hashlib, json, time
from datetime import datetime, timezone
from pathlib import Path
import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
IN, OUT, ROI_DIR, PREV = HERE / 'inputs', HERE / 'complete', HERE / 'roi', HERE / 'preview'
for d in (OUT, ROI_DIR, PREV):
    d.mkdir(parents=True, exist_ok=True)

EPS = 1e-3
TILE = 768
ROUND = 'R10_1_ATOMIC_CLOSED_LOOP'
RUNNER_NAME = 'run_r10_1.py'

# Locked mesh ROIs (x,y,w,h) — derived once from HF silver on poison, frozen here.
FIXED_MESH_ROI = {
    'P0': (307, 409, 256, 256),
    'P1': (627, 921, 256, 256),
    'PEEP2_R7b': (2534, 1715, 512, 512),
    'PEEP3': (691, 1113, 256, 256),
    'PEEP3_origLP': (691, 1113, 256, 256),
}

# Explicit job plan (what this runner WILL attempt)
JOB_PLAN = [
    ('P0', 'A_luma'),
    ('P0', 'B_material'),
    ('P0', 'C_adaptive'),
    ('P1', 'A_luma'),
    ('P1', 'B_material'),
    ('P1', 'C_adaptive'),
    ('PEEP2_R7b', 'A_luma'),
    ('PEEP2_R7b', 'B_material'),  # becomes SKIPPED_OOM
    ('PEEP2_R7b', 'C_adaptive'),  # becomes SKIPPED_OOM
    ('PEEP3', 'N1_DIRECT'),
    ('PEEP3', 'N2_REBASE'),
    ('PEEP3_origLP', 'A_luma'),
]

REQUIRED_INPUTS = [
    'P0_L0_512.png', 'P0_POISON_2048.png',
    'P1_L0_512.png', 'P1_POISON_2048.png',
    'PEEP2_LP_4096.png', 'PEEP2_POISON_R7b.png',
    'PEEP3_L0_512.jpg', 'PEEP3_POISON_R8.png',
]

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def to_y(bgr):
    b = bgr.astype(np.float32)
    return 0.114 * b[..., 0] + 0.587 * b[..., 1] + 0.299 * b[..., 2]

def crop(img, roi):
    x, y, w, h = roi
    return img[y:y + h, x:x + w]

def auto_worst_roi(lp, poison, bs=256, step=64):
    d = np.abs(poison.astype(np.float32) - lp.astype(np.float32)).mean(axis=2)
    H, W = d.shape
    best, bx, by = -1.0, 0, 0
    for y in range(0, max(1, H - bs + 1), step):
        for x in range(0, max(1, W - bs + 1), step):
            m = float(d[y:y + bs, x:x + bs].mean())
            if m > best:
                best, bx, by = m, x, y
    return (bx, by, min(bs, W - bx), min(bs, H - by)), best

def core_luma(lp, sr):
    lp_f = lp.astype(np.float32)
    y_lp, y_sr = to_y(lp_f), to_y(sr)
    return np.clip((lp_f / (y_lp[..., None] + EPS)) * y_sr[..., None], 0, 255).astype(np.uint8)

def core_material(lp, sr, silver_sat_max=55.0, silver_v_min=40.0, chroma_allow=0.15):
    lp_f, sr_f = lp.astype(np.float32), sr.astype(np.float32)
    y_lp, y_sr = to_y(lp_f), to_y(sr_f)
    hsv = cv2.cvtColor(lp, cv2.COLOR_BGR2HSV)
    S, V = hsv[..., 1].astype(np.float32), hsv[..., 2].astype(np.float32)
    silver = cv2.GaussianBlur(((S <= silver_sat_max) & (V >= silver_v_min)).astype(np.float32), (0, 0), 1.2)
    base = (lp_f / (y_lp[..., None] + EPS)) * y_sr[..., None]
    res = sr_f - lp_f
    res_c = res - to_y(res)[..., None]
    return np.clip(base + res_c * ((1.0 - silver) * chroma_allow)[..., None], 0, 255).astype(np.uint8)

def core_adaptive(lp, sr, k=0.25, thr=3.0):
    lp_f, sr_f = lp.astype(np.float32), sr.astype(np.float32)
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

def tile_map(lp, sr, core):
    H, W = lp.shape[:2]
    if H * W <= 2048 * 2048:
        return core(lp, sr)
    out = np.empty_like(lp)
    for y in range(0, H, TILE):
        for x in range(0, W, TILE):
            y2, x2 = min(y + TILE, H), min(x + TILE, W)
            out[y:y2, x:x2] = core(lp[y:y2, x:x2], sr[y:y2, x:x2])
        print(f'      tile y={y}/{H}', flush=True)
        gc.collect()
    return out

def nested_n1(lp_n, sr8):
    return core_luma(lp_n, sr8)

def nested_n2(lp_n, lp_o, sr8):
    y_n, y_o, y_s = to_y(lp_n), to_y(lp_o), to_y(sr8)
    ratio = lp_n.astype(np.float32) / (y_n[..., None] + EPS)
    return np.clip(ratio * (y_n + (y_s - y_o))[..., None], 0, 255).astype(np.uint8)

def ten(img):
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
    gx = cv2.Sobel(g, cv2.CV_32F, 1, 0, 3)
    gy = cv2.Sobel(g, cv2.CV_32F, 0, 1, 3)
    return float((gx * gx + gy * gy).mean())

def sncc(a, b):
    ga = cv2.GaussianBlur(cv2.cvtColor(a, cv2.COLOR_BGR2GRAY).astype(np.float32), (0, 0), 2.0)
    gb = cv2.GaussianBlur(cv2.cvtColor(b, cv2.COLOR_BGR2GRAY).astype(np.float32), (0, 0), 2.0)
    ga -= ga.mean(); gb -= gb.mean()
    return float((ga * gb).sum() / (np.linalg.norm(ga) * np.linalg.norm(gb) + 1e-8))

def luma_norm(img):
    f = img.astype(np.float32)
    return f / (to_y(f)[..., None] + EPS) * 100.0

def lab_ab_abs_mean(a, b):
    la = cv2.cvtColor(a, cv2.COLOR_BGR2LAB).astype(np.float32)
    lb = cv2.cvtColor(b, cv2.COLOR_BGR2LAB).astype(np.float32)
    return float(np.abs(la[..., 1:] - lb[..., 1:]).mean())

def blue_opp_mean(a, b):
    """Positive blue excess on luma-normalized RGB (B-G, B-R). Not full chroma error."""
    d = luma_norm(b) - luma_norm(a)
    return float((np.maximum(d[..., 0] - d[..., 1], 0) + np.maximum(d[..., 0] - d[..., 2], 0)).mean())

def improve(p, d):
    if p < 1e-6:
        return 0.0 if d < 1e-6 else -100.0
    return round((1 - d / p) * 100, 2)

def metrics_at_roi(lp, poison, detox, roi, roi_kind):
    rlp, rpo, rde = crop(lp, roi), crop(poison, roi), crop(detox, roi)
    ab_p, ab_d = lab_ab_abs_mean(rlp, rpo), lab_ab_abs_mean(rlp, rde)
    bo_p, bo_d = blue_opp_mean(rlp, rpo), blue_opp_mean(rlp, rde)
    ten_p, ten_d = ten(rpo), ten(rde)
    sn_d = sncc(rlp, rde)
    m = dict(
        roi_kind=roi_kind,
        roi=list(roi),
        lab_ab_poison=ab_p, lab_ab_detox=ab_d, lab_ab_improve_pct=improve(ab_p, ab_d),
        blue_opp_poison=bo_p, blue_opp_detox=bo_d, blue_opp_improve_pct=improve(bo_p, bo_d),
        ten_poison=ten_p, ten_detox=ten_d, ten_keep_pct=round(ten_d / max(ten_p, 1e-9) * 100, 2),
        sn_detox=sn_d,
        note_lab='Lab a,b without explicit luminance match — not pure chroma',
        note_blue='positive blue excess only on luma-norm RGB',
    )
    # Formal gates on THIS roi
    m['PASS_lab_ab'] = (ab_d <= ab_p * 0.55) if ab_p >= 1e-6 else (ab_d <= 0.25)
    m['PASS_blue_opp'] = (bo_d <= bo_p * 0.55) if bo_p >= 1e-6 else (bo_d <= 0.5)
    m['PASS_ten'] = m['ten_keep_pct'] >= 92.0
    m['PASS_sn'] = sn_d >= 0.95
    m['PASS_FORMAL'] = all([m['PASS_lab_ab'], m['PASS_blue_opp'], m['PASS_ten'], m['PASS_sn']])
    return m

def dual_metrics(lp, poison, detox, tag):
    mesh = FIXED_MESH_ROI[tag]
    auto, auto_sc = auto_worst_roi(lp, poison, bs=mesh[2])
    m_mesh = metrics_at_roi(lp, poison, detox, mesh, 'FIXED_MESH')
    m_auto = metrics_at_roi(lp, poison, detox, auto, 'AUTO_WORST')
    m_auto['auto_score'] = auto_sc
    # Formal = must pass BOTH ROI kinds (stricter audit)
    formal = bool(m_mesh['PASS_FORMAL'] and m_auto['PASS_FORMAL'])
    return dict(
        dual_roi=dict(FIXED_MESH=m_mesh, AUTO_WORST=m_auto),
        PASS_FORMAL=formal,
        # convenience: report mesh blue as primary blue target
        primary_blue_improve_pct=m_mesh['blue_opp_improve_pct'],
        primary_lab_improve_pct=m_mesh['lab_ab_improve_pct'],
        primary_ten_keep_pct=m_mesh['ten_keep_pct'],
    )

def save_png(path: Path, img) -> dict:
    ok = cv2.imwrite(str(path), img, [cv2.IMWRITE_PNG_COMPRESSION, 3])
    assert ok, path
    return dict(path=str(path), name=path.name, bytes=path.stat().st_size,
                sha256=sha256_file(path), hw=list(img.shape[:2]))

def proof_roi(lp, poison, detox, roi, labels, out_jpg):
    tiles = [cv2.resize(crop(im, roi), (320, 320), interpolation=cv2.INTER_AREA)
             for im in (lp, poison, detox)]
    strip = np.hstack(tiles)
    ban = np.zeros((36, strip.shape[1], 3), np.uint8)
    for i, t in enumerate(labels):
        cv2.putText(ban, t, (i * 320 + 6, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 180), 1)
    cv2.imwrite(str(out_jpg), np.vstack([ban, strip]), [int(cv2.IMWRITE_JPEG_QUALITY), 92])
    return dict(name=out_jpg.name, bytes=out_jpg.stat().st_size, sha256=sha256_file(out_jpg))

def make_detox(name, lp, poison, *, lp_orig=None):
    if name == 'A_luma':
        return tile_map(lp, poison, core_luma)
    if name == 'B_material':
        return core_material(lp, poison) if lp.shape[0] <= 2048 else tile_map(lp, poison, core_material)
    if name == 'C_adaptive':
        return core_adaptive(lp, poison) if lp.shape[0] <= 2048 else tile_map(lp, poison, core_adaptive)
    if name == 'N1_DIRECT':
        return nested_n1(lp, poison)
    if name == 'N2_REBASE':
        assert lp_orig is not None
        return nested_n2(lp, lp_orig, poison)
    raise ValueError(name)

def main():
    t0 = time.time()
    print(f'{ROUND} start', flush=True)
    runner_path = Path(__file__).resolve()
    runner_sha = sha256_file(runner_path)
    runner_src = runner_path.read_bytes()

    missing = [r for r in REQUIRED_INPUTS if not (IN / r).exists()]
    if missing:
        raise SystemExit(f'MISSING inputs: {missing}')

    # wipe outputs once for atomic run
    for d in (OUT, ROI_DIR, PREV):
        for p in d.iterdir():
            if p.is_file():
                p.unlink()

    input_manifest = []
    for p in sorted(IN.iterdir()):
        if p.is_file():
            input_manifest.append(dict(name=p.name, bytes=p.stat().st_size, sha256=sha256_file(p)))

    # Load boards once each as needed
    jobs = []
    roi_proofs = []
    out_files = []

    def record_job(tag, method, lp, poison, det, *, status='OK', skip_reason=None, lp_orig=None, extra=None):
        if status != 'OK':
            job = dict(
                tag=tag, method=method, status=status, skip_reason=skip_reason,
                PASS_FORMAL=None, path=None, sha256=None,
            )
            if extra:
                job.update(extra)
            jobs.append(job)
            print(f'  {tag}/{method} SKIPPED {skip_reason}', flush=True)
            return
        meta = save_png(OUT / f'{tag}_{method}.png', det)
        out_files.append(meta)
        dual = dual_metrics(lp, poison, det, tag)
        # ROI proofs for both
        mesh = FIXED_MESH_ROI[tag]
        auto = dual['dual_roi']['AUTO_WORST']['roi']
        rp1 = proof_roi(lp, poison, det, mesh, ['LP', 'poison', f'{method}/mesh'],
                        ROI_DIR / f'{tag}_{method}_MESH_ROI.jpg')
        rp2 = proof_roi(lp, poison, det, auto, ['LP', 'poison', f'{method}/auto'],
                        ROI_DIR / f'{tag}_{method}_AUTO_ROI.jpg')
        roi_proofs.extend([rp1, rp2])
        job = dict(tag=tag, method=method, status='OK', **meta, **dual)
        if extra:
            job.update(extra)
        if method in ('N1_DIRECT', 'N2_REBASE'):
            job['formula'] = (
                'Y_out=Y_SR8; chrom(LP_nested)' if method == 'N1_DIRECT'
                else 'Y_out=Y_LP_nested+(Y_SR8-Y_LP_orig); chrom(LP_nested)'
            )
        jobs.append(job)
        m = dual['dual_roi']['FIXED_MESH']
        print(
            f"  {tag}/{method} FORMAL={dual['PASS_FORMAL']} "
            f"mesh_lab↑{m['lab_ab_improve_pct']}% mesh_blue↑{m['blue_opp_improve_pct']}% "
            f"auto_blue↑{dual['dual_roi']['AUTO_WORST']['blue_opp_improve_pct']}%",
            flush=True,
        )
        del det
        gc.collect()

    # --- P0 ---
    lp0 = cv2.resize(cv2.imread(str(IN / 'P0_L0_512.png')), (2048, 2048), interpolation=cv2.INTER_LANCZOS4)
    po0 = cv2.imread(str(IN / 'P0_POISON_2048.png'))
    out_files.append(save_png(OUT / 'P0_LP_2048.png', lp0))
    for method in ('A_luma', 'B_material', 'C_adaptive'):
        det = make_detox(method, lp0, po0)
        record_job('P0', method, lp0, po0, det)
    del lp0, po0; gc.collect()

    # --- P1 ---
    lp1 = cv2.resize(cv2.imread(str(IN / 'P1_L0_512.png')), (2048, 2048), interpolation=cv2.INTER_LANCZOS4)
    po1 = cv2.imread(str(IN / 'P1_POISON_2048.png'))
    out_files.append(save_png(OUT / 'P1_LP_2048.png', lp1))
    for method in ('A_luma', 'B_material', 'C_adaptive'):
        det = make_detox(method, lp1, po1)
        record_job('P1', method, lp1, po1, det)
    del lp1, po1; gc.collect()

    # --- PEEP2 ---
    lp2 = cv2.imread(str(IN / 'PEEP2_LP_4096.png'))
    po2 = cv2.imread(str(IN / 'PEEP2_POISON_R7b.png'))
    # A full
    det = make_detox('A_luma', lp2, po2)
    record_job('PEEP2_R7b', 'A_luma', lp2, po2, det)
    # B/C skipped OOM (honest)
    record_job('PEEP2_R7b', 'B_material', lp2, po2, None,
               status='SKIPPED_OOM',
               skip_reason='full 4096 B/C float32 peak exceeds 1.9GB host; not ROI-paste substitute')
    record_job('PEEP2_R7b', 'C_adaptive', lp2, po2, None,
               status='SKIPPED_OOM',
               skip_reason='full 4096 B/C float32 peak exceeds 1.9GB host; not ROI-paste substitute')

    # nested parent from A_luma on disk
    det2 = cv2.imread(str(OUT / 'PEEP2_R7b_A_luma.png'))
    wx, wy, ww, wh = 2276, 28, 512, 512  # peep3 window on peep2 — documented constant
    lp3_nested = cv2.resize(det2[wy:wy + wh, wx:wx + ww], (2048, 2048), interpolation=cv2.INTER_LANCZOS4)
    del det2, lp2, po2; gc.collect()

    lp3_orig = cv2.resize(cv2.imread(str(IN / 'PEEP3_L0_512.jpg')), (2048, 2048), interpolation=cv2.INTER_LANCZOS4)
    sr8 = cv2.imread(str(IN / 'PEEP3_POISON_R8.png'))
    out_files.append(save_png(OUT / 'PEEP3_LP_nested_2048.png', lp3_nested))
    out_files.append(save_png(OUT / 'PEEP3_LP_orig_2048.png', lp3_orig))

    for method in ('N1_DIRECT', 'N2_REBASE'):
        det = make_detox(method, lp3_nested, sr8, lp_orig=lp3_orig)
        record_job('PEEP3', method, lp3_nested, sr8, det, lp_orig=lp3_orig)

    det = make_detox('A_luma', lp3_orig, sr8)
    record_job('PEEP3_origLP', 'A_luma', lp3_orig, sr8, det)
    del lp3_orig, sr8, lp3_nested; gc.collect()

    # consistency check: jobs vs plan
    assert len(jobs) == len(JOB_PLAN), (len(jobs), len(JOB_PLAN))
    for j, (t, m) in zip(jobs, JOB_PLAN):
        assert j['tag'] == t and j['method'] == m, (j['tag'], j['method'], t, m)

    n_ok = sum(1 for j in jobs if j['status'] == 'OK')
    n_formal = sum(1 for j in jobs if j.get('PASS_FORMAL') is True)
    n_skip = sum(1 for j in jobs if j['status'] != 'OK')

    # Champions: Lab vs Blue separate (mesh ROI primary)
    def champ(metric_key):
        best = {}
        for j in jobs:
            if j['status'] != 'OK':
                continue
            tag = j['tag']
            v = j['dual_roi']['FIXED_MESH'][metric_key]
            # higher improve better for improve_pct; for residual would invert
            if tag not in best or v > best[tag]['value']:
                best[tag] = dict(method=j['method'], value=v, PASS_FORMAL=j['PASS_FORMAL'],
                                 path=j.get('path'), sha256=j.get('sha256'))
        return best

    champions_lab = champ('lab_ab_improve_pct')
    champions_blue = champ('blue_opp_improve_pct')

    # Nested head-to-head on SAME mesh ROI
    nested = {}
    for j in jobs:
        if j['tag'] == 'PEEP3' and j['status'] == 'OK':
            nested[j['method']] = dict(
                lab_ab_improve_pct=j['dual_roi']['FIXED_MESH']['lab_ab_improve_pct'],
                blue_opp_improve_pct=j['dual_roi']['FIXED_MESH']['blue_opp_improve_pct'],
                blue_opp_detox=j['dual_roi']['FIXED_MESH']['blue_opp_detox'],
                ten_keep_pct=j['dual_roi']['FIXED_MESH']['ten_keep_pct'],
                PASS_FORMAL=j['PASS_FORMAL'],
            )
    nested_pick = dict(
        lab_champion='N2_REBASE' if nested.get('N2_REBASE', {}).get('lab_ab_improve_pct', -1) >= nested.get('N1_DIRECT', {}).get('lab_ab_improve_pct', -1) else 'N1_DIRECT',
        blue_champion='N1_DIRECT' if nested.get('N1_DIRECT', {}).get('blue_opp_improve_pct', -1) >= nested.get('N2_REBASE', {}).get('blue_opp_improve_pct', -1) else 'N2_REBASE',
        note='blue detox primary = FIXED_MESH blue_opp; Lab secondary',
        detail=nested,
    )

    accept = dict(
        round=ROUND,
        audit_response=[
            'single runner atomic ACCEPT once',
            'JOB_PLAN length == jobs length',
            'dual ROI FIXED_MESH + AUTO_WORST',
            'PEEP2 B/C explicit SKIPPED_OOM not silent drop',
            'N1/N2 dual champions lab vs blue',
            'no GitHub upload inside runner',
            'merge_main NO',
        ],
        runner=dict(path=str(runner_path), name=RUNNER_NAME, sha256=runner_sha, bytes=len(runner_src)),
        formulas={
            'A_luma': 'Y_out=Y_SR; RGB=chrom(LP)*Y_SR',
            'B_material': 'A+(1-silver)*0.15*chroma_residual',
            'C_adaptive': 'A+allow*chroma; kill blue-excess residual',
            'N1_DIRECT': 'Y_out=Y_SR8; chrom(LP_nested)',
            'N2_REBASE': 'Y_out=Y_LP_nested+(Y_SR8-Y_LP_orig); chrom(LP_nested)',
        },
        fixed_mesh_roi=FIXED_MESH_ROI,
        peep3_window_on_peep2=[2276, 28, 512, 512],
        job_plan=[{'tag': t, 'method': m} for t, m in JOB_PLAN],
        metrics_formal=['FIXED_MESH and AUTO_WORST both: lab_ab, blue_opp, ten, sn'],
        metrics_notes=[
            'Lab a,b without luminance match — not pure chroma',
            'blue_opp = positive blue excess on luma-norm RGB only',
            'AUTO_WORST = max mean |poison-LP| block (stress), not pre-locked mesh',
        ],
        input_manifest=input_manifest,
        output_pngs=out_files,
        roi_proofs=roi_proofs,
        jobs=jobs,
        n_jobs=len(jobs),
        n_ok=n_ok,
        n_skip=n_skip,
        n_pass_formal=n_formal,
        champions_lab_mesh=champions_lab,
        champions_blue_mesh=champions_blue,
        nested_head_to_head=nested_pick,
        status='PARTIAL' if (n_formal < n_ok or n_skip) else 'ALL_FORMAL',
        merge_main='NO',
        asof=datetime.now(timezone.utc).isoformat(),
        elapsed_s=round(time.time() - t0, 2),
    )

    # Write ALL reports once
    acc_path = OUT / 'ACCEPT_R10_1.json'
    acc_path.write_text(json.dumps(accept, indent=2, ensure_ascii=False))
    # root mirror identical bytes
    (HERE / 'ACCEPT_R10_1.json').write_text(acc_path.read_text())

    roi_report = []
    for j in jobs:
        row = dict(tag=j['tag'], method=j['method'], status=j['status'], PASS_FORMAL=j.get('PASS_FORMAL'))
        if j['status'] == 'OK':
            row['mesh'] = j['dual_roi']['FIXED_MESH']
            row['auto'] = j['dual_roi']['AUTO_WORST']
            row['path'] = j.get('path')
            row['sha256'] = j.get('sha256')
        else:
            row['skip_reason'] = j.get('skip_reason')
        roi_report.append(row)
    (OUT / 'ROI_REPORT_R10_1.json').write_text(json.dumps(roi_report, indent=2, ensure_ascii=False))

    manifest = dict(
        round=ROUND,
        runner_sha256=runner_sha,
        runner_name=RUNNER_NAME,
        accept_sha256=sha256_file(acc_path),
        inputs=input_manifest,
        outputs_png=out_files,
        roi_jpgs=roi_proofs,
        job_plan=[{'tag': t, 'method': m} for t, m in JOB_PLAN],
        n_jobs=len(jobs),
        asof=accept['asof'],
    )
    (OUT / 'MANIFEST_SHA256_R10_1.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False))

    log = [
        f'# {ROUND}',
        '',
        f'- status: **{accept["status"]}** formal {n_formal}/{n_ok} ok · skip {n_skip}',
        f'- runner sha256: `{runner_sha}`',
        f'- accept sha256: `{manifest["accept_sha256"]}`',
        f'- jobs: {len(jobs)} == JOB_PLAN (locked)',
        f'- dual ROI: FIXED_MESH + AUTO_WORST',
        f'- merge main: **NO**',
        f'- elapsed: {accept["elapsed_s"]}s',
        '',
        '## Nested head-to-head (same FIXED_MESH ROI)',
        f'- Lab champion: **{nested_pick["lab_champion"]}**',
        f'- Blue champion: **{nested_pick["blue_champion"]}**',
        '',
        '## Champions (mesh Lab)',
    ]
    for k, v in champions_lab.items():
        log.append(f'- {k}: {v["method"]} lab↑{v["value"]}% FORMAL={v["PASS_FORMAL"]}')
    log += ['', '## Champions (mesh Blue)']
    for k, v in champions_blue.items():
        log.append(f'- {k}: {v["method"]} blue↑{v["value"]}% FORMAL={v["PASS_FORMAL"]}')
    log += ['', '## Skips']
    for j in jobs:
        if j['status'] != 'OK':
            log.append(f'- {j["tag"]}/{j["method"]}: {j["skip_reason"]}')
    (HERE / 'LOG_R10_1.md').write_text('\n'.join(log) + '\n')
    (OUT / 'LOG_R10_1.md').write_text('\n'.join(log) + '\n')

    # self-check: root ACCEPT == complete ACCEPT
    assert (HERE / 'ACCEPT_R10_1.json').read_bytes() == acc_path.read_bytes()
    assert len(jobs) == len(JOB_PLAN)

    summary = dict(
        status=accept['status'],
        n_jobs=len(jobs), n_ok=n_ok, n_skip=n_skip, n_pass_formal=n_formal,
        nested=nested_pick,
        runner_sha256=runner_sha,
        accept_sha256=manifest['accept_sha256'],
        elapsed_s=accept['elapsed_s'],
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print('DONE R10.1', OUT)

if __name__ == '__main__':
    main()
