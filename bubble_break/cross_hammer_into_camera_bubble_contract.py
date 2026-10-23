#!/usr/bin/env python3
"""L1–L5 consumable panel contract: CROSS hammer (十字槌) + unbroken INTO-CAMERA bubble barrage.

Maps the Imagine visual line (cross maul + continuous bubbles flying into lens) onto the same
progressive-lock / cumulative full re-audit pattern as layered_divine_hammer_wash_audit.py.

Geometry (hard):
  - Head is a true CROSS / plus-sign: four arms meeting at a central boss.
  - Arm axes: horizontal pair u_h and vertical pair u_v with |u_h · u_v| ≈ 0 (orthogonal).
  - Handle v_handle attaches at boss, roughly perpendicular to the cross plane OR in-plane
    as a shaft; NOT a simple double-ended cylinder (that is REJECT for this contract).
  - NO spear-handle trap: when striking a bubble on the into-camera axis n_cam,
    a true end-face of one cross arm must align with n_cam, not the shaft axis alone.

Scene (hard):
  - Bubbles fly toward camera (into-lens stream); stream never "clears" (unbroken barrage).
  - Each impact may explode the bubble; new bubbles keep arriving.
  - visual_acceptance_status remains NOT_VERIFIED_BY_CODE until human eye gates.

Imagine anchors (session, non-binding metadata):
  - still: 34eede64-2215-4412-a459-8a27a27daa9a
  - video: a2fa4cef-704c-4711-aebb-64ecb8754c04
"""
from __future__ import annotations

import hashlib
import math
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Sequence

import numpy as np
from PIL import Image

# ---------------------------------------------------------------------------
# Face / method vocab for single-heroine cross maul vs into-camera bubbles
# ---------------------------------------------------------------------------

VALID_CROSS_STRIKE_FACES: tuple[str, ...] = (
    "CX_ARM_END_N",       # +Y arm tip (screen-up relative to cross)
    "CX_ARM_END_S",       # -Y
    "CX_ARM_END_E",       # +X
    "CX_ARM_END_W",       # -X
    "CX_BOSS_CENTER",     # central boss (rare, thrust-into-lens)
    "CX_BEVEL_45",        # chamfer between arms
)

VALID_SKILL_MOVE_IDS: tuple[str, ...] = (
    "SK_OVERHEAD_SMASH",
    "SK_SPIN_SLASH",
    "SK_THRUST_INTO_LENS",
    "SK_WHIRLWIND",
    "SK_SIDE_SWEEP",
    "SK_COUNTER_PUNCH",
    "SK_COMBO_3HIT",
)

VALID_CAMERA_RIGS: tuple[str, ...] = (
    "CAM_INTO_LENS_EYE",      # bubbles rush toward lens, hero mid/far
    "CAM_INTO_LENS_LOW",
    "CAM_INTO_LENS_DUTCH",
    "CAM_ORBIT_LEFT",
    "CAM_ORBIT_RIGHT",
)


@dataclass
class CrossHammerGeometry:
    """Single 十字槌 instance."""

    instance_id: str
    # Four arm tips in image px (N, E, S, W order preferred); boss is centroid.
    arm_tip_n_px: tuple[float, float]
    arm_tip_e_px: tuple[float, float]
    arm_tip_s_px: tuple[float, float]
    arm_tip_w_px: tuple[float, float]
    boss_center_px: tuple[float, float]
    handle_axis_px: tuple[tuple[float, float], tuple[float, float]]  # boss→grip end
    grip_point_px: tuple[float, float]
    pull_force_vec: tuple[float, float]
    declared_strike_face_id: str
    active_face_center_px: tuple[float, float]
    active_face_radius_px: float


@dataclass
class BubbleBarrageSpec:
    """Unbroken into-camera bubble stream metadata (panel-level)."""

    bubble_count_visible: int
    into_camera_fraction: float  # 0..1 fraction annotated as flying toward lens
    exploding_near_lens_count: int
    stream_never_clears: bool  # hard contract: must be True
    primary_impact_p_px: tuple[float, float]


