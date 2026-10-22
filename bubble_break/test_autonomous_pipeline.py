#!/usr/bin/env python3
"""Unit tests for v5 Canonical Spine + Cross-Frame Continuity Lock + 5-Keyframe Trilogy Engine."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from bubble_break.autonomous_pipeline import (
    AUTONOMOUS_STAGE_SEQUENCE,
    audit_candidate_frame,
    gate_cross_frame_continuity,
    gate_pre_contact_windup_air_gap,
    render_synthetic_stage_raster,
    run_autonomous_pipeline,
)
from bubble_break.dense_hammer_bubble_workflow import (
    auto_select_candidate,
    estimate_candidate_roi,
    make_candidates,
)


class AutonomousPipelineTests(unittest.TestCase):
    def test_auto_select_candidate_deterministically_picks_c13(self) -> None:
        candidates = make_candidates()
        winner, ranking = auto_select_candidate(candidates)
        self.assertEqual(winner.candidate_id, "C13")
        self.assertGreater(ranking[0]["total_score"], 0.85)
        roi = estimate_candidate_roi(winner)
        self.assertEqual(len(roi), 4)

    def test_cross_frame_continuity_rejects_scene_jump_and_passes_connected(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            p_parent = Path(td) / "d2.jpg"
            p_good = Path(td) / "d3_good.jpg"
            p_jump = Path(td) / "d3_jump.jpg"
            render_synthetic_stage_raster(p_parent, "D2")
            render_synthetic_stage_raster(p_good, "D3")
            render_synthetic_stage_raster(p_jump, "D3", inject_fault="scene_jump")

            g_ok = gate_cross_frame_continuity(p_good, p_parent)
            self.assertTrue(g_ok.passed, g_ok.detail)

            g_bad = gate_cross_frame_continuity(p_jump, p_parent)
            self.assertFalse(g_bad.passed)
            self.assertIn("disconnected from parent frame", g_bad.detail)

    def test_pre_contact_windup_air_gap_rejects_stuck_cylinder_and_passes_detached(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            stuck_p = Path(td) / "h0_stuck.jpg"
            render_synthetic_stage_raster(stuck_p, "PRE_FAR", inject_fault="stuck_on_bubble")
            g_stuck = gate_pre_contact_windup_air_gap(stuck_p)
            self.assertFalse(g_stuck.passed)

            detached_p = Path(td) / "h0_detached.jpg"
            render_synthetic_stage_raster(detached_p, "PRE_FAR")
            g_ok = gate_pre_contact_windup_air_gap(detached_p)
            self.assertTrue(g_ok.passed, g_ok.detail)

    def test_fault_injection_triggers_auto_rejection_and_rollback(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            outdir = Path(td) / "auto_run"
            report = run_autonomous_pipeline(outdir, simulate_fault_injection=True)
            self.assertTrue(report.all_stages_passed)
            self.assertEqual(report.selected_candidate_id, "C13")
            self.assertEqual(report.passed_stages, len(AUTONOMOUS_STAGE_SEQUENCE))
            self.assertEqual(report.auto_rejections_and_rollbacks, 3)
            self.assertEqual(len(report.five_keyframe_trilogy), 5)

    def test_grid_split_candidate_is_rejected_by_single_frame_gate(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            grid_p = Path(td) / "grid_fault.jpg"
            render_synthetic_stage_raster(grid_p, "B", inject_fault="grid_split")
            passed, score, gates, reasons = audit_candidate_frame("B", grid_p)
            self.assertFalse(passed)
            self.assertTrue(any("single_full_frame_no_grid" in r for r in reasons))


if __name__ == "__main__":
    unittest.main()
