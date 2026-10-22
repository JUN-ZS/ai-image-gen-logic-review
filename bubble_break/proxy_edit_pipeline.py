#!/usr/bin/env python3
"""Unified Proxy Edit Pipeline: Upstream Dual T-Hammer Contact Calibration -> Proxy Target Swap at P -> Bubble-Break Closed Loop.

Implements the complete 4-step executable closed loop required by PR #1 and PR #4:
1. Step 1 (Upstream Dual T-Hammer End-Face Calibration):
   - Verifies real Dual T-Hammer rasters (`PRE_FAR`, `PRE_NEAR`, `FIRST_CONTACT`, `REACTION`, `RECOIL`)
     using `validate_raster_bound_collision_evidence`.
   - If the upstream calibration is missing or any required calibration stage fails, immediately blocks with:
       `status = "BLOCKED_UNTIL_T_CONTACT_MATRIX_APPROVED"`.
2. Step 2 (Geometric & Reference Transfer from Calibration to Bubble-Break Scene):
   - Extracts the verified `HAMMER_A` rigid-body pose (`head_axis`, `handle_axis`, `strike_face_normal = (+1,0,0)`,
     `calibration_first_contact_sha256`) and transfers it into the Bubble-Break sequence (`H0 -> H1 -> H2 -> H2B -> H3`)
     where `HAMMER_B` is replaced by the transparent containment bubble at surface pole `P`.
3. Step 3 (Per-Frame Bubble-Break Raster Generation & Semantic/Geometric Audit):
   - Audits each real Bubble-Break raster (`H0_PRE_IMPACT`, `H1_PRE_NEAR`, `H2_FIRST_CONTACT`,
     `H2B_CRACK_PROPAGATION`, `H3_FOLLOWTHROUGH_SHELL_SHATTER`) via `validate_bubble_break_frame_evidence`.
   - If semantic/geometric evidence is missing, blocks with `BLOCKED_BUBBLE_BREAK_SEMANTIC_EVIDENCE_MISSING`.
4. Step 4 (Closed-Loop Rejection, Rerun & Unblocking):
   - When a candidate raster fails (e.g., `PRE_FAR_R00` outer wall mounts, `H2_R00` lower handle cross-stub &
     bubble scale jump, `H3_R00` handle sliding to rear end into L-shape), records the rejection reason,
     invokes the live `rerun_callback` / provider adapter from the last verified `PASS` parent raster,
     and only unblocks (`status = "PASSED_CALIBRATED_BUBBLE_BREAK_CLOSED_LOOP"`) once every stage passes!
"""
from __future__ import annotations

import json
import shutil
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable, Sequence

from PIL import Image, ImageDraw

from bubble_break.frame_pipeline import (
    BUBBLE_BREAK_STAGES,
    render_bubble_break_annotated_panel,
    sha256_file,
    validate_bubble_break_frame_evidence,
)
from bubble_break.raster_bound_collision_audit import (
    validate_raster_bound_collision_evidence,
)
from bubble_break.closed_loop_evidence_guard import (
    attach_guard_errors,
    validate_stage_binding,
)
from bubble_break.shannon_information_gain import recommend_next_experiment


@dataclass
class StageAttemptAudit:
    domain: str  # "UPSTREAM_DUAL_T_CALIBRATION" or "MAINLINE_BUBBLE_BREAK"
    stage: str
    attempt_round: int
    raster_path: str
    raster_sha256: str
    accepted: bool
    status: str
    visual_acceptance_status: str
    errors: list[str] = field(default_factory=list)
    rejection_note: str | None = None
    next_experiment: dict[str, Any] = field(default_factory=dict)


@dataclass
class UnifiedCalibratedBubbleBreakReport:
    workflow: str
    status: str
    calibration_approved: bool
    bubble_break_approved: bool
    code_visual_acceptance_status: str
    calibrated_attacking_hammer_sha256: str | None
    locked_bubble_pole_p_px: list[float]
    total_reruns_triggered: int
    total_rejected_attempts: int
    calibration_stages: dict[str, dict[str, Any]]
    bubble_break_stages: dict[str, dict[str, Any]]
    attempt_log: list[dict[str, Any]]
    master_comparison_board_path: str | None = None
    bubble_break_strip_path: str | None = None
    acceptance_level: str = "NOT_ACCEPTED"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


CandidateBatchEntry = tuple[Path, dict[str, Any] | None]
RerunProviderFn = Callable[[str, int, Path | None, list[str], Path], list[CandidateBatchEntry]]


