#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bridge bulk story JSONL to a small, auditable geometry/edit batch. Does not render images."""
from __future__ import annotations
import argparse, json, re, sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List

from frame_pipeline import compile_frame_set, write_packet as write_frame_packet
from proxy_edit_pipeline import write_packet as write_proxy_packet

def safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+","_",value).strip("._")[:100] or "story"

def select_records(input_path: Path, per_kernel: int=1, limit: int=20) -> List[Dict[str,Any]]:
    if per_kernel < 1: raise ValueError("--per-kernel must be >= 1")
    if limit < 1: raise ValueError("--limit must be >= 1")
    selected=[]; counts=Counter()
    with input_path.open("r",encoding="utf-8") as handle:
        for line in handle:
            if not line.strip(): continue
            row=json.loads(line)
            kernel=str(row.get("causal_kernel_id") or row.get("root_sin") or "UNASSIGNED")
            if counts[kernel] >= per_kernel: continue
            selected.append(row); counts[kernel]+=1
            if len(selected)>=limit: break
    if not selected: raise ValueError("no records selected from input JSONL")
    return selected

def build_batch(input_path: Path, outdir: Path, per_kernel: int=1, limit: int=20,
                final_weapon: str="T") -> Dict[str,Any]:
    final_weapon=final_weapon.upper()
    if final_weapon not in ("CROSS","T","RADIAL"):
        raise ValueError("--final-weapon must be CROSS, T, or RADIAL")
    records=select_records(input_path,per_kernel,limit)
    outdir.mkdir(parents=True,exist_ok=True)
    packages=[]
    for record in records:
        story_id=str(record.get("story_id") or "STORY-UNKNOWN")
        story_dir=outdir/safe_name(story_id)
        frame_out=story_dir/"frames"
        packet=compile_frame_set(record,weapon_topology=final_weapon)
        frame_summary=write_frame_packet(packet,frame_out)
        layout_path=Path(frame_summary["directory"])/"layout.json"
        proxy_dir=story_dir/"proxy_edit"
        proxy_summary=write_proxy_packet(layout_path,proxy_dir,final_weapon=final_weapon)
        packages.append({
            "story_id":story_id,
            "causal_kernel_id":record.get("causal_kernel_id") or record.get("root_sin") or "UNASSIGNED",
            "causal_signature":record.get("causal_signature"),
            "final_weapon":final_weapon,
            "frame_directory":frame_summary["directory"],
            "proxy_directory":proxy_summary["outdir"],
            "proxy_status":proxy_summary["status"],
            "terminal_face_gap_px":proxy_summary["terminal_face_gap_px"],
            "image_realization":"NOT_RUN",
            "edited_pixel_audit":"NOT_RUN",
        })
    batch={
        "pipeline_version":"1.0.0",
        "input":str(input_path),
        "requested_per_kernel":per_kernel,
        "requested_limit":limit,
        "selected_stories":len(packages),
        "distinct_causal_kernels":len({p["causal_kernel_id"] for p in packages}),
        "final_weapon":final_weapon,
        "method":"bulk JSONL -> per-story frame packet -> cross proxy -> target-only sphere edit plan -> final weapon edit plan",
        "image_realization":"NOT_RUN",
        "pixel_audit_status":"NOT_RUN",
        "packages":packages,
    }
    (outdir/"realize_batch_manifest.json").write_text(json.dumps(batch,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return batch

def main(argv=None):
    parser=argparse.ArgumentParser(description="Select a small per-kernel sample from bulk JSONL and compile edit packets; no AI render is run.")
    parser.add_argument("--input",required=True)
    parser.add_argument("--outdir",required=True)
    parser.add_argument("--per-kernel",type=int,default=1)
    parser.add_argument("--limit",type=int,default=20)
    parser.add_argument("--final-weapon",choices=("CROSS","T","RADIAL"),default="T")
    args=parser.parse_args(argv)
    try: result=build_batch(Path(args.input),Path(args.outdir),args.per_kernel,args.limit,args.final_weapon)
    except (OSError,ValueError,json.JSONDecodeError) as exc:
        print("BLOCK: "+str(exc),file=sys.stderr); return 2
    print(json.dumps({k:result[k] for k in ("selected_stories","distinct_causal_kernels","final_weapon","image_realization","pixel_audit_status")},
                     ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__": raise SystemExit(main())
