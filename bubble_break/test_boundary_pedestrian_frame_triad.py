"""Tests for SHA-gated H2 master-first PRE/MID/POST continuity."""
from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from bubble_break.boundary_pedestrian_frame_triad import (
    REQUIRED_H2_CHECKS,
    build_triad,
    label_text_sha256,
    sha256_file,
)
from bubble_break.boundary_pedestrian_try_art import text_content_sha256


def package_fixture() -> dict:
    return {
        "combination_id": "BPX-TEST-0001",
        "loop_id": "LOOP-000123",
        "try_id": "TRY-ABC123",
        "axes": {
            "geo_family": "T",
            "contact": "H2",
            "camera": "X_RIGHT__CAM07_GRAZING_FACE__M1",
            "camera_pack": "T192",
        },
        "art_label_spec": {
            "story": "THE BOUNDARY WALKER",
            "loop_id": "LOOP-000123",
            "try_id": "TRY-ABC123",
            "method_id": "GEO.T",
            "method_label": "T-hammer terminal end-face contact · H2",
            "geometry_family": "T",
            "contact_method": "H2",
            "camera_id": "T192-X_RIGHT-CAM07-M1",
            "pose_id": "P03",
            "style_id": "S01",
            "series_id": "S01-RAIN-TOKYO",
            "world_label": "Rainy Tokyo / 雨夜東京",
            "acts": {"3": {"act_id": "3", "prompt_id": "BPX-TEST-0001-I-ACT3"}},
        },
    }


class BoundaryPedestrianFrameTriadTests(unittest.TestCase):
    def test_without_h2_review_pre_post_are_blocked(self) -> None:
        result = build_triad(package_fixture())
        self.assertEqual(result["status"], "HOLD_MID_CORRECTION_AND_REVIEW")
        self.assertFalse(result["mid_geometry_review_accepted"])
        self.assertEqual(result["frames"][0]["status"], "MID_CORRECTION_REQUIRED")
        self.assertEqual(result["frames"][1]["status"], "BLOCKED_UNTIL_MID_H2_ACCEPTED")
        self.assertEqual(result["frames"][2]["status"], "BLOCKED_UNTIL_MID_H2_ACCEPTED")
        self.assertEqual(result["generation_order"], [
            "MID_H2_CORRECT_AND_REVIEW",
            "PRE_H1_FROM_ACCEPTED_MID",
            "POST_H3_FROM_ACCEPTED_MID",
        ])

    def test_exact_sha_and_all_geometry_checks_unlock_reference_derivatives(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            mid = Path(tmp) / "corrected_mid_h2.png"
            mid.write_bytes(b"candidate raster bytes - accepted fixture")
            receipt = {
                "review_status": "HUMAN_ACCEPTED",
                "image_sha256": sha256_file(mid),
                "geometry_checks": {field: True for field in REQUIRED_H2_CHECKS},
            }
            result = build_triad(package_fixture(), mid, receipt)
            self.assertEqual(result["status"], "TRIAD_READY_AFTER_MID_REVIEW")
            self.assertTrue(result["mid_geometry_review_accepted"])
            self.assertEqual(result["mid_master_sha256"], hashlib.sha256(mid.read_bytes()).hexdigest())
            self.assertEqual(result["frames"][0]["status"], "HUMAN_ACCEPTED")
            self.assertEqual(result["frames"][1]["status"], "PROMPT_READY")
            self.assertEqual(result["frames"][2]["status"], "PROMPT_READY")
            self.assertEqual(result["frames"][1]["parent_sha256"], result["mid_master_sha256"])
            self.assertEqual(result["frames"][2]["parent_sha256"], result["mid_master_sha256"])
            self.assertEqual(result["frames"][1]["parent_frame_id"], "MID_H2")
            self.assertEqual(result["frames"][2]["parent_frame_id"], "MID_H2")
            self.assertTrue(all(frame["text_content_sha256"] == result["frame_typography"]["text_content_sha256"]
                                for frame in result["frames"]))
            self.assertIn("do not generate independently", result["frames"][1]["prompt"])
            self.assertIn("same accepted H2 mid-frame raster", result["frames"][2]["prompt"])
            self.assertIn("positive air gap", result["frames"][1]["prompt"])
            self.assertIn("same-axis H3 follow-through", result["frames"][2]["prompt"])
            self.assertIn("pixel-registered", result["frames"][1]["prompt"])
            self.assertIn("only temporal change", result["frames"][2]["prompt"])

    def test_stale_sha_or_one_missing_geometry_check_keeps_gate_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            mid = Path(tmp) / "mid.png"
            mid.write_bytes(b"corrected H2 candidate")
            receipt = {
                "review_status": "HUMAN_ACCEPTED",
                "image_sha256": "0" * 64,
                "geometry_checks": {field: True for field in REQUIRED_H2_CHECKS},
            }
            receipt["geometry_checks"]["crossbar_and_handle_topology_correct"] = False
            result = build_triad(package_fixture(), mid, receipt)
            self.assertFalse(result["mid_geometry_review_accepted"])
            self.assertEqual(result["frames"][1]["status"], "BLOCKED_UNTIL_MID_H2_ACCEPTED")
            self.assertTrue(any("does not match" in reason for reason in result["blocked_reasons"]))
            self.assertTrue(any("crossbar_and_handle_topology_correct" in reason for reason in result["blocked_reasons"]))

    def test_rejects_other_contact_or_geometry_instead_of_inventing_transition(self) -> None:
        package = package_fixture()
        package["axes"]["geo_family"] = "MULTI"
        with self.assertRaises(ValueError):
            build_triad(package)

    def test_triad_text_hash_matches_poster_renderer_signature(self) -> None:
        label = package_fixture()["art_label_spec"]
        act = label["acts"]["3"]
        metadata = {
            "story": label["story"],
            "loop_id": label["loop_id"],
            "try_id": label["try_id"],
            "method_id": label["method_id"],
            "method_label": label["method_label"],
            "geometry_family": label["geometry_family"],
            "contact_method": label["contact_method"],
            "camera_id": label["camera_id"],
            "pose_id": label["pose_id"],
            "style_id": label["style_id"],
            "series_id": label["series_id"],
            "world_label": label["world_label"],
            "prompt_id": act["prompt_id"],
        }
        self.assertEqual(label_text_sha256(label, "3"), text_content_sha256(metadata))

    def test_typography_signature_is_stable_for_same_try(self) -> None:
        label = package_fixture()["art_label_spec"]
        first = label_text_sha256(label, "3")
        second = label_text_sha256(json.loads(json.dumps(label)), "3")
        self.assertEqual(first, second)
        self.assertEqual(len(first), 64)


if __name__ == "__main__":
    unittest.main()
