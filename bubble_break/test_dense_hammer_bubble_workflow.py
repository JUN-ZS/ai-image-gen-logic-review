import hashlib
import json
import math
import tempfile
import unittest
from pathlib import Path

from bubble_break.dense_hammer_bubble_workflow import (
    BUBBLE_RADIUS,
    CANDIDATE_COUNT,
    FACE_GAP,
    HANDLE_DIAMETER,
    HANDLE_LENGTH,
    HEAD_DIAMETER,
    HEAD_LENGTH,
    build_packet,
    candidate_by_id,
    dot,
    length,
    make_candidates,
    make_stage_a_prompt,
    make_stage_b_prompt,
    make_stage_c_prompt,
    make_stage_d_prompt,
    make_stage_e_prompt,
    make_svg,
    unit,
)


class TestDenseHammerBubbleWorkflow(unittest.TestCase):
    def test_deterministic_dense_non_grid_candidate_set(self):
        a = make_candidates()
        b = make_candidates()
        self.assertEqual(len(a), CANDIDATE_COUNT)
        self.assertEqual([item.candidate_id for item in a], [f"C{i:02d}" for i in range(1, 25)])
        self.assertEqual(a, b)
        self.assertGreater(len({item.azimuth_deg for item in a}), 20)
        self.assertGreater(len({item.polar_deg_to_camera for item in a}), 20)

    def test_every_hammer_faces_inward_and_handle_extends_outward(self):
        for item in make_candidates():
            radial = unit(item.radial_normal)
            face_normal = unit(item.front_face_normal)
            handle = unit(item.handle_direction)
            self.assertAlmostEqual(length(radial), 1.0, places=7)
            self.assertAlmostEqual(dot(radial, face_normal), -1.0, places=6)
            self.assertAlmostEqual(dot(radial, handle), 1.0, places=6)
            self.assertAlmostEqual(length(item.bubble_contact_anchor), BUBBLE_RADIUS, places=5)
            face_offset = tuple(
                item.glowing_face_center[i] - item.bubble_contact_anchor[i]
                for i in range(3)
            )
            self.assertAlmostEqual(length(face_offset), FACE_GAP, places=4)

    def test_hammer_ratio_contract(self):
        self.assertAlmostEqual(HEAD_DIAMETER / (2 * BUBBLE_RADIUS), 0.08, places=7)
        self.assertAlmostEqual(HEAD_LENGTH / HEAD_DIAMETER, 1.5, places=7)
        self.assertAlmostEqual(HANDLE_LENGTH / HEAD_LENGTH, 3.0, places=7)
        self.assertAlmostEqual(HANDLE_DIAMETER / HEAD_DIAMETER, 0.1, places=7)
        for item in make_candidates():
            self.assertAlmostEqual(item.head_stub_length / item.head_diameter, 1.5, places=7)
            self.assertAlmostEqual(item.handle_length / item.head_stub_length, 3.0, places=7)
            self.assertAlmostEqual(item.handle_diameter / item.head_diameter, 0.1, places=7)

    def test_candidate_lookup_is_case_insensitive_and_rejects_unknown(self):
        candidates = make_candidates()
        self.assertEqual(candidate_by_id(candidates, "c17"), candidate_by_id(candidates, "C17"))
        with self.assertRaises(ValueError):
            candidate_by_id(candidates, "C99")

    def test_stage_a_prompt_requires_one_bubble_and_complete_glowing_hammers(self):
        prompt = make_stage_a_prompt(make_candidates()).lower()
        for expected in (
            "exactly 24",
            "single large",
            "complete, separate tool",
            "front circular terminal face",
            "no regular rings",
            "no humans",
            "no huge spark spray",
            "not a grid",
        ):
            self.assertIn(expected, prompt)
        self.assertIn("c24", prompt)

    def test_stage_b_uses_raster_authority_and_removes_other_hammers(self):
        selected = candidate_by_id(make_candidates(), "C17")
        prompt = make_stage_b_prompt(selected, 1.0, 1.0)
        self.assertIn("exact accepted Stage-A image", prompt)
        self.assertIn("raster wins over the proxy coordinate", prompt)
        self.assertIn("all 23 non-selected heads", prompt)
        self.assertIn("No person, hands", prompt)
        self.assertIn("head stub Hs", prompt)
        self.assertIn("handle L", prompt)
        self.assertNotIn("Use C17's proxy coordinates as exact pixel", prompt)

    def test_stage_c_d_e_are_separate_and_preserve_tool(self):
        selected = candidate_by_id(make_candidates(), "C17")
        stage_c = make_stage_c_prompt(selected, 0.65)
        stage_d = make_stage_d_prompt(selected)
        stage_e = make_stage_e_prompt(selected)
        self.assertIn("exactly one full human figure", stage_c.lower())
        self.assertIn("0.650", stage_c)
        self.assertIn("accepted Stage-C image", stage_d)
        self.assertIn("do not move or flip", stage_d.lower())
        self.assertIn("radial fractures", stage_e)
        self.assertIn("at least one clean contact frame", stage_e.lower())
        self.assertIn("unselected hammer", stage_e.lower())

    def test_svg_contains_all_ids_and_selected_candidate(self):
        candidates = make_candidates()
        svg = make_svg(candidates)
        for item in candidates:
            self.assertIn(item.candidate_id, svg)
        self.assertIn("NOT raster evidence", svg)
        self.assertIn("Selected C17", make_svg(candidates, "C17"))

    def test_unselected_packet_does_not_emit_later_stages(self):
        with tempfile.TemporaryDirectory() as directory:
            result = build_packet(Path(directory))
            self.assertEqual(result["candidate_count"], 24)
            self.assertIsNone(result["selected_candidate_id"])
            self.assertEqual(result["image_realization"], "NOT_RUN")
            self.assertNotIn("stage_b_one_hammer_no_person.md", result["outputs"])
            self.assertTrue((Path(directory) / "stage_a_dense_hammer_atlas.md").is_file())
            summary = json.loads((Path(directory) / "packet_summary.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["pixel_audit"], "NOT_RUN")

    def test_selected_packet_emits_stages_b_to_e_and_scale_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            result = build_packet(
                Path(directory),
                selected_id="C17",
                bubble_scale=1.2,
                hammer_scale=0.8,
                person_height_of_bubble=0.55,
            )
            self.assertEqual(result["selected_candidate_id"], "C17")
            for name in (
                "stage_b_one_hammer_no_person.md",
                "stage_c_add_person.md",
                "stage_d_action_refinement.md",
                "stage_e_glow_bubble_break.md",
            ):
                self.assertIn(name, result["outputs"])
                self.assertTrue((Path(directory) / name).is_file())
            manifest = json.loads((Path(directory) / "candidate_manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["scale_changes"]["bubble_scale"], 1.2)
            self.assertEqual(manifest["scale_changes"]["hammer_scale"], 0.8)
            self.assertEqual(manifest["scale_changes"]["person_height_over_bubble_diameter"], 0.55)
            self.assertEqual(manifest["raster_selection_evidence"], "PENDING_REAL_RASTER_REFERENCE")

    def test_source_raster_sha_and_roi_are_recorded(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "stage-a.jpg"
            source.write_bytes(b"fixture-raster-data")
            result = build_packet(
                root / "out",
                selected_id="C17",
                source_raster=source,
                roi=(100, 200, 90, 120),
            )
            manifest = json.loads((root / "out" / "candidate_manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["source_stage_a_sha256"], hashlib.sha256(b"fixture-raster-data").hexdigest())
            self.assertEqual(manifest["selected_raster_roi_xywh"], [100, 200, 90, 120])
            self.assertEqual(manifest["raster_selection_evidence"], "SOURCE_SHA256_AND_USER_ROI_RECORDED")
            stage_b = (root / "out" / "stage_b_one_hammer_no_person.md").read_text(encoding="utf-8")
            self.assertIn(manifest["source_stage_a_sha256"], stage_b)
            self.assertIn("(100, 200, 90, 120)", stage_b)
            self.assertTrue(result["raster_selection_evidence"].startswith("SOURCE_"))

    def test_roi_requires_source_raster_and_bad_scalars_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(ValueError):
                build_packet(root / "bad", selected_id="C17", roi=(1, 2, 3, 4))
            with self.assertRaises(ValueError):
                build_packet(root / "bad-scale", bubble_scale=0.0)
            with self.assertRaises(ValueError):
                build_packet(root / "bad-source", source_raster=root / "missing.jpg")


if __name__ == "__main__":
    unittest.main()
