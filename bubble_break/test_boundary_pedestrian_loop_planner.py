"""Tests for the complete Boundary Walker loop prompt compiler."""
from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path

from bubble_break.boundary_pedestrian_loop_planner import (
    REQUIRED_COLUMNS,
    build_episode,
    compile_csv,
    interleave_buckets,
    method_description,
)


def make_row(**overrides: str) -> dict[str, str]:
    row = {key: "" for key in REQUIRED_COLUMNS}
    row.update({
        "id": "BP-3H-T-H2-X_RIGHT__CAM01_GRAZING_FACE__M1-W00-S01-FRONT",
        "lane": "HARD",
        "media": "IMAGE",
        "act": "3",
        "geo_family": "T",
        "geo_catalog": "I-01;I-04;I-18",
        "contact": "H2",
        "cam": "X_RIGHT__CAM01_GRAZING_FACE__M1",
        "wash": "W00",
        "style": "S01",
        "shot": "FRONT",
        "video_method": "",
        "count_bucket": "HARD_T_192",
    })
    row.update(overrides)
    return row


class BoundaryWalkerLoopPlannerTests(unittest.TestCase):
    def test_episode_has_six_story_acts_and_one_primary_try(self) -> None:
        row = make_row()
        episode = build_episode(row, 7, "abc123")
        self.assertEqual(episode["loop_id"], "LOOP-0007")
        self.assertEqual(episode["try_id"], "TRY-0007")
        self.assertEqual(len(episode["acts"]), 6)
        self.assertEqual(sum(act["is_primary_try"] for act in episode["acts"]), 1)
        self.assertEqual(episode["acts"][2]["media"], "IMAGE")
        self.assertIn("only the nominated terminal striking face", episode["acts"][2]["prompt"])
        self.assertIn("H2", episode["method_label"])
        self.assertEqual(episode["status"], "PROMPT_READY")
        self.assertEqual(episode["pixel_audit_status"], "NOT_RUN")
        self.assertEqual(episode["visual_acceptance_status"], "NOT_VERIFIED")
        self.assertFalse(episode["external_generation_called"])

    def test_bucket_interleave_changes_method_family_early(self) -> None:
        rows = [
            make_row(id="soft-1", lane="SOFT", media="IMAGE", act="1", geo_family="NONE",
                     contact="NA", count_bucket="SOFT_IMAGE", shot="WIDE"),
            make_row(id="soft-2", lane="SOFT", media="IMAGE", act="2", geo_family="NONE",
                     contact="NA", count_bucket="SOFT_IMAGE", shot="HOLD"),
            make_row(id="video-1", lane="SOFT", media="VIDEO", act="1", geo_family="NONE",
                     contact="NA", video_method="V-09", count_bucket="VIDEO_BP"),
            make_row(id="rod-1", lane="HARD", media="IMAGE", act="3", geo_family="ROD",
                     contact="POS", count_bucket="HARD_ROD"),
        ]
        ordered = interleave_buckets(rows)
        self.assertEqual([r["id"] for r in ordered], ["soft-1", "video-1", "rod-1", "soft-2"])

    def test_planted_side_handle_is_not_described_as_a_flying_strike(self) -> None:
        description = method_description(make_row(
            geo_family="PLANT_S", contact="H2",
            geo_catalog="I-13", count_bucket="HARD_PLANT_S",
        ))
        self.assertIn("fixed anchor, not a flying impact", description)
        self.assertIn("side-middle tangent", description)
        self.assertNotIn("only the nominated terminal striking face touches", description)

    def test_multi_facet_head_uses_selected_broad_face(self) -> None:
        description = method_description(make_row(geo_family="MULTI", contact="H2"))
        self.assertIn("nominated broad planar facet", description)
        self.assertIn("do not turn the head into a T-hammer", description)

    def test_v09_unbound_geometry_is_story_only(self) -> None:
        row = make_row(
            id="BP-3V-NONE-NA-V09-W00-S01-ACT",
            lane="HARD",
            media="VIDEO",
            act="3",
            geo_family="T_OR_MULTI",
            geo_catalog="V-09",
            contact="NA",
            cam="V09",
            style="S01",
            shot="ACT3",
            video_method="V-09",
            count_bucket="VIDEO_BP",
        )
        episode = build_episode(row, 9, "source-sha")
        prompt = episode["acts"][2]["prompt"]
        self.assertIn("narrative montage", prompt)
        self.assertIn("do not depict a precise weapon/sphere contact", prompt)
        self.assertEqual(episode["acts"][2]["media"], "VIDEO")

    def test_compiler_writes_unique_id_index_and_honest_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "variants.csv"
            fields = [
                "id", "lane", "media", "act", "geo_family", "geo_catalog", "contact",
                "cam", "wash", "style", "shot", "video_method", "count_bucket",
            ]
            rows = [
                make_row(id="soft-1", lane="SOFT", media="IMAGE", act="1", geo_family="NONE",
                         contact="NA", cam="NA", shot="WIDE", count_bucket="SOFT_IMAGE"),
                make_row(id="hard-1"),
                make_row(id="video-1", lane="SOFT", media="VIDEO", act="1", geo_family="NONE",
                         contact="NA", cam="V09", shot="ACT1", video_method="V-09", count_bucket="VIDEO_BP"),
            ]
            with source.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                for row in rows:
                    writer.writerow({key: row[key] for key in fields})
            outdir = root / "out"
            summary = compile_csv(source, outdir)
            self.assertEqual(summary["source_total_variants"], 3)
            self.assertEqual(summary["compiled_variant_count"], 3)
            self.assertTrue(summary["full_sweep_compiled"])
            self.assertTrue(summary["all_selected_variant_ids_once"])
            self.assertFalse(summary["external_generation_called"])
            records = [
                json.loads(line)
                for line in (outdir / "loop_prompt_packets.jsonl").read_text(encoding="utf-8").splitlines()
            ]
            self.assertEqual(len(records), 3)
            self.assertEqual(len({record["variant_id"] for record in records}), 3)
            self.assertTrue(all(len(record["acts"]) == 6 for record in records))
            self.assertTrue(all(record["status"] == "PROMPT_READY" for record in records))
            self.assertEqual(len((outdir / "loop_index.csv").read_text(encoding="utf-8").splitlines()), 4)


if __name__ == "__main__":
    unittest.main()
