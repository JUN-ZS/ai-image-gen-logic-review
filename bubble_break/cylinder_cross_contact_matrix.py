#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compile a stratified single-image cylinder-ended cross hammer end-face collision matrix.

This creates prompts and audit manifests only. It never calls an image model.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import zlib
from pathlib import Path
from typing import Any, Dict, List, Tuple

VERSION = "2.1.0"

MASTER_REVIEW_CHECKS = (
    "two_distinct_cylinder_ended_cross_hammers",
    "plus_shaped_cross_head_on_each_hammer",
    "one_rigid_centered_handle_per_hammer",
    "both_outer_cylinders_present",
    "no_bent_twisted_or_detached_parts",
)

REVIEW_CHECKS = (
    "two_distinct_cylinder_ended_cross_hammers",
    "active_flat_circular_end_cap_A_identified",
    "active_flat_circular_end_cap_B_identified",
    "both_flat_circular_end_caps_coincident",
    "cap_normals_opposite_along_collision_axis",
    "no_curved_cylinder_barrel_first",
    "no_crossbar_side_cross_arm_or_corner_first",
    "no_handle_first",
    "both_handles_and_center_joints_rigid",
)

CAMERA_VIEWS: Tuple[Tuple[str, str], ...] = (
    ("FACE_ON", "slightly grazing face-oriented view, about 10–15 degrees off the collision axis; show the contact seam, end-face perimeter edges and nearby depth cues. Do not pretend the camera can see through two coincident contact faces from directly along their normals"),
    ("SIDE_PROFILE", "true side profile perpendicular to the collision axis, both cylinder-ended cross-hammer profiles readable and the contact seam visible"),
    ("FRONT_THREE_QUARTER", "front three-quarter view about 35 degrees off the collision axis, showing each end-face plane and its cheek depth"),
    ("REVERSE_THREE_QUARTER", "reverse three-quarter view from the opposite side about 35 degrees off the collision axis, showing the same face-to-face joint"),
    ("LOW_ANGLE", "low camera angle slightly below the heads, looking up while retaining a clear view of both terminal faces"),
    ("HIGH_ANGLE", "high camera angle slightly above the heads, looking down while retaining a clear view of both terminal faces"),
    ("OVERHEAD", "overhead view from above the hammer pair, with both selected END FACES and their shared contact point unoccluded"),
    ("DUTCH_ROLL", "controlled 15-degree Dutch roll; the camera rolls, but neither hammer nor either contact plane bends"),
    ("MACRO_SEAM", "tight macro of the exact face-to-face seam, including enough adjacent crossbar and handle-joint geometry to identify both separate cylinder-ended cross hammers"),
    ("OVER_SHOULDER", "over the trailing handle/shoulder line of hammer A toward hammer B, with both striking faces and the seam unobstructed"),
    ("LONG_LENS", "compressed long-lens side three-quarter view with strong depth cues and both face planes still independently readable"),
    ("WIDE_ESTABLISHING", "wide 16:9 establishing view, both complete hammers and their handles visible, contact faces still large enough to inspect"),
)

STRIKE_AXES: Tuple[Tuple[str, str], ...] = (
    ("HORIZONTAL", "a horizontal left-to-right collision axis in the scene"),
    ("VERTICAL", "a vertical bottom-to-top collision axis in the scene"),
    ("DIAGONAL_RISE", "a diagonal collision axis rising from lower-left toward upper-right"),
    ("DEPTH_AXIS", "a front-to-back collision axis with visible depth separation before contact"),
)