@dataclass
class CrossHammerPanelCandidateSpec:
    panel_id: str
    panel_index: int
    raster_path: Path
    raster_sha256: str
    skill_move_id: str
    camera_rig_id: str
    camera_elevation_deg: float
    camera_azimuth_deg: float
    # Into-camera impact axis in image plane: angle of n_cam projected (0=right, 90=up)
    into_camera_axis_angle_deg: float
    hammer: CrossHammerGeometry
    barrage: BubbleBarrageSpec
    # optional dual-actor unused; reserved
    notes: str = ""


@dataclass
class LayerGateResult:
    layer_id: str
    panel_id: str
    passed: bool
    errors: list[str] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)


@dataclass
class CumulativeReauditReport:
    up_to_layer: int
    total_panels_audited: int
    passed: bool
    status: str
    visual_acceptance_status: str
    layer_results: list[dict[str, Any]]
    blocking_errors: list[str]
    contract_id: str = "CROSS_HAMMER_INTO_CAMERA_BUBBLE_L1_L5"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _unit_vec(p0: Sequence[float], p1: Sequence[float]) -> tuple[tuple[float, float], float]:
    dx = float(p1[0]) - float(p0[0])
    dy = float(p1[1]) - float(p0[1])
    length = math.hypot(dx, dy)
    if length < 1e-6:
        return (0.0, 0.0), 0.0
    return (dx / length, dy / length), length


def _dot(a: tuple[float, float], b: tuple[float, float]) -> float:
    return a[0] * b[0] + a[1] * b[1]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def measure_raster_symmetry_and_thumb(path: Path) -> tuple[float, np.ndarray]:
    im = Image.open(path).convert("RGB")
    g = np.asarray(im.resize((160, 90), Image.Resampling.BILINEAR), dtype=np.float32).mean(axis=2)
    g_flip = np.fliplr(g)
    g_c = g - g.mean()
    gf_c = g_flip - g_flip.mean()
    lr_sym = float((g_c * gf_c).mean() / (np.sqrt((g_c**2).mean() * (gf_c**2).mean()) + 1e-8))
    return round(lr_sym, 4), g


def compute_layout_ncc(g1: np.ndarray, g2: np.ndarray) -> float:
    c1 = g1 - g1.mean()
    c2 = g2 - g2.mean()
    return round(float((c1 * c2).mean() / (np.sqrt((c1**2).mean() * (c2**2).mean()) + 1e-8)), 4)


def _cross_arm_lengths(h: CrossHammerGeometry) -> dict[str, float]:
    b = h.boss_center_px
    return {
        "N": math.hypot(h.arm_tip_n_px[0] - b[0], h.arm_tip_n_px[1] - b[1]),
        "E": math.hypot(h.arm_tip_e_px[0] - b[0], h.arm_tip_e_px[1] - b[1]),
        "S": math.hypot(h.arm_tip_s_px[0] - b[0], h.arm_tip_s_px[1] - b[1]),
        "W": math.hypot(h.arm_tip_w_px[0] - b[0], h.arm_tip_w_px[1] - b[1]),
    }


