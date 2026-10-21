#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import tempfile
import unittest
from pathlib import Path
from proxy_edit_pipeline import validate_geometry, write_packet

def sample_layout():
    return {"projection_lock":{
        "canvas":{"width":1920,"height":1080},
        "sphere_center":{"x":1090,"y":330},
        "sphere_radius":280,
        "P_six_oclock":{"x":1090,"y":610},
        "frames":{"H2":{"head_center":{"x":1090,"y":690},"top_face_y":610,"gap_px":0}}
    }}

class CrossProxyTests(unittest.TestCase):
    def test_both_attack_faces_share_exact_P(self):
        p=validate_geometry(sample_layout())
        h2=p["frames"]["H2"]
        self.assertEqual(h2["top_face_y"],p["P_six_oclock"]["y"])
        self.assertEqual(p["sphere_center"]["y"]+p["sphere_radius"],p["P_six_oclock"]["y"])
        self.assertEqual(h2["head_center"]["x"],p["P_six_oclock"]["x"])
    def test_invalid_center_radius_blocks(self):
        bad=sample_layout()
        bad["projection_lock"]["P_six_oclock"]["y"]=611
        with self.assertRaisesRegex(ValueError,"sphere bottom pole is not P"):
            validate_geometry(bad)
    def test_invalid_attack_face_blocks(self):
        bad=sample_layout()
        bad["projection_lock"]["frames"]["H2"]["top_face_y"]=609
        with self.assertRaisesRegex(ValueError,"attack cross face"):
            validate_geometry(bad)
    def test_emits_proxy_sphere_mask_and_two_edit_prompts(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            source=root/"layout.json"
            source.write_text(json.dumps(sample_layout()),encoding="utf-8")
            out=root/"packet"
            result=write_packet(source,out)
            for name in ("00_cross_to_cross_proxy.svg","01_target_cross_replaced_by_sphere.svg",
                         "02_target_cross_edit_mask.svg","03_attacker_edit_mask.svg",
                         "04_final_weapon_preview.svg","edit_target_plus_to_bubble.txt",
                         "edit_attacker_plus_to_radial_hammer.txt","edit_attacker_to_T.txt",
                         "edit_attacker_keep_cross.txt","edit_plan.json"):
                self.assertTrue((out/name).exists(),name)
            plan=json.loads((out/"edit_plan.json").read_text(encoding="utf-8"))
            self.assertEqual(plan["terminal_face_gap_px"],0)
            self.assertEqual(plan["pixel_truth"]["edited_images"],"NOT_RUN")
            self.assertEqual(plan["pixel_truth"]["contact_matrix_images"],"NOT_RUN")
            self.assertIsNone(plan["terminal_face_gap_px"])
            proxy=(out/"00_cross_to_cross_proxy.svg").read_text(encoding="utf-8")
            sphere=(out/"01_target_cross_replaced_by_sphere.svg").read_text(encoding="utf-8")
            self.assertIn('cx="1090" cy="330" r="280"',sphere)
            self.assertIn('x1="1060" y1="610" x2="1120" y2="610"',proxy)
            self.assertIn("EDIT ONLY THE TARGET PLUS-SIGN",(out/"edit_target_plus_to_bubble.txt").read_text(encoding="utf-8"))
            self.assertIn("EDIT ONLY THE ATTACKING PLUS-SIGN",(out/"edit_attacker_plus_to_radial_hammer.txt").read_text(encoding="utf-8"))
            target_mask=(out/"02_target_cross_edit_mask.svg").read_text(encoding="utf-8")
            attacker_mask=(out/"03_attacker_edit_mask.svg").read_text(encoding="utf-8")
            self.assertIn('fill="#ffffff"',target_mask)
            self.assertIn('fill="#000000"',target_mask)
            self.assertIn('fill="#ffffff"',attacker_mask)
            self.assertIn('fill="#000000"',attacker_mask)


    def test_t_final_weapon_uses_one_T_master_not_a_T_pair(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); source=root/"layout.json"
            source.write_text(json.dumps(sample_layout()),encoding="utf-8")
            out=root/"packet"
            write_packet(source,out,final_weapon="T")
            plan=json.loads((out/"edit_plan.json").read_text(encoding="utf-8"))
            preview=(out/"04_T_final_weapon_preview.svg").read_text(encoding="utf-8")
            self.assertEqual(plan["final_weapon"],"T")
            self.assertEqual(plan["method"],"T_MASTER_THEN_T_END_FACE_CONTACT_MATRIX_THEN_STORY_SCENE_GENERATION")
            self.assertEqual(plan["status"],"BLOCKED_UNTIL_T_CONTACT_MATRIX_APPROVED")
            self.assertEqual(plan["stage_gate_status"],"BLOCKED_UNTIL_T_CONTACT_MATRIX_APPROVED")
            self.assertEqual(plan["selected_edit_prompt"],"generate_scene_with_T_master.txt")
            self.assertEqual(plan["required_artifacts"]["stage_a_image"],"A_T_weapon_master.png")
            self.assertIn('x="866" y="585" width="224" height="50"',preview)
            self.assertIn('x="1082" y="587" width="8" height="46"',preview)
            self.assertTrue((out/"00_T_weapon_master_geometry.svg").exists())
            self.assertTrue((out/"00_generate_T_weapon_master.txt").exists())
            self.assertTrue((out/"01_T_terminal_end_face_contact_schematic.svg").exists())
            self.assertTrue((out/"02_target_bubble_edit_mask.svg").exists())
            self.assertTrue((out/"03_attacker_T_protect_mask.svg").exists())
            prompt=(out/"00_generate_T_weapon_master.txt").read_text(encoding="utf-8")
            self.assertIn("exactly ONE T-headed hammer",prompt)
            self.assertIn("NO second hammer",prompt)
            self.assertIn("NO bubble",prompt)
            self.assertNotIn("exactly TWO",prompt)
            scene_prompt=(out/"generate_scene_with_T_master.txt").read_text(encoding="utf-8")
            self.assertIn("weapon-shape reference only",scene_prompt.lower())
            self.assertIn("never draw an upper inverted T",scene_prompt)
            self.assertIn("48-view contact matrix",scene_prompt)
            shape_prompt=(out/"T_weapon_shape_lock.txt").read_text(encoding="utf-8")
            self.assertIn("one single long handle",shape_prompt)
            gate=json.loads((out/"stage_gate.json").read_text(encoding="utf-8"))
            self.assertEqual(gate["status"],"BLOCKED_UNTIL_T_CONTACT_MATRIX_APPROVED")
            self.assertTrue(gate["manual_visual_approval_required"])
            self.assertTrue(gate["do_not_mark_pass_from_prompt_or_svg_alone"])
            self.assertTrue((out/"05_T_silhouette_reference.svg").exists())
            silhouette=(out/"05_T_silhouette_reference.svg").read_text(encoding="utf-8")
            self.assertIn('x="300" y="150" width="400" height="105"',silhouette)
            self.assertIn('x="465" y="255" width="70" height="520"',silhouette)
            self.assertIn("handle itself forms the single stem of the T",plan["shape_contract"])
            self.assertEqual(plan["pixel_truth"]["edited_images"],"NOT_RUN")

    def test_invalid_final_weapon_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); source=root/"layout.json"
            source.write_text(json.dumps(sample_layout()),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"final_weapon"):
                write_packet(source,root/"out",final_weapon="STAR")

if __name__=="__main__": unittest.main()
