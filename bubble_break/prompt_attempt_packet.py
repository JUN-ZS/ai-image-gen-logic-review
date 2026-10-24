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
    from bubble_break.prompt_failure_diagnosis import diagnose_attempt
except ModuleNotFoundError:  # support direct execution as: python bubble_break/prompt_attempt_packet.py
    from prompt_evidence_board import build_svg
    from prompt_failure_diagnosis import diagnose_attempt


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

    overrides = variant.get("variables_changed")
    if isinstance(overrides, dict):
        vars_changed.update(overrides)
    expected_by_prompt = variant.get("expected_by_prompt")
    if isinstance(expected_by_prompt, dict) and isinstance(expected_by_prompt.get(prompt_id), dict):
        expected = dict(expected_by_prompt[prompt_id])
    elif isinstance(variant.get("expected"), dict):
        expected = dict(variant["expected"])

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
    resolved_topology = str(variant.get("topology_id") or ("dual_t_hammer_terminal_face_pair" if prompt_id.startswith("stage_a") else topology_id))
    manifest = {
        "schema_version": 1,
        "attempt_id": f"{variant_id}__{stage}__TRY{attempt_index:04d}",
        "branch": branch,
        "source_commit_sha": commit_sha,
        "source_matrix_sha256": matrix_sha,
        "source_artifact_path": variant.get("source_artifact_path", ""),
        "source_artifact_sha256": variant.get("source_artifact_sha256", matrix_sha),
        "source_format": variant.get("source_format", "matrix"),
        "source_record_id": variant.get("source_record_id", ""),
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
    manifest["diagnosis"] = diagnose_attempt(manifest)
    manifest["next_change"] = manifest["diagnosis"]["next_change"]
    return manifest


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
                "topology_id": manifest["topology_id"],
                "source_artifact_sha256": manifest["source_artifact_sha256"],
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
        "source_format": matrix.get("source_format", "matrix"),
        "source_artifact_path": matrix.get("source_artifact_path", str(matrix_path)),
        "source_artifact_sha256": matrix.get("source_artifact_sha256", matrix_sha),
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




def _validated_provenance(branch: str, commit_sha: str) -> None:
    if not branch.strip() or not re.fullmatch(r"[0-9a-fA-F]{40}|[0-9a-fA-F]{64}", commit_sha):
        raise ValueError("branch and an exact 40- or 64-hex source commit SHA are required for traceability")


def package_adapted_records(
    records: list[dict[str, Any]],
    source_path: Path,
    outdir: Path,
    branch: str,
    commit_sha: str,
    default_topology: str,
    source_format: str,
) -> dict[str, Any]:
    if not records:
        raise ValueError(f"no prompt records found in {source_format} input: {source_path}")
    _validated_provenance(branch, commit_sha)
    source_bytes = source_path.read_bytes()
    source_sha = hashlib.sha256(source_bytes).hexdigest()
    for record in records:
        record.setdefault("source_artifact_path", str(source_path))
        record.setdefault("source_artifact_sha256", source_sha)
        record.setdefault("source_format", source_format)
    outdir.mkdir(parents=True, exist_ok=True)
    normalized = outdir / "normalized_input_matrix.json"
    normalized.write_text(
        json.dumps({
            "source_format": source_format,
            "source_artifact_path": str(source_path),
            "source_artifact_sha256": source_sha,
            "variants": records,
        }, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )
    index = package_matrix(normalized, outdir, branch, commit_sha, default_topology)
    index["source_format"] = source_format
    index["source_artifact_path"] = str(source_path)
    index["source_artifact_sha256"] = source_sha
    (outdir / "prompt_attempt_index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    suffix = source_path.suffix or ".source"
    snapshot = outdir / f"source_artifact_snapshot{suffix}"
    if source_path.resolve() != snapshot.resolve():
        shutil.copyfile(source_path, snapshot)
    return index


def package_original_sin_jsonl(
    input_path: Path, outdir: Path, branch: str, commit_sha: str
) -> dict[str, Any]:
    raw = input_path.read_bytes()
    source_sha = hashlib.sha256(raw).hexdigest()
    records: list[dict[str, Any]] = []
    topology_map = {
        "WEAPON_C_RADIAL_SPHERE": "radial_multi_face_round_head",
        # This generator defines the T mode as an upper plane of the crossbar, not the
        # terminal-face contract used by the separate T-Hammer engine. Keep that distinction.
        "WEAPON_T": "original_sin_t_crossbar_upper_plane",
        "WEAPON_PROXY_CROSS": "original_sin_proxy_cross_upper_terminal_face",
    }
    try:
        lines = raw.decode("utf-8").splitlines()
    except UnicodeDecodeError as exc:
        raise ValueError("Original Sin input must be UTF-8 JSONL") from exc

    for line_no, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSONL record on line {line_no}: {exc}") from exc
        if not isinstance(row, dict):
            continue
        story_id = str(row.get("story_id", f"STORY_LINE_{line_no:06d}"))
        axes = row.get("axes", {}) if isinstance(row.get("axes"), dict) else {}
        prompts_by_mode = row.get("prompts", {}) if isinstance(row.get("prompts"), dict) else {}
        topology = topology_map.get(str(row.get("weapon_topology", "")), "other")
        base_variables = {
            "story_id": story_id,
            "combination_index": row.get("combination_index", "UNSPECIFIED"),
            "root_sin": row.get("root_sin", "UNSPECIFIED"),
            "causal_signature": row.get("causal_signature", "UNSPECIFIED"),
            "weapon_topology_source": row.get("weapon_topology", "UNSPECIFIED"),
            "title": row.get("title", "UNSPECIFIED"),
            "environment": axes.get("environment", {}).get("id", "UNSPECIFIED") if isinstance(axes.get("environment"), dict) else "UNSPECIFIED",
            "camera": axes.get("camera", {}).get("id", "UNSPECIFIED") if isinstance(axes.get("camera"), dict) else "UNSPECIFIED",
            "shell": axes.get("shell", {}).get("id", "UNSPECIFIED") if isinstance(axes.get("shell"), dict) else "UNSPECIFIED",
            "palette": axes.get("palette", {}).get("id", "UNSPECIFIED") if isinstance(axes.get("palette"), dict) else "UNSPECIFIED",
            "fracture": axes.get("fracture", {}).get("id", "UNSPECIFIED") if isinstance(axes.get("fracture"), dict) else "UNSPECIFIED",
        }
        coordinate = row.get("coordinate_contract", {}) if isinstance(row.get("coordinate_contract"), dict) else {}
        negative = str(row.get("negative_prompt", "") or "")
        for mode, beat_prompts in prompts_by_mode.items():
            if not isinstance(beat_prompts, dict):
                continue
            variant_prompts: dict[str, str] = {}
            expected_by_prompt: dict[str, dict[str, Any]] = {}
            for beat in ("H0", "H1", "H2", "H3"):
                text = prompt_value(beat_prompts.get(beat))
                if not text:
                    continue
                if negative:
                    text += "\n\nNEGATIVE PROMPT:\n" + negative
                variant_prompts[beat] = text
                if beat in ("H0", "H1"):
                    expected_by_prompt[beat] = {
                        "state": "pre-impact",
                        "gap_state": "positive",
                        "sphere_intact": True,
                        "early_cracks": False,
                        "camera_lock": coordinate.get("camera_lock", "same camera across H0-H3"),
                    }
                elif beat == "H2":
                    expected_by_prompt[beat] = {
                        "state": "first contact",
                        "contact_point": "P",
                        "gap": 0,
                        "active_face_contract": coordinate.get("first_contact", "SEE_SOURCE_PROMPT"),
                        "cracks_begin_at_P": True,
                        "residents_untouched": True,
                    }
                else:
                    expected_by_prompt[beat] = {
                        "state": "shell broken",
                        "cracks_origin": "P",
                        "residents_alive": True,
                        "same_scene_and_tool_topology": True,
                    }
            if variant_prompts:
                records.append({
                    "variant_id": f"{story_id}__{mode}",
                    "topology_id": topology,
                    "prompts": variant_prompts,
                    "variables_changed": {**base_variables, "mode": mode},
                    "expected_by_prompt": expected_by_prompt,
                    "audit_status": {
                        "image_realization": "NOT_RUN",
                        "pixel_audit": "NOT_RUN",
                    },
                    "source_artifact_path": str(input_path),
                    "source_artifact_sha256": source_sha,
                    "source_record_id": story_id,
                    "source_format": "original-sin-jsonl",
                })

        cells = row.get("storyboard_9", [])
        if isinstance(cells, list) and cells:
            board_prompts: dict[str, str] = {}
            expected_by_prompt = {}
            for cell in cells:
                if not isinstance(cell, dict):
                    continue
                cell_no = int(cell.get("cell", len(board_prompts) + 1))
                key = f"STORYBOARD_{cell_no:02d}"
                text = prompt_value(cell.get("prompt"))
                if text:
                    if negative:
                        text += "\n\nNEGATIVE PROMPT:\n" + negative
                    board_prompts[key] = text
                    expected_by_prompt[key] = {
                        "story_id": story_id,
                        "storyboard_cell": cell_no,
                        "narrative_role": cell.get("narrative_role", "UNSPECIFIED"),
                        "image_realization": "NOT_RUN",
                    }
            if board_prompts:
                records.append({
                    "variant_id": f"{story_id}__STORYBOARD",
                    "topology_id": topology,
                    "prompts": board_prompts,
                    "variables_changed": {**base_variables, "storyboard": "9-cell narrative beat prompts"},
                    "expected_by_prompt": expected_by_prompt,
                    "audit_status": {"image_realization": "NOT_RUN", "pixel_audit": "NOT_RUN"},
                    "source_artifact_path": str(input_path),
                    "source_artifact_sha256": source_sha,
                    "source_record_id": story_id,
                    "source_format": "original-sin-jsonl",
                })

    return package_adapted_records(
        records, input_path, outdir, branch, commit_sha,
        "other", "original-sin-jsonl"
    )


def package_dense_atlas(
    manifest_path: Path, outdir: Path, branch: str, commit_sha: str
) -> dict[str, Any]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("dense-atlas manifest root must be an object")
    prompt_rel = manifest.get("prompt_file")
    if not isinstance(prompt_rel, str) or not prompt_rel:
        raise ValueError("dense-atlas manifest has no prompt_file field")
    prompt_path = manifest_path.parent / prompt_rel
    if not prompt_path.is_file():
        raise ValueError(f"dense-atlas prompt file missing: {prompt_path}")
    prompt = prompt_path.read_text(encoding="utf-8")
    # The atlas generator hashes the prompt string before writing its trailing newline.
    prompt_sha = hashlib.sha256(prompt.rstrip("\r\n").encode("utf-8")).hexdigest()
    expected_prompt_sha = str(manifest.get("prompt_sha256", "")).lower()
    if expected_prompt_sha and expected_prompt_sha != prompt_sha:
        raise ValueError("dense-atlas prompt SHA does not match its manifest")
    variant = {
        "variant_id": "CYLINDER_CROSS_DENSE_ATLAS",
        "topology_id": "cylinder_cross_cap_pair",
        "prompts": {"DENSE_ATLAS": prompt},
        "variables_changed": {
            "canvas": manifest.get("canvas", {}).get("aspect_ratio", "UNSPECIFIED"),
            "target_collision_pairs": manifest.get("target_local_collision_count", "UNSPECIFIED"),
            "target_hammers": manifest.get("target_hammer_count", "UNSPECIFIED"),
            "required_long_handles": manifest.get("required_visible_long_handles", "UNSPECIFIED"),
            "collision_axes": manifest.get("sampling_balance", {}).get("collision_axes", "UNSPECIFIED"),
            "projection_styles": manifest.get("sampling_balance", {}).get("projection_styles", "UNSPECIFIED"),
        },
        "expected_by_prompt": {
            "DENSE_ATLAS": {
                "intended_contact": "outer flat circular end cap to end cap",
                "target_pairs": manifest.get("target_local_collision_count", "UNSPECIFIED"),
                "no_grid": manifest.get("canvas", {}).get("layout", "UNSPECIFIED"),
                "image_realization": manifest.get("generation_status", "NOT_RUN"),
                "pixel_audit": manifest.get("pixel_audit_status", "NOT_RUN"),
            }
        },
        "audit_status": {"image_realization": "NOT_RUN", "pixel_audit": "NOT_RUN"},
        "source_artifact_path": str(manifest_path),
        "source_artifact_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
        "source_record_id": "CYLINDER_CROSS_DENSE_ATLAS",
        "source_format": "dense-atlas",
    }
    return package_adapted_records(
        [variant], manifest_path, outdir, branch, commit_sha,
        "cylinder_cross_cap_pair", "dense-atlas"
    )


def package_dense_bubble(
    input_path: Path, outdir: Path, branch: str, commit_sha: str
) -> dict[str, Any]:
    summary_path = input_path / "packet_summary.json" if input_path.is_dir() else input_path
    if not summary_path.is_file():
        raise ValueError(f"dense-bubble packet summary not found: {summary_path}")
    root = summary_path.parent
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    candidate_path = root / "candidate_manifest.json"
    if not candidate_path.is_file():
        raise ValueError(f"dense-bubble candidate manifest missing: {candidate_path}")
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    source_sha = hashlib.sha256(candidate_path.read_bytes()).hexdigest()
    outputs = summary.get("outputs", [])
    stage_files = [
        name for name in outputs
        if isinstance(name, str)
        and name.endswith(".md")
        and (name.startswith("stage_a_") or name.startswith("stage_b_")
             or name.startswith("stage_c_") or name.startswith("stage_d_")
             or name.startswith("stage_e_"))
        and name != "stage_d_GATES.md"
    ]
    if not stage_files:
        raise ValueError("no stage prompt markdown files listed in dense-bubble packet_summary.json")
    ratios = candidate.get("hammer_proportions", {})
    scale = candidate.get("scale_changes", {})
    records: list[dict[str, Any]] = []
    for stage_file in stage_files:
        prompt_path = root / stage_file
        if not prompt_path.is_file():
            continue
        stage_id = prompt_path.stem.upper()
        text = prompt_path.read_text(encoding="utf-8")
        expected = {
            "topology": "double-ended planted cylinder with side-middle lateral handle",
            "selected_candidate_id": candidate.get("selected_candidate_id"),
            "source_stage_a_sha256": candidate.get("source_stage_a_sha256"),
            "hammer_proportions": ratios,
            "NO_NEW_HANDLE": scale.get("NO_NEW_HANDLE", True),
            "stage": stage_id,
            "pixel_audit": "NOT_RUN",
        }
        if stage_file.startswith("stage_a_"):
            expected.update({"sphere_intact": True, "people": 0, "cracks": 0})
        elif "step_D2" in stage_file:
            expected.update({"allowed_change": "grip the same existing side handle only"})
        elif stage_file.startswith("stage_e_"):
            expected.update({"crack_origin": "same accepted anchor P", "shell_only_break": True})
        records.append({
            "variant_id": f"PLANTED_BUBBLE_{candidate.get('selected_candidate_id') or 'UNSELECTED'}",
            "topology_id": "planted_cylinder_side_handle",
            "prompts": {stage_file.removesuffix(".md"): text},
            "variables_changed": {
                "stage": stage_id,
                "selected_candidate_id": candidate.get("selected_candidate_id", "UNSELECTED"),
                "bubble_scale": scale.get("bubble_scale", "UNSPECIFIED"),
                "hammer_scale": scale.get("hammer_scale", "UNSPECIFIED"),
                "person_to_hammer_scale": scale.get("person_to_hammer_scale", "UNSPECIFIED"),
                "head_diameter_over_bubble_diameter": ratios.get("head_diameter_over_bubble_diameter", "UNSPECIFIED"),
                "head_axial_length_over_head_diameter": ratios.get("head_axial_length_over_head_diameter", "UNSPECIFIED"),
                "lateral_handle_length_over_head_axial_length": ratios.get("lateral_handle_length_over_head_axial_length", "UNSPECIFIED"),
                "handle_diameter_over_head_diameter": ratios.get("handle_diameter_over_head_diameter", "UNSPECIFIED"),
            },
            "expected_by_prompt": {stage_file.removesuffix(".md"): expected},
            "audit_status": {"image_realization": "NOT_RUN", "pixel_audit": "NOT_RUN"},
            "source_artifact_path": str(prompt_path),
            "source_artifact_sha256": hashlib.sha256(prompt_path.read_bytes()).hexdigest(),
            "source_record_id": stage_id,
            "source_format": "dense-bubble",
        })
    index = package_adapted_records(
        records, candidate_path, outdir, branch, commit_sha,
        "planted_cylinder_side_handle", "dense-bubble"
    )
    index["source_packet_summary"] = str(summary_path)
    (outdir / "prompt_attempt_index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return index


def package_planted_bubble(
    packet_path: Path, outdir: Path, branch: str, commit_sha: str
) -> dict[str, Any]:
    packet = json.loads(packet_path.read_text(encoding="utf-8"))
    stages = packet.get("stages")
    if not isinstance(stages, dict):
        raise ValueError("planted-bubble prompt packet must contain a stages object")
    records: list[dict[str, Any]] = []
    for stage, info in stages.items():
        if not isinstance(info, dict) or not isinstance(info.get("prompt_file"), str):
            continue
        req_path = packet_path.parent / info["prompt_file"]
        if not req_path.is_file():
            raise ValueError(f"planted-bubble stage request missing: {req_path}")
        request = json.loads(req_path.read_text(encoding="utf-8"))
        prompt = prompt_value(request.get("prompt"))
        if not prompt:
            raise ValueError(f"stage request has no prompt text: {req_path}")
        records.append({
            "variant_id": f"PLANTED_BUBBLE_{stage}",
            "topology_id": "planted_cylinder_side_handle",
            "prompts": {stage: prompt},
            "variables_changed": {
                "stage": stage,
                "attempt_round": request.get("attempt_round", 0),
                "authorized_delta_fields": request.get("authorized_delta_fields", []),
                "must_preserve": request.get("must_preserve", []),
                "contract_id": request.get("contract_id", packet.get("contract_id", "UNSPECIFIED")),
            },
            "expected_by_prompt": {
                stage: {
                    "stage": stage,
                    "authorized_delta_fields": request.get("authorized_delta_fields", []),
                    "must_preserve": request.get("must_preserve", []),
                    "mask_policy": request.get("mask_policy", {}),
                    "visual_acceptance": "NOT_VERIFIED_BY_PROMPT_COMPILER",
                }
            },
            "audit_status": {"image_realization": "NOT_RUN", "pixel_audit": "NOT_RUN"},
            "source_artifact_path": str(req_path),
            "source_artifact_sha256": hashlib.sha256(req_path.read_bytes()).hexdigest(),
            "source_record_id": stage,
            "source_format": "planted-bubble-packet",
        })
    return package_adapted_records(
        records, packet_path, outdir, branch, commit_sha,
        "planted_cylinder_side_handle", "planted-bubble-packet"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--format",
        choices=["matrix", "original-sin-jsonl", "dense-atlas", "dense-bubble", "planted-bubble-packet"],
        default="matrix",
        help="source generator format to normalize into per-prompt packets"
    )
    parser.add_argument("--matrix", help="legacy alias for --input when --format=matrix")
    parser.add_argument("--input", help="input artifact: matrix JSON, JSONL, atlas manifest, packet summary/directory, or planted-bubble prompt packet")
    parser.add_argument("--outdir", required=True, help="output attempt-packet directory")
    parser.add_argument("--branch", required=True, help="exact source branch name")
    parser.add_argument("--commit-sha", required=True, help="exact 40- or 64-hex commit SHA that generated the source artifact")
    parser.add_argument("--topology-id", default="t_hammer_terminal_face", help="default topology for matrix format")
    args = parser.parse_args()
    raw_input = args.input or args.matrix
    if not raw_input:
        parser.error("supply --input (or --matrix for the legacy matrix format)")
    input_path = Path(raw_input)
    outdir = Path(args.outdir)
    if not input_path.exists():
        parser.error(f"input artifact does not exist: {input_path}")

    try:
        if args.format == "matrix":
            index = package_matrix(input_path, outdir, args.branch, args.commit_sha, args.topology_id)
        elif args.format == "original-sin-jsonl":
            index = package_original_sin_jsonl(input_path, outdir, args.branch, args.commit_sha)
        elif args.format == "dense-atlas":
            index = package_dense_atlas(input_path, outdir, args.branch, args.commit_sha)
        elif args.format == "dense-bubble":
            index = package_dense_bubble(input_path, outdir, args.branch, args.commit_sha)
        else:
            index = package_planted_bubble(input_path, outdir, args.branch, args.commit_sha)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))

    print(json.dumps({
        "outdir": args.outdir,
        "source_format": index.get("source_format", args.format),
        "variant_count": index["variant_count"],
        "attempt_count": index["attempt_count"],
        "source_matrix_sha256": index.get("source_matrix_sha256"),
        "source_artifact_sha256": index.get("source_artifact_sha256"),
        "image_realization": index["image_realization"],
        "pixel_audit": index["pixel_audit"],
        "note": "Each prompt gets prompt.txt, manifest.json, and a no-raster teaching-board placeholder. No image or pixel PASS is inferred."
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
