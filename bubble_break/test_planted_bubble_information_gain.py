from __future__ import annotations

import math
import unittest

from bubble_break.planted_bubble_information_gain import (
    HYPOTHESES,
    classify_failure_hypotheses,
    expected_information_gain_bits,
    recommend_next_experiment,
    shannon_entropy_bits,
)


class PlantedBubbleInformationGainTests(unittest.TestCase):
    def test_entropy_and_perfect_diagnostic(self):
        self.assertAlmostEqual(shannon_entropy_bits({"A": 0.5, "B": 0.5}), 1.0, places=7)
        self.assertAlmostEqual(shannon_entropy_bits({"A": 1.0, "B": 0.0}), 0.0, places=7)
        self.assertAlmostEqual(
            expected_information_gain_bits(
                {"A": 0.5, "B": 0.5}, {"A": 1.0, "B": 0.0}
            ),
            1.0,
            places=7,
        )

    def test_handle_error_recommends_existing_handle_track_audit(self):
        result = recommend_next_experiment([
            "NEW_HANDLE_OR_STUB_DETECTED_OR_UNVERIFIED",
            "SIDE_HANDLE_INSTANCE_CHANGED",
        ])
        self.assertIn("HANDLE_INSTANCE_OR_AXIS_DRIFT", result["identified_failure_hypotheses"])
        self.assertEqual(
            result["selected_experiment"]["action_id"],
            "EXISTING_HANDLE_TRACK_AUDIT",
        )
        self.assertEqual(result["calibration_status"], "UNVALIDATED_ENGINEERING_PRIORS")
        self.assertIn("cannot override a hard gate", result["hard_rule"])

    def test_crack_error_recommends_fracture_causality_audit(self):
        result = recommend_next_experiment([
            "CRACKS_DO_NOT_ORIGINATE_AT_P",
            "SHELL_STATE_WRONG_FOR_STAGE",
        ])
        self.assertIn("SHELL_FRACTURE_CAUSALITY_FAILURE", result["identified_failure_hypotheses"])
        self.assertEqual(
            result["selected_experiment"]["action_id"],
            "CRACK_ORIGIN_AND_OUTWARD_FRONT_AUDIT",
        )

    def test_ranking_is_deterministic_finite_and_cost_adjusted(self):
        first = recommend_next_experiment([])
        second = recommend_next_experiment([])
        self.assertEqual(
            [x["action_id"] for x in first["ranked_experiments"]],
            [x["action_id"] for x in second["ranked_experiments"]],
        )
        self.assertTrue(all(math.isfinite(x["information_gain_per_cost"]) for x in first["ranked_experiments"]))
        self.assertTrue(all(x["expected_information_gain_bits"] >= 0 for x in first["ranked_experiments"]))
        self.assertEqual(set(first["posterior_hypotheses"]), set(HYPOTHESES))
        self.assertEqual(first["calibration_status"], "UNVALIDATED_ENGINEERING_PRIORS")

    def test_unknown_error_preserves_uncertainty_instead_of_claiming_a_cause(self):
        found = classify_failure_hypotheses(["some entirely new failure code"])
        self.assertEqual(set(found), set(HYPOTHESES))


if __name__ == "__main__":
    unittest.main(verbosity=2)
