#!/usr/bin/env python3
"""
Step ④⑤ of the true pipe:
  MASK from A (WNK kill map) → place on B (另母) → CLIP pixels → paste onto A_WNK

Does NOT: NCNN / PATH1E / ECC. Those are later stages.

Usage:
  python pipe_mask_clip_paste.py \
    --a-wnk OUT_WNK.png \
    --mask  WNK_KILL_MASK.png \
    --b-donor FAIR_or_10d59_7168.png \
    --out-dir runs/mask_paste
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import cv2
import numpy as np


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def load_mask(path: Path, hw: tuple[int, int]) -> np.ndarray:
    m = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if m is None:
        raise FileNotFoundError(path)
    if m.ndim == 3:
        m = cv2.cvtColor(m, cv2.COLOR_BGR2GRAY)
    H, W = hw
    if m.shape[:2] != (H, W):
        m = cv2.resize(m, (W, H), interpolation=cv2.INTER_NEAREST)
    return (m > 127).astype(np.uint8)


def run(a_wnk: Path, mask_p: Path, b_donor: Path, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    A = cv2.imread(str(a_wnk), cv2.IMREAD_COLOR)
    B = cv2.imread(str(b_donor), cv2.IMREAD_COLOR)
    if A is None or B is None:
        raise FileNotFoundError("A or B unreadable")
    Ha, Wa = A.shape[:2]
    Hb, Wb = B.shape[:2]
    MASK_A = load_mask(mask_p, (Ha, Wa))

    # scale mask to B, CLIP B pixels
    MASK_B = cv2.resize(MASK_A, (Wb, Hb), interpolation=cv2.INTER_NEAREST)
    CLIP = np.zeros((Hb, Wb, 4), dtype=np.uint8)
    CLIP[..., :3] = B
    CLIP[..., 3] = MASK_B * 255
    clip_path = out_dir / "CLIP_PIXELS_from_donor_BGRA.png"
    cv2.imwrite(str(clip_path), CLIP)

    # bring CLIP (+ mask) back to A size for paste — only intermediates scale
    if (Wb, Hb) != (Wa, Ha):
        B_on_A = cv2.resize(B, (Wa, Ha), interpolation=cv2.INTER_LANCZOS4)
        # re-derive mask at A (already have MASK_A)
    else:
        B_on_A = B

    A_paste = A.copy()
    sel = MASK_A.astype(bool)
    kill_px = int(sel.sum())
    A_paste[sel] = B_on_A[sel]

    out_path = out_dir / "OUT_WNK_MASKPASTE.png"
    if out_path.exists():
        raise FileExistsError(f"refuse overwrite {out_path}")
    cv2.imwrite(str(out_path), A_paste)

    # debug previews
    heat = np.zeros_like(A)
    heat[sel] = (0, 0, 255)
    overlay = cv2.addWeighted(A, 0.65, heat, 0.35, 0)
    cv2.imwrite(str(out_dir / "MASK_overlay_preview.jpg"), overlay, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    half = cv2.resize(A_paste, (A_paste.shape[1] // 2, A_paste.shape[0] // 2), cv2.INTER_AREA)
    cv2.imwrite(str(out_dir / "OUT_WNK_MASKPASTE_preview.jpg"), half, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

    doc = {
        "format": "ige.skill.wnk_mask_paste",
        "format_version": "1.2",
        "skill": "MASK(from A) → CLIP(B) → paste onto A_WNK",
        "A_wnk": str(a_wnk),
        "A_sha256": sha256_file(a_wnk),
        "A_wh": [Wa, Ha],
        "mask": str(mask_p),
        "mask_sha256": sha256_file(mask_p),
        "B_donor": str(b_donor),
        "B_sha256": sha256_file(b_donor),
        "B_wh": [Wb, Hb],
        "scale_A_to_B": [Wb / Wa, Hb / Ha],
        "clip_bgra": str(clip_path),
        "clip_sha256": sha256_file(clip_path),
        "kill_px": kill_px,
        "kill_frac": kill_px / float(Wa * Ha),
        "output": str(out_path),
        "output_sha256": sha256_file(out_path),
        "output_wh": [Wa, Ha],
        "pixel_drop": False,
        "note": "A space preserved for paste; B only provides pixels under MASK",
        "quality_qualified": False,
        "asof": datetime.now(timezone.utc).isoformat(),
    }
    (out_dir / "RESULT_MASKPASTE.json").write_text(
        json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return doc


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a-wnk", type=Path, required=True)
    ap.add_argument("--mask", type=Path, required=True)
    ap.add_argument("--b-donor", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, default=Path("runs/mask_paste"))
    args = ap.parse_args()
    doc = run(args.a_wnk, args.mask, args.b_donor, args.out_dir)
    print(json.dumps({"ok": True, "sha": doc["output_sha256"], "kill_frac": doc["kill_frac"]}, indent=2))


if __name__ == "__main__":
    main()
