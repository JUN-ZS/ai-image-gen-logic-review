#!/usr/bin/env python3
"""R7 · ② PEEP2 1024→4096 FULL-RES · NCNN GENERAL · memmap STREAM · tiled fuse
Iron: 4× MODEL → 4× residual/child · no downscale primary · register on P0-2048
"""
from __future__ import annotations
import gc, json, time
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import cv2
import ncnn

P0 = Path("/workspace/artifacts/SETS/PROJ_R5_SILVER_ARMOR_2394/r6c/complete/P0_CHILD_2048_NCNN_PBI_R6c.png")
P0_FALLBACK = Path("/workspace/artifacts/SETS/PROJ_R5_SILVER_ARMOR_2394/r6c/complete/P0_CHILD_2048_NCNN_GENERAL_R6c.png")
PARAM = Path("/workspace/artifacts/artifacts/sr_contest/general_x4v3.ncnn.param")
BIN = Path("/workspace/artifacts/artifacts/sr_contest/general_x4v3.ncnn.bin")
OUT = Path("/workspace/artifacts/SETS/PROJ_R5_SILVER_ARMOR_2394/r7_peep2")
COMP = OUT / "complete"
BENCH = OUT / "bench"
PEEP = OUT / "peep"
for d in (COMP, BENCH, PEEP):
    d.mkdir(parents=True, exist_ok=True)

TILE, S, GAIN = 64, 4, 1.10
# PBI default: PREVENT BLUE INJECTION
PBI_MODE = "luma_only"  # "luma_only" | "legacy_rgb"
# GitHub path (this branch): work/scripts/r6c_pbi/run_r7_peep2_final.py
REPO_SCRIPT = "work/scripts/r6c_pbi/run_r7_peep2_final.py"
PBI_DOC = "hyb = C(LP)×(Y_LP + ridge(dY)); multi_sigma on Y only"

def to_y_bgr(bgr):
    f = bgr.astype(np.float32)
    return 0.114 * f[..., 0] + 0.587 * f[..., 1] + 0.299 * f[..., 2]

def chrom_bgr(bgr, y=None):
    f = bgr.astype(np.float32)
    if y is None:
        y = to_y_bgr(f)
    return f / (y[..., None] + 1e-3)

def multi_sigma_fill_y(res_y, weight, sigmas=(4, 8, 16)):
    filled = np.zeros_like(res_y, dtype=np.float32)
    wacc = np.zeros(weight.shape, np.float32)
    for s in sigmas:
        filled += cv2.GaussianBlur(res_y, (0, 0), s)
        wacc += cv2.GaussianBlur(weight, (0, 0), s)
    filled /= np.maximum(wacc, 1e-6)
    m = (weight > 0.15).astype(np.float32)
    return res_y * m + filled * (1.0 - m)

def ridge_hard_y(residual_y, parent_hd, thr_k=0.35, dil=3):
    g = cv2.cvtColor(parent_hd, cv2.COLOR_BGR2GRAY).astype(np.float32)
    gx = cv2.Sobel(g, cv2.CV_32F, 1, 0, 3)
    gy = cv2.Sobel(g, cv2.CV_32F, 0, 1, 3)
    mag = cv2.magnitude(gx, gy)
    thr = float(mag.mean() + thr_k * mag.std())
    hard = (mag > thr).astype(np.uint8)
    hard = cv2.dilate(hard, np.ones((2 * dil + 1, 2 * dil + 1), np.uint8), 1)
    inv = (1 - hard).astype(np.uint8)
    dist = cv2.distanceTransform(inv, cv2.DIST_L2, 3)
    soft = np.maximum(hard.astype(np.float32), np.exp(-(dist ** 2) / (2 * 2.2 ** 2)) * (1 - hard))
    soft = np.clip(cv2.GaussianBlur(soft, (0, 0), 1.2), 0, 1)
    cell = (mag < mag.mean() * 0.55).astype(np.float32)
    cell = cv2.erode(cell, np.ones((3, 3), np.uint8), 1)
    gate = np.clip(soft * (1 - 0.85 * cell * (1 - soft)), 0, 1)
    gate_p = np.power(gate, 0.65)
    res_h = residual_y * gate_p * (1.0 + 0.25 * hard.astype(np.float32))
    rmag = np.abs(res_h)
    align = float((rmag * soft).sum() / (rmag.sum() + 1e-8))
    spill = float((rmag * (1 - soft)).sum() / (rmag.sum() + 1e-8))
    return res_h, align, spill

