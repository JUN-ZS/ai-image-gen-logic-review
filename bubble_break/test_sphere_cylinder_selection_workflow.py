import json
import math
import tempfile
import unittest
from pathlib import Path

from bubble_break.sphere_cylinder_selection_workflow import (
    CAMERA_DIRECTION,
    SPHERE_RADIUS,
    Candidate,
    build_packet,
    candidate_by_id,
    dot,
    length,
    make_candidates,
    make_stage1_prompt,
    make_stage2_prompt,
    make_stage3_prompt,
    make_stage4_prompt,
    make_svg,
    unit,
)


class TestSphereCylinderSelectionWorkflow(unittest.TestCase):
    def test_deterministic_25_candidate_atlas(self):
        first = make_candidates()
        second = make_candidates()
        self.assertEqual(len(first), 25)
        self.assertEqual([c.candidate_id for c in first], [f"C{i:02d}" for i in range(1, 26)])
        self.assertEqual(first, second)

    def test_anchors_on_sphere_and_axes_unit_with_exact_tilt(self):
        for candidate in make_candidates():
            self.assertAlmostEqual(length(candidate.anchor), SPHERE_RADIUS, places=4)
            normal = unit(candidate.outward_normal)
            axis = unit(candidate.cylinder_axis)
            self.assertAlmostEqual(length(normal), 1.0, places=7)
            self.assertAlmostEqual(length(axis), 1.0, places=7)
            self.assertAlmostEqual(
                dot(normal, axis),
                math.cos(math.radians(candidate.tilt_deg)),
                places=6,
            )
            self.assertGreater(dot(axis, CAMERA_DIRECTION), 0.0)

    def test_candidate_id_lookup_is_stable_and_case_insensitive(self):
        candidates = make_candidates()
        self.assertEqual(candidate_by_id(candidates, "c07"), candidate_by_id(candidates, "C07"))
        with self.assertRaises(ValueError):
            candidate_by_id(candidates, "C99")

    def test_stage1_is_only_short_stubs_and_interface_glow(self):
        prompt = make_stage1_prompt(make_candidates()).lower()
        self.assertIn("short, stubby cylindrical projections", prompt)
        self.assertIn("base interface", prompt)
        self.assertIn("no people", prompt)
        self.assertIn("no hands", prompt)
        self.assertIn("no handles", prompt)
        self.assertIn("no cracks", prompt)
        self.assertIn("exactly 25", prompt)

    def test_selected_pipeline_locks_anchor_and_removes_all_other_stubs(self):
        selected = candidate_by_id(make_candidates(), "C07")
        stage2 = make_stage2_prompt(selected)
        stage3 = make_stage3_prompt(selected)
        stage4 = make_stage4_prompt(selected)
        for prompt in (stage2, stage3, stage4):
            self.assertIn("C07", prompt)
            self.assertIn("LOCK", prompt)
            self.assertIn("unselected", prompt.lower())
        self.assertIn("exactly ONE full human figure", stage2)
        self.assertIn("long, straight, rigid handle", stage2)
        self.assertIn("all unselected candidate cylinders", stage2.lower())
        self.assertIn("weight transfer", stage3)
        self.assertIn("radial cracks", stage4)
        self.assertIn("shell rupture", stage4)

    def test_svg_labels_all_candidates_and_selected_candidate(self):
        candidates = make_candidates()
        svg = make_svg(candidates)
        for candidate in candidates:
            self.assertIn(candidate.candidate_id, svg)
        selected_svg = make_svg(candidates, "C07")
        self.assertIn("Selected: C07", selected_svg)

    def test_build_packet_outputs_only_later_stages_after_selection(self):
        with tempfile.TemporaryDirectory() as directory:
            first = build_packet(Path(directory))
            self.assertEqual(first["candidate_count"], 25)
            self.assertEqual(first["image_realization"], "NOT_RUN")
            self.assertNotIn("stage2_attach_handle_person.md", first["outputs"])
            manifest = json.loads((Path(directory) / "candidate_manifest.json").read_text(encoding="utf-8"))
            self.assertIsNone(manifest["selected_candidate_id"])
            self.assertFalse(manifest["selection_lock"])

        with tempfile.TemporaryDirectory() as directory:
            second = build_packet(Path(directory), "C07")
            self.assertEqual(second["selected_candidate_id"], "C07")
            self.assertIn("stage2_attach_handle_person.md", second["outputs"])
            self.assertIn("stage3_action_refine.md", second["outputs"])
            self.assertIn("stage4_contact_bloom_break.md", second["outputs"])
            manifest = json.loads((Path(directory) / "candidate_manifest.json").read_text(encoding="utf-8"))
            self.assertTrue(manifest["selection_lock"])
            self.assertEqual(manifest["selected_candidate_id"], "C07")

    def test_svg_selected_id_is_escaped_and_unknown_selection_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                build_packet(Path(directory), "not-a-candidate")


if __name__ == "__main__":
    unittest.main()
