#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compile an exhaustive single-image T-hammer end-face collision matrix.

This creates prompts and audit manifests only. It never calls an image model.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

VERSION = "1.1.0"

REVIEW_CHECKS = (
    "two_distinct_T_hammers",
    "active_terminal_face_A_identified",
    "active_terminal_face_B_identified",
    "both_terminal_end_faces_coincident",
    "face_normals_opposite",
    "no_cheek_first",
    "no_upper_lower_long_surface_first",
    "no_corner_first",
    "no_handle_first",
)

CAMERA_VIEWS: Tuple[Tuple[str, str], ...] = (
    ("FACE_ON", "near head-on along the collision axis, both rectangular terminal END FACES fully visible and the seam centered"),
    ("SIDE_PROFILE", "true side profile perpendicular to the collision axis, both T profiles readable and the contact seam visible"),
    ("FRONT_THREE_QUARTER", "front three-quarter view about 35 degrees off the collision axis, showing each end-face plane and its cheek depth"),
    ("REVERSE_THREE_QUARTER", "reverse three-quarter view from the opposite side about 35 degrees off the collision axis, showing the same face-to-face joint"),
    ("LOW_ANGLE", "low camera angle slightly below the heads, looking up while retaining a clear view of both terminal faces"),
    ("HIGH_ANGLE", "high camera angle slightly above the heads, looking down while retaining a clear view of both terminal faces"),
    ("OVERHEAD", "overhead view from above the hammer pair, with both selected END FACES and their shared contact point unoccluded"),
    ("DUTCH_ROLL", "controlled 15-degree Dutch roll; the camera rolls, but neither hammer nor either contact plane bends"),
    ("MACRO_SEAM", "tight macro of the exact face-to-face seam, including enough adjacent crossbar and handle-joint geometry to identify both separate T hammers"),
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

STATE_TEXT: Dict[str, str] = {
    "H0": (
        "PRE-CONTACT: both designated END STRIKING FACES are aligned face-to-face on the same collision axis, "
        "with a small, plainly visible air gap between the two planes. The gap is the only separation along the "
        "collision axis; no sparks, no contact, no dents, no cracks, no overlap."
    ),
    "H2": (
        "EXACT FIRST-CONTACT PROOF FRAME: the designated terminal END STRIKING FACE of hammer A and the designated "
        "terminal END STRIKING FACE of hammer B meet face-to-face. Their planar contact patches are coincident at one "
        "shared contact centre P; the two outward face normals point in exactly opposite directions along the collision "
        "axis. Show both actual face planes meeting at the same seam. There is zero visible gap and zero interpenetration. "
        "The broad long side walls/cheeks, upper and lower non-terminal surfaces, corners, T-stems and handles do NOT "
        "touch first. No model may substitute cheek-to-cheek, top-plane-to-top-plane, handle-first or corner-first contact. "
        "This frame exists to prove which planes touch, not merely to depict two T shapes near each other."
    ),
    "H3": (
        "IMMEDIATE POST-CONTACT: the same two designated END STRIKING FACES have just recoiled a small distance along "
        "the same collision axis after their face-to-face impact. Both contact faces remain identifiable, with matching "
        "small central impact marks at the former shared P; no side wall, corner or handle has made the first contact. "
        "Preserve each hammer's rigid geometry; no extra hammer, no merged H-shaped single object, no bent bars."
    ),
}

TOPOLOGY_LOCK = (
    "Exactly TWO separate, complete T-headed hammers, hammer A and hammer B. Each hammer has ONE straight rigid "
    "rectangular crossbar/head and ONE handle joined to the head's defined central handle joint; the handle belongs "
    "to that hammer only. Each crossbar remains straight, rectangular and rigid. Each hammer has a designated terminal "
    "END STRIKING FACE on the end of its crossbar. The active surface is that terminal end face, NOT the broad cheek/"
    "long side wall and NOT the broad upper or lower surface of the crossbar. Orient the complete rigid hammer in "
    "three-dimensional space so the selected terminal faces oppose one another; do not bend or reshape the T to fake contact. "
    "When viewed from particular directions, the two-head composition may look H-like at the joint, but it must remain "
    "two real T hammers with two distinct handles and two separately identifiable terminal face planes."
)

NEGATIVE = (
    "no plus-sign cross hammer, no X head, no radial sphere hammer, no axe, no blade, no spikes, no extra shaft, "
    "no third hammer, no halo of hammers, no detached head, no duplicated handle, no merged single H-shaped weapon, "
    "no face-on-face contact claimed when only cheeks touch, no top-plane contact, no side-wall-first contact, "
    "no corner-first contact, no handle-first contact, no impossible bending, no label, no arrow, no text, no watermark, "
    "no contact sheet, no storyboard, no split screen, no collage"
)

def make_prompt(variant_id: str, camera_id: str, camera_text: str,
                axis_id: str, axis_text: str, state: str) -> str:
    state_clause = STATE_TEXT[state]
    return (
        "ONE standalone photorealistic 16:9 industrial-design collision-test image. "
        "This is one view of a controlled end-face contact experiment, not a diagram, not a storyboard and not a collage. "
        + TOPOLOGY_LOCK + " "
        + f"VARIANT={variant_id}; CAMERA_VIEW={camera_id}: {camera_text}. "
        + f"COLLISION_AXIS={axis_id}: {axis_text}. "
        + state_clause + " "
        + "Keep both T heads, both selected terminal face planes, both handle joints and both handles readable to the degree "
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
            variant_id = f"V{len(variants)+1:03d}_{camera_id}_{axis_id}"
            variant_dir = outdir / variant_id
            variant_dir.mkdir(parents=True, exist_ok=True)
            image_path = variant_dir / f"{variant_id}_H2.png"
            review_path = variant_dir / f"{variant_id}_H2_review.json"
            review_template_path = variant_dir / f"{variant_id}_H2_review.template.json"
            review_template = {
                "variant_id": variant_id,
                "status": "UNASSESSED",
                "image": str(image_path),
                "manual_pixel_review": False,
                "checks": {name: False for name in REVIEW_CHECKS},
                "notes": "",
                "warning": "Do not set PASS unless a human has inspected the actual H2 PNG and every face-plane check is visibly true.",
            }
            review_template_path.write_text(json.dumps(review_template, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            state_files = {}
            for state in ("H0", "H2", "H3"):
                prompt = make_prompt(variant_id, camera_id, camera_text, axis_id, axis_text, state)
                prompt_path = variant_dir / f"{state}.txt"
                prompt_path.write_text(prompt + "\n", encoding="utf-8")
                row = {
                    "variant_id": variant_id,
                    "camera_view_id": camera_id,
                    "camera_view": camera_text,
                    "collision_axis_id": axis_id,
                    "collision_axis": axis_text,
                    "state": state,
                    "prompt_file": str(prompt_path),
                    "prompt": prompt,
                    "expected_contact_contract": {
                        "active_surface_A": "TERMINAL_END_STRIKING_FACE",
                        "active_surface_B": "TERMINAL_END_STRIKING_FACE",
                        "plane_relation_H2": "COINCIDENT_FACE_TO_FACE",
                        "normal_relation_H2": "OPPOSITE_ALONG_COLLISION_AXIS",
                        "forbidden_first_contacts": ["CHEEK", "UPPER_OR_LOWER_LONG_SURFACE", "CORNER", "STEM", "HANDLE"],
                    },
                    "image_realization": "NOT_RUN",
                    "pixel_audit": "NOT_RUN",
                }
                rows.append(row)
                state_files[state] = str(prompt_path)
            variants.append({
                "variant_id": variant_id,
                "camera_view_id": camera_id,
                "collision_axis_id": axis_id,
                "state_prompt_files": state_files,
                "required_H2_image": str(image_path),
                "required_H2_review": str(review_path),
                "review_template": str(review_template_path),
                "required_review_checks": list(REVIEW_CHECKS),
                "status": "UNASSESSED",
            })
    jsonl_path = outdir / "t_contact_matrix.jsonl"
    jsonl_path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
    manifest = {
        "pipeline_version": VERSION,
        "purpose": "Prove that the image model understands T-hammer terminal END-FACE-to-END-FACE first contact across camera and collision-axis variants.",
        "manual_review_contract": {
            "pass_requires": ["actual non-empty PNG image", "matching H2_review.json", "status PASS", "manual_pixel_review true", "non-empty notes", "every required review check true"],
            "automatic_pixel_claims": False,
            "blank_or_missing_evidence_status": "BLOCKED",
        },
        "camera_view_count": len(CAMERA_VIEWS),
        "collision_axis_count": len(STRIKE_AXES),
        "variant_count": len(variants),
        "states_per_variant": 3,
        "single_image_prompt_count": len(rows),
        "required_H2_contact_proof_images": len(variants),
        "expected_prompt_count": len(CAMERA_VIEWS) * len(STRIKE_AXES) * 3,
        "topology_contract": "T_TO_T_TERMINAL_END_FACE_TO_TERMINAL_END_FACE",
        "contact_contract": {
            "surface_A": "TERMINAL_END_STRIKING_FACE",
            "surface_B": "TERMINAL_END_STRIKING_FACE",
            "H2_planes": "COINCIDENT",
            "H2_normals": "OPPOSITE",
            "forbidden": ["CHEEK_FIRST", "TOP_OR_BOTTOM_LONG_SURFACE_FIRST", "CORNER_FIRST", "HANDLE_FIRST"],
        },
        "generation_policy": "Every JSONL row is one separately generated image. Never ask the model for a multi-panel/contact sheet.",
        "image_realization": "NOT_RUN",
        "pixel_audit": "NOT_RUN",
        "prompt_jsonl": str(jsonl_path),
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


def png_is_present_and_plausible(path: Path) -> bool:
    """Fail closed on missing, empty or non-PNG placeholders; this is not a visual pixel audit."""
    try:
        data = path.read_bytes()
    except OSError:
        return False
    return len(data) >= 33 and data.startswith(bytes([137, 80, 78, 71, 13, 10, 26, 10])) and data[12:16] == b"IHDR"


def validate_matrix(outdir: Path) -> Dict[str, Any]:
    """Check actual H2 files and explicit human review JSONs; cannot inspect pixels itself."""
    manifest_path = outdir / "contact_matrix_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    results = []
    variants = manifest.get("variants", [])
    for variant in variants:
        image_path = Path(variant["required_H2_image"])
        review_path = Path(variant["required_H2_review"])
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
    parser = argparse.ArgumentParser(description="Compile T-to-T contact prompts or validate generated H2 PNGs and explicit human reviews. Never renders images.")
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
