#!/usr/bin/env python3
"""Verify that an accepted donor's opaque pixels are unchanged in the final VM."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageChops

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--donor", required=True, type=Path)
    ap.add_argument("--master", required=True, type=Path)
    ap.add_argument("--xy", required=True, nargs=2, type=int, metavar=("X","Y"))
    ap.add_argument("--visible-mask", type=Path, default=None,
                    help="Optional donor-sized mask of pixels owned/visible in the final multi-layer composite.")
    ap.add_argument("--alpha-threshold", type=int, default=250)
    ap.add_argument("--out", type=Path, required=True)
    args=ap.parse_args()

    donor=Image.open(args.donor)
    if donor.mode != "RGBA":
        raise SystemExit(f"BLOCK: donor must be RGBA, got {donor.mode}")
    master=Image.open(args.master).convert("RGB")
    donor_rgb=donor.convert("RGB")
    alpha=donor.getchannel("A")
    core=alpha.point(lambda v:255 if v>=args.alpha_threshold else 0)
    if args.visible_mask:
        visible=Image.open(args.visible_mask).convert("L")
        if visible.size != donor.size:
            raise SystemExit(f"BLOCK: visible mask size {visible.size} != donor {donor.size}")
        visible=visible.point(lambda v:255 if v>=128 else 0)
        core=ImageChops.multiply(core,visible)

    count=sum(core.histogram()[1:])
    x,y=args.xy
    w,h=donor.size
    if x<0 or y<0 or x+w>master.width or y+h>master.height:
        raise SystemExit("BLOCK: donor paste rectangle lies outside Virtual Master")
    crop=master.crop((x,y,x+w,y+h))
    diff=ImageChops.difference(donor_rgb,crop)
    masked=ImageChops.composite(diff,Image.new("RGB",donor.size,(0,0,0)),core)
    maxima=[ch.getextrema()[1] for ch in masked.split()]
    max_diff=max(maxima) if maxima else 0
    result={
      "status":"PASS" if count>0 and max_diff==0 else "BLOCK",
      "core_exact":bool(count>0 and max_diff==0),
      "donor_sha256":sha256(args.donor),
      "master_sha256":sha256(args.master),
      "donor_xy":[x,y],
      "donor_canvas_wh":[w,h],
      "verified_visible_opaque_pixels":int(count),
      "alpha_threshold":args.alpha_threshold,
      "max_channel_diff":int(max_diff),
      "visible_mask_sha256":sha256(args.visible_mask) if args.visible_mask else None,
      "method":"PIL RGB exact comparison on donor alpha core, restricted by visible ownership mask when supplied"
    }
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False,indent=2))
    raise SystemExit(0 if result["status"]=="PASS" else 2)

if __name__=="__main__":
    main()
