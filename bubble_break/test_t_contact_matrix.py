#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import tempfile
import unittest
from pathlib import Path

from t_contact_matrix import CAMERA_VIEWS, REVIEW_CHECKS, STRIKE_AXES, build_matrix, make_prompt, review_payload_passes, validate_matrix


class TContactMatrixTests(unittest.TestCase):
    def test_matrix_has_48_variants_and_144_single_image_prompts(self):
        with tempfile.TemporaryDirectory() as td:
            result=build_matrix(Path(td))
            self.assertEqual(result["camera_view_count"],12)
            self.assertEqual(result["collision_axis_count"],4)
            self.assertEqual(result["variant_count"],48)
            self.assertEqual(result["single_image_prompt_count"],144)
            self.assertEqual(result["required_H2_contact_proof_images"],48)
            rows=[json.loads(x) for x in (Path(td)/"t_contact_matrix.jsonl").read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(rows),144)
            self.assertEqual(sum(x["state"]=="H2" for x in rows),48)
            self.assertEqual(len({x["variant_id"] for x in rows}),48)
            self.assertEqual(len({x["prompt"] for x in rows}),144)
            self.assertEqual(result["image_realization"],"NOT_RUN")
            self.assertEqual(result["pixel_audit"],"NOT_RUN")

    def test_h2_requires_two_terminal_end_faces_not_cheeks(self):
        prompt=make_prompt("V001","FACE_ON","head-on view","HORIZONTAL","horizontal strike","H2")
        self.assertIn("terminal END STRIKING FACE of hammer A",prompt)
        self.assertIn("terminal END STRIKING FACE of hammer B",prompt)
        self.assertIn("face-to-face",prompt)
        self.assertIn("coincident at one shared contact centre P",prompt)
        self.assertIn("normals point in exactly opposite directions",prompt)
        self.assertIn("long side walls/cheeks",prompt)
        self.assertIn("top-plane-to-top-plane",prompt)
        self.assertIn("handle-first",prompt)
        self.assertIn("one standalone",prompt.lower())
        self.assertIn("no contact sheet",prompt.lower())

    def test_matrix_creates_review_templates_and_unreviewed_images_stay_blocked(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            manifest=build_matrix(root)
            templates=[root/Path(v["review_template"]) for v in manifest["variants"]]
            self.assertEqual(len(templates),48)
            self.assertTrue(all(p.exists() for p in templates))
            first=json.loads(templates[0].read_text(encoding="utf-8"))
            self.assertEqual(first["status"],"UNASSESSED")
            self.assertFalse(first["manual_pixel_review"])
            self.assertEqual(set(first["checks"]),set(REVIEW_CHECKS))
            self.assertTrue(all(v is False for v in first["checks"].values()))
            report=validate_matrix(root)
            self.assertEqual(report["overall_status"],"BLOCKED")
            self.assertEqual(report["reviewed_pass_count"],0)
            self.assertEqual(report["blocked_count"],48)
            self.assertFalse(report["automatic_pixel_claims"])
            self.assertTrue((root/"contact_matrix_audit_report.json").exists())

    def test_review_cannot_pass_without_manual_review_notes_and_all_checks(self):
        payload={
            "status":"PASS",
            "manual_pixel_review":True,
            "notes":"Inspected the actual rendered H2 image at native resolution.",
            "checks":{name:True for name in REVIEW_CHECKS},
        }
        self.assertTrue(review_payload_passes(payload))
        payload["manual_pixel_review"]=False
        self.assertFalse(review_payload_passes(payload))
        payload["manual_pixel_review"]=True
        payload["checks"]["no_cheek_first"]=False
        self.assertFalse(review_payload_passes(payload))
        payload["checks"]["no_cheek_first"]=True
        payload["notes"]="   "
        self.assertFalse(review_payload_passes(payload))

    def test_all_camera_and_axis_slots_are_nonempty_and_distinct(self):
        self.assertEqual(len(CAMERA_VIEWS),12)
        self.assertEqual(len(STRIKE_AXES),4)
        self.assertEqual(len({x[0] for x in CAMERA_VIEWS}),12)
        self.assertEqual(len({x[0] for x in STRIKE_AXES}),4)
        self.assertTrue(all(description for _,description in CAMERA_VIEWS))
        self.assertTrue(all(description for _,description in STRIKE_AXES))


if __name__ == "__main__":
    unittest.main()
