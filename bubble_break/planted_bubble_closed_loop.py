#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shannon-inspired, raster-bound closed loop for the planted-cylinder Bubble-Break concept.

Canonical geometry (derived from the project's recorded B3 success path):
- a double-ended cylindrical hammer head is planted radially on the bubble;
- a conformal curved seat remains fully in contact with the bubble at P;
- one pre-existing handle grows laterally from the cylinder's side-middle, tangent to
  the bubble and transverse to the cylinder axis;
- the exposed outer end cap remains clear; no axial handle, extra stub, or new rod;
- the planted contact does NOT open/close across the timeline. The human's pose changes;
  then glow/cracks grow from the same seat P, and only the shell shatters.

This module compiles prompts and validates evidence records tied to exact raster bytes.
It is not an image-generation service or a pixel-level semantic vision model.
Every code status therefore keeps visual_acceptance_status=NOT_VERIFIED_BY_CODE.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import shlex
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from PIL import Image, ImageChops, ImageDraw

from bubble_break.planted_bubble_information_gain import recommend_next_experiment


CONTRACT_ID = "PLANTED_DOUBLE_ENDED_CYLINDER_BUBBLE_CONTACT_V1"
STAGE_ORDER: tuple[str, ...] = (
    "B_LOCKED_TOOL_MASTER",
    "C_PERSON_SCALE_NO_GRIP",
    "D1_APPROACH_NO_GRIP",
    "D2_FIRST_GRIP_EXISTING_HANDLE",
    "D3_TENSION_EXISTING_HANDLE",
    "E_MID_GLOW_CRACKS_FROM_P",
    "E_END_SHELL_SHATTER_FROM_P",
)

# Only these fields may change in each serial full-frame edit. All unspecified
# geometry remains invariant. This is a rate/distortion-style policy: preserve
# the geometry signal, spend variation budget only on authorized fields.
STAGE_SPECS: dict[str, dict[str, Any]] = {
    "B_LOCKED_TOOL_MASTER": {
        "label_zh": "B：隔離並鎖定單一種植圓柱母版",
        "actor_present": False,
        "grip_existing_handle": False,
        "shell_state": "INTACT",
        "crack_state": "NONE",
        "authorized_delta_fields": ["isolate_selected_tool_roi", "remove_other_candidate_tools"],
        "must_preserve": ["bubble_center_radius", "P", "conformal_base_seat", "cylinder_axis", "outer_cap", "side_middle_handle"],
        "prompt": (
            "Make one isolated master from the exact selected ROI in the source atlas. Keep exactly one "
            "double-ended cylindrical hammer head planted on the bubble surface. The bubble-side end has a "
            "conformal curved seat fully contacting the bubble at P and a restrained glow at that base interface. "
            "The cylinder axis follows the local outward surface normal. One existing straight handle attaches "
            "at the cylinder side-middle and extends along the local tangent (transverse to the cylinder axis, "
            "about 90 degrees). Keep the opposite outer circular end cap completely clear: no rod or handle "
            "extends axially from it. Do not redraw the tool, change its proportions, move P, or create a flying "
            "hammer. No person, no cracks, no broken shell. This is one full-frame image, not a grid."
        ),
    },
    "C_PERSON_SCALE_NO_GRIP": {
        "label_zh": "C：加入迷你人物，不握柄",
        "actor_present": True,
        "grip_existing_handle": False,
        "shell_state": "INTACT",
        "crack_state": "NONE",
        "authorized_delta_fields": ["add_one_miniature_protagonist", "adjust_heroine_scale_and_position"],
        "must_preserve": ["all_B_master_pixels_outside_actor_edit_region", "P", "base_contact", "cylinder", "same_side_handle"],
        "prompt": (
            "Use the accepted B master as the parent image. Add one miniature heroine at the specified scene "
            "scale, but do NOT let her grip the handle yet. The planted double-ended cylinder, conformal glowing "
            "base seat, P, outer-cap clearance, and the existing side-middle tangent handle must remain the same "
            "object and same geometry. Do not add, replace, lengthen, or redirect any rod. Bubble remains intact "
            "with no cracks. Edit the authorized person region only; full-frame image, not a collage."
        ),
    },
    "D1_APPROACH_NO_GRIP": {
        "label_zh": "D1：人物蓄力定位，仍不握柄",
        "actor_present": True,
        "grip_existing_handle": False,
        "shell_state": "INTACT",
        "crack_state": "NONE",
        "authorized_delta_fields": ["heroine_pose", "heroine_body_position", "cloth_and_hair_motion"],
        "must_preserve": ["P", "base_contact", "cylinder_axis", "outer_cap_clearance", "side_handle_instance_and_axis"],
        "prompt": (
            "Start from the accepted C frame. Change only the heroine's pose/body position and natural cloth/hair "
            "motion into a readable wind-up. The cylinder is already planted and remains fully seated at the same "
            "bubble point P; it does NOT approach through an air gap. Keep the original side-middle handle visible "
            "and untouched. No hand grip yet. Do not create a new handle or a second rod. Bubble intact, no cracks."
        ),
    },
    "D2_FIRST_GRIP_EXISTING_HANDLE": {
        "label_zh": "D2：首次握住來源圖已有的側柄",
        "actor_present": True,
        "grip_existing_handle": True,
        "shell_state": "INTACT",
        "crack_state": "NONE",
        "authorized_delta_fields": ["heroine_hands_and_forearms", "minimum_required_arm_pose"],
        "must_preserve": ["P", "base_contact", "cylinder", "outer_cap_clearance", "existing_handle_pixels_and_axis"],
        "prompt": (
            "Start from the accepted D1 parent and make only the first grip. Both hands must contact the exact "
            "already-existing side-middle handle identified by the supplied handle track/ROI. Move hands/forearms "
            "to the existing rod; never move the rod to the hands, grow a grip-friendly replacement, add a lower "
            "stub, or attach anything to either circular end cap. The rod keeps its same instance, attachment point, "
            "axis and length. Keep P and the conformal planted seat fixed; bubble remains intact and uncracked."
        ),
    },
    "D3_TENSION_EXISTING_HANDLE": {
        "label_zh": "D3：沿既有側柄建立張力",
        "actor_present": True,
        "grip_existing_handle": True,
        "shell_state": "INTACT",
        "crack_state": "NONE",
        "authorized_delta_fields": ["heroine_pose_tension", "shoulder_hip_weight_shift", "hair_and_cloth_followthrough"],
        "must_preserve": ["same_gripped_handle_track", "P", "base_contact", "cylinder_geometry", "outer_cap_clearance"],
        "prompt": (
            "Starting from the accepted D2 image, increase the heroine's full-body tension and readable torque "
            "through the existing handle. This is one serial image edit, not a 20-cell pose board. The same hands "
            "grip the same pre-existing side rod; its attachment point, tangent axis, length, cylinder and planted "
            "conformal base remain locked. Do not swing/fly the cylinder toward the bubble: it is already planted. "
            "No premature cracks or shell damage."
        ),
    },
    "E_MID_GLOW_CRACKS_FROM_P": {
        "label_zh": "E 中幀：底座發光增強，裂紋從 P 擴散",
        "actor_present": True,
        "grip_existing_handle": True,
        "shell_state": "CRACKING_NOT_SHATTERED",
        "crack_state": "RADIAL_FROM_P",
        "authorized_delta_fields": ["base_interface_glow_intensity", "shell_cracks_radiating_from_P", "restrained_shock_rings"],
        "must_preserve": ["same_gripped_handle_track", "P", "conformal_base_seat", "cylinder_pose", "sanctuary_and_residents"],
        "prompt": (
            "Start from the accepted D3 parent. Keep the cylinder planted and the conformal base seat touching at "
            "the exact same P. Intensify the glow at the BASE-TO-BUBBLE interface, not at the outer cap or handle "
            "joint. Fine cracks begin at P and radiate across the outer shell; the shell is still recognizably "
            "present and has not yet exploded. Preserve the miniature sanctuary and every resident unharmed. "
            "The handle remains the same existing side-middle rod and the heroine keeps that grip."
        ),
    },
    "E_END_SHELL_SHATTER_FROM_P": {
        "label_zh": "E 尾幀：只破泡殼，內部居民完好",
        "actor_present": True,
        "grip_existing_handle": True,
        "shell_state": "SHATTERED",
        "crack_state": "SHATTERED_OUTWARD_FROM_P",
        "authorized_delta_fields": ["shell_fragmentation_outward_from_P", "light_and_shockwave_aftermath"],
        "must_preserve": ["same_gripped_handle_track", "P", "cylinder_pose", "conformal_base_seat", "outer_cap_clearance", "sanctuary_and_residents"],
        "prompt": (
            "Use the accepted E-mid image as the parent. The outer bubble shell shatters outward from the same P; "
            "do not add a second blast origin. The double-ended cylinder remains planted in its conformal seat and "
            "the heroine still grips the same side-middle tangent handle. Do not convert the tool into a long sledge, "
            "change the handle axis, or make the tool fly away. Destroy only the containment shell. The interior "
            "sanctuary, its buildings and every resident remain intact and unharmed, now exposed to open air/light."
        ),
    },
}

GLOBAL_LOCKS: tuple[str, ...] = (
    "double-ended solid cylindrical hammer head, not a spherical mace or a T-v-T pair",
    "bubble-side conformal curved seat stays fully seated at P through every frame",
    "cylinder axis follows the local outward surface normal at P",
    "one existing handle attaches at the cylinder side-middle and runs tangent to the bubble",
    "handle instance/axis/length do not change after B; hands move to it at D2, not vice versa",
    "opposite outer circular end cap remains empty; no axial handle, lower stub, duplicate rod, or extra tool",
    "P, bubble center/radius, selected master geometry, camera/landmarks stay locked unless explicitly authorized",
    "base-interface glow and shell cracks originate from P; only the shell breaks; sanctuary/residents stay safe",
    "one serial full-frame image edit per step; never use a multi-cell image as evidence for per-frame locks",
)

REVIEW_MODES = {"HUMAN_PIXEL_REVIEW", "SEMANTIC_VISION_REVIEW"}


@dataclass(frozen=True)
class Candidate:
    image_path: Path
    evidence: dict[str, Any]


@dataclass
class AttemptRecord:
    stage: str
    attempt_round: int
    raster_path: str
    raster_sha256: str
    contract_valid: bool
    eligible_for_next_stage: bool
    errors: list[str]
    creativity_score: float
    novelty_score: float
    selected: bool = False


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def compute_background_landmarks_sha256(image_path: str | Path, border_fraction: float = 0.02) -> str:
    """Hash a narrow, lossless RGB border used as a stable scene/camera background landmark."""
    if not 0.005 <= border_fraction <= 0.10:
        raise ValueError("border_fraction must be between 0.005 and 0.10")
    with Image.open(image_path) as im:
        image = im.convert("RGB")
    width, height = image.size
    margin_x = max(1, int(width * border_fraction))
    margin_y = max(1, int(height * border_fraction))
    digest = hashlib.sha256()
    digest.update(f"{width}x{height}|border={border_fraction:.4f}|".encode("ascii"))
    # Hash four non-overlapping border strips. Their pixels are protected by every child edit mask.
    strips = (
        image.crop((0, 0, width, margin_y)),
        image.crop((0, height-margin_y, width, height)),
        image.crop((0, margin_y, margin_x, height-margin_y)),
        image.crop((width-margin_x, margin_y, width, height-margin_y)),
    )
    for strip in strips:
        digest.update(strip.size[0].to_bytes(4, "big"))
        digest.update(strip.size[1].to_bytes(4, "big"))
        digest.update(strip.tobytes())
    return digest.hexdigest()


def authorized_pixel_delta(parent_path: str | Path, child_path: str | Path, edit_mask_path: str | Path) -> dict[str, Any]:
    """Measure whether an edit changed any pixels inside the allowed mask."""
    with Image.open(parent_path) as im:
        parent = im.convert("RGB")
    with Image.open(child_path) as im:
        child = im.convert("RGB")
    with Image.open(edit_mask_path) as im:
        mask = im.convert("L")
    if parent.size != child.size or parent.size != mask.size:
        return {"passed": False, "status": "BLOCK_DIMENSION_MISMATCH", "changed_editable_pixels": None}
    mask = mask.point(lambda value: 255 if value >= 128 else 0)
    diff = ImageChops.difference(parent, child).convert("L")
    changed = ImageChops.multiply(diff, mask)
    changed_count = sum(changed.histogram()[1:])
    editable_count = mask.histogram()[255]
    return {"passed": changed_count > 0, "status": "PASS_AUTHORIZED_PIXEL_DELTA" if changed_count > 0 else "BLOCK_NO_AUTHORIZED_PIXEL_DELTA",
            "changed_editable_pixels": changed_count, "editable_pixels": editable_count}


def compose_masked_edit(parent_path: str | Path, generated_path: str | Path, edit_mask_path: str | Path, output_path: str | Path) -> str:
    """Take new pixels only inside the authorized mask; output PNG preserves frozen pixels exactly."""
    with Image.open(parent_path) as im:
        parent = im.convert("RGB")
    with Image.open(generated_path) as im:
        generated = im.convert("RGB")
    with Image.open(edit_mask_path) as im:
        mask = im.convert("L")
    if parent.size != generated.size or parent.size != mask.size:
        raise ValueError("parent, generated image, and edit mask must have identical dimensions")
    mask = mask.point(lambda value: 255 if value >= 128 else 0)
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    Image.composite(generated, parent, mask).save(out, format="PNG")
    return sha256_file(out)


def validate_frozen_pixels(parent_path: str | Path, child_path: str | Path, edit_mask_path: str | Path) -> dict[str, Any]:
    """Reject any pixel drift outside the authorized edit mask."""
    with Image.open(parent_path) as im:
        parent = im.convert("RGB")
    with Image.open(child_path) as im:
        child = im.convert("RGB")
    with Image.open(edit_mask_path) as im:
        mask = im.convert("L")
    if parent.size != child.size or parent.size != mask.size:
        return {"passed": False, "status": "BLOCK_DIMENSION_MISMATCH", "outside_edit_mismatch_pixels": None}
    mask = mask.point(lambda value: 255 if value >= 128 else 0)
    frozen = mask.point(lambda value: 255 - value)
    difference = ImageChops.difference(parent, child).convert("L")
    frozen_difference = ImageChops.multiply(difference, frozen)
    mismatch = sum(frozen_difference.histogram()[1:])
    frozen_count = frozen.histogram()[255]
    return {"passed": mismatch == 0,
            "status": "PASS_FROZEN_PIXELS_IDENTICAL" if mismatch == 0 else "BLOCK_FROZEN_PIXEL_DRIFT",
            "outside_edit_mismatch_pixels": mismatch, "outside_edit_pixels": frozen_count,
            "parent_sha256": sha256_file(parent_path), "child_sha256": sha256_file(child_path)}


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def contract_fingerprint() -> str:
    return canonical_sha256({
        "contract_id": CONTRACT_ID,
        "stage_order": STAGE_ORDER,
        "stage_specs": STAGE_SPECS,
        "global_locks": GLOBAL_LOCKS,
    })


def _vec3(value: Any, key: str) -> tuple[float, float, float]:
    if not isinstance(value, (list, tuple)) or len(value) != 3:
        raise ValueError(f"{key} must be a 3-vector")
    vector = tuple(float(item) for item in value)
    if not all(math.isfinite(item) for item in vector):
        raise ValueError(f"{key} must contain finite numbers")
    return vector  # type: ignore[return-value]


def _point2(value: Any, key: str) -> tuple[float, float]:
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise ValueError(f"{key} must be a 2-vector")
    point = (float(value[0]), float(value[1]))
    if not all(math.isfinite(item) for item in point):
        raise ValueError(f"{key} must contain finite numbers")
    return point


def _dot(a: Sequence[float], b: Sequence[float]) -> float:
    return sum(float(a[i]) * float(b[i]) for i in range(len(a)))


def _norm(a: Sequence[float]) -> float:
    return math.sqrt(_dot(a, a))


def _unit(a: Any, key: str) -> tuple[float, float, float]:
    vector = _vec3(a, key)
    magnitude = _norm(vector)
    if magnitude < 1e-9:
        raise ValueError(f"{key} must not be zero")
    return tuple(v / magnitude for v in vector)  # type: ignore[return-value]


def _distance2(a: Sequence[float], b: Sequence[float]) -> float:
    return math.hypot(float(a[0]) - float(b[0]), float(a[1]) - float(b[1]))


def _valid_bbox(value: Any, key: str, width: int, height: int) -> tuple[float, float, float, float]:
    if not isinstance(value, (list, tuple)) or len(value) != 4:
        raise ValueError(f"{key} must be [x0,y0,x1,y1]")
    box = tuple(float(item) for item in value)
    x0, y0, x1, y1 = box
    if not all(math.isfinite(item) for item in box) or not (0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height):
        raise ValueError(f"{key} must be a non-empty bounding box inside the raster")
    return box  # type: ignore[return-value]


def _review_errors(
    review: Any,
    *,
    stage: str,
    image_sha: str,
    parent_sha: str | None,
    anchor_sha: str,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(review, dict):
        return ["REVIEW_RECORD_MISSING"]
    if review.get("decision") != "PASS":
        errors.append("EXTERNAL_REVIEW_NOT_PASS")
    if review.get("mode") not in REVIEW_MODES:
        errors.append("REVIEW_MODE_MUST_BE_HUMAN_OR_SEMANTIC_VISION")
    if not isinstance(review.get("reviewer_or_model"), str) or not review["reviewer_or_model"].strip():
        errors.append("REVIEWER_OR_MODEL_VERSION_MISSING")
    if review.get("reviewed_raster_sha256") != image_sha:
        errors.append("REVIEW_RASTER_SHA256_MISMATCH")
    if review.get("reviewed_parent_sha256") != parent_sha:
        errors.append("REVIEW_PARENT_SHA256_MISMATCH")
    if review.get("reviewed_scene_anchor_sha256") != anchor_sha:
        errors.append("REVIEW_SCENE_ANCHOR_SHA256_MISMATCH")
    if str(review.get("stage", "")).upper() != stage:
        errors.append("REVIEW_STAGE_MISMATCH")
    if not isinstance(review.get("notes"), str) or not review["notes"].strip():
        errors.append("REVIEW_NOTES_MISSING")
    return errors


def _selection_errors(selection: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(selection, dict):
        return ["MASTER_SELECTION_RECORD_MISSING"]
    if selection.get("selection_mode") != "HUMAN_ROI":
        errors.append("MASTER_SELECTION_MUST_USE_EXPLICIT_HUMAN_ROI_NOT_LABEL_ONLY")
    if not isinstance(selection.get("selection_reviewer"), str) or not selection["selection_reviewer"].strip():
        errors.append("MASTER_SELECTION_REVIEWER_MISSING")
    if not isinstance(selection.get("selection_notes"), str) or not selection["selection_notes"].strip():
        errors.append("MASTER_SELECTION_NOTES_MISSING")
    atlas_path = selection.get("source_atlas_image_path")
    atlas_sha = selection.get("source_atlas_raster_sha256")
    if not isinstance(atlas_path, str) or not Path(atlas_path).is_file():
        errors.append("MASTER_SELECTION_SOURCE_ATLAS_MISSING")
    else:
        try:
            real_sha = sha256_file(atlas_path)
            if atlas_sha != real_sha:
                errors.append("MASTER_SELECTION_SOURCE_ATLAS_SHA256_MISMATCH")
            with Image.open(atlas_path) as atlas:
                atlas_w, atlas_h = atlas.size
            expected_size = (selection.get("source_atlas_width_px"), selection.get("source_atlas_height_px"))
            if expected_size != (atlas_w, atlas_h):
                errors.append("MASTER_SELECTION_SOURCE_ATLAS_DIMENSIONS_MISMATCH")
            _valid_bbox(selection.get("selected_roi_xyxy_px"), "selected_roi_xyxy_px", atlas_w, atlas_h)
        except (OSError, ValueError, TypeError) as exc:
            errors.append(f"MASTER_SELECTION_ROI_INVALID:{exc}")
    if selection.get("selected_tool_is_single_instance") is not True:
        errors.append("MASTER_SELECTION_MUST_IDENTIFY_ONE_TOOL_INSTANCE")
    # A textual label may assist a person, but is never the selection key.
    return errors


def load_master_selection_manifest(path: str | Path) -> dict[str, Any]:
    """Load and verify the explicit human ROI selected from a source atlas."""
    manifest_path = Path(path).resolve()
    raw = json.loads(manifest_path.read_text(encoding="utf-8"))
    selection = raw.get("master_selection", raw) if isinstance(raw, dict) else None
    if not isinstance(selection, dict):
        raise ValueError("master-selection manifest must be an object")
    selection = dict(selection)
    atlas_path = selection.get("source_atlas_image_path")
    if isinstance(atlas_path, str) and not Path(atlas_path).is_absolute():
        selection["source_atlas_image_path"] = str((manifest_path.parent / atlas_path).resolve())
    errors = _selection_errors(selection)
    if errors:
        raise ValueError("invalid master-selection manifest: " + "; ".join(errors))
    return selection


def validate_planted_bubble_frame(
    image_path: str | Path,
    evidence: dict[str, Any] | None,
    *,
    expected_stage: str,
    expected_parent_sha256: str | None = None,
    expected_anchor_sha256: str | None = None,
    locked_contact_point_px: tuple[float, float] | None = None,
    expected_cylinder_instance_id: str | None = None,
    expected_handle_track_id: str | None = None,
    expected_locked_geometry: Mapping[str, Any] | None = None,
    expected_scene_lock: Mapping[str, Any] | None = None,
    expected_parent_evidence: Mapping[str, Any] | None = None,
    expected_parent_image_path: str | Path | None = None,
) -> dict[str, Any]:
    """Validate exact raster binding, planted-cylinder geometry, scene state, and external review receipt.

    A contract pass means an externally reviewed evidence record is bound to these exact image bytes.
    The code does not infer object geometry or verify that the stated reviewer actually saw the pixels.
    """
    path = Path(image_path)
    if expected_stage not in STAGE_SPECS:
        return {"contract_valid": False, "eligible_for_next_stage": False, "status": "BLOCKED_UNKNOWN_STAGE",
                "errors": ["UNKNOWN_STAGE"], "visual_acceptance_status": "NOT_VERIFIED_BY_CODE"}
    if not path.is_file():
        return {"contract_valid": False, "eligible_for_next_stage": False, "status": "BLOCKED_RASTER_MISSING",
                "errors": ["RASTER_MISSING"], "visual_acceptance_status": "NOT_VERIFIED_BY_CODE"}
    if not isinstance(evidence, dict):
        return {"contract_valid": False, "eligible_for_next_stage": False, "status": "BLOCKED_EVIDENCE_MISSING",
                "errors": ["EVIDENCE_RECORD_MISSING"], "visual_acceptance_status": "NOT_VERIFIED_BY_CODE"}

    errors: list[str] = []
    digest = sha256_file(path)
    try:
        with Image.open(path) as image:
            width, height = image.size
            image.verify()
        with Image.open(path) as image:
            width, height = image.size
    except Exception as exc:
        return {"contract_valid": False, "eligible_for_next_stage": False, "status": "BLOCKED_RASTER_UNREADABLE",
                "errors": [f"RASTER_UNREADABLE:{exc}"], "visual_acceptance_status": "NOT_VERIFIED_BY_CODE"}

    stage = expected_stage
    if evidence.get("contract_id") != CONTRACT_ID:
        errors.append("CONTRACT_ID_MISMATCH")
    if evidence.get("contract_sha256") != contract_fingerprint():
        errors.append("CONTRACT_FINGERPRINT_MISMATCH")
    if str(evidence.get("stage", "")).upper() != stage:
        errors.append("EVIDENCE_STAGE_MISMATCH")
    if str(evidence.get("raster_sha256", "")).lower() != digest:
        errors.append("RASTER_SHA256_MISMATCH")
    if stage != "B_LOCKED_TOOL_MASTER":
        if expected_parent_sha256 and digest == expected_parent_sha256:
            errors.append("NO_OP_FRAME_COPIED_FROM_PARENT")
        if expected_parent_image_path is None or not Path(expected_parent_image_path).is_file():
            errors.append("PREVIOUS_PASS_PARENT_IMAGE_PATH_REQUIRED")
        else:
            mask_path = evidence.get("edit_mask_path")
            mask_parent_sha = evidence.get("edit_mask_parent_sha256")
            if not isinstance(mask_path, str) or not Path(mask_path).is_file():
                errors.append("AUTHORIZED_EDIT_MASK_MISSING")
            elif mask_parent_sha != expected_parent_sha256:
                errors.append("EDIT_MASK_NOT_BOUND_TO_LAST_PASS_PARENT")
            else:
                frozen_audit = validate_frozen_pixels(expected_parent_image_path, path, mask_path)
                if not frozen_audit.get("passed", False):
                    errors.append("UNAUTHORIZED_PIXEL_DRIFT_OUTSIDE_EDIT_MASK")
                delta_audit = authorized_pixel_delta(expected_parent_image_path, path, mask_path)
                if not delta_audit.get("passed", False):
                    errors.append("NO_AUTHORIZED_PIXEL_DELTA_IN_CHILD")

    if stage == "B_LOCKED_TOOL_MASTER":
        if expected_parent_sha256 is not None:
            errors.append("MASTER_MUST_NOT_HAVE_A_PREVIOUS_PASS_PARENT")
        if evidence.get("parent_raster_sha256") not in (None, ""):
            errors.append("MASTER_MUST_NOT_CLAIM_A_PREVIOUS_PASS_PARENT")
        if evidence.get("scene_anchor_raster_sha256") != digest:
            errors.append("MASTER_ANCHOR_MUST_EQUAL_LOCKED_MASTER_RASTER")
    else:
        if not expected_parent_sha256:
            errors.append("PREVIOUS_PASS_PARENT_REQUIRED")
        elif evidence.get("parent_raster_sha256") != expected_parent_sha256:
            errors.append("PARENT_RASTER_SHA256_MISMATCH")
        if not expected_anchor_sha256:
            errors.append("LOCKED_MASTER_ANCHOR_SHA256_REQUIRED")
        elif evidence.get("scene_anchor_raster_sha256") != expected_anchor_sha256:
            errors.append("SCENE_ANCHOR_SHA256_MISMATCH")

    ann = evidence.get("raster_annotations")
    if not isinstance(ann, dict):
        errors.append("RASTER_ANNOTATIONS_MISSING")
        ann = {}
    if ann.get("image_width_px") != width or ann.get("image_height_px") != height:
        errors.append("ANNOTATION_DIMENSIONS_MISMATCH")

    # A single story timeline cannot silently swap camera rigs or scene/background landmarks.
    scene_id = evidence.get("scene_id")
    camera_rig_id = evidence.get("camera_rig_id")
    camera_view_fingerprint = evidence.get("camera_view_fingerprint")
    background_landmarks_sha256 = evidence.get("background_landmarks_sha256")
    if not isinstance(scene_id, str) or not scene_id.strip():
        errors.append("SCENE_ID_MISSING")
    if not isinstance(camera_rig_id, str) or not camera_rig_id.strip():
        errors.append("CAMERA_RIG_ID_MISSING")
    if not isinstance(camera_view_fingerprint, str) or not camera_view_fingerprint.strip():
        errors.append("CAMERA_VIEW_FINGERPRINT_MISSING")
    if not isinstance(background_landmarks_sha256, str) or len(background_landmarks_sha256) != 64 or any(ch not in "0123456789abcdef" for ch in background_landmarks_sha256.lower()):
        errors.append("BACKGROUND_LANDMARKS_SHA256_MISSING_OR_INVALID")
    raster_background_sha = compute_background_landmarks_sha256(path)
    if background_landmarks_sha256 != raster_background_sha:
        errors.append("BACKGROUND_LANDMARK_FINGERPRINT_MISMATCH")
    scene_lock = {"scene_id": scene_id, "camera_rig_id": camera_rig_id,
                  "camera_view_fingerprint": camera_view_fingerprint,
                  "background_landmarks_sha256": raster_background_sha}
    if expected_scene_lock is not None:
        for key, issue in (( "scene_id", "SCENE_ID_CHANGED"),
                           ("camera_rig_id", "CAMERA_RIG_CHANGED"),
                           ("camera_view_fingerprint", "CAMERA_VIEW_CHANGED_WITHIN_TIMELINE"),
                           ("background_landmarks_sha256", "BACKGROUND_LANDMARKS_CHANGED")):
            if scene_lock.get(key) != expected_scene_lock.get(key):
                errors.append(issue)

    if stage == "B_LOCKED_TOOL_MASTER":
        errors.extend(_selection_errors(evidence.get("master_selection")))

    bubble = ann.get("bubble")
    cylinder = ann.get("planted_cylinder")
    heroine = ann.get("heroine")
    shell = ann.get("shell")
    contact_point: tuple[float, float] | None = None
    bubble_radius = 0.0
    cylinder_id: str | None = None
    handle_id: str | None = None
    geometry_metrics: dict[str, Any] = {}
    locked_geometry: dict[str, Any] = {}
    body_bbox: tuple[float, float, float, float] | None = None
    handle_bbox: tuple[float, float, float, float] | None = None
    handle_start_px: tuple[float, float] | None = None
    handle_end_px: tuple[float, float] | None = None
    sanctuary_bbox: tuple[float, float, float, float] | None = None

    try:
        if not isinstance(bubble, dict):
            raise ValueError("bubble annotation missing")
        bubble_center = _point2(bubble.get("center_px"), "bubble.center_px")
        bubble_radius = float(bubble.get("radius_px"))
        if not math.isfinite(bubble_radius) or bubble_radius <= 0:
            raise ValueError("bubble.radius_px must be finite and positive")
        if not (0 <= bubble_center[0] < width and 0 <= bubble_center[1] < height):
            raise ValueError("bubble center lies outside raster")
        contact_point = _point2(ann.get("contact_point_p_px"), "contact_point_p_px")
        if not (0 <= contact_point[0] < width and 0 <= contact_point[1] < height):
            raise ValueError("contact point P lies outside raster")
        surface_distance = abs(_distance2(contact_point, bubble_center) - bubble_radius)
        if surface_distance > max(3.0, bubble_radius * 0.03):
            errors.append("P_NOT_ON_BUBBLE_SURFACE")
        if locked_contact_point_px is not None:
            drift = _distance2(contact_point, locked_contact_point_px)
            if drift > max(3.0, bubble_radius * 0.02):
                errors.append("CONTACT_POINT_P_DRIFTED")
        if not isinstance(cylinder, dict):
            raise ValueError("planted_cylinder annotation missing")

        cylinder_id = str(cylinder.get("instance_id", "")).strip() or None
        if not cylinder_id:
            errors.append("CYLINDER_INSTANCE_ID_MISSING")
        if expected_cylinder_instance_id and cylinder_id != expected_cylinder_instance_id:
            errors.append("CYLINDER_INSTANCE_CHANGED")
        handle = cylinder.get("side_handle")
        if not isinstance(handle, dict):
            raise ValueError("side_handle annotation missing")
        handle_id = str(handle.get("track_id", "")).strip() or None
        if not handle_id:
            errors.append("SIDE_HANDLE_TRACK_ID_MISSING")
        if expected_handle_track_id and handle_id != expected_handle_track_id:
            errors.append("SIDE_HANDLE_INSTANCE_CHANGED")

        base_px = _point2(cylinder.get("base_seat_center_px"), "base_seat_center_px")
        outer_px = _point2(cylinder.get("outer_end_cap_center_px"), "outer_end_cap_center_px")
        seat_distance = _distance2(base_px, contact_point)
        if seat_distance > max(3.0, bubble_radius * 0.02):
            errors.append("CONFORMAL_BASE_SEAT_MOVED_OFF_P")
        body_bbox = _valid_bbox(cylinder.get("body_bbox_xyxy_px"), "cylinder.body_bbox_xyxy_px", width, height)
        handle_bbox = _valid_bbox(handle.get("bbox_xyxy_px"), "side_handle.bbox_xyxy_px", width, height)
        handle_start_px = _point2(handle.get("axis_start_px"), "side_handle.axis_start_px")
        handle_end_px = _point2(handle.get("axis_end_px"), "side_handle.axis_end_px")
        for key, point in (("side_handle.axis_start_px", handle_start_px), ("side_handle.axis_end_px", handle_end_px)):
            if not (0 <= point[0] < width and 0 <= point[1] < height):
                errors.append(f"{key} lies outside the raster")
        if _distance2(handle_start_px, handle_end_px) < 4:
            errors.append("SIDE_HANDLE_PIXEL_AXIS_IMPLAUSIBLY_SHORT")
        if _distance2(base_px, outer_px) < 4:
            errors.append("CYLINDER_AXIS_PIXELS_IMPLAUSIBLY_SHORT")

        if cylinder.get("base_seat_surface") != "CONFORMAL_CURVED_SEAT_TO_BUBBLE":
            errors.append("WRONG_BASE_SEAT_SURFACE")
        if cylinder.get("full_base_contact_verified") is not True:
            errors.append("FULL_CONFORMAL_BASE_CONTACT_NOT_VERIFIED")
        if cylinder.get("outer_end_cap_clear") is not True:
            errors.append("OUTER_END_CAP_NOT_CLEAR")
        if cylinder.get("additional_handle_or_stub_detected") is not False:
            errors.append("NEW_HANDLE_OR_STUB_DETECTED_OR_UNVERIFIED")

        body_axis = _unit(cylinder.get("body_axis_world"), "body_axis_world")
        surface_normal = _unit(cylinder.get("bubble_surface_normal_world"), "bubble_surface_normal_world")
        handle_axis = _unit(handle.get("axis_world"), "side_handle.axis_world")
        normal_dot = _dot(body_axis, surface_normal)
        handle_body_dot = abs(_dot(handle_axis, body_axis))
        handle_normal_dot = abs(_dot(handle_axis, surface_normal))
        if normal_dot < math.cos(math.radians(15.0)):
            errors.append("CYLINDER_AXIS_NOT_ALIGNED_TO_LOCAL_BUBBLE_NORMAL")
        if handle_body_dot > math.sin(math.radians(20.0)):
            errors.append("SIDE_HANDLE_NOT_TRANSVERSE_TO_CYLINDER_AXIS")
        if handle_normal_dot > math.sin(math.radians(20.0)):
            errors.append("SIDE_HANDLE_NOT_TANGENT_TO_BUBBLE")

        base_world = _vec3(cylinder.get("base_center_world"), "base_center_world")
        cap_world = _vec3(cylinder.get("outer_end_cap_center_world"), "outer_end_cap_center_world")
        attach_world = _vec3(handle.get("attachment_world"), "side_handle.attachment_world")
        axis_world = tuple(cap_world[i] - base_world[i] for i in range(3))
        length_world = _norm(axis_world)
        if length_world < 1e-9:
            errors.append("WORLD_CYLINDER_AXIS_ZERO")
            attach_fraction = -1.0
        else:
            axis_unit = tuple(v / length_world for v in axis_world)
            attach_fraction = _dot(tuple(attach_world[i] - base_world[i] for i in range(3)), axis_unit) / length_world
            if not (0.35 <= attach_fraction <= 0.65):
                errors.append("SIDE_HANDLE_ATTACHMENT_NOT_AT_CYLINDER_MID_BODY")
        geometry_metrics = {
            "P_surface_distance_px": round(surface_distance, 3),
            "base_seat_to_P_distance_px": round(seat_distance, 3),
            "cylinder_axis_dot_surface_normal": round(normal_dot, 5),
            "handle_axis_dot_cylinder_axis_abs": round(handle_body_dot, 5),
            "handle_axis_dot_surface_normal_abs": round(handle_normal_dot, 5),
            "side_handle_attachment_fraction": round(attach_fraction, 5),
        }

        sanctuary_bbox = _valid_bbox(ann.get("sanctuary_bbox_xyxy_px"), "sanctuary_bbox_xyxy_px", width, height)
        locked_geometry = {
            "image_size_px": [width, height],
            "bubble_center_px": list(bubble_center),
            "bubble_radius_px": bubble_radius,
            "contact_point_p_px": list(contact_point),
            "cylinder_body_bbox_xyxy_px": list(body_bbox),
            "base_seat_center_px": list(base_px),
            "outer_end_cap_center_px": list(outer_px),
            "base_center_world": list(base_world),
            "outer_end_cap_center_world": list(cap_world),
            "body_axis_world": list(body_axis),
            "handle_bbox_xyxy_px": list(handle_bbox),
            "handle_axis_start_px": list(handle_start_px),
            "handle_axis_end_px": list(handle_end_px),
            "handle_axis_world": list(handle_axis),
            "handle_attachment_world": list(attach_world),
            "side_handle_track_id": handle_id,
            "cylinder_instance_id": cylinder_id,
            "sanctuary_bbox_xyxy_px": list(sanctuary_bbox),
            "scene_id": scene_id,
            "camera_rig_id": camera_rig_id,
            "camera_view_fingerprint": camera_view_fingerprint,
            "background_landmarks_sha256": raster_background_sha,
        }
    except (KeyError, TypeError, ValueError, IndexError) as exc:
        errors.append(f"GEOMETRY_ANNOTATION_INVALID:{exc}")

    # Track IDs are labels, not proof of invariant geometry. Compare coordinates and axes with the accepted master.
    if expected_locked_geometry is not None:
        lock = expected_locked_geometry
        if locked_geometry:
            if locked_geometry.get("image_size_px") != lock.get("image_size_px"):
                errors.append("CANVAS_SIZE_CHANGED_FROM_MASTER")
            for key, issue in (
                ("bubble_center_px", "BUBBLE_CENTER_DRIFTED_FROM_MASTER"),
                ("contact_point_p_px", "CONTACT_POINT_DRIFTED_FROM_MASTER"),
                ("base_seat_center_px", "BASE_SEAT_PIXEL_POSITION_DRIFTED"),
                ("outer_end_cap_center_px", "OUTER_END_CAP_PIXEL_POSITION_DRIFTED"),
                ("handle_axis_start_px", "HANDLE_AXIS_START_DRIFTED"),
                ("handle_axis_end_px", "HANDLE_AXIS_END_DRIFTED"),
            ):
                if key in lock and key in locked_geometry and _distance2(locked_geometry[key], lock[key]) > 2.0:
                    errors.append(issue)
            if abs(float(locked_geometry.get("bubble_radius_px", 0)) - float(lock.get("bubble_radius_px", 0))) > max(2.0, float(lock.get("bubble_radius_px", 0)) * 0.01):
                errors.append("BUBBLE_RADIUS_CHANGED_FROM_MASTER")
            for key, issue in (
                ("cylinder_body_bbox_xyxy_px", "CYLINDER_BODY_BBOX_CHANGED_FROM_MASTER"),
                ("handle_bbox_xyxy_px", "HANDLE_BBOX_CHANGED_FROM_MASTER"),
                ("sanctuary_bbox_xyxy_px", "SANCTUARY_BBOX_CHANGED_FROM_MASTER"),
            ):
                current_box, master_box = locked_geometry.get(key), lock.get(key)
                if current_box is not None and master_box is not None and any(abs(float(a) - float(b)) > 2.0 for a, b in zip(current_box, master_box)):
                    errors.append(issue)
            try:
                if _dot(_unit(locked_geometry["body_axis_world"], "body_axis_world"), _unit(lock["body_axis_world"], "master.body_axis_world")) < math.cos(math.radians(5.0)):
                    errors.append("CYLINDER_AXIS_ROTATED_FROM_MASTER")
                if abs(_dot(_unit(locked_geometry["handle_axis_world"], "handle_axis_world"), _unit(lock["handle_axis_world"], "master.handle_axis_world"))) < math.cos(math.radians(5.0)):
                    errors.append("SIDE_HANDLE_AXIS_ROTATED_FROM_MASTER")
                if math.dist(locked_geometry["base_center_world"], lock["base_center_world"]) > 0.02:
                    errors.append("CYLINDER_BASE_WORLD_POSITION_CHANGED")
                if math.dist(locked_geometry["outer_end_cap_center_world"], lock["outer_end_cap_center_world"]) > 0.02:
                    errors.append("CYLINDER_OUTER_CAP_WORLD_POSITION_CHANGED")
                if math.dist(locked_geometry["handle_attachment_world"], lock["handle_attachment_world"]) > 0.02:
                    errors.append("SIDE_HANDLE_ATTACHMENT_WORLD_POSITION_CHANGED")
            except (KeyError, TypeError, ValueError):
                errors.append("MASTER_GEOMETRY_LOCK_VECTOR_INCOMPLETE")
            if locked_geometry.get("cylinder_instance_id") != lock.get("cylinder_instance_id"):
                errors.append("CYLINDER_INSTANCE_CHANGED_FROM_MASTER")
            if locked_geometry.get("side_handle_track_id") != lock.get("side_handle_track_id"):
                errors.append("SIDE_HANDLE_TRACK_CHANGED_FROM_MASTER")
        else:
            errors.append("CURRENT_GEOMETRY_LOCK_VECTOR_MISSING")

    spec = STAGE_SPECS[stage]
    if not isinstance(heroine, dict):
        errors.append("HEROINE_ANNOTATION_MISSING")
        heroine = {}
    else:
        if heroine.get("present") is not spec["actor_present"]:
            errors.append("HEROINE_PRESENCE_WRONG_FOR_STAGE")
        if spec["actor_present"]:
            try:
                hero_box = _valid_bbox(heroine.get("bbox_xyxy_px"), "heroine.bbox_xyxy_px", width, height)
                hero_height = hero_box[3] - hero_box[1]
                hero_center = ((hero_box[0] + hero_box[2]) / 2.0, (hero_box[1] + hero_box[3]) / 2.0)
                hero_height_ratio = hero_height / max(2.0 * bubble_radius, 1.0)
                if hero_height_ratio > 0.60:
                    errors.append(f"HEROINE_TOO_LARGE_RELATIVE_TO_BUBBLE:{hero_height_ratio:.3f}")
            except (ValueError, TypeError) as exc:
                errors.append(f"HEROINE_BBOX_INVALID:{exc}")
                hero_height, hero_center = 0.0, (0.0, 0.0)
            if heroine.get("scale_class") != "MINIATURE":
                errors.append("HEROINE_SCALE_CLASS_NOT_MINIATURE")
            if not isinstance(heroine.get("identity_id"), str) or not heroine["identity_id"].strip():
                errors.append("HEROINE_IDENTITY_TRACK_MISSING")
            pose_signature = heroine.get("pose_signature")
            if not isinstance(pose_signature, str) or len(pose_signature) < 8:
                errors.append("HEROINE_POSE_SIGNATURE_MISSING")
            if expected_parent_evidence is not None:
                p_ann = expected_parent_evidence.get("raster_annotations", {})
                p_hero = p_ann.get("heroine", {}) if isinstance(p_ann, dict) else {}
                if p_hero.get("present") is True:
                    if heroine.get("identity_id") != p_hero.get("identity_id"):
                        errors.append("HEROINE_IDENTITY_CHANGED_FROM_PARENT")
                    try:
                        p_box = _valid_bbox(p_hero.get("bbox_xyxy_px"), "parent heroine bbox", width, height)
                        p_height = p_box[3] - p_box[1]
                        p_center = ((p_box[0] + p_box[2]) / 2.0, (p_box[1] + p_box[3]) / 2.0)
                        if p_height > 0 and abs(hero_height / p_height - 1.0) > 0.18:
                            errors.append("HEROINE_SCALE_JUMP_FROM_PARENT")
                        if _distance2(hero_center, p_center) > max(12.0, bubble_radius * 0.85):
                            errors.append("HEROINE_POSITION_JUMP_FROM_PARENT")
                    except (ValueError, TypeError):
                        errors.append("PARENT_HEROINE_BBOX_INVALID")
                    if stage in ("D1_APPROACH_NO_GRIP", "D2_FIRST_GRIP_EXISTING_HANDLE", "D3_TENSION_EXISTING_HANDLE") and pose_signature == p_hero.get("pose_signature"):
                        errors.append("AUTHORIZED_POSE_DELTA_NOT_VISIBLE")
        grip_id = heroine.get("gripping_handle_track_id")
        if spec["grip_existing_handle"]:
            if heroine.get("both_hands_on_existing_handle") is not True:
                errors.append("BOTH_HANDS_NOT_VERIFIED_ON_EXISTING_HANDLE")
            if not handle_id or grip_id != handle_id:
                errors.append("HEROINE_NOT_GRIPPING_THE_LOCKED_HANDLE_INSTANCE")
        elif grip_id not in (None, "") or heroine.get("both_hands_on_existing_handle") is True:
            errors.append("PRE_GRIP_STAGE_MUST_NOT_GRIP_HANDLE")

    if not isinstance(shell, dict):
        errors.append("SHELL_STATE_ANNOTATION_MISSING")
        shell = {}
    if shell.get("state") != spec["shell_state"]:
        errors.append("SHELL_STATE_WRONG_FOR_STAGE")
    if shell.get("crack_state") != spec["crack_state"]:
        errors.append("CRACK_STATE_WRONG_FOR_STAGE")
    if shell.get("base_glow_on_conformal_seat") is not True:
        errors.append("BASE_INTERFACE_GLOW_MISSING_OR_WRONG_ORIGIN")
    if not isinstance(shell.get("base_glow_origin_px"), (list, tuple)) or contact_point is None:
        errors.append("BASE_GLOW_ORIGIN_MISSING")
    else:
        try:
            glow_origin = _point2(shell.get("base_glow_origin_px"), "base_glow_origin_px")
            if _distance2(glow_origin, contact_point) > max(4.0, bubble_radius * 0.04):
                errors.append("BASE_GLOW_NOT_ORIGINATING_AT_P")
        except (ValueError, TypeError):
            errors.append("BASE_GLOW_ORIGIN_INVALID")
    if shell.get("sanctuary_state") != "INTACT" or shell.get("inhabitants_unharmed") is not True:
        errors.append("SANCTUARY_OR_INHABITANT_SAFETY_NOT_VERIFIED")

    if stage in ("E_MID_GLOW_CRACKS_FROM_P", "E_END_SHELL_SHATTER_FROM_P"):
        if shell.get("shell_only_breach") is not True:
            errors.append("BREACH_IS_NOT_SHELL_ONLY")
        if shell.get("crack_rays_radial_from_P") is not True:
            errors.append("RADIAL_CRACK_PROPAGATION_NOT_VERIFIED")
        if stage == "E_END_SHELL_SHATTER_FROM_P" and shell.get("fragments_propagate_outward_from_P") is not True:
            errors.append("SHARDS_NOT_VERIFIED_OUTWARD_FROM_P")
        crack_origin = shell.get("crack_origin_px")
        if not isinstance(crack_origin, (list, tuple)) or contact_point is None:
            errors.append("CRACK_ORIGIN_MISSING")
        else:
            try:
                origin = _point2(crack_origin, "crack_origin_px")
                if _distance2(origin, contact_point) > max(5.0, bubble_radius * 0.04):
                    errors.append("CRACKS_DO_NOT_ORIGINATE_AT_P")
            except (TypeError, ValueError):
                errors.append("CRACK_ORIGIN_INVALID")
    elif shell.get("crack_origin_px") not in (None, ""):
        errors.append("PRE_FX_STAGE_HAS_PREMATURE_CRACK_ORIGIN")

    anchor_sha = digest if stage == "B_LOCKED_TOOL_MASTER" else (expected_anchor_sha256 or "")
    errors.extend(_review_errors(
        evidence.get("review"),
        stage=stage,
        image_sha=digest,
        parent_sha=expected_parent_sha256,
        anchor_sha=anchor_sha,
    ))

    errors = sorted(set(errors))
    contract_valid = not errors
    return {
        "contract_valid": contract_valid,
        "eligible_for_next_stage": contract_valid,
        "status": "EXTERNAL_REVIEW_RECORD_BOUND" if contract_valid else "BLOCKED_PLANTED_BUBBLE_CONTRACT_FAIL",
        "stage": stage,
        "raster_path": str(path),
        "raster_sha256": digest,
        "raster_size_px": [width, height],
        "scene_anchor_raster_sha256": anchor_sha or None,
        "parent_raster_sha256": expected_parent_sha256,
        "locked_contact_point_p_px": list(locked_contact_point_px) if locked_contact_point_px else (list(contact_point) if contact_point else None),
        "cylinder_instance_id": cylinder_id,
        "side_handle_track_id": handle_id,
        "geometry_metrics": geometry_metrics,
        "locked_geometry": locked_geometry,
        "errors": errors,
        "visual_acceptance_status": "NOT_VERIFIED_BY_CODE",
        "limitation": "The code checks exact raster binding and submitted geometry/review records. It does not itself recognize the objects or authenticate that the named reviewer/model saw the pixels.",
    }



def build_stage_masks(
    parent_image_path: str | Path,
    parent_evidence: Mapping[str, Any],
    stage: str,
    outdir: str | Path,
) -> dict[str, str]:
    """Build complementary binary masks from the last accepted frame's reviewed geometry annotations.

    White in edit_mask.png means editable; white in freeze_mask.png means protected.
    These are conservative ROI masks, not segmentation. The raster-bound gate remains
    authoritative after generation because masks alone cannot guarantee pixel invariance.
    """
    if stage not in STAGE_SPECS:
        raise ValueError(f"Unknown mask stage {stage!r}")
    path = Path(parent_image_path)
    ann = parent_evidence.get("raster_annotations")
    if not path.is_file() or not isinstance(ann, dict):
        raise ValueError("mask construction requires a real accepted parent raster and its annotations")
    with Image.open(path) as source:
        width, height = source.size
    bubble = ann.get("bubble", {})
    cylinder = ann.get("planted_cylinder", {})
    handle = cylinder.get("side_handle", {}) if isinstance(cylinder, dict) else {}
    heroine = ann.get("heroine", {})
    shell = ann.get("shell", {})
    cx, cy = _point2(bubble.get("center_px"), "bubble.center_px")
    radius = float(bubble.get("radius_px"))
    if not math.isfinite(radius) or radius <= 0:
        raise ValueError("mask parent bubble radius is invalid")
    cylinder_box = _valid_bbox(cylinder.get("body_bbox_xyxy_px"), "planted_cylinder.body_bbox_xyxy_px", width, height)
    handle_box = _valid_bbox(handle.get("bbox_xyxy_px"), "side_handle.bbox_xyxy_px", width, height)
    sanctuary_box = _valid_bbox(ann.get("sanctuary_bbox_xyxy_px"), "sanctuary_bbox_xyxy_px", width, height)
    edit = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(edit)

    def rect(box: Sequence[float], pad: float = 0.0) -> tuple[int, int, int, int]:
        x0, y0, x1, y1 = [float(v) for v in box]
        return (
            max(0, int(math.floor(x0 - pad))),
            max(0, int(math.floor(y0 - pad))),
            min(width - 1, int(math.ceil(x1 + pad))),
            min(height - 1, int(math.ceil(y1 + pad))),
        )

    def protect(box: Sequence[float], pad: float = 0.0) -> None:
        draw.rectangle(rect(box, pad), fill=0)

    if stage == "C_PERSON_SCALE_NO_GRIP":
        # Add the miniature heroine in the left/lower scene region, not inside the bubble.
        draw.rectangle((0, int(height * 0.12), int(width * 0.56), int(height * 0.97)), fill=255)
        draw.ellipse((int(cx-radius), int(cy-radius), int(cx+radius), int(cy+radius)), fill=0)
        protect(sanctuary_box, 2)
        protect(cylinder_box, 5)
        protect(handle_box, 4)
    elif stage in ("D1_APPROACH_NO_GRIP", "D3_TENSION_EXISTING_HANDLE"):
        hero_box = heroine.get("bbox_xyxy_px") if isinstance(heroine, dict) else None
        if not isinstance(hero_box, (list, tuple)) or len(hero_box) != 4:
            raise ValueError(f"{stage} mask requires the parent heroine bbox")
        x0, y0, x1, y1 = [float(v) for v in hero_box]
        pad_x = max(12.0, (x1 - x0) * 0.40)
        pad_y = max(12.0, (y1 - y0) * 0.30)
        draw.rectangle(rect((x0, y0, x1, y1), max(pad_x, pad_y)), fill=255)
        # Preserve all non-actor objects, especially the tool and the existing handle.
        protect(cylinder_box, 5)
        protect(handle_box, 3)
        protect(sanctuary_box, 2)
    elif stage == "D2_FIRST_GRIP_EXISTING_HANDLE":
        hero_box = heroine.get("bbox_xyxy_px") if isinstance(heroine, dict) else None
        if not isinstance(hero_box, (list, tuple)) or len(hero_box) != 4:
            raise ValueError("D2 mask requires the parent heroine bbox")
        x0, y0, x1, y1 = [float(v) for v in hero_box]
        hx0, hy0, hx1, hy1 = [float(v) for v in handle_box]
        union = (min(x0, hx0), min(y0, hy0), max(x1, hx1), max(y1, hy1))
        pad = max(16.0, (y1 - y0) * 0.15)
        draw.rectangle(rect(union, pad), fill=255)
        # The handle may be temporarily under the fingers, but the cylinder itself is frozen;
        # its bbox, handle track, axis and world attachment are checked after generation.
        protect(cylinder_box, 5)
        protect(sanctuary_box, 2)
    elif stage in ("E_MID_GLOW_CRACKS_FROM_P", "E_END_SHELL_SHATTER_FROM_P"):
        # Edit the shell annulus and outward shatter zone, not the sanctuary.
        outer_radius = radius * (1.40 if stage == "E_END_SHELL_SHATTER_FROM_P" else 1.05)
        inner_radius = radius * 0.72
        draw.ellipse((cx-outer_radius, cy-outer_radius, cx+outer_radius, cy+outer_radius), fill=255)
        draw.ellipse((cx-inner_radius, cy-inner_radius, cx+inner_radius, cy+inner_radius), fill=0)
        # Open a small shell-local window around P for glow/crack growth without unfreezing the tool's body.
        px, py = _point2(ann.get("contact_point_p_px"), "contact_point_p_px")
        p_radius = max(5.0, radius * 0.08)
        draw.ellipse((px-p_radius, py-p_radius, px+p_radius, py+p_radius), fill=255)
        protect(cylinder_box, 2)
        protect(handle_box, 2)
        protect(sanctuary_box, 2)
    else:
        raise ValueError(f"{stage} does not have a parent-image mask stage")

    # Preserve a narrow border as an actual pixel landmark for same-camera/background checks.
    border_x = max(1, int(width * 0.02))
    border_y = max(1, int(height * 0.02))
    draw.rectangle((0, 0, width - 1, border_y - 1), fill=0)
    draw.rectangle((0, height - border_y, width - 1, height - 1), fill=0)
    draw.rectangle((0, 0, border_x - 1, height - 1), fill=0)
    draw.rectangle((width - border_x, 0, width - 1, height - 1), fill=0)
    freeze = Image.eval(edit, lambda value: 255 - value)
    root = Path(outdir)
    root.mkdir(parents=True, exist_ok=True)
    edit_path = root / "edit_mask.png"
    freeze_path = root / "freeze_mask.png"
    edit.save(edit_path)
    freeze.save(freeze_path)
    return {
        "edit_mask_path": str(edit_path.resolve()),
        "freeze_mask_path": str(freeze_path.resolve()),
        "mask_convention": "edit_mask white=editable; freeze_mask white=protected",
        "mask_provenance_parent_sha256": sha256_file(path),
        "mask_status": "BUILT_FROM_ACCEPTED_PARENT_ANNOTATIONS_NOT_SEGMENTATION",
    }


def compile_stage_request(
    stage: str,
    *,
    attempt_round: int,
    parent_image_path: str | None,
    parent_raster_sha256: str | None,
    scene_anchor_raster_sha256: str | None,
    locked_contact_point_px: Sequence[float] | None,
    locked_cylinder_instance_id: str | None,
    locked_handle_track_id: str | None,
    rejection_errors: Sequence[str] = (),
    master_selection: Mapping[str, Any] | None = None,
    parent_evidence: Mapping[str, Any] | None = None,
    mask_output_dir: str | Path | None = None,
    diagnostic_experiment: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Encode one stage contract and the last verified parent/error vector for a generator wrapper."""
    if stage not in STAGE_SPECS:
        raise ValueError(f"Unknown stage {stage!r}")
    spec = STAGE_SPECS[stage]
    mask_info: dict[str, str] = {}
    if stage != "B_LOCKED_TOOL_MASTER" and parent_image_path is not None:
        if parent_evidence is None or mask_output_dir is None:
            raise ValueError(f"{stage} requires parent_evidence and mask_output_dir to build protected edit masks")
        mask_info = build_stage_masks(parent_image_path, parent_evidence, stage, mask_output_dir)
    prompt = (
        f"CONTRACT={CONTRACT_ID}; CONTRACT_SHA256={contract_fingerprint()}; STAGE={stage}. "
        + "GLOBAL LOCKS: " + " | ".join(GLOBAL_LOCKS) + " "
        + "STAGE ACTION: " + spec["prompt"] + " "
        + "AUTHORIZED DELTAS ONLY: " + ", ".join(spec["authorized_delta_fields"]) + ". "
        + "FROZEN FIELDS: " + ", ".join(spec["must_preserve"]) + ". "
        + f"ATTEMPT={attempt_round}. LAST VERIFIED PARENT SHA256={parent_raster_sha256 or 'NONE_FOR_MASTER'}. "
        + f"MASTER ANCHOR SHA256={scene_anchor_raster_sha256 or 'SET_BY_ACCEPTED_MASTER'}. "
        + f"LOCKED P={list(locked_contact_point_px) if locked_contact_point_px else 'SET_BY_ACCEPTED_MASTER'}. "
        + f"LOCKED CYLINDER ID={locked_cylinder_instance_id or 'SET_BY_ACCEPTED_MASTER'}; "
        + f"LOCKED HANDLE TRACK={locked_handle_track_id or 'SET_BY_ACCEPTED_MASTER'}. "
        + (
            "HUMAN SELECTED SOURCE ATLAS: "
            + str(master_selection.get("source_atlas_image_path", ""))
            + "; SOURCE SHA256=" + str(master_selection.get("source_atlas_raster_sha256", ""))
            + "; ROI XYXY PX=" + str(master_selection.get("selected_roi_xyxy_px", ""))
            + ". Use this explicit ROI, never a printed label alone. "
            if stage == "B_LOCKED_TOOL_MASTER" and master_selection is not None else
            ("BLOCKED: a human ROI master-selection manifest is required before Stage B generation. "
             if stage == "B_LOCKED_TOOL_MASTER" else "")
        )
        + "PRIOR FAILURE VECTOR=" + ("; ".join(sorted(set(rejection_errors))) if rejection_errors else "NONE") + ". "
        + (
            "SHANNON-STYLE NEXT DIAGNOSTIC: " + str(diagnostic_experiment.get("action_id", "NONE"))
            + " — " + str(diagnostic_experiment.get("diagnostic_instruction", "No classified failure yet."))
            + ". Expected information gain/cost="
            + str(diagnostic_experiment.get("information_gain_per_cost", "NA"))
            + "; assumptions=" + str(diagnostic_experiment.get("assumptions_status", "UNVALIDATED_ENGINEERING_PRIORS"))
            + ". This selects an inspection/edit emphasis only and must not override hard locks. "
            if diagnostic_experiment is not None else
            "SHANNON-STYLE NEXT DIAGNOSTIC: none selected yet; preserve all hard locks. "
        )
        + "Return one independent full-frame raster and a raster-bound geometry annotation/review receipt. "
        + "If a lock conflicts with a requested change, preserve the lock and report the unmet change. "
        + "Do not invent a new handle, move P, unseat the base, or shatter the sanctuary."
    )
    return {
        "contract_id": CONTRACT_ID,
        "contract_sha256": contract_fingerprint(),
        "stage": stage,
        "attempt_round": attempt_round,
        "parent_image_path": parent_image_path,
        "parent_raster_sha256": parent_raster_sha256,
        "scene_anchor_raster_sha256": scene_anchor_raster_sha256,
        "locked_contact_point_p_px": list(locked_contact_point_px) if locked_contact_point_px else None,
        "locked_cylinder_instance_id": locked_cylinder_instance_id,
        "locked_handle_track_id": locked_handle_track_id,
        "master_selection": dict(master_selection) if master_selection is not None else None,
        "parent_geometry_annotation": dict(parent_evidence.get("raster_annotations", {})) if parent_evidence is not None else None,
        "parent_scene_identity": ({key: parent_evidence.get(key) for key in ("scene_id", "camera_rig_id", "camera_view_fingerprint", "background_landmarks_sha256")} if parent_evidence is not None else None),
        **mask_info,
        "authorized_delta_fields": list(spec["authorized_delta_fields"]),
        "must_preserve": list(spec["must_preserve"]),
        "global_locks": list(GLOBAL_LOCKS),
        "mask_policy": {
            "use_parent_image_as_reference": parent_image_path is not None,
            "freeze_all_unauthorized_regions": True,
            "edit_only_authorized_delta_regions": True,
            "one_full_frame_per_request": True,
            "source_hash_must_be_preserved_in_receipt": True,
        },
        "repair_error_vector": sorted(set(rejection_errors)),
        "diagnostic_experiment": dict(diagnostic_experiment) if diagnostic_experiment is not None else None,
        "prompt": prompt,
    }


CandidateBatch = Sequence[Candidate]
RerunProvider = Callable[[dict[str, Any], Path], CandidateBatch]


def _candidate_score(candidate: Candidate) -> tuple[float, float, str]:
    ranking = candidate.evidence.get("selection_metrics", {})
    try:
        creativity = float(ranking.get("creativity_score", 0.0))
    except (TypeError, ValueError):
        creativity = 0.0
    try:
        novelty = float(ranking.get("novelty_score", 0.0))
    except (TypeError, ValueError):
        novelty = 0.0
    digest = sha256_file(candidate.image_path) if candidate.image_path.is_file() else "MISSING"
    # Creativity/novelty are ranking signals only; they can never rescue a contract failure.
    return creativity, novelty, digest


def run_planted_bubble_closed_loop(
    outdir: str | Path,
    *,
    candidate_batches: Mapping[str, CandidateBatch] | None = None,
    rerun_provider: RerunProvider | None = None,
    max_retries: int = 2,
    master_selection: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Run B -> C -> D1 -> D2 -> D3 -> E-mid -> E-end without passing a failed frame.

    On retries, the provider always receives the last accepted parent raster—not a failed child.
    All candidates in a batch are audited before selecting the highest-ranked eligible candidate.
    """
    if not 0 <= max_retries <= 10:
        raise ValueError("max_retries must be between 0 and 10")
    root = Path(outdir).resolve()
    root.mkdir(parents=True, exist_ok=True)
    batches = candidate_batches or {}
    configured_selection: Mapping[str, Any] | None = master_selection
    if configured_selection is None:
        seed_candidates = list(batches.get("B_LOCKED_TOOL_MASTER", []))
        if seed_candidates:
            seed_selection = seed_candidates[0].evidence.get("master_selection")
            if isinstance(seed_selection, dict):
                configured_selection = seed_selection
    attempt_log: list[dict[str, Any]] = []
    accepted_stages: dict[str, dict[str, Any]] = {}
    total_reruns = 0
    total_rejections = 0
    parent_path: Path | None = None
    parent_sha: str | None = None
    anchor_sha: str | None = None
    locked_p: tuple[float, float] | None = None
    cylinder_id: str | None = None
    handle_id: str | None = None
    locked_geometry: dict[str, Any] | None = None
    parent_evidence: dict[str, Any] | None = None
    scene_lock: dict[str, Any] | None = None
    block_status: str | None = None

    for stage in STAGE_ORDER:
        stage_candidates = list(batches.get(stage, []))
        rejection_vector: list[str] = []
        stage_accepted: Candidate | None = None
        stage_validation: dict[str, Any] | None = None

        for attempt_round in range(max_retries + 1):
            if attempt_round > 0 or not stage_candidates:
                if rerun_provider is None:
                    break
                if stage == "B_LOCKED_TOOL_MASTER" and configured_selection is None:
                    rejection_vector = sorted(set(rejection_vector + ["HUMAN_MASTER_SELECTION_REQUIRED"]))
                    block_status = "BLOCKED_HUMAN_MASTER_SELECTION_REQUIRED"
                    break
                request_dir = root / "provider_requests" / f"{stage}_R{attempt_round:02d}"
                request_dir.mkdir(parents=True, exist_ok=True)
                diagnostic = (
                    recommend_next_experiment(rejection_vector, attempt_log)
                    if rejection_vector else None
                )
                diagnostic = diagnostic["selected_experiment"] if diagnostic else None
                request = compile_stage_request(
                    stage,
                    attempt_round=attempt_round,
                    parent_image_path=str(parent_path) if parent_path else None,
                    parent_raster_sha256=parent_sha,
                    scene_anchor_raster_sha256=anchor_sha,
                    locked_contact_point_px=locked_p,
                    locked_cylinder_instance_id=cylinder_id,
                    locked_handle_track_id=handle_id,
                    rejection_errors=rejection_vector,
                    master_selection=configured_selection,
                    parent_evidence=parent_evidence,
                    mask_output_dir=request_dir / "masks",
                    diagnostic_experiment=diagnostic,
                )
                request_path = request_dir / "request.json"
                request_path.write_text(json.dumps(request, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                total_reruns += 1
                try:
                    stage_candidates = list(rerun_provider(request, request_dir))
                except Exception as exc:
                    stage_candidates = []
                    rejection_vector = sorted(set(rejection_vector + [f"PROVIDER_ERROR:{type(exc).__name__}:{exc}"]))
                if not stage_candidates:
                    rejection_vector = sorted(set(rejection_vector + ["PROVIDER_RETURNED_NO_CANDIDATES"]))
                    continue

            reviewed_batch: list[tuple[Candidate, dict[str, Any]]] = []
            for candidate in stage_candidates:
                cand_path = Path(candidate.image_path).resolve()
                item = Candidate(cand_path, candidate.evidence)
                validation = validate_planted_bubble_frame(
                    cand_path,
                    item.evidence,
                    expected_stage=stage,
                    expected_parent_sha256=parent_sha,
                    expected_anchor_sha256=anchor_sha,
                    locked_contact_point_px=locked_p,
                    expected_cylinder_instance_id=cylinder_id,
                    expected_handle_track_id=handle_id,
                    expected_locked_geometry=locked_geometry,
                    expected_scene_lock=scene_lock,
                    expected_parent_evidence=parent_evidence,
                    expected_parent_image_path=parent_path,
                )
                is_valid = bool(validation["eligible_for_next_stage"])
                scores = _candidate_score(item)
                record = AttemptRecord(
                    stage=stage,
                    attempt_round=attempt_round,
                    raster_path=str(cand_path),
                    raster_sha256=str(validation.get("raster_sha256", "MISSING")),
                    contract_valid=is_valid,
                    eligible_for_next_stage=is_valid,
                    errors=list(validation.get("errors", [])),
                    creativity_score=scores[0],
                    novelty_score=scores[1],
                )
                attempt_log.append(asdict(record))
                if is_valid:
                    reviewed_batch.append((item, validation))
                else:
                    total_rejections += 1
                    rejection_vector.extend(validation.get("errors", []))
            rejection_vector = sorted(set(rejection_vector))

            # Shannon feedback policy: evaluate the entire candidate batch, select only among
            # evidence-complete candidates, and keep creativity/novelty downstream of hard gates.
            if reviewed_batch:
                chosen, stage_validation = max(reviewed_batch, key=lambda pair: _candidate_score(pair[0]))
                stage_accepted = chosen
                break
            stage_candidates = []

        if stage_accepted is None or stage_validation is None:
            block_status = f"BLOCKED_NO_EVIDENCE_PASS_{stage}"
            break

        stage_dir = root / "locked_frames"
        stage_dir.mkdir(parents=True, exist_ok=True)
        suffix = stage_accepted.image_path.suffix or ".png"
        locked_path = stage_dir / f"{stage}{suffix}"
        if stage_accepted.image_path.resolve() != locked_path.resolve():
            shutil.copy2(stage_accepted.image_path, locked_path)
        locked_sha = sha256_file(locked_path)
        if locked_sha != stage_validation["raster_sha256"]:
            block_status = f"BLOCKED_LOCKED_COPY_SHA_MISMATCH_{stage}"
            break
        stage_validation = dict(stage_validation)
        stage_validation["raster_path"] = str(locked_path)
        stage_validation["raster_sha256"] = locked_sha
        accepted_stages[stage] = stage_validation
        for record in reversed(attempt_log):
            if record["stage"] == stage and record["raster_sha256"] == locked_sha and record["eligible_for_next_stage"]:
                record["selected"] = True
                break

        if stage == "B_LOCKED_TOOL_MASTER":
            anchor_sha = locked_sha
            locked_p = tuple(stage_validation["locked_contact_point_p_px"])  # type: ignore[assignment]
            cylinder_id = stage_validation["cylinder_instance_id"]
            handle_id = stage_validation["side_handle_track_id"]
            locked_geometry = dict(stage_validation["locked_geometry"])
            scene_lock = {key: locked_geometry[key] for key in ("scene_id", "camera_rig_id", "camera_view_fingerprint", "background_landmarks_sha256")}
        parent_path = locked_path
        parent_sha = locked_sha
        parent_evidence = dict(stage_accepted.evidence)

    all_passed = len(accepted_stages) == len(STAGE_ORDER) and block_status is None
    report = {
        "workflow": "shannon-inspired-planted-cylinder-bubble-break-v1",
        "contract_id": CONTRACT_ID,
        "contract_sha256": contract_fingerprint(),
        "status": "ALL_STAGE_EVIDENCE_PACKETS_PASS_REVIEW_NOT_VERIFIED_BY_CODE" if all_passed else (block_status or "BLOCKED"),
        "stage_order": list(STAGE_ORDER),
        "accepted_stage_count": len(accepted_stages),
        "required_stage_count": len(STAGE_ORDER),
        "accepted_stages": accepted_stages,
        "attempt_log": attempt_log,
        "total_rerun_provider_calls": total_reruns,
        "total_rejected_candidates": total_rejections,
        "locked_contact_point_p_px": list(locked_p) if locked_p else None,
        "locked_cylinder_instance_id": cylinder_id,
        "locked_handle_track_id": handle_id,
        "visual_acceptance_status": "NOT_VERIFIED_BY_CODE",
        "review_interpretation": "External review receipts are hash-bound records; this program does not authenticate reviewer identity or visually recognize the raster.",
        "next_stage_allowed": all_passed,
    }
    (root / "SHANNON_PLANTED_BUBBLE_RUN_MANIFEST.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return report


def load_candidate_manifest(path: str | Path) -> dict[str, list[Candidate]]:
    """Load an offline candidate/evidence bundle; paths are resolved relative to the manifest."""
    manifest_path = Path(path).resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    raw_batches = manifest.get("candidate_batches")
    if not isinstance(raw_batches, dict):
        raise ValueError("manifest must contain object field candidate_batches")
    root = manifest_path.parent
    batches: dict[str, list[Candidate]] = {}
    for stage, items in raw_batches.items():
        if stage not in STAGE_SPECS or not isinstance(items, list):
            raise ValueError(f"invalid stage candidate list: {stage}")
        candidates: list[Candidate] = []
        for item in items:
            if not isinstance(item, dict) or not isinstance(item.get("image"), str):
                raise ValueError(f"{stage}: each candidate needs an image path")
            image_path = Path(item["image"])
            if not image_path.is_absolute():
                image_path = root / image_path
            if isinstance(item.get("evidence"), dict):
                evidence = dict(item["evidence"])
            elif isinstance(item.get("evidence_json"), str):
                evidence_path = Path(item["evidence_json"])
                if not evidence_path.is_absolute():
                    evidence_path = root / evidence_path
                evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
            else:
                raise ValueError(f"{stage}: each candidate needs inline evidence or evidence_json")
            selection = evidence.get("master_selection")
            if isinstance(selection, dict) and isinstance(selection.get("source_atlas_image_path"), str):
                atlas_path = Path(selection["source_atlas_image_path"])
                if not atlas_path.is_absolute():
                    selection["source_atlas_image_path"] = str((root / atlas_path).resolve())
            candidates.append(Candidate(image_path.resolve(), evidence))
        batches[stage] = candidates
    return batches


def command_provider(command: str, *, base_cwd: Path | None = None) -> RerunProvider:
    """Adapter contract for any external generator/reviewer wrapper; no provider is bundled or implied.

    Invoke COMMAND with the absolute path to request.json. It must write one JSON object to stdout, e.g.
    {"candidates":[{"image":"path.png","evidence":{...}}]} or use an evidence_json path.
    Relative image/evidence paths are resolved from the request directory. Credentials/provider setup belong
    to that external command. This adapter is a handoff interface, not a connected Gemini API.
    """
    argv = shlex.split(command)
    if not argv:
        raise ValueError("provider command is empty")
    cwd = (base_cwd or Path.cwd()).resolve()

    def invoke(request: dict[str, Any], request_dir: Path) -> CandidateBatch:
        request_path = request_dir / "request.json"
        request_path.write_text(json.dumps(request, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        completed = subprocess.run(
            argv + [str(request_path.resolve())],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            check=False,
        )
        (request_dir / "provider_stdout.txt").write_text(completed.stdout or "", encoding="utf-8")
        (request_dir / "provider_stderr.txt").write_text(completed.stderr or "", encoding="utf-8")
        if completed.returncode != 0:
            raise RuntimeError(f"provider command exit code {completed.returncode}")
        try:
            response = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise ValueError("provider stdout must be one JSON object") from exc
        records = response.get("candidates", []) if isinstance(response, dict) else []
        candidates: list[Candidate] = []
        for record in records:
            if not isinstance(record, dict) or not isinstance(record.get("image"), str):
                continue
            image_path = Path(record["image"])
            if not image_path.is_absolute():
                image_path = request_dir / image_path
            if isinstance(record.get("evidence"), dict):
                evidence = dict(record["evidence"])
            elif isinstance(record.get("evidence_json"), str):
                evidence_path = Path(record["evidence_json"])
                if not evidence_path.is_absolute():
                    evidence_path = request_dir / evidence_path
                evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
            else:
                continue
            if str(request.get("stage", "")).upper() == "B_LOCKED_TOOL_MASTER" and not isinstance(evidence.get("master_selection"), dict):
                selection = request.get("master_selection")
                if isinstance(selection, dict):
                    evidence["master_selection"] = dict(selection)
            selection = evidence.get("master_selection")
            if isinstance(selection, dict) and isinstance(selection.get("source_atlas_image_path"), str):
                atlas_path = Path(selection["source_atlas_image_path"])
                if not atlas_path.is_absolute():
                    selection["source_atlas_image_path"] = str((request_dir / atlas_path).resolve())
            candidates.append(Candidate(image_path.resolve(), evidence))
        return candidates

    return invoke


def compile_prompt_packet(outdir: str | Path) -> dict[str, Any]:
    root = Path(outdir).resolve()
    root.mkdir(parents=True, exist_ok=True)
    prompts_dir = root / "stage_prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, Any] = {
        "contract_id": CONTRACT_ID,
        "contract_sha256": contract_fingerprint(),
        "stage_order": list(STAGE_ORDER),
        "global_locks": list(GLOBAL_LOCKS),
        "stages": {},
        "image_realization": "NOT_RUN_BY_PROMPT_COMPILER",
        "visual_acceptance_status": "NOT_VERIFIED_BY_CODE",
    }
    for stage in STAGE_ORDER:
        request = compile_stage_request(
            stage,
            attempt_round=0,
            parent_image_path=None,
            parent_raster_sha256=None,
            scene_anchor_raster_sha256=None,
            locked_contact_point_px=None,
            locked_cylinder_instance_id=None,
            locked_handle_track_id=None,
        )
        target = prompts_dir / f"{stage}.json"
        target.write_text(json.dumps(request, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        manifest["stages"][stage] = {
            "prompt_file": str(target.relative_to(root)),
            "authorized_delta_fields": request["authorized_delta_fields"],
            "must_preserve": request["must_preserve"],
        }
    (root / "SHANNON_PLANTED_BUBBLE_PROMPT_PACKET.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=Path("out/shannon_planted_bubble"))
    parser.add_argument("--candidate-manifest", type=Path, default=None)
    parser.add_argument("--master-selection-json", type=Path, default=None,
                        help="required for provider-generated Stage B unless the candidate manifest already embeds a human ROI selection")
    parser.add_argument("--provider-command", type=str, default=None,
                        help="optional external command wrapper; this repository does not bundle a generator")
    parser.add_argument("--max-retries", type=int, default=2)
    parser.add_argument("--compile-only", action="store_true")
    args = parser.parse_args(argv)
    if args.compile_only:
        manifest = compile_prompt_packet(args.outdir)
        print(json.dumps({
            "status": "PROMPT_PACKET_COMPILED",
            "contract_id": manifest["contract_id"],
            "stages": len(manifest["stages"]),
            "image_realization": manifest["image_realization"],
            "visual_acceptance_status": manifest["visual_acceptance_status"],
            "outdir": str(args.outdir),
        }, ensure_ascii=False, indent=2))
        return 0
    if args.candidate_manifest is None and not args.provider_command:
        parser.error("supply --candidate-manifest and/or --provider-command, or use --compile-only")
    try:
        batches = load_candidate_manifest(args.candidate_manifest) if args.candidate_manifest else {}
        provider = command_provider(args.provider_command) if args.provider_command else None
        selection = load_master_selection_manifest(args.master_selection_json) if args.master_selection_json else None
        report = run_planted_bubble_closed_loop(
            args.outdir,
            candidate_batches=batches,
            rerun_provider=provider,
            max_retries=args.max_retries,
            master_selection=selection,
        )
    except (OSError, ValueError, json.JSONDecodeError, RuntimeError) as exc:
        print(f"BLOCK: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({
        "status": report["status"],
        "accepted_stage_count": report["accepted_stage_count"],
        "required_stage_count": report["required_stage_count"],
        "total_rerun_provider_calls": report["total_rerun_provider_calls"],
        "total_rejected_candidates": report["total_rejected_candidates"],
        "visual_acceptance_status": report["visual_acceptance_status"],
        "manifest": str(Path(args.outdir).resolve() / "SHANNON_PLANTED_BUBBLE_RUN_MANIFEST.json"),
    }, ensure_ascii=False, indent=2))
    return 0 if report["next_stage_allowed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
