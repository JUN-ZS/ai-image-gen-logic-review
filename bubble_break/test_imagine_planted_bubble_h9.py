#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests for H9 Imagine planted-bubble packet/ingest (no network, no API key)."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from bubble_break.imagine_planted_bubble_h9 import (
    H9_ID,
    H9_PROVIDER,
    VISUAL,
    compile_h9_packet,
    ingest_h9_run,
)
from bubble_break.planted_bubble_closed_loop import STAGE_ORDER


def _rgb(path: Path, color: tuple[int, int, int], size=(64, 36)) -> None:
    Image.new("RGB", size, color).save(path, format="JPEG", quality=90)


class ImagineH9Tests(unittest.TestCase):
    def test_compile_and_ingest_seven_stages_without_api_key(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            master = root / "b3.jpg"
            person = root / "her.jpg"
            _rgb(master, (40, 40, 50))
            _rgb(person, (200, 160, 140))
            packet_dir = root / "packet"
            packet = compile_h9_packet(outdir=packet_dir, master_b3=master, person_ref=person)
            self.assertEqual(packet["h9_id"], H9_ID)
            self.assertEqual(packet["provider"], H9_PROVIDER)
            self.assertEqual(packet["code_visual_acceptance_status"], VISUAL)
            self.assertEqual(len(packet["stage_order"]), 7)
            for stage in STAGE_ORDER:
                self.assertTrue((packet_dir / "prompts" / f"{stage}.md").is_file())

            rasters = root / "rasters"
            rasters.mkdir()
            # distinct colors so no-op detection stays false
            palette = [
                (10, 10, 10),
                (20, 20, 30),
                (30, 40, 50),
                (40, 50, 60),
                (50, 60, 70),
                (60, 70, 80),
                (70, 80, 90),
            ]
            for stage, color in zip(STAGE_ORDER, palette):
                _rgb(rasters / f"{stage}.jpg", color)

            out = root / "run"
            manifest = ingest_h9_run(packet_dir=packet_dir, rasters_dir=rasters, outdir=out)
            self.assertTrue(manifest["all_stages_ingested"])
            self.assertFalse(manifest["any_no_op_child"])
            self.assertEqual(manifest["code_visual_acceptance_status"], VISUAL)
            self.assertTrue((out / "H9_RUN_MANIFEST.json").is_file())
            self.assertTrue((out / "H9_7STAGE_STRIP.jpg").is_file())
            self.assertEqual(len(manifest["stages"]), 7)

    def test_ingest_rejects_missing_stage(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            master = root / "b3.jpg"
            _rgb(master, (1, 2, 3))
            packet_dir = root / "packet"
            compile_h9_packet(outdir=packet_dir, master_b3=master)
            rasters = root / "rasters"
            rasters.mkdir()
            _rgb(rasters / f"{STAGE_ORDER[0]}.jpg", (9, 9, 9))
            with self.assertRaises(FileNotFoundError):
                ingest_h9_run(packet_dir=packet_dir, rasters_dir=rasters, outdir=root / "run")


if __name__ == "__main__":
    unittest.main()