HANDLE_CLOCK_VARIANTS: Tuple[Tuple[str, str], ...] = (
    ("H_LIKE_OPPOSED_HANDLES", "POSE H-LIKE PAIR: because the selected head-end-face normals follow the collision axis, roll the two complete rigid hammers about that same axis so hammer A's handle projects to one side of the seam and hammer B's handle projects to the opposite side. The pair may read visually like H versus H from this camera, but it MUST remain two separate cylinder-ended cross hammers with two separate heads, two centered joints, and two handles; never merge them into one H-shaped weapon."),
    ("PARALLEL_HANDLES_SAME_SIDE", "POSE PARALLEL HANDLES: roll both rigid hammers about the collision axis so their handles project toward the same side of the face-to-face seam. Both terminal end faces still oppose and meet; the handles and cheeks do not touch first."),
    ("DEPTH_ROLLED_HANDLES", "POSE DEPTH-ROLLED HANDLES: roll hammer A's handle toward the camera and hammer B's handle away from the camera around the shared collision axis. Keep each handle attached at its own crossbar midpoint and retain a clear view of both terminal end-face planes at the seam."),
    ("OBLIQUE_OPPOSED_HANDLES", "POSE OBLIQUE HANDLES: roll the two complete rigid hammers around the collision axis to give their handles distinct diagonal screen directions, approximately +45 and -45 degrees where this view permits. Do not bend either crossbar or rotate a head independently of its own handle."),
)

STATE_TEXT: Dict[str, str] = {
    "H0": (
        "PRE-CONTACT: the two designated FLAT CIRCULAR END CAPS at the outer ends of the opposed cylindrical head pieces "
        "are aligned cap-to-cap on the same collision axis, with a small clearly visible air gap between the circular planes. "
        "No contact, sparks, dents, cracks or overlap."
    ),
    "H2": (
        "EXACT FIRST-CONTACT PROOF FRAME: ONLY the flat circular end cap of hammer A's cylinder and the flat circular end cap "
        "of hammer B's opposing cylinder meet cap-to-cap. The two circular cap planes coincide at one shared contact centre P; "
        "their outward normals point in exactly opposite directions along the collision axis. Show the circular cap rims and "
        "the cap-to-cap seam clearly. The curved cylindrical barrel walls, crossbar sides, cross arms, corners and handles "
        "must NOT touch first. Never substitute curved-side-to-curved-side, crossbar-to-crossbar, corner-first or handle-first contact."
    ),
    "H3": (
        "IMMEDIATE POST-CONTACT: the same two designated flat circular end caps have just recoiled a small distance along "
        "the same collision axis. Keep both circular cap faces and their cylindrical bodies identifiable, with small impact "
        "marks centered on the former shared P. Preserve each cross hammer as a rigid object; no bent, twisted, telescoping "
        "or detached handle, no extra hammer, and no merged single object."
    ),
}

TOPOLOGY_LOCK = (
    "Exactly TWO separate, complete rigid cross hammers, hammer A and hammer B. Each hammer has a plus-shaped cross head "
    "with a straight horizontal crossbar and a straight vertical arm, and a single long rigid handle fixed at the exact "
    "cross-center joint. The TWO opposite ends of the horizontal crossbar each terminate in a short, solid cylinder aligned "
    "with the crossbar. Each cylinder has one flat circular end cap and one curved cylindrical barrel wall. The ONLY permitted "
    "impact surfaces are the two designated flat circular END CAPS at the OUTER ends of the opposed cylinders. Those round caps "
    "must meet cap-to-cap. The curved barrel walls are NOT striking faces. Crossbar sides, vertical arm, corners and handles "
    "are also forbidden as first-contact surfaces. Keep each entire hammer rigid: no bending, kinking, twisting, telescoping, "
    "detaching or independently rotating the handle or head. The pair may look H-like from a camera angle, but remains two "
    "separate cross hammers with two handles and two visible circular cap planes."
)

NEGATIVE = (
    "no T head, no X head, no radial sphere hammer, no axe, no blade, no spikes, no extra shaft, "
    "no third hammer, no halo of hammers, no detached head, no duplicated handle, no merged single H-shaped weapon, "
    "no flat-cap contact claimed when only curved cylinder walls touch, no crossbar-side-first contact, no cross-arm-first contact, "
    "no corner-first contact, no handle-first contact, no impossible bending, no label, no arrow, no text, no watermark, "
    "no contact sheet, no storyboard, no split screen, no collage"
)

