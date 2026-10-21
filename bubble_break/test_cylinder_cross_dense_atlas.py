#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regression tests for the single-image dense CYLINDER_CROSS candidate atlas."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from cylinder_cross_dense_atlas import TARGET_INTERACTIONS, build_atlas, main


class CylinderCrossDenseAtlasTests(unittest.TestCase):
    def test_builds_irregular_manifest_for_24_varied_local_pairs(self):
        manifest = build_atlas()
        self.assertEqual(manifest["artifact_type"], "SINGLE_IMAGE_DENSE_CANDIDATE_ATLAS")
        self.assertEqual(manifest["topology"], "CYLINDER_CROSS")
        self.assertEqual(manifest["target_local_collision_count"], 24)
        self.assertEqual(manifest["target_hammer_count"], 48)
        self.assertEqual(manifest["required_visible_long_handles"], 48)
        self.assertEqual(manifest["minimum_handle_to_head_width_ratio"], 2.5)
        self.assertEqual(TARGET_INTERACTIONS, 24)
        self.assertEqual(manifest["canvas"]["layout"], "IRREGULAR_SCATTER_NO_GRID")
        self.assertFalse(manifest["sampling_balance"]["rendered_instance_count_guaranteed"])
        self.assertEqual(manifest["generation_status"], "IMAGE_REALIZATION_NOT_RUN")
        self.assertEqual(manifest["pixel_audit_status"], "PIXEL_AUDIT_NOT_RUN")
        self.assertTrue(manifest["variation_contract"]["independent_3d_pair_orientations_required"])
        self.assertTrue(manifest["variation_contract"]["both_long_handles_visible_per_pair"])
        self.assertFalse(manifest["variation_contract"]["uniform_grid_allowed"])
        instances = manifest["instances"]
        self.assertEqual(len(instances), 24)
        self.assertEqual(len({item["instance_id"] for item in instances}), 24)
        self.assertEqual(len({item["region_hint"] for item in instances}), 24)
        self.assertEqual({v for v in manifest["sampling_balance"]["counts_by_collision_axis"].values()}, {6})
        self.assertEqual(set(manifest["sampling_balance"]["counts_by_handle_roll"].values()), {6})

    def test_prompt_locks_cap_contact_rigid_body_and_crop_separation(self):
        prompt = build_atlas()["prompt_text"].lower()
        for phrase in (
            "ultra-dense",
            "16:9",
            "24 distinct 3d hammer-pair collision studies",
            "flat circular end caps",
            "face-to-face",
            "coincident planes",
            "opposite normals",
            "curved-barrel-side collision",
            "no short central peg",
            "at least 2.5 times",
            "both separate handles",
            "impact sparks at the center joint",
            "upper-left pocket",
            "do not form neat rows or columns",
            "for later human scanning and cropping",
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
