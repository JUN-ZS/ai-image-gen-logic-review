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
from PIL import Image

PHASES = [
    "PREFLIGHT", "TARGET_CAPTURED", "TARGET_SPEC_LOCKED", "DONOR_READY",
    "ANCHORED", "FIT_DONE", "POSE_GATE_DONE", "READY_TO_PASTE", "FINALIZED"
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
    "design_spec": "DESIGN_SPEC"
}
PHASE_ARTIFACTS = {
    "TARGET_SPEC_LOCKED": {"target_landmarks", "size_contract"},
    "DONOR_READY": {"donor_rgba", "donor_mask", "genfit_report"},
    "ANCHORED": {"donor_landmarks", "anchor_audit"},
    "FIT_DONE": {"fit_report"},
    "POSE_GATE_DONE": {"pose_report"},
    "READY_TO_PASTE": {"paste_plan"},
    "FINALIZED": {"paste_report", "pixel_audit"}
}

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def binary_mask_bbox(path: Path, threshold: int = 128):
    im = Image.open(path).convert("L")
    mask = im.point(lambda v: 255 if v >= threshold else 0)
    return mask.getbbox(), im.size

def rgba_alpha_bbox(path: Path, threshold: int = 16):
    im = Image.open(path)
    if im.mode != "RGBA":
        raise ValueError(f"donor must be true RGBA PNG, got mode={im.mode}")
    alpha = im.getchannel("A")
    mask = alpha.point(lambda v: 255 if v >= threshold else 0)
    return mask.getbbox(), im.size

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
    preflight = state.get("preflight", {})
    if preflight.get("method_id_frozen") != method:
        fail("preflight method_id does not match run method_id", errors)

    repo_root = Path(state.get("repo_root", Path(__file__).resolve().parents[3])).resolve()
    skill_file = repo_root / "skills/shengqing-huiwei/SKILL.md"
    no_repeat_file = repo_root / "skills/shengqing-huiwei/SHQ_DO_NOT_REPEAT.md"
    registry_file = repo_root / "skills/shengqing-huiwei/SHQ_METHOD_REGISTRY.json"
    for field, path in [
        ("canonical_skill_sha256", skill_file),
        ("do_not_repeat_sha256", no_repeat_file),
        ("method_registry_sha256", registry_file)
    ]:
        if not path.is_file():
            fail(f"canonical file missing: {path}", errors)
        elif preflight.get(field) != sha256(path):
            fail(f"{field} missing or stale; current canonical file was not loaded", errors)

    regression_rel = preflight.get("golden_regression_report")
    if not regression_rel:
        fail("golden_regression_report path is required", errors)
    else:
        regression_path = (repo_root / regression_rel).resolve()
        if not regression_path.is_file():
            fail(f"golden regression report missing: {regression_path}", errors)
        else:
            try:
                regression = load_json(regression_path)
                if regression.get("fixture_id") != "DDXX_MANUAL_PANEL_GOLD_01" or regression.get("status") != "PASS":
                    fail("DDXX solver golden regression did not pass", errors)
            except Exception as exc:
                fail(f"golden regression report invalid: {exc}", errors)

    phase_index = PHASES.index(phase) if phase in PHASES else 0
    required_keys = set(BASE_ARTIFACTS) if phase_index >= PHASES.index("TARGET_CAPTURED") else set()
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

        if phase_index >= PHASES.index("DONOR_READY"):
            gen = check_report_json(unit_dir, "genfit_report", artifacts, errors)
            spec = check_report_json(unit_dir, "size_contract", artifacts, errors)
            donor_rel = artifacts.get("donor_rgba")
            target_mask_rel = artifacts.get("target_silhouette")
            if gen:
                if gen.get("native_generated") is not True:
                    fail(f"{uid}: donor is not verified native-generated", errors)
                if gen.get("donor_resized_after_generation") is not False:
                    fail(f"{uid}: donor was resized after generation or provenance unknown", errors)
            if spec and donor_rel and target_mask_rel:
                donor_path = (unit_dir / donor_rel).resolve()
                target_mask_path = (unit_dir / target_mask_rel).resolve()
                try:
                    alpha_bbox, donor_canvas_wh = rgba_alpha_bbox(donor_path, int(spec.get("alpha_threshold", 16)))
                    target_bbox, target_canvas_wh = binary_mask_bbox(target_mask_path, int(spec.get("target_mask_threshold", 128)))
                    if alpha_bbox is None or target_bbox is None:
                        fail(f"{uid}: donor alpha or target silhouette mask is empty", errors)
                    else:
                        dw = alpha_bbox[2] - alpha_bbox[0]
                        dh = alpha_bbox[3] - alpha_bbox[1]
                        tw = target_bbox[2] - target_bbox[0]
                        th = target_bbox[3] - target_bbox[1]
                        s_plan = float(spec.get("scene_scale_plan", 0))
                        if s_plan <= 0:
                            fail(f"{uid}: size_contract.scene_scale_plan must be > 0", errors)
                        else:
                            req_w, req_h = round(tw * s_plan), round(th * s_plan)
                            declared = spec.get("required_native_wh", [])
                            if len(declared) != 2 or abs(float(declared[0])-req_w) > 1 or abs(float(declared[1])-req_h) > 1:
                                fail(f"{uid}: required_native_wh is not derived from TARGET mask × scene_scale_plan", errors)
                            size_tol = float(spec.get("size_tolerance", 0.08))
                            ar_tol = float(spec.get("aspect_ratio_tolerance", 0.02))
                            eps_w = abs(dw-req_w) / max(req_w, 1)
                            eps_h = abs(dh-req_h) / max(req_h, 1)
                            ar_target = tw / max(th, 1)
                            ar_donor = dw / max(dh, 1)
                            ar_err = abs(ar_donor-ar_target) / max(ar_target, 1e-9)
                            if eps_w > size_tol:
                                fail(f"{uid}: measured donor alpha width error {eps_w:.4f} exceeds {size_tol:.4f}", errors)
                            if eps_h > size_tol:
                                fail(f"{uid}: measured donor alpha height error {eps_h:.4f} exceeds {size_tol:.4f}", errors)
                            if ar_err > ar_tol:
                                fail(f"{uid}: measured donor alpha AR error {ar_err:.4f} exceeds {ar_tol:.4f}", errors)
                            genfit_measured = {"actual_alpha_bbox_wh":[dw,dh],"required_native_wh":[req_w,req_h],"eps_w":eps_w,"eps_h":eps_h,"ar_error":ar_err}
                            u.setdefault("_guard_measured_genfit", genfit_measured)
                    if gen:
                        if gen.get("aspect_ratio_pass") is not True or gen.get("width_pass") is not True or gen.get("height_pass") is not True:
                            fail(f"{uid}: GENFIT report flags must all pass", errors)
                        declared_sha = gen.get("generation_output_sha256")
                        if not declared_sha:
                            fail(f"{uid}: genfit_report must bind generation_output_sha256", errors)
                        elif declared_sha != hashes.get("donor_rgba"):
                            fail(f"{uid}: generation output SHA differs from current donor file", errors)
                    donor_mask_path = (unit_dir / artifacts["donor_mask"]).resolve()
                    mask_size = Image.open(donor_mask_path).size
                    if mask_size != donor_canvas_wh:
                        fail(f"{uid}: donor mask canvas {mask_size} != donor RGBA canvas {donor_canvas_wh}", errors)
                except Exception as exc:
                    fail(f"{uid}: unable to measure donor/target geometry: {exc}", errors)
        if phase_index >= PHASES.index("ANCHORED"):
            audit = check_report_json(unit_dir, "anchor_audit", artifacts, errors)
            if audit:
                if audit.get("semantic_labels_valid") is not True:
                    fail(f"{uid}: paired anchor semantics did not pass audit", errors)
                if audit.get("target_reference_sha256") != hashes.get("target_solo"):
                    fail(f"{uid}: anchor audit TARGET SHA does not match TARGET_SOLO", errors)
                if audit.get("donor_reference_sha256") != hashes.get("donor_rgba"):
                    fail(f"{uid}: anchor audit DONOR SHA does not match donor RGBA", errors)
                if method == "DDXX_MECHA_CORE_SIMILARITY_V1" and audit.get("annotation_type") not in {"MANUAL_SEMANTIC", "MECHA_KEYPOINT_MODEL"}:
                    fail(f"{uid}: mecha anchors must be semantic machine keypoints, not arbitrary contour points", errors)
        if phase_index >= PHASES.index("FIT_DONE"):
            fit = check_report_json(unit_dir, "fit_report", artifacts, errors)
            spec = check_report_json(unit_dir, "size_contract", artifacts, errors)
            if fit:
                if fit.get("method_id") != method:
                    fail(f"{uid}: fit_report method_id differs from frozen method", errors)
                if fit.get("fit_status") != "PASS":
                    fail(f"{uid}: fit_status is not PASS", errors)
                if fit.get("annotation_semantics_valid") is not True:
                    fail(f"{uid}: semantic anchor audit not PASS", errors)
                if fit.get("forbidden_fit_points"):
                    fail(f"{uid}: forbidden/background/rubble points included in fit", errors)
                if method == "DDXX_MECHA_CORE_SIMILARITY_V1":
                    if fit.get("annotation_type") not in {"MANUAL_SEMANTIC", "MECHA_KEYPOINT_MODEL"}:
                        fail(f"{uid}: mecha fit requires semantic machine keypoints; contour samples are not joints", errors)
                    required_core = {"head_center","chest_center","pelvis_center","left_shoulder_joint","right_shoulder_joint"}
                    if not required_core.issubset(set(fit.get("fit_anchor_names", []))):
                        fail(f"{uid}: mecha COREFIT missing one or more required core anchors", errors)
                if fit.get("scale_a") is None:
                    fail(f"{uid}: fit_report must include measured scale_a", errors)
                else:
                    a_fit = float(fit["scale_a"])
                    if a_fit <= 0:
                        fail(f"{uid}: fit scale_a must be positive", errors)
                    elif spec:
                        s_fit = 1.0 / a_fit
                        s_plan = float(spec.get("scene_scale_plan", 0))
                        tol = float(spec.get("scale_consistency_tolerance", 0.08))
                        if s_plan <= 0 or abs(s_fit-s_plan)/max(s_plan,1e-9) > tol:
                            fail(f"{uid}: fit-derived scene scale 1/a disagrees with prelocked scene_scale_plan", errors)
        if phase_index >= PHASES.index("POSE_GATE_DONE"):
            pose = check_report_json(unit_dir, "pose_report", artifacts, errors)
            if pose:
                if pose.get("pose_status") != "PASS":
                    fail(f"{uid}: target pose gate is not PASS", errors)
                if pose.get("target_to_base_status") != "PASS":
                    fail(f"{uid}: TARGET_TO_BASE must pass; BASE_TO_DETAIL alone is not pose proof", errors)
                if pose.get("primary_reference_role") != "ORIGINAL_TARGET":
                    fail(f"{uid}: pose gate did not use original TARGET as primary reference", errors)
                if pose.get("primary_reference_sha256") != hashes.get("target_solo"):
                    fail(f"{uid}: pose gate target SHA does not match TARGET_SOLO", errors)
                if pose.get("soft_to_detail_only") is True:
                    fail(f"{uid}: soft-to-detail check cannot substitute target-to-base pose gate", errors)
        if phase_index >= PHASES.index("FINALIZED"):
            paste = check_report_json(unit_dir, "paste_report", artifacts, errors)
            pixel = check_report_json(unit_dir, "pixel_audit", artifacts, errors)
            if paste:
                if float(paste.get("unit_scale", -1)) != 1.0:
                    fail(f"{uid}: unit_scale must be exactly 1.0", errors)
                if paste.get("donor_sha256") != hashes.get("donor_rgba"):
                    fail(f"{uid}: pasted donor SHA does not match accepted donor", errors)
                if paste.get("hardpaste") is not True:
                    fail(f"{uid}: final operation is not verified HARDPASTE", errors)
            if pixel:
                if pixel.get("status") != "PASS" or pixel.get("core_exact") is not True:
                    fail(f"{uid}: pixel-level hardpaste verification did not pass", errors)
                if pixel.get("donor_sha256") != hashes.get("donor_rgba"):
                    fail(f"{uid}: pixel audit donor SHA differs from accepted donor", errors)
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
    ap.add_argument("run_state", type=Path, nargs="?")
    ap.add_argument("--out", type=Path)
    ap.add_argument("--print-canonical-hashes", action="store_true")
    args = ap.parse_args()
    repo_root = Path(__file__).resolve().parents[3]
    if args.print_canonical_hashes:
        paths = {
            "canonical_skill_sha256": repo_root / "skills/shengqing-huiwei/SKILL.md",
            "do_not_repeat_sha256": repo_root / "skills/shengqing-huiwei/SHQ_DO_NOT_REPEAT.md",
            "method_registry_sha256": repo_root / "skills/shengqing-huiwei/SHQ_METHOD_REGISTRY.json"
        }
        output = {k: sha256(v) if v.is_file() else None for k, v in paths.items()}
        print(json.dumps(output, indent=2))
        raise SystemExit(0 if all(output.values()) else 2)
    if args.run_state is None:
        ap.error("run_state is required unless --print-canonical-hashes is used")
    try:
        result = check_run(args.run_state.resolve())
    except Exception as exc:
        result = {"guard": "SHQ_EXECUTION_GUARD_V1_2", "status": "BLOCK", "errors": [str(exc)]}
    raw = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(raw + "\n", encoding="utf-8")
    print(raw)
    sys.exit(0 if result.get("status") == "PASS" else 2)

if __name__ == "__main__":
    main()
