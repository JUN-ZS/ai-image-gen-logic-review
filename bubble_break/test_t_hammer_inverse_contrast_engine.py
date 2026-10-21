import unittest
from bubble_break.t_hammer_inverse_contrast_engine import (
    AIR_MOVES, GROUND_MOVES, CAMERAS, AIR_OUTWARD, GROUND_OUTWARD,
    build_contacts, build_matrix, camera_frame, dot, norm, unit, mul,
    make_variant, render_proxy_svg,
)


class TestTHammerInverseContrast(unittest.TestCase):
    def test_matrix_size_and_unique_variant_ids(self):
        matrix = build_matrix()
        self.assertEqual(len(AIR_MOVES), 4)
        self.assertEqual(len(GROUND_MOVES), 4)
        self.assertEqual(len(CAMERAS), 12)
        self.assertEqual(matrix["counts"]["total_variants"], 192)
        ids = [x["variant_id"] for x in matrix["variants"]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_positive_face_is_correct_terminal_cap_contact(self):
        c = build_contacts()["AIRBORNE_CORRECT"]
        self.assertEqual(c["contact_surface"], "TERMINAL_END_FACE")
        self.assertEqual(c["first_contact_class"], "CORRECT_TERMINAL_FACE")
        self.assertAlmostEqual(c["normal_dot_sphere"], -1.0, places=7)
        self.assertAlmostEqual(c["head_axis_dot_inward_normal"], 1.0, places=7)
        self.assertAlmostEqual(c["handle_dot_head_axis"], 0.0, places=7)

    def test_ground_negative_control_is_wrong_cheek_first_never_pass(self):
        c = build_contacts()["GROUND_LOW_WRONG"]
        self.assertEqual(c["contact_surface"], "BROAD_CHEEK_SIDEWALL")
        self.assertEqual(c["first_contact_class"], "INTENTIONAL_WRONG_FACE_FIRST")
        self.assertAlmostEqual(c["normal_dot_sphere"], -1.0, places=7)
        self.assertAlmostEqual(c["head_axis_dot_inward_normal"], 0.0, places=7)
        self.assertAlmostEqual(c["handle_dot_head_axis"], 0.0, places=7)
        wrong = [v for v in build_matrix()["variants"]]
        self.assertTrue(all(v["expected_acceptance"]["grounded_wrong_contact"] == "EXPECTED_FAIL_NEGATIVE_CONTROL" for v in wrong))

    def test_two_fighters_have_distinct_surface_points_on_visible_hemisphere(self):
        a, g = unit(AIR_OUTWARD), unit(GROUND_OUTWARD)
        self.assertGreater(norm(tuple(a[i]-g[i] for i in range(3))), 0.7)
        self.assertLess(a[1], 0.0)
        self.assertLess(g[1], 0.0)
        self.assertGreater(a[2], 0.0)  # airborne-side strike pole
        self.assertLess(g[2], 0.0)    # ground-low strike pole

    def test_camera_change_does_not_change_contacts(self):
        matrix = build_matrix()
        chosen = [v for v in matrix["variants"] if v["air_move"]["move_id"] == AIR_MOVES[0].move_id and v["ground_move"]["move_id"] == GROUND_MOVES[0].move_id]
        self.assertEqual(len(chosen), 12)
        baseline = chosen[0]["contact_geometry"]
        for variant in chosen[1:]:
            geo = variant["contact_geometry"]
            for role in ("airborne_positive_control", "grounded_negative_control"):
                for key in ("sphere_outward_normal", "contact_point", "head_long_axis", "contact_surface", "contact_surface_normal"):
                    self.assertEqual(geo[role][key], baseline[role][key])
            self.assertFalse(geo["camera_changes_contact_geometry"])

    def test_distinct_attack_actions_are_not_collapsed_into_one_motion(self):
        ids = set()
        for v in build_matrix()["variants"]:
            ids.add((v["air_move"]["move_id"], v["ground_move"]["move_id"]))
            self.assertNotEqual(v["air_move"]["move_id"], v["ground_move"]["move_id"])
            self.assertIn("AIRBORNE", v["contact_geometry"]["airborne_positive_control"]["role"])
            self.assertIn("GROUND_LOW", v["contact_geometry"]["grounded_negative_control"]["role"])
        self.assertEqual(len(ids), 16)

    def test_prompt_separates_positive_and_negative_controls(self):
        v = make_variant(AIR_MOVES[0], GROUND_MOVES[0], CAMERAS[0])
        pair = v["prompts"]["paired_contrast_scene"]
        positive = v["prompts"]["positive_correct_face_crop"]
        negative = v["prompts"]["negative_wrong_face_crop"]
        self.assertIn("EXACTLY TWO adult fighters", pair)
        self.assertIn("AIRBORNE", pair)
        self.assertIn("INTENTIONAL INVERSE / NEGATIVE CONTROL", pair)
        self.assertIn("ONLY the narrow flat terminal end cap", positive)
        self.assertIn("BROAD CHEEK/SIDEWALL", negative.upper())
        self.assertIn("never be scored as a successful strike", negative.lower())
        self.assertEqual(v["expected_acceptance"]["paired_scene_as_a_whole"], "CONTRAST_EXPERIMENT_NOT_A_SINGLE_PASS")

    def test_correct_and_wrong_roles_are_not_swapped_by_variants(self):
        for v in build_matrix()["variants"]:
            self.assertEqual(v["contact_geometry"]["airborne_positive_control"]["contact_surface"], "TERMINAL_END_FACE")
            self.assertEqual(v["contact_geometry"]["grounded_negative_control"]["contact_surface"], "BROAD_CHEEK_SIDEWALL")
            self.assertEqual(v["expected_acceptance"]["airborne_correct_contact"], "REVIEW_FOR_PASS")
            self.assertEqual(v["expected_acceptance"]["grounded_wrong_contact"], "EXPECTED_FAIL_NEGATIVE_CONTROL")

    def test_camera_basis_is_orthonormal_and_dutch_roll_varies_view_only(self):
        for c in CAMERAS:
            pos, fw, right, up = camera_frame(c)
            for v in (pos, fw, right, up):
                self.assertAlmostEqual(norm(v), 1.0, places=6)
            self.assertAlmostEqual(dot(fw, right), 0.0, places=6)
            self.assertAlmostEqual(dot(fw, up), 0.0, places=6)
            self.assertAlmostEqual(dot(right, up), 0.0, places=6)
        self.assertNotEqual(camera_frame(CAMERAS[0]), camera_frame(CAMERAS[6]))

    def test_proxy_explicitly_not_pixel_proof(self):
        v = make_variant(AIR_MOVES[1], GROUND_MOVES[2], CAMERAS[4])
        svg = render_proxy_svg(v)
        self.assertIn('data-image-realization="NOT_RUN"', svg)
        self.assertIn("schematic only, NOT pixel proof", svg)
        self.assertIn("AIRBORNE", svg)
        self.assertIn("GROUND LOW", svg)

    def test_gate_remains_not_run_until_actual_raster_review(self):
        m = build_matrix()
        self.assertEqual(m["acceptance_gate"]["image_realization"], "NOT_RUN")
        self.assertEqual(m["acceptance_gate"]["pixel_audit"], "NOT_RUN")
        self.assertEqual(m["acceptance_gate"]["positive_review_pass_count"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
