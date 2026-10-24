#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import base64
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from t_contact_matrix import CAMERA_VIEWS, HANDLE_CLOCK_VARIANTS, MASTER_REVIEW_CHECKS, REVIEW_CHECKS, STRIKE_AXES, build_matrix, make_prompt, master_review_payload_passes, review_payload_passes, validate_master_review, validate_matrix


class TContactMatrixTests(unittest.TestCase):
    def test_matrix_has_48_variants_and_144_single_image_prompts(self):
        with tempfile.TemporaryDirectory() as td:
            result=build_matrix(Path(td))
            self.assertEqual(result["camera_view_count"],12)
            self.assertEqual(result["collision_axis_count"],4)
            self.assertEqual(result["variant_count"],48)
            self.assertEqual(result["single_image_prompt_count"],144)
            self.assertEqual(result["required_H2_contact_proof_images"],48)
            self.assertEqual(result["expected_prompt_count"],144)
            pose_counts={pose_id: sum(v["handle_roll_variant_id"]==pose_id for v in result["variants"]) for pose_id,_ in HANDLE_CLOCK_VARIANTS}
            self.assertEqual(pose_counts,{pose_id:12 for pose_id,_ in HANDLE_CLOCK_VARIANTS})
            self.assertEqual(result["handle_roll_by_camera"],{camera_id:{pose_id:1 for pose_id,_ in HANDLE_CLOCK_VARIANTS} for camera_id,_ in CAMERA_VIEWS})
            self.assertEqual(result["handle_roll_by_collision_axis"],{axis_id:{pose_id:3 for pose_id,_ in HANDLE_CLOCK_VARIANTS} for axis_id,_ in STRIKE_AXES})
            self.assertEqual(len({(v["camera_view_id"],v["collision_axis_id"]) for v in result["variants"]}),48)
            for camera_id,_ in CAMERA_VIEWS:
                camera_rows=[v for v in result["variants"] if v["camera_view_id"]==camera_id]
                self.assertEqual(len(camera_rows),4)
                self.assertEqual({v["handle_roll_variant_id"] for v in camera_rows},{pose_id for pose_id,_ in HANDLE_CLOCK_VARIANTS})
            for axis_id,_ in STRIKE_AXES:
                axis_rows=[v for v in result["variants"] if v["collision_axis_id"]==axis_id]
                self.assertEqual(len(axis_rows),12)
                axis_pose_counts={pose_id: sum(v["handle_roll_variant_id"]==pose_id for v in axis_rows) for pose_id,_ in HANDLE_CLOCK_VARIANTS}
                self.assertEqual(axis_pose_counts,{pose_id:3 for pose_id,_ in HANDLE_CLOCK_VARIANTS})
            rows=[json.loads(x) for x in (Path(td)/"t_contact_matrix.jsonl").read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(rows),144)
            self.assertEqual(sum(x["state"]=="H2" for x in rows),48)
            self.assertEqual(len({x["variant_id"] for x in rows}),48)
            self.assertEqual(len({x["prompt"] for x in rows}),144)
            self.assertEqual(result["image_realization"],"NOT_RUN")
            self.assertEqual(result["pixel_audit"],"NOT_RUN")

    def test_h2_requires_two_terminal_end_faces_not_cheeks(self):
        prompt=make_prompt("V001","FACE_ON","slightly grazing view","HORIZONTAL","horizontal strike","H_LIKE_OPPOSED_HANDLES","opposed projected handles","H2")
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

    def test_matrix_review_is_bound_to_exact_image_sha256(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            manifest=build_matrix(root)
            variant=manifest["variants"][0]
            image_path=root/variant["required_H2_image"]
            image_path.parent.mkdir(parents=True,exist_ok=True)
            # Tiny PNG fixture; this test checks byte-to-review binding, not visual geometry.
            png=base64.b64decode(
                "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADUlEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC"
            )
            image_path.write_bytes(png)
            review={
                "variant_id":variant["variant_id"],
                "status":"PASS",
                "manual_pixel_review":True,
                "image_sha256":hashlib.sha256(png).hexdigest(),
                "notes":"Test fixture only: review is bound to these exact image bytes.",
                "checks":{name:True for name in REVIEW_CHECKS},
            }
            review_path=root/variant["required_H2_review"]
            review_path.write_text(json.dumps(review),encoding="utf-8")
            report=validate_matrix(root)
            first=next(row for row in report["variants"] if row["variant_id"]==variant["variant_id"])
            self.assertEqual(first["status"],"PASS_MANUAL_REVIEW_RECORDED",first["issues"])
            self.assertEqual(first["image_sha256"],review["image_sha256"])

            # Replacing the raster while retaining the old review must invalidate that PASS.
            changed=bytearray(png)
            changed[-10] ^= 1
            image_path.write_bytes(bytes(changed))
            stale=validate_matrix(root)
            first_stale=next(row for row in stale["variants"] if row["variant_id"]==variant["variant_id"])
            self.assertEqual(first_stale["status"],"BLOCKED")
            self.assertIn("REVIEW_IMAGE_SHA256_MISMATCH",first_stale["issues"])

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

    def test_master_review_requires_real_png_and_complete_human_review(self):
        payload={
            "status":"PASS",
            "manual_pixel_review":True,
            "notes":"Inspected A_T_weapon_master.png at native resolution.",
            "checks":{name:True for name in MASTER_REVIEW_CHECKS},
        }
        self.assertTrue(master_review_payload_passes(payload))
        payload["checks"]["no_second_or_inverted_T"]=False
        self.assertFalse(master_review_payload_passes(payload))
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            (root/"A_T_weapon_master_review.json").write_text(json.dumps(payload),encoding="utf-8")
            result=validate_master_review(root/"A_T_weapon_master.png",root/"A_T_weapon_master_review.json")
            self.assertEqual(result["status"],"BLOCKED")
            self.assertIn("MISSING_OR_INVALID_MASTER_PNG",result["issues"])

    def test_all_camera_and_axis_slots_are_nonempty_and_distinct(self):
        self.assertEqual(len(CAMERA_VIEWS),12)
        self.assertEqual(len(STRIKE_AXES),4)
        self.assertEqual(len({x[0] for x in CAMERA_VIEWS}),12)
        self.assertEqual(len({x[0] for x in STRIKE_AXES}),4)
        self.assertTrue(all(description for _,description in CAMERA_VIEWS))
        self.assertTrue(all(description for _,description in STRIKE_AXES))


if __name__ == "__main__":
    unittest.main()