def audit_layer1_cross_hammer_topology(cand: CrossHammerPanelCandidateSpec) -> LayerGateResult:
    """L1: SHA bind + true CROSS head (4 arms, orthogonal pairs, not plain cylinder)."""
    errs: list[str] = []
    if not cand.raster_path.is_file():
        return LayerGateResult("L1_CROSS_HAMMER_TOPOLOGY", cand.panel_id, False, ["raster file missing"])

    actual_sha = sha256_file(cand.raster_path)
    if actual_sha != cand.raster_sha256.lower():
        errs.append(f"SHA-256 mismatch: expected {cand.raster_sha256[:12]}, got {actual_sha[:12]}")

    h = cand.hammer
    if h.declared_strike_face_id not in VALID_CROSS_STRIKE_FACES:
        errs.append(f"declared_strike_face_id={h.declared_strike_face_id!r} not in VALID_CROSS_STRIKE_FACES")

    if cand.skill_move_id not in VALID_SKILL_MOVE_IDS:
        errs.append(f"skill_move_id={cand.skill_move_id!r} not in VALID_SKILL_MOVE_IDS")
    if cand.camera_rig_id not in VALID_CAMERA_RIGS:
        errs.append(f"camera_rig_id={cand.camera_rig_id!r} not in VALID_CAMERA_RIGS")

    lens = _cross_arm_lengths(h)
    metrics: dict[str, Any] = {"arm_lengths_px": {k: round(v, 2) for k, v in lens.items()}, "sha256_verified": actual_sha == cand.raster_sha256.lower()}

    # Each arm must exist (min length)
    for k, L in lens.items():
        if L < 28.0:
            errs.append(f"CROSS arm {k} too short: {L:.1f}px < 28 (not a true 十字 head)")

    # Pair balance: N/S and E/W within 35% of each other
    if lens["N"] > 1e-6 and lens["S"] > 1e-6:
        ratio_ns = max(lens["N"], lens["S"]) / max(min(lens["N"], lens["S"]), 1e-6)
        metrics["ns_length_ratio"] = round(ratio_ns, 3)
        if ratio_ns > 1.55:
            errs.append(f"N/S arm imbalance ratio={ratio_ns:.2f} > 1.55 (asymmetric pseudo-cross)")
    if lens["E"] > 1e-6 and lens["W"] > 1e-6:
        ratio_ew = max(lens["E"], lens["W"]) / max(min(lens["E"], lens["W"]), 1e-6)
        metrics["ew_length_ratio"] = round(ratio_ew, 3)
        if ratio_ew > 1.55:
            errs.append(f"E/W arm imbalance ratio={ratio_ew:.2f} > 1.55")

    # Orthogonality of NS axis vs EW axis
    u_ns, ln = _unit_vec(h.arm_tip_s_px, h.arm_tip_n_px)
    u_ew, le = _unit_vec(h.arm_tip_w_px, h.arm_tip_e_px)
    if ln < 40.0 or le < 40.0:
        errs.append("NS or EW span too short for orthogonal cross check")
    else:
        ortho = abs(_dot(u_ns, u_ew))
        metrics["cross_arm_ortho_cos"] = round(ortho, 4)
        if ortho > 0.35:
            errs.append(
                f"NOT_TRUE_CROSS: |u_NS · u_EW|={ortho:.3f} > 0.35 "
                f"(arms not orthogonal — looks like T/cylinder, not 十字)"
            )

    # Handle must exist
    _, handle_len = _unit_vec(h.handle_axis_px[0], h.handle_axis_px[1])
    metrics["handle_len_px"] = round(handle_len, 2)
    if handle_len < 40.0:
        errs.append(f"handle_len={handle_len:.1f} too short")

    # Reject "plain double cylinder" signature: if E and W arms missing but N/S long → cylinder
    if lens["E"] < 20.0 and lens["W"] < 20.0 and (lens["N"] + lens["S"]) > 80.0:
        errs.append("PLAIN_CYLINDER_NOT_CROSS: E/W arms missing while N/S form a bar")

    return LayerGateResult("L1_CROSS_HAMMER_TOPOLOGY", cand.panel_id, len(errs) == 0, errs, metrics)


def audit_layer2_true_strike_and_anti_spear_into_camera(
    cand: CrossHammerPanelCandidateSpec,
) -> LayerGateResult:
    """L2: Strike face vs into-camera axis; reject spear-handle (shaft-only) into-lens hits."""
    errs: list[str] = []
    rad = math.radians(cand.into_camera_axis_angle_deg)
    n_cam = (math.cos(rad), math.sin(rad))
    h = cand.hammer
    metrics: dict[str, Any] = {"into_camera_axis_angle_deg": cand.into_camera_axis_angle_deg}

    # Active face must sit near primary impact P (bubble being smashed toward lens)
    px, py = cand.barrage.primary_impact_p_px
    dist_p = math.hypot(h.active_face_center_px[0] - px, h.active_face_center_px[1] - py)
    metrics["active_face_dist_to_p_px"] = round(dist_p, 2)
    if dist_p > h.active_face_radius_px + 18.0:
        errs.append(
            f"active face {h.active_face_center_px} does not touch primary impact P={cand.barrage.primary_impact_p_px}"
        )

    v_handle, _ = _unit_vec(h.handle_axis_px[0], h.handle_axis_px[1])
    handle_dot_n = abs(_dot(v_handle, n_cam))
    metrics["handle_dot_n_cam"] = round(handle_dot_n, 4)

    # Direction from boss to active face ≈ strike axis of chosen arm
    u_strike, strike_len = _unit_vec(h.boss_center_px, h.active_face_center_px)
    metrics["strike_arm_len_px"] = round(strike_len, 2)
    if strike_len < 20.0:
        errs.append("strike arm boss→active_face too short")
    else:
        strike_dot_n = abs(_dot(u_strike, n_cam))
        metrics["strike_arm_dot_n_cam"] = round(strike_dot_n, 4)

        if h.declared_strike_face_id.startswith("CX_ARM_END"):
            # Spear trap: handle aimed at camera while strike arm not aligned
            if handle_dot_n > 0.70 and strike_dot_n < 0.40:
                errs.append(
                    f"SPEAR_HANDLE_INTO_LENS_TRAP: handle aimed into camera "
                    f"(|v_handle·n|={handle_dot_n:.2f}) while cross-arm strike is off "
                    f"(|u_strike·n|={strike_dot_n:.2f}) — shaft poke instead of 十字 arm face"
                )
            elif strike_dot_n < 0.55:
                errs.append(
                    f"declared {h.declared_strike_face_id} but strike arm not into-camera "
                    f"(|u_strike·n|={strike_dot_n:.2f} < 0.55)"
                )
        elif h.declared_strike_face_id == "CX_BOSS_CENTER":
            # boss thrust: handle may align with n_cam
            if handle_dot_n < 0.70:
                errs.append(f"CX_BOSS_CENTER requires handle roughly along n_cam (|v·n|={handle_dot_n:.2f})")

    return LayerGateResult("L2_TRUE_STRIKE_ANTI_SPEAR_INTO_CAM", cand.panel_id, len(errs) == 0, errs, metrics)


