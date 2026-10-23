import json
import tempfile
import unittest
from pathlib import Path

from bubble_break.prompt_attempt_packet import package_matrix


class TestPromptAttemptPacket(unittest.TestCase):
    def example_matrix(self):
        return {
            "counts": {"total_variants": 1},
            "variants": [{
                "variant_id": "X_RIGHT__CAM02__M1",
                "axis": {"axis_id": "X_RIGHT", "normal": [1, 0, 0]},
                "camera": {
                    "camera_id": "CAM02_FRONT_THREE_QUARTER",
                    "off_normal_deg": 38,
                    "orbit_deg": 35,
                    "roll_deg": 0,
                    "focal_mm": 35
                },
                "swing": {"swing_id": "SIDE_SWEEP"},
                "windup_profile": {"profile_id": "WINDUP_COMPACT_SNAP"},
                "geometry": {
                    "normal_dot": -1.0,
                    "H0_total_gap": 50.0,
                    "H2_gap": 0.0,
                    "H3_advance": 15.0,
                    "roll_A": 0,
                    "roll_B": 90
                },
                "prompts": {
                    "H2_first_contact": "Terminal end-face touches the sphere at P.",
                    "H3_followthrough": "Advance the same rigid hammer along n."
                },
                "audit_status": {
                    "image_realization": "NOT_RUN",
                    "pixel_audit": "NOT_RUN"
                }
            }]
        }

    def test_each_matrix_prompt_gets_independent_traceable_packet(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            matrix_path = root / "matrix.json"
            matrix_path.write_text(json.dumps(self.example_matrix()), encoding="utf-8")
            outdir = root / "packets"
            index = package_matrix(
                matrix_path, outdir, "feat/example", "a" * 40,
                "t_hammer_terminal_face"
            )
            self.assertEqual(index["variant_count"], 1)
            self.assertEqual(index["attempt_count"], 2)
            self.assertEqual(index["image_realization"], "NOT_RUN")
            self.assertEqual(index["pixel_audit"], "NOT_RUN")
            for item in index["attempts"]:
                folder = outdir / item["manifest"].split("/")[0]
                manifest = json.loads((outdir / item["manifest"]).read_text(encoding="utf-8"))
                prompt = (outdir / item["prompt"]).read_text(encoding="utf-8")
                board = (outdir / item["teaching_board"]).read_text(encoding="utf-8")
                self.assertEqual(manifest["source_commit_sha"], "a" * 40)
                self.assertEqual(manifest["branch"], "feat/example")
                self.assertEqual(manifest["pixel_audit_status"], "NOT_RUN")
                self.assertEqual(manifest["observed"]["active_surface"], "UNVERIFIED")
                self.assertEqual(manifest["prompt_sha256"], item["prompt_sha256"])
                self.assertIn("NO SOURCE RASTER ATTACHED", board)
                self.assertIn("NOT_RUN", board)
                self.assertTrue(prompt.strip())
                self.assertTrue((folder / "manifest.json").exists())
            self.assertTrue((outdir / "source_matrix_snapshot.json").exists())
            self.assertTrue((outdir / "prompt_attempt_index.json").exists())

    def test_rejects_unpinned_or_invalid_commit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            matrix_path = root / "matrix.json"
            matrix_path.write_text(json.dumps(self.example_matrix()), encoding="utf-8")
            with self.assertRaises(ValueError):
                package_matrix(matrix_path, root / "out", "feat/example", "UNPINNED")

    def test_empty_prompt_entries_are_not_mispackaged_as_attempts(self):
        matrix = self.example_matrix()
        matrix["variants"][0]["prompts"]["blank_prompt"] = "   "
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            matrix_path = root / "matrix.json"
            matrix_path.write_text(json.dumps(matrix), encoding="utf-8")
            index = package_matrix(matrix_path, root / "out", "feat/example", "b" * 40)
            self.assertEqual(index["attempt_count"], 2)


if __name__ == "__main__":
    unittest.main()
