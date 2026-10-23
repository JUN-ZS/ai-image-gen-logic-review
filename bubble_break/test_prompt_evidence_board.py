import base64
import hashlib
import tempfile
import unittest
from pathlib import Path

from bubble_break.prompt_evidence_board import audit_state, build_svg


TINY_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jK2cAAAAASUVORK5CYII="
)


class TestPromptEvidenceBoard(unittest.TestCase):
    def base_manifest(self):
        return {
            "schema_version": 1,
            "attempt_id": "TRY-0042",
            "branch": "feat/demo",
            "source_commit_sha": "0123456789abcdef",
            "prompt_id": "H2_first_contact",
            "variant_id": "X_RIGHT__CAM02__M2",
            "topology_id": "t_hammer_terminal_face",
            "stage_id": "H2",
            "variables_changed": {
                "impact_axis": "X_RIGHT",
                "camera": "CAM02",
                "windup": "COMPACT_SNAP",
                "expected_gap_units": 0
            },
            "expected": {
                "active_surface": "terminal_end_face",
                "contact_point": "P",
                "gap_units": 0,
                "normal_dot": -1
            },
            "observed": {
                "active_surface": "UNVERIFIED",
                "contact_point": "UNVERIFIED",
                "gap_state": "UNVERIFIED"
            },
            "image_realization_status": "NOT_RUN",
            "pixel_audit_status": "NOT_RUN",
            "failure_reasons": [],
            "next_change": "Attach raster and inspect the exact contact face.",
            "prompt_excerpt": "Design-only example; not a generated image."
        }

    def test_pass_is_demoted_without_source_raster(self):
        manifest = self.base_manifest()
        manifest["pixel_audit_status"] = "PASS"
        manifest["review_receipt"] = {
            "reviewer": "reviewer",
            "verdict": "PASS",
            "raster_sha256": "abc123"
        }
        image_status, audit, reason = audit_state(manifest, None)
        self.assertEqual(audit, "UNVERIFIED")
        self.assertIn("no source raster", reason)
        svg = build_svg(manifest, None)
        self.assertIn("PIXEL AUDIT", svg)
        self.assertIn("UNVERIFIED", svg)
        self.assertIn("NO SOURCE RASTER ATTACHED", svg)

    def test_matching_raster_sha_receipt_allows_displaying_pass(self):
        manifest = self.base_manifest()
        manifest["image_realization_status"] = "IMAGE_GENERATED"
        manifest["pixel_audit_status"] = "PASS"
        with tempfile.TemporaryDirectory() as tmp:
            raster = Path(tmp) / "source.png"
            raster.write_bytes(TINY_PNG)
            digest = hashlib.sha256(TINY_PNG).hexdigest()
            manifest["review_receipt"] = {
                "reviewer": "human-review",
                "verdict": "PASS",
                "raster_sha256": digest,
                "reviewed_at": "2026-10-23T00:00:00Z"
            }
            _, audit, reason = audit_state(manifest, digest)
            self.assertEqual(audit, "PASS")
            self.assertEqual(reason, "")
            svg = build_svg(manifest, raster)
            self.assertIn("data:image/png;base64,", svg)
            self.assertIn("PIXEL AUDIT", svg)
            self.assertIn("PASS", svg)
            self.assertIn(digest[:24], svg)

    def test_stale_receipt_hash_cannot_show_pass(self):
        manifest = self.base_manifest()
        manifest["pixel_audit_status"] = "PASS"
        with tempfile.TemporaryDirectory() as tmp:
            raster = Path(tmp) / "source.png"
            raster.write_bytes(TINY_PNG)
            manifest["review_receipt"] = {
                "reviewer": "human-review",
                "verdict": "PASS",
                "raster_sha256": "0" * 64
            }
            actual = hashlib.sha256(TINY_PNG).hexdigest()
            _, audit, reason = audit_state(manifest, actual)
            self.assertEqual(audit, "UNVERIFIED")
            self.assertIn("SHA mismatch", reason)

    def test_metadata_is_visible_and_escaped(self):
        manifest = self.base_manifest()
        manifest["attempt_id"] = "TRY <42>"
        svg = build_svg(manifest, None)
        self.assertIn("TRY &lt;42&gt;", svg)
        self.assertIn("X_RIGHT", svg)
        self.assertIn("t_hammer_terminal_face", svg)
        self.assertIn("face=end-face", svg)
        self.assertIn("FAILURE REASONS", svg)
        self.assertIn("NEXT CHANGE", svg)

    def test_next_change_is_derived_from_sha_bound_failure_not_generic_text(self):
        manifest = self.base_manifest()
        manifest["pixel_audit_status"] = "FAIL"
        manifest["observed"]["active_surface"] = "broad_sidewall"
        with tempfile.TemporaryDirectory() as tmp:
            raster = Path(tmp) / "source.png"
            raster.write_bytes(TINY_PNG)
            digest = hashlib.sha256(TINY_PNG).hexdigest()
            manifest["review_receipt"] = {
                "reviewer": "human-review",
                "verdict": "FAIL",
                "raster_sha256": digest,
                "reviewed_at": "2026-10-23T08:00:00Z"
            }
            svg = build_svg(manifest, raster)
            self.assertIn("WRONG_CONTACT_FACE", svg)
            self.assertIn("approach_vector", svg)
            self.assertIn("weapon_topology", svg)
            self.assertIn("REPAIR_PLAN_READY", svg)

    def test_board_holds_next_change_when_review_sha_does_not_match(self):
        manifest = self.base_manifest()
        manifest["pixel_audit_status"] = "FAIL"
        manifest["observed"]["active_surface"] = "broad_sidewall"
        with tempfile.TemporaryDirectory() as tmp:
            raster = Path(tmp) / "source.png"
            raster.write_bytes(TINY_PNG)
            manifest["review_receipt"] = {
                "reviewer": "human-review",
                "verdict": "FAIL",
                "raster_sha256": "0" * 64
            }
            svg = build_svg(manifest, raster)
            self.assertIn("INSUFFICIENT_EVIDENCE", svg)
            self.assertIn("Do not change the image formula yet", svg)

    def test_contact_roi_is_overlaid_only_when_raster_exists(self):
        manifest = self.base_manifest()
        manifest["contact_roi_norm"] = {"x": 0.4, "y": 0.45, "w": 0.12, "h": 0.1}
        svg_without = build_svg(manifest, None)
        self.assertNotIn("P / REVIEW ROI", svg_without)
        with tempfile.TemporaryDirectory() as tmp:
            raster = Path(tmp) / "source.png"
            raster.write_bytes(TINY_PNG)
            svg_with = build_svg(manifest, raster)
            self.assertIn("P / REVIEW ROI", svg_with)
            self.assertIn("stroke-dasharray", svg_with)


if __name__ == "__main__":
    unittest.main()