def audit_layer3_barrage_and_lever_torque(
    cand: CrossHammerPanelCandidateSpec,
    *,
    max_lr_symmetry_ncc: float = 0.62,
    min_into_camera_fraction: float = 0.55,
    min_bubbles: int = 4,
) -> LayerGateResult:
    """L3: Unbroken into-camera barrage + lever torque (not axial push-only)."""
    errs: list[str] = []
    b = cand.barrage
    metrics: dict[str, Any] = {
        "bubble_count_visible": b.bubble_count_visible,
        "into_camera_fraction": b.into_camera_fraction,
        "exploding_near_lens_count": b.exploding_near_lens_count,
        "stream_never_clears": b.stream_never_clears,
    }

    if not b.stream_never_clears:
        errs.append("STREAM_CLEARED_ILLEGAL: stream_never_clears must be True (打不斷飛入鏡頭)")
    if b.bubble_count_visible < min_bubbles:
        errs.append(f"too few bubbles visible: {b.bubble_count_visible} < {min_bubbles}")
    if b.into_camera_fraction < min_into_camera_fraction:
        errs.append(
            f"INTO_CAMERA_FRACTION_LOW: {b.into_camera_fraction:.2f} < {min_into_camera_fraction} "
            f"(bubbles not mostly flying into lens)"
        )
    if b.exploding_near_lens_count < 1:
        errs.append("no near-lens explosion annotated (need at least one 泡爆 at lens)")

    lr_sym, _ = measure_raster_symmetry_and_thumb(cand.raster_path)
    metrics["left_right_symmetry_ncc"] = lr_sym
    if lr_sym > max_lr_symmetry_ncc:
        errs.append(
            f"EXCESSIVE_MIRROR_SYMMETRY_CLONE: lr_ncc={lr_sym:.3f} > {max_lr_symmetry_ncc} "
            f"(static mirror template, not violent skill motion)"
        )

    h = cand.hammer
    px, py = b.primary_impact_p_px
    r_vec, r_len = _unit_vec((px, py), h.grip_point_px)
    f_vec, f_len = _unit_vec((0.0, 0.0), h.pull_force_vec)
    if r_len < 25.0 or f_len < 1e-4:
        errs.append("missing valid grip lever arm or pull force vector")
    else:
        cross_sin = abs(r_vec[0] * f_vec[1] - r_vec[1] * f_vec[0])
        metrics["lever_torque_sin"] = round(cross_sin, 4)
        if cross_sin < 0.30:
            errs.append(
                f"AXIAL_PUSH_NO_LEVER_TORQUE: |r×F| sin={cross_sin:.3f} < 0.30 "
                f"(need wrench/swing torque for violent skill moves)"
            )

    return LayerGateResult("L3_BARRAGE_AND_LEVER_TORQUE", cand.panel_id, len(errs) == 0, errs, metrics)


def audit_layer4_cross_panel_variance(
    cand: CrossHammerPanelCandidateSpec,
    prior: Sequence[CrossHammerPanelCandidateSpec],
    *,
    max_same_skill_count: int = 2,
    max_pairwise_layout_ncc: float = 0.58,
) -> LayerGateResult:
    """L4: Panel k must diversify skill / camera / face vs 1..k-1."""
    errs: list[str] = []
    _, curr_thumb = measure_raster_symmetry_and_thumb(cand.raster_path)
    same_skill = 1
    max_ncc = 0.0
    nearest = "NONE"

    for prev in prior:
        if prev.skill_move_id == cand.skill_move_id:
            same_skill += 1
        if prev.skill_move_id == cand.skill_move_id and prev.camera_rig_id == cand.camera_rig_id:
            errs.append(
                f"DUPLICATE_SKILL_AND_CAMERA: matches {prev.panel_id} "
                f"({cand.skill_move_id}, {cand.camera_rig_id})"
            )
        if (
            prev.hammer.declared_strike_face_id == cand.hammer.declared_strike_face_id
            and prev.skill_move_id == cand.skill_move_id
        ):
            errs.append(
                f"DUPLICATE_FACE_AND_SKILL: matches {prev.panel_id} "
                f"({cand.hammer.declared_strike_face_id}, {cand.skill_move_id})"
            )

        _, prev_thumb = measure_raster_symmetry_and_thumb(prev.raster_path)
        ncc = compute_layout_ncc(curr_thumb, prev_thumb)
        if ncc > max_ncc:
            max_ncc = ncc
            nearest = prev.panel_id

    if same_skill > max_same_skill_count:
        errs.append(
            f"SKILL_OVER_CAP: skill {cand.skill_move_id} appears {same_skill} times "
            f"(max={max_same_skill_count})"
        )
    if max_ncc > max_pairwise_layout_ncc:
        errs.append(
            f"LAYOUT_NCC_CLONE_DETECTED: ncc={max_ncc:.3f} > {max_pairwise_layout_ncc} "
            f"(clone of {nearest})"
        )

    if prior:
        last = prior[-1]
        axis_diff = abs(cand.into_camera_axis_angle_deg - last.into_camera_axis_angle_deg)
        cam_diff = math.hypot(
            cand.camera_elevation_deg - last.camera_elevation_deg,
            cand.camera_azimuth_deg - last.camera_azimuth_deg,
        )
        if axis_diff < 12.0 and cam_diff < 20.0 and cand.skill_move_id == last.skill_move_id:
            errs.append(
                f"INSUFFICIENT_ADJACENT_STEP_VARIANCE vs {last.panel_id}: "
                f"axis_diff={axis_diff:.1f} cam_diff={cam_diff:.1f} same skill"
            )

    metrics = {
        "same_skill_count_so_far": same_skill,
        "max_layout_ncc_with_prior": max_ncc,
        "most_similar_prior_panel": nearest,
        "strike_face": cand.hammer.declared_strike_face_id,
        "skill_move_id": cand.skill_move_id,
    }
    return LayerGateResult("L4_CROSS_PANEL_VARIANCE", cand.panel_id, len(errs) == 0, errs, metrics)


def run_cumulative_cross_hammer_full_reaudit(
    panels: Sequence[CrossHammerPanelCandidateSpec],
    *,
    up_to_layer: int = 5,
    max_lr_symmetry_ncc: float = 0.62,
    max_pairwise_layout_ncc: float = 0.58,
    max_same_skill_count: int = 2,
) -> CumulativeReauditReport:
    """L5: Full cumulative re-audit of L1..up_to_layer across all panels 1..k before advance."""
    layer_results: list[dict[str, Any]] = []
    blocking: list[str] = []

    for idx, cand in enumerate(panels):
        prior = panels[:idx]
        if up_to_layer >= 1:
            r1 = audit_layer1_cross_hammer_topology(cand)
            layer_results.append(asdict(r1))
            if not r1.passed:
                blocking.extend([f"[{cand.panel_id}][L1] {e}" for e in r1.errors])
        if up_to_layer >= 2:
            r2 = audit_layer2_true_strike_and_anti_spear_into_camera(cand)
            layer_results.append(asdict(r2))
            if not r2.passed:
                blocking.extend([f"[{cand.panel_id}][L2] {e}" for e in r2.errors])
        if up_to_layer >= 3:
            r3 = audit_layer3_barrage_and_lever_torque(cand, max_lr_symmetry_ncc=max_lr_symmetry_ncc)
            layer_results.append(asdict(r3))
            if not r3.passed:
                blocking.extend([f"[{cand.panel_id}][L3] {e}" for e in r3.errors])
        if up_to_layer >= 4:
            r4 = audit_layer4_cross_panel_variance(
                cand,
                prior,
                max_same_skill_count=max_same_skill_count,
                max_pairwise_layout_ncc=max_pairwise_layout_ncc,
            )
            layer_results.append(asdict(r4))
            if not r4.passed:
                blocking.extend([f"[{cand.panel_id}][L4] {e}" for e in r4.errors])

    passed = len(blocking) == 0
    return CumulativeReauditReport(
        up_to_layer=up_to_layer,
        total_panels_audited=len(panels),
        passed=passed,
        status=(
            "PASSED_CUMULATIVE_CROSS_HAMMER_REAUDIT_ADVANCE_APPROVED"
            if passed
            else "BLOCKED_CROSS_HAMMER_LAYER_ADVANCE_DENIED_BY_FULL_REAUDIT"
        ),
        visual_acceptance_status="NOT_VERIFIED_BY_CODE",
        layer_results=layer_results,
        blocking_errors=blocking,
    )


# Session Imagine anchors (documentation only; not used by gates)
IMAGINE_SESSION_ANCHORS: dict[str, str] = {
    "cross_still": "34eede64-2215-4412-a459-8a27a27daa9a",
    "violent_skill_video_10s": "a2fa4cef-704c-4711-aebb-64ecb8754c04",
    "face_id": "6ee74baf-2c16-44e8-aa14-b771002c7ebd",
    "cosplay_grip": "e40ef777-69a3-447c-8199-c9958560ce1b",
}
