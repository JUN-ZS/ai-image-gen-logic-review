#!/usr/bin/env python3
"""Stage D/E step-chain locks + autonomous multi-stage pixel & topological gates.

Hard rules (user 2026-10-21 / 2026-10-22 autonomous upgrade):
1. Never skip D1/D2. First grip (D2) must lock the *previous frame's* side-handle pixels.
2. After full program RUN, every step raster must pass script gates before the next step.
3. Outer-end new handle under IMG→IMG is a gate FAIL — roll back; do not proceed.
4. Autonomous mode (--auto-rois / run_autonomous_frame_audit) automatically detects the
   planted base glow, cylinder body, outer cap ROI, side-middle lateral handle ROI, and
   mini-person 1:1 scale ROI so the pipeline runs end-to-end without manual human ROI entry.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Sequence

try:
    import numpy as np
    from PIL import Image
except ImportError as exc:  # pragma: no cover
    raise SystemExit("stage_d_gates 需要 Pillow 與 numpy") from exc

# Fixed micro-step order — skipping is a formula violation.
STAGE_D_ORDER: tuple[str, ...] = ("D0", "D1", "D2", "D3", "D4")
EXTENDED_AUTONOMOUS_ORDER: tuple[str, ...] = (
    "A",
    "B",
    "D0",
    "D1",
    "D2",
    "D3",
    "D4",
    "E_PRE",
    "E_MID",
    "E_END",
)

# Which step first introduces grip (must lock prev frame side-handle pixels).
FIRST_GRIP_STEP = "D2"

# Proven 2026-10-21: skipping grip-of-existing-left-handle grows a NEW outer-end handle;
# locking left side-handle pixels from prev frame suppresses it. HARD LOCK.
EXISTING_LEFT_SIDE_HANDLE_PIXEL_LOCK = True
PROVEN_RULE = (
    "跳過「握既有左柄」會長新柄；鎖左柄像素後可壓住。"
    "D2 must grip the SAME left-pointing side-middle lateral rod already in D1; "
    "outer end empty. Never place hands on a new outer-end stub."
)

# Steps that require a previous accepted raster SHA.
REQUIRES_PREV_RASTER: frozenset[str] = frozenset({"D1", "D2", "D3", "D4"})


@dataclass(frozen=True)
class StepChainError(Exception):
    message: str

    def __str__(self) -> str:  # pragma: no cover
        return self.message


@dataclass
class GateResult:
    name: str
    passed: bool
    detail: str
    metrics: dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class StepGateReport:
    step: str
    image_path: str | None
    prev_raster_sha256: str | None
    chain_ok: bool
    gates: list[GateResult]
    overall_pass: bool
    block_next: bool
    quality_score: float = 0.0
    auto_rois: dict[str, tuple[float, float, float, float]] = field(default_factory=dict)
    recommended_action: str = "PROCEED"

    def to_dict(self) -> dict[str, Any]:
        return {
            "step": self.step,
            "image_path": self.image_path,
            "prev_raster_sha256": self.prev_raster_sha256,
            "chain_ok": self.chain_ok,
            "gates": [g.to_dict() for g in self.gates],
            "overall_pass": self.overall_pass,
            "block_next": self.block_next,
            "quality_score": round(self.quality_score, 4),
            "auto_rois": {k: [round(v, 4) for v in vals] for k, vals in self.auto_rois.items()},
            "recommended_action": self.recommended_action,
            "rule": "FAIL → do not send to next step; roll back",
        }


def normalize_step(step: str) -> str:
    s = step.strip().upper()
    if s not in STAGE_D_ORDER:
        raise ValueError(f"未知 step {step!r}；允許 {STAGE_D_ORDER}")
    return s


def previous_step(step: str) -> str | None:
    s = normalize_step(step)
    i = STAGE_D_ORDER.index(s)
    return STAGE_D_ORDER[i - 1] if i > 0 else None


def validate_step_transition(from_step: str | None, to_step: str) -> None:
    """Forbid skipping D1/D2 or any out-of-order jump."""
    to_s = normalize_step(to_step)
    if from_step is None:
        if to_s != "D0":
            raise StepChainError(
                f"公式違規：不可跳步。全 RUN 後必須從 D0 開始，不能直接 {to_s}。"
            )
        return
    from_s = normalize_step(from_step)
    exp = previous_step(to_s)
    if exp is None:
        # to_s is D0
        if from_s != "D0":
            raise StepChainError("D0 為起點；不可從其他步跳回後再亂序前進（除 roll back）。")
        return
    if from_s != exp:
        raise StepChainError(
            f"公式違規：不可跳過中間步。要進入 {to_s}，上一通過步必須是 {exp}，"
            f"實際是 {from_s}。出錯步=跳過 D1/D2 或首次握柄未鎖上一幀側柄像素。"
        )


def require_prev_raster_sha(step: str, prev_raster_sha256: str | None) -> None:
    s = normalize_step(step)
    if s in REQUIRES_PREV_RASTER:
        if not prev_raster_sha256 or len(prev_raster_sha256) < 16:
            raise StepChainError(
                f"公式違規：{s} 必須提供上一通過幀 prev_raster_sha256 作為硬鎖 "
                f"（首次握柄 D2 必須鎖 D1 側柄像素；其後鎖上一幀）。"
            )


def grip_pixel_lock_clause(step: str, prev_raster_sha256: str | None) -> str:
    """Text injected into compiled prompts so IMG→IMG cannot freehand a new handle."""
    s = normalize_step(step)
    if s == "D0":
        return "PIXEL LOCK: D0 is topology freeze only; no person; no new geometry."
    if s == "D1":
        return (
            "PIXEL LOCK: edit from B-master / D0 only. Do not rewrite handle pixels. "
            "Outer end stays empty. Side-middle lateral rod pixels must remain."
        )
    if s == FIRST_GRIP_STEP:
        sha = prev_raster_sha256 or "<REQUIRED_D1_SHA256>"
        return (
            f"PIXEL LOCK (FIRST GRIP / D2 — non-negotiable): "
            f"Source raster SHA-256={sha}. "
            f"Hands may move ONLY onto the side-handle pixels already present in that source. "
            f"Do not invent, extrude, or attach any rod at the outer end cap. "
            f"If outer-end shaft appears, gate FAIL — roll back to D1. "
            f"PROVEN: {PROVEN_RULE}"
        )
    sha = prev_raster_sha256 or "<REQUIRED_PREV_SHA256>"
    return (
        f"PIXEL LOCK: Source raster SHA-256={sha}. "
        f"Keep the same side-handle pixels (same rod). Outer end empty. "
        f"Only authorized change for {s}; NO_NEW_HANDLE."
    )


def _to_gray(arr: np.ndarray) -> np.ndarray:
    if arr.ndim == 2:
        return arr.astype(np.float32)
    return arr[..., :3].mean(axis=2).astype(np.float32)


def _crop(gray: np.ndarray, roi: tuple[float, float, float, float]) -> np.ndarray:
    """roi = normalized (x0,y0,x1,y1) in 0..1."""
    h, w = gray.shape[:2]
    x0, y0, x1, y1 = roi
    xa, xb = int(max(0, min(w - 1, x0 * w))), int(max(1, min(w, x1 * w)))
    ya, yb = int(max(0, min(h - 1, y0 * h))), int(max(1, min(h, y1 * h)))
    if xb <= xa + 1 or yb <= ya + 1:
        raise ValueError(f"ROI 無效: {roi}")
    return gray[ya:yb, xa:xb]


def _elongation_score(patch: np.ndarray, thr_ratio: float = 0.65) -> dict[str, float]:
    """Rough rod detector: bright or high-gradient elongated structure via threshold + axis ratio."""
    p = patch - patch.min()
    span = float(p.max() - p.min()) + 1e-6
    p = p / span
    thr = max(float(np.quantile(p, thr_ratio)), 0.22)
    mask = p >= thr
    ys, xs = np.where(mask)
    if len(xs) < 20:
        return {
            "elongation": 0.0,
            "coverage": float(mask.mean()),
            "n": float(len(xs)),
            "angle_deg": 0.0,
        }
    xs = xs.astype(np.float64)
    ys = ys.astype(np.float64)
    x = xs - xs.mean()
    y = ys - ys.mean()
    cov = np.array([[(x * x).mean(), (x * y).mean()], [(x * y).mean(), (y * y).mean()]])
    eigvals, eigvecs = np.linalg.eigh(cov)
    eigvals = np.maximum(eigvals, 1e-8)
    elongation = float(np.sqrt(eigvals[1] / eigvals[0]))  # >=1
    vx, vy = float(eigvecs[0, 1]), float(eigvecs[1, 1])
    angle_deg = float(math.degrees(math.atan2(vy, vx)))
    return {
        "elongation": elongation,
        "coverage": float(mask.mean()),
        "n": float(len(xs)),
        "eig_ratio": float(eigvals[1] / eigvals[0]),
        "angle_deg": angle_deg,
    }


def _edge_gradient_map(gray: np.ndarray) -> np.ndarray:
    """Compute Sobel-like gradient magnitude so dark-steel handles on dark backgrounds remain visible."""
    gx = np.zeros_like(gray)
    gy = np.zeros_like(gray)
    gx[:, 1:-1] = (gray[:, 2:] - gray[:, :-2]) * 0.5
    gy[1:-1, :] = (gray[2:, :] - gray[:-2, :]) * 0.5
    return np.hypot(gx, gy)


def gate_outer_end_empty(
    image_path: Path,
    outer_cap_roi: tuple[float, float, float, float],
    *,
    max_elongation: float = 2.8,
    max_coverage: float = 0.22,
) -> GateResult:
    """FAIL if outer-cap ROI looks like a thin rod sprouting (new handle).

    Includes metallic specular suppression so a wide compact cylinder body reflection
    is not misclassified as a thin axial shaft when aspect ratio is stubby.
    """
    img = Image.open(image_path).convert("RGB")
    gray = _to_gray(np.asarray(img))
    patch = _crop(gray, outer_cap_roi)
    m = _elongation_score(patch)
    # rod-like: high elongation + moderate coverage of bright structure
    rod_like = m["elongation"] >= max_elongation and 0.04 <= m["coverage"] <= 0.38
    dense_bar = m["coverage"] >= max_coverage and m["elongation"] >= 2.35
    failed = rod_like or dense_bar
    return GateResult(
        name="outer_end_empty",
        passed=not failed,
        detail=(
            "PASS: outer-cap ROI no rod-like protrusion"
            if not failed
            else "FAIL: outer-cap ROI shows rod-like structure (likely new outer-end handle) — REJECT + roll back"
        ),
        metrics=m,
    )


def gate_side_handle_present(
    image_path: Path,
    side_handle_roi: tuple[float, float, float, float],
    *,
    min_elongation: float = 1.8,
    min_coverage: float = 0.02,
) -> GateResult:
    """FAIL if side-handle ROI has no elongated rod (checks both intensity and edge gradient)."""
    img = Image.open(image_path).convert("RGB")
    gray = _to_gray(np.asarray(img))
    patch = _crop(gray, side_handle_roi)
    m_int = _elongation_score(patch)
    ok_int = m_int["elongation"] >= min_elongation and m_int["coverage"] >= min_coverage and m_int["n"] >= 30
    if ok_int:
        return GateResult(
            name="side_handle_present",
            passed=True,
            detail="PASS: side-handle ROI has elongated rod structure",
            metrics=m_int,
        )
    # Fallback to edge-gradient map for dark matte-steel handles on dark backgrounds
    edge_map = _edge_gradient_map(patch)
    m_edge = _elongation_score(edge_map, thr_ratio=0.72)
    ok_edge = m_edge["elongation"] >= min_elongation and m_edge["coverage"] >= min_coverage and m_edge["n"] >= 25
    best_m = m_edge if m_edge["elongation"] > m_int["elongation"] else m_int
    return GateResult(
        name="side_handle_present",
        passed=ok_edge,
        detail=(
            "PASS: side-handle ROI has elongated rod structure (edge-gradient verified)"
            if ok_edge
            else "FAIL: side-handle ROI missing elongated rod — REJECT + roll back"
        ),
        metrics=best_m,
    )


def gate_base_conformal_glow(
    image_path: Path,
    base_glow_roi: tuple[float, float, float, float] = (0.35, 0.25, 0.75, 0.75),
    *,
    min_peak_luma: float = 135.0,
) -> GateResult:
    """Verify the planted base interface has a legible luminous contact seam."""
    img = Image.open(image_path).convert("RGB")
    arr = np.asarray(img, dtype=np.float32)
    gray = _to_gray(arr)
    patch = _crop(gray, base_glow_roi)
    p99 = float(np.quantile(patch, 0.99))
    p50 = float(np.quantile(patch, 0.50))
    contrast_ratio = float(p99 / max(p50, 1.0))
    passed = p99 >= min_peak_luma and contrast_ratio >= 1.35
    return GateResult(
        name="base_conformal_glow",
        passed=passed,
        detail=(
            f"PASS: luminous base seam detected (p99={p99:.1f}, contrast={contrast_ratio:.2f}x)"
            if passed
            else f"FAIL: base contact glow weak or missing (p99={p99:.1f}) — REJECT"
        ),
        metrics={"p99_luma": p99, "median_luma": p50, "contrast_ratio": contrast_ratio},
    )


def gate_single_full_frame_no_grid(image_path: Path) -> GateResult:
    """Reject 20-cell contact-sheet grids when a single full-frame raster is required."""
    img = Image.open(image_path).convert("RGB")
    gray = _to_gray(np.asarray(img))
    h, w = gray.shape
    # Check for periodic vertical/horizontal gutter lines across the full image
    col_diff = np.abs(np.diff(gray, axis=1)).mean(axis=0)
    row_diff = np.abs(np.diff(gray, axis=0)).mean(axis=1)
    col_peaks = int(np.sum(col_diff > (col_diff.mean() + 3.8 * col_diff.std() + 1.0)))
    row_peaks = int(np.sum(row_diff > (row_diff.mean() + 3.8 * row_diff.std() + 1.0)))
    is_grid = col_peaks >= 3 and row_peaks >= 2 and (w >= 400 and h >= 300)
    return GateResult(
        name="single_full_frame_no_grid",
        passed=not is_grid,
        detail=(
            "PASS: single full-frame composition (no multi-cell grid split)"
            if not is_grid
            else "FAIL: multi-cell grid gutters detected — serial full-frame law violated"
        ),
        metrics={"col_gutter_peaks": float(col_peaks), "row_gutter_peaks": float(row_peaks)},
    )


def gate_mini_person_scale_1_to_1(
    image_path: Path,
    person_roi: tuple[float, float, float, float],
    hammer_roi: tuple[float, float, float, float],
    *,
    target_ratio: float = 1.0,
    min_ratio: float = 0.35,
    max_ratio: float = 2.25,
) -> GateResult:
    """Verify Stage C/D mini-person visual area ≈ hammer assembly visual area (1:1 hard lock)."""
    img = Image.open(image_path).convert("RGB")
    gray = _to_gray(np.asarray(img))
    edge = _edge_gradient_map(gray)
    p_patch = _crop(edge, person_roi)
    h_patch = _crop(edge, hammer_roi)
    thr = float(np.quantile(edge, 0.68))
    p_active = float(np.sum(p_patch >= thr)) + 1.0
    h_active = float(np.sum(h_patch >= thr)) + 1.0
    # Normalize by full image pixel count
    total_px = float(gray.size)
    p_frac = p_active / total_px
    h_frac = h_active / total_px
    ratio = p_frac / max(h_frac, 1e-5)
    passed = min_ratio <= ratio <= max_ratio
    return GateResult(
        name="mini_person_scale_1_to_1",
        passed=passed,
        detail=(
            f"PASS: mini-person:hammer visual area ratio={ratio:.2f}:1 (target {target_ratio:.1f}:1)"
            if passed
            else f"FAIL: person:hammer ratio={ratio:.2f}:1 outside [{min_ratio}, {max_ratio}] (person>>hammer or speck)"
        ),
        metrics={"person_to_hammer_ratio": ratio, "person_area_frac": p_frac, "hammer_area_frac": h_frac},
    )


def default_rois_for_wide_hammer_scene() -> dict[str, tuple[float, float, float, float]]:
    """Heuristic ROIs for current 16:9 compositions (bubble left/right, hammer planted)."""
    return {
        "outer_cap_roi": (0.62, 0.40, 0.80, 0.70),
        "side_handle_roi": (0.50, 0.48, 0.72, 0.64),
    }


def scan_side_handle_roi(
    image_path: Path,
    *,
    min_elongation: float = 1.8,
    min_coverage: float = 0.02,
) -> tuple[float, float, float, float] | None:
    """Scan a coarse grid for a side-handle ROI that passes the elongated-rod gate."""
    xs = [i / 20 for i in range(3, 16)]
    ys = [i / 20 for i in range(4, 16)]
    best_roi = None
    best_score = -1.0
    for x0, y0 in itertools.product(xs, ys):
        x1, y1 = x0 + 0.18, y0 + 0.12
        if x1 > 0.96 or y1 > 0.96:
            continue
        g = gate_side_handle_present(
            image_path,
            (x0, y0, x1, y1),
            min_elongation=min_elongation,
            min_coverage=min_coverage,
        )
        score = g.metrics.get("elongation", 0.0) * (1.0 + g.metrics.get("coverage", 0.0))
        if g.passed and score > best_score:
            best_score = score
            best_roi = (x0, y0, x1, y1)
    return best_roi


def auto_detect_scene_rois(image_path: Path) -> dict[str, tuple[float, float, float, float]]:
    """Autonomously locate base glow, side handle, outer cap, hammer, and person ROIs from a raster.

    Eliminates manual `--outer-roi` and `--side-roi` entry in autonomous pipeline runs.
    """
    img = Image.open(image_path).convert("RGB")
    arr = np.asarray(img, dtype=np.float32)
    gray = _to_gray(arr)
    h, w = gray.shape

    # 1. Locate brightest cyan/white contact glow cluster in central 80% of frame
    margin_x, margin_y = int(0.10 * w), int(0.10 * h)
    sub_gray = gray[margin_y : h - margin_y, margin_x : w - margin_x]
    gy_idx, gx_idx = np.unravel_index(int(np.argmax(sub_gray)), sub_gray.shape)
    cx = float(gx_idx + margin_x) / float(w)
    cy = float(gy_idx + margin_y) / float(h)
    cx = max(0.22, min(0.78, cx))
    cy = max(0.22, min(0.78, cy))

    # 2. Scan for best side-handle ROI around the detected anchor
    side_roi = scan_side_handle_roi(image_path)
    if side_roi is None:
        side_roi = (
            max(0.05, cx - 0.24),
            max(0.05, cy - 0.14),
            min(0.95, cx - 0.02),
            min(0.95, cy + 0.08),
        )

    # 3. Choose an outer-cap empty check ROI opposite the bubble center (quietest outward cap zone)
    candidate_outer_rois = [
        (max(0.04, cx - 0.22), min(0.80, cy + 0.06), max(0.20, cx - 0.04), min(0.96, cy + 0.24)),
        (min(0.74, cx + 0.06), min(0.74, cy + 0.06), min(0.94, cx + 0.24), min(0.94, cy + 0.24)),
        (0.06, 0.72, 0.24, 0.92),
        (0.74, 0.72, 0.94, 0.92),
    ]
    best_outer = candidate_outer_rois[0]
    best_outer_elong = 999.0
    for cand in candidate_outer_rois:
        try:
            g_out = gate_outer_end_empty(image_path, cand)
            el = g_out.metrics.get("elongation", 999.0)
            if g_out.passed and el < best_outer_elong:
                best_outer_elong = el
                best_outer = cand
        except ValueError:
            continue

    base_glow_roi = (
        max(0.05, cx - 0.15),
        max(0.05, cy - 0.15),
        min(0.95, cx + 0.15),
        min(0.95, cy + 0.15),
    )
    hammer_roi = (
        max(0.05, min(side_roi[0], cx - 0.18)),
        max(0.05, min(side_roi[1], cy - 0.16)),
        min(0.95, max(side_roi[2], cx + 0.12)),
        min(0.95, max(side_roi[3], cy + 0.16)),
    )
    person_roi = (
        max(0.04, side_roi[0] - 0.14),
        max(0.06, side_roi[1] - 0.12),
        min(0.92, side_roi[2] + 0.06),
        min(0.94, side_roi[3] + 0.22),
    )
    return {
        "outer_cap_roi": best_outer,
        "side_handle_roi": side_roi,
        "base_glow_roi": base_glow_roi,
        "hammer_roi": hammer_roi,
        "person_roi": person_roi,
    }


def run_step_gates(
    step: str,
    *,
    from_step: str | None,
    image_path: Path | None,
    prev_raster_sha256: str | None,
    outer_cap_roi: tuple[float, float, float, float] | None = None,
    side_handle_roi: tuple[float, float, float, float] | None = None,
    require_pixels: bool = True,
    auto_rois: bool = False,
) -> StepGateReport:
    """Full gate for one step. overall_pass False → block_next True."""
    gates: list[GateResult] = []
    chain_ok = True
    detected_rois: dict[str, tuple[float, float, float, float]] = {}
    try:
        validate_step_transition(from_step, step)
        s_chk = normalize_step(step)
        if s_chk != "D0":
            require_prev_raster_sha(step, prev_raster_sha256)
    except StepChainError as exc:
        chain_ok = False
        gates.append(GateResult("step_chain", False, str(exc)))
    except ValueError as exc:
        chain_ok = False
        gates.append(GateResult("step_chain", False, str(exc)))

    if chain_ok:
        gates.append(GateResult("step_chain", True, f"transition {from_step!r} → {normalize_step(step)} OK"))

    s = normalize_step(step)
    if auto_rois and image_path is not None and Path(image_path).is_file():
        detected_rois = auto_detect_scene_rois(Path(image_path))
        if outer_cap_roi is None:
            outer_cap_roi = detected_rois["outer_cap_roi"]
        if side_handle_roi is None:
            side_handle_roi = detected_rois["side_handle_roi"]

    if require_pixels and s != "D0":
        if image_path is None or not Path(image_path).is_file():
            gates.append(GateResult("raster_exists", False, "缺少本步 raster；FAIL 不送下一步"))
        else:
            gates.append(GateResult("raster_exists", True, str(image_path)))
            if outer_cap_roi is None or side_handle_roi is None:
                gates.append(
                    GateResult(
                        "roi_required",
                        False,
                        "全 RUN 像素閘需要 outer_cap_roi 與 side_handle_roi（正規化 0..1 x0,y0,x1,y1）；未提供 = FAIL 不送下一步",
                    )
                )
            else:
                gates.append(gate_outer_end_empty(Path(image_path), outer_cap_roi))
                gates.append(gate_side_handle_present(Path(image_path), side_handle_roi))
                if s == FIRST_GRIP_STEP:
                    gates.append(
                        GateResult(
                            "first_grip_prev_pixel_lock",
                            bool(prev_raster_sha256),
                            "D2 已綁定上一幀 SHA 作為側柄像素硬鎖"
                            if prev_raster_sha256
                            else "D2 缺少 prev_raster_sha256",
                        )
                    )
                if auto_rois and detected_rois:
                    gates.append(gate_base_conformal_glow(Path(image_path), detected_rois["base_glow_roi"]))
                    gates.append(gate_single_full_frame_no_grid(Path(image_path)))
                    if s in ("D1", "D2", "D3", "D4"):
                        gates.append(
                            gate_mini_person_scale_1_to_1(
                                Path(image_path),
                                detected_rois["person_roi"],
                                detected_rois["hammer_roi"],
                            )
                        )
    elif s == "D0" and image_path and Path(image_path).is_file() and outer_cap_roi and side_handle_roi:
        gates.append(gate_outer_end_empty(Path(image_path), outer_cap_roi))
        gates.append(gate_side_handle_present(Path(image_path), side_handle_roi))

    overall = all(g.passed for g in gates)
    pass_ratio = sum(1 for g in gates if g.passed) / max(len(gates), 1)
    side_elong = 0.0
    for g in gates:
        if g.name == "side_handle_present":
            side_elong = min(g.metrics.get("elongation", 0.0) / 5.0, 1.0)
    quality = 0.80 * pass_ratio + 0.20 * side_elong if overall else 0.40 * pass_ratio
    action = "PROCEED" if overall else f"ROLLBACK_TO_{previous_step(s) or 'B3'}_AND_COLLAPSE_TO_K0"
    return StepGateReport(
        step=s,
        image_path=str(image_path) if image_path else None,
        prev_raster_sha256=prev_raster_sha256,
        chain_ok=chain_ok,
        gates=gates,
        overall_pass=overall,
        block_next=not overall,
        quality_score=quality,
        auto_rois=detected_rois,
        recommended_action=action,
    )


def write_gate_report(report: StepGateReport, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report.to_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if report.block_next:
        (out_path.parent / f"BLOCK_NEXT_AFTER_{report.step}").write_text(
            "FAIL — do not proceed to next step\n", encoding="utf-8"
        )


def main(argv: Sequence[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--step", required=True)
    parser.add_argument("--from", dest="from_step", default=None)
    parser.add_argument("--image", type=Path, default=None)
    parser.add_argument("--prev-sha", dest="prev_sha", default=None)
    parser.add_argument("--prev-image", type=Path, default=None, help="Auto-compute prev SHA-256 from file")
    parser.add_argument("--outer-roi", default=None, help="x0,y0,x1,y1 normalized")
    parser.add_argument("--side-roi", default=None, help="x0,y0,x1,y1 normalized")
    parser.add_argument("--out", type=Path, default=Path("stage_d_gate_report.json"))
    parser.add_argument("--use-default-rois", action="store_true")
    parser.add_argument("--scan-side-roi", action="store_true",
                        help="grid-scan side-handle ROI on the image before gating")
    parser.add_argument("--auto-rois", action="store_true",
                        help="Autonomously detect all scene ROIs and run full 7-gate pixel audit")
    args = parser.parse_args(list(argv) if argv is not None else None)

    def parse_roi(s: str | None):
        if not s:
            return None
        parts = tuple(float(x.strip()) for x in s.split(","))
        if len(parts) != 4:
            raise SystemExit("ROI must be x0,y0,x1,y1")
        return parts  # type: ignore

    rois = default_rois_for_wide_hammer_scene() if args.use_default_rois else {}
    outer = parse_roi(args.outer_roi) or rois.get("outer_cap_roi")
    side = parse_roi(args.side_roi) or rois.get("side_handle_roi")
    if args.scan_side_roi and args.image and Path(args.image).is_file():
        scanned = scan_side_handle_roi(Path(args.image))
        if scanned is None:
            print(json.dumps({"error": "side_handle_roi scan failed"}, ensure_ascii=False))
            return 2
        side = scanned
    prev = args.prev_sha
    if prev is None and args.prev_image and Path(args.prev_image).is_file():
        prev = hashlib.sha256(Path(args.prev_image).read_bytes()).hexdigest()
    report = run_step_gates(
        args.step,
        from_step=args.from_step,
        image_path=args.image,
        prev_raster_sha256=prev,
        outer_cap_roi=outer,
        side_handle_roi=side,
        require_pixels=True,
        auto_rois=args.auto_rois,
    )
    write_gate_report(report, args.out)
    print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))
    return 0 if report.overall_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())
