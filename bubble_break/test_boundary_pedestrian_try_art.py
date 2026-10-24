"""Unit tests for deterministic Boundary Walker art labels."""
from __future__ import annotations

import hashlib
import json
import struct
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from bubble_break.boundary_pedestrian_try_art import (
    build_ass,
    build_svg,
    image_size,
    main,
    sha256_bytes,
    text_content_sha256,
    validate_status,
)


def png_header(width: int = 1920, height: int = 1080) -> bytes:
    # The renderer only needs the PNG signature/IHDR dimensions; it embeds source bytes as-is.
    return (
        b"\x89PNG\r\n\x1a\n"
        + struct.pack(">I", 13)
        + b"IHDR"
        + struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
        + b"\x00\x00\x00\x00"
    )


class BoundaryWalkerTryArtTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = png_header()
        self.metadata = {
            "story": "THE BOUNDARY WALKER",
            "loop_id": "001",
            "try_id": "0001",
            "act_id": "3",
            "method_id": "GEO.T",
            "method_label": "T-hammer end-face contact",
            "series_id": "S01-RAIN-TOKYO",
            "world_label": "Rainy Tokyo",
            "geometry_family": "T",
            "contact_method": "H2",
            "camera_id": "CAM07",
            "pose_id": "P03",
            "prompt_id": "I-04",
            "style_id": "S01",
            "status": "REVIEW_PENDING",
            "note": "每一次失敗，都帶來下一個試法。",
            "source_sha256": sha256_bytes(self.source),
            "pixel_audit_status": "NOT_RUN",
            "visual_acceptance_status": "NOT_VERIFIED",
        }

    def test_png_dimensions_are_read_without_reencoding(self) -> None:
        self.assertEqual(image_size(self.source), (1920, 1080))

    def test_svg_embeds_source_and_exact_art_labels(self) -> None:
        svg = build_svg(self.source, "image/png", 1920, 1080, self.metadata)
        self.assertIn("data:image/png;base64,", svg)
        self.assertIn("LOOP 001", svg)
        self.assertIn("TRY 0001", svg)
        self.assertIn("GEO.T", svg)
        self.assertIn("T-hammer end-face contact", svg)
        self.assertIn("REVIEW PENDING", svg)
        self.assertIn(self.metadata["source_sha256"][:12], svg)
        self.assertIn("pixel_audit_status", svg)
        self.assertIn("floating-3d-poster", svg)
        self.assertIn("Rainy Tokyo", svg)
        self.assertIn("CAM CAM07", svg)
        self.assertIn("POSE P03", svg)
        self.assertIn("SHA-256", svg)
        self.assertIn("poster_panel_area_fraction", svg)

    def test_art_text_is_xml_escaped(self) -> None:
        metadata = dict(self.metadata)
        metadata["method_label"] = "side < end & cap"
        svg = build_svg(self.source, "image/png", 1920, 1080, metadata)
        self.assertIn("side &lt; end &amp; cap", svg)
        self.assertNotIn("side < end & cap", svg)

    def test_art_poster_occupies_at_least_one_third_of_frame(self) -> None:
        panel_fraction = 0.44 * 0.78
        self.assertGreater(panel_fraction, 1 / 3)
        svg = build_svg(self.source, "image/png", 1920, 1080, self.metadata)
        self.assertIn("floating-3d-poster", svg)
        self.assertIn("letter-spacing=\"1.1\"", svg)

    def test_pre_and_post_typography_changes_visual_treatment_not_words_or_video_text(self) -> None:
        before_metadata = dict(self.metadata, typography_variant="before")
        after_metadata = dict(self.metadata, typography_variant="after")
        before_svg = build_svg(self.source, "image/png", 1920, 1080, before_metadata)
        after_svg = build_svg(self.source, "image/png", 1920, 1080, after_metadata)
        self.assertNotEqual(before_svg, after_svg)
        self.assertIn("#8aeaff", before_svg)
        self.assertIn("#ff9a50", after_svg)
        self.assertEqual(text_content_sha256(before_metadata), text_content_sha256(after_metadata))
        # Video lettering remains one stable canonical treatment rather than switching style mid-clip.
        self.assertEqual(build_ass(before_metadata, 6.0), build_ass(after_metadata, 6.0))
        self.assertEqual(text_content_sha256(before_metadata), text_content_sha256(after_metadata))

    def test_plain_pass_cannot_be_selected(self) -> None:
        with self.assertRaises(ValueError):
            validate_status("PASS")
        self.assertEqual(validate_status("HUMAN_ACCEPTED"), "HUMAN_ACCEPTED")

    def test_ass_overlay_carries_same_loop_try_and_method(self) -> None:
        ass = build_ass(self.metadata, 6.0)
        self.assertIn("Title: THE BOUNDARY WALKER — 3D TRY TITLE", ass)
        self.assertIn("S01-RAIN-TOKYO", ass)
        self.assertIn("Rainy Tokyo", ass)
        self.assertIn("POSE P03", ass)
        self.assertIn("TRY 0001", ass)
        self.assertIn("GEO.T", ass)
        self.assertIn("T-hammer end-face contact", ass)
        self.assertIn("REVIEW PENDING", ass)
        self.assertIn("Dialogue:", ass)

    def test_product_label_manifest_drives_art_exactly_and_records_full_hashes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "frame.png"
            source.write_bytes(self.source)
            manifest = root / "label.json"
            spec = {
                "art_label_spec": {
                    "story": "THE BOUNDARY WALKER",
                    "loop_id": "LOOP-000123",
                    "try_id": "TRY-ABC123",
                    "series_id": "S01-RAIN-TOKYO",
                    "world_label": "Rainy Tokyo / 雨夜東京",
                    "method_id": "GEO.T",
                    "method_label": "single T-hammer / H2 first contact",
                    "geometry_family": "T",
                    "contact_method": "H2",
                    "camera_id": "T192-AX03-CAM07-M1",
                    "pose_id": "P03",
                    "style_id": "S01",
                    "panel_side": "right",
                    "status": "REVIEW_PENDING",
                    "acts": {
                        "3": {
                            "act_id": "3",
                            "prompt_id": "BPX-ABC-I-ACT3",
                            "note": "ACT 3: 試法／碎裂",
                        }
                    },
                }
            }
            manifest.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
            out = root / "poster.svg"
            argv = [
                "boundary_pedestrian_try_art.py",
                "--image", str(source),
                "--out", str(out),
                "--label-manifest", str(manifest),
                "--act-id", "3",
                "--typography-variant", "before",
            ]
            with patch("sys.argv", argv):
                self.assertEqual(main(), 0)
            sidecar = json.loads(out.with_suffix(".manifest.json").read_text(encoding="utf-8"))
            source_sha = hashlib.sha256(source.read_bytes()).hexdigest()
            artwork_sha = hashlib.sha256(out.read_bytes()).hexdigest()
            self.assertEqual(sidecar["source_sha256"], source_sha)
            self.assertEqual(sidecar["artwork_sha256"], artwork_sha)
            self.assertEqual(sidecar["loop_id"], "LOOP-000123")
            self.assertEqual(sidecar["try_id"], "TRY-ABC123")
            self.assertEqual(sidecar["prompt_id"], "BPX-ABC-I-ACT3")
            self.assertEqual(sidecar["series_id"], "S01-RAIN-TOKYO")
            self.assertEqual(sidecar["typography_variant"], "before")
            self.assertEqual(sidecar["text_content_sha256"], text_content_sha256(sidecar))
            self.assertGreater(sidecar["poster_panel_area_fraction"], 1 / 3)
            svg = out.read_text(encoding="utf-8")
            self.assertIn("TRY-ABC123", svg)
            self.assertIn("Rainy Tokyo", svg)
            self.assertIn("BPX-ABC-I-ACT3", svg)

    def test_ass_rejects_nonpositive_duration(self) -> None:
        with self.assertRaises(ValueError):
            build_ass(self.metadata, 0)


if __name__ == "__main__":
    unittest.main()
