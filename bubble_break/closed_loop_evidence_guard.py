"""Strict frame identity, parent provenance, and state-transition guards.

These checks validate structured evidence supplied for a raster. They do not infer annotations
from pixels and never certify visual correctness by themselves.
"""
from __future__ import annotations

import math
from pathlib import Path
from typing import Any

CALIBRATION_SEQUENCE = ("PRE_FAR", "PRE_NEAR", "FIRST_CONTACT", "REACTION", "RECOIL")
BUBBLE_SEQUENCE = (
    "H0_PRE_IMPACT",
    "H1_PRE_NEAR",
    "H2_FIRST_CONTACT",
    "H2B_CRACK_PROPAGATION",
    "H3_FOLLOWTHROUGH_SHELL_SHATTER",
)
BUBBLE_SHELL_STATE = {
    "H0_PRE_IMPACT": "INTACT",
    "H1_PRE_NEAR": "INTACT",
    "H2_FIRST_CONTACT": "INITIATED",
    "H2B_CRACK_PROPAGATION": "PROPAGATING",
    "H3_FOLLOWTHROUGH_SHELL_SHATTER": "SHATTERED",
}
LOCK_FIELDS = ("scene_lock_id", "camera_lock_id")
CALIBRATION_ID_FIELDS = ("tool_a_identity_id", "tool_b_identity_id")
BUBBLE_ID_FIELDS = ("attacking_hammer_identity_id", "bubble_identity_id")


def _nonempty_str(evidence: dict[str, Any], name: str, errors: list[str]) -> str | None:
    value = evidence.get(name)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"MISSING_LOCK_FIELD:{name}")
        return None
    return value.strip()


def _finite_number(evidence: dict[str, Any], name: str, errors: list[str]) -> float | None:
    try:
        value = float(evidence[name])
    except (KeyError, TypeError, ValueError):
        errors.append(f"MISSING_OR_INVALID_NUMERIC_FIELD:{name}")
        return None
    if not math.isfinite(value):
        errors.append(f"NONFINITE_NUMERIC_FIELD:{name}")
        return None
    return value


