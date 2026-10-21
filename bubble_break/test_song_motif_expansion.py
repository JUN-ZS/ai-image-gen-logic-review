import json
import tempfile
import unittest
from collections import Counter
from pathlib import Path

from song_motif_expansion import (
    EXTREMITIES,
    FLOWER_MOTIFS,
    GUMEN_MOTIFS,
    _song_pair_sequence,
    generate,
    iter_records,
)
import generate as base_engine


class TestSongMotifExpansion(unittest.TestCase):
    def test_source_axes_are_large_and_distinct(self):
        self.assertEqual(len(FLOWER_MOTIFS), 11)
        self.assertEqual(len(GUMEN_MOTIFS), 12)
        self.assertEqual(len(EXTREMITIES), 20)
        self.assertEqual(len({row[0] for row in FLOWER_MOTIFS}), 11)
        self.assertEqual(len({row[0] for row in GUMEN_MOTIFS}), 12)
        self.assertEqual(len({row[0] for row in EXTREMITIES}), 20)

    def test_one_shuffled_block_covers_all_132_song_pairs(self):
        pairs = _song_pair_sequence(132, 20261021)
        self.assertEqual(len(pairs), 132)
        self.assertEqual(len(set(pairs)), 132)
        self.assertEqual(set(pairs), {
            (f, g) for f in range(len(FLOWER_MOTIFS))
            for g in range(len(GUMEN_MOTIFS))
        })

    def test_pair_sampling_is_balanced_across_blocks(self):
        pairs = _song_pair_sequence(400, 20261021)
        counts = Counter(pairs)
        self.assertEqual(len(counts), 132)
        self.assertLessEqual(max(counts.values()) - min(counts.values()), 1)

    def test_deterministic_seed_and_unique_story_ids(self):
        first = list(iter_records(3, 7781, "heroine", "RADIAL"))
        second = list(iter_records(3, 7781, "heroine", "RADIAL"))
        self.assertEqual([r["story_id"] for r in first], [r["story_id"] for r in second])
        self.assertEqual([r["song_semantic_layer"] for r in first],
                         [r["song_semantic_layer"] for r in second])
        many = list(iter_records(80, 7781, "heroine", "RADIAL"))
        self.assertEqual(len({r["story_id"] for r in many}), len(many))
        self.assertGreaterEqual(len({r["causal_kernel_id"] for r in many}), 20)

    def test_each_frame_has_source_motifs_extremity_and_correct_story_phase(self):
        index = next(base_engine.iter_diverse_indices(1, 334455))
        from song_motif_expansion import build_song_layered_record
        record = build_song_layered_record(
            base_index=index,
            ordinal=7,
            pair=(3, 2),
            next_pair=(10, 9),
            seed=20261021,
            mode="heroine",
            weapon_topology="RADIAL",
        )
        self.assertEqual(record["song_semantic_layer"]["flower_source"]["motif_id"], "F04_AMBER_HEART")
        self.assertEqual(record["song_semantic_layer"]["gumen_source"]["motif_id"], "G03_COPPER_MIRROR_SOULS")
        self.assertEqual(record["song_semantic_layer"]["beta_cross_story"]["next_gumen_motif_id"], "G10_SHADOW_FIRST_THRESHOLD")
        self.assertFalse(record["song_semantic_layer"]["lyrics_copied"])
        self.assertEqual(record["audit"]["status"], "PROMPT_CONTRACT_PASS")
        for mode_prompts in record["prompts"].values():
            for beat, prompt in mode_prompts.items():
                self.assertIn("EFV 語義借意層", prompt)
                self.assertIn("X", prompt)
                self.assertIn("花系意象", prompt)
                self.assertIn("古門系意象", prompt)
                if beat == "H0":
                    self.assertIn("球膜必須完整", prompt)
                    self.assertIn("清楚空隙", prompt)
                if beat == "H1":
                    self.assertIn("不許預先出裂紋", prompt)
                if beat == "H2":
                    self.assertIn("第一次接觸 P", prompt)
                    self.assertIn("裂紋只在接觸後從 P", prompt)
                if beat == "H3":
                    self.assertIn("自願選擇的路", prompt)
        self.assertEqual(record["start_prompt"], record["prompts"]["heroine"]["H0"])
        self.assertEqual(record["contact_prompt"], record["prompts"]["heroine"]["H2"])

    def test_dual_mode_separates_heroine_and_abstract_prompts(self):
        record = next(iter_records(1, 10101, "dual", "T"))
        self.assertEqual(set(record["prompts"]), {"heroine", "abstract"})
        self.assertIn("F", record["prompts"]["heroine"]["H0"])
        self.assertIn("G", record["prompts"]["abstract"]["H3"])
        self.assertIn("T", record["weapon_topology"])
        self.assertEqual(record["audit"]["image_realization"], "NOT_RUN")
        self.assertEqual(record["audit"]["pixel_audit_status"], "NOT_RUN")

    def test_100_records_include_all_original_sin_kernels(self):
        records = list(iter_records(100, 20261021, "abstract", "RADIAL"))
        causes = Counter(row["causal_kernel_id"] for row in records)
        self.assertEqual(len(causes), 20)
        self.assertLessEqual(max(causes.values()) - min(causes.values()), 1)

    def test_cli_export_is_streamable_and_honest_about_image_status(self):
        with tempfile.TemporaryDirectory() as temp:
            output = str(Path(temp) / "batch.jsonl")
            summary = generate(4, 20261021, "heroine", "jsonl", output, "RADIAL")
            rows = [json.loads(line) for line in Path(output).read_text(encoding="utf-8").splitlines()]
            self.assertEqual(summary["written_count"], 4)
            self.assertEqual(len(rows), 4)
            self.assertTrue(all(r["audit"]["status"] == "PROMPT_CONTRACT_PASS" for r in rows))
            self.assertTrue(all(r["audit"]["image_realization"] == "NOT_RUN" for r in rows))
            self.assertTrue(all(r["audit"]["pixel_audit_status"] == "NOT_RUN" for r in rows))
            self.assertTrue(all("EFV 語義借意層" in r["contact_prompt"] for r in rows))


if __name__ == "__main__":
    unittest.main()
