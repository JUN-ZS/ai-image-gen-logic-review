#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, tempfile, unittest
from pathlib import Path
from frame_pipeline import FRAME_IDS, build_packets, compile_frame_set, write_packet

def sample():
    return {"story_id":"TEST-001","root_sin":"Identity Ownership",
      "root_mechanism":"The shell suppresses self-chosen names.","human_cost":"Residents lose autonomy.",
      "axes":{"environment":{"id":"ENV01","description":"a drowned archive"},
      "scale":{"id":"SCALE03","description":"a giant bubble in a chamber"},
      "shell":{"id":"SHELL01","description":"an iridescent membrane"},
      "palette":{"id":"PAL01","description":"cold silver, cyan and amber"},
      "fracture":{"id":"FRAC01","description":"radial cracks from one impact point"}}}

class FramePipelineTests(unittest.TestCase):
    def test_three_separate_single_frame_prompts(self):
        p=compile_frame_set(sample())
        self.assertEqual(p["frame_order"],["H0","H2","H3"])
        for prompt in p["prompts"].values():
            self.assertIn("ONE standalone cinematic frame",prompt)
            self.assertIn("not a collage",prompt.lower())
            self.assertIn("No writing",prompt)
            self.assertIn("broad, flat polygonal sledgehammer striking faces",prompt)
    def test_h0_has_gap_and_no_cracks(self):
        p=compile_frame_set(sample())["prompts"]["H0"]
        self.assertIn("zero cracks",p)
        self.assertIn("clearly visible continuous band of empty air",p)
        self.assertNotIn("FIRST touches",p)
    def test_h2_flat_face_contacts_exact_bottom_point(self):
        p=compile_frame_set(sample())["prompts"]["H2"]
        self.assertIn("FIRST touches the exact six-o'clock bottom point P",p)
        self.assertIn("only the single upper-facing flat polygon",p)
        self.assertIn("radiate outward from that one contact center",p)
        self.assertIn("shaft does not touch shell",p)
    def test_h3_preserves_residents_and_scene(self):
        p=compile_frame_set(sample())["prompts"]["H3"]
        self.assertIn("No continuous unbroken membrane remains",p)
        self.assertIn("All residents remain alive and uninjured",p)
        self.assertIn("same swing path",p)
    def test_same_shot_lock_is_deterministic(self):
        a,b=compile_frame_set(sample()),compile_frame_set(sample())
        self.assertEqual(a["shot_lock_id"],b["shot_lock_id"])
        self.assertIn("same horizon",a["prompts"]["H0"])
        for fid in FRAME_IDS: self.assertIn("same horizon, vanishing lines",a["prompts"][fid])
    def test_prompt_pass_never_claims_pixel_pass(self):
        p=compile_frame_set(sample())
        self.assertEqual(p["prompt_contract_status"],"PROMPT_CONTRACT_PASS")
        self.assertEqual(p["image_realization"],"NOT_RUN")
        self.assertEqual(p["pixel_audit_status"],"NOT_RUN")
        self.assertTrue(all(x["result"]=="UNASSESSED" for x in p["pixel_audit_checks"]))
    def test_writes_three_prompts_manifest_and_audit(self):
        with tempfile.TemporaryDirectory() as td:
            summary=write_packet(compile_frame_set(sample()),Path(td))
            d=Path(summary["directory"])
            self.assertTrue((d/"H0_pre_impact.txt").exists())
            self.assertTrue((d/"H2_first_contact_anchor.txt").exists())
            self.assertTrue((d/"H3_post_impact.txt").exists())
            self.assertTrue((d/"manifest.json").exists())
            self.assertTrue((d/"pixel_audit.md").exists())
            self.assertTrue((d/"H0_pre_impact_geometry.svg").exists())
            self.assertTrue((d/"H2_first_contact_anchor_geometry.svg").exists())
            self.assertTrue((d/"H3_post_impact_geometry.svg").exists())
            layout=json.loads((d/"layout.json").read_text(encoding="utf-8"))
            projection=layout["projection_lock"]
            self.assertEqual(projection["P_six_oclock"],{"x":1090,"y":610})
            self.assertEqual(projection["frames"]["H0"]["gap_px"],50)
            self.assertEqual(projection["frames"]["H2"]["gap_px"],0)
            self.assertEqual(projection["frames"]["H3"]["gap_px"],-15)
            h0_svg=(d/"H0_pre_impact_geometry.svg").read_text(encoding="utf-8")
            h2_svg=(d/"H2_first_contact_anchor_geometry.svg").read_text(encoding="utf-8")
            h3_svg=(d/"H3_post_impact_geometry.svg").read_text(encoding="utf-8")
            impact_glint='r="9" fill="#ffffff"'
            self.assertNotIn(impact_glint,h0_svg)
            self.assertIn(impact_glint,h2_svg)
            self.assertNotIn(impact_glint,h3_svg)
            self.assertTrue(all(Path(d/name).exists() for name in layout["geometry_files"].values()))
    def test_batch_reads_jsonl(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); source=root/"stories.jsonl"
            source.write_text(json.dumps(sample())+"\n",encoding="utf-8")
            out= root/"out"; result=build_packets(source,out,limit=1)
            self.assertEqual(result["written_story_packets"],1)
            self.assertTrue((out/"batch_manifest.json").exists())


    def test_t_topology_replaces_radial_lock_in_prompt_and_geometry(self):
        p=compile_frame_set(sample(),weapon_topology="T")
        self.assertEqual(p["canonical_weapon"],"WEAPON_T")
        self.assertEqual(p["prompt_contract_status"],"PROMPT_CONTRACT_PASS")
        self.assertIn("broad upper plane of the horizontal crossbar",p["active_striking_surface"])
        self.assertIn("horizontal crossbar",p["weapon_shape_contract"])
        self.assertIn("midpoint",p["weapon_shape_contract"])
        self.assertEqual(p["workflow"]["realization_stage_gate"],"BLOCKED_UNTIL_T_WEAPON_MASTER_APPROVED")
        self.assertEqual(p["workflow"]["required_stage_a_artifact"],"A_T_weapon_master.png")
        self.assertTrue(p["workflow"]["do_not_claim_scene_pass_from_master_or_svg"])
        for prompt in p["prompts"].values():
            self.assertIn("WEAPON_TOPOLOGY_ID=WEAPON_T",prompt)
            positive=prompt.split("NEGATIVE PROMPT:",1)[0]
            self.assertIn("T silhouette",positive)
            negative=prompt.split("NEGATIVE PROMPT:",1)[1]
            self.assertIn("horizontal rectangular crossbar",positive)
            self.assertIn("handle itself forms the single stem",positive)
            self.assertNotIn("spherical multi-face hammer head",positive)
            self.assertNotIn("polygonal sledgehammer striking face",positive)
            self.assertIn("radial spherical hammer head",negative)
            self.assertNotIn("conventional rectangular hammer",negative)
        with tempfile.TemporaryDirectory() as temp:
            summary=write_packet(p,Path(temp))
            d=Path(summary["directory"])
            manifest=json.loads((d/"manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["weapon_topology"],"T")
            self.assertEqual(manifest["workflow"]["realization_stage_gate"],"BLOCKED_UNTIL_T_WEAPON_MASTER_APPROVED")
            gate=json.loads((d/"stage_gate.json").read_text(encoding="utf-8"))
            self.assertEqual(gate["status"],"BLOCKED_UNTIL_T_WEAPON_MASTER_APPROVED")
            audit=(d/"pixel_audit.md").read_text(encoding="utf-8")
            self.assertIn("T-topology real-image work must start with an actual isolated single-T weapon master",audit)
            self.assertIn("Prompt text and vector SVG are not pixel evidence",audit)
            svg=(d/"H2_first_contact_anchor_geometry.svg").read_text(encoding="utf-8")
            self.assertIn('cx="1090" cy="610"',svg)
            self.assertIn('data-contact-p="1090,610"',svg)
            self.assertIn('x1="690" y1="920" x2="1090" y2="668"',svg)


if __name__=="__main__": unittest.main()
