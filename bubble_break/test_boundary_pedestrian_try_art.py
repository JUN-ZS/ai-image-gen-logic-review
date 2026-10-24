"""Unit tests for deterministic Boundary Walker art labels."""
from __future__ import annotations

import struct
import unittest

from bubble_break.boundary_pedestrian_try_art import (
    build_ass,
    build_svg,
    image_size,
    sha256_bytes,
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

    def test_ass_rejects_nonpositive_duration(self) -> None:
        with self.assertRaises(ValueError):
            build_ass(self.metadata, 0)


if __name__ == "__main__":
    unittest.main()
