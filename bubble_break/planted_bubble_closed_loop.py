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

from PIL import Image


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
        _valid_bbox(cylinder.get("body_bbox_xyxy_px"), "cylinder.body_bbox_xyxy_px", width, height)
        _valid_bbox(handle.get("bbox_xyxy_px"), "side_handle.bbox_xyxy_px", width, height)
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
    except (KeyError, TypeError, ValueError, IndexError) as exc:
        errors.append(f"GEOMETRY_ANNOTATION_INVALID:{exc}")

    spec = STAGE_SPECS[stage]
    if not isinstance(heroine, dict):
        errors.append("HEROINE_ANNOTATION_MISSING")
        heroine = {}
    else:
        if heroine.get("present") is not spec["actor_present"]:
            errors.append("HEROINE_PRESENCE_WRONG_FOR_STAGE")
        if spec["actor_present"]:
            try:
                _valid_bbox(heroine.get("bbox_xyxy_px"), "heroine.bbox_xyxy_px", width, height)
            except (ValueError, TypeError) as exc:
                errors.append(f"HEROINE_BBOX_INVALID:{exc}")
            if heroine.get("scale_class") != "MINIATURE":
                errors.append("HEROINE_SCALE_CLASS_NOT_MINIATURE")
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
        "errors": errors,
        "visual_acceptance_status": "NOT_VERIFIED_BY_CODE",
        "limitation": "The code checks exact raster binding and submitted geometry/review records. It does not itself recognize the objects or authenticate that the named reviewer/model saw the pixels.",
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
                )
                request_dir = root / "provider_requests" / f"{stage}_R{attempt_round:02d}"
                request_dir.mkdir(parents=True, exist_ok=True)
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
        parent_path = locked_path
        parent_sha = locked_sha

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
        report = run_planted_bubble_closed_loop(
            args.outdir,
            candidate_batches=batches,
            rerun_provider=provider,
            max_retries=args.max_retries,
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