def make_prompt(variant_id: str, camera_id: str, camera_text: str,
                axis_id: str, axis_text: str, pose_id: str, pose_text: str, state: str) -> str:
    state_clause = STATE_TEXT[state]
    return (
        "ONE standalone photorealistic 16:9 industrial-design collision-test image. "
        "This is one view of a controlled end-face contact experiment, not a diagram, not a storyboard and not a collage. "
        + TOPOLOGY_LOCK + " "
        + f"VARIANT={variant_id}; CAMERA_VIEW={camera_id}: {camera_text}. "
        + f"COLLISION_AXIS={axis_id}: {axis_text}. "
        + f"HANDLE_ROLL_VARIANT={pose_id}: {pose_text}. "
        + state_clause + " "
        + "Keep both cylinder-ended cross heads, both selected flat circular end-cap planes, both handle joints and both handles readable to the degree "
        "appropriate for this camera. Use directional neutral studio light and realistic metal materials; a narrow contrasting "
        "rim on the active end faces may clarify the two planes, but no drawn labels, arrows, lines or instructional overlay. "
        + "NEGATIVE PROMPT: " + NEGATIVE
    )

def build_matrix(outdir: Path) -> Dict[str, Any]:
    outdir.mkdir(parents=True, exist_ok=True)
    rows: List[Dict[str, Any]] = []
    variants: List[Dict[str, Any]] = []
    for cam_index, (camera_id, camera_text) in enumerate(CAMERA_VIEWS, start=1):
        for axis_index, (axis_id, axis_text) in enumerate(STRIKE_AXES, start=1):
            # Keep the requested 12 x 4 matrix at 48 variants. Rotate through all
            # four handle-roll relationships in a balanced, deterministic cycle.
            # Each camera sees all four poses; each collision axis sees each pose
            # three times across the twelve cameras.
            variant_index = len(variants)
            # Latin-style allocation: each camera gets all four poses, and each
            # collision axis sees each pose exactly three times across 12 cameras.
            pose_index = ((cam_index - 1) + (axis_index - 1)) % len(HANDLE_CLOCK_VARIANTS)
            pose_id, pose_text = HANDLE_CLOCK_VARIANTS[pose_index]
            variant_id = f"V{variant_index+1:03d}_{camera_id}_{axis_id}_{pose_id}"
            variant_dir = outdir / variant_id
            variant_dir.mkdir(parents=True, exist_ok=True)
            image_path = variant_dir / f"{variant_id}_H2.png"
            review_path = variant_dir / f"{variant_id}_H2_review.json"
            review_template_path = variant_dir / f"{variant_id}_H2_review.template.json"
            review_template = {
                "variant_id": variant_id,
                "status": "UNASSESSED",
                "image": f"{variant_id}/{image_path.name}",
                "manual_pixel_review": False,
                "checks": {name: False for name in REVIEW_CHECKS},
                "notes": "",
                "warning": "Do not set PASS unless a human has inspected the actual H2 PNG and every face-plane check is visibly true.",
            }
            review_template_path.write_text(json.dumps(review_template, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            state_files = {}
            for state in ("H0", "H2", "H3"):
                prompt = make_prompt(variant_id, camera_id, camera_text, axis_id, axis_text, pose_id, pose_text, state)
                prompt_path = variant_dir / f"{state}.txt"
                prompt_path.write_text(prompt + "\n", encoding="utf-8")
                row = {
                    "variant_id": variant_id,
                    "camera_view_id": camera_id,
                    "camera_view": camera_text,
                    "collision_axis_id": axis_id,
                    "collision_axis": axis_text,
                    "handle_roll_variant_id": pose_id,
                    "handle_roll_variant": pose_text,
                    "state": state,
                    "prompt_file": str(Path(variant_id) / prompt_path.name),
                    "prompt": prompt,
                    "expected_contact_contract": {
                        "active_surface_A": "FLAT_CIRCULAR_END_CAP",
                        "active_surface_B": "FLAT_CIRCULAR_END_CAP",
                        "plane_relation_H2": "COINCIDENT_FACE_TO_FACE",
                        "normal_relation_H2": "OPPOSITE_ALONG_COLLISION_AXIS",
                        "forbidden_first_contacts": ["CURVED_BARREL", "CROSSBAR_SIDE", "CROSS_ARM", "CORNER", "HANDLE"],
                    },
                    "image_realization": "NOT_RUN",
                    "pixel_audit": "NOT_RUN",
                }
                rows.append(row)
                state_files[state] = str(Path(variant_id) / prompt_path.name)
            variants.append({
                "variant_id": variant_id,
                "camera_view_id": camera_id,
                "collision_axis_id": axis_id,
                "handle_roll_variant_id": pose_id,
                "handle_roll_variant": pose_text,
                "state_prompt_files": state_files,
                "required_H2_image": str(Path(variant_id) / image_path.name),
                "required_H2_review": str(Path(variant_id) / review_path.name),
                "review_template": str(Path(variant_id) / review_template_path.name),
                "required_review_checks": list(REVIEW_CHECKS),
                "status": "UNASSESSED",
            })
    jsonl_path = outdir / "cylinder_cross_contact_matrix.jsonl"
    jsonl_path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
    manifest = {
        "pipeline_version": VERSION,
        "purpose": "Prove that the image model understands two rigid plus-headed cross hammers whose ONLY first-contact surfaces are opposed flat circular cylinder end caps, across camera and collision-axis variants.",
        "manual_review_contract": {
            "pass_requires": ["actual non-empty PNG image", "matching H2_review.json", "status PASS", "manual_pixel_review true", "non-empty notes", "every required review check true"],
            "automatic_pixel_claims": False,
            "blank_or_missing_evidence_status": "BLOCKED",
        },
        "camera_view_count": len(CAMERA_VIEWS),
        "collision_axis_count": len(STRIKE_AXES),
        "handle_roll_variant_count": len(HANDLE_CLOCK_VARIANTS),
        "variant_count": len(variants),
        "states_per_variant": 3,
        "single_image_prompt_count": len(rows),
        "required_H2_contact_proof_images": len(variants),
        "expected_prompt_count": len(CAMERA_VIEWS) * len(STRIKE_AXES) * 3,
        "variant_formula": "12 camera views x 4 collision axes = 48 variants; the four handle-roll relationships are deterministically balanced across the matrix; each variant has H0/H2/H3 = 144 separate image prompts",
        "handle_roll_variant_distribution": {pose_id: len(CAMERA_VIEWS) for pose_id, _ in HANDLE_CLOCK_VARIANTS},
        "handle_roll_by_camera": {
            camera_id: {
                pose_id: sum(v["camera_view_id"] == camera_id and v["handle_roll_variant_id"] == pose_id for v in variants)
                for pose_id, _ in HANDLE_CLOCK_VARIANTS
            }
            for camera_id, _ in CAMERA_VIEWS
        },
        "handle_roll_by_collision_axis": {
            axis_id: {
                pose_id: sum(v["collision_axis_id"] == axis_id and v["handle_roll_variant_id"] == pose_id for v in variants)
                for pose_id, _ in HANDLE_CLOCK_VARIANTS
            }
            for axis_id, _ in STRIKE_AXES
        },
        "topology_contract": "CYLINDER_CROSS_FLAT_CIRCULAR_END_CAP_TO_END_CAP",
        "contact_contract": {
            "surface_A": "FLAT_CIRCULAR_END_CAP_ONLY",
            "surface_B": "FLAT_CIRCULAR_END_CAP_ONLY",
            "H2_planes": "COINCIDENT",
            "H2_normals": "OPPOSITE",
            "forbidden": ["CURVED_CYLINDER_BARREL_FIRST", "CROSSBAR_SIDE_FIRST", "CROSS_ARM_OR_CORNER_FIRST", "HANDLE_FIRST"],
        },
        "generation_policy": "Every JSONL row is one separately generated image. Never ask the model for a multi-panel/contact sheet.",
        "image_realization": "NOT_RUN",
        "pixel_audit": "NOT_RUN",
        "prompt_jsonl": jsonl_path.name,
        "variants": variants,
    }
    (outdir / "contact_matrix_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest

def review_payload_passes(review: Dict[str, Any]) -> bool:
    """Accept only a complete human review record; never infer PASS from prompts."""
    checks = review.get("checks")
    return (
        review.get("status") == "PASS"
        and review.get("manual_pixel_review") is True
        and isinstance(review.get("notes"), str)
        and bool(review["notes"].strip())
        and isinstance(checks, dict)
        and all(checks.get(name) is True for name in REVIEW_CHECKS)
    )


def master_review_payload_passes(review: Dict[str, Any]) -> bool:
    """Accept a complete human cylinder-cross master review, not a prompt-derived PASS."""
    checks = review.get("checks")
    return (
        review.get("status") == "PASS"
        and review.get("manual_pixel_review") is True
        and isinstance(review.get("notes"), str)
        and bool(review["notes"].strip())
        and isinstance(checks, dict)
        and all(checks.get(name) is True for name in MASTER_REVIEW_CHECKS)
    )


def png_is_present_and_plausible(path: Path) -> bool:
    """Require a structurally complete PNG with valid chunk CRCs; this is not a visual pixel audit."""
    try:
        data = path.read_bytes()
    except OSError:
        return False
    if len(data) < 45 or data[:8] != bytes([137, 80, 78, 71, 13, 10, 26, 10]):
        return False
    cursor = 8
    saw_ihdr = saw_idat = saw_iend = False
    while cursor + 12 <= len(data):
        length = int.from_bytes(data[cursor:cursor + 4], "big")
        kind_start = cursor + 4
        payload_start = cursor + 8
        payload_end = payload_start + length
        crc_end = payload_end + 4
        if crc_end > len(data):
            return False
        kind = data[kind_start:payload_start]
        chunk_crc = int.from_bytes(data[payload_end:crc_end], "big")
        if (zlib.crc32(data[kind_start:payload_end]) & 0xFFFFFFFF) != chunk_crc:
            return False
        if not saw_ihdr:
            if kind != b"IHDR" or length != 13:
                return False
            width = int.from_bytes(data[payload_start:payload_start + 4], "big")
            height = int.from_bytes(data[payload_start + 4:payload_start + 8], "big")
            if width <= 0 or height <= 0:
                return False
            saw_ihdr = True
        elif kind == b"IHDR":
            return False
        if kind == b"IDAT":
            saw_idat = True
        if kind == b"IEND":
            if length != 0 or crc_end != len(data):
                return False
            saw_iend = True
            cursor = crc_end
            break
        cursor = crc_end
    return saw_ihdr and saw_idat and saw_iend and cursor == len(data)


def validate_master_review(image_path: Path, review_path: Path) -> Dict[str, Any]:
    """Check a real cylinder-cross shape-master PNG plus an explicit human review record."""
    issues = []
    if not png_is_present_and_plausible(image_path):
        issues.append("MISSING_OR_INVALID_MASTER_PNG")
    review = None
    try:
        review = json.loads(review_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        issues.append("MISSING_OR_INVALID_MASTER_REVIEW_JSON")
    if review is not None and not master_review_payload_passes(review):
        issues.append("MASTER_REVIEW_NOT_COMPLETE_PASS")
    return {
        "status": "PASS_MANUAL_REVIEW_RECORDED" if not issues else ("FAIL_MANUAL_REVIEW" if review and review.get("status") == "FAIL" else "BLOCKED"),
        "image_path": str(image_path),
        "review_path": str(review_path),
        "issues": issues,
    }


def validate_matrix(outdir: Path) -> Dict[str, Any]:
    """Check actual H2 files and explicit human review JSONs; cannot inspect pixels itself."""
    manifest_path = outdir / "contact_matrix_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    results = []
    variants = manifest.get("variants", [])
    for variant in variants:
        image_path = outdir / variant["required_H2_image"]
        review_path = outdir / variant["required_H2_review"]
        issues = []
        if not png_is_present_and_plausible(image_path):
            issues.append("MISSING_OR_INVALID_H2_PNG")
        review = None
        try:
            review = json.loads(review_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            issues.append("MISSING_OR_INVALID_REVIEW_JSON")
        if review is not None:
            if review.get("variant_id") != variant["variant_id"]:
                issues.append("REVIEW_VARIANT_ID_MISMATCH")
            if review.get("image") != variant["required_H2_image"]:
                issues.append("REVIEW_IMAGE_PATH_MISMATCH")
            if not review_payload_passes(review):
                issues.append("REVIEW_NOT_COMPLETE_PASS")
        if not issues:
            status = "PASS_MANUAL_REVIEW_RECORDED"
        elif review is not None and review.get("status") == "FAIL":
            status = "FAIL_MANUAL_REVIEW"
        else:
            status = "BLOCKED"
        results.append({
            "variant_id": variant["variant_id"],
            "status": status,
            "image_path": str(image_path),
            "review_path": str(review_path),
            "issues": issues,
        })
    pass_count = sum(row["status"] == "PASS_MANUAL_REVIEW_RECORDED" for row in results)
    fail_count = sum(row["status"] == "FAIL_MANUAL_REVIEW" for row in results)
    blocked_count = sum(row["status"] == "BLOCKED" for row in results)
    if pass_count == len(variants) and pass_count > 0:
        overall = "PASS_MANUAL_REVIEW_RECORDED"
    elif fail_count:
        overall = "FAIL"
    else:
        overall = "BLOCKED"
    report = {
        "pipeline_version": VERSION,
        "overall_status": overall,
        "variant_count": len(results),
        "reviewed_pass_count": pass_count,
        "reviewed_fail_count": fail_count,
        "blocked_count": blocked_count,
        "automatic_pixel_claims": False,
        "warning": "This report checks PNG presence and human review records only. The reviewer must inspect the pixels; this script does not prove which planes touch.",
        "variants": results,
    }
    (outdir / "contact_matrix_audit_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return report


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Compile 48 cylinder-cross end-cap-to-end-cap contact variants (12 cameras x 4 collision axes; four handle-roll poses balanced across the matrix) or validate actual H2 PNGs and human reviews. Never renders images.")
    parser.add_argument("--outdir", help="destination for prompts, variants and review templates")
    parser.add_argument("--validate-dir", help="validate generated H2 PNGs and manual review JSONs in an existing matrix")
    args = parser.parse_args(argv)
    if bool(args.outdir) == bool(args.validate_dir):
        parser.error("provide exactly one of --outdir or --validate-dir")
    try:
        result = build_matrix(Path(args.outdir)) if args.outdir else validate_matrix(Path(args.validate_dir))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("BLOCK: " + str(exc), file=sys.stderr)
        return 2
    keys = (
        ("camera_view_count", "collision_axis_count", "variant_count", "single_image_prompt_count", "required_H2_contact_proof_images", "image_realization", "pixel_audit")
        if args.outdir else
        ("overall_status", "variant_count", "reviewed_pass_count", "reviewed_fail_count", "blocked_count", "automatic_pixel_claims")
    )
    print(json.dumps({k: result[k] for k in keys}, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