PARENT, CHILD = 1024, 4096
NPROBE = 48
TS = 512  # tile size for fuse

def load_ncnn(th=2):
    net = ncnn.Net()
    net.opt.use_vulkan_compute = False
    net.opt.num_threads = th
    net.load_param(str(PARAM))
    net.load_model(str(BIN))
    return net

def ncnn_4x(net, bgr):
    h, w = bgr.shape[:2]
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    mat = ncnn.Mat.from_pixels(rgb, ncnn.Mat.PixelType.PIXEL_RGB, w, h)
    mat.substract_mean_normalize([0, 0, 0], [1 / 255.0] * 3)
    ex = net.create_extractor()
    assert ex.input("in0", mat) == 0
    ret, mo = ex.extract("out0")
    assert ret == 0
    arr = np.array(mo)
    out = arr.transpose(1, 2, 0) if arr.shape[0] == 3 else arr.reshape(3, h * 4, w * 4).transpose(1, 2, 0)
    out = np.clip(out, 0, 1)
    return cv2.cvtColor((out * 255).round().astype(np.uint8), cv2.COLOR_RGB2BGR)

def tenengrad(img):
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
    gx = cv2.Sobel(g, cv2.CV_32F, 1, 0, 3)
    gy = cv2.Sobel(g, cv2.CV_32F, 0, 1, 3)
    return float((gx * gx + gy * gy).mean())