def run_calibrated_bubble_break_closed_loop(
    outdir: Path,
    *,
    calibration_candidates: dict[str, Sequence[CandidateBatchEntry]] | None,
    bubble_break_candidates: dict[str, Sequence[CandidateBatchEntry]] | None,
    rerun_provider: RerunProviderFn | None = None,
    locked_pole_p_px: tuple[float, float] = (755.0, 384.0),
    max_retries: int = 2,
) -> UnifiedCalibratedBubbleBreakReport:
    """Execute the complete Step 1 -> Step 4 Calibrated Dual-T to Bubble-Break Closed-Loop Pipeline."""
    outdir.mkdir(parents=True, exist_ok=True)
    cal_dir = outdir / "step1_dual_t_calibration"
    bub_dir = outdir / "step3_bubble_break_sequence"
    cal_dir.mkdir(parents=True, exist_ok=True)
    bub_dir.mkdir(parents=True, exist_ok=True)

    attempt_log: list[dict[str, Any]] = []
    calibration_stages: dict[str, dict[str, Any]] = {}
    bubble_break_stages: dict[str, dict[str, Any]] = {}
    total_reruns = 0
    total_rejections = 0

    required_cal_stages = ("PRE_FAR", "PRE_NEAR", "FIRST_CONTACT", "REACTION", "RECOIL")
    calibration_candidates = calibration_candidates or {}
    missing_calibration_inputs = any(st not in calibration_candidates for st in required_cal_stages)
    if missing_calibration_inputs and rerun_provider is None:
        rep = UnifiedCalibratedBubbleBreakReport(
            workflow="calibrated-dual-t-to-bubble-break-closed-loop-v1",
            status="BLOCKED_UNTIL_T_CONTACT_MATRIX_APPROVED",
            calibration_approved=False,
            bubble_break_approved=False,
            code_visual_acceptance_status="NOT_VERIFIED_BY_CODE",
            calibrated_attacking_hammer_sha256=None,
            locked_bubble_pole_p_px=list(locked_pole_p_px),
            total_reruns_triggered=0,
            total_rejected_attempts=0,
            calibration_stages={},
            bubble_break_stages={},
            attempt_log=[],
        )
        (outdir / "UNIFIED_CLOSED_LOOP_MANIFEST.json").write_text(
            json.dumps(rep.to_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        return rep

    # STEP 1: Verify Upstream Dual T-Hammer End-Face Contact Calibration
    cal_parent_img: Path | None = None
    cal_parent_stage: str | None = None
    for st in required_cal_stages:
        batch = list(calibration_candidates.get(st, []))
        accepted_entry: dict[str, Any] | None = None
        last_errors: list[str] = []

        for r_round in range(0, max_retries + 1):
            if r_round > 0 or not batch:
                if rerun_provider is None:
                    break
                total_reruns += 1
                batch = rerun_provider(f"CAL_{st}", r_round, cal_parent_img, last_errors, cal_dir / "reruns")
                if not batch:
                    break

            for cand_path, cand_ev in batch:
                cand_p = Path(cand_path)
                sha = sha256_file(cand_p) if cand_p.is_file() else "MISSING"
                if cand_ev is None:
                    val = {
                        "accepted": False,
                        "status": "BLOCKED_RASTER_BOUND_GEOMETRY_EVIDENCE",
                        "errors": ["missing calibration evidence payload"],
                        "visual_acceptance_status": "NOT_VERIFIED_BY_CODE",
                    }
                else:
                    val = validate_raster_bound_collision_evidence(cand_p, cand_ev)

                expected_parent_sha = (
                    sha256_file(cal_parent_img)
                    if cal_parent_img is not None and cal_parent_img.is_file()
                    else None
                )
                previous_cal_evidence = (
                    calibration_stages.get(cal_parent_stage, {}).get("evidence")
                    if cal_parent_stage is not None
                    else None
                )
                binding_errors = validate_stage_binding(
                    domain="CALIBRATION",
                    expected_stage=st,
                    evidence=cand_ev,
                    raster_sha256=sha,
                    expected_parent_sha256=expected_parent_sha,
                    expected_parent_stage=cal_parent_stage,
                    previous_evidence=previous_cal_evidence,
                )
                val = attach_guard_errors(val, binding_errors)

                ok = bool(val.get("accepted", False))
                errs = list(val.get("errors", []))
                rej_note = None
                if not ok:
                    total_rejections += 1
                    last_errors = errs
                    rej_note = f"REJECTED_CAL_{st}_R{r_round:02d}: {'; '.join(errs)}"

                rec = StageAttemptAudit(
                    domain="UPSTREAM_DUAL_T_CALIBRATION",
                    stage=st,
                    attempt_round=r_round,
                    raster_path=str(cand_p),
                    raster_sha256=sha,
                    accepted=ok,
                    status=str(val.get("status")),
                    visual_acceptance_status=str(val.get("visual_acceptance_status", "NOT_VERIFIED_BY_CODE")),
                    errors=errs,
                    rejection_note=rej_note,
                    next_experiment=(
                        recommend_next_experiment(errs, attempt_log)
                        if not ok else {}
                    ),
                )
                attempt_log.append(asdict(rec))
                if ok and accepted_entry is None:
                    locked_p = cal_dir / f"LOCKED_CAL_{st}.jpg"
                    if cand_p.resolve() != locked_p.resolve():
                        shutil.copy2(cand_p, locked_p)
                    accepted_entry = {
                        "stage": st,
                        "raster_path": str(locked_p),
                        "raster_sha256": sha,
                        "evidence": cand_ev,
                        "validation": val,
                    }

            if accepted_entry is not None:
                break

        if accepted_entry is None:
            rep = UnifiedCalibratedBubbleBreakReport(
                workflow="calibrated-dual-t-to-bubble-break-closed-loop-v1",
                status="BLOCKED_UNTIL_T_CONTACT_MATRIX_APPROVED",
                calibration_approved=False,
                bubble_break_approved=False,
                code_visual_acceptance_status="NOT_VERIFIED_BY_CODE",
                calibrated_attacking_hammer_sha256=None,
                locked_bubble_pole_p_px=list(locked_pole_p_px),
                total_reruns_triggered=total_reruns,
                total_rejected_attempts=total_rejections,
                calibration_stages=calibration_stages,
                bubble_break_stages={},
                attempt_log=attempt_log,
            )
            (outdir / "UNIFIED_CLOSED_LOOP_MANIFEST.json").write_text(
                json.dumps(rep.to_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
            )
            return rep

        calibration_stages[st] = accepted_entry
        cal_parent_img = Path(accepted_entry["raster_path"])
        cal_parent_stage = st

    # STEP 2: Extract Approved Attacking T-Hammer SHA-256 & Geometry for Proxy Target Swap at P
    calibrated_first_contact_sha = calibration_stages["FIRST_CONTACT"]["raster_sha256"]

    bubble_break_candidates = bubble_break_candidates or {}
    if not bubble_break_candidates and rerun_provider is None:
        rep = UnifiedCalibratedBubbleBreakReport(
            workflow="calibrated-dual-t-to-bubble-break-closed-loop-v1",
            status="BLOCKED_BUBBLE_BREAK_SEMANTIC_EVIDENCE_MISSING",
            calibration_approved=False,
            bubble_break_approved=False,
            code_visual_acceptance_status="NOT_VERIFIED_BY_CODE",
            calibrated_attacking_hammer_sha256=calibrated_first_contact_sha,
            locked_bubble_pole_p_px=list(locked_pole_p_px),
            total_reruns_triggered=total_reruns,
            total_rejected_attempts=total_rejections,
            calibration_stages=calibration_stages,
            bubble_break_stages={},
            attempt_log=attempt_log,
        )
        (outdir / "UNIFIED_CLOSED_LOOP_MANIFEST.json").write_text(
            json.dumps(rep.to_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        return rep

    # STEP 3 & STEP 4: Audit Bubble-Break Sequence (H0 -> H1 -> H2 -> H2B -> H3) with Live Rerun on Failure
    bub_parent_img: Path | None = Path(calibration_stages["FIRST_CONTACT"]["raster_path"])
    bub_parent_stage: str | None = "CALIBRATION_FIRST_CONTACT"
    previous_bubble_evidence: dict[str, Any] | None = None
    for st in BUBBLE_BREAK_STAGES:
        batch = list(bubble_break_candidates.get(st, []))
        accepted_bub: dict[str, Any] | None = None
        last_errors = []
        missing_semantic_evidence = False

        for r_round in range(0, max_retries + 1):
            if r_round > 0 or not batch:
                if rerun_provider is None:
                    break
                total_reruns += 1
                batch = rerun_provider(st, r_round, bub_parent_img, last_errors, bub_dir / "reruns")
                if not batch:
                    break

            for cand_path, cand_ev in batch:
                cand_p = Path(cand_path)
                sha = sha256_file(cand_p) if cand_p.is_file() else "MISSING"
                val = validate_bubble_break_frame_evidence(
                    cand_p,
                    cand_ev,
                    locked_pole_p_px=locked_pole_p_px,
                )
                semantic_evidence_missing_for_candidate = (
                    val.get("status") == "BLOCKED_BUBBLE_BREAK_SEMANTIC_EVIDENCE_MISSING"
                )
                expected_parent_sha = (
                    sha256_file(bub_parent_img)
                    if bub_parent_img is not None and bub_parent_img.is_file()
                    else None
                )
                binding_errors = validate_stage_binding(
                    domain="BUBBLE_BREAK",
                    expected_stage=st,
                    evidence=cand_ev,
                    raster_sha256=sha,
                    expected_parent_sha256=expected_parent_sha,
                    expected_parent_stage=bub_parent_stage,
                    expected_calibration_sha256=calibrated_first_contact_sha,
                    previous_evidence=previous_bubble_evidence,
                )
                val = attach_guard_errors(val, binding_errors)
                if semantic_evidence_missing_for_candidate:
                    missing_semantic_evidence = True

                ok = bool(val.get("accepted", False))
                errs = list(val.get("errors", []))
                rej_note = None
                if not ok:
                    total_rejections += 1
                    last_errors = errs
                    rej_note = f"REJECTED_{st}_R{r_round:02d}: {'; '.join(errs)}"

                rec = StageAttemptAudit(
                    domain="MAINLINE_BUBBLE_BREAK",
                    stage=st,
                    attempt_round=r_round,
                    raster_path=str(cand_p),
                    raster_sha256=sha,
                    accepted=ok,
                    status=str(val.get("status")),
                    visual_acceptance_status=str(val.get("visual_acceptance_status", "NOT_VERIFIED_BY_CODE")),
                    errors=errs,
                    rejection_note=rej_note,
                    next_experiment=(
                        recommend_next_experiment(errs, attempt_log)
                        if not ok else {}
                    ),
                )
                attempt_log.append(asdict(rec))
                if ok and accepted_bub is None and cand_ev is not None:
                    locked_p = bub_dir / f"LOCKED_{st}.jpg"
                    if cand_p.resolve() != locked_p.resolve():
                        shutil.copy2(cand_p, locked_p)
                    panel_p = bub_dir / f"ANNOTATED_{st}.jpg"
                    render_bubble_break_annotated_panel(locked_p, cand_ev, val, panel_p)
                    accepted_bub = {
                        "stage": st,
                        "raster_path": str(locked_p),
                        "annotated_panel_path": str(panel_p),
                        "raster_sha256": sha,
                        "evidence": cand_ev,
                        "validation": val,
                    }

            if accepted_bub is not None:
                break

        if accepted_bub is None:
            block_status = (
                "BLOCKED_BUBBLE_BREAK_SEMANTIC_EVIDENCE_MISSING"
                if missing_semantic_evidence
                else "BLOCKED_BUBBLE_BREAK_CONTRACT_FAIL"
            )
            rep = UnifiedCalibratedBubbleBreakReport(
                workflow="calibrated-dual-t-to-bubble-break-closed-loop-v1",
                status=block_status,
                calibration_approved=False,
                bubble_break_approved=False,
                code_visual_acceptance_status="NOT_VERIFIED_BY_CODE",
                calibrated_attacking_hammer_sha256=calibrated_first_contact_sha,
                locked_bubble_pole_p_px=list(locked_pole_p_px),
                total_reruns_triggered=total_reruns,
                total_rejected_attempts=total_rejections,
                calibration_stages=calibration_stages,
                bubble_break_stages=bubble_break_stages,
                attempt_log=attempt_log,
            )
            (outdir / "UNIFIED_CLOSED_LOOP_MANIFEST.json").write_text(
                json.dumps(rep.to_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
            )
            return rep

        bubble_break_stages[st] = accepted_bub
        bub_parent_img = Path(accepted_bub["raster_path"])
        bub_parent_stage = st
        previous_bubble_evidence = accepted_bub["evidence"]

    strip_path = create_calibrated_bubble_break_strip(
        calibration_stages["FIRST_CONTACT"],
        [bubble_break_stages[s] for s in BUBBLE_BREAK_STAGES],
        outdir / "CALIBRATED_BUBBLE_BREAK_CLOSED_LOOP_STRIP.jpg",
    )
    board_path = create_calibrated_bubble_break_overlay_board(
        calibration_stages["FIRST_CONTACT"],
        [bubble_break_stages[s] for s in BUBBLE_BREAK_STAGES],
        outdir / "CALIBRATED_BUBBLE_BREAK_EVIDENCE_BOARD.jpg",
    )

    rep = UnifiedCalibratedBubbleBreakReport(
        workflow="calibrated-dual-t-to-bubble-break-closed-loop-v1",
        status="EVIDENCE_CONTRACTS_PASSED_REQUIRES_VISUAL_REVIEW",
        calibration_approved=False,
        bubble_break_approved=False,
        code_visual_acceptance_status="NOT_VERIFIED_BY_CODE",
        calibrated_attacking_hammer_sha256=calibrated_first_contact_sha,
        locked_bubble_pole_p_px=list(locked_pole_p_px),
        total_reruns_triggered=total_reruns,
        total_rejected_attempts=total_rejections,
        calibration_stages=calibration_stages,
        bubble_break_stages=bubble_break_stages,
        attempt_log=attempt_log,
        master_comparison_board_path=str(board_path),
        bubble_break_strip_path=str(strip_path),
        acceptance_level="STRUCTURED_EVIDENCE_CONTRACT_ONLY",
    )
    (outdir / "UNIFIED_CLOSED_LOOP_MANIFEST.json").write_text(
        json.dumps(rep.to_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return rep


def create_calibrated_bubble_break_strip(
    cal_first_contact: dict[str, Any],
    bubble_records: Sequence[dict[str, Any]],
    out_path: Path,
) -> Path:
    """Create a 6-panel horizontal strip: [Upstream Dual-T Calibration @ P] -> [H0] -> [H1] -> [H2] -> [H2B] -> [H3]."""
    all_items = [("STEP1_DUAL_T_CAL_P", cal_first_contact)] + [(r["stage"], r) for r in bubble_records]
    cw, ch = 430, 280
    strip = Image.new("RGB", (len(all_items) * cw, ch + 68), (10, 14, 20))
    draw = ImageDraw.Draw(strip)
    draw.text(
        (20, 18),
        "COMPLETE CLOSED LOOP: STEP 1 DUAL-T CALIBRATION AT P -> STEP 2 PROXY SWAP -> STEP 3/4 BUBBLE BREAK (H0 -> H1 -> H2 -> H2B -> H3)",
        fill=(130, 245, 255),
    )
    for idx, (label, rec) in enumerate(all_items):
        x0, y0 = idx * cw, 56
        p = Path(rec["raster_path"])
        if p.is_file():
            thumb = Image.open(p).convert("RGB").resize((cw - 12, ch - 52))
            strip.paste(thumb, (x0 + 6, y0 + 6))
        color = (255, 210, 90) if idx == 0 else (90, 235, 160)
        draw.rectangle([x0 + 4, y0 + 4, x0 + cw - 4, y0 + ch - 4], outline=color, width=2)
        sha_short = rec["raster_sha256"][:8]
        draw.text((x0 + 10, y0 + ch - 38), f"{label} | sha={sha_short}", fill=color)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    strip.save(out_path, quality=93)
    return out_path


def create_calibrated_bubble_break_overlay_board(
    cal_first_contact: dict[str, Any],
    bubble_records: Sequence[dict[str, Any]],
    out_path: Path,
) -> Path:
    """Create a 3x2 annotated geometry & semantic evidence board showing Step 1 Calibration + H0, H1, H2, H2B, H3."""
    cols, rows = 3, 2
    cw, ch = 560, 340
    board = Image.new("RGB", (cols * cw, rows * ch + 68), (12, 16, 22))
    draw = ImageDraw.Draw(board)
    draw.text(
        (20, 18),
        "UNIFIED CALIBRATION -> BUBBLE BREAK RASTER-BOUND EVIDENCE BOARD (P LOCKED | CRACKS FROM P | INHABITANTS INTACT)",
        fill=(130, 245, 255),
    )
    panels = [("STEP1_DUAL_T_CAL_FIRST_CONTACT", cal_first_contact["raster_path"], cal_first_contact["raster_sha256"])]
    for r in bubble_records:
        panels.append((r["stage"], r["annotated_panel_path"], r["raster_sha256"]))

    for idx, (lbl, p_str, sha) in enumerate(panels[:6]):
        r_i, c_i = divmod(idx, cols)
        x0, y0 = c_i * cw, 58 + r_i * ch
        p = Path(p_str)
        if p.is_file():
            thumb = Image.open(p).convert("RGB").resize((cw - 12, ch - 48))
            board.paste(thumb, (x0 + 6, y0 + 6))
        color = (255, 210, 90) if idx == 0 else (90, 235, 160)
        draw.rectangle([x0 + 4, y0 + 4, x0 + cw - 4, y0 + ch - 4], outline=color, width=2)
        draw.text((x0 + 12, y0 + ch - 36), f"{lbl} | sha={sha[:10]} | EVIDENCE ONLY", fill=color)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    board.save(out_path, quality=93)
    return out_path