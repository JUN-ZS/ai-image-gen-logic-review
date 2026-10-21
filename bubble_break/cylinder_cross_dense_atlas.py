#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compile a varied, handle-explicit, single-image CYLINDER_CROSS candidate atlas.

The generator writes prompts and a crop map only. It does not create images or
certify the actual geometry.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List

from cylinder_cross_contact_matrix import CAMERA_VIEWS, HANDLE_CLOCK_VARIANTS, NEGATIVE, STRIKE_AXES, TOPOLOGY_LOCK

VERSION = "1.1.0"
TARGET_INTERACTIONS = 24

# An irregular scatter instead of the old 8x6 tile plan. Hints are deliberately
# non-uniform and local; the model must not print them on the image.
REGION_HINTS = (
    "upper-left pocket, foreground scale, rotated clockwise",
    "upper edge near center, medium scale, steep diagonal pose",
    "upper-right pocket, large scale, cap faces clearly foreshortened",
    "left side above center, smaller depth layer, vertical projected axis",
    "right side above center, medium scale, handle projecting toward viewer",
    "center-left open pocket, foreground scale, opposite handle-roll relation",
    "center-right open pocket, small but full tool silhouettes",
    "left perimeter below midpoint, oblique orientation, all parts inside frame",
    "right perimeter below midpoint, low-looking 3D orientation",
    "lower-left pocket, large scale, handles extending apart across the canvas",
    "lower-right pocket, medium scale, cap rims readable against dark metal",
    "lower edge left of center, foreshortened depth-axis pose",
    "lower edge right of center, strong diagonal orientation",
    "near upper-left but behind another depth layer, compact scale",
    "near upper-right but closer to camera, large readable handles",
    "mid-left foreground, profile-like projection with the two caps aligned",
    "mid-right foreground, reverse three-quarter projection",
    "center-upper pocket, vertical collision axis, oblique handle roll",
    "center-lower pocket, horizontal collision axis, handles projecting in depth",
    "left-center far pocket, reduced scale but long handles still unmistakable",
    "right-center far pocket, long-lens-like compression with visible cap seam",
    "near lower-left corner but fully inside frame, elevated perspective",
    "near lower-right corner but fully inside frame, low perspective",
    "remaining negative-space pocket, distinct axis and unique silhouette",
)

# Remove atlas-incompatible clauses inherited from the single-pair matrix prompt.
ATLAS_NEGATIVE = (
    NEGATIVE.replace("no contact sheet, ", "")
    .replace("no storyboard, ", "")
    .replace("no split screen, ", "")
    .replace("no collage", "no visible collage borders")
)
ATLAS_NEGATIVE += (
    ", no uniform isometric pose repeated across the image, no cloned or stamped pairs, "
    "no flat icon silhouettes, no missing handles, no short central peg instead of a handle, "
    "no head-joint contact, no sparks hiding the circular end-cap seam"
)


def build_atlas() -> Dict[str, Any]:
    """Build 24 deliberately varied local interactions; count is a target, not proof."""
    instances: List[Dict[str, Any]] = []
    for i in range(TARGET_INTERACTIONS):
        camera_index = (i * 5) % len(CAMERA_VIEWS)
        axis_index = (i * 3) % len(STRIKE_AXES)
        pose_index = (i * 3 + i // 4) % len(HANDLE_CLOCK_VARIANTS)
        camera_id, camera_text = CAMERA_VIEWS[camera_index]
        axis_id, axis_text = STRIKE_AXES[axis_index]
        pose_id, pose_text = HANDLE_CLOCK_VARIANTS[pose_index]
        instances.append({
            "instance_id": f"A{i + 1:02d}",
            "region_hint": REGION_HINTS[i],
            "collision_axis_id": axis_id,
            "collision_axis": axis_text,
            "projection_style_id": camera_id,
            "projection_style": camera_text,
            "handle_roll_variant_id": pose_id,
            "handle_roll_variant": pose_text,
            "intended_objects": 2,
            "required_visible_handles": 2,
            "minimum_handle_to_head_width_ratio": 2.5,
            "intended_contact": "FLAT_CIRCULAR_END_CAP_TO_FLAT_CIRCULAR_END_CAP",
            "generation_status": "NOT_RUN",
            "crop_review_status": "CROP_CANDIDATES_UNREVIEWED",
        })

    assignment_lines = []
    for item in instances:
        assignment_lines.append(
            f'{item["instance_id"]} (internal guidance only; do NOT render text): '
            f'{item["region_hint"]}; collision axis: {item["collision_axis"]}; '
            f'local projection treatment: {item["projection_style"]}; '
            f'handle roll: {item["handle_roll_variant"]}'
        )
    assignments = "\n".join(assignment_lines)

    prompt = (
        "ONE SINGLE ULTRA-DENSE PHOTOREALISTIC 16:9 RASTER IMAGE. Create an organically scattered "
        "field of 24 distinct 3D hammer-pair collision studies for later human scanning and cropping. "
        "This is not a uniform grid, not a repeated tile, not a contact sheet with boxes, and not a row "
        "of identical stamps. Use the full canvas with crowded but readable spacing, a loose diagonal flow, "
        "varied local scale, varied depth placement and clearly different projected orientations. A single "
        "coherent overall scene camera may be used, but the 24 pairs must each have their own visibly "
        "different 3D orientation and projected collision direction. At least 16 pair silhouettes should "
        "be unmistakably distinct at a glance. Never satisfy density by shrinking all tools into tiny copies. "
        "If necessary, render fewer distinct pairs rather than omit the long handles, repeat one pose, or "
        "obscure the active contact geometry. Do not print instance IDs, words, labels, grid lines, cell borders, "
        "arrows, captions or watermarks. "
        "GEOMETRY OF EACH INDIVIDUAL HAMMER — THIS IS CRITICAL: every collision pair consists of exactly "
        "TWO complete, separate hammers, therefore two separate heads and two separate long handles. Each "
        "head is a real 3D plus-shaped cross head in one plane: one straight horizontal crossbar and one "
        "straight vertical cross arm intersecting at the exact center. The two opposite OUTER ends of the "
        "horizontal crossbar terminate in short solid cylinders. Each cylinder has a clearly distinct flat "
        "circular end cap and curved barrel wall. One and only one long straight handle attaches at the exact "
        "center BACK of each plus-shaped head and extends perpendicular out of the head plane as a third axis. "
        "The handle is NOT the vertical cross arm. The handle is NOT a short central peg. The head does NOT "
        "have an extra upright post instead of the handle. Each handle must be unmistakably long, at least 2.5 "
        "times the full cross-head width in visible projected length whenever framing permits, continuously "
        "connected to its own center joint and clearly traceable away from the head. Show BOTH separate handles "
        "for every pair; do not let the handles overlap so completely that they become one rod. Keep each whole "
        "hammer inside the frame. Rotate each complete rigid head-plus-handle as one object to create pose "
        "variation; never bend the handle or rotate it independently. "
        + TOPOLOGY_LOCK + " "
        "ABSOLUTE CONTACT RULE: the two hammers in each pair make first contact ONLY at the two OUTER FLAT "
        "CIRCULAR END CAPS of their opposed horizontal-end cylinders. The flat circular planes touch face-to-face "
        "at one small shared seam, with coincident planes and opposite normals. The contact must be visibly at "
        "the far outer cylinder caps, NOT at the central plus-head joint. Both circular cap rims and a sliver of "
        "the flat cap planes must remain visible around the seam; a tiny restrained spark may sit at the outer "
        "cap seam but must never cover it. No impact sparks at the center joint. No cap merely hovering near "
        "the other cap. No curved-barrel-side collision. No crossbar-side, cross-arm, corner, or handle contact. "
        "For every pair, keep the two central joints and both handles visibly away from the contact seam. "
        "Vary the actual orientations, not just lighting: show left-right, top-bottom, rising diagonal, falling "
        "diagonal and front-to-back/depth-axis contacts; some cap planes nearly face the viewer, some are viewed "
        "at a grazing angle, and others have obvious perspective foreshortening. Vary handle projection: some "
        "handles extend to opposite sides of the seam; some both project toward the same side; some one points "
        "toward camera and the other away; some project up/down or at distinct diagonal angles. Each pair must "
        "read as a physically complete independent two-tool collision, not as one fused H-like object. "
        "INSTANCE-BY-INSTANCE POSE ASSIGNMENTS — use these to make the local silhouettes and collision directions "
        "different; the IDs are instruction metadata only, NEVER visible text:\n"
        + assignments
        + "\n"
        "The region descriptions are loose placement hints, NOT panel locations. Do not form neat rows or "
        "columns. Use irregular spacing and different scales, but maintain a narrow clean boundary around each "
        "pair so adjacent heads and handles do not fuse. Prefer hard readable metal silhouettes, controlled "
        "directional studio lighting, high detail at each circular cap, and restrained effects. The result must "
        "look three-dimensional: visible cylinder depth, bevel/edge transitions, cast shadows, foreshortening, "
        "occlusion and clear shaft attachment depth. Never use a flat top-down icon language. "
        "NEGATIVE PROMPT: "
        + ATLAS_NEGATIVE
    )

    axes_count = {axis_id: sum(1 for x in instances if x["collision_axis_id"] == axis_id)
                  for axis_id, _ in STRIKE_AXES}
    pose_count = {pose_id: sum(1 for x in instances if x["handle_roll_variant_id"] == pose_id)
                  for pose_id, _ in HANDLE_CLOCK_VARIANTS}
    return {
        "pipeline_version": VERSION,
        "artifact_type": "SINGLE_IMAGE_DENSE_CANDIDATE_ATLAS",
        "topology": "CYLINDER_CROSS",
        "canvas": {"aspect_ratio": "16:9", "layout": "IRREGULAR_SCATTER_NO_GRID"},
        "target_local_collision_count": TARGET_INTERACTIONS,
        "target_hammer_count": TARGET_INTERACTIONS * 2,
        "required_visible_long_handles": TARGET_INTERACTIONS * 2,
        "minimum_handle_to_head_width_ratio": 2.5,
        "prompt_file": "cylinder_cross_dense_atlas_prompt.txt",
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "prompt_text": prompt,
        "instances": instances,
        "sampling_balance": {
            "collision_axes": len(STRIKE_AXES),
            "projection_styles": len(CAMERA_VIEWS),
            "handle_roll_relationships": len(HANDLE_CLOCK_VARIANTS),
            "counts_by_collision_axis": axes_count,
            "counts_by_handle_roll": pose_count,
            "rendered_instance_count_guaranteed": False,
        },
        "variation_contract": {
            "uniform_grid_allowed": False,
            "repeated_stamp_pose_allowed": False,
            "minimum_visibly_distinct_pair_silhouettes_target": 16,
            "independent_3d_pair_orientations_required": True,
            "both_long_handles_visible_per_pair": True,
            "contact_sparks_may_hide_cap_seam": False,
            "contact_at_center_joint_allowed": False,
        },
        "immutable_contact_contract": {
            "only_permitted_first_contact": ["FLAT_CIRCULAR_END_CAP_A", "FLAT_CIRCULAR_END_CAP_B"],
            "required_relation": "COINCIDENT_CAP_PLANES_OPPOSITE_NORMALS",
            "forbidden_first_contacts": ["CURVED_CYLINDER_BARREL", "CROSSBAR_SIDE", "CROSS_ARM", "CORNER", "HANDLE", "CENTER_JOINT"],
            "head_geometry": "PLUS_CROSS_HEAD_WITH_TWO_CYLINDER_TERMINAL_ENDS",
            "handle_geometry": "ONE_LONG_STRAIGHT_HANDLE_FROM_CENTER_BACK_PERPENDICULAR_TO_HEAD_PLANE",
            "rigid_body_required": True,
        },
        "generation_status": "IMAGE_REALIZATION_NOT_RUN",
        "crop_review_status": "CROP_CANDIDATES_UNREVIEWED",
        "pixel_audit_status": "PIXEL_AUDIT_NOT_RUN",
        "gate": "ATLAS_PROMPT_READY",
        "warning": (
            "This atlas is a candidate-finding aid and does not satisfy the independent 48-H2 evidence matrix gate. "
            "The user rejected the previous uniformly repeated atlas; this revision reduces target count to improve "
            "handle visibility and pose diversity. The model may render fewer than 24 valid interactions. "
            "Legacy T-hammer images are excluded."
        ),
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Write the varied single-image CYLINDER_CROSS prompt; no image rendering occurs.")
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
        "# CYLINDER_CROSS varied dense candidate atlas\n\n"
        "Generate one single 16:9 image with 24 target distinct collision pairs in an irregular, non-grid field. "
        "The target is not a guarantee of the rendered count. Every pair must show two complete cross hammers "
        "and two unmistakably long, separate handles. Scan the real image and crop only visibly correct outer "
        "flat-circular-end-cap contacts. This atlas does not replace the independent 48-H2 evidence matrix.\n"
    )
    (outdir / "README.md").write_text(readme, encoding="utf-8")
    print(json.dumps({
        "gate": manifest["gate"],
        "target_local_collision_count": manifest["target_local_collision_count"],
        "target_hammer_count": manifest["target_hammer_count"],
        "minimum_visible_long_handles": manifest["required_visible_long_handles"],
        "prompt_file": manifest["prompt_file"],
        "generation_status": manifest["generation_status"],
        "pixel_audit_status": manifest["pixel_audit_status"],
        "outdir": str(outdir),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
