#!/usr/bin/env python3
"""Package every prompt in a matrix JSON as a traceable per-attempt bundle.

Initial adapter supports matrix objects shaped like t_hammer_multiview_swing_engine.py:
  {"variants": [{"variant_id": ..., "prompts": {...}, "geometry": ..., "axis": ..., "camera": ...}]}
It creates prompt.txt + manifest.json + a manifest-only teaching board for each prompt.
It does not generate images or promote unverified evidence to PASS.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path
from typing import Any

try:
    from bubble_break.prompt_evidence_board import build_svg
except ModuleNotFoundError:  # support direct execution as: python bubble_break/prompt_attempt_packet.py
    from prompt_evidence_board import build_svg


STAGE_IDS = {
    "stage_a_two_hammer_proof": "STAGE_A",
    "H0_preimpact": "H0",
    "H1_preimpact": "H1",
    "H2_first_contact": "H2",
    "H3_followthrough": "H3",
}


def slug(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip("-._")
    return cleaned[:140] or "unnamed"


def prompt_value(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        for key in ("prompt", "text", "content"):
            if isinstance(value.get(key), str):
                return value[key]
    return ""


def compile_manifest(
    variant: dict[str, Any],
    prompt_id: str,
    prompt_text: str,
    branch: str,
    commit_sha: str,
    matrix_sha: str,
    topology_id: str,
    attempt_index: int,
) -> dict[str, Any]:
    variant_id = str(variant.get("variant_id", f"VARIANT_{attempt_index:04d}"))
    geometry = variant.get("geometry") if isinstance(variant.get("geometry"), dict) else {}
    axis = variant.get("axis") if isinstance(variant.get("axis"), dict) else {}
    camera = variant.get("camera") if isinstance(variant.get("camera"), dict) else {}
    swing = variant.get("swing") if isinstance(variant.get("swing"), dict) else {}
    windup = variant.get("windup_profile") if isinstance(variant.get("windup_profile"), dict) else {}
    stage = STAGE_IDS.get(prompt_id, prompt_id.upper())
    off = camera.get("off_normal_deg", "UNSPECIFIED")
    orbit = camera.get("orbit_deg", "UNSPECIFIED")
    roll = camera.get("roll_deg", "UNSPECIFIED")
    vars_changed = {
        "impact_axis": axis.get("axis_id", axis.get("name_en", "UNSPECIFIED")),
        "camera": camera.get("camera_id", camera.get("name_en", "UNSPECIFIED")),
        "camera_view_deg": f"off={off}, orbit={orbit}, roll={roll}",
        "focal_mm": camera.get("focal_mm", "UNSPECIFIED"),
        "windup_profile": windup.get("profile_id", "UNSPECIFIED"),
        "handle_rolls_deg": f"A={geometry.get('roll_A', 'UNSPECIFIED')}, B={geometry.get('roll_B', 'UNSPECIFIED')}",
        "distance_contract": f"H0_total_gap={geometry.get('H0_total_gap', 'UNSPECIFIED')}, H2_gap={geometry.get('H2_gap', 'UNSPECIFIED')}, H3_advance={geometry.get('H3_advance', 'UNSPECIFIED')}",
    }
    if prompt_id.startswith("stage_a"):
        expected = {
            "contact_mode": "two independent hammer terminal faces",
            "active_surface": "terminal_end_face_to_terminal_end_face",
            "normal_dot": geometry.get("normal_dot", "UNVERIFIED"),
            "H0_total_gap_units": geometry.get("H0_total_gap", "UNVERIFIED"),
            "H2_gap_units": geometry.get("H2_gap", "UNVERIFIED"),
            "no_interpenetration": True,
        }
    elif prompt_id.startswith("H0"):
        expected = {
            "contact_mode": "single hammer to sphere; pre-impact",
            "active_surface": "terminal_end_face",
            "gap_units": 50,
            "sphere_intact": True,
            "early_cracks": False,
        }
    elif prompt_id.startswith("H2"):
        expected = {
            "contact_mode": "single hammer to sphere; first contact",
            "active_surface": "terminal_end_face",
            "contact_point_id": "P",
            "gap_units": geometry.get("H2_gap", 0),
            "normal_dot": geometry.get("normal_dot", -1.0),
            "no_interpenetration": True,
            "cracks_begin_at_P_only": True,
        }
    elif prompt_id.startswith("H3"):
        expected = {
            "contact_mode": "same rigid hammer follow-through",
            "active_surface": "terminal_end_face",
            "contact_point_id": "P",
            "advance_units": geometry.get("H3_advance", 15),
            "same_collision_axis": True,
            "cracks_propagate_from_P": True,
        }
    else:
        expected = {"contact_contract": "SEE_PROMPT_AND_BRANCH_SPEC"}

    source_status = variant.get("audit_status") if isinstance(variant.get("audit_status"), dict) else {}
    image_status = str(source_status.get("image_realization", "NOT_RUN")).upper()
    audit_status = str(source_status.get("pixel_audit", "NOT_RUN")).upper()
    if image_status not in {"NOT_RUN", "IMAGE_GENERATED", "BLOCKED", "SYNTHETIC_TEST_ONLY", "UNKNOWN"}:
        image_status = "UNKNOWN"
    if audit_status not in {"NOT_RUN", "PENDING", "PASS", "FAIL", "UNVERIFIED"}:
        audit_status = "UNVERIFIED"
    if image_status != "IMAGE_GENERATED":
        # A compiler/matrix normally has only prompt/proxy output, never a generated raster.
        audit_status = "NOT_RUN"

    prompt_sha = hashlib.sha256(prompt_text.encode("utf-8")).hexdigest()
    resolved_topology = "dual_t_hammer_terminal_face_pair" if prompt_id.startswith("stage_a") else topology_id
    return {
        "schema_version": 1,
        "attempt_id": f"{variant_id}__{stage}__TRY{attempt_index:04d}",
        "branch": branch,
        "source_commit_sha": commit_sha,
        "source_matrix_sha256": matrix_sha,
        "prompt_id": prompt_id,
        "prompt_sha256": prompt_sha,
        "variant_id": variant_id,
        "topology_id": resolved_topology,
        "stage_id": stage,
        "variables_changed": vars_changed,
        "expected": expected,
        "observed": {
            "active_surface": "UNVERIFIED",
            "contact_point_id": "UNVERIFIED",
            "measured_gap": "UNVERIFIED",
            "rigid_body_topology": "UNVERIFIED",
            "visual_causality": "UNVERIFIED",
        },
        "image_realization_status": image_status,
        "pixel_audit_status": audit_status,
        "continuity_status": "NOT_RUN",
        "failure_reasons": [],
        "next_change": "NOT GENERATED: attach the actual raster, audit the declared contact contract, then change only a measured failed variable.",
        "prompt_excerpt": prompt_text[:240],
    }


def package_matrix(
    matrix_path: Path,
    outdir: Path,
    branch: str,
    commit_sha: str,
    topology_id: str = "t_hammer_terminal_face",
) -> dict[str, Any]:
    raw = matrix_path.read_bytes()
    matrix_sha = hashlib.sha256(raw).hexdigest()
    matrix = json.loads(raw.decode("utf-8"))
    variants = matrix.get("variants")
    if not isinstance(variants, list):
        raise ValueError("input matrix must contain a 'variants' array")
    if not branch.strip() or not re.fullmatch(r"[0-9a-fA-F]{40}|[0-9a-fA-F]{64}", commit_sha):
        raise ValueError("branch and an exact 40- or 64-hex source commit SHA are required for traceability")
    outdir.mkdir(parents=True, exist_ok=True)
    index_items: list[dict[str, Any]] = []
    attempt_index = 0

    for variant in variants:
        if not isinstance(variant, dict):
            continue
        variant_id = str(variant.get("variant_id", f"VARIANT_{len(index_items):04d}"))
        prompts = variant.get("prompts")
        if not isinstance(prompts, dict):
            continue
        for prompt_id, prompt_obj in prompts.items():
            text = prompt_value(prompt_obj)
            if not text.strip():
                continue
            attempt_index += 1
            manifest = compile_manifest(
                variant, str(prompt_id), text, branch, commit_sha,
                matrix_sha, topology_id, attempt_index
            )
            folder = outdir / slug(manifest["attempt_id"])
            folder.mkdir(parents=True, exist_ok=True)
            (folder / "prompt.txt").write_text(text.rstrip() + "\n", encoding="utf-8")
            (folder / "manifest.json").write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8"
            )
            (folder / "teaching_board.svg").write_text(
                build_svg(manifest, None), encoding="utf-8"
            )
            index_items.append({
                "attempt_id": manifest["attempt_id"],
                "variant_id": variant_id,
                "prompt_id": prompt_id,
                "stage_id": manifest["stage_id"],
                "topology_id": topology_id,
                "prompt_sha256": manifest["prompt_sha256"],
                "manifest": f"{folder.name}/manifest.json",
                "prompt": f"{folder.name}/prompt.txt",
                "teaching_board": f"{folder.name}/teaching_board.svg",
                "image_realization_status": manifest["image_realization_status"],
                "pixel_audit_status": manifest["pixel_audit_status"],
            })

    index = {
        "schema_version": 1,
        "source_matrix": str(matrix_path),
        "source_matrix_sha256": matrix_sha,
        "branch": branch,
        "source_commit_sha": commit_sha,
        "topology_id": topology_id,
        "variant_count": len(variants),
        "attempt_count": len(index_items),
        "image_realization": "NOT_RUN",
        "pixel_audit": "NOT_RUN",
        "attempts": index_items,
        "warning": "Prompt packages and teaching-board placeholders are not image evidence. Attach actual rasters and SHA-bound review receipts before any visual PASS."
    }
    (outdir / "prompt_attempt_index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )
    shutil.copyfile(matrix_path, outdir / "source_matrix_snapshot.json")
    return index


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix", required=True, help="JSON matrix containing variants[*].prompts")
    parser.add_argument("--outdir", required=True, help="output attempt-packet directory")
    parser.add_argument("--branch", required=True, help="exact source branch name")
    parser.add_argument("--commit-sha", required=True, help="exact commit SHA that generated this matrix")
    parser.add_argument("--topology-id", default="t_hammer_terminal_face")
    args = parser.parse_args()
    index = package_matrix(
        Path(args.matrix), Path(args.outdir), args.branch, args.commit_sha, args.topology_id
    )
    print(json.dumps({
        "outdir": args.outdir,
        "variant_count": index["variant_count"],
        "attempt_count": index["attempt_count"],
        "source_matrix_sha256": index["source_matrix_sha256"],
        "image_realization": "NOT_RUN",
        "pixel_audit": "NOT_RUN",
        "note": "Each prompt gets prompt.txt, manifest.json, and a no-raster teaching-board placeholder."
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
