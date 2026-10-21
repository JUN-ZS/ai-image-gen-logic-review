#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regression tests for the cylinder-ended cross-hammer contact matrix."""
import json
import tempfile
import unittest
from pathlib import Path

from cylinder_cross_contact_matrix import (
    CAMERA_VIEWS,
    HANDLE_CLOCK_VARIANTS,
    REVIEW_CHECKS,
    STATE_TEXT,
    STRIKE_AXES,
    TOPOLOGY_LOCK,
    build_matrix,
    review_payload_passes,
    validate_matrix,
)


class CylinderCrossContactMatrixTests(unittest.TestCase):
    def test_generator_emits_48_variants_and_144_single_state_prompts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = build_matrix(root)
            rows = [
                json.loads(line)
                for line in (root / "cylinder_cross_contact_matrix.jsonl")
                .read_text(encoding="utf-8").splitlines()
            ]
            self.assertEqual(len(CAMERA_VIEWS), 12)
            self.assertEqual(len(STRIKE_AXES), 4)
            self.assertEqual(len(HANDLE_CLOCK_VARIANTS), 4)
            self.assertEqual(manifest["variant_count"], 48)
            self.assertEqual(manifest["single_image_prompt_count"], 144)
            self.assertEqual(len(rows), 144)
            self.assertEqual({row["state"] for row in rows}, {"H0", "H2", "H3"})
            self.assertEqual(len(list(root.glob("V*/H0.txt"))), 48)
            self.assertEqual(len(list(root.glob("V*/H2.txt"))), 48)
            self.assertEqual(len(list(root.glob("V*/H3.txt"))), 48)
            self.assertEqual(len(list(root.glob("V*/V*_H2_review.template.json"))), 48)

    def test_contract_names_only_flat_circular_caps_as_active_surfaces(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = build_matrix(root)
            row = next(
                json.loads(line)
                for line in (root / "cylinder_cross_contact_matrix.jsonl")
                .read_text(encoding="utf-8").splitlines()
                if '"state": "H2"' in line
            )
            contract = row["expected_contact_contract"]
            self.assertEqual(contract["active_surface_A"], "FLAT_CIRCULAR_END_CAP")
            self.assertEqual(contract["active_surface_B"], "FLAT_CIRCULAR_END_CAP")
            self.assertIn("CURVED_BARREL", contract["forbidden_first_contacts"])
            self.assertEqual(manifest["contact_contract"]["surface_A"], "FLAT_CIRCULAR_END_CAP_ONLY")
            self.assertIn("CURVED_CYLINDER_BARREL_FIRST", manifest["contact_contract"]["forbidden"])
            h2 = STATE_TEXT["H2"]
            self.assertIn("ONLY", h2)
            self.assertIn("flat circular end cap", h2)
            self.assertIn("must NOT touch first", h2)
            self.assertIn("rigid", TOPOLOGY_LOCK.lower())

    def test_h0_h2_h3_lock_geometry_and_forbid_flexible_handles(self):
        self.assertIn("small clearly visible air gap", STATE_TEXT["H0"])
        self.assertIn("cap-to-cap", STATE_TEXT["H2"])
        self.assertIn("recoiled", STATE_TEXT["H3"])
        for forbidden_word in ("bending", "twisting", "telescoping", "detaching"):
            self.assertIn(forbidden_word, TOPOLOGY_LOCK)

    def test_generated_reviews_fail_closed_until_human_pixel_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_matrix(root)
            report = validate_matrix(root)
            self.assertEqual(report["overall_status"], "BLOCKED")
            self.assertEqual(report["variant_count"], 48)
            self.assertEqual(report["blocked_count"], 48)
            self.assertEqual(report["reviewed_pass_count"], 0)
        incomplete = {
            "status": "PASS",
            "manual_pixel_review": True,
            "notes": "looked",
            "checks": {name: True for name in REVIEW_CHECKS if name != REVIEW_CHECKS[-1]},
        }
        self.assertFalse(review_payload_passes(incomplete))
        complete = {
            "status": "PASS",
            "manual_pixel_review": True,
            "notes": "Inspected the actual H2 PNG at full resolution.",
            "checks": {name: True for name in REVIEW_CHECKS},
        }
        self.assertTrue(review_payload_passes(complete))


if __name__ == "__main__":
    unittest.main()
