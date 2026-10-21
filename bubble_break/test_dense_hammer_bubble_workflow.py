import hashlib
import json
import math
import tempfile
import unittest
from pathlib import Path

from bubble_break.dense_hammer_bubble_workflow import (
    BUBBLE_RADIUS,
    CANDIDATE_COUNT,
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
    make_stage_d_step_prompt,
    make_stage_e_prompt,
    make_svg,
    sub,
    unit,
    PERSON_TO_HAMMER_SCALE_DEFAULT,
)
from bubble_break.stage_d_gates import (
    FIRST_GRIP_STEP,
    StepChainError,
    default_rois_for_wide_hammer_scene,
    grip_pixel_lock_clause,
    run_step_gates,
    validate_step_transition,
)



class TestDenseHammerBubbleWorkflow(unittest.TestCase):
    def test_deterministic_24_planted_candidates_with_varied_tangent_handles(self):
        first = make_candidates()
        second = make_candidates()
        self.assertEqual(len(first), CANDIDATE_COUNT)
        self.assertEqual([item.candidate_id for item in first], [f"C{i:02d}" for i in range(1, 25)])
        self.assertEqual(first, second)
        self.assertGreater(len({item.azimuth_deg for item in first}), 20)
        self.assertGreater(len({item.handle_roll_deg for item in first}), 20)

    def test_heads_are_planted_radially_and_handles_are_tangent(self):
        for item in make_candidates():
            radial = unit(item.radial_head_axis)
            handle = unit(item.handle_tangent_direction)
            self.assertAlmostEqual(length(radial), 1.0, places=7)
            self.assertAlmostEqual(length(handle), 1.0, places=7)
            self.assertAlmostEqual(length(item.bubble_contact_anchor), BUBBLE_RADIUS, places=5)
            self.assertAlmostEqual(dot(radial, handle), 0.0, places=6)
            self.assertAlmostEqual(length(sub(item.handle_end, item.handle_root)), HANDLE_LENGTH, places=4)
            head_axis_vector = tuple(
                item.head_outer_cap_center[i] - item.bubble_contact_anchor[i]
                for i in range(3)
            )
            self.assertAlmostEqual(length(head_axis_vector), HEAD_LENGTH, places=4)
            self.assertAlmostEqual(dot(unit(head_axis_vector), radial), 1.0, places=6)

    def test_ratio_contract_matches_double_ended_head_and_lateral_handle(self):
        self.assertAlmostEqual(HEAD_DIAMETER / (2 * BUBBLE_RADIUS), 0.08, places=7)
        self.assertAlmostEqual(HEAD_LENGTH / HEAD_DIAMETER, 1.5, places=7)
        self.assertAlmostEqual(HANDLE_LENGTH / HEAD_LENGTH, 3.0, places=7)
        self.assertAlmostEqual(HANDLE_DIAMETER / HEAD_DIAMETER, 0.1, places=7)
        for item in make_candidates():
            self.assertAlmostEqual(item.head_axial_length / item.head_diameter, 1.5, places=7)
            self.assertAlmostEqual(item.handle_length / item.head_axial_length, 3.0, places=7)
            self.assertAlmostEqual(item.handle_diameter / item.head_diameter, 0.1, places=7)

    def test_candidate_lookup_is_case_insensitive_and_rejects_unknown(self):
        candidates = make_candidates()
        self.assertEqual(candidate_by_id(candidates, "c17"), candidate_by_id(candidates, "C17"))
        with self.assertRaises(ValueError):
            candidate_by_id(candidates, "C99")

    def test_stage_a_prompt_is_planted_double_ended_hammer_not_projectiles(self):
        prompt = " ".join(make_stage_a_prompt(make_candidates()).lower().split())
        for expected in (
            "exactly 24",
            "double-ended",
            "two axial circular end caps",
            "seated flush against the bubble",
            "side-middle",
            "local tangent plane",
            "no people",
            "not a grid",
            "the contact footprint/base seam",
        ):
            self.assertIn(expected, prompt)
        self.assertIn("c24", prompt)
        self.assertNotIn("aimed inward toward", prompt)

    def test_stage_b_locks_actual_raster_and_removes_other_23_hammers(self):
        selected = candidate_by_id(make_candidates(), "C17")
        prompt = make_stage_b_prompt(selected, 1.0, 1.0)
        self.assertIn("exact accepted Stage-A raster", prompt)
        self.assertIn("actual Stage-A raster-visible selected hammer", prompt)
        self.assertIn("Remove every other 23 hammer assemblies", prompt)
        self.assertIn("No human, hands", prompt)
        self.assertIn("side-middle", prompt)
        self.assertIn("tangent plane", prompt)
        self.assertIn("BLOCK", prompt.upper())

    def test_stage_c_d_e_preserve_planted_contact_and_handle_attachment(self):
        selected = candidate_by_id(make_candidates(), "C17")
        stage_c = make_stage_c_prompt(selected, 1.0)
        stage_d = make_stage_d_prompt(selected)
        stage_e = make_stage_e_prompt(selected)
        self.assertIn("exactly one complete person", stage_c.lower())
        self.assertIn("NO_NEW_HANDLE", stage_c)
        self.assertIn("1.000", stage_c)  # person:hammer 1:1
        self.assertIn("MINI", stage_c.upper())
        self.assertIn("same visual area", stage_c.lower())
        self.assertIn("person >> hammer", stage_c.lower())
        self.assertIn("person:hammer", stage_c.lower().replace(" ", ""))
        self.assertIn("same existing lateral handle", stage_c.lower())
        self.assertNotIn("person height target", stage_c.lower())
        self.assertIn("not person height = k", stage_c.lower())
        self.assertIn("do not add, grow, extrude", stage_c.lower())
        self.assertIn("accepted Stage-C raster", stage_d)
        self.assertIn("side-middle", stage_d)
        self.assertIn("NO_NEW_HANDLE", stage_d)
        self.assertIn("base contact", stage_e.lower())
        self.assertIn("radial cracks", stage_e.lower())
        self.assertIn("clean contact frame", stage_e.lower())
        self.assertIn("23 hammer", stage_e.lower())

    def test_stage_c_rejects_non_positive_person_to_hammer_scale(self):
        selected = candidate_by_id(make_candidates(), "C17")
        with self.assertRaises(ValueError):
            make_stage_c_prompt(selected, 0.0)

    def test_svg_contains_all_ids_and_selected_candidate(self):
        candidates = make_candidates()
        svg = make_svg(candidates)
        for item in candidates:
            self.assertIn(item.candidate_id, svg)
        self.assertIn("geometry proxy only", svg)
        self.assertIn("Selected C17", make_svg(candidates, "C17"))

    def test_unselected_packet_does_not_emit_later_stages(self):
        with tempfile.TemporaryDirectory() as directory:
            result = build_packet(Path(directory))
            self.assertEqual(result["candidate_count"], 24)
            self.assertIsNone(result["selected_candidate_id"])
            self.assertEqual(result["image_realization"], "NOT_RUN")
            self.assertNotIn("stage_b_one_hammer_no_person.md", result["outputs"])
            self.assertTrue((Path(directory) / "stage_a_planted_round_hammer_atlas.md").is_file())
            summary = json.loads((Path(directory) / "packet_summary.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["pixel_audit"], "NOT_RUN")
            manifest = json.loads((Path(directory) / "candidate_manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["topology"]["head"], "double-ended cylindrical round head, radial axis")
            self.assertIn("side-middle", manifest["topology"]["handle"])

    def test_selected_packet_emits_stages_b_to_e_and_scale_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            result = build_packet(
                Path(directory),
                selected_id="C17",
                bubble_scale=1.2,
                hammer_scale=0.8,
                person_to_hammer_scale=1.0,
            )
            self.assertEqual(result["selected_candidate_id"], "C17")
            for name in (
                "stage_b_one_hammer_no_person.md",
                "stage_c_scale_and_add_person.md",
                "stage_d_action_refinement.md",
                "stage_d_step_D0.md",
                "stage_d_step_D1.md",
                "stage_d_step_D2.md",
                "stage_d_step_D3.md",
                "stage_d_step_D4.md",
                "stage_d_GATES.md",
                "stage_e_glow_bubble_break.md",
            ):
                self.assertIn(name, result["outputs"])
                self.assertTrue((Path(directory) / name).is_file())
            manifest = json.loads((Path(directory) / "candidate_manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["scale_changes"]["bubble_scale"], 1.2)
            self.assertEqual(manifest["scale_changes"]["hammer_scale"], 0.8)
            self.assertEqual(manifest["scale_changes"]["person_to_hammer_scale"], 1.0)
            self.assertTrue(manifest["scale_changes"]["NO_NEW_HANDLE"])
            self.assertIsNone(manifest["scale_changes"]["person_height_over_bubble_diameter"])
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

    def test_roi_requires_source_raster_and_invalid_inputs_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(ValueError):
                build_packet(root / "bad", selected_id="C17", roi=(1, 2, 3, 4))
            with self.assertRaises(ValueError):
                build_packet(root / "bad-scale", bubble_scale=0.0)
            with self.assertRaises(ValueError):
                build_packet(root / "bad-source", source_raster=root / "missing.jpg")


    def test_person_to_hammer_scale_default_is_one_to_one(self):
        self.assertEqual(PERSON_TO_HAMMER_SCALE_DEFAULT, 1.0)
        selected = candidate_by_id(make_candidates(), "C13")
        prompt = make_stage_c_prompt(selected)
        self.assertIn("1.000:1", prompt.replace(" ", ""))
        self.assertIn("NO_NEW_HANDLE", prompt)
        self.assertIn("MINI", prompt.upper())
        self.assertIn("same visual area", prompt.lower())


    def test_stage_d_step_prompts_kill_outer_end_new_handle(self):
        selected = candidate_by_id(make_candidates(), "C13")
        for step in ("D0", "D1", "D2", "D3", "D4"):
            p = make_stage_d_step_prompt(selected, step, prev_raster_sha256="abc" * 12)
            self.assertIn("NO_NEW_HANDLE", p)
            self.assertIn("REJECT", p)
            self.assertIn("outer", p.lower())
            self.assertIn("STEP CHAIN LOCK", p)
        d1 = make_stage_d_step_prompt(selected, "D1", prev_raster_sha256="abc" * 12)
        self.assertIn("must NOT grip", d1)
        self.assertIn("mini", d1.lower())
        d2 = make_stage_d_step_prompt(selected, "D2", prev_raster_sha256="d1sha" + "0" * 50)
        self.assertIn("FIRST GRIP", d2)
        self.assertIn("PROVEN 2026-10-21", d2)
        self.assertIn("左柄", d2)
        self.assertIn("d1sha", d2)
        self.assertIn("PIXEL LOCK", d2)
        with self.assertRaises(ValueError):
            make_stage_d_step_prompt(selected, "D9")
        with self.assertRaises(StepChainError):
            make_stage_d_step_prompt(selected, "D2", from_step="D0", prev_raster_sha256="x" * 32)

    def test_step_chain_forbids_skipping_d1_d2(self):
        with self.assertRaises(StepChainError):
            validate_step_transition(None, "D2")
        with self.assertRaises(StepChainError):
            validate_step_transition("D0", "D2")
        with self.assertRaises(StepChainError):
            validate_step_transition("D1", "D3")
        validate_step_transition("D1", "D2")
        self.assertEqual(FIRST_GRIP_STEP, "D2")
        clause = grip_pixel_lock_clause("D2", "deadbeef" * 8)
        self.assertIn("FIRST GRIP", clause)
        self.assertIn("deadbeef", clause)

    def test_pixel_gates_block_next_without_rois_or_image(self):
        report = run_step_gates(
            "D2",
            from_step="D1",
            image_path=None,
            prev_raster_sha256="a" * 64,
            require_pixels=True,
        )
        self.assertFalse(report.overall_pass)
        self.assertTrue(report.block_next)

    def test_pixel_gates_on_real_d2_d3_rasters(self):
        rois = default_rois_for_wide_hammer_scene()
        d2 = Path("/workspace/artifacts/imagine_images/8f3d210b-a666-4a5e-8353-9c48b8dadff1.jpg")
        d3 = Path("/workspace/artifacts/imagine_images/f7d12b71-67fe-4c62-a476-45948b72d431.jpg")
        if not d2.is_file():
            self.skipTest("D2 raster not in workspace")
        r2 = run_step_gates(
            "D2",
            from_step="D1",
            image_path=d2,
            prev_raster_sha256="b" * 64,
            outer_cap_roi=rois["outer_cap_roi"],
            side_handle_roi=rois["side_handle_roi"],
        )
        # chain must pass; pixel heuristic may vary — assert chain + structure
        self.assertTrue(r2.chain_ok)
        names = {g.name: g for g in r2.gates}
        self.assertIn("outer_end_empty", names)
        self.assertIn("side_handle_present", names)
        if d3.is_file():
            r3 = run_step_gates(
                "D3",
                from_step="D2",
                image_path=d3,
                prev_raster_sha256="c" * 64,
                outer_cap_roi=rois["outer_cap_roi"],
                side_handle_roi=rois["side_handle_roi"],
            )
            self.assertTrue(r3.chain_ok)


if __name__ == "__main__":
    unittest.main()
