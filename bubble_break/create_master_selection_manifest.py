#!/usr/bin/env python3
"""Create a hash-bound human ROI selection manifest and an auditable crop preview.

This utility does not detect/choose the correct tool. A human must visually inspect the
source atlas, choose the bounding box, supply reviewer/notes, and explicitly confirm the
ROI contains one tool instance. The downstream validator still checks all file metadata.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Sequence

from PIL import Image


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def create_master_selection_manifest(
    source_atlas_path: str | Path,
    roi_xyxy: Sequence[int],
    *,
    reviewer: str,
    notes: str,
    confirm_single_tool: bool,
    output_json: str | Path,
    crop_output: str | Path,
) -> dict:
    atlas = Path(source_atlas_path).resolve()
    if not atlas.is_file():
        raise FileNotFoundError(f"source atlas does not exist: {atlas}")
    if not reviewer.strip():
        raise ValueError("reviewer must be non-empty")
    if not notes.strip():
        raise ValueError("notes must be non-empty")
    if confirm_single_tool is not True:
        raise ValueError("human must explicitly confirm the ROI contains exactly one selected tool instance")
    if len(roi_xyxy) != 4:
        raise ValueError("ROI must be [x0,y0,x1,y1]")
    x0, y0, x1, y1 = (int(value) for value in roi_xyxy)
    with Image.open(atlas) as image:
        image.load()
        width, height = image.size
        if not (0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height):
            raise ValueError(f"ROI [{x0},{y0},{x1},{y1}] must be inside source atlas {width}x{height}")
        crop = image.crop((x0, y0, x1, y1))
        crop_path = Path(crop_output).resolve()
        crop_path.parent.mkdir(parents=True, exist_ok=True)
        crop.save(crop_path)

    record = {
        "selection_mode": "HUMAN_ROI",
        "selection_reviewer": reviewer.strip(),
        "selection_notes": notes.strip(),
        "source_atlas_image_path": str(atlas),
        "source_atlas_raster_sha256": sha256_file(atlas),
        "source_atlas_width_px": width,
        "source_atlas_height_px": height,
        "selected_roi_xyxy_px": [x0, y0, x1, y1],
        "selected_roi_crop_path": str(crop_path),
        "selected_roi_crop_sha256": sha256_file(crop_path),
        "selected_tool_is_single_instance": True,
        "human_confirmed_single_tool_instance": True,
        "visual_tool_acceptance_status": "HUMAN_ROI_SELECTION_ONLY_TOOL_GEOMETRY_STILL_REQUIRES_STAGE_B_REVIEW",
    }
    output = Path(output_json).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return record


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-atlas", type=Path, required=True)
    parser.add_argument("--roi", type=int, nargs=4, metavar=("X0", "Y0", "X1", "Y1"), required=True)
    parser.add_argument("--reviewer", required=True)
    parser.add_argument("--notes", required=True)
    parser.add_argument("--out-json", type=Path, default=Path("out/master-selection.json"))
    parser.add_argument("--crop-out", type=Path, default=Path("out/selected-master-roi.png"))
    parser.add_argument("--confirm-single-tool", action="store_true",
                        help="required human attestation that the selected ROI contains one tool instance")
    args = parser.parse_args(argv)
    try:
        result = create_master_selection_manifest(
            args.source_atlas, args.roi, reviewer=args.reviewer, notes=args.notes,
            confirm_single_tool=args.confirm_single_tool, output_json=args.out_json,
            crop_output=args.crop_out,
        )
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps({
        "status": "HUMAN_ROI_MANIFEST_CREATED",
        "source_atlas_sha256": result["source_atlas_raster_sha256"],
        "source_atlas_size_px": [result["source_atlas_width_px"], result["source_atlas_height_px"]],
        "selected_roi_xyxy_px": result["selected_roi_xyxy_px"],
        "crop_path": result["selected_roi_crop_path"],
        "crop_sha256": result["selected_roi_crop_sha256"],
        "visual_tool_acceptance_status": result["visual_tool_acceptance_status"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
