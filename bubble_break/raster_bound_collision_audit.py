#!/usr/bin/env python3
"""Bind dual-T-hammer geometry annotations to one exact raster before any review decision.

This is an evidence-integrity gate, not a vision model. It checks the supplied annotation
contract and its binding to a raster; it NEVER claims to infer geometry from pixels itself.
Visual acceptance remains NOT_VERIFIED_BY_CODE until a real semantic vision judge or
human review has explicitly inspected the exact raster.
"""
from __future__ import annotations

import hashlib
import math
from pathlib import Path
from typing import Any

from PIL import Image

from bubble_break.dual_t_hammer_collision import validate_collision_evidence


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _point(raw: Any, key: str) -> tuple[float, float]:
    if not isinstance(raw, (list, tuple)) or len(raw) != 2:
        raise ValueError(f"{key} must be a 2-vector [x,y] in raster pixels")
    point = (float(raw[0]), float(raw[1]))
    if not all(math.isfinite(v) for v in point):
        raise ValueError(f"{key} must contain finite coordinates")
    return point


def _bbox(raw: Any, key: str, width: int, height: int) -> tuple[float, float, float, float]:
    if not isinstance(raw, (list, tuple)) or len(raw) != 4:
        raise ValueError(f"{key} must be [x0,y0,x1,y1]")
    box = tuple(float(v) for v in raw)
    if not all(math.isfinite(v) for v in box):
        raise ValueError(f"{key} must contain finite values")
    x0, y0, x1, y1 = box
    if not (0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height):
        raise ValueError(f"{key} must be a non-empty box fully inside the raster")
    return box  # type: ignore[return-value]


def _axis(raw: Any, key: str, width: int, height: int) -> tuple[tuple[float, float], tuple[float, float]]:
    if not isinstance(raw, (list, tuple)) or len(raw) != 2:
        raise ValueError(f"{key} must contain two [x,y] endpoints")
    p0 = _point(raw[0], f"{key}[0]")
    p1 = _point(raw[1], f"{key}[1]")
    for x, y in (p0, p1):
        if not (0 <= x < width and 0 <= y < height):
            raise ValueError(f"{key} endpoints must be inside the raster")
    length = math.dist(p0, p1)
    if length < 2.0:
        raise ValueError(f"{key} is too short to establish a visible axis")
    return p0, p1


def _midpoint(axis: tuple[tuple[float, float], tuple[float, float]]) -> tuple[float, float]:
    return ((axis[0][0] + axis[1][0]) / 2.0, (axis[0][1] + axis[1][1]) / 2.0)


