#!/usr/bin/env python3
"""Mainline Bubble-Break Frame Pipeline (`H0 -> H1 -> H2 -> H2B -> H3`) & Raster-Bound Semantic/Geometric Gate.

**LEGACY CONTRACT NOTICE:** this file's T-hammer/H0-H2-H3 topology is not the latest B3-derived planted-cylinder design documented in docs/半成HAM.txt. Use bubble_break.planted_bubble_closed_loop for the current side-middle-handle/conformal-seat workflow; this module remains for historical comparison and must not approve that workflow.

Enforces the PR #1 & PR #4 historical Bubble-Break contract:
1. Mainline task is a SINGLE calibrated T-hammer (`HAMMER_A`) striking a transparent containment bubble at
   a locked surface pole `P` (`outward_normal = -n`, `hammer_face_normal = +n`, `dot = -1`), NOT two hammers
   colliding in the final scene, and NOT a handleless cylinder ram.
2. Legacy pixel gates alone can NEVER declare a bubble-break frame passed. Without SHA-256 bound geometric
   and semantic evidence attached to the exact raster bytes, validation returns:
     `status = "BLOCKED_BUBBLE_BREAK_SEMANTIC_EVIDENCE_MISSING"`.
3. Every bubble-break stage (`H0_PRE_IMPACT`, `H1_PRE_NEAR`, `H2_FIRST_CONTACT`, `H2B_CRACK_PROPAGATION`,
   `H3_FOLLOWTHROUGH_SHELL_SHATTER`) is verified for:
   - Exact `raster_sha256` & `image_width_px` / `image_height_px` match.
   - Single T-hammer rigid-body topology: horizontal head axis aligned with `+n`, single 90° handle attached
     at the head midpoint (`|cos| <= 0.35`, `joint_offset_ratio <= 0.25` — rejecting L-shape handle slide),
     and `has_forbidden_lower_handle_stub == False` (rejecting cross-shaped handle stubs below the head).
   - Contact surface is strictly `FLAT_END_FACE_TO_BUBBLE_POLE_P` (for `H2`, `H2B`, `H3`) or `NONE` (for `H0`, `H1`).
   - Monotonic pre-contact gap narrowing (`H0 >= 0.08`, `0.004 <= H1 < H0`, `H2 == 0.0`, `H2B == 0.0`, `H3 >= 0.0`).
   - Causal fracture origin: for `H2`, `H2B`, `H3`, `crack_origin_px` must lie within `15 px` of the locked
     bubble pole `P` (`cracks_originate_strictly_from_p == True`).
   - Interior sanctuary & inhabitants protection: `shell_only_breach == True`, `inhabitants_unharmed == True`,
     and measured interior sanctuary warmth (`R - B` mean in `sanctuary_bbox_xyxy_px`) `>= 15.0`.
"""
from __future__ import annotations

import hashlib
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageDraw


BUBBLE_BREAK_STAGES: tuple[str, ...] = (
    "H0_PRE_IMPACT",
    "H1_PRE_NEAR",
    "H2_FIRST_CONTACT",
    "H2B_CRACK_PROPAGATION",
    "H3_FOLLOWTHROUGH_SHELL_SHATTER",
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def measure_sanctuary_warmth_and_contact_luma(
    image_path: Path,
    contact_point_p_px: list[float],
    sanctuary_bbox_xyxy_px: list[float],
) -> dict[str, float]:
    """Measure contact flash peak luma near P and golden warmth inside the miniature sanctuary bbox."""
    im = Image.open(image_path).convert("RGB")
    arr = np.asarray(im, dtype=np.float32)
    gray = arr.mean(axis=2)
    h, w = gray.shape

    px, py = int(round(contact_point_p_px[0])), int(round(contact_point_p_px[1]))
    x0, x1 = max(0, px - 28), min(w, px + 28)
    y0, y1 = max(0, py - 28), min(h, py + 28)
    p_patch = gray[y0:y1, x0:x1]
    contact_peak_luma = float(p_patch.max()) if p_patch.size else 0.0

    sx0, sy0, sx1, sy1 = [int(round(v)) for v in sanctuary_bbox_xyxy_px]
    sx0, sx1 = max(0, sx0), min(w, sx1)
    sy0, sy1 = max(0, sy0), min(h, sy1)
    s_rgb = arr[sy0:sy1, sx0:sx1]
    sanctuary_warmth = float((s_rgb[..., 0] - s_rgb[..., 2]).mean()) if s_rgb.size else 0.0
    sanctuary_luma_std = float(gray[sy0:sy1, sx0:sx1].std()) if s_rgb.size else 0.0

    return {
        "contact_peak_luma_at_p": round(contact_peak_luma, 2),
        "sanctuary_warmth_r_minus_b": round(sanctuary_warmth, 2),
        "sanctuary_detail_std": round(sanctuary_luma_std, 2),
    }


def validate_bubble_break_frame_evidence(
    image_path: str | Path,
    evidence: dict[str, Any] | None,
    *,
    locked_pole_p_px: tuple[float, float] = (755.0, 384.0),
    max_pole_drift_px: float = 15.0,
) -> dict[str, Any]:
    """Validate SHA-256 bound geometric & semantic evidence for a mainline Bubble-Break frame (`H0..H3`)."""
    path = Path(image_path)
    if not path.is_file():
        return {
            "accepted": False,
            "status": "BLOCKED_RASTER_MISSING",
            "errors": [f"raster file does not exist: {path}"],
            "visual_acceptance_status": "NOT_VERIFIED_BY_CODE",
        }

    if not evidence or not isinstance(evidence, dict) or "raster_annotations" not in evidence:
        return {
            "accepted": False,
            "status": "BLOCKED_BUBBLE_BREAK_SEMANTIC_EVIDENCE_MISSING",
            "errors": [
                "Bubble-break frame lacks raster-bound geometric & semantic evidence; "
                "pixel gates alone cannot approve bubble contact or fracture causality."
            ],
            "visual_acceptance_status": "NOT_VERIFIED_BY_CODE",
        }

    digest = sha256_file(path)
    errors: list[str] = []
    if str(evidence.get("raster_sha256", "")).lower() != digest:
        errors.append("raster_sha256 does not match the exact bubble-break raster bytes")

    if not str(evidence.get("calibrated_from_dual_hammer_sha256", "")).strip():
        errors.append("missing calibrated_from_dual_hammer_sha256 provenance link from upstream T-hammer calibration")

    with Image.open(path) as im:
        width, height = im.size

    ann = evidence.get("raster_annotations", {})
    if (ann.get("image_width_px"), ann.get("image_height_px")) != (width, height):
        errors.append(f"annotation dimensions {(ann.get('image_width_px'), ann.get('image_height_px'))} != {(width, height)}")

    stage = str(evidence.get("stage", "")).upper()
    if stage not in BUBBLE_BREAK_STAGES:
        errors.append(f"unknown bubble-break stage: {stage!r}")

    # 1. Single attacking T-hammer rigid-body topology check
    if not evidence.get("single_attacking_t_hammer_only", False):
        errors.append("scene must contain exactly ONE attacking T-hammer and ONE containment bubble (not two hammers)")
    if evidence.get("has_forbidden_lower_handle_stub", False):
        errors.append("attacking T-hammer has a forbidden lower handle stub below the head (cross shape instead of T-hammer)")

    hammer = ann.get("attacking_hammer", {})
    try:
        head_axis = hammer["head_axis_px"]
        handle_axis = hammer["handle_axis_px"]
        face_center = hammer["strike_face_center_px"]
        face_radius = float(hammer["strike_face_radius_px"])
        hx = float(head_axis[1][0]) - float(head_axis[0][0])
        hy = float(head_axis[1][1]) - float(head_axis[0][1])
        gx = float(handle_axis[1][0]) - float(handle_axis[0][0])
        gy = float(handle_axis[1][1]) - float(handle_axis[0][1])
        head_len = math.hypot(hx, hy)
        handle_len = math.hypot(gx, gy)
        if head_len < 40.0 or handle_len < 40.0:
            errors.append("head_axis_px or handle_axis_px is implausibly short")
        else:
            cosine = abs((hx * gx + hy * gy) / (head_len * handle_len))
            if cosine > 0.35:
                errors.append(f"T-hammer handle is not orthogonal to head axis (|cos|={cosine:.3f} > 0.35)")
            mid_x = (float(head_axis[0][0]) + float(head_axis[1][0])) * 0.5
            mid_y = (float(head_axis[0][1]) + float(head_axis[1][1])) * 0.5
            joint_dist = min(
                math.hypot(mid_x - float(handle_axis[0][0]), mid_y - float(handle_axis[0][1])),
                math.hypot(mid_x - float(handle_axis[1][0]), mid_y - float(handle_axis[1][1])),
            )
            offset_ratio = joint_dist / max(head_len, 1.0)
            if offset_ratio > 0.25:
                errors.append(
                    f"T-hammer handle slid away from head midpoint into L-shape "
                    f"(joint_offset_ratio={offset_ratio:.3f} > 0.25)"
                )
    except (KeyError, TypeError, ValueError, IndexError) as exc:
        errors.append(f"invalid attacking_hammer geometry annotation: {exc}")
        face_center = [0.0, 0.0]
        face_radius = 1.0

    # 2. Bubble pole P & gap state check
    pole_p = ann.get("bubble_pole_p_px", [0.0, 0.0])
    pole_drift = math.hypot(float(pole_p[0]) - locked_pole_p_px[0], float(pole_p[1]) - locked_pole_p_px[1])
    if pole_drift > max_pole_drift_px:
        errors.append(
            f"bubble contact pole P={pole_p} drifted from locked P={list(locked_pole_p_px)} "
            f"(drift={pole_drift:.1f}px > {max_pole_drift_px:.1f}px)"
        )

    surface = str(evidence.get("contact_surface", "")).upper()
    gap = float(evidence.get("signed_gap", -1.0))

    if stage == "H0_PRE_IMPACT":
        if surface != "NONE" or gap < 0.08:
            errors.append(f"H0_PRE_IMPACT requires surface=NONE and gap >= 0.08 (got surface={surface}, gap={gap:.4f})")
    elif stage == "H1_PRE_NEAR":
        if surface != "NONE" or not (0.004 <= gap <= 0.06):
            errors.append(f"H1_PRE_NEAR requires surface=NONE and shrinking positive gap in [0.004, 0.06] (got surface={surface}, gap={gap:.4f})")
    elif stage in ("H2_FIRST_CONTACT", "H2B_CRACK_PROPAGATION", "H3_FOLLOWTHROUGH_SHELL_SHATTER"):
        if surface != "FLAT_END_FACE_TO_BUBBLE_POLE_P":
            errors.append(f"{stage} requires contact_surface=FLAT_END_FACE_TO_BUBBLE_POLE_P (got {surface})")
        if stage in ("H2_FIRST_CONTACT", "H2B_CRACK_PROPAGATION") and abs(gap) > 0.003:
            errors.append(f"{stage} requires zero gap within ±0.003 (got {gap:.4f})")
        face_to_p = math.hypot(float(face_center[0]) - float(pole_p[0]), float(face_center[1]) - float(pole_p[1]))
        if face_to_p > face_radius + 16.0:
            errors.append(f"{stage} strike face center {face_center} does not meet bubble pole P {pole_p} (dist={face_to_p:.1f}px)")
        crack_origin = ann.get("crack_origin_px")
        if not crack_origin or math.hypot(float(crack_origin[0]) - float(pole_p[0]), float(crack_origin[1]) - float(pole_p[1])) > 15.0:
            errors.append(f"{stage} radial cracks do not originate from locked contact point P={pole_p} (crack_origin={crack_origin})")
        if not evidence.get("cracks_originate_strictly_from_p", False):
            errors.append(f"{stage} must verify cracks_originate_strictly_from_p=True")

    # 3. Interior sanctuary & inhabitants unharmed check
    if not evidence.get("shell_only_breach", False) or not evidence.get("inhabitants_unharmed", False):
        errors.append("must verify shell_only_breach=True and inhabitants_unharmed=True")

    sanctuary_bbox = ann.get("sanctuary_bbox_xyxy_px", [830, 290, 1180, 520])
    pixel_metrics = measure_sanctuary_warmth_and_contact_luma(path, pole_p, sanctuary_bbox)
    if pixel_metrics["sanctuary_warmth_r_minus_b"] < 15.0:
        errors.append(
            f"interior sanctuary city lost warm illumination or was damaged "
            f"(warmth={pixel_metrics['sanctuary_warmth_r_minus_b']:.2f} < 15.0)"
        )
    if stage in ("H2_FIRST_CONTACT", "H2B_CRACK_PROPAGATION", "H3_FOLLOWTHROUGH_SHELL_SHATTER"):
        if pixel_metrics["contact_peak_luma_at_p"] < 220.0:
            errors.append(f"{stage} missing visible impact/fracture energy at P (peak_luma={pixel_metrics['contact_peak_luma_at_p']:.1f} < 220.0)")

    accepted = not errors
    return {
        "accepted": accepted,
        "status": "BUBBLE_BREAK_RASTER_EVIDENCE_PASS" if accepted else "BLOCKED_BUBBLE_BREAK_CONTRACT_FAIL",
        "stage": stage,
        "raster_path": str(path),
        "raster_sha256": digest,
        "raster_size_px": [width, height],
        "pole_drift_px": round(pole_drift, 2),
        "pixel_metrics": pixel_metrics,
        "errors": errors,
        "visual_acceptance_status": "NOT_VERIFIED_BY_CODE",
    }


def render_bubble_break_annotated_panel(
    image_path: Path,
    evidence: dict[str, Any],
    validation_result: dict[str, Any],
    out_path: Path,
) -> Path:
    """Draw the calibrated attacking T-hammer axes, bubble pole P, crack origin, and intact sanctuary box."""
    img = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(img)
    ann = evidence["raster_annotations"]
    h_info = ann["attacking_hammer"]

    draw.rectangle(h_info["head_bbox_xyxy_px"], outline=(80, 220, 255), width=3)
    draw.rectangle(h_info["handle_bbox_xyxy_px"], outline=(0, 255, 180), width=3)
    draw.line([tuple(h_info["head_axis_px"][0]), tuple(h_info["head_axis_px"][1])], fill=(80, 220, 255), width=4)
    draw.line([tuple(h_info["handle_axis_px"][0]), tuple(h_info["handle_axis_px"][1])], fill=(0, 255, 180), width=4)

    fc = h_info["strike_face_center_px"]
    fr = float(h_info["strike_face_radius_px"])
    draw.ellipse([fc[0] - fr, fc[1] - fr, fc[0] + fr, fc[1] + fr], outline=(255, 255, 100), width=3)

    px, py = ann["bubble_pole_p_px"]
    draw.ellipse([px - 11, py - 11, px + 11, py + 11], fill=(255, 55, 55), outline=(255, 255, 255), width=2)
    draw.text((px + 14, py - 22), f"P=({int(px)},{int(py)})", fill=(255, 240, 120))

    s_box = ann["sanctuary_bbox_xyxy_px"]
    draw.rectangle(s_box, outline=(255, 200, 70), width=3)
    draw.text((s_box[0] + 8, s_box[1] - 22), "INTACT SANCTUARY & INHABITANTS", fill=(255, 215, 90))

    ok = validation_result["accepted"]
    banner = (
        f"{evidence['stage']} | gap={evidence['signed_gap']:+.4f} | {validation_result['status']} | "
        f"warmth={validation_result['pixel_metrics']['sanctuary_warmth_r_minus_b']:+.1f} | "
        f"CODE_VISUAL={validation_result['visual_acceptance_status']}"
    )
    draw.rectangle([12, 12, 1260, 48], fill=(10, 14, 20))
    draw.text((20, 22), banner, fill=(130, 250, 175) if ok else (255, 95, 95))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, quality=93)
    return out_path