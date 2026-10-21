#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regression tests for the single-image dense CYLINDER_CROSS candidate atlas."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from cylinder_cross_dense_atlas import COLUMNS, ROWS, build_atlas, main


class CylinderCrossDenseAtlasTests(unittest.TestCase):
    def test_builds_single_image_manifest_for_48_intended_local_pairs(self):
        manifest = build_atlas()
        self.assertEqual(manifest["artifact_type"], "SINGLE_IMAGE_DENSE_CANDIDATE_ATLAS")
        self.assertEqual(manifest["topology"], "CYLINDER_CROSS")
        self.assertEqual(manifest["intended_local_collision_count"], 48)
        self.assertEqual(manifest["intended_hammer_count"], 96)
        self.assertEqual(manifest["canvas"]["target_layout_columns"], 8)
        self.assertEqual(manifest["canvas"]["target_layout_rows"], 6)
        self.assertEqual((COLUMNS, ROWS), (8, 6))
        self.assertFalse(manifest["sampling_balance"]["rendered_instance_count_guaranteed"])
        self.assertEqual(manifest["generation_status"], "IMAGE_REALIZATION_NOT_RUN")
        self.assertEqual(manifest["pixel_audit_status"], "PIXEL_AUDIT_NOT_RUN")
        instances = manifest["instances"]
        self.assertEqual(len(instances), 48)
        self.assertEqual(len({item["instance_id"] for item in instances}), 48)
        self.assertEqual(len({(item["grid_row"], item["grid_column"]) for item in instances}), 48)
        self.assertEqual({item["grid_row"] for item in instances}, set(range(1, 7)))
        self.assertEqual({item["grid_column"] for item in instances}, set(range(1, 9)))

    def test_prompt_locks_cap_contact_rigid_body_and_crop_separation(self):
        prompt = build_atlas()["prompt_text"].lower()
        for phrase in (
            "ultra-dense",
            "16:9",
            "flat circular end caps",
            "flat-face-to-flat-face",
            "coincident cap planes",
            "opposite outward normals",
            "curved cylindrical barrel walls",
            "never make first contact",
            "no bending",
            "for later visual scanning and cropping",
            "neighboring pairs",
        ):
            self.assertIn(phrase, prompt)
        self.assertNotIn("Keep both T heads", prompt)
        self.assertNotIn("no contact sheet", prompt)

    def test_cli_writes_prompt_with_matching_hash_and_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(main(["--outdir", tmp]), 0)
            root = Path(tmp)
            prompt_path = root / "cylinder_cross_dense_atlas_prompt.txt"
            manifest_path = root / "cylinder_cross_dense_atlas_manifest.json"
            self.assertTrue(prompt_path.exists())
            self.assertTrue(manifest_path.exists())
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            prompt = prompt_path.read_text(encoding="utf-8").rstrip("\n")
            self.assertEqual(hashlib.sha256(prompt.encode("utf-8")).hexdigest(), manifest["prompt_sha256"])
            self.assertEqual(manifest["gate"], "ATLAS_PROMPT_READY")
            self.assertEqual(manifest["crop_review_status"], "CROP_CANDIDATES_UNREVIEWED")
            self.assertIn("Legacy T-hammer images are excluded", manifest["warning"])
            self.assertTrue((root / "README.md").exists())


if __name__ == "__main__":
    unittest.main()
