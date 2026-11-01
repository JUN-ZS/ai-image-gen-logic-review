#!/usr/bin/env python3
"""Unify R6c+R7 THIS_RUN outputs → SHA256SUMS + MANIFEST (no self-hash)."""
from __future__ import annotations
import hashlib, json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/workspace/artifacts/SETS/PROJ_R5_SILVER_ARMOR_2394")
R6 = ROOT / "r6c" / "complete"
R7 = ROOT / "r7_peep2" / "complete"
R7OUT = ROOT / "r7_peep2"

CANDIDATES = [
    R6 / "P0_CHILD_2048_NCNN_PBI_R6c.png",
    R6 / "P1_CHILD_2048_NCNN_PBI_R6c.png",
    R6 / "P0_PROOF.jpg",
    R6 / "P1_PROOF.jpg",
    R6 / "P0_DIFF.jpg",
    R6 / "P1_DIFF.jpg",
    R6 / "P0_G8_DEBUG.jpg",
    R6 / "P1_G8_DEBUG.jpg",
    R6 / "P0_PBI_PREVIEW_512.jpg",
    R6 / "P1_PBI_PREVIEW_512.jpg",
    R6 / "ACCEPT_R6c_PBI.json",
    ROOT / "r6c" / "LOG_R6c_PBI.md",
    R7 / "PEEP2_CHILD_4096_NCNN_PBI_R7.png",
    R7 / "ACCEPT_R7_PBI.json",
    R7OUT / "LOG_R7_PBI.md",
    R7 / "PEEP2_CHILD_4096_PREVIEW_1024.jpg",
    R7 / "PROOF_PEEP2_R7.jpg",
    R7 / "ZOOM_L0_vs_R7_NATIVE.jpg",
    R7 / "ZOOM400_PEEP2_CENTER.png",
]

def main():
    entries, lines = [], []
    for p in CANDIDATES:
        if not p.is_file():
            continue
        b = p.read_bytes()
        h = hashlib.sha256(b).hexdigest()
        entries.append({"path": str(p), "sha256": h, "bytes": len(b)})
        lines.append(f"{h}  {p}")
    sums = R6 / "SHA256SUMS_PBI.txt"
    sums.write_text("\n".join(lines) + "\n")
    sh = hashlib.sha256(sums.read_bytes()).hexdigest()
    # read gates
    gates = {}
    acc = R6 / "ACCEPT_R6c_PBI.json"
    if acc.is_file():
        a = json.loads(acc.read_text())
        gates["r6c_status"] = a.get("status")
        gates["r6c_image_generation"] = a.get("image_generation")
        gates["n_accept"] = a.get("n_accept")
        gates["n_struct"] = a.get("n_struct")
    a7 = R7 / "ACCEPT_R7_PBI.json"
    if a7.is_file():
        b = json.loads(a7.read_text())
        gates["r7_status"] = b.get("status")
        gates["r7_parent_mode"] = b.get("parent_mode")
        gates["r7_align"] = (b.get("peep2") or {}).get("align")
    man = {
        "bundle": "R6c_R7_PBI_UNIFIED",
        "asof": datetime.now(timezone.utc).isoformat(),
        "rule": "entries exclude MANIFEST self-hash; verify SHA256SUMS_PBI.txt",
        "sha256sums_sidecar": {"path": str(sums), "sha256": sh, "bytes": sums.stat().st_size},
        "entries": entries,
        "gates_honest": gates,
        "merge_main": "NO",
    }
    mp = R6 / "MANIFEST_SHA256_R6c_PBI.json"
    mp.write_text(json.dumps(man, indent=2, ensure_ascii=False) + "\n")
    (R6 / "SHA256_MANIFEST_NOTE.txt").write_text(
        f"{hashlib.sha256(mp.read_bytes()).hexdigest()}  {mp}\n{sh}  {sums}\n"
    )
    print(json.dumps({"n_entries": len(entries), "gates": gates}, indent=2))

if __name__ == "__main__":
    main()
