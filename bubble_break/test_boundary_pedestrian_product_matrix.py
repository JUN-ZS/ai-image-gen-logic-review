"""Tests for the true geometry × camera/style × video × story product matrix."""
from __future__ import annotations

import csv
import gzip
import json
import tempfile
import unittest
from pathlib import Path

from bubble_break.boundary_pedestrian_product_matrix import (
    STORY_ROUTES,
    VIDEO_METHODS,
    build_image_configs,
    compile_product_matrix,
)


def synthetic_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    counter = 0

    def add(bucket: str, geo: str, contact: str, camera: str, wash: str, style: str) -> None:
        nonlocal counter
        counter += 1
        rows.append({
            "id": f"SYN-{counter:06d}",
            "lane": "HARD",
            "media": "IMAGE",
            "act": "3",
            "geo_family": geo,
            "geo_catalog": "SYNTHETIC_TEST_FIXTURE",
            "contact": contact,
            "cam": camera,
            "wash": wash,
            "style": style,
            "shot": "FRONT",
            "video_method": "",
            "count_bucket": bucket,
        })

    styles = ("S01", "S02", "S03")
    cameras_192 = [
        f"AX{axis:02d}__CAM{cam:02d}_TEST__{wind}"
        for axis in range(8)
        for cam in range(1, 13)
        for wind in ("M1", "M2")
    ]
    assert len(cameras_192) == 192
    for contact in ("H0", "H1", "H2", "H3"):
        for camera in cameras_192:
            for style in styles:
                add("HARD_T_192", "T", contact, camera, "W00", style)
    cameras_48 = [f"AX{axis:02d}__CAM{cam:02d}_DUAL" for axis in range(4) for cam in range(1, 13)]
    assert len(cameras_48) == 48
    for geo in ("T2", "CROSS"):
        for contact in (("H0", "FACE") if geo == "T2" else ("FACE",)):
            for camera in cameras_48:
                for style in styles:
                    add("HARD_DUAL48", geo, contact, camera, "W00", style)
    for geo, contacts, bucket in (
        ("ROD", ("POS", "NEG"), "HARD_ROD"),
        ("PLANT_S", ("PLANTED",), "HARD_PLANT_S"),
        ("PLANT_O", ("PLANTED",), "HARD_PLANT_O"),
        ("MULTI", ("H0", "H2"), "HARD_MULTI"),
    ):
        for contact in contacts:
            for wash in (f"W{i:02d}" for i in range(1, 11)):
                for style in styles:
                    add(bucket, geo, contact, "NA", wash, style)
    return rows


class BoundaryWalkerProductMatrixTests(unittest.TestCase):
    def test_image_dimension_product_counts_and_video_compatibility(self) -> None:
        configs = build_image_configs(synthetic_rows())
        counts: dict[str, int] = {}
        for config in configs:
            counts[config.geo_family] = counts.get(config.geo_family, 0) + 1
        self.assertEqual(counts, {
            "T": 4032,
            "T2": 288,
            "CROSS": 144,
            "ROD": 60,
            "PLANT_S": 30,
            "PLANT_O": 30,
            "MULTI": 60,
        })
        self.assertEqual(sum(counts.values()), 4644)
        self.assertEqual(sum(len(VIDEO_METHODS[config.geo_family]) for config in configs), 17964)
        self.assertEqual(len(STORY_ROUTES), 6)
        self.assertEqual(17964 * len(STORY_ROUTES), 107784)

    def test_h2_impact_pack_does_not_double_count_front(self) -> None:
        configs = build_image_configs(synthetic_rows())
        h2_pack_shots = [c.shot for c in configs if c.camera_pack == "T_H2_IMPACT4"]
        self.assertEqual(len(h2_pack_shots), 192 * 3 * 3)
        self.assertEqual(set(h2_pack_shots), {"LOW", "PEAK", "SIDE"})
        self.assertNotIn("FRONT", h2_pack_shots)

    def test_plant_handles_are_separate_topologies(self) -> None:
        configs = build_image_configs(synthetic_rows())
        side = [c for c in configs if c.geo_family == "PLANT_S"]
        outer = [c for c in configs if c.geo_family == "PLANT_O"]
        self.assertEqual(len(side), 30)
        self.assertEqual(len(outer), 30)
        self.assertEqual({c.contact for c in side}, {"PLANTED"})
        self.assertEqual({c.contact for c in outer}, {"PLANTED"})

    def test_sample_product_writes_six_image_and_six_video_prompts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_csv = root / "variants.csv"
            rows = synthetic_rows()
            fieldnames = list(rows[0])
            with source_csv.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            catalog_doc = root / "catalog.md"
            catalog_doc.write_text("# synthetic prompt catalog\n", encoding="utf-8")
            outdir = root / "out"
            summary = compile_product_matrix(source_csv, outdir, catalog_doc, limit=4)
            self.assertEqual(summary["full_cross_product_combinations"], 107784)
            self.assertEqual(summary["compiled_combinations"], 4)
            self.assertFalse(summary["full_product_compiled"])
            self.assertFalse(summary["external_generation_called"])
            self.assertEqual(summary["visual_acceptance_status"], "NOT_VERIFIED")
            with gzip.open(outdir / "boundary_walker_full_product.jsonl.gz", "rt", encoding="utf-8") as handle:
                records = [json.loads(line) for line in handle]
            self.assertEqual(len(records), 4)
            for record in records:
                self.assertEqual(len(record["acts"]), 6)
                self.assertEqual(sum(act["primary_try"] for act in record["acts"]), 1)
                self.assertTrue(all(act["image_prompt"].startswith("Create one single") for act in record["acts"]))
                self.assertTrue(all("independently reviewable" in act["video_prompt"] for act in record["acts"]))
                self.assertEqual(record["image_realization"], "NOT_RUN")
                self.assertEqual(record["pixel_audit_status"], "NOT_RUN")
            with (outdir / "boundary_walker_product_index.csv").open(encoding="utf-8", newline="") as handle:
                self.assertEqual(len(list(csv.DictReader(handle))), 4)

    def test_v02_and_mv_routes_have_independent_prompt_expansions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_csv = root / "variants.csv"
            rows = synthetic_rows()
            with source_csv.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            catalog_doc = root / "catalog.md"
            catalog_doc.write_text("catalog fixture\n", encoding="utf-8")
            # The full hash-ordered product is compiled in CI. This test verifies helper expansion counts directly.
            from bubble_break.boundary_pedestrian_product_matrix import ImageConfig, make_keyframes, mv_shot_specs
            cfg = ImageConfig("T", "H2", "T192", "AX00__CAM01_TEST__M1", "W00", "S01", "FRONT", "M1", "I-04")
            self.assertEqual(len(make_keyframes(cfg, "BP6-I20", "LOOP-X", "TRY-X")), 5)
            self.assertEqual(len(mv_shot_specs("MV24")), 24)
            self.assertEqual(len(mv_shot_specs("MV52")), 52)


if __name__ == "__main__":
    unittest.main()
