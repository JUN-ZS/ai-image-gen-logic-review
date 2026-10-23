import hashlib
import unittest

from bubble_break.prompt_failure_diagnosis import (
    build_repair_prompt,
    diagnose_attempt,
)


class TestPromptFailureDiagnosis(unittest.TestCase):
    def reviewed_manifest(self, **observed):
        digest = "a" * 64
        manifest = {
            "attempt_id": "TRY-0042",
            "stage_id": "H2",
            "topology_id": "t_hammer_terminal_face",
            "expected": {
                "active_surface": "terminal_end_face",
                "gap_units": 0,
                "contact_point_id": "P",
                "advance_units": 15,
            },
            "observed": {
                "active_surface": "UNVERIFIED",
                "measured_gap_units": "UNVERIFIED",
                "penetration_depth_units": "UNVERIFIED",
                "crack_origin": "UNVERIFIED",
                "handle_status": "UNVERIFIED",
                "camera_contact_seam_visible": "UNVERIFIED",
                "scene_identity_match": "UNVERIFIED",
                "character_identity_match": "UNVERIFIED",
                "residents_safe": "UNVERIFIED",
                "measured_advance_units": "UNVERIFIED",
            },
            "failure_codes": [],
            "failure_reasons": [],
            "raster_sha256": digest,
            "review_receipt": {
                "reviewer": "reviewer-01",
                "verdict": "FAIL",
                "raster_sha256": digest,
                "reviewed_at": "2026-10-23T08:00:00Z",
            },
        }
        manifest["observed"].update(observed)
        return manifest, digest

    def test_no_sha_bound_fail_receipt_means_hold(self):
        manifest, digest = self.reviewed_manifest(active_surface="sidewall")
        manifest["review_receipt"]["raster_sha256"] = "0" * 64
        result = diagnose_attempt(manifest, raster_sha256=digest)
        self.assertEqual(result["status"], "HOLD")
        self.assertEqual(result["primary_failure_code"], "INSUFFICIENT_EVIDENCE")
        self.assertIn("matching raster_sha256", result["repair_prompt_delta"])

    def test_no_actual_raster_hash_means_hold_even_with_failure_code(self):
        manifest, _ = self.reviewed_manifest()
        manifest["failure_codes"] = ["WRONG_CONTACT_FACE"]
        result = diagnose_attempt(manifest, raster_sha256=None)
        self.assertEqual(result["status"], "HOLD")
        self.assertEqual(result["all_failure_codes"], [])

    def test_wrong_face_maps_to_pose_only_change_and_freezes_topology(self):
        manifest, digest = self.reviewed_manifest(active_surface="broad_sidewall")
        result = diagnose_attempt(manifest, raster_sha256=digest)
        self.assertEqual(result["status"], "REPAIR_PLAN_READY")
        self.assertEqual(result["primary_failure_code"], "WRONG_CONTACT_FACE")
        self.assertIn("approach_vector", result["edit_only"])
        self.assertIn("weapon_topology", result["freeze"])
        self.assertIn("broad_sidewall", result["primary_evidence"])
        prompt = build_repair_prompt("Original H2 prompt", result)
        self.assertIn("[DATA-DRIVEN NEXT-ATTEMPT DELTA]", prompt)
        self.assertIn("KEEP FROZEN", prompt)
        self.assertIn("do not change success", prompt.lower())

    def test_positive_contact_gap_selects_translation_not_camera_or_scale(self):
        manifest, digest = self.reviewed_manifest(measured_gap_units=4.5)
        result = diagnose_attempt(manifest, raster_sha256=digest)
        self.assertEqual(result["primary_failure_code"], "GAP_REMAINS")
        self.assertEqual(result["edit_only"], ["weapon_translation_along_collision_normal"])
        self.assertIn("camera_rig", result["freeze"])
        self.assertIn("4.5 units", result["evidence"][0]["basis"])

    def test_interpenetration_has_priority_over_residual_gap(self):
        manifest, digest = self.reviewed_manifest(measured_gap_units=-2.0, penetration_depth_units=2.0)
        result = diagnose_attempt(manifest, raster_sha256=digest)
        self.assertEqual(result["primary_failure_code"], "INTERPENETRATION")
        self.assertIn("inverse collision normal", result["repair_prompt_delta"])

    def test_wrong_crack_origin_changes_effect_only(self):
        manifest, digest = self.reviewed_manifest(crack_origin="far_side")
        result = diagnose_attempt(manifest, raster_sha256=digest)
        self.assertEqual(result["primary_failure_code"], "WRONG_CRACK_ORIGIN")
        self.assertEqual(result["edit_only"], ["crack_origin", "fracture_effect_region"])
        self.assertIn("weapon_pose", result["freeze"])
        self.assertIn("far_side", result["primary_evidence"])

    def test_new_handle_forces_rollback_and_freeze(self):
        manifest, digest = self.reviewed_manifest(handle_status="NEW_HANDLE")
        result = diagnose_attempt(manifest, raster_sha256=digest)
        self.assertEqual(result["primary_failure_code"], "HANDLE_TOPOLOGY_FAIL")
        self.assertIn("restore_from_last_pass_parent", result["edit_only"])
        self.assertIn("Do not proceed", result["repair_prompt_delta"])

    def test_camera_failure_changes_view_only(self):
        manifest, digest = self.reviewed_manifest(camera_contact_seam_visible=False)
        result = diagnose_attempt(manifest, raster_sha256=digest)
        self.assertEqual(result["primary_failure_code"], "CAMERA_OBSCURES_CONTACT")
        self.assertEqual(result["edit_only"], ["camera_view"])
        self.assertIn("world_collision_axis", result["freeze"])

    def test_multiple_failures_are_listed_but_one_minimal_repair_is_prioritized(self):
        manifest, digest = self.reviewed_manifest(active_surface="sidewall", residents_safe=False)
        result = diagnose_attempt(manifest, raster_sha256=digest)
        self.assertEqual(result["primary_failure_code"], "WRONG_CONTACT_FACE")
        self.assertIn("RESIDENT_SAFETY_FAIL", result["all_failure_codes"])
        self.assertIn("RESIDENT_SAFETY_FAIL", result["additional_failure_codes"])

    def test_unclassified_prose_does_not_invent_diagnosis(self):
        manifest, digest = self.reviewed_manifest()
        manifest["failure_reasons"] = ["looks bad somehow"]
        result = diagnose_attempt(manifest, raster_sha256=digest)
        self.assertEqual(result["status"], "HOLD")
        self.assertEqual(result["primary_failure_code"], "INSUFFICIENT_EVIDENCE")


if __name__ == "__main__":
    unittest.main()
