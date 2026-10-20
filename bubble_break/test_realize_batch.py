#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json,tempfile,unittest
from pathlib import Path
from realize_batch import select_records,build_batch

def sample_row(i,k):
    return {"story_id":f"S{i}","causal_kernel_id":k,"causal_signature":f"CAUSE-{k}",
      "root_sin":k,"root_mechanism":"a coercive rule","human_cost":"loss of choice",
      "axes":{"environment":{"id":"ENV01","description":"archive"},
      "scale":{"id":"SCALE01","description":"giant bubble"},
      "shell":{"id":"SHELL01","description":"membrane"},
      "palette":{"id":"PAL01","description":"blue amber"},
      "fracture":{"id":"FRAC01","description":"radial cracks"}}}

class RealizeBatchTests(unittest.TestCase):
    def test_selects_per_kernel_not_first_n_duplicate_variants(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"rows.jsonl"
            rows=[sample_row(1,"A"),sample_row(2,"A"),sample_row(3,"B"),sample_row(4,"B"),sample_row(5,"C")]
            path.write_text("".join(json.dumps(x)+"\n" for x in rows),encoding="utf-8")
            chosen=select_records(path,per_kernel=1,limit=10)
            self.assertEqual([x["story_id"] for x in chosen],["S1","S3","S5"])
    def test_builds_one_complete_T_packet_per_kernel_and_does_not_claim_render(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); source=root/"rows.jsonl"
            rows=[sample_row(1,"A"),sample_row(2,"A"),sample_row(3,"B")]
            source.write_text("".join(json.dumps(x)+"\n" for x in rows),encoding="utf-8")
            out=root/"out"; result=build_batch(source,out,per_kernel=1,limit=20,final_weapon="T")
            self.assertEqual(result["selected_stories"],2)
            self.assertEqual(result["distinct_causal_kernels"],2)
            self.assertEqual(result["final_weapon"],"T")
            self.assertEqual(result["stage_gate_status"],"BLOCKED_UNTIL_T_TO_T_IMAGE_APPROVED")
            self.assertEqual(result["required_first_stage"],"A_T_TO_T_ANCHOR")
            self.assertEqual(result["image_realization"],"NOT_RUN")
            self.assertEqual(result["pixel_audit_status"],"NOT_RUN")
            for p in result["packages"]:
                d=Path(p["proxy_directory"])
                self.assertTrue((d/"00_T_to_T_geometry_proxy.svg").exists())
                self.assertTrue((d/"00_generate_T_to_T_anchor.txt").exists())
                self.assertTrue((d/"04_T_final_weapon_preview.svg").exists())
                self.assertEqual(p["stage_gate_status"],"BLOCKED_UNTIL_T_TO_T_IMAGE_APPROVED")
                self.assertEqual(p["required_first_stage_artifact"],"A_T_to_T_anchor.png")
                plan=json.loads((d/"edit_plan.json").read_text(encoding="utf-8"))
                self.assertEqual(plan["final_weapon"],"T")
                self.assertEqual(plan["method"],"T_TO_T_THEN_TARGET_T_ONLY_SPHERE_EDIT")
                self.assertEqual(plan["status"],"BLOCKED_UNTIL_T_TO_T_IMAGE_APPROVED")
                self.assertEqual(plan["selected_edit_prompt"],"edit_target_T_to_bubble.txt")
                self.assertEqual(plan["terminal_face_gap_px"],0)
                self.assertEqual(plan["pixel_truth"]["edited_images"],"NOT_RUN")
            self.assertTrue((out/"realize_batch_manifest.json").exists())
    def test_invalid_final_weapon_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); source=root/"rows.jsonl"
            source.write_text(json.dumps(sample_row(1,"A"))+"\n",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"--final-weapon"):
                build_batch(source,root/"out",final_weapon="STAR")

if __name__=="__main__": unittest.main()