def validate_raster_bound_collision_evidence(
    image_path: str | Path,
    evidence: dict[str, Any],
) -> dict[str, Any]:
    """Validate geometry evidence and prove it refers to the exact raster bytes.

    Required extra evidence fields:
      raster_sha256: SHA-256 of the exact candidate image bytes
      raster_annotations: image_width_px, image_height_px, reviewer_or_model,
        tool_a/tool_b annotations (distinct instance_id, head/handle boxes, head/handle
        axes, strike-face center and radius), and contact_point_px for FIRST_CONTACT.

    This validates schema, internal geometry consistency, dimensions, and image binding.
    It does not replace semantic image inspection; visual acceptance deliberately remains
    NOT_VERIFIED_BY_CODE.
    """
    path = Path(image_path)
    if not path.is_file():
        return {
            "accepted": False,
            "status": "BLOCKED_RASTER_MISSING",
            "errors": [f"raster does not exist: {path}"],
            "visual_acceptance_status": "NOT_VERIFIED_BY_CODE",
        }

    digest = sha256_file(path)
    errors: list[str] = []
    declared_hash = evidence.get("raster_sha256")
    if not isinstance(declared_hash, str) or declared_hash.lower() != digest:
        errors.append("raster_sha256 is missing or does not match the exact raster bytes")

    annotations = evidence.get("raster_annotations")
    if not isinstance(annotations, dict):
        errors.append("raster_annotations is required; boolean 'tool present' claims alone are insufficient")
        annotations = {}

    try:
        with Image.open(path) as image:
            width, height = image.size
            image.verify()
    except Exception as exc:
        return {
            "accepted": False,
            "status": "BLOCKED_UNREADABLE_RASTER",
            "raster_sha256": digest,
            "errors": errors + [f"unable to read raster: {exc}"],
            "visual_acceptance_status": "NOT_VERIFIED_BY_CODE",
        }

    try:
        declared_size = (int(annotations["image_width_px"]), int(annotations["image_height_px"]))
        if declared_size != (width, height):
            errors.append(f"annotation dimensions {declared_size} do not match raster dimensions {(width, height)}")
        annotator = annotations.get("reviewer_or_model")
        if not isinstance(annotator, str) or not annotator.strip():
            errors.append("raster annotation must identify the human reviewer or vision model/version")

        tools: dict[str, dict[str, Any]] = {}
        for tool_key in ("tool_a", "tool_b"):
            item = annotations.get(tool_key)
            if not isinstance(item, dict):
                errors.append(f"{tool_key} raster annotation is required")
                continue
            instance_id = item.get("instance_id")
            if not isinstance(instance_id, str) or not instance_id.strip():
                errors.append(f"{tool_key}.instance_id is required")
            tools[tool_key] = item
            _bbox(item.get("head_bbox_xyxy_px"), f"{tool_key}.head_bbox_xyxy_px", width, height)
            _bbox(item.get("handle_bbox_xyxy_px"), f"{tool_key}.handle_bbox_xyxy_px", width, height)
            head_axis = _axis(item.get("head_axis_px"), f"{tool_key}.head_axis_px", width, height)
            handle_axis = _axis(item.get("handle_axis_px"), f"{tool_key}.handle_axis_px", width, height)
            face_center = _point(item.get("strike_face_center_px"), f"{tool_key}.strike_face_center_px")
            radius = float(item.get("strike_face_radius_px"))
            if not (0 <= face_center[0] < width and 0 <= face_center[1] < height):
                errors.append(f"{tool_key}.strike_face_center_px is outside the raster")
            if not math.isfinite(radius) or radius <= 0:
                errors.append(f"{tool_key}.strike_face_radius_px must be finite and positive")
            if radius > max(width, height):
                errors.append(f"{tool_key}.strike_face_radius_px is implausibly larger than the raster")
            hx, hy = head_axis[1][0] - head_axis[0][0], head_axis[1][1] - head_axis[0][1]
            gx, gy = handle_axis[1][0] - handle_axis[0][0], handle_axis[1][1] - handle_axis[0][1]
            cosine = abs((hx * gx + hy * gy) / (math.hypot(hx, hy) * math.hypot(gx, gy)))
            if cosine > 0.35:
                errors.append(f"{tool_key} handle axis is not visibly transverse to its head axis (|cos|={cosine:.3f})")
            center = _midpoint(head_axis)
            joint_distance = min(math.dist(center, handle_axis[0]), math.dist(center, handle_axis[1]))
            head_length = math.dist(*head_axis)
            if joint_distance > max(4.0, head_length * 0.25):
                errors.append(f"{tool_key} handle is not visibly attached near the head midpoint")
            x0, y0, x1, y1 = _bbox(item.get("head_bbox_xyxy_px"), f"{tool_key}.head_bbox_xyxy_px", width, height)
            if not (x0 <= face_center[0] <= x1 and y0 <= face_center[1] <= y1):
                errors.append(f"{tool_key} striking-face center is outside its own head bounds")

        if len(tools) == 2:
            ids = [item.get("instance_id") for item in tools.values()]
            if ids[0] == ids[1]:
                errors.append("HAMMER_A and HAMMER_B must be distinct raster instances")

        stage = str(evidence.get("stage", "")).upper()
        if stage == "FIRST_CONTACT" and len(tools) == 2:
            p = _point(annotations.get("contact_point_px"), "contact_point_px")
            for key, item in tools.items():
                center = _point(item.get("strike_face_center_px"), f"{key}.strike_face_center_px")
                radius = float(item.get("strike_face_radius_px"))
                if math.dist(p, center) > radius + 1.5:
                    errors.append(f"contact point P is outside {key}'s annotated striking-face disk")
    except (KeyError, TypeError, ValueError) as exc:
        errors.append(f"invalid raster annotation schema: {exc}")

    geometry = validate_collision_evidence(evidence)
    if not geometry.get("accepted", False):
        errors.extend(geometry.get("errors", ["dual-hammer geometry contract failed"]))

    accepted = not errors
    return {
        "accepted": accepted,
        "status": "RASTER_BOUND_GEOMETRY_ANNOTATION_PASS" if accepted else "BLOCKED_RASTER_BOUND_GEOMETRY_EVIDENCE",
        "raster_path": str(path),
        "raster_sha256": digest,
        "raster_size_px": [width, height],
        "geometry_evidence": geometry,
        "errors": errors,
        "visual_acceptance_status": "NOT_VERIFIED_BY_CODE",
        "limitation": "Raster hash and annotation contract are checked; the code has not itself visually recognized or approved the pictured geometry.",
    }
