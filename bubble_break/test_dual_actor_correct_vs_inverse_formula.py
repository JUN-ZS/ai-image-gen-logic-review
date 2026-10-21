#!/usr/bin/env python3
import math
import unittest
from dual_actor_correct_vs_inverse_formula import (
    DEFAULT_TOL_DEG,
    build_matrix,
    check_contact,
    face_for_mode,
    make_trial,
    unit,
)

class TestDualActorFormula(unittest.TestCase):
    def test_spec_demo_correct_and_inverse(self):
        n = (1.0, 0.0, 0.0)
        correct = check_contact(n, (-1.0, 0.0, 0.0))
        inverse = check_contact(n, (1.0, 0.0, 0.0))
        self.assertTrue(correct["pass"])
        self.assertFalse(inverse["pass"])
        self.assertAlmostEqual(correct["alignment"], 1.0, places=6)
        self.assertAlmostEqual(inverse["alignment"], -1.0, places=6)

    def test_tolerance_boundary(self):
        n = (1.0, 0.0, 0.0)
        # f nearly -n within 8 deg should pass
        ang = math.radians(7.0)
        f = (-math.cos(ang), math.sin(ang), 0.0)
        self.assertTrue(check_contact(n, f, 8.0)["pass"])
        ang2 = math.radians(9.0)
        f2 = (-math.cos(ang2), math.sin(ang2), 0.0)
        self.assertFalse(check_contact(n, f2, 8.0)["pass"])

    def test_camera_does_not_appear_in_alignment(self):
        n = unit((1.0, 1.0, 0.0))
        c = check_contact(n, face_for_mode(n, "CORRECT"))
        # alignment independent of any camera string
        self.assertTrue(c["pass"])
        self.assertNotIn("camera", c)

    def test_trial_assigns_pass_fail_roles(self):
        t = make_trial((0.0, 0.0, 1.0), True, "side_profile_85mm", "dive_overhead", "ground_sweep", 0)
        self.assertTrue(t.checks[t.correct_actor]["pass"])
        self.assertFalse(t.checks[t.inverse_actor]["pass"])
        heights = {a.height for a in t.actors}
        self.assertEqual(heights, {"airborne", "ground_low"})

    def test_alternate_which_actor_is_correct(self):
        t1 = make_trial((1.0, 0.0, 0.0), True, "low_hero_24mm", "spin_slash", "kneel_thrust", 1)
        t2 = make_trial((1.0, 0.0, 0.0), False, "low_hero_24mm", "spin_slash", "kneel_thrust", 1)
        self.assertEqual(t1.correct_actor, "A_AIR")
        self.assertEqual(t2.correct_actor, "B_GROUND")

    def test_matrix_honest_gates(self):
        m = build_matrix(limit=12)
        self.assertEqual(m["acceptance_gate"]["image_realization"], "NOT_RUN")
        self.assertEqual(m["acceptance_gate"]["pixel_audit"], "NOT_RUN")
        self.assertTrue(m["demo"]["CORRECT"]["pass"])
        self.assertFalse(m["demo"]["INVERSE_NEGATIVE_CONTROL"]["pass"])
        self.assertEqual(len(m["trials"]), 12)

if __name__ == "__main__":
    unittest.main()
