#!/usr/bin/env python3
"""
Orchestrator skeleton for:
  A抽白 → MASK → B CLIP → paste A → ROI/PATH1E/DHY/ECC → NCNN

Calls sibling scripts; fill paths. Does not invent quality PASS.
"""
from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path

def sh(cmd: list[str]) -> None:
    print("+", " ".join(cmd), flush=True)
    r = subprocess.run(cmd)
    if r.returncode != 0:
        sys.exit(r.returncode)

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a-mother", type=Path, required=True, help="noisy A 母")
    ap.add_argument("--b-donor", type=Path, required=True, help="另母 clean pixels")
    ap.add_argument("--work", type=Path, default=Path("runs/pipe_A"))
    ap.add_argument("--skip-ncnn", action="store_true")
    ap.add_argument("--skip-path1e", action="store_true", help="PATH1E needs external Ref/Imagine")
    args = ap.parse_args()
    W = args.work
    W.mkdir(parents=True, exist_ok=True)

    # 1 WNK
    sh([sys.executable, "tools/wnk_white_noise_kill.py",
        "--input", str(args.a_mother), "--out-dir", str(W / "01_wnk")])
    # expect OUT_WNK.png + MASK — adjust names to your WNK tool
    a_wnk = W / "01_wnk" / "OUT_WNK.png"
    mask = W / "01_wnk" / "WNK_KILL_MASK.png"

    # 2 mask clip paste
    sh([sys.executable, str(Path(__file__).resolve().parent / "pipe_mask_clip_paste.py"),
        "--a-wnk", str(a_wnk), "--mask", str(mask),
        "--b-donor", str(args.b_donor), "--out-dir", str(W / "02_paste")])
    a_paste = W / "02_paste" / "OUT_WNK_MASKPASTE.png"

    # 3 PATH1E / DHY / ECC — plug your peep tools here
    if not args.skip_path1e:
        print("TODO: ROI face/armor → PATH1E plate → ECC hardpaste onto master")
        print("  see pipe_e357_ecc_hardpaste.py for ECC stage")

    # 4 NCNN memsafe
    if not args.skip_ncnn:
        print("TODO: ncnn_fullframe_pbi.py --input <1792 or keep 7k> --out-dir 04_ncnn")
        print("  default: write RAW then strip PBI; never claim quality PASS")

    summary = {
        "A": str(args.a_mother),
        "B": str(args.b_donor),
        "A_paste": str(a_paste),
        "pixel_drop": False,
        "quality_qualified": False,
        "pipe": "WNK→MASK→CLIP(B)→paste(A)→[PATH1E/ECC]→[NCNN]",
    }
    (W / "PIPE_SUMMARY.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
