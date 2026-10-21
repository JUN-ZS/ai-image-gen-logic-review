#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compile one dense CYLINDER_CROSS collision-atlas prompt and a crop map.

This generator writes a single-image prompt and metadata only. It does not generate
images or claim the contact geometry has been visually achieved.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List

from cylinder_cross_contact_matrix import (
    CAMERA_VIEWS,
    HANDLE_CLOCK_VARIANTS,
    NEGATIVE,
    STRIKE_AXES,
    TOPOLOGY_LOCK,
)

VERSION = "1.0.0"
COLUMNS = 8
ROWS = 6


def build_atlas() -> Dict[str, Any]:
    """Build 48 intended local collision pockets: 12 views x 4 axes."""
    instances: List[Dict[str, Any]] = []
    index = 0
    for camera_index, (camera_id, camera_text) in enumerate(CAMERA_VIEWS, start=1):
        for axis_index, (axis_id, axis_text) in enumerate(STRIKE_AXES, start=1):
            pose_index = ((camera_index - 1) + (axis_index - 1)) % len(HANDLE_CLOCK_VARIANTS)
            pose_id, pose_text = HANDLE_CLOCK_VARIANTS[pose_index]
            index += 1
            instances.append({
                "instance_id": f"A{index:02d}",
                "grid_row": (index - 1) // COLUMNS + 1,
                "grid_column": (index - 1) % COLUMNS + 1,
                "camera_view_id": camera_id,
                "camera_view": camera_text,
                "collision_axis_id": axis_id,
                "collision_axis": axis_text,
                "handle_roll_variant_id": pose_id,
                "handle_roll_variant": pose_text,
                "intended_objects": 2,
                "intended_contact": "FLAT_CIRCULAR_END_CAP_TO_FLAT_CIRCULAR_END_CAP",
                "generation_status": "NOT_RUN",
                "crop_review_status": "CROP_CANDIDATES_UNREVIEWED",
            })

    prompt = (
        "CREATE ONE SINGLE, ULTRA-DENSE, PHOTOREALISTIC 16:9 IMAGE: a seamless field of many "
        "independent cylinder-ended cross-hammer collisions, made for later visual scanning and cropping. "
        "Target 48 local collision instances in an implicit 8-column by 6-row field. Do not draw cell borders, "
        "grid lines, dividers, labels, IDs, arrows, captions, text or watermarks. The entire canvas should be "
        "densely populated without large empty margins. Every local instance must remain independently traceable; "
        "leave only a narrow clean moat between neighboring pairs so their handles and heads do not merge. "
        "Each local instance contains exactly TWO distinct hammers that collide with one another; never let a "
        "hammer from one instance contact a hammer from a neighboring instance. Vary camera angle, collision-axis "
        "direction, perspective, handle roll and scale, while prioritizing readable circular-cap contact over "
        "decoration. "
        + TOPOLOGY_LOCK + " "
        "HARD CONTACT RULE FOR EVERY INTENDED VALID INSTANCE: the two designated OUTER FLAT CIRCULAR END CAPS "
        "meet flat-face-to-flat-face at one shared contact seam, with coincident cap planes and opposite outward "
        "normals along that instance's collision axis. The cap rims and circular face planes must be visible enough "
        "to judge in a crop. Curved cylindrical barrel walls, crossbar sides, vertical cross arms, corners and "
        "handles NEVER make first contact. A valid instance cannot substitute a side-on cylinder collision, "
        "bar-to-bar collision, corner hit, handle hit, or caps merely near each other. Each complete cross hammer "
        "is one rigid body: no bending, kinking, twisting, telescoping, detaching, or independent head/handle rotation. "
        "Do not create impossible extra arms, fused heads, shared handles, three-way impacts or merged neighboring pairs. "
        "COMPOSITION TARGET: 48 distinct collision pockets in implicit reading order from top-left to bottom-right. "
        "Sample all four scene collision axes: horizontal, vertical, rising diagonal and front-to-back depth. Vary "
        "grazing face-oriented, side-profile, three-quarter, low, high, overhead, macro-seam and wide views. Vary "
        "the rigid handle-roll relationships while preserving the same end-cap-only contact rule. This is a "
        "candidate-finding atlas, not proof that every tiny instance is correct. Optimize seam visibility and object "
        "separation for later cropping; a smaller number of clean, clearly correct instances is preferable to a field "
        "of ambiguous or physically wrong contacts. Use realistic metal, coherent perspective, controlled neutral "
        "studio illumination, crisp silhouettes and high local contrast at the circular contact seams. No visible "
        "grid or panel frames; this should read as one continuous dense image. NEGATIVE PROMPT: " + NEGATIVE
    )

    return {
        "pipeline_version": VERSION,
        "artifact_type": "SINGLE_IMAGE_DENSE_CANDIDATE_ATLAS",
        "topology": "CYLINDER_CROSS",
        "canvas": {"aspect_ratio": "16:9", "target_layout_rows": ROWS, "target_layout_columns": COLUMNS},
        "intended_local_collision_count": len(instances),
        "intended_hammer_count": len(instances) * 2,
        "prompt_file": "cylinder_cross_dense_atlas_prompt.txt",
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "prompt_text": prompt,
        "instances": instances,
        "sampling_balance": {
            "camera_views": len(CAMERA_VIEWS),
            "collision_axes": len(STRIKE_AXES),
            "handle_roll_relationships": len(HANDLE_CLOCK_VARIANTS),
            "view_axis_pairs": len(instances),
            "rendered_instance_count_guaranteed": False,
        },
        "immutable_contact_contract": {
            "only_permitted_first_contact": ["FLAT_CIRCULAR_END_CAP_A", "FLAT_CIRCULAR_END_CAP_B"],
            "required_relation": "COINCIDENT_CAP_PLANES_OPPOSITE_NORMALS",
            "forbidden_first_contacts": ["CURVED_CYLINDER_BARREL", "CROSSBAR_SIDE", "CROSS_ARM", "CORNER", "HANDLE"],
            "rigid_body_required": True,
        },
        "generation_status": "IMAGE_REALIZATION_NOT_RUN",
        "crop_review_status": "CROP_CANDIDATES_UNREVIEWED",
        "pixel_audit_status": "PIXEL_AUDIT_NOT_RUN",
        "gate": "ATLAS_PROMPT_READY",
        "warning": (
            "This atlas does not satisfy the independent 48-H2 evidence matrix gate. It is a discovery aid; "
            "only separately cropped and manually reviewed actual pixels may become candidate evidence. "
            "Legacy T-hammer images are excluded."
        ),
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Write one dense CYLINDER_CROSS atlas prompt and crop map; never generates images."
    )
    parser.add_argument("--outdir", required=True, help="Output directory for prompt and manifest")
    args = parser.parse_args(argv)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    manifest = build_atlas()
    prompt = manifest.pop("prompt_text")
    (outdir / manifest["prompt_file"]).write_text(prompt + "\n", encoding="utf-8")
    (outdir / "cylinder_cross_dense_atlas_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    readme = (
        "# Dense CYLINDER_CROSS candidate atlas\n\n"
        "Generate one very dense 16:9 image using the prompt file. Use the JSON manifest only as a "
        "crop-map and coverage target; do not assume the model actually renders all 48 instances. "
        "Scan the real image and crop only visibly correct end-cap-to-end-cap contacts. Every kept crop "
        "remains unreviewed until its actual pixels are manually inspected. This atlas does not replace "
        "the separate 48-H2 evidence matrix.\n"
    )
    (outdir / "README.md").write_text(readme, encoding="utf-8")
    print(json.dumps({
        "gate": manifest["gate"],
        "intended_local_collision_count": manifest["intended_local_collision_count"],
        "prompt_file": manifest["prompt_file"],
        "generation_status": manifest["generation_status"],
        "pixel_audit_status": manifest["pixel_audit_status"],
        "outdir": str(outdir),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
