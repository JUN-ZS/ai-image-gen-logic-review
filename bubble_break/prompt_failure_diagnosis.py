#!/usr/bin/env python3
"""Rule-based, evidence-gated next-change diagnosis for image prompt attempts.

This module does not inspect pixels or pretend to be a vision model. It consumes
structured observations written by a reviewer (or a separately validated vision
audit) and proposes one minimal, topology-specific next experiment.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


RULES: dict[str, dict[str, Any]] = {
    "WRONG_CONTACT_FACE": {
        "priority": 10, "severity": "BLOCKING",
        "when": "observed.active_surface is a cheek/sidewall/corner/handle/center joint rather than the topology's designated active surface, or failure_codes explicitly says WRONG_CONTACT_FACE.",
        "change": "Only the declared rigid-body approach orientation/trajectory needed to present the specified active face to P; do not change weapon topology or add a shaft.",
        "edit_only": ["weapon_rigid_pose", "approach_vector", "active_face_orientation"],
        "freeze": ["weapon_topology", "head_handle_joint", "target_geometry", "camera_rig", "character_identity", "scene_landmarks"],
        "delta": "Use the approved weapon topology. Rotate/translate the entire rigid weapon as one body so its designated active face, not the cheek/sidewall/corner/handle, is the first surface at P. Preserve the existing head-handle joint and approach path after the face is correctly presented.",
        "expect": "reviewed active_surface equals the topology's declared active face; all forbidden surfaces remain clear.",
    },
    "GAP_REMAINS": {
        "priority": 20, "severity": "BLOCKING",
        "when": "the audited contact frame has a measured positive gap above tolerance.",
        "change": "Translate the same rigid body along the declared collision normal by the measured residual gap; change no scale, camera, topology, or effects.",
        "edit_only": ["weapon_translation_along_collision_normal"],
        "freeze": ["weapon_topology", "head_handle_joint", "weapon_rotation", "target_geometry", "camera_rig", "crack_state", "scene_landmarks"],
        "delta": "The reviewed H2 still has a positive face-to-sphere gap. Translate the same rigid weapon toward P along the existing collision normal by the measured residual gap only. Do not rotate, scale, redesign, or add effects. Target gap is zero without interpenetration.",
        "expect": "measured gap is zero within the declared tolerance and penetration depth is zero.",
    },
    "INTERPENETRATION": {
        "priority": 15, "severity": "BLOCKING",
        "when": "audited penetration_depth_units is positive, or the reviewer explicitly records mesh interpenetration.",
        "change": "Move the same rigid body outward along the collision normal by the measured penetration depth; do not rescale geometry.",
        "edit_only": ["weapon_translation_along_collision_normal"],
        "freeze": ["weapon_topology", "head_handle_joint", "weapon_rotation", "target_geometry", "camera_rig", "crack_state"],
        "delta": "The reviewed contact frame intersects the target. Retract the same rigid weapon along the inverse collision normal by the measured penetration depth only; preserve pose and scale. Re-establish exact face contact at P without a gap or overlap.",
        "expect": "penetration depth becomes zero and the active-face gap remains zero within tolerance.",
    },
    "WRONG_CRACK_ORIGIN": {
        "priority": 30, "severity": "BLOCKING",
        "when": "the audited crack origin is not P.",
        "change": "Change only the shell fracture-origin/effect mask so the first crack begins at the accepted P; freeze weapon pose and target geometry.",
        "edit_only": ["crack_origin", "fracture_effect_region"],
        "freeze": ["weapon_topology", "weapon_pose", "contact_point_P", "camera_rig", "character_identity", "background_landmarks", "inner_sanctuary"],
        "delta": "Keep the accepted contact geometry and P fixed. Remove crack paths that originate elsewhere. Rebuild only the shell fracture effect so the first micro-crack begins exactly at P and propagates outward from that same anchor.",
        "expect": "first crack origin equals P; no pre-existing or unrelated crack origin remains.",
    },
    "EARLY_CRACKS": {
        "priority": 25, "severity": "BLOCKING",
        "when": "H0/H1 or another pre-contact state contains cracks/contact glow before contact.",
        "change": "Edit only pre-contact shell/effect state to restore an intact sphere; freeze weapon, person, camera, and scene.",
        "edit_only": ["precontact_shell_state", "contact_glow"],
        "freeze": ["weapon_topology", "weapon_pose", "character_identity", "camera_rig", "scene_landmarks"],
        "delta": "This is a pre-contact frame. Remove all cracks, impact glow, sparks, debris, and contact shadows that imply an earlier hit. Restore a pristine intact sphere while keeping the existing positive air gap and every unrelated pixel locked.",
        "expect": "sphere is intact and no contact effect is visible before H2.",
    },
    "HANDLE_TOPOLOGY_FAIL": {
        "priority": 5, "severity": "BLOCKING",
        "when": "the handle is missing, newly invented, bent, detached, or attached at the wrong point.",
        "change": "Rollback to the last PASS parent; restore the same handle/head topology using parent pixel locks. Do not try to fix it with camera or effects.",
        "edit_only": ["restore_from_last_pass_parent", "existing_handle_roi"],
        "freeze": ["weapon_topology", "head_handle_joint", "handle_axis", "weapon_scale", "camera_rig", "contact_point_P"],
        "delta": "Rollback to the last accepted parent raster. Restore the same existing straight handle and original head-handle joint. Freeze the existing handle ROI; do not add, extend, duplicate, bend, detach, or move the handle. Do not proceed to later stages until the handle gate passes.",
        "expect": "same handle track and head joint as the last PASS parent; no new or missing handle.",
    },
    "CAMERA_OBSCURES_CONTACT": {
        "priority": 60, "severity": "REVIEW_BLOCK",
        "when": "the intended contact seam/active face cannot be inspected because of occlusion or projection.",
        "change": "Change camera view only; preserve world-space collision geometry and contact state.",
        "edit_only": ["camera_view"],
        "freeze": ["world_collision_axis", "weapon_pose", "contact_point_P", "target_geometry", "character_identity", "scene_landmarks"],
        "delta": "Change only the camera to a grazing three-quarter view that exposes the active-face boundary and contact seam. Keep the same world-space weapon pose, collision normal, P, target geometry, and scene. Do not use the new angle to change or conceal the physical contact.",
        "expect": "reviewer can distinguish the active face from cheek/sidewall and inspect P.",
    },
    "SCENE_CONTINUITY_FAIL": {
        "priority": 50, "severity": "BLOCKING",
        "when": "background landmark, scene identity, or camera-rig continuity differs from the accepted parent without authorization.",
        "change": "Rollback to last PASS parent and freeze scene/background; edit only the authorized motion/effect region.",
        "edit_only": ["authorized_delta_region"],
        "freeze": ["scene_id", "camera_rig", "background_landmarks", "sphere_center_radius", "contact_point_P", "weapon_topology"],
        "delta": "Return to the last accepted parent image. Preserve scene ID, camera rig, background landmarks, sphere placement, and P. Reapply only the authorized edit mask for this stage; do not regenerate the whole composition.",
        "expect": "all locked landmarks match the parent within the project's declared tolerances.",
    },
    "IDENTITY_DRIFT": {
        "priority": 55, "severity": "BLOCKING",
        "when": "the character identity or scale changes outside the allowed tolerance.",
        "change": "Rollback to last PASS parent; restore character reference/identity lock and keep the contact geometry frozen.",
        "edit_only": ["character_identity_roi", "authorized_pose_delta"],
        "freeze": ["weapon_topology", "weapon_pose", "contact_point_P", "camera_rig", "scene_landmarks"],
        "delta": "Use the last PASS character raster/reference to restore the same face, hair, outfit, and scale. Change only the authorized pose region. Freeze the hammer, sphere, P, camera, and background.",
        "expect": "character identity and scale satisfy the declared continuity gates; weapon/contact geometry is unchanged.",
    },
    "RESIDENT_SAFETY_FAIL": {
        "priority": 8, "severity": "BLOCKING",
        "when": "shell fragments/effects damage or obscure protected inhabitants/sanctuary.",
        "change": "Change only fragment trajectories/effect mask and protect the sanctuary ROI; do not alter the accepted contact geometry.",
        "edit_only": ["fragment_trajectory", "effect_mask", "sanctuary_protection_roi"],
        "freeze": ["weapon_topology", "contact_point_P", "accepted_crack_origin", "character_identity", "camera_rig"],
        "delta": "Keep the accepted weapon pose, contact point, and crack origin fixed. Redirect shell fragments outward and away from the sanctuary; remove effects inside the protected ROI. Do not damage or obscure the inhabitants.",
        "expect": "protected residents and sanctuary remain visible, intact, and untouched.",
    },
    "FOLLOWTHROUGH_MISMATCH": {
        "priority": 40, "severity": "BLOCKING",
        "when": "H3 advance is absent, in the wrong direction, or differs from the declared advance beyond tolerance.",
        "change": "Change only rigid-body translation along the existing collision normal by the measured advance error.",
        "edit_only": ["weapon_translation_along_collision_normal"],
        "freeze": ["weapon_topology", "head_handle_joint", "weapon_rotation", "contact_point_P", "camera_rig", "scene_landmarks"],
        "delta": "Keep the accepted H2 as parent. Translate the same rigid hammer along the declared collision normal to the H3 target advance only. Do not independently rotate the head, bend the handle, change the camera, or create new cracks away from P.",
        "expect": "measured H3 advance matches the declared target; the weapon remains rigid and the crack origin remains P.",
    },
    "INSUFFICIENT_EVIDENCE": {
        "priority": 999, "severity": "HOLD",
        "when": "there is no structured observation or explicit reviewer failure code tied to the actual raster.",
        "change": "Do not alter the formula yet. Attach and inspect the actual raster, then record which invariant failed.",
        "edit_only": [],
        "freeze": ["all_variables_until_evidence"],
        "delta": "NO REPAIR PROMPT YET. The actual raster has not supplied a measured failure. Attach the exact generated raster and a SHA-bound review record; record the observed contact surface, gap/penetration, crack origin, handle integrity, camera visibility, continuity, and resident safety before choosing a repair.",
        "expect": "actual raster and structured observations are available; diagnosis is no longer HOLD.",
    },
}

ALIASES = {
    "WRONG_FACE": "WRONG_CONTACT_FACE",
    "SIDEWALL_FIRST": "WRONG_CONTACT_FACE",
    "CHEEK_FIRST": "WRONG_CONTACT_FACE",
    "HANDLE_FIRST": "HANDLE_TOPOLOGY_FAIL",
    "NEW_HANDLE": "HANDLE_TOPOLOGY_FAIL",
    "MISSING_HANDLE": "HANDLE_TOPOLOGY_FAIL",
    "BENT_HANDLE": "HANDLE_TOPOLOGY_FAIL",
    "DETACHED_HANDLE": "HANDLE_TOPOLOGY_FAIL",
    "GAP_NONZERO": "GAP_REMAINS",
    "GAP_REMAINS": "GAP_REMAINS",
    "PENETRATION": "INTERPENETRATION",
    "INTERPENETRATION": "INTERPENETRATION",
    "CRACK_WRONG_ORIGIN": "WRONG_CRACK_ORIGIN",
    "CRACK_ORIGIN_WRONG": "WRONG_CRACK_ORIGIN",
    "CRACK_BEFORE_CONTACT": "EARLY_CRACKS",
    "EARLY_CRACKS": "EARLY_CRACKS",
    "CAMERA_HIDES_SEAM": "CAMERA_OBSCURES_CONTACT",
    "CAMERA_OBSCURES_CONTACT": "CAMERA_OBSCURES_CONTACT",
    "BACKGROUND_DRIFT": "SCENE_CONTINUITY_FAIL",
    "SCENE_DRIFT": "SCENE_CONTINUITY_FAIL",
    "IDENTITY_DRIFT": "IDENTITY_DRIFT",
    "RESIDENTS_HARMED": "RESIDENT_SAFETY_FAIL",
    "SANCTUARY_OBSCURED": "RESIDENT_SAFETY_FAIL",
    "FOLLOWTHROUGH_MISMATCH": "FOLLOWTHROUGH_MISMATCH",
}

UNVERIFIED = {"UNVERIFIED", "UNKNOWN", "NOT_RUN", "PENDING", "", None}
TOLERANCE = 1e-3


def _number(value: Any) -> float | None:
    try:
        result = float(value)
        return result if result == result and abs(result) != float("inf") else None
    except (TypeError, ValueError):
        return None


def _truth(value: Any) -> bool | None:
    if value in UNVERIFIED:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)) and value in (0, 1):
        return bool(value)
    if isinstance(value, str):
        v = value.strip().upper()
        if v in {"TRUE", "YES", "PASS", "MATCH", "VISIBLE", "INTACT", "SAFE", "PRESENT"}:
            return True
        if v in {"FALSE", "NO", "FAIL", "MISMATCH", "HIDDEN", "BROKEN", "UNSAFE", "MISSING"}:
            return False
    return None


def _canon_failure(code: Any) -> str | None:
    normalized = re.sub(r"[^A-Z0-9]+", "_", str(code or "").strip().upper()).strip("_")
    normalized = ALIASES.get(normalized, normalized)
    return normalized if normalized in RULES and normalized != "INSUFFICIENT_EVIDENCE" else None


def _inferred_failures(manifest: dict[str, Any]) -> list[tuple[str, str]]:
    observed = manifest.get("observed") if isinstance(manifest.get("observed"), dict) else {}
    expected = manifest.get("expected") if isinstance(manifest.get("expected"), dict) else {}
    stage = str(manifest.get("stage_id", "")).upper()
    found: list[tuple[str, str]] = []

    active = observed.get("active_surface", observed.get("contact_surface"))
    if active not in UNVERIFIED:
        active_s = re.sub(r"[^a-z0-9]+", "_", str(active).lower()).strip("_")
        allowed = str(expected.get("active_surface", "")).lower()
        if active_s in {"cheek", "sidewall", "broad_sidewall", "handle", "corner", "center_joint", "barrel_side", "槌腰側面"}:
            found.append(("WRONG_CONTACT_FACE", f"observed.active_surface={active}"))
        elif allowed and allowed not in {"see_source_prompt", "unverified"}:
            norm_allowed = re.sub(r"[^a-z0-9]+", "_", allowed).strip("_")
            if active_s != norm_allowed and not (norm_allowed in active_s or active_s in norm_allowed):
                found.append(("WRONG_CONTACT_FACE", f"observed.active_surface={active}; expected={allowed}"))

    measured_gap = _number(observed.get("measured_gap_units", observed.get("gap_units", observed.get("measured_gap"))))
    if measured_gap is not None and stage in {"H2", "H2_FIRST_CONTACT", "CONTACT"}:
        if measured_gap < -TOLERANCE:
            found.append(("INTERPENETRATION", f"measured gap={measured_gap} units (<0)"))
        elif measured_gap > TOLERANCE:
            found.append(("GAP_REMAINS", f"measured gap={measured_gap} units (>0 at contact stage)"))

    penetration = _number(observed.get("penetration_depth_units", observed.get("penetration_depth")))
    if penetration is not None and penetration > TOLERANCE:
        found.append(("INTERPENETRATION", f"penetration_depth={penetration} units"))

    crack_origin = observed.get("crack_origin")
    if crack_origin not in UNVERIFIED and str(crack_origin).upper() not in {"P", "CONTACT_POINT_P", "ANCHOR_P"}:
        found.append(("WRONG_CRACK_ORIGIN", f"observed.crack_origin={crack_origin}; required=P"))

    early_cracks = _truth(observed.get("early_cracks", observed.get("cracks_before_contact")))
    if early_cracks is True and stage in {"H0", "H1", "H0_PREIMPACT", "H1_PREIMPACT", "PRE_FAR", "PRE_NEAR"}:
        found.append(("EARLY_CRACKS", f"pre-contact stage={stage}; early_cracks=true"))

    handle_status = str(observed.get("handle_status", "")).upper()
    if handle_status in {"MISSING", "NEW", "NEW_HANDLE", "BENT", "DETACHED", "WRONG_JOINT", "WRONG_SIDE"}:
        found.append(("HANDLE_TOPOLOGY_FAIL", f"observed.handle_status={handle_status}"))

    if _truth(observed.get("camera_contact_seam_visible")) is False or _truth(observed.get("active_face_inspectable")) is False:
        found.append(("CAMERA_OBSCURES_CONTACT", "contact seam/active face is not inspectable"))

    for key in ("scene_identity_match", "background_landmarks_match", "camera_rig_match"):
        if _truth(observed.get(key)) is False:
            found.append(("SCENE_CONTINUITY_FAIL", f"observed.{key}=false"))

    if _truth(observed.get("character_identity_match")) is False or _truth(observed.get("character_scale_match")) is False:
        found.append(("IDENTITY_DRIFT", "character identity or scale mismatch"))

    if _truth(observed.get("residents_safe")) is False or _truth(observed.get("sanctuary_intact")) is False:
        found.append(("RESIDENT_SAFETY_FAIL", "protected residents/sanctuary not safe"))

    expected_advance = _number(expected.get("advance_units", expected.get("H3_advance_units")))
    measured_advance = _number(observed.get("measured_advance_units", observed.get("advance_units")))
    if stage in {"H3", "H3_FOLLOWTHROUGH", "FOLLOWTHROUGH"} and measured_advance is not None and expected_advance is not None:
        if abs(measured_advance - expected_advance) > TOLERANCE:
            found.append(("FOLLOWTHROUGH_MISMATCH", f"measured advance={measured_advance}; expected={expected_advance}"))

    # Explicit measured boolean for rigidity is preferred over free-text inference.
    if _truth(observed.get("rigid_body_intact")) is False:
        found.append(("HANDLE_TOPOLOGY_FAIL", "observed.rigid_body_intact=false"))

    dedup: dict[str, str] = {}
    for code, evidence in found:
        dedup.setdefault(code, evidence)
    return [(code, evidence) for code, evidence in dedup.items()]


def diagnose_attempt(manifest: dict[str, Any]) -> dict[str, Any]:
    """Return a minimal next-change plan grounded in structured observed failures."""
    explicit = manifest.get("failure_codes", [])
    if isinstance(explicit, str):
        explicit = [explicit]
    evidence_pairs: list[tuple[str, str]] = []
    for code in explicit if isinstance(explicit, list) else []:
        canonical = _canon_failure(code)
        if canonical:
            evidence_pairs.append((canonical, f"reviewer failure_code={code}"))

    # Failure-reason prose may add a hint, but an unclassified sentence never counts as proof.
    prose = manifest.get("failure_reasons", [])
    if isinstance(prose, str):
        prose = [prose]
    for item in prose if isinstance(prose, list) else []:
        raw = str(item).upper()
        for needle, code in (
            ("SIDEWALL", "WRONG_CONTACT_FACE"), ("CHEEK", "WRONG_CONTACT_FACE"),
            ("WRONG FACE", "WRONG_CONTACT_FACE"), ("GAP REMAINS", "GAP_REMAINS"),
            ("INTERPENETRATION", "INTERPENETRATION"), ("PENETRATION", "INTERPENETRATION"),
            ("CRACK ORIGIN", "WRONG_CRACK_ORIGIN"), ("EARLY CRACK", "EARLY_CRACKS"),
            ("NEW HANDLE", "HANDLE_TOPOLOGY_FAIL"), ("HANDLE MISSING", "HANDLE_TOPOLOGY_FAIL"),
            ("BENT HANDLE", "HANDLE_TOPOLOGY_FAIL"), ("SEAM HIDDEN", "CAMERA_OBSCURES_CONTACT"),
            ("BACKGROUND DRIFT", "SCENE_CONTINUITY_FAIL"), ("IDENTITY DRIFT", "IDENTITY_DRIFT"),
            ("RESIDENT", "RESIDENT_SAFETY_FAIL"), ("FOLLOWTHROUGH", "FOLLOWTHROUGH_MISMATCH"),
        ):
            if needle in raw:
                evidence_pairs.append((code, f"failure_reasons contains {needle!r}"))

    evidence_pairs.extend(_inferred_failures(manifest))
    unique: dict[str, str] = {}
    for code, evidence in evidence_pairs:
        unique.setdefault(code, evidence)

    valid = [
        (code, evidence) for code, evidence in unique.items()
        if code in RULES and code != "INSUFFICIENT_EVIDENCE"
    ]
    if not valid:
        rule = RULES["INSUFFICIENT_EVIDENCE"]
        return {
            "status": "HOLD",
            "method": "DETERMINISTIC_RULES_OVER_REVIEWED_FIELDS",
            "primary_failure_code": "INSUFFICIENT_EVIDENCE",
            "all_failure_codes": [],
            "evidence": [],
            "severity": rule["severity"],
            "next_change": rule["change"],
            "edit_only": rule["edit_only"],
            "freeze": rule["freeze"],
            "repair_prompt_delta": rule["delta"],
            "expected_after_change": rule["expect"],
            "auto_visual_detection": False,
        }

    valid.sort(key=lambda pair: RULES[pair[0]]["priority"])
    primary, primary_evidence = valid[0]
    rule = RULES[primary]
    other = [code for code, _ in valid[1:]]
    return {
        "status": "REPAIR_PLAN_READY",
        "method": "DETERMINISTIC_RULES_OVER_REVIEWED_FIELDS",
        "primary_failure_code": primary,
        "all_failure_codes": [code for code, _ in valid],
        "additional_failure_codes": other,
        "evidence": [{"code": c, "basis": e} for c, e in valid],
        "primary_evidence": primary_evidence,
        "severity": rule["severity"],
        "next_change": rule["change"],
        "edit_only": rule["edit_only"],
        "freeze": rule["freeze"],
        "repair_prompt_delta": rule["delta"],
        "expected_after_change": rule["expect"],
        "auto_visual_detection": False,
    }


def build_repair_prompt(original_prompt: str, diagnosis: dict[str, Any]) -> str:
    if diagnosis.get("status") != "REPAIR_PLAN_READY":
        return (
            original_prompt.rstrip()
            + "\n\n[REPAIR GATE: HOLD]\n"
            + str(diagnosis.get("repair_prompt_delta", "Do not change the prompt without reviewed evidence."))
            + "\n"
        )
    freeze = ", ".join(map(str, diagnosis.get("freeze", [])))
    edit = ", ".join(map(str, diagnosis.get("edit_only", [])))
    return (
        original_prompt.rstrip()
        + "\n\n[DATA-DRIVEN NEXT-ATTEMPT DELTA]\n"
        + f"PRIMARY FAILURE: {diagnosis.get('primary_failure_code')}\n"
        + f"OBSERVED EVIDENCE: {diagnosis.get('primary_evidence')}\n"
        + f"CHANGE ONLY: {edit}\n"
        + f"KEEP FROZEN: {freeze}\n"
        + str(diagnosis.get("repair_prompt_delta", ""))
        + "\nEXPECTED NEXT OBSERVATION: "
        + str(diagnosis.get("expected_after_change", "UNSPECIFIED"))
        + "\nDo not claim success until the newly generated raster is reviewed against this expected observation.\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, help="the actual reviewed attempt manifest JSON")
    parser.add_argument("--prompt", required=True, help="the exact parent prompt.txt")
    parser.add_argument("--outdir", required=True, help="directory for diagnosis.json and repair_prompt.txt")
    args = parser.parse_args()
    manifest_path, prompt_path, outdir = Path(args.manifest), Path(args.prompt), Path(args.outdir)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    prompt = prompt_path.read_text(encoding="utf-8")
    if not isinstance(manifest, dict):
        raise SystemExit("manifest root must be an object")
    diagnosis = diagnose_attempt(manifest)
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "diagnosis.json").write_text(json.dumps(diagnosis, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (outdir / "repair_prompt.txt").write_text(build_repair_prompt(prompt, diagnosis), encoding="utf-8")
    print(json.dumps({
        "status": diagnosis["status"],
        "primary_failure_code": diagnosis["primary_failure_code"],
        "next_change": diagnosis["next_change"],
        "diagnosis_file": str(outdir / "diagnosis.json"),
        "repair_prompt_file": str(outdir / "repair_prompt.txt"),
        "note": "This rules engine consumes reviewed fields; it does not analyze the raster itself."
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