def validate_stage_binding(
    *,
    domain: str,
    expected_stage: str,
    evidence: dict[str, Any] | None,
    raster_sha256: str,
    expected_parent_sha256: str | None,
    expected_parent_stage: str | None,
    expected_calibration_sha256: str | None = None,
    previous_evidence: dict[str, Any] | None = None,
) -> list[str]:
    """Return fail-closed contract errors for one actual candidate raster.

    Evidence must state its own stage, the exact parent raster SHA (except the first calibration
    frame), stable scene/camera/object identities, and—on bubble frames—the SHA of the upstream
    approved dual-T FIRST_CONTACT raster from which the weapon geometry was calibrated.
    """
    errors: list[str] = []
    if not isinstance(evidence, dict):
        return ["MISSING_EVIDENCE_OBJECT"]

    actual_stage = evidence.get("stage")
    if actual_stage != expected_stage:
        errors.append(f"STAGE_SLOT_MISMATCH:expected={expected_stage}:evidence={actual_stage}")

    normalized_domain = domain.strip().upper()
    if normalized_domain not in {"CALIBRATION", "BUBBLE_BREAK"}:
        return errors + [f"UNKNOWN_EVIDENCE_DOMAIN:{domain}"]

    if expected_parent_sha256 is not None:
        declared_parent = evidence.get("parent_raster_sha256")
        if not isinstance(declared_parent, str) or declared_parent.lower() != expected_parent_sha256.lower():
            errors.append("PARENT_RASTER_SHA256_MISMATCH")
        if evidence.get("parent_stage") != expected_parent_stage:
            errors.append(
                f"PARENT_STAGE_MISMATCH:expected={expected_parent_stage}:evidence={evidence.get('parent_stage')}"
            )
        if raster_sha256 and raster_sha256.lower() == expected_parent_sha256.lower():
            errors.append("NO_OP_TRANSITION_IMAGE_IDENTICAL_TO_PARENT")
    elif expected_parent_stage is not None:
        errors.append("INTERNAL_GUARD_ERROR_PARENT_STAGE_WITHOUT_PARENT_SHA")

    for name in LOCK_FIELDS:
        _nonempty_str(evidence, name, errors)

    id_fields = CALIBRATION_ID_FIELDS if normalized_domain == "CALIBRATION" else BUBBLE_ID_FIELDS
    for name in id_fields:
        _nonempty_str(evidence, name, errors)

    if normalized_domain == "BUBBLE_BREAK":
        declared_calibration = evidence.get("calibrated_from_dual_hammer_sha256")
        if (
            not isinstance(expected_calibration_sha256, str)
            or not expected_calibration_sha256.strip()
        ):
            errors.append("INTERNAL_GUARD_ERROR_CALIBRATION_SHA_NOT_PROVIDED")
        elif not isinstance(declared_calibration, str) or declared_calibration.lower() != expected_calibration_sha256.lower():
            errors.append("CALIBRATED_FROM_DUAL_HAMMER_SHA256_MISMATCH")

        expected_shell = BUBBLE_SHELL_STATE.get(expected_stage)
        actual_shell = evidence.get("shell_integrity_state")
        if expected_shell and actual_shell != expected_shell:
            errors.append(f"SHELL_STATE_MISMATCH:expected={expected_shell}:evidence={actual_shell}")

        crack_ratio = _finite_number(evidence, "crack_front_radius_ratio", errors)
        preexisting_cracks = evidence.get("preexisting_cracks")
        if expected_stage in {"H0_PRE_IMPACT", "H1_PRE_NEAR"}:
            if preexisting_cracks is not False:
                errors.append("PRECONTACT_FRAME_MUST_EXPLICITLY_HAVE_NO_PREEXISTING_CRACKS")
            if crack_ratio is not None and abs(crack_ratio) > 1e-9:
                errors.append("PRECONTACT_FRAME_CRACK_FRONT_MUST_BE_ZERO")
        elif expected_stage == "H2_FIRST_CONTACT":
            if preexisting_cracks is not False:
                errors.append("FIRST_CONTACT_MUST_DECLARE_NO_PREEXISTING_CRACKS")
            if crack_ratio is not None and not (0.0 <= crack_ratio <= 0.15):
                errors.append("FIRST_CONTACT_CRACK_FRONT_TOO_LARGE_FOR_INITIATION_STATE")
        elif expected_stage in {"H2B_CRACK_PROPAGATION", "H3_FOLLOWTHROUGH_SHELL_SHATTER"}:
            if preexisting_cracks is not True:
                errors.append(f"{expected_stage}_MUST_DECLARE_CRACKS_PRESENT")

        if expected_stage == "H3_FOLLOWTHROUGH_SHELL_SHATTER":
            if evidence.get("shell_only_breach") is not True:
                errors.append("FINAL_FRAME_MUST_DECLARE_SHELL_ONLY_BREACH")
            if evidence.get("inhabitants_unharmed") is not True:
                errors.append("FINAL_FRAME_MUST_DECLARE_INHABITANTS_UNHARMED")

    # Stable identity bindings are compared only within the same physical domain. H0 begins a
    # new scene after target substitution, so its identity IDs intentionally differ from calibration.
    if previous_evidence is not None and actual_stage == expected_stage:
        compare_fields = LOCK_FIELDS + id_fields
        for name in compare_fields:
            prev = previous_evidence.get(name)
            current = evidence.get(name)
            if isinstance(prev, str) and prev.strip() and current != prev:
                errors.append(f"IDENTITY_LOCK_CHANGED:{name}")

        if normalized_domain == "BUBBLE_BREAK":
            prev_ratio = previous_evidence.get("crack_front_radius_ratio")
            curr_ratio = evidence.get("crack_front_radius_ratio")
            try:
                prev_ratio = float(prev_ratio)
                curr_ratio = float(curr_ratio)
            except (TypeError, ValueError):
                pass
            else:
                if not (math.isfinite(prev_ratio) and math.isfinite(curr_ratio)):
                    errors.append("NONFINITE_CRACK_FRONT_TRANSITION")
                elif expected_stage == "H2B_CRACK_PROPAGATION" and curr_ratio <= prev_ratio:
                    errors.append("CRACK_FRONT_DID_NOT_EXPAND_FROM_H2_TO_H2B")
                elif expected_stage == "H3_FOLLOWTHROUGH_SHELL_SHATTER" and curr_ratio <= prev_ratio:
                    errors.append("FINAL_SHELL_BREAK_HAS_NO_INCREASED_OUTWARD_FRACTURE_EXTENT")

    return errors


def attach_guard_errors(validation: dict[str, Any], guard_errors: list[str]) -> dict[str, Any]:
    """Combine semantic/geometry gate output with binding/state guards without mutating the input."""
    result = dict(validation)
    errors = list(result.get("errors", [])) + list(guard_errors)
    result["errors"] = errors
    result["accepted"] = bool(result.get("accepted", False)) and not guard_errors
    if guard_errors:
        result["status"] = "BLOCKED_EVIDENCE_BINDING_OR_STATE_TRANSITION"
    if not result.get("visual_acceptance_status"):
        result["visual_acceptance_status"] = "NOT_VERIFIED_BY_CODE"
    result["acceptance_level"] = (
        "STRUCTURED_EVIDENCE_CONTRACT_ONLY"
        if result["accepted"]
        else "BLOCKED"
    )
    return result
