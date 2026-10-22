from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from PIL import Image

from bubble_break.raster_bound_collision_audit import (
    sha256_file,
    validate_raster_bound_collision_evidence,
)


class RasterBoundCollisionAuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.image_path = Path(self.tmp.name) / "first_contact.jpg"
        Image.new("RGB", (200, 100), (20, 20, 20)).save(self.image_path, quality=95)

    def valid_evidence(self):
        return {
            "stage": "FIRST_CONTACT",
            "contact_surface": "END_FACE_TO_END_FACE",
            "signed_gap": 0.0,
            "face_normal_a": [1.0, 0.0, 0.0],
            "face_normal_b": [-1.0, 0.0, 0.0],
            "face_center_a": [0.0, 0.0, 0.0],
            "face_center_b": [0.0, 0.0, 0.0],
            "contact_point": [0.0, 0.0, 0.0],
            "face_radius_a": 0.02,
            "face_radius_b": 0.02,
            "tool_a_present": True,
            "tool_b_present": True,
            "separate_handles": True,
            "evidence_source": "HUMAN_REVIEW",
            "raster_sha256": sha256_file(self.image_path),
            "raster_annotations": {
                "image_width_px": 200,
                "image_height_px": 100,
                "reviewer_or_model": "test-reviewer-v1",
                "tool_a": {
                    "instance_id": "A",
                    "head_bbox_xyxy_px": [20, 40, 80, 60],
                    "handle_bbox_xyxy_px": [45, 50, 55, 90],
                    "head_axis_px": [[20, 50], [80, 50]],
                    "handle_axis_px": [[50, 50], [50, 90]],
                    "strike_face_center_px": [80, 50],
                    "strike_face_radius_px": 10,
                },
                "tool_b": {
                    "instance_id": "B",
                    "head_bbox_xyxy_px": [100, 40, 160, 60],
                    "handle_bbox_xyxy_px": [125, 50, 135, 90],
                    "head_axis_px": [[160, 50], [100, 50]],
                    "handle_axis_px": [[130, 50], [130, 90]],
                    "strike_face_center_px": [100, 50],
                    "strike_face_radius_px": 10,
                },
                "contact_point_px": [90, 50],
            },
        }

    def test_valid_annotations_are_bound_to_exact_raster_but_not_auto_visually_approved(self):
        result = validate_raster_bound_collision_evidence(self.image_path, self.valid_evidence())
        self.assertTrue(result["accepted"], result["errors"])
        self.assertEqual(result["raster_sha256"], sha256_file(self.image_path))
        self.assertEqual(result["visual_acceptance_status"], "NOT_VERIFIED_BY_CODE")

    def test_missing_or_wrong_raster_hash_blocks(self):
        evidence = self.valid_evidence()
        evidence["raster_sha256"] = "0" * 64
        result = validate_raster_bound_collision_evidence(self.image_path, evidence)
        self.assertFalse(result["accepted"])
        self.assertTrue(any("raster_sha256" in e for e in result["errors"]))

    def test_duplicate_hammer_instance_id_blocks(self):
        evidence = self.valid_evidence()
        evidence["raster_annotations"]["tool_b"]["instance_id"] = "A"
        result = validate_raster_bound_collision_evidence(self.image_path, evidence)
        self.assertFalse(result["accepted"])
        self.assertTrue(any("distinct raster instances" in e for e in result["errors"]))

    def test_parallel_handle_is_not_accepted_as_a_t_hammer(self):
        evidence = self.valid_evidence()
        evidence["raster_annotations"]["tool_a"]["handle_axis_px"] = [[50, 50], [90, 50]]
        result = validate_raster_bound_collision_evidence(self.image_path, evidence)
        self.assertFalse(result["accepted"])
        self.assertTrue(any("not visibly transverse" in e for e in result["errors"]))

    def test_contact_point_must_be_inside_both_strike_face_disks(self):
        evidence = self.valid_evidence()
        evidence["raster_annotations"]["contact_point_px"] = [150, 50]
        result = validate_raster_bound_collision_evidence(self.image_path, evidence)
        self.assertFalse(result["accepted"])
        self.assertTrue(any("outside" in e and "face disk" in e for e in result["errors"]))


if __name__ == "__main__":
    unittest.main()