def struct_ncc(a, b):
    ga = cv2.GaussianBlur(cv2.cvtColor(a, cv2.COLOR_BGR2GRAY).astype(np.float32), (0, 0), 2)
    gb = cv2.GaussianBlur(cv2.cvtColor(b, cv2.COLOR_BGR2GRAY).astype(np.float32), (0, 0), 2)
    ga = cv2.resize(ga, (max(1, ga.shape[1] // 2), max(1, ga.shape[0] // 2)), interpolation=cv2.INTER_AREA)
    gb = cv2.resize(gb, (ga.shape[1], ga.shape[0]), interpolation=cv2.INTER_AREA)
    aa, bb = ga - ga.mean(), gb - gb.mean()
    return float((aa * bb).sum() / ((np.linalg.norm(aa) * np.linalg.norm(bb)) + 1e-8))

def pick_probes(L0, tile=64, target=48, min_step=24):
    g = cv2.cvtColor(L0, cv2.COLOR_BGR2GRAY).astype(np.float32)
    gx = cv2.Sobel(g, cv2.CV_32F, 1, 0, 3)
    gy = cv2.Sobel(g, cv2.CV_32F, 0, 1, 3)
    mag = cv2.magnitude(gx, gy)
    k = np.ones((tile, tile), np.float32) / (tile * tile)
    energy = cv2.filter2D(mag, -1, k)
    h, w = g.shape
    cands = []
    for y in range(0, h - tile + 1, min_step):
        for x in range(0, w - tile + 1, min_step):
            cands.append((float(energy[y + tile // 2, x + tile // 2]), y, x))
    cands.sort(reverse=True)
    chosen, occ = [], np.zeros((h, w), np.float32)
    for e, y, x in cands:
        if len(chosen) >= target:
            break
        if float(occ[y:y + tile, x:x + tile].mean()) < 0.35:
            chosen.append((y, x))
            occ[y:y + tile, x:x + tile] += 1
    return chosen

def multi_sigma_fill(res, weight, sigmas=(4, 8, 16)):
    filled = np.zeros_like(res)
    wacc = np.zeros(weight.shape, np.float32)
    for s in sigmas:
        for c in range(3):
            filled[:, :, c] += cv2.GaussianBlur(res[:, :, c], (0, 0), s)
        wacc += cv2.GaussianBlur(weight, (0, 0), s)
    filled /= np.maximum(wacc[:, :, None], 1e-6)
    m = (weight > 0.15).astype(np.float32)[:, :, None]
    return res * m + filled * (1 - m)

def ridge_hard(residual, parent_hd, thr_k=0.35, dil=3):
    g = cv2.cvtColor(parent_hd, cv2.COLOR_BGR2GRAY).astype(np.float32)
    gx = cv2.Sobel(g, cv2.CV_32F, 1, 0, 3)
    gy = cv2.Sobel(g, cv2.CV_32F, 0, 1, 3)
    mag = cv2.magnitude(gx, gy)
    thr = float(mag.mean() + thr_k * mag.std())
    hard = (mag > thr).astype(np.uint8)
    hard = cv2.dilate(hard, np.ones((2 * dil + 1, 2 * dil + 1), np.uint8), 1)
    inv = (1 - hard).astype(np.uint8)
    dist = cv2.distanceTransform(inv, cv2.DIST_L2, 3)
    soft = np.maximum(hard.astype(np.float32), np.exp(-(dist ** 2) / (2 * 2.2 ** 2)) * (1 - hard))
    soft = np.clip(cv2.GaussianBlur(soft, (0, 0), 1.2), 0, 1)
    cell = (mag < mag.mean() * 0.55).astype(np.float32)
    cell = cv2.erode(cell, np.ones((3, 3), np.uint8), 1)
    gate = np.clip(soft * (1 - 0.85 * cell * (1 - soft)), 0, 1)
    gate_p = np.power(gate, 0.65)
    res_h = residual * gate_p[:, :, None] * (1.0 + 0.25 * hard.astype(np.float32))[:, :, None]
    rmag = np.linalg.norm(res_h, axis=2)
    align = float((rmag * soft).sum() / (rmag.sum() + 1e-8))
    spill = float((rmag * (1 - soft)).sum() / (rmag.sum() + 1e-8))
    return res_h, align, spill

def main():
    t_all = time.time()
    print("R7 PEEP2 1024→4096 FULL-RES STREAM", flush=True)
    p0_path = P0 if P0.is_file() else P0_FALLBACK
    print(f"P0 parent: {p0_path.name} exists={p0_path.is_file()}", flush=True)
    board = cv2.imread(str(p0_path))
    assert board is not None and board.shape[0] == 2048, board.shape if board is not None else None

    g = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY).astype(np.float32)
    gx = cv2.Sobel(g, cv2.CV_32F, 1, 0, 3)
    gy = cv2.Sobel(g, cv2.CV_32F, 0, 1, 3)
    mag = cv2.magnitude(gx, gy)
    k = np.ones((PARENT, PARENT), np.float32) / (PARENT * PARENT)
    energy = cv2.filter2D(mag, -1, k)
    margin = PARENT // 2 + 4
    e = energy.copy()
    e[:margin, :] = 0
    e[-margin:, :] = 0
    e[:, :margin] = 0
    e[:, -margin:] = 0
    y, x = np.unravel_index(np.argmax(e), e.shape)
    y0 = max(0, min(board.shape[0] - PARENT, int(y) - PARENT // 2))
    x0 = max(0, min(board.shape[1] - PARENT, int(x) - PARENT // 2))
    score = float(energy[int(y), int(x)])
    print(f"PEEP2 window on P0-2048: xy=({x0},{y0}) score={score:.1f}", flush=True)

    L0 = board[y0:y0 + PARENT, x0:x0 + PARENT].copy()
    del board, g, gx, gy, mag, energy, e
    gc.collect()
    cv2.imwrite(str(PEEP / "PEEP2_L0_1024.jpg"), L0, [int(cv2.IMWRITE_JPEG_QUALITY), 92])

    manifest = dict(
        parent_of="R6c_P0_CHILD_2048",
        window_on_2048=[x0, y0, 1024, 1024],
        mother_peep0_xy=[300, 693],
        mother_window_approx=[300 + x0 // 4, 693 + y0 // 4, 256, 256],
        scale_chain="mother⊂512 peep → 2048 board → 1024 PEEP2 → 4096 child (×4 FULLRES)",
        register=dict(board_xy=[x0, y0], peep=1024, child_hw=4096, scale=4, relative_to="P0_2048"),
        iron="4x_MODEL_to_4x_CHILD · primary=4096 PNG · no AREA kill",
    )
    (COMP / "TRANSFORM_PEEP2.json").write_text(json.dumps(manifest, indent=2))

    print("  LP Lanczos 1024→4096…", flush=True)
    # write LP as uint8 PNG (avoid keeping float LP in RAM)
    LP_u8 = cv2.resize(L0, (CHILD, CHILD), interpolation=cv2.INTER_LANCZOS4)
    lp_path = PEEP / "LP_4096.png"
    cv2.imwrite(str(lp_path), LP_u8, [cv2.IMWRITE_PNG_COMPRESSION, 1])
    ten_lp = tenengrad(LP_u8)
    del LP_u8
    gc.collect()

    # memmap Y residual + weight (PBI: no RGB residual stack)
    res_path = str(BENCH / "res_y_acc.dat")
    w_path = str(BENCH / "w_acc.dat")
    res_y_acc = np.memmap(res_path, dtype=np.float32, mode="w+", shape=(CHILD, CHILD))
    w_acc = np.memmap(w_path, dtype=np.float32, mode="w+", shape=(CHILD, CHILD))
    res_y_acc[:] = 0
    w_acc[:] = 0

    yy, xx = np.mgrid[0:TILE, 0:TILE]
    c = (TILE - 1) / 2.0
    gw = np.exp(-((yy - c) ** 2 + (xx - c) ** 2) / (2 * (TILE * 0.28) ** 2)).astype(np.float32)
    gw2 = cv2.resize(gw, (TILE * S, TILE * S), interpolation=cv2.INTER_LINEAR)

    net = load_ncnn(2)
    probes = pick_probes(L0, TILE, NPROBE, min_step=24)
    print(f"  probes {len(probes)} · NCNN FULLRES · PBI_MODE={PBI_MODE}", flush=True)
    t0 = time.time()
    for i, (py, px) in enumerate(probes):
        tile = L0[py:py + TILE, px:px + TILE]
        sr = ncnn_4x(net, tile).astype(np.float32)
        lp = cv2.resize(tile, (TILE * S, TILE * S), interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
        dy = to_y_bgr(sr) - to_y_bgr(lp)
        del sr, lp
        Y, X = py * S, px * S
        res_y_acc[Y:Y + TILE * S, X:X + TILE * S] += dy * gw2
        w_acc[Y:Y + TILE * S, X:X + TILE * S] += gw2
        del dy
        if (i + 1) % 8 == 0:
            res_y_acc.flush()
            w_acc.flush()
            print(f"    {i+1}/{len(probes)}", flush=True)
            gc.collect()
    infer_s = time.time() - t0
    res_y_acc.flush()
    w_acc.flush()
    print(f"  infer {infer_s:.1f}s", flush=True)

    print("  normalize dY residual tiled…", flush=True)
    for y0t in range(0, CHILD, TS):
        for x0t in range(0, CHILD, TS):
            y1, x1 = min(CHILD, y0t + TS), min(CHILD, x0t + TS)
            ww = np.maximum(np.array(w_acc[y0t:y1, x0t:x1], dtype=np.float32), 1e-6)
            chunk = np.array(res_y_acc[y0t:y1, x0t:x1], dtype=np.float32)
            res_y_acc[y0t:y1, x0t:x1] = chunk / ww
            del ww, chunk
        res_y_acc.flush()
        gc.collect()

    print("  multi-sigma fill Y-only + M → residual_y_new…", flush=True)
    rnew_path = str(BENCH / "res_y_new.dat")
    residual_y_new = np.memmap(rnew_path, dtype=np.float32, mode="w+", shape=(CHILD, CHILD))
    wmax = float(np.percentile(np.array(w_acc[::16, ::16], dtype=np.float32), 99)) + 1e-6
    for y0t in range(0, CHILD, TS):
        for x0t in range(0, CHILD, TS):
            y1, x1 = min(CHILD, y0t + TS), min(CHILD, x0t + TS)
            pad = 48
            ya, yb = max(0, y0t - pad), min(CHILD, y1 + pad)
            xa, xb = max(0, x0t - pad), min(CHILD, x1 + pad)
            res_p = np.array(res_y_acc[ya:yb, xa:xb], dtype=np.float32)
            w_p = np.array(w_acc[ya:yb, xa:xb], dtype=np.float32)
            filled = multi_sigma_fill_y(res_p, w_p)
            mag = np.abs(filled)
            rough = (mag > (mag.mean() + 0.5 * mag.std())).astype(np.float32)
            M = np.clip(w_p / wmax, 0, 1)
            M = np.clip(M + 0.85 * rough * 0.5, 0, 1)
            out = filled * M * GAIN
            cy0, cx0 = y0t - ya, x0t - xa
            residual_y_new[y0t:y1, x0t:x1] = out[cy0:cy0 + (y1 - y0t), cx0:cx0 + (x1 - x0t)]
            del res_p, w_p, filled, mag, rough, M, out
        residual_y_new.flush()
        gc.collect()
        print(f"    fill row y={y0t}", flush=True)

    del res_y_acc
    try:
        Path(res_path).unlink(missing_ok=True)
    except Exception:
        pass
    del w_acc
    try:
        Path(w_path).unlink(missing_ok=True)
    except Exception:
        pass
    gc.collect()

    print("  ridge Y + PBI chrom lock fuse tiled…", flush=True)
    LP_full = cv2.imread(str(lp_path))
    assert LP_full is not None
    # Start from LP; apply dY with locked chrom per tile
    hyb_u8 = LP_full.copy()
    del LP_full
    gc.collect()

    align_acc = spill_acc = weight_acc = 0.0
    for y0t in range(0, CHILD, TS):
        for x0t in range(0, CHILD, TS):
            y1, x1 = min(CHILD, y0t + TS), min(CHILD, x0t + TS)
            pad = 8
            ya, yb = max(0, y0t - pad), min(CHILD, y1 + pad)
            xa, xb = max(0, x0t - pad), min(CHILD, x1 + pad)
            parent_p = hyb_u8[ya:yb, xa:xb].copy()  # LP chrom base
            res_p = np.array(residual_y_new[ya:yb, xa:xb], dtype=np.float32)
            res_h_y, al, sp = ridge_hard_y(res_p, parent_p, 0.35, 3)
            cy0, cx0 = y0t - ya, x0t - xa
            dy_add = res_h_y[cy0:cy0 + (y1 - y0t), cx0:cx0 + (x1 - x0t)]
            base = hyb_u8[y0t:y1, x0t:x1].astype(np.float32)
            y_lp = to_y_bgr(base)
            y_out = y_lp + dy_add
            hyb_u8[y0t:y1, x0t:x1] = np.clip(chrom_bgr(base, y_lp) * y_out[..., None], 0, 255).astype(np.uint8)
            area = (y1 - y0t) * (x1 - x0t)
            align_acc += al * area
            spill_acc += sp * area
            weight_acc += area
            del parent_p, res_p, res_h_y, dy_add, base, y_lp, y_out
        gc.collect()
        print(f"    fuse row y={y0t}", flush=True)

    del residual_y_new
    try:
        Path(rnew_path).unlink(missing_ok=True)
    except Exception:
        pass
    gc.collect()

    align = align_acc / max(weight_acc, 1)
    spill = spill_acc / max(weight_acc, 1)
    # struct vs LP reload
    LP_cmp = cv2.imread(str(lp_path))
    ten = tenengrad(hyb_u8)
    sn = struct_ncc(LP_cmp, hyb_u8)
    ten_lp = tenengrad(LP_cmp)
    del LP_cmp
    gc.collect()

    path = COMP / "PEEP2_CHILD_4096_NCNN_PBI_R7.png"
    print("  write PNG…", flush=True)
    cv2.imwrite(str(path), hyb_u8, [cv2.IMWRITE_PNG_COMPRESSION, 3])
    print(f"  wrote {path.stat().st_size/1e6:.1f} MB · align={align:.3f} sn={sn:.3f} ten={ten:.0f}", flush=True)

    # proofs
    prev = cv2.resize(hyb_u8, (1024, 1024), interpolation=cv2.INTER_AREA)
    cv2.imwrite(str(COMP / "PEEP2_CHILD_4096_PREVIEW_1024.jpg"), prev, [int(cv2.IMWRITE_JPEG_QUALITY), 92])

    L0_show = cv2.resize(L0, (512, 512), interpolation=cv2.INTER_AREA)
    lp_show = cv2.imread(str(lp_path))
    lp_show = cv2.resize(lp_show, (512, 512), interpolation=cv2.INTER_AREA) if lp_show is not None else L0_show
    ch_show = cv2.resize(hyb_u8, (512, 512), interpolation=cv2.INTER_AREA)
    strip = np.hstack([L0_show, lp_show, ch_show])
    ban = np.zeros((28, strip.shape[1], 3), np.uint8)
    cv2.putText(ban, f"R7 PEEP2 L0|LP|4096 align {align:.3f} sn {sn:.3f} ten {ten:.0f} PNG {path.stat().st_size//1024}KB",
                (6, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 255, 180), 1, cv2.LINE_AA)
    cv2.imwrite(str(COMP / "PROOF_PEEP2_R7.jpg"), np.vstack([ban, strip]), [int(cv2.IMWRITE_JPEG_QUALITY), 92])

    # zoom: native 512 crop from 4096 vs L0 nearest
    c = CHILD // 2
    zc = hyb_u8[c - 256:c + 256, c - 256:c + 256]
    z0 = L0[c // 4 - 64:c // 4 + 64, c // 4 - 64:c // 4 + 64]
    zstrip = np.hstack([
        cv2.resize(z0, (512, 512), interpolation=cv2.INTER_NEAREST),
        zc,
    ])
    ban2 = np.zeros((24, zstrip.shape[1], 3), np.uint8)
    cv2.putText(ban2, "L0 NEAREST x4 vs R7 native 512 crop (same FOV)", (6, 16),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 180), 1, cv2.LINE_AA)
    cv2.imwrite(str(COMP / "ZOOM_L0_vs_R7_NATIVE.jpg"), np.vstack([ban2, zstrip]), [int(cv2.IMWRITE_JPEG_QUALITY), 92])
    cv2.imwrite(str(COMP / "ZOOM400_PEEP2_CENTER.png"), zc, [cv2.IMWRITE_PNG_COMPRESSION, 3])

    ok = bool(align >= 0.65 and sn >= 0.97 and hyb_u8.shape[0] == 4096)
    accept = dict(
        round="R7_PEEP2_1024_to_4096_PBI_LUMA",
        option=2,
        constitution="§0.12.56 + NCPG nested peep",
        peep2=dict(
            window_on_p0_2048=[x0, y0, 1024, 1024],
            score=score,
            child=str(path),
            child_bytes=path.stat().st_size,
            child_hw=4096,
            align=align,
            spill=spill,
            sn=sn,
            ten=ten,
            ten_lp=ten_lp,
            n_probes=len(probes),
            infer_s=round(infer_s, 2),
            engine="NCNN_GENERAL_x4v3_PBI_LUMA",
            iron="4x residual Y-only PBI · primary lossless PNG", pbi_mode=PBI_MODE, pbi=PBI_DOC,
        ),
        register=manifest["register"],
        PASS=ok,
        status="ACCEPT" if ok else "PARTIAL",
        asof=datetime.now(timezone.utc).isoformat(),
        elapsed_s=round(time.time() - t_all, 2),
    )
    (COMP / "ACCEPT_R7_PBI.json").write_text(json.dumps(accept, indent=2, ensure_ascii=False))
    (OUT / "LOG_R7_PBI.md").write_text(f"""# R7 · ② PEEP2 更細 1024→4096

## 鐵序
P0 2048 高能窗 1024 → NCNN 4× residual → **4096 原生子板**（禁縮回 1024 當主）

## 結果
- window on P0: ({x0},{y0})
- align **{align:.3f}** · sn **{sn:.3f}** · ten {ten:.0f} (LP {ten_lp:.0f})
- child **{path.stat().st_size/1e6:.1f} MB** · 4096²
- engine NCNN GENERAL · infer {infer_s:.1f}s / 48 probes
- PASS={ok}

## 記憶
memmap residual · tiled fill/ridge · 避免 4096 float 全幅堆疊 OOM
""")
    print(json.dumps(accept, indent=2, ensure_ascii=False), flush=True)
    print("DONE R7", flush=True)
    del hyb_u8
    gc.collect()

if __name__ == "__main__":
    main()
