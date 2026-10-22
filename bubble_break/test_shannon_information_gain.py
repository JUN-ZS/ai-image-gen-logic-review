from __future__ import annotations

import math
import unittest

from bubble_break.shannon_information_gain import (
    HYPOTHESES,
    classify_failure_hypotheses,
    expected_information_gain_bits,
    normalize_distribution,
    rank_diagnostic_experiments,
    recommend_next_experiment,
    shannon_entropy_bits,
)


class ShannonInformationGainTests(unittest.TestCase):
    def test_entropy_of_fair_binary_choice_is_one_bit(self):
        self.assertAlmostEqual(shannon_entropy_bits({"A": 0.5, "B": 0.5}), 1.0, places=7)

    def test_entropy_of_certain_choice_is_zero(self):
        self.assertAlmostEqual(shannon_entropy_bits({"A": 1.0, "B": 0.0}), 0.0, places=7)

    def test_distribution_is_normalized_and_rejects_negative_mass(self):
        self.assertEqual(normalize_distribution({"A": 2, "B": 2}), {"A": 0.5, "B": 0.5})
        with self.assertRaises(ValueError):
            normalize_distribution({"A": 1, "B": -1})

    def test_perfect_diagnostic_has_positive_information_gain(self):
        priors = {"CONTACT": 0.5, "TOPOLOGY": 0.5}
        perfect = {"CONTACT": 1.0, "TOPOLOGY": 0.0}
        uninformative = {"CONTACT": 0.5, "TOPOLOGY": 0.5}
        self.assertAlmostEqual(expected_information_gain_bits(priors, perfect), 1.0, places=7)
        self.assertAlmostEqual(expected_information_gain_bits(priors, uninformative), 0.0, places=7)

    def test_known_contact_error_prioritizes_contact_diagnostic(self):
        result = recommend_next_experiment([
            "FIRST_CONTACT strike face center does not meet bubble pole P",
            "contact_surface requires FLAT_END_FACE_TO_BUBBLE_POLE_P",
        ])
        self.assertIn("WRONG_CONTACT_SURFACE", result["identified_failure_hypotheses"])
        self.assertEqual(
            result["selected_experiment"]["action_id"],
            "CONTACT_PLANE_GRAZING_MACRO",
        )
        self.assertEqual(result["calibration_status"], "UNVALIDATED_ENGINEERING_PRIORS")
        self.assertIn("cannot override", result["hard_rule"])

    def test_parent_hash_error_recommends_provenance_check(self):
        result = recommend_next_experiment(["PARENT_RASTER_SHA256_MISMATCH", "NO_OP_TRANSITION_IMAGE_IDENTICAL_TO_PARENT"])
        self.assertIn("PARENT_OR_IDENTITY_DRIFT", result["identified_failure_hypotheses"])
        self.assertEqual(
            result["selected_experiment"]["action_id"],
            "PARENT_PAIR_LOCK_AUDIT",
        )

    def test_ranking_is_deterministic_and_cost_adjusted(self):
        priors = {hypothesis: 1 / len(HYPOTHESES) for hypothesis in HYPOTHESES}
        first = rank_diagnostic_experiments(priors)
        second = rank_diagnostic_experiments(priors)
        self.assertEqual([item.action_id for item in first], [item.action_id for item in second])
        self.assertTrue(all(item.expected_information_gain_bits >= 0 for item in first))
        self.assertTrue(all(math.isfinite(item.information_gain_per_cost) for item in first))

    def test_failure_taxonomy_uses_multiple_observed_signals(self):
        matched = classify_failure_hypotheses([
            "crack origin is too far from P",
            "inhabitants are not verified unharmed",
        ])
        self.assertIn("FRACTURE_CAUSALITY_FAILURE", matched)
        self.assertIn("SANCTUARY_PROTECTION_FAILURE", matched)


if __name__ == "__main__":
    unittest.main(verbosity=2)
