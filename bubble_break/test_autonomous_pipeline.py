#!/usr/bin/env python3
"""Unit tests for V5.1 Closed-Loop Generative Backend, Honest Evidence Gates, SceneState & Two-Layer Scorer."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from bubble_break.autonomous_pipeline import (
    AUTONOMOUS_STAGE_SEQUENCE,
    CallbackGeneratorBackend,
    audit_candidate_frame,
    default_v51_scene_state,
    gate_cross_frame_continuity,
    gate_no_vertical_splice_seam,
    gate_pre_contact_windup_air_gap,
    gate_static_background_stability,
    render_synthetic_stage_raster,
    run_autonomous_pipeline,
)
from bubble_break.dense_hammer_bubble_workflow import (
    auto_select_candidate,
    estimate_candidate_roi,
    make_candidates,
)


class AutonomousPipelineV51Tests(unittest.TestCase):
    def test_auto_select_candidate_deterministically_picks_c13(self) -> None:
        candidates = make_candidates()
        winner, ranking = auto_select_candidate(candidates)
        self.assertEqual(winner.candidate_id, "C13")
        self.assertGreater(ranking[0]["total_score"], 0.85)
        roi = estimate_candidate_roi(winner)
        self.assertEqual(len(roi), 4)

    def test_scene_state_and_original_sin_causal_engine_are_valid(self) -> None:
        scene = default_v51_scene_state()
        self.assertTrue(scene.causal_engine.validate())
        self.assertEqual(len(scene.frame_specs), 5)
        self.assertIn("KF5_10S_E_END_BLAST", scene.frame_specs)

    def test_production_run_without_real_rasters_or_backend_blocks_honestly(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            report = run_autonomous_pipeline(Path(td) / "blocked_run")
            self.assertEqual(report.evidence_mode, "BLOCKED")
            self.assertFalse(report.all_stages_passed)
            self.assertFalse(report.synthetic_test_passed)

    def test_synthetic_test_mode_never_claims_production_all_stages_passed(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            outdir = Path(td) / "synth_run"
            report = run_autonomous_pipeline(outdir, simulate_fault_injection=True)
            self.assertEqual(report.evidence_mode, "SYNTHETIC_TEST_ONLY")
            self.assertEqual(report.status, "SYNTHETIC_TEST_ONLY")
            self.assertFalse(report.all_stages_passed)  # PR #3 rule: synthetic never sets all_stages_passed=True
            self.assertTrue(report.synthetic_test_passed)
            self.assertEqual(report.passed_stages, len(AUTONOMOUS_STAGE_SEQUENCE))
            self.assertEqual(len(report.five_keyframe_trilogy), 5)
            self.assertEqual(len(report.five_keyframe_transition_audits), 4)
            self.assertGreaterEqual(report.backend_rerun_invocations, 3)

    def test_gate_cross_frame_continuity_fails_when_parent_missing_or_jumped(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            p_good = Path(td) / "d3.jpg"
            render_synthetic_stage_raster(p_good, "D3")
            g_missing = gate_cross_frame_continuity(p_good, None)
            self.assertFalse(g_missing.passed)
            g_bg_missing = gate_static_background_stability(p_good, None)
            self.assertFalse(g_bg_missing.passed)

    def test_stage_blocks_and_halts_if_all_backend_retries_fail(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            def _always_bad_d2(st_id, prompt, parent_p, mask_p, attempt, b_dir):
                b_dir.mkdir(parents=True, exist_ok=True)
                p = b_dir / f"{st_id}_r{attempt}.jpg"
                fault = "outer_end_shaft" if st_id == "D2" else None
                render_synthetic_stage_raster(p, st_id, inject_fault=fault)
                return [p]

            bad_backend = CallbackGeneratorBackend(_always_bad_d2, name="always-fail-d2", synthetic_only=True)
            report = run_autonomous_pipeline(Path(td) / "halt_run", backend=bad_backend, max_retries=2)
            self.assertEqual(report.status, "BLOCKED")
            self.assertFalse(report.all_stages_passed)
            self.assertFalse(report.synthetic_test_passed)
            # Must halt at D2 and NOT populate D3, E_MID, E_END!
            self.assertNotIn("D3", report.canonical_sequence)


if __name__ == "__main__":
    unittest.main()
