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


    def test_t_final_weapon_is_selectable_and_keeps_P_locked(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); source=root/"layout.json"
            source.write_text(json.dumps(sample_layout()),encoding="utf-8")
            out=root/"packet"
            write_packet(source,out,final_weapon="T")
            plan=json.loads((out/"edit_plan.json").read_text(encoding="utf-8"))
            preview=(out/"04_final_weapon_preview.svg").read_text(encoding="utf-8")
            self.assertEqual(plan["final_weapon"],"T")
            self.assertEqual(plan["selected_edit_prompt"],"edit_attacker_to_T.txt")
            self.assertIn('x="978" y="618" width="224" height="50"',preview)
            self.assertIn("T-shaped hammer", (out/"edit_attacker_to_T.txt").read_text(encoding="utf-8"))
            prompt=(out/"edit_attacker_to_T.txt").read_text(encoding="utf-8")
            self.assertIn("handle itself forms the single stem of the T",prompt)
            self.assertIn("BROAD UPPER PLANE",prompt)
            self.assertTrue((out/"05_T_silhouette_reference.svg").exists())
            silhouette=(out/"05_T_silhouette_reference.svg").read_text(encoding="utf-8")
            self.assertIn('x="300" y="150" width="400" height="105"',silhouette)
            self.assertIn('x="465" y="255" width="70" height="520"',silhouette)
            self.assertIn("the handle itself is the only stem",plan["shape_contract"])

    def test_invalid_final_weapon_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); source=root/"layout.json"
            source.write_text(json.dumps(sample_layout()),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"final_weapon"):
                write_packet(source,root/"out",final_weapon="STAR")

if __name__=="__main__": unittest.main()
