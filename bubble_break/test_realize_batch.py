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
    def test_builds_story_variants_with_one_shared_T_master_and_does_not_claim_render(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); source=root/"rows.jsonl"
            rows=[sample_row(1,"A"),sample_row(2,"A"),sample_row(3,"B")]
            source.write_text("".join(json.dumps(x)+"\n" for x in rows),encoding="utf-8")
            out=root/"out"; result=build_batch(source,out,per_kernel=1,limit=20,final_weapon="T")
            self.assertEqual(result["selected_stories"],2)
            self.assertEqual(result["distinct_causal_kernels"],2)
            self.assertEqual(result["final_weapon"],"T")
            self.assertEqual(result["stage_gate_status"],"BLOCKED_UNTIL_T_WEAPON_MASTER_APPROVED")
            self.assertEqual(result["required_first_stage"],"A_T_WEAPON_MASTER")
            self.assertEqual(result["image_realization"],"NOT_RUN")
            self.assertEqual(result["pixel_audit_status"],"NOT_RUN")
            shared=Path(result["shared_weapon_master_directory"])
            self.assertTrue((shared/"00_generate_T_weapon_master.txt").exists())
            self.assertTrue((shared/"05_T_silhouette_reference.svg").exists())
            self.assertTrue((shared/"stage_gate.json").exists())
            self.assertEqual(len({p["shared_weapon_master_directory"] for p in result["packages"]}),1)
            self.assertEqual(len({p["required_first_stage_artifact"] for p in result["packages"]}),1)
            for p in result["packages"]:
                d=Path(p["proxy_directory"])
                self.assertTrue((d/"04_T_final_weapon_preview.svg").exists())
                self.assertTrue((d/"generate_scene_with_T_master.txt").exists())
                self.assertFalse((d/"00_generate_T_weapon_master.txt").exists())
                self.assertFalse((d/"05_T_silhouette_reference.svg").exists())
                self.assertEqual(p["stage_gate_status"],"BLOCKED_UNTIL_T_WEAPON_MASTER_APPROVED")
                self.assertEqual(p["required_first_stage_artifact"],str(shared/"A_T_weapon_master.png"))
                plan=json.loads((d/"edit_plan.json").read_text(encoding="utf-8"))
                self.assertEqual(plan["final_weapon"],"T")
                self.assertEqual(plan["method"],"T_MASTER_THEN_STORY_VARIANT_SCENE_GENERATION")
                self.assertEqual(plan["status"],"BLOCKED_UNTIL_T_WEAPON_MASTER_APPROVED")
                self.assertEqual(plan["master_scope"],"SHARED_ACROSS_BATCH")
                self.assertEqual(plan["required_artifacts"]["stage_a_image"],str(shared/"A_T_weapon_master.png"))
                self.assertEqual(plan["selected_edit_prompt"],"generate_scene_with_T_master.txt")
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
