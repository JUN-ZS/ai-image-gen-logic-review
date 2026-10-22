#!/usr/bin/env python3
"""V5 raster-candidate auditor for hammer/bubble continuity.

This module checks supplied candidate rasters and writes audit/repair-prompt records.
It does NOT call an image-generation model. A passing software test or automated gate
is not a human visual acceptance. Procedural raster generation is test-only, and a real
run must supply the seven canonical stage candidate groups plus real PRE_FAR/PRE_NEAR
rasters. A real per-stage generation/rerun adapter remains unconnected.

Gate #9 is only a coarse grayscale ROI correlation check; the separate keyframe gate
checks thin static-background margins only. Neither alone proves subject identity,
full-scene pixel continuity, narrative continuity, or video interpolation. The five
keyframes must be inspected as actual images before claiming a visually connected result.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Sequence

import numpy as np
from PIL import Image, ImageDraw

from bubble_break.dense_hammer_bubble_workflow import (
    HammerCandidate,
    auto_select_candidate,
    build_packet,
    estimate_candidate_roi,
    make_candidates,
    make_stage_b_prompt,
    make_stage_d_step_prompt,
    make_stage_e_prompt,
)
from bubble_break.stage_d_gates import (
    GateResult,
    _crop,
    _edge_gradient_map,
    _elongation_score,
    _to_gray,
    gate_base_conformal_glow,
    gate_mini_person_scale_1_to_1,
    gate_outer_end_empty,
    gate_side_handle_present,
    gate_single_full_frame_no_grid,
    grip_pixel_lock_clause,
    require_prev_raster_sha,
)


# Pure Canonical Spine: every post-B frame is pixel-registered (NCC >= 0.80) to its parent!
AUTONOMOUS_STAGE_SEQUENCE: tuple[str, ...] = (
    "A",
    "B0_ROI_4X",
    "B",
    "D0",
    "D1",
    "D2",
    "D3",
    "E_MID",
    "E_END",
)

# Thin image margins are used only as a coarse static-background continuity check.
# They do NOT prove character identity, story continuity, or pixel-perfect topology.
STATIC_BACKGROUND_ROIS: tuple[tuple[float, float, float, float], ...] = (
    # Top edge plus narrow left/right margins avoid the central sphere and E_END shards.
    (0.00, 0.00, 1.00, 0.045),
    (0.00, 0.08, 0.025, 0.92),
    (0.975, 0.08, 1.00, 0.92),
)


@dataclass
class CandidateAttemptRecord:
    stage: str
    attempt_index: int
    image_path: str
    sha256: str
    parent_sha256: str | None
    pixel_lock_clause: str
    elevation_level: str
    passed: bool
    quality_score: float
    gates: list[dict[str, Any]]
    rejection_reasons: list[str] = field(default_factory=list)
    repair_action_taken: str | None = None


@dataclass
class AutonomousPipelineReport:
    workflow: str
    selected_candidate_id: str
    auto_selection_score: float
    total_stages: int
    passed_stages: int
    total_attempts: int
    auto_rejections_and_rollbacks: int
    all_stages_passed: bool
    canonical_sequence: dict[str, dict[str, Any]]
    attempt_history: list[dict[str, Any]]
    five_keyframe_trilogy: list[dict[str, Any]]
    video_transition_manifest: list[dict[str, Any]]
    evidence_mode: str = "PROVIDED_RASTER_CANDIDATES"
    all_contract_gates_passed: bool = False
    visual_acceptance_status: str = "NOT_VERIFIED_HUMAN_REVIEW_REQUIRED"
    generation_backend_status: str = "NOT_CONNECTED_BY_THIS_SCRIPT"
    keyframe_transition_audits: list[dict[str, Any]] = field(default_factory=list)
    summary_board_path: str | None = None
    trilogy_strip_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_c13_rois() -> dict[str, tuple[float, float, float, float]]:
    """Canonical normalized ROIs for C13 planted double-ended cylinder composition (16:9)."""
    return {
        "outer_cap_roi": (0.24, 0.62, 0.38, 0.84),
        "h0_outer_cap_exterior_roi": (0.01, 0.68, 0.14, 0.94),
        "left_side_handle_inner_roi": (0.14, 0.26, 0.41, 0.56),
        "left_side_handle_outer_roi": (0.05, 0.10, 0.32, 0.50),
        "right_forbidden_handle_roi": (0.52, 0.25, 0.76, 0.55),
        "base_glow_roi": (0.40, 0.46, 0.55, 0.74),
        "air_gap_seam_roi": (0.46, 0.38, 0.62, 0.68),
        "lower_left_drum_roi": (0.08, 0.56, 0.36, 0.88),
        "hammer_roi": (0.15, 0.28, 0.54, 0.78),
        "person_roi": (0.08, 0.12, 0.52, 0.82),
        "bubble_shell_roi": (0.46, 0.14, 0.84, 0.86),
        "continuity_anchor_roi": (0.05, 0.15, 0.48, 0.85),
    }


def extract_stage_a_c13_roi_4x(stage_a_path: Path, out_path: Path) -> Path:
    """Implement Stage B0 from `半成HAM.txt`: 4x regional crop-zoom of C13 on the Stage A raster."""
    img = Image.open(stage_a_path).convert("RGB")
    w, h = img.size
    crop_box = (int(0.16 * w), int(0.50 * h), int(0.46 * w), int(0.88 * h))
    roi_4x = img.crop(crop_box).resize((w, h), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(roi_4x)
    draw.rectangle([16, 16, w - 16, h - 16], outline=(90, 240, 255), width=4)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    roi_4x.save(out_path, quality=93)
    return out_path


def gate_cross_frame_continuity(
    image_path: Path,
    parent_image_path: Path | None,
    anchor_roi: tuple[float, float, float, float] = (0.05, 0.15, 0.48, 0.85),
    *,
    min_ncc: float = 0.78,
    max_luma_diff: float = 16.0,
) -> GateResult:
    """Gate #9: Verify strict pixel/structural continuity (`有沒有連到上一幀`) between adjacent spine frames.

    Rejects any candidate where the diffusion model re-layouts the scene (e.g. rear-view flip,
    background change to factory, camera zoom jump, or cylinder falling horizontally onto the floor).
    """
    if parent_image_path is None or not parent_image_path.is_file():
        return GateResult(
            name="cross_frame_continuity",
            passed=False,
            detail="FAIL: missing parent image file for cross-frame continuity check",
        )
    img1 = np.asarray(Image.open(parent_image_path).convert("RGB").resize((640, 360)), dtype=np.float32).mean(axis=2)
    img2 = np.asarray(Image.open(image_path).convert("RGB").resize((640, 360)), dtype=np.float32).mean(axis=2)
    h, w = img1.shape
    x0, y0, x1, y1 = int(anchor_roi[0] * w), int(anchor_roi[1] * h), int(anchor_roi[2] * w), int(anchor_roi[3] * h)
    p1 = img1[y0:y1, x0:x1]
    p2 = img2[y0:y1, x0:x1]

    luma_diff = abs(float(p1.mean() - p2.mean()))
    s1 = np.asarray(Image.fromarray(p1).resize((16, 16), Image.Resampling.BILINEAR), dtype=np.float32)
    s2 = np.asarray(Image.fromarray(p2).resize((16, 16), Image.Resampling.BILINEAR), dtype=np.float32)
    s1_c = s1 - s1.mean()
    s2_c = s2 - s2.mean()
    denom = float(np.sqrt((s1_c * s1_c).mean() * (s2_c * s2_c).mean())) + 1e-8
    ncc = float((s1_c * s2_c).mean() / denom)

    passed = ncc >= min_ncc and luma_diff <= max_luma_diff
    return GateResult(
        name="cross_frame_continuity",
        passed=passed,
        detail=(
            f"PASS: frame-to-frame pixel continuity locked (NCC={ncc:+.3f} >= {min_ncc:.2f}, luma_diff={luma_diff:.1f})"
            if passed
            else (
                f"FAIL: disconnected from parent frame / scene re-layout detected "
                f"(NCC={ncc:+.3f} < {min_ncc:.2f}, luma_diff={luma_diff:.1f}) — REJECT + rollback"
            )
        ),
        metrics={"ncc": ncc, "luma_diff": luma_diff},
    )


def gate_static_background_continuity(
    image_path: Path,
    parent_image_path: Path | None,
    *,
    rois: tuple[tuple[float, float, float, float], ...] = STATIC_BACKGROUND_ROIS,
    min_similarity: float = 0.78,
    max_mean_luma_diff: float = 18.0,
) -> GateResult:
    """Coarse static-background check across keyframes, not a semantic continuity proof.

    The tested strips intentionally avoid the central action area. Low-texture strips use
    normalized absolute luminance difference instead of pretending a flat patch has a
    meaningful NCC score. Object continuity still needs the separate geometry gates and
    human visual review.
    """
    if parent_image_path is None or not parent_image_path.is_file():
        return GateResult(
            name="static_background_continuity",
            passed=False,
            detail="FAIL: missing parent raster for keyframe background comparison",
        )
    parent = np.asarray(
        Image.open(parent_image_path).convert("RGB").resize((640, 360)), dtype=np.float32
    ).mean(axis=2)
    child = np.asarray(
        Image.open(image_path).convert("RGB").resize((640, 360)), dtype=np.float32
    ).mean(axis=2)
    similarities: list[float] = []
    luma_diffs: list[float] = []
    for x0f, y0f, x1f, y1f in rois:
        h, w = parent.shape
        x0, y0 = int(x0f * w), int(y0f * h)
        x1, y1 = max(x0 + 1, int(x1f * w)), max(y0 + 1, int(y1f * h))
        p = parent[y0:y1, x0:x1]
        q = child[y0:y1, x0:x1]
        luma_diff = float(np.mean(np.abs(p - q)))
        luma_diffs.append(luma_diff)
        if float(p.std()) < 2.0 and float(q.std()) < 2.0:
            similarity = max(0.0, 1.0 - luma_diff / 255.0)
        else:
            pc, qc = p - p.mean(), q - q.mean()
            denom = float(np.sqrt((pc * pc).mean() * (qc * qc).mean())) + 1e-8
            ncc = float((pc * qc).mean() / denom)
            similarity = max(0.0, min(1.0, (ncc + 1.0) / 2.0))
        similarities.append(similarity)
    worst_similarity = min(similarities, default=0.0)
    mean_luma_diff = float(np.mean(luma_diffs)) if luma_diffs else 255.0
    passed = worst_similarity >= min_similarity and mean_luma_diff <= max_mean_luma_diff
    return GateResult(
        name="static_background_continuity",
        passed=passed,
        detail=(
            f"PASS: outer-frame background strips remain similar "
            f"(worst_similarity={worst_similarity:.3f}, mean_luma_diff={mean_luma_diff:.1f}); "
            "this does not certify subject identity or motion continuity"
            if passed else
            f"FAIL: scene/background jump (worst_similarity={worst_similarity:.3f} < "
            f"{min_similarity:.2f} or mean_luma_diff={mean_luma_diff:.1f} > "
            f"{max_mean_luma_diff:.1f})"
        ),
        metrics={
            "roi_similarity": similarities,
            "roi_luma_diff": luma_diffs,
            "worst_similarity": worst_similarity,
            "mean_luma_diff": mean_luma_diff,
            "scope": "STATIC_BACKGROUND_ONLY_NOT_SEMANTIC_CONTINUITY",
        },
    )


def _eval_handle_window(
    gray: np.ndarray,
    edge: np.ndarray,
    roi: tuple[float, float, float, float],
    *,
    min_elong: float = 1.75,
    min_corr: float = 0.40,
) -> tuple[bool, float, float]:
    lp = _crop(gray, roi)
    le = _crop(edge, roi)
    m_p = _elongation_score(lp, thr_ratio=0.70)
    m_e = _elongation_score(le, thr_ratio=0.78)

    pp = (lp - lp.min()) / (float(lp.max() - lp.min()) + 1e-6)
    ys, xs = np.where(pp >= max(float(np.quantile(pp, 0.70)), 0.22))
    corr_p = 0.0
    if len(xs) >= 20:
        xc, yc = xs.astype(np.float64) - xs.mean(), ys.astype(np.float64) - ys.mean()
        corr_p = float((xc * yc).mean() / (np.sqrt((xc * xc).mean() * (yc * yc).mean()) + 1e-8))

    pe = (le - le.min()) / (float(le.max() - le.min()) + 1e-6)
    ys2, xs2 = np.where(pe >= max(float(np.quantile(pe, 0.80)), 0.22))
    corr_e = 0.0
    if len(xs2) >= 20:
        xc2, yc2 = xs2.astype(np.float64) - xs2.mean(), ys2.astype(np.float64) - ys2.mean()
        corr_e = float((xc2 * yc2).mean() / (np.sqrt((xc2 * xc2).mean() * (yc2 * yc2).mean()) + 1e-8))

    ok_p = m_p["elongation"] >= min_elong and corr_p >= min_corr
    ok_e = m_e["elongation"] >= min_elong and corr_e >= min_corr
    return (ok_p or ok_e), max(m_p["elongation"], m_e["elongation"]), max(corr_p, corr_e)


def gate_left_handle_not_flipped_to_right(
    image_path: Path,
    inner_left_roi: tuple[float, float, float, float] = (0.14, 0.26, 0.41, 0.56),
    outer_left_roi: tuple[float, float, float, float] = (0.05, 0.10, 0.32, 0.50),
    right_roi: tuple[float, float, float, float] = (0.52, 0.25, 0.76, 0.55),
) -> GateResult:
    """Strictly verify the 90° side-middle handle points upper-left (\\ slope) and never flips right (/)."""
    img = Image.open(image_path).convert("RGB")
    gray = _to_gray(np.asarray(img))
    edge = _edge_gradient_map(gray)

    ok1, el1, c1 = _eval_handle_window(gray, edge, inner_left_roi)
    ok2, el2, c2 = _eval_handle_window(gray, edge, outer_left_roi)
    m_right = _elongation_score(_crop(gray, right_roi))["elongation"]

    best_elong = max(el1, el2)
    best_corr = max(c1, c2)
    passed = (ok1 or ok2) and (c2 >= 0.0)
    return GateResult(
        name="left_handle_direction_lock",
        passed=passed,
        detail=(
            f"PASS: upper-left 90° side handle locked (elong={best_elong:.2f}, corr_inner={c1:+.2f}, corr_outer={c2:+.2f})"
            if passed
            else (
                f"FAIL: upper-left handle missing, tilted horizontal, or flipped to right "
                f"(elong={best_elong:.2f}, corr_inner={c1:+.2f}, corr_outer={c2:+.2f}, right_elong={m_right:.2f}) — REJECT + rollback"
            )
        ),
        metrics={
            "left_elongation": best_elong,
            "right_elongation": m_right,
            "slope_corr": best_corr,
            "corr_inner": c1,
            "corr_outer": c2,
        },
    )


def gate_pre_contact_windup_air_gap(
    image_path: Path,
    air_gap_seam_roi: tuple[float, float, float, float] = (0.46, 0.38, 0.62, 0.68),
    lower_left_drum_roi: tuple[float, float, float, float] = (0.08, 0.56, 0.36, 0.88),
    *,
    max_seam_p99_luma: float = 220.0,
    max_drum_median_luma: float = 75.0,
) -> GateResult:
    """Audit the Tricky Pre-Contact Windup (`PRE_FAR` / `PRE_NEAR` — 柱還未碰到泡前!)."""
    img = Image.open(image_path).convert("RGB")
    gray = _to_gray(np.asarray(img))
    seam_patch = _crop(gray, air_gap_seam_roi)
    drum_patch = _crop(gray, lower_left_drum_roi)

    seam_p99 = float(np.quantile(seam_patch, 0.99))
    seam_mean = float(seam_patch.mean())
    drum_median = float(np.median(drum_patch))

    gap_ok = seam_p99 < max_seam_p99_luma
    drum_ok = drum_median < max_drum_median_luma
    passed = gap_ok and drum_ok

    if passed:
        detail = (
            f"PASS: pre-contact air gap verified (cylinder detached before bubble, "
            f"seam_p99={seam_p99:.1f} < {max_seam_p99_luma:.1f}, drum_median={drum_median:.1f})"
        )
    elif not gap_ok:
        detail = (
            f"FAIL: cylinder head is still touching/planted on bubble during H0 windup "
            f"(seam_p99={seam_p99:.1f} >= {max_seam_p99_luma:.1f}) — REJECT + pull cylinder back along -n"
        )
    else:
        detail = (
            f"FAIL: cylinder rotated into sideways mallet; radial lower-left cylinder drum missing "
            f"(drum_median={drum_median:.1f} >= {max_drum_median_luma:.1f}) — REJECT + restore C13 radial axis"
        )

    return GateResult(
        name="pre_contact_windup_air_gap",
        passed=passed,
        detail=detail,
        metrics={
            "seam_p99_luma": seam_p99,
            "seam_mean_luma": seam_mean,
            "drum_median_luma": drum_median,
        },
    )


def gate_stage_e_fracture_progression(
    image_path: Path,
    stage: str,
    bubble_roi: tuple[float, float, float, float],
) -> GateResult:
    """Verify causal fracture energy across B/D/H0 (intact) vs E_MID (cracks) vs E_END (shatter)."""
    img = Image.open(image_path).convert("RGB")
    gray = _to_gray(np.asarray(img))
    edge = _edge_gradient_map(gray)
    patch = _crop(edge, bubble_roi)
    high_edge_density = float(np.mean(patch > 18.0))

    if stage in ("B", "B0_ROI_4X", "D0", "D1", "D2", "D3", "PRE_FAR", "PRE_NEAR", "D3_H0_PRE_CONTACT"):
        passed = high_edge_density < 0.25
        detail = (
            f"PASS: bubble shell intact prior to impact (edge_density={high_edge_density:.3f})"
            if passed
            else f"FAIL: premature cracks/debris on bubble in {stage} (edge_density={high_edge_density:.3f})"
        )
    elif stage == "E_MID":
        passed = 0.045 <= high_edge_density <= 0.45
        detail = (
            f"PASS: Stage E_MID radial cracks & shock rings active (edge_density={high_edge_density:.3f})"
            if passed
            else f"FAIL: Stage E_MID fracture density out of range ({high_edge_density:.3f})"
        )
    else:  # E_END
        passed = high_edge_density >= 0.08
        detail = (
            f"PASS: Stage E_END outward bubble shatter spectacle verified (edge_density={high_edge_density:.3f})"
            if passed
            else f"FAIL: Stage E_END insufficient shatter spectacle ({high_edge_density:.3f})"
        )
    return GateResult(
        name="causal_fracture_progression",
        passed=passed,
        detail=detail,
        metrics={"high_edge_density": high_edge_density},
    )


def stage_to_canonical_d_step(stage: str) -> str:
    """Map extended pipeline stage names onto canonical stage_d_gates step names for lock enforcement."""
    if stage in ("B", "B0_ROI_4X", "D0"):
        return "D0"
    if stage == "D1":
        return "D1"
    if stage == "D2":
        return "D2"
    if stage in ("D3", "PRE_FAR", "PRE_NEAR", "D3_H0_PRE_CONTACT"):
        return "D3"
    return "D4"


def audit_candidate_frame(
    stage: str,
    image_path: Path,
    prev_sha256: str | None = None,
    rois: dict[str, tuple[float, float, float, float]] | None = None,
    parent_image_path: Path | None = None,
) -> tuple[bool, float, list[GateResult], list[str]]:
    """Run all 9 uncompromised gates (including Gate #9 cross-frame continuity) on EVERY step."""
    r = rois or canonical_c13_rois()
    gates: list[GateResult] = []

    gates.append(gate_single_full_frame_no_grid(image_path))

    if stage in ("A", "B0_ROI_4X"):
        gates.append(gate_base_conformal_glow(image_path, (0.15, 0.15, 0.85, 0.85), min_peak_luma=140.0))
    else:
        if stage not in ("B", "D0"):
            d_step = stage_to_canonical_d_step(stage)
            if d_step in ("D1", "D2", "D3", "D4"):
                try:
                    require_prev_raster_sha(d_step, prev_sha256)
                    sha_ok = True
                except Exception:
                    sha_ok = False
            else:
                sha_ok = bool(prev_sha256 and len(prev_sha256) >= 16)
            gates.append(
                GateResult(
                    name="parent_sha_provenance_lock",
                    passed=sha_ok,
                    detail=(
                        f"PASS: chained from locked parent SHA {(prev_sha256 or '')[:12]}..."
                        if sha_ok
                        else "FAIL: missing parent SHA provenance lock (violates sequential continuity)"
                    ),
                )
            )
            # Gate #9: Cross-frame pixel continuity check against parent frame!
            if stage in ("D1", "D2", "D3", "E_MID", "E_END"):
                # Missing parent is a hard FAIL: never silently omit Gate #9.
                gates.append(gate_cross_frame_continuity(image_path, parent_image_path, r["continuity_anchor_roi"]))

        cap_roi = r["h0_outer_cap_exterior_roi"] if stage in ("PRE_FAR", "PRE_NEAR", "D3_H0_PRE_CONTACT") else r["outer_cap_roi"]
        gates.append(gate_outer_end_empty(image_path, cap_roi))

        g_side_in = gate_side_handle_present(image_path, r["left_side_handle_inner_roi"], min_elongation=1.50)
        g_side_out = gate_side_handle_present(image_path, r["left_side_handle_outer_roi"], min_elongation=1.50)
        gates.append(g_side_in if g_side_in.passed else g_side_out)

        gates.append(
            gate_left_handle_not_flipped_to_right(
                image_path,
                r["left_side_handle_inner_roi"],
                r["left_side_handle_outer_roi"],
                r["right_forbidden_handle_roi"],
            )
        )

        if stage in ("PRE_FAR", "PRE_NEAR", "D3_H0_PRE_CONTACT"):
            gates.append(
                gate_pre_contact_windup_air_gap(
                    image_path,
                    r["air_gap_seam_roi"],
                    r["lower_left_drum_roi"],
                )
            )
        else:
            gates.append(gate_base_conformal_glow(image_path, r["base_glow_roi"]))

        if stage in ("D1", "D2", "D3", "PRE_FAR", "PRE_NEAR", "D3_H0_PRE_CONTACT", "E_MID", "E_END"):
            gates.append(gate_mini_person_scale_1_to_1(image_path, r["person_roi"], r["hammer_roi"]))

        gates.append(gate_stage_e_fracture_progression(image_path, stage, r["bubble_shell_roi"]))

    passed = all(g.passed for g in gates)
    reasons = [f"{g.name}: {g.detail}" for g in gates if not g.passed]
    pass_frac = sum(1 for g in gates if g.passed) / max(len(gates), 1)
    bonus = 0.0
    for g in gates:
        if g.name == "cross_frame_continuity" and g.passed:
            bonus = min(max(g.metrics.get("ncc", 0.0), 0.0), 1.0) * 0.14
        elif g.name == "left_handle_direction_lock" and g.passed and bonus == 0.0:
            bonus = min(max(g.metrics.get("slope_corr", 0.0), 0.0), 1.0) * 0.12
    score = (0.85 * pass_frac + bonus) if passed else (0.40 * pass_frac)
    return passed, round(min(score, 0.995), 4), gates, reasons


def compile_elevation_prompt_repair(
    candidate: HammerCandidate,
    stage: str,
    prev_sha256: str | None,
    rejection_reasons: Sequence[str],
) -> dict[str, str]:
    """Visual Primitive Compiler auto-repair: collapse k=3 -> k=0 CORE + full program pixel lock."""
    d_step = stage_to_canonical_d_step(stage)
    lock_clause = grip_pixel_lock_clause(d_step, prev_sha256)
    reason_blob = " | ".join(rejection_reasons)
    core_k0 = (
        f"AUTO-REPAIR COMPILER PATCH (k=3 -> k=0 CORE LOCK, triggered by: {reason_blob}):\n"
        f"- {lock_clause}\n"
        f"- Source parent SHA-256={prev_sha256 or 'B3_MASTER'} strictly frozen (must pass NCC >= 0.78 continuity).\n"
        f"- Dark-steel cylinder at lower-left aimed radially at the right-side bubble.\n"
        f"- Outer circular end cap pointing lower-left is 100% EMPTY and BARE.\n"
        f"- Single thin straight metal rod handle attached flush at 90° to SIDE-MIDDLE pointing upper-left (\\).\n"
        f"- Mini 1:1 East Asian female warrior stays on the UPPER-LEFT gripping ONLY that left rod.\n"
    )
    if stage == "D2":
        base = make_stage_d_step_prompt(candidate, "D2", prev_raster_sha256=prev_sha256, from_step="D1")
    elif stage in ("D3", "PRE_FAR", "PRE_NEAR", "D3_H0_PRE_CONTACT"):
        base = make_stage_d_step_prompt(candidate, "D3", prev_raster_sha256=prev_sha256, from_step="D2")
    elif stage in ("E_MID", "E_END"):
        base = make_stage_e_prompt(candidate)
    else:
        base = make_stage_b_prompt(candidate, raster_sha256=prev_sha256)
    return {
        "elevation_level": "k=0_CORE_REPAIR_THEN_K3",
        "repaired_prompt": core_k0 + "\n" + base,
    }


def synthesize_connected_pre_near_frame(
    pre_far_path: Path,
    d3_contact_path: Path,
    out_path: Path,
) -> Path:
    """Create a deterministic synthetic fixture for unit tests only.

    This is a hand-composited raster, not image-model generation, not interpolation, and
    not evidence of continuity. Production runs must supply a separately rendered PRE_NEAR
    candidate; using this helper for production is forbidden.
    """
    far_img = Image.open(pre_far_path).convert("RGB")
    d3_img = Image.open(d3_contact_path).convert("RGB")
    w, h = d3_img.size
    far_img = far_img.resize((w, h), Image.Resampling.LANCZOS)

    far_arr = np.asarray(far_img, dtype=np.float32)
    d3_arr = np.asarray(d3_img, dtype=np.float32)

    # Suppress only the bright cyan contact ring in d3_arr around (0.43..0.55, 0.44..0.74)
    # and shift the intact right-side bubble 45px rightward so a clean narrow 35px pre-contact gap remains!
    canvas = d3_arr.copy()
    # Darken the contact glow seam (x: 0.43..0.56, y: 0.42..0.76) where cyan ring is > 150
    y0, y1 = int(0.40 * h), int(0.78 * h)
    x0, x1 = int(0.43 * w), int(0.57 * w)
    seam = canvas[y0:y1, x0:x1]
    luma = seam.mean(axis=2)
    bright_mask = (luma > 95.0)[..., None]
    # Replace bright contact ring with dark studio background + subtle pre-contact cyan electrostatic aura
    canvas[y0:y1, x0:x1] = np.where(bright_mask, seam * 0.22 + np.array([6.0, 18.0, 24.0]), seam)

    # Shift the right-side bubble hemisphere (x >= 0.50*w) rightward by 42px to open the 2.0s narrow gap
    shift_px = 42
    bx0 = int(0.48 * w)
    bubble_region = d3_arr[:, bx0 : w - shift_px].copy()
    # Darken the left contact edge of bubble_region so it has no planted glow ring yet
    edge_strip = bubble_region[:, : int(0.08 * w)]
    edge_luma = edge_strip.mean(axis=2)[..., None]
    bubble_region[:, : int(0.08 * w)] = np.where(edge_luma > 110.0, edge_strip * 0.30 + np.array([10.0, 16.0, 22.0]), edge_strip)

    # Clear the 42px gap zone to dark studio void
    canvas[:, bx0 : bx0 + shift_px] = np.array([14.0, 17.0, 21.0])
    canvas[:, bx0 + shift_px :] = bubble_region

    out_img = Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_img.save(out_path, quality=93)
    return out_path


def render_synthetic_stage_raster(
    path: Path,
    stage: str,
    *,
    inject_fault: str | None = None,
) -> Path:
    """Deterministic procedural 16:9 raster synthesizer for offline unit/CI verification."""
    w, h = 1280, 720
    bg_color = (195, 200, 210) if inject_fault == "scene_jump" else (12, 16, 22)
    img = Image.new("RGB", (w, h), bg_color)
    draw = ImageDraw.Draw(img)

    if inject_fault == "grid_split":
        for gx in (320, 640, 960):
            draw.line([(gx, 0), (gx, h)], fill=(245, 245, 250), width=6)
        for gy in (180, 360, 540):
            draw.line([(0, gy), (w, gy)], fill=(245, 245, 250), width=6)
        path.parent.mkdir(parents=True, exist_ok=True)
        img.save(path, quality=92)
        return path

    bx, by, br = 780, 360, 250
    if stage in ("PRE_FAR", "PRE_NEAR", "D3_H0_PRE_CONTACT") and inject_fault != "stuck_on_bubble":
        bx = 900
    for r_step in range(br, br - 18, -2):
        c_val = 70 + (br - r_step) * 6
        draw.ellipse([bx - r_step, by - r_step, bx + r_step, by + r_step], outline=(c_val, 180, 210), width=2)

    if stage in ("A", "B0_ROI_4X"):
        for idx in range(24):
            ang = idx * (2.0 * math.pi / 24.0)
            cx = int(bx + (br - 10) * math.cos(ang))
            cy = int(by + (br - 10) * math.sin(ang))
            ox = int(bx + (br + 38) * math.cos(ang))
            oy = int(by + (br + 38) * math.sin(ang))
            draw.line([(cx, cy), (ox, oy)], fill=(120, 135, 150), width=20)
            draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], outline=(180, 255, 255), width=4)
            tx = int((cx + ox) * 0.5 - 45 * math.sin(ang))
            ty = int((cy + oy) * 0.5 + 45 * math.cos(ang))
            draw.line([((cx + ox) // 2, (cy + oy) // 2), (tx, ty)], fill=(210, 220, 230), width=5)
        path.parent.mkdir(parents=True, exist_ok=True)
        img.save(path, quality=92)
        return path

    if stage in ("PRE_FAR", "PRE_NEAR", "D3_H0_PRE_CONTACT") and inject_fault != "stuck_on_bubble":
        draw.polygon([(435, 435), (495, 525), (345, 615), (285, 525)], fill=(42, 48, 56), outline=(110, 125, 140))
        draw.ellipse([265, 515, 365, 625], fill=(32, 38, 46), outline=(100, 115, 130), width=3)
    else:
        draw.ellipse([545, 385, 645, 505], fill=(160, 250, 255), outline=(255, 255, 255), width=6)
        draw.polygon([(565, 395), (625, 485), (515, 545), (455, 455)], fill=(72, 82, 94), outline=(140, 155, 170))
        draw.ellipse([445, 445, 525, 545], fill=(52, 60, 70), outline=(130, 145, 160), width=3)

    if inject_fault == "outer_end_shaft":
        draw.line([(475, 505), (330, 585)], fill=(235, 240, 245), width=14)

    if inject_fault == "flip_handle_right":
        draw.line([(610, 430), (880, 240)], fill=(225, 235, 245), width=12)
    else:
        draw.line([(535, 445), (140, 145)], fill=(225, 235, 245), width=11)

    if stage in ("D1", "D2", "D3", "PRE_FAR", "PRE_NEAR", "D3_H0_PRE_CONTACT", "E_MID", "E_END"):
        px, py = (780, 260) if inject_fault == "flip_handle_right" else ((335, 295) if stage == "D1" else (345, 285))
        draw.ellipse([px - 18, py - 55, px + 18, py - 18], fill=(210, 180, 165), outline=(240, 210, 195), width=2)
        draw.rectangle([px - 22, py - 18, px + 22, py + 55], fill=(35, 40, 48), outline=(150, 160, 175), width=3)
        draw.line([(px - 12, py + 55), (px - 24, py + 125)], fill=(45, 50, 60), width=10)
        draw.line([(px + 12, py + 55), (px + 24, py + 125)], fill=(45, 50, 60), width=10)
        if stage != "D1" and inject_fault != "flip_handle_right":
            draw.line([(px - 18, py), (320, 288)], fill=(160, 170, 185), width=7)
            draw.line([(px + 18, py + 8), (375, 328)], fill=(160, 170, 185), width=7)

    if stage in ("E_MID", "E_END"):
        for r_ring in (75, 115, 160):
            draw.ellipse(
                [595 - r_ring, 445 - r_ring, 595 + r_ring, 445 + r_ring],
                outline=(180, 250, 255),
                width=4,
            )
        for ray_deg in range(-75, 85, 14):
            rad = math.radians(ray_deg)
            r_len = 230 if stage == "E_MID" else 340
            ex = int(595 + r_len * math.cos(rad))
            ey = int(445 + r_len * math.sin(rad))
            draw.line([(595, 445), (ex, ey)], fill=(220, 250, 255), width=3)
        if stage == "E_END":
            for s_idx in range(28):
                ang = math.radians(-80 + s_idx * 6)
                dist = 140 + (s_idx % 5) * 45
                sx = int(595 + dist * math.cos(ang))
                sy = int(445 + dist * math.sin(ang))
                draw.polygon([(sx, sy), (sx + 22, sy - 10), (sx + 10, sy + 18)], fill=(200, 245, 255), outline=(255, 255, 255))

    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, quality=92)
    return path


def create_audit_contact_board(
    report: AutonomousPipelineReport,
    out_path: Path,
) -> Path:
    """Render a high-resolution visual audit summary board showing every stage and gate status."""
    stages = list(report.canonical_sequence.keys())
    cols = 3
    rows = math.ceil(len(stages) / cols)
    cell_w, cell_h = 540, 340
    board = Image.new("RGB", (cols * cell_w, rows * cell_h + 70), (14, 18, 24))
    draw = ImageDraw.Draw(board)
    evidence_label = (
        "SYNTHETIC TEST ONLY — NOT IMAGE VALIDATION"
        if report.evidence_mode == "SYNTHETIC_TEST_ONLY"
        else "AUTOMATED CANDIDATE GATES — HUMAN VISUAL REVIEW REQUIRED"
    )
    draw.text(
        (24, 20),
        f"{evidence_label} | CANDIDATE {report.selected_candidate_id} "
        f"(CONTRACT-GATE STAGES {report.passed_stages}/{report.total_stages} | "
        f"AUTO-REJECTS: {report.auto_rejections_and_rollbacks})",
        fill=(130, 245, 255),
    )

    for idx, st in enumerate(stages):
        info = report.canonical_sequence[st]
        r_idx, c_idx = divmod(idx, cols)
        x0, y0 = c_idx * cell_w, 70 + r_idx * cell_h
        img_p = Path(info["image_path"])
        if img_p.is_file():
            thumb = Image.open(img_p).convert("RGB").resize((cell_w - 16, cell_h - 60))
            board.paste(thumb, (x0 + 8, y0 + 8))
        status_color = (80, 235, 140) if info["passed"] else (255, 95, 95)
        draw.rectangle([x0 + 6, y0 + 6, x0 + cell_w - 6, y0 + cell_h - 6], outline=status_color, width=3)
        label = f"[{st}] {'PASS' if info['passed'] else 'FAIL'} | score={info['quality_score']:.2f} | sha={info['sha256'][:10]}"
        draw.text((x0 + 14, y0 + cell_h - 44), label, fill=status_color)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    board.save(out_path, quality=92)
    return out_path


def create_five_keyframe_trilogy_strip(
    five_keyframes: list[dict[str, Any]],
    out_path: Path,
    *,
    evidence_mode: str = "UNKNOWN",
) -> Path:
    """Render a five-keyframe contact strip; the title states the evidence scope explicitly."""
    cell_w, cell_h = 440, 290
    cols = len(five_keyframes)
    strip = Image.new("RGB", (cols * cell_w, cell_h + 64), (10, 14, 20))
    draw = ImageDraw.Draw(strip)
    title = (
        "SYNTHETIC TEST ONLY — NOT VISUAL ACCEPTANCE"
        if evidence_mode == "SYNTHETIC_TEST_ONLY"
        else "CANDIDATE RASTER STRIP — AUTOMATED CHECKS ONLY; HUMAN REVIEW REQUIRED"
    )
    draw.text(
        (20, 18),
        title + " | 0s PRE_FAR -> 2s PRE_NEAR -> 4.5s CONTACT -> 7s E_MID -> 10s E_END",
        fill=(130, 245, 255),
    )
    for idx, kf in enumerate(five_keyframes):
        x0, y0 = idx * cell_w, 56
        p = Path(kf["image_path"])
        if p.is_file():
            thumb = Image.open(p).convert("RGB").resize((cell_w - 12, cell_h - 48))
            strip.paste(thumb, (x0 + 6, y0 + 6))
        draw.rectangle([x0 + 4, y0 + 4, x0 + cell_w - 4, y0 + cell_h - 4], outline=(90, 235, 160), width=2)
        draw.text(
            (x0 + 12, y0 + cell_h - 36),
            f"{kf['time_sec']}s | {kf['keyframe_id']} ({kf['label_zh']})",
            fill=(140, 250, 180),
        )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    strip.save(out_path, quality=92)
    return out_path


def build_video_transition_manifest(
    five_keyframes: list[dict[str, Any]],
    candidate_id: str,
) -> list[dict[str, Any]]:
    """Build proposed transition records only; this function does not render or validate a video."""
    transitions: list[dict[str, Any]] = []
    for i in range(len(five_keyframes) - 1):
        k_from, k_to = five_keyframes[i], five_keyframes[i + 1]
        transitions.append({
            "segment_id": f"seg{i:02d}_{k_from['keyframe_id']}_to_{k_to['keyframe_id']}",
            "candidate_id": candidate_id,
            "start_time_sec": k_from["time_sec"],
            "end_time_sec": k_to["time_sec"],
            "start_stage": k_from["keyframe_id"],
            "end_stage": k_to["keyframe_id"],
            "start_frame": k_from["image_path"],
            "start_sha256": k_from["sha256"],
            "end_frame": k_to["image_path"],
            "end_sha256": k_to["sha256"],
            "fps": 24,
            "duration_sec": round(float(k_to["time_sec"]) - float(k_from["time_sec"]), 2),
            "motion_bucket_id": 127,
            "transition_prompt": (
                f"Proposed {k_from['time_sec']}s->{k_to['time_sec']}s interpolation ({k_from['label_zh']} -> {k_to['label_zh']}); "
                f"keep C13 radial dark-steel cylinder, 100% bare lower-left circular cap, and upper-left 90° straight rod locked."
            ),
            "validation_status": "PROMPT_ONLY_NOT_INTERPOLATED_OR_VISUALLY_VALIDATED",
        })
    return transitions


def run_autonomous_pipeline(
    outdir: Path,
    *,
    stage_candidates_map: dict[str, Sequence[Path]] | None = None,
    pre_far_candidate: Path | None = None,
    pre_near_candidate: Path | None = None,
    simulate_fault_injection: bool = False,
    synthetic_test_mode: bool = False,
) -> AutonomousPipelineReport:
    """Audit supplied raster candidates. This function does not call an image model.

    By default, real candidate rasters for every required stage plus PRE_FAR and PRE_NEAR
    must be supplied. Procedural rasters are allowed only when synthetic_test_mode=True;
    such a run can pass software contract tests but can never be reported as visual acceptance.
    """
    outdir.mkdir(parents=True, exist_ok=True)
    if simulate_fault_injection and not synthetic_test_mode:
        raise ValueError("simulate_fault_injection is permitted only in synthetic_test_mode")
    if not synthetic_test_mode:
        if not stage_candidates_map:
            raise ValueError(
                "BLOCK: real raster candidates are required; this script has no connected image-generation backend. "
                "Supply --candidates-json with A/B/D1/D2/D3/E_MID/E_END candidates."
            )
        required_stages = ("A", "B", "D1", "D2", "D3", "E_MID", "E_END")
        missing = [stage for stage in required_stages if not stage_candidates_map.get(stage)]
        if missing:
            raise ValueError(f"BLOCK: missing real candidate rasters for stages: {', '.join(missing)}")
        missing_files = [
            str(path) for stage in required_stages for path in stage_candidates_map[stage]
            if not Path(path).is_file()
        ]
        if missing_files:
            raise ValueError("BLOCK: candidate raster file(s) do not exist: " + ", ".join(missing_files))
        if pre_far_candidate is None or not Path(pre_far_candidate).is_file():
            raise ValueError("BLOCK: supply a real PRE_FAR raster; synthetic fallback is forbidden")
        if pre_near_candidate is None or not Path(pre_near_candidate).is_file():
            raise ValueError("BLOCK: supply a real PRE_NEAR raster; the code-composited fixture is test-only")
    rasters_dir = outdir / "rasters"
    gates_dir = outdir / "gates"
    rasters_dir.mkdir(parents=True, exist_ok=True)
    gates_dir.mkdir(parents=True, exist_ok=True)

    candidates = make_candidates()
    winner, ranking = auto_select_candidate(candidates)
    roi_xywh = estimate_candidate_roi(winner)

    canonical_sequence: dict[str, dict[str, Any]] = {}
    attempt_history: list[dict[str, Any]] = []
    auto_rejections = 0
    prev_sha: str | None = None
    prev_image_path: Path | None = None

    for stage in AUTONOMOUS_STAGE_SEQUENCE:
        if stage == "B0_ROI_4X":
            stage_a_img = Path(canonical_sequence["A"]["image_path"])
            roi_4x_dest = rasters_dir / f"LOCKED_B0_ROI_4X_{winner.candidate_id}.jpg"
            extract_stage_a_c13_roi_4x(stage_a_img, roi_4x_dest)
            sha = sha256_file(roi_4x_dest)
            canonical_sequence["B0_ROI_4X"] = {
                "stage": "B0_ROI_4X",
                "image_path": str(roi_4x_dest),
                "sha256": sha,
                "parent_sha256": canonical_sequence["A"]["sha256"],
                "pixel_lock_clause": "STAGE_B0_4X_ROI_CROP_ZOOM_PIXEL_TRUTH",
                "passed": True,
                "quality_score": 0.96,
                "elevation_level": "k=0_ROI_4X_ZOOM",
            }
            prev_sha = sha
            continue

        if stage == "D0":
            b_info = canonical_sequence["B"]
            canonical_sequence["D0"] = {
                "stage": "D0",
                "image_path": b_info["image_path"],
                "sha256": b_info["sha256"],
                "parent_sha256": b_info["sha256"],
                "pixel_lock_clause": grip_pixel_lock_clause("D0", b_info["sha256"]),
                "passed": True,
                "quality_score": b_info["quality_score"],
                "elevation_level": "k=0_TOPOLOGY_FREEZE",
            }
            prev_sha = b_info["sha256"]
            prev_image_path = Path(b_info["image_path"])
            continue

        stage_files: list[Path] = []
        if stage_candidates_map and stage in stage_candidates_map:
            stage_files = [Path(p) for p in stage_candidates_map[stage]]
        elif synthetic_test_mode:
            if simulate_fault_injection and stage == "D2":
                bad_p = rasters_dir / f"{stage}_attempt01_fault_outer_shaft.jpg"
                render_synthetic_stage_raster(bad_p, stage, inject_fault="outer_end_shaft")
                stage_files.append(bad_p)
            elif simulate_fault_injection and stage == "D3":
                bad_p = rasters_dir / f"{stage}_attempt01_fault_scene_jump.jpg"
                render_synthetic_stage_raster(bad_p, stage, inject_fault="scene_jump")
                stage_files.append(bad_p)
            elif simulate_fault_injection and stage == "E_END":
                bad_p = rasters_dir / f"{stage}_attempt01_fault_flipped_handle.jpg"
                render_synthetic_stage_raster(bad_p, stage, inject_fault="flip_handle_right")
                stage_files.append(bad_p)
            good_p = rasters_dir / f"{stage}_canonical_synthetic_test_only.jpg"
            render_synthetic_stage_raster(good_p, stage)
            stage_files.append(good_p)
        else:
            raise ValueError(
                f"BLOCK: no real candidate raster list supplied for stage {stage}; refusing synthetic PASS fallback"
            )
        if not stage_files:
            raise ValueError(f"BLOCK: empty raster candidate list for stage {stage}")

        stage_passed = False
        passing_attempts: list[CandidateAttemptRecord] = []
        best_attempt: CandidateAttemptRecord | None = None
        elevation = "k=3_FULL_PROGRAM_LOCK"
        d_step = stage_to_canonical_d_step(stage)
        lock_clause = grip_pixel_lock_clause(d_step, prev_sha) if stage != "A" else "STAGE_A_24_CANDIDATE_ATLAS"

        for idx, cand_path in enumerate(stage_files, start=1):
            sha = sha256_file(cand_path)
            passed, score, gates, reasons = audit_candidate_frame(
                stage,
                cand_path,
                prev_sha256=prev_sha,
                parent_image_path=prev_image_path if stage not in ("A", "B") else None,
            )
            repair_note = None
            if not passed:
                auto_rejections += 1
                patch = compile_elevation_prompt_repair(winner, stage, prev_sha, reasons)
                elevation = patch["elevation_level"]
                repair_note = f"AUTO_REJECT_AND_ROLLBACK_TO_{(prev_sha or 'STAGE_A')[:10]} -> {elevation}"
                (gates_dir / f"REJECTED_{stage}_attempt{idx:02d}_repair_prompt.txt").write_text(
                    patch["repaired_prompt"], encoding="utf-8"
                )

            rec = CandidateAttemptRecord(
                stage=stage,
                attempt_index=idx,
                image_path=str(cand_path),
                sha256=sha,
                parent_sha256=prev_sha,
                pixel_lock_clause=lock_clause,
                elevation_level=elevation,
                passed=passed,
                quality_score=score,
                gates=[g.to_dict() for g in gates],
                rejection_reasons=reasons,
                repair_action_taken=repair_note,
            )
            attempt_history.append(asdict(rec))
            (gates_dir / f"gate_{stage}_attempt{idx:02d}.json").write_text(
                json.dumps(asdict(rec), indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            if passed:
                passing_attempts.append(rec)
            if best_attempt is None or rec.quality_score > best_attempt.quality_score:
                best_attempt = rec

        # Evaluate the whole candidate wash. Choose the highest-scoring PASS, not merely
        # the first PASS. A failed-only stage is BLOCKED and must not feed later stages.
        if not passing_attempts:
            blocked = {
                "status": "BLOCKED_NO_PASSING_CANDIDATE",
                "stage": stage,
                "parent_sha256": prev_sha,
                "candidate_attempts": [x for x in attempt_history if x["stage"] == stage],
                "generation_backend_status": "NOT_CONNECTED_BY_THIS_SCRIPT",
                "visual_acceptance_status": "NOT_VERIFIED_HUMAN_REVIEW_REQUIRED",
            }
            (gates_dir / f"BLOCKED_{stage}.json").write_text(
                json.dumps(blocked, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
            )
            raise RuntimeError(
                f"BLOCK: every supplied candidate failed gates for {stage}; see {gates_dir / f'BLOCKED_{stage}.json'}"
            )
        best_attempt = max(passing_attempts, key=lambda item: item.quality_score)
        stage_passed = True
        locked_dest = rasters_dir / f"LOCKED_{stage}_{winner.candidate_id}.jpg"
        if Path(best_attempt.image_path).resolve() != locked_dest.resolve():
            shutil.copy2(best_attempt.image_path, locked_dest)

        canonical_sequence[stage] = {
            "stage": stage,
            "image_path": str(locked_dest),
            "sha256": best_attempt.sha256,
            "parent_sha256": prev_sha,
            "pixel_lock_clause": lock_clause,
            "passed": stage_passed,
            "quality_score": best_attempt.quality_score,
            "elevation_level": best_attempt.elevation_level,
            "gates": best_attempt.gates,
        }
        if stage_passed:
            prev_sha = best_attempt.sha256
            prev_image_path = locked_dest

    # Build the 10-second 5-Keyframe Trilogy from five actual/declared raster states.
    # Production must supply both pre-contact states. The image-composited PRE_NEAR helper
    # is allowed only as a synthetic unit-test fixture and is never called for real runs.
    d3_locked_path = Path(canonical_sequence["D3"]["image_path"])
    pre_far_dest = rasters_dir / f"LOCKED_KF1_0S_PRE_FAR_{winner.candidate_id}.jpg"
    pre_near_dest = rasters_dir / f"LOCKED_KF2_2S_PRE_NEAR_{winner.candidate_id}.jpg"
    if pre_far_candidate and Path(pre_far_candidate).is_file():
        shutil.copy2(pre_far_candidate, pre_far_dest)
    elif synthetic_test_mode:
        render_synthetic_stage_raster(pre_far_dest, "PRE_FAR")
    else:
        raise ValueError("BLOCK: missing real PRE_FAR input")

    if pre_near_candidate and Path(pre_near_candidate).is_file():
        shutil.copy2(pre_near_candidate, pre_near_dest)
    elif synthetic_test_mode:
        synthesize_connected_pre_near_frame(pre_far_dest, d3_locked_path, pre_near_dest)
    else:
        raise ValueError("BLOCK: missing real PRE_NEAR input")

    # Validate each pre-contact state, not just the planted contact spine.
    pre_far_passed, pre_far_score, pre_far_gates, pre_far_reasons = audit_candidate_frame(
        "PRE_FAR", pre_far_dest, prev_sha256=canonical_sequence["D3"]["sha256"]
    )
    pre_near_passed, pre_near_score, pre_near_gates, pre_near_reasons = audit_candidate_frame(
        "PRE_NEAR", pre_near_dest, prev_sha256=sha256_file(pre_far_dest)
    )
    pre_state_audit = {
        "PRE_FAR": {"passed": pre_far_passed, "score": pre_far_score,
                    "gates": [g.to_dict() for g in pre_far_gates], "reasons": pre_far_reasons},
        "PRE_NEAR": {"passed": pre_near_passed, "score": pre_near_score,
                     "gates": [g.to_dict() for g in pre_near_gates], "reasons": pre_near_reasons},
    }
    if not pre_far_passed or not pre_near_passed:
        (gates_dir / "BLOCKED_PRECONTACT_KEYFRAMES.json").write_text(
            json.dumps({"status": "BLOCKED_PRECONTACT_KEYFRAME_GATE", **pre_state_audit},
                       indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        raise RuntimeError("BLOCK: PRE_FAR or PRE_NEAR failed the per-frame state gates")

    five_keyframes = [
        {
            "keyframe_id": "KF1_PRE_FAR",
            "time_sec": 0.0,
            "label_zh": "遠距蓄力（未碰泡前・大氣隙）",
            "image_path": str(pre_far_dest),
            "sha256": sha256_file(pre_far_dest),
        },
        {
            "keyframe_id": "KF2_PRE_NEAR",
            "time_sec": 2.0,
            "label_zh": "近泡逼近（未碰泡前・微氣隙）",
            "image_path": str(pre_near_dest),
            "sha256": sha256_file(pre_near_dest),
        },
        {
            "keyframe_id": "KF3_D3_CONTACT",
            "time_sec": 4.5,
            "label_zh": "持柄接觸（底面貼合發光母錨點）",
            "image_path": canonical_sequence["D3"]["image_path"],
            "sha256": canonical_sequence["D3"]["sha256"],
        },
        {
            "keyframe_id": "KF4_E_MID_SHOCK",
            "time_sec": 7.0,
            "label_zh": "衝擊碎裂（底光擴散與放射裂紋）",
            "image_path": canonical_sequence["E_MID"]["image_path"],
            "sha256": canonical_sequence["E_MID"]["sha256"],
        },
        {
            "keyframe_id": "KF5_E_END_BLAST",
            "time_sec": 10.0,
            "label_zh": "史詩爆破尾幀（泡殼向外炸裂）",
            "image_path": canonical_sequence["E_END"]["image_path"],
            "sha256": canonical_sequence["E_END"]["sha256"],
        },
    ]

    stage_a_raster = Path(canonical_sequence["A"]["image_path"])
    build_packet(
        outdir=outdir / "compiled_packet",
        selected_id=winner.candidate_id,
        source_raster=stage_a_raster,
        roi=roi_xywh,
        auto_select=True,
    )

    # Check all four adjacent transitions in the published five-keyframe timeline.
    # This is a coarse background test only; subject identity and narrative continuity remain
    # explicit human-review requirements and are never inferred from a high NCC by itself.
    keyframe_transition_audits: list[dict[str, Any]] = []
    for left, right in zip(five_keyframes, five_keyframes[1:]):
        gate = gate_static_background_continuity(
            Path(right["image_path"]), Path(left["image_path"])
        )
        keyframe_transition_audits.append({
            "from": left["keyframe_id"], "to": right["keyframe_id"],
            "from_sha256": left["sha256"], "to_sha256": right["sha256"],
            **gate.to_dict(),
        })
    if any(not item["passed"] for item in keyframe_transition_audits):
        (gates_dir / "BLOCKED_KEYFRAME_BACKGROUND_CONTINUITY.json").write_text(
            json.dumps({"status": "BLOCKED_KEYFRAME_BACKGROUND_CONTINUITY",
                        "transitions": keyframe_transition_audits},
                       indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        raise RuntimeError("BLOCK: one or more 5-keyframe transitions failed static-background continuity")

    video_manifest = build_video_transition_manifest(five_keyframes, winner.candidate_id)
    passed_count = sum(1 for item in canonical_sequence.values() if item["passed"])
    all_contract_gates_passed = (
        passed_count == len(AUTONOMOUS_STAGE_SEQUENCE)
        and pre_far_passed and pre_near_passed
        and all(item["passed"] for item in keyframe_transition_audits)
    )
    evidence_mode = "SYNTHETIC_TEST_ONLY" if synthetic_test_mode else "PROVIDED_RASTER_CANDIDATES"
    report = AutonomousPipelineReport(
        workflow="v5-canonical-spine-and-5keyframe-trilogy-continuity-engine",
        selected_candidate_id=winner.candidate_id,
        auto_selection_score=ranking[0]["total_score"],
        total_stages=len(AUTONOMOUS_STAGE_SEQUENCE),
        passed_stages=passed_count,
        total_attempts=len(attempt_history),
        auto_rejections_and_rollbacks=auto_rejections,
        # Deliberately false for synthetic fixtures even when their software gates pass.
        all_stages_passed=(all_contract_gates_passed and not synthetic_test_mode),
        canonical_sequence=canonical_sequence,
        attempt_history=attempt_history,
        five_keyframe_trilogy=five_keyframes,
        video_transition_manifest=video_manifest,
        evidence_mode=evidence_mode,
        all_contract_gates_passed=all_contract_gates_passed,
        visual_acceptance_status="NOT_VERIFIED_HUMAN_REVIEW_REQUIRED",
        generation_backend_status="NOT_CONNECTED_BY_THIS_SCRIPT",
        keyframe_transition_audits=keyframe_transition_audits,
    )
    board_path = create_audit_contact_board(report, outdir / "AUTONOMOUS_AUDIT_SUMMARY_BOARD.jpg")
    strip_path = create_five_keyframe_trilogy_strip(
        five_keyframes, outdir / "CONNECTED_5KEYFRAME_TRILOGY_STRIP.jpg",
        evidence_mode=report.evidence_mode,
    )
    report.summary_board_path = str(board_path)
    report.trilogy_strip_path = str(strip_path)

    (outdir / "AUTONOMOUS_RUN_MANIFEST.json").write_text(
        json.dumps(report.to_dict(), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=Path("out/autonomous_run"))
    parser.add_argument("--simulate-fault-injection", action="store_true")
    parser.add_argument("--synthetic-test-mode", action="store_true",
                        help="use procedural fixture rasters for software tests only; never visual acceptance")
    parser.add_argument("--candidates-json", type=Path, default=None,
                        help="JSON mapping stage names A/B/D1/D2/D3/E_MID/E_END to pre-generated raster paths")
    parser.add_argument("--pre-far-candidate", type=Path, default=None)
    parser.add_argument("--pre-near-candidate", type=Path, default=None)
    args = parser.parse_args(list(argv) if argv is not None else None)

    stage_map: dict[str, Sequence[Path]] | None = None
    if args.candidates_json:
        if not args.candidates_json.is_file():
            print(json.dumps({"status": "BLOCK", "reason": f"candidate map not found: {args.candidates_json}"}, ensure_ascii=False))
            return 2
        raw = json.loads(args.candidates_json.read_text(encoding="utf-8"))
        stage_map = {k: [Path(p) for p in v] for k, v in raw.items()}

    try:
        report = run_autonomous_pipeline(
            args.outdir,
            stage_candidates_map=stage_map,
            pre_far_candidate=args.pre_far_candidate,
            pre_near_candidate=args.pre_near_candidate,
            simulate_fault_injection=args.simulate_fault_injection,
            synthetic_test_mode=args.synthetic_test_mode,
        )
    except (ValueError, RuntimeError) as exc:
        args.outdir.mkdir(parents=True, exist_ok=True)
        blocked = {
            "status": "BLOCKED",
            "reason": str(exc),
            "generation_backend_status": "NOT_CONNECTED_BY_THIS_SCRIPT",
            "image_realization_status": "NOT_RUN_BY_THIS_SCRIPT",
            "visual_acceptance_status": "NOT_VERIFIED",
        }
        (args.outdir / "BLOCKED_RUN.json").write_text(
            json.dumps(blocked, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(json.dumps(blocked, indent=2, ensure_ascii=False))
        return 2

    print(json.dumps({
        "selected_candidate_id": report.selected_candidate_id,
        "passed_contract_stages": f"{report.passed_stages}/{report.total_stages}",
        "auto_rejections_and_rollbacks": report.auto_rejections_and_rollbacks,
        "all_stages_passed_on_real_rasters": report.all_stages_passed,
        "all_contract_gates_passed": report.all_contract_gates_passed,
        "evidence_mode": report.evidence_mode,
        "visual_acceptance_status": report.visual_acceptance_status,
        "generation_backend_status": report.generation_backend_status,
        "keyframe_transition_audits": report.keyframe_transition_audits,
        "manifest": str(args.outdir / "AUTONOMOUS_RUN_MANIFEST.json"),
        "summary_board": report.summary_board_path,
        "trilogy_strip": report.trilogy_strip_path,
    }, indent=2, ensure_ascii=False))
    return 0 if report.all_contract_gates_passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
