#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import collections
import unittest
from generate import (
    AXES, AFTERGLOWS, CAMERAS, COMPATIBLE_PAIRS, COMPATIBLE_FRACTURES,
    ENVIRONMENTS, FRACTURES, HAMMER_FINISHES, PALETTES, RAW_COMBINATIONS,
    SCALES, SHELL_FORMS, SIN_PROFILES, TOTAL_COMBINATIONS,
    _decode_index, _encode_index, _is_compatible, _select_by_index,
    build_record, iter_diverse_indices,
)


class BubbleBreakEngineTests(unittest.TestCase):
    def test_compatible_space_count_is_consistent(self):
        other_axes = (len(SIN_PROFILES) * len(ENVIRONMENTS) * len(SCALES)
                      * len(HAMMER_FINISHES) * len(CAMERAS) * len(PALETTES)
                      * len(AFTERGLOWS))
        self.assertEqual(TOTAL_COMBINATIONS, other_axes * len(COMPATIBLE_PAIRS))
        self.assertGreater(RAW_COMBINATIONS, TOTAL_COMBINATIONS)

    def test_mixed_radix_encode_decode_round_trip(self):
        probes = [(0,) * len(AXES), tuple(len(v)-1 for _, v in AXES),
                  (19, 13, 13, 9, 9, 11, 11, 11, 9)]
        for digits in probes:
            self.assertEqual(_decode_index(_encode_index(digits)), digits)

    def test_seed_is_deterministic(self):
        self.assertEqual(list(iter_diverse_indices(100, 20261020)),
                         list(iter_diverse_indices(100, 20261020)))

    def test_all_20_root_causes_covered_and_balanced(self):
        indices = list(iter_diverse_indices(1003, 20261020))
        counts = collections.Counter(_select_by_index(i)["sin"][0] for i in indices)
        self.assertEqual(set(counts), {p[0] for p in SIN_PROFILES})
        self.assertLessEqual(max(counts.values()) - min(counts.values()), 1)

    def test_sampled_combinations_obey_material_compatibility(self):
        for i in iter_diverse_indices(2000, 11):
            digits = _decode_index(i)
            self.assertTrue(_is_compatible(digits))
            shell_id, fracture_id = SHELL_FORMS[digits[1]][0], FRACTURES[digits[5]][0]
            self.assertIn(fracture_id, COMPATIBLE_FRACTURES[shell_id])

    def test_unique_visual_ids_do_not_fake_causal_diversity(self):
        records = [build_record(i, "heroine") for i in iter_diverse_indices(100, 9)]
        self.assertEqual(len({r["story_id"] for r in records}), 100)
        self.assertEqual({r["causal_kernel_id"] for r in records}, {p[0] for p in SIN_PROFILES})
        self.assertEqual(len({r["causal_signature"] for r in records}), 20)

    def test_incompatible_pair_blocked(self):
        invalid = _encode_index((0, 0, 0, 0, 0, 0, 0, 0, 0))  # SHELL01 + FRAC01
        with self.assertRaisesRegex(ValueError, "incompatible shell/fracture"):
            build_record(invalid, "heroine")

    def test_prompt_contract_and_safe_end(self):
        record = build_record(next(iter_diverse_indices(1, 1234)), "heroine")
        self.assertEqual(record["audit"]["status"], "PROMPT_CONTRACT_PASS")
        self.assertEqual(record["audit"]["image_realization"], "NOT_RUN")
        self.assertIn("6 點鐘位置", record["contact_prompt"])
        self.assertIn("第一次", record["contact_prompt"])
        self.assertIn("全部存活", record["end_prompt"])
        self.assertIn("沒有傷口", record["end_prompt"])

    def test_start_and_end_states_distinct(self):
        record = build_record(next(iter_diverse_indices(1, 4321)), "abstract")
        self.assertIn("可見的空隙", record["start_prompt"])
        self.assertIn("無預存裂紋", record["start_prompt"])
        self.assertIn("已解體", record["end_prompt"])

    def test_dual_modes_export_separately(self):
        record = build_record(next(iter_diverse_indices(1, 99)), "dual")
        self.assertIn("heroine", record["prompts"])
        self.assertIn("abstract", record["prompts"])
        self.assertNotEqual(record["prompts"]["heroine"]["H0"], record["prompts"]["abstract"]["H0"])


if __name__ == "__main__":
    unittest.main()
