#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from generate import TOTAL_COMBINATIONS, _decode_index, build_record, iter_diverse_indices


class BubbleBreakEngineTests(unittest.TestCase):
    def test_combination_space_is_large(self):
        self.assertGreater(TOTAL_COMBINATIONS, 1_000_000)

    def test_decode_indices_are_unique_at_edges(self):
        self.assertNotEqual(_decode_index(0), _decode_index(TOTAL_COMBINATIONS - 1))

    def test_seed_is_deterministic(self):
        self.assertEqual(list(iter_diverse_indices(20, 7)), list(iter_diverse_indices(20, 7)))

    def test_unique_story_ids(self):
        records = [build_record(i, "heroine") for i in iter_diverse_indices(80, 9)]
        self.assertEqual(len({r["story_id"] for r in records}), len(records))

    def test_contact_contract_and_safe_ending(self):
        record = build_record(next(iter_diverse_indices(1, 1234)), "heroine")
        self.assertIn("PROMPT_CONTRACT_PASS", record["audit"]["status"])
        self.assertIn("6 點鐘位置", record["contact_prompt"])
        self.assertIn("第一次", record["contact_prompt"])
        self.assertIn("全部存活", record["end_prompt"])
        self.assertIn("沒有傷口", record["end_prompt"])
        self.assertEqual(record["audit"]["image_realization"], "NOT_RUN")

    def test_h0_is_not_contact_and_h3_is_not_preimpact(self):
        record = build_record(next(iter_diverse_indices(1, 4321)), "abstract")
        self.assertIn("可見的空隙", record["start_prompt"])
        self.assertIn("無預存裂紋", record["start_prompt"])
        self.assertIn("已解體", record["end_prompt"])

    def test_dual_mode_is_split_not_blended(self):
        record = build_record(next(iter_diverse_indices(1, 99)), "dual")
        self.assertIn("heroine", record["prompts"])
        self.assertIn("abstract", record["prompts"])
        self.assertNotEqual(record["prompts"]["heroine"]["H0"], record["prompts"]["abstract"]["H0"])


if __name__ == "__main__":
    unittest.main()
