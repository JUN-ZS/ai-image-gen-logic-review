from __future__ import annotations

import unittest

from bubble_break.closed_loop_evidence_guard import (
    attach_guard_errors,
    validate_stage_binding,
)


class ClosedLoopEvidenceGuardTests(unittest.TestCase):
    def calibration_evidence(self, stage, parent_sha=None, parent_stage=None):
        return {
            "stage": stage,
            "parent_raster_sha256": parent_sha,
            "parent_stage": parent_stage,
            "scene_lock_id": "scene-001",
            "camera_lock_id": "camera-locked-01",
            "tool_a_identity_id": "HAMMER_A_TRACK",
            "tool_b_identity_id": "HAMMER_B_TRACK",
        }

    def bubble_evidence(self, stage, parent_sha, parent_stage, crack_ratio, shell_state, cracks):
        return {
            "stage": stage,
            "parent_raster_sha256": parent_sha,
            "parent_stage": parent_stage,
            "calibrated_from_dual_hammer_sha256": "dual-contact-sha",
            "scene_lock_id": "bubble-scene-001",
            "camera_lock_id": "camera-locked-01",
            "attacking_hammer_identity_id": "HAMMER_A_TRACK",
            "bubble_identity_id": "BUBBLE_TRACK",
            "shell_integrity_state": shell_state,
            "crack_front_radius_ratio": crack_ratio,
            "preexisting_cracks": cracks,
            "shell_only_breach": stage == "H3_FOLLOWTHROUGH_SHELL_SHATTER",
            "inhabitants_unharmed": stage == "H3_FOLLOWTHROUGH_SHELL_SHATTER",
        }

    def test_first_calibration_stage_can_start_without_parent(self):
        evidence = self.calibration_evidence("PRE_FAR")
        self.assertEqual(
            validate_stage_binding(
                domain="CALIBRATION", expected_stage="PRE_FAR", evidence=evidence,
                raster_sha256="raster-sha-0", expected_parent_sha256=None,
                expected_parent_stage=None,
            ),
            [],
        )

    def test_wrong_stage_cannot_be_placed_in_another_slot(self):
        evidence = self.calibration_evidence("REACTION", "parent-sha", "FIRST_CONTACT")
        errors = validate_stage_binding(
            domain="CALIBRATION", expected_stage="PRE_NEAR", evidence=evidence,
            raster_sha256="raster-sha-1", expected_parent_sha256="parent-sha",
            expected_parent_stage="PRE_FAR",
        )
        self.assertTrue(any(x.startswith("STAGE_SLOT_MISMATCH") for x in errors))
        self.assertTrue(any(x.startswith("PARENT_STAGE_MISMATCH") for x in errors))

    def test_parent_hash_mismatch_and_noop_are_blocked(self):
        evidence = self.calibration_evidence("PRE_NEAR", "stale-parent", "PRE_FAR")
        errors = validate_stage_binding(
            domain="CALIBRATION", expected_stage="PRE_NEAR", evidence=evidence,
            raster_sha256="parent-sha", expected_parent_sha256="parent-sha",
            expected_parent_stage="PRE_FAR",
        )
        self.assertIn("PARENT_RASTER_SHA256_MISMATCH", errors)
        self.assertIn("NO_OP_TRANSITION_IMAGE_IDENTICAL_TO_PARENT", errors)

    def test_camera_or_tool_identity_drift_is_blocked(self):
        previous = self.calibration_evidence("PRE_FAR")
        evidence = self.calibration_evidence("PRE_NEAR", "parent-sha", "PRE_FAR")
        evidence["camera_lock_id"] = "new-camera"
        errors = validate_stage_binding(
            domain="CALIBRATION", expected_stage="PRE_NEAR", evidence=evidence,
            raster_sha256="new-raster-sha", expected_parent_sha256="parent-sha",
            expected_parent_stage="PRE_FAR", previous_evidence=previous,
        )
        self.assertIn("IDENTITY_LOCK_CHANGED:camera_lock_id", errors)

    def test_bubble_stage_requires_exact_dual_t_provenance(self):
        evidence = self.bubble_evidence(
            "H0_PRE_IMPACT", "cal-sha", "CALIBRATION_FIRST_CONTACT", 0.0, "INTACT", False
        )
        errors = validate_stage_binding(
            domain="BUBBLE_BREAK", expected_stage="H0_PRE_IMPACT", evidence=evidence,
            raster_sha256="h0-sha", expected_parent_sha256="cal-sha",
            expected_parent_stage="CALIBRATION_FIRST_CONTACT",
            expected_calibration_sha256="another-calibration-sha",
        )
        self.assertIn("CALIBRATED_FROM_DUAL_HAMMER_SHA256_MISMATCH", errors)

    def test_shell_fracture_must_expand_monotonically_from_contact(self):
        h1 = self.bubble_evidence("H1_PRE_NEAR", "h0-sha", "H0_PRE_IMPACT", 0.0, "INTACT", False)
        h2 = self.bubble_evidence("H2_FIRST_CONTACT", "h1-sha", "H1_PRE_NEAR", 0.08, "INITIATED", False)
        h2b = self.bubble_evidence("H2B_CRACK_PROPAGATION", "h2-sha", "H2_FIRST_CONTACT", 0.04, "PROPAGATING", True)
        errors = validate_stage_binding(
            domain="BUBBLE_BREAK", expected_stage="H2B_CRACK_PROPAGATION", evidence=h2b,
            raster_sha256="h2b-sha", expected_parent_sha256="h2-sha",
            expected_parent_stage="H2_FIRST_CONTACT", expected_calibration_sha256="dual-contact-sha",
            previous_evidence=h2,
        )
        self.assertIn("CRACK_FRONT_DID_NOT_EXPAND_FROM_H2_TO_H2B", errors)

    def test_final_frame_requires_shell_only_breach_and_safe_inhabitants(self):
        h2b = self.bubble_evidence("H2B_CRACK_PROPAGATION", "h2-sha", "H2_FIRST_CONTACT", 0.3, "PROPAGATING", True)
        h3 = self.bubble_evidence("H3_FOLLOWTHROUGH_SHELL_SHATTER", "h2b-sha", "H2B_CRACK_PROPAGATION", 0.75, "SHATTERED", True)
        h3["inhabitants_unharmed"] = False
        errors = validate_stage_binding(
            domain="BUBBLE_BREAK", expected_stage="H3_FOLLOWTHROUGH_SHELL_SHATTER", evidence=h3,
            raster_sha256="h3-sha", expected_parent_sha256="h2b-sha",
            expected_parent_stage="H2B_CRACK_PROPAGATION", expected_calibration_sha256="dual-contact-sha",
            previous_evidence=h2b,
        )
        self.assertIn("FINAL_FRAME_MUST_DECLARE_INHABITANTS_UNHARMED", errors)

    def test_guard_errors_override_a_pixel_gate_pass(self):
        raw = {"accepted": True, "status": "BUBBLE_BREAK_RASTER_EVIDENCE_PASS", "errors": []}
        out = attach_guard_errors(raw, ["PARENT_RASTER_SHA256_MISMATCH"])
        self.assertFalse(out["accepted"])
        self.assertEqual(out["status"], "BLOCKED_EVIDENCE_BINDING_OR_STATE_TRANSITION")
        self.assertEqual(out["acceptance_level"], "BLOCKED")


if __name__ == "__main__":
    unittest.main(verbosity=2)
