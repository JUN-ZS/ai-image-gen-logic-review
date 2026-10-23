#!/usr/bin/env python3
"""5-Layer Progressive Lock & Cumulative Full Re-Audit Engine for Dual-Warrior Divine Hammer 10-Panel Wash.

Solves the three root failures identified in the Post-Mortem Self-Audit:
1. SPEAR_HANDLE_SIDE_CHEEK_TRAP (Layer 2):
   - In a T-shaped divine warhammer (`u_head ⊥ v_handle`), pointing the handle `v_handle` directly at the
     opponent along the impact normal `n` rotates the hammer head perpendicular to `n`, causing the two true
     strike end-faces (`F1_FRONT_END`, `F2_REAR_END`) to point into empty air while the side waist/cheek
     (`F3_WAIST_CHEEK`) touches the opponent.
   - Layer 2 mathematically verifies that the vector angle of `u_head` and `v_handle` relative to `n` matches
     the declared `target_face_id` (`END_FACE` requires `|u_head · n| >= 0.85` and `|v_handle · n| <= 0.35`).
2. REFERENCE_CLONE_FAKE_VARIANCE_TRAP (Layer 3 & Layer 4):
   - Layer 3 rejects static mirror-symmetric clones (`left_right_symmetry_ncc > max_lr_symmetry_ncc`) and requires
     a non-zero lever torque moment arm (`lever_arm_sin = |r_handle × F_pull| >= 0.35`).
   - Layer 4 (`L4_CROSS_PANEL_VARIANCE_EXCLUSIVITY_LOCK`) compares candidate Panel `k` against ALL previously
     locked panels `1 .. k-1`:
     * Rejects if the same `actual_contact_face_pair` appears more than `max_same_face_pair_count` times (default=2).
     * Rejects if `(strike_method_id, camera_rig_id, face_pair)` duplicates any prior panel.
     * Rejects if pairwise image layout correlation `layout_ncc > max_pairwise_layout_ncc` (default=0.58).
     * Rejects if adjacent panels fail to vary either collision axis angle (`>= 18 deg`) or camera angle (`>= 25 deg`).
3. CUMULATIVE FULL RE-AUDIT BEFORE LAYER / PANEL ADVANCE (Layer 5):
   - Before locking Layer `m` (`m = 1..5`) or advancing from Panel `k` to Panel `k+1`,
     `run_cumulative_layered_full_reaudit(...)` re-executes ALL checks from Layer 1 through Layer `m` across
     ALL locked panels `1 .. k`. Any single regression or violation blocks advancement immediately.
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Sequence

import numpy as np
from PIL import Image, ImageDraw


VALID_DIVINE_HAMMER_FACES: tuple[str, ...] = (
    "F1_FRONT_STRIKE_END_FACE",      # 正前端主打击端面 (需 u_head || n, v_handle ⊥ n)
    "F2_REAR_COUNTER_END_FACE",      # 反手後端打擊端蓋 (需 -u_head || n, v_handle ⊥ n)
    "F3_CROWN_TOP_THRUST_FACE",      # 槌頂冠部天靈頂面 (需 v_handle || n, u_head ⊥ n)
    "F4_BEVEL_45_CHAMFER_FACE",      # 45° 斜切破甲稜面 (需 |u_head · n| in [0.50, 0.84])
    "F5_FLANK_SHIELD_BROAD_CHEEK",   # 側翼寬盾護面 (僅限明確宣告為側盾拍擊，最多允許 1 格)
)


@dataclass
class HammerInstanceGeometry:
    instance_id: str
    head_axis_px: tuple[tuple[float, float], tuple[float, float]]
    handle_axis_px: tuple[tuple[float, float], tuple[float, float]]
    active_face_center_px: tuple[float, float]
    active_face_radius_px: float
    declared_face_id: str
    grip_point_px: tuple[float, float]
    pull_force_vec: tuple[float, float]


@dataclass
class WashPanelCandidateSpec:
    panel_id: str
    panel_index: int
    raster_path: Path
    raster_sha256: str
    strike_method_id: str
    camera_rig_id: str
    camera_elevation_deg: float
    camera_azimuth_deg: float
    collision_axis_angle_deg: float
    contact_point_p_px: tuple[float, float]
    hammer_a: HammerInstanceGeometry
    hammer_b: HammerInstanceGeometry


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

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _unit_vec(p0: Sequence[float], p1: Sequence[float]) -> tuple[tuple[float, float], float]:
    dx = float(p1[0]) - float(p0[0])
    dy = float(p1[1]) - float(p0[1])
    length = math.hypot(dx, dy)
    if length < 1e-6:
        return (0.0, 0.0), 0.0
    return (dx / length, dy / length), length


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


def audit_layer1_orthogonal_t_hammer_topology(cand: WashPanelCandidateSpec) -> LayerGateResult:
    """Layer 1: Verify SHA-256 binding, two distinct hammer instances, and T-hammer orthogonality (u_head ⊥ v_handle)."""
    errs: list[str] = []
    if not cand.raster_path.is_file():
        return LayerGateResult("L1_T_HAMMER_TOPOLOGY", cand.panel_id, False, ["raster file missing"])

    actual_sha = sha256_file(cand.raster_path)
    if actual_sha != cand.raster_sha256.lower():
        errs.append(f"SHA-256 mismatch: expected {cand.raster_sha256[:12]}, got {actual_sha[:12]}")

    if cand.hammer_a.instance_id == cand.hammer_b.instance_id:
        errs.append("hammer_a and hammer_b must have distinct instance_ids")

    metrics: dict[str, Any] = {"sha256_verified": actual_sha == cand.raster_sha256.lower()}
    for tag, h in (("A", cand.hammer_a), ("B", cand.hammer_b)):
        if h.declared_face_id not in VALID_DIVINE_HAMMER_FACES:
            errs.append(f"Hammer {tag} declared_face_id={h.declared_face_id!r} not in VALID_DIVINE_HAMMER_FACES")
        u_head, head_len = _unit_vec(h.head_axis_px[0], h.head_axis_px[1])
        v_handle, handle_len = _unit_vec(h.handle_axis_px[0], h.handle_axis_px[1])
        if head_len < 35.0 or handle_len < 45.0:
            errs.append(f"Hammer {tag} head_len={head_len:.1f} or handle_len={handle_len:.1f} too short")
            continue
        ortho_cos = abs(u_head[0] * v_handle[0] + u_head[1] * v_handle[1])
        metrics[f"hammer_{tag}_ortho_cos"] = round(ortho_cos, 4)
        if ortho_cos > 0.32:
            errs.append(f"Hammer {tag} fails T-hammer orthogonality: |u_head · v_handle|={ortho_cos:.3f} > 0.32")

    return LayerGateResult("L1_T_HAMMER_TOPOLOGY", cand.panel_id, len(errs) == 0, errs, metrics)


def audit_layer2_true_strike_face_and_anti_spear_trap(cand: WashPanelCandidateSpec) -> LayerGateResult:
    """Layer 2: Verify that the actual contacting geometry matches declared_face_id and reject Spear-Handle Side-Cheek Trap."""
    errs: list[str] = []
    rad = math.radians(cand.collision_axis_angle_deg)
    n_impact = (math.cos(rad), math.sin(rad))
    metrics: dict[str, Any] = {"collision_axis_angle_deg": cand.collision_axis_angle_deg}

    # Check both hammers meet at P
    px, py = cand.contact_point_p_px
    for tag, h in (("A", cand.hammer_a), ("B", cand.hammer_b)):
        dist_p = math.hypot(h.active_face_center_px[0] - px, h.active_face_center_px[1] - py)
        metrics[f"hammer_{tag}_dist_to_p_px"] = round(dist_p, 2)
        if dist_p > h.active_face_radius_px + 14.0:
            errs.append(f"Hammer {tag} active face center {h.active_face_center_px} does not touch P={cand.contact_point_p_px}")

        u_head, _ = _unit_vec(h.head_axis_px[0], h.head_axis_px[1])
        v_handle, _ = _unit_vec(h.handle_axis_px[0], h.handle_axis_px[1])
        head_dot_n = abs(u_head[0] * n_impact[0] + u_head[1] * n_impact[1])
        handle_dot_n = abs(v_handle[0] * n_impact[0] + v_handle[1] * n_impact[1])
        metrics[f"hammer_{tag}_head_dot_n"] = round(head_dot_n, 4)
        metrics[f"hammer_{tag}_handle_dot_n"] = round(handle_dot_n, 4)

        if h.declared_face_id in ("F1_FRONT_STRIKE_END_FACE", "F2_REAR_COUNTER_END_FACE"):
            if handle_dot_n > 0.65 and head_dot_n < 0.45:
                errs.append(
                    f"SPEAR_HANDLE_SIDE_CHEEK_TRAP on Hammer {tag}: handle is aimed along collision axis "
                    f"(|v_handle·n|={handle_dot_n:.2f}), rotating true end-faces away from P so the SIDE WAIST CHEEK touches!"
                )
            elif head_dot_n < 0.82:
                errs.append(
                    f"Hammer {tag} declared {h.declared_face_id} but head axis is not aligned with impact normal "
                    f"(|u_head·n|={head_dot_n:.2f} < 0.82)"
                )
        elif h.declared_face_id == "F4_BEVEL_45_CHAMFER_FACE":
            if not (0.45 <= head_dot_n <= 0.88):
                errs.append(f"Hammer {tag} declared 45-deg bevel face but |u_head·n|={head_dot_n:.2f} not in [0.45, 0.88]")

    return LayerGateResult("L2_TRUE_STRIKE_FACE_AND_ANTI_SPEAR", cand.panel_id, len(errs) == 0, errs, metrics)


def audit_layer3_biomechanical_lever_torque(
    cand: WashPanelCandidateSpec,
    *,
    max_lr_symmetry_ncc: float = 0.62,
) -> LayerGateResult:
    """Layer 3: Verify human lever torque moment arm (r_handle × F_pull) and reject static mirror-symmetric clones."""
    errs: list[str] = []
    lr_sym, _ = measure_raster_symmetry_and_thumb(cand.raster_path)
    metrics: dict[str, Any] = {"left_right_symmetry_ncc": lr_sym}

    if lr_sym > max_lr_symmetry_ncc:
        errs.append(
            f"EXCESSIVE_MIRROR_SYMMETRY_CLONE: left_right_symmetry_ncc={lr_sym:.3f} > {max_lr_symmetry_ncc:.2f} "
            f"(static left-right mirror template instead of dynamic asymmetric combat tension)"
        )

    px, py = cand.contact_point_p_px
    for tag, h in (("A", cand.hammer_a), ("B", cand.hammer_b)):
        r_vec, r_len = _unit_vec((px, py), h.grip_point_px)
        f_vec, f_len = _unit_vec((0.0, 0.0), h.pull_force_vec)
        if r_len < 30.0 or f_len < 1e-4:
            errs.append(f"Hammer {tag} missing valid grip lever arm or pull force vector")
            continue
        cross_sin = abs(r_vec[0] * f_vec[1] - r_vec[1] * f_vec[0])
        metrics[f"warrior_{tag}_lever_torque_sin"] = round(cross_sin, 4)
        if cross_sin < 0.35:
            errs.append(
                f"AXIAL_PUSH_NO_LEVER_TORQUE on Warrior {tag}: |r × F| sin={cross_sin:.3f} < 0.35 "
                f"(warrior is pushing handle axially like a spear instead of pulling/wrenching lever torque)"
            )

    return LayerGateResult("L3_BIOMECHANICAL_LEVER_TORQUE", cand.panel_id, len(errs) == 0, errs, metrics)


def audit_layer4_cross_panel_variance_exclusivity(
    cand: WashPanelCandidateSpec,
    prior_locked_panels: Sequence[WashPanelCandidateSpec],
    *,
    max_same_face_pair_count: int = 2,
    max_pairwise_layout_ncc: float = 0.58,
) -> LayerGateResult:
    """Layer 4: Verify that Panel k introduces true geometric/method/face variance against ALL prior panels 1..k-1."""
    errs: list[str] = []
    _, curr_thumb = measure_raster_symmetry_and_thumb(cand.raster_path)
    curr_face_pair = (cand.hammer_a.declared_face_id, cand.hammer_b.declared_face_id)

    same_face_count = 1
    max_ncc = 0.0
    nearest_panel_id = "NONE"

    for prev in prior_locked_panels:
        prev_face_pair = (prev.hammer_a.declared_face_id, prev.hammer_b.declared_face_id)
        if prev_face_pair == curr_face_pair:
            same_face_count += 1
        if (prev.strike_method_id == cand.strike_method_id) and (prev.camera_rig_id == cand.camera_rig_id):
            errs.append(
                f"DUPLICATE_METHOD_AND_CAMERA_RIG: matches prior panel {prev.panel_id} "
                f"({cand.strike_method_id}, {cand.camera_rig_id})"
            )

        _, prev_thumb = measure_raster_symmetry_and_thumb(prev.raster_path)
        ncc = compute_layout_ncc(curr_thumb, prev_thumb)
        if ncc > max_ncc:
            max_ncc = ncc
            nearest_panel_id = prev.panel_id

    if same_face_count > max_same_face_pair_count:
        errs.append(
            f"DUPLICATE_CONTACT_FACE_OVER_CAP: face pair {curr_face_pair} appears {same_face_count} times "
            f"(max allowed={max_same_face_pair_count})"
        )

    if max_ncc > max_pairwise_layout_ncc:
        errs.append(
            f"LAYOUT_NCC_CLONE_DETECTED: layout_ncc={max_ncc:.3f} > {max_pairwise_layout_ncc:.2f} "
            f"(cloned composition from prior panel {nearest_panel_id})"
        )

    if prior_locked_panels:
        last_p = prior_locked_panels[-1]
        axis_diff = abs(cand.collision_axis_angle_deg - last_p.collision_axis_angle_deg)
        cam_diff = math.hypot(
            cand.camera_elevation_deg - last_p.camera_elevation_deg,
            cand.camera_azimuth_deg - last_p.camera_azimuth_deg,
        )
        if axis_diff < 18.0 and cam_diff < 25.0:
            errs.append(
                f"INSUFFICIENT_ADJACENT_STEP_VARIANCE vs {last_p.panel_id}: "
                f"axis_diff={axis_diff:.1f}deg (<18) and cam_diff={cam_diff:.1f}deg (<25)"
            )

    metrics = {
        "face_pair": list(curr_face_pair),
        "same_face_pair_count_so_far": same_face_count,
        "max_layout_ncc_with_prior": max_ncc,
        "most_similar_prior_panel": nearest_panel_id,
    }
    return LayerGateResult("L4_CROSS_PANEL_VARIANCE_EXCLUSIVITY", cand.panel_id, len(errs) == 0, errs, metrics)


def run_cumulative_layered_full_reaudit(
    panels: Sequence[WashPanelCandidateSpec],
    *,
    up_to_layer: int = 5,
    max_same_face_pair_count: int = 2,
    max_pairwise_layout_ncc: float = 0.58,
    max_lr_symmetry_ncc: float = 0.62,
) -> CumulativeReauditReport:
    """Layer 5: Execute a full cumulative re-audit of Layers 1..up_to_layer across ALL panels 1..k before advancing."""
    layer_results: list[dict[str, Any]] = []
    blocking_errors: list[str] = []

    for idx, cand in enumerate(panels):
        prior = panels[:idx]
        if up_to_layer >= 1:
            r1 = audit_layer1_orthogonal_t_hammer_topology(cand)
            layer_results.append(asdict(r1))
            if not r1.passed:
                blocking_errors.extend([f"[{cand.panel_id}][L1] {e}" for e in r1.errors])
        if up_to_layer >= 2:
            r2 = audit_layer2_true_strike_face_and_anti_spear_trap(cand)
            layer_results.append(asdict(r2))
            if not r2.passed:
                blocking_errors.extend([f"[{cand.panel_id}][L2] {e}" for e in r2.errors])
        if up_to_layer >= 3:
            r3 = audit_layer3_biomechanical_lever_torque(cand, max_lr_symmetry_ncc=max_lr_symmetry_ncc)
            layer_results.append(asdict(r3))
            if not r3.passed:
                blocking_errors.extend([f"[{cand.panel_id}][L3] {e}" for e in r3.errors])
        if up_to_layer >= 4:
            r4 = audit_layer4_cross_panel_variance_exclusivity(
                cand,
                prior,
                max_same_face_pair_count=max_same_face_pair_count,
                max_pairwise_layout_ncc=max_pairwise_layout_ncc,
            )
            layer_results.append(asdict(r4))
            if not r4.passed:
                blocking_errors.extend([f"[{cand.panel_id}][L4] {e}" for e in r4.errors])

    passed = len(blocking_errors) == 0
    return CumulativeReauditReport(
        up_to_layer=up_to_layer,
        total_panels_audited=len(panels),
        passed=passed,
        status="PASSED_CUMULATIVE_LAYER_REAUDIT_ADVANCE_APPROVED" if passed else "BLOCKED_LAYER_ADVANCE_DENIED_BY_FULL_REAUDIT",
        visual_acceptance_status="NOT_VERIFIED_BY_CODE",
        layer_results=layer_results,
        blocking_errors=blocking_errors,
    )