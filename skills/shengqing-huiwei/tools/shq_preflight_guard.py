#!/usr/bin/env python3
"""SHQ v1.2 evidence-backed preflight and phase gate.

This guard verifies declared artifacts and report provenance. It does not run an
image generator or claim visual correctness. A phase can advance only when the
required evidence files exist and their cross-references agree.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
from pathlib import Path

PHASES = [
    "PREFLIGHT", "TARGET_CAPTURED", "ANCHORED", "DONOR_READY",
    "FIT_DONE", "POSE_GATE_DONE", "READY_TO_PASTE", "FINALIZED"
]
METHODS = {
    "SHQ_BEST_CORE_V1_1",
    "DDXX_WHOLEBODY_SIMILARITY_V1",
    "DDXX_MECHA_CORE_SIMILARITY_V1"
}
BASE_ARTIFACTS = {
    "target_solo": "TARGET_SOLO",
    "target_pose_map": "POSE_MAP",
    "target_silhouette": "TARGET_SILHOUETTE",
    "target_landmarks": "TARGET_LANDMARKS",
    "design_spec": "DESIGN_SPEC"
}
PHASE_ARTIFACTS = {
    "DONOR_READY": {"donor_rgba", "donor_mask", "donor_landmarks", "genfit_report"},
    "FIT_DONE": {"fit_report"},
    "POSE_GATE_DONE": {"pose_report"},
    "READY_TO_PASTE": {"paste_plan"},
    "FINALIZED": {"paste_report"}
}

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def fail(msg: str, errors: list[str]):
    errors.append(msg)

def check_report_json(unit_dir: Path, key: str, artifacts: dict, errors: list[str]):
    rel = artifacts.get(key)
    if not rel:
        fail(f"missing artifact path: {key}", errors)
        return None
    p = (unit_dir / rel).resolve()
    if not p.is_file():
        fail(f"missing file: {key}={p}", errors)
        return None
    try:
        return load_json(p)
    except Exception as exc:
        fail(f"invalid JSON {key}: {exc}", errors)
        return None

def check_run(run_path: Path):
    errors = []
    state = load_json(run_path)
    root = run_path.parent
    if state.get("schema_version") != "SHQ-RUN-1.2":
        fail("schema_version must be SHQ-RUN-1.2", errors)
    method = state.get("method_id")
    if method not in METHODS:
        fail(f"method_id must be one of {sorted(METHODS)}", errors)
    phase = state.get("phase")
    if phase not in PHASES:
        fail(f"unknown phase: {phase}", errors)
    task = state.get("task", {})
    mode = task.get("mode")
    units = state.get("units", [])
    expected_n = int(task.get("unit_count", -1))
    if mode not in {"SINGLE", "MULTI"}:
        fail("task.mode must be SINGLE or MULTI", errors)
    if expected_n != len(units) or expected_n < 1:
        fail(f"unit_count mismatch: declared={expected_n}, listed={len(units)}", errors)
    if mode == "SINGLE" and expected_n != 1:
        fail("SINGLE task must contain exactly one unit", errors)
    if mode == "MULTI" and expected_n < 2:
        fail("MULTI task must contain at least two units", errors)
    ids = [u.get("unit_id") for u in units]
    if len(set(ids)) != len(ids) or any(not x for x in ids):
        fail("unit_id values must be present and unique", errors)
    if mode == "MULTI" and task.get("solo_then_compose") is not True:
        fail("MULTI requires solo_then_compose=true; group plate is not canonical", errors)
    if state.get("preflight", {}).get("canonical_skill_loaded") is not True:
        fail("canonical_skill_loaded must be evidence-backed true", errors)
    if state.get("preflight", {}).get("do_not_repeat_loaded") is not True:
        fail("do_not_repeat_loaded must be evidence-backed true", errors)
    if state.get("preflight", {}).get("golden_solver_regression") != "PASS":
        fail("golden_solver_regression must be PASS before production run", errors)
    if state.get("preflight", {}).get("method_id_frozen") != method:
        fail("preflight method_id does not match run method_id", errors)

    phase_index = PHASES.index(phase) if phase in PHASES else 0
    required_keys = set(BASE_ARTIFACTS)
    for pidx, p_name in enumerate(PHASES):
        if phase_index >= pidx and p_name in PHASE_ARTIFACTS:
            required_keys |= PHASE_ARTIFACTS[p_name]

    donor_hashes = []
    unit_summaries = []
    for u in units:
        uid = u.get("unit_id", "UNKNOWN")
        unit_dir = (root / u.get("unit_dir", uid)).resolve()
        artifacts = u.get("artifacts", {})
        for key in sorted(required_keys):
            if key not in artifacts:
                fail(f"{uid}: missing required artifact key {key}", errors)
                continue
            path = (unit_dir / artifacts[key]).resolve()
            if not path.is_file():
                fail(f"{uid}: missing {key} file {path}", errors)
        hashes = {}
        for key in ("target_solo", "target_pose_map", "target_silhouette", "donor_rgba"):
            rel = artifacts.get(key)
            if rel:
                p = (unit_dir / rel).resolve()
                if p.is_file():
                    hashes[key] = sha256(p)
        # If a source SHA was recorded, it must still match the exact file.
        expected_target_sha = u.get("target_solo_sha256")
        if expected_target_sha and hashes.get("target_solo") != expected_target_sha:
            fail(f"{uid}: TARGET_SOLO SHA mismatch / target changed mid-run", errors)
        if hashes.get("donor_rgba"):
            donor_hashes.append(hashes["donor_rgba"])

        if phase_index >= PHASES.index("FIT_DONE"):
            fit = check_report_json(unit_dir, "fit_report", artifacts, errors)
            if fit:
                if fit.get("method_id") != method:
                    fail(f"{uid}: fit_report method_id differs from frozen method", errors)
                if fit.get("fit_status") != "PASS":
                    fail(f"{uid}: fit_status is not PASS", errors)
                if fit.get("annotation_semantics_valid") is not True:
                    fail(f"{uid}: semantic anchor audit not PASS", errors)
                if fit.get("forbidden_fit_points"):
                    fail(f"{uid}: forbidden/background/rubble points included in fit", errors)
                if method == "DDXX_MECHA_CORE_SIMILARITY_V1" and fit.get("annotation_type") not in {"MANUAL_SEMANTIC", "MECHA_KEYPOINT_MODEL"}:
                    fail(f"{uid}: mecha fit requires semantic machine keypoints; contour samples are not joints", errors)
        if phase_index >= PHASES.index("DONOR_READY"):
            gen = check_report_json(unit_dir, "genfit_report", artifacts, errors)
            if gen:
                if gen.get("native_generated") is not True:
                    fail(f"{uid}: donor is not verified native-generated", errors)
                if gen.get("donor_resized_after_generation") is not False:
                    fail(f"{uid}: donor was resized after generation or provenance unknown", errors)
                if gen.get("aspect_ratio_pass") is not True:
                    fail(f"{uid}: donor aspect ratio gate did not pass", errors)
                if gen.get("width_pass") is not True or gen.get("height_pass") is not True:
                    fail(f"{uid}: both width and height must pass", errors)
        if phase_index >= PHASES.index("POSE_GATE_DONE"):
            pose = check_report_json(unit_dir, "pose_report", artifacts, errors)
            if pose:
                if pose.get("pose_status") != "PASS":
                    fail(f"{uid}: target pose gate is not PASS", errors)
                if pose.get("primary_reference_role") != "ORIGINAL_TARGET":
                    fail(f"{uid}: pose gate did not use original TARGET as primary reference", errors)
                if pose.get("primary_reference_sha256") != hashes.get("target_solo"):
                    fail(f"{uid}: pose gate target SHA does not match TARGET_SOLO", errors)
                if pose.get("soft_to_detail_only") is True:
                    fail(f"{uid}: soft-to-detail check cannot substitute target-to-base pose gate", errors)
        if phase_index >= PHASES.index("FINALIZED"):
            paste = check_report_json(unit_dir, "paste_report", artifacts, errors)
            if paste:
                if float(paste.get("unit_scale", -1)) != 1.0:
                    fail(f"{uid}: unit_scale must be exactly 1.0", errors)
                if paste.get("core_exact") is not True:
                    fail(f"{uid}: core_exact did not pass", errors)
                if paste.get("donor_sha256") != hashes.get("donor_rgba"):
                    fail(f"{uid}: pasted donor SHA does not match accepted donor", errors)
                if paste.get("hardpaste") is not True:
                    fail(f"{uid}: final operation is not verified HARDPASTE", errors)
        unit_summaries.append({"unit_id": uid, "hashes": hashes})

    if mode == "MULTI" and donor_hashes and len(donor_hashes) != len(set(donor_hashes)):
        fail("MULTI donor SHA collision: separate units unexpectedly share identical donor bytes", errors)
    if mode == "MULTI" and phase_index >= PHASES.index("FINALIZED"):
        comp = state.get("composition", {})
        if comp.get("mode") != "MULTI_RETURN":
            fail("final multi composition mode must be MULTI_RETURN", errors)
        if not comp.get("z_order_far_to_near"):
            fail("multi composition needs explicit z_order_far_to_near", errors)
        ratios = comp.get("slot_ratios", {})
        if set(ratios) != set(ids):
            fail("slot_ratios must be declared for every unit", errors)
        bad = {k: v for k, v in ratios.items() if abs(float(v) - 1.0) > float(comp.get("slot_ratio_tolerance", 0.02))}
        if bad and comp.get("status") != "MULTI_SCALE_COMPROMISE":
            fail("non-unit slot ratios must be explicitly labelled MULTI_SCALE_COMPROMISE", errors)

    result = {
        "guard": "SHQ_EXECUTION_GUARD_V1_2",
        "run_id": state.get("run_id"),
        "phase": phase,
        "method_id": method,
        "task_mode": mode,
        "unit_count": expected_n,
        "unit_summaries": unit_summaries,
        "status": "PASS" if not errors else "BLOCK",
        "errors": errors
    }
    return result

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_state", type=Path)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    try:
        result = check_run(args.run_state.resolve())
    except Exception as exc:
        result = {"guard": "SHQ_EXECUTION_GUARD_V1_2", "status": "BLOCK", "errors": [str(exc)]}
    raw = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.write_text(raw + "\n", encoding="utf-8")
    print(raw)
    sys.exit(0 if result.get("status") == "PASS" else 2)

if __name__ == "__main__":
    main()
