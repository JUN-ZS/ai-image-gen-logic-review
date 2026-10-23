import json
import tempfile
import unittest
from pathlib import Path

from bubble_break.prompt_attempt_packet import (
    package_matrix,
    package_original_sin_jsonl,
    package_dense_atlas,
    package_dense_bubble,
    package_planted_bubble,
)


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

    def test_original_sin_jsonl_adapter_keeps_branch_topology_and_negative_prompt(self):
        record = {
            "story_id": "ORIG-TEST-001",
            "weapon_topology": "WEAPON_T",
            "combination_index": 17,
            "title": "test story",
            "root_sin": "false protection",
            "causal_signature": "CAUSE-ABC123",
            "axes": {
                "environment": {"id": "ENV_FACTORY"},
                "camera": {"id": "CAM_THREE_QUARTER"},
                "shell": {"id": "SHELL_GLASS"},
                "palette": {"id": "PALETTE_CYAN"},
                "fracture": {"id": "FRACTURE_RADIAL"}
            },
            "prompts": {
                "heroine": {
                    "H0": "H0 pre-impact test prompt",
                    "H1": "H1 approach test prompt",
                    "H2": "H2 contact at P test prompt",
                    "H3": "H3 shell break test prompt"
                }
            },
            "negative_prompt": "no axe, no extra handle",
            "storyboard_9": [
                {"cell": 1, "prompt": "storyboard one", "narrative_role": "setup"},
                {"cell": 2, "prompt": "storyboard two", "narrative_role": "reveal"}
            ],
            "audit": {"status": "PROMPT_CONTRACT_PASS", "image_realization": "NOT_RUN", "errors": []}
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            src = root / "stories.jsonl"
            src.write_text(json.dumps(record, ensure_ascii=False) + "\n", encoding="utf-8")
            index = package_original_sin_jsonl(src, root / "packets", "feat/original-sin-bubble-break-engine", "c" * 40)
            self.assertEqual(index["source_format"], "original-sin-jsonl")
            self.assertEqual(index["attempt_count"], 6)
            h2_item = next(x for x in index["attempts"] if x["prompt_id"] == "H2")
            manifest = json.loads((root / "packets" / h2_item["manifest"]).read_text(encoding="utf-8"))
            prompt = (root / "packets" / h2_item["prompt"]).read_text(encoding="utf-8")
            self.assertEqual(manifest["topology_id"], "original_sin_t_crossbar_upper_plane")
            self.assertEqual(manifest["expected"]["contact_point"], "P")
            self.assertEqual(manifest["expected"]["gap"], 0)
            self.assertIn("NEGATIVE PROMPT", prompt)
            self.assertIn("no axe", prompt)
            self.assertEqual(manifest["source_artifact_sha256"], index["source_artifact_sha256"])
            self.assertEqual(manifest["pixel_audit_status"], "NOT_RUN")

    def test_dense_atlas_adapter_checks_prompt_sha_and_records_target_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prompt = "Create one dense CYLINDER_CROSS collision atlas without labels."
            prompt_path = root / "cylinder_cross_dense_atlas_prompt.txt"
            prompt_path.write_text(prompt + "\n", encoding="utf-8")
            manifest_path = root / "cylinder_cross_dense_atlas_manifest.json"
            metadata = {
                "prompt_file": prompt_path.name,
                "prompt_sha256": __import__("hashlib").sha256(prompt.encode("utf-8")).hexdigest(),
                "canvas": {"aspect_ratio": "16:9", "layout": "IRREGULAR_SCATTER_NO_GRID"},
                "target_local_collision_count": 24,
                "target_hammer_count": 48,
                "required_visible_long_handles": 48,
                "sampling_balance": {"collision_axes": 4, "projection_styles": 12},
                "generation_status": "IMAGE_REALIZATION_NOT_RUN",
                "pixel_audit_status": "PIXEL_AUDIT_NOT_RUN"
            }
            manifest_path.write_text(json.dumps(metadata), encoding="utf-8")
            index = package_dense_atlas(manifest_path, root / "packets", "feat/cylinder-cross-dense-atlas", "d" * 40)
            self.assertEqual(index["attempt_count"], 1)
            item = index["attempts"][0]
            manifest = json.loads((root / "packets" / item["manifest"]).read_text(encoding="utf-8"))
            self.assertEqual(manifest["topology_id"], "cylinder_cross_cap_pair")
            self.assertEqual(manifest["expected"]["target_pairs"], 24)
            self.assertEqual(manifest["pixel_audit_status"], "NOT_RUN")

    def test_dense_bubble_adapter_packs_each_stage_prompt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "stage_a_planted_round_hammer_atlas.md").write_text("Stage A prompt: planted cylinders.", encoding="utf-8")
            (root / "stage_b_one_hammer_no_person.md").write_text("Stage B prompt: isolate C13.", encoding="utf-8")
            candidate = {
                "selected_candidate_id": "C13",
                "source_stage_a_sha256": "e" * 64,
                "hammer_proportions": {
                    "head_diameter_over_bubble_diameter": 0.08,
                    "head_axial_length_over_head_diameter": 1.5
                },
                "scale_changes": {
                    "bubble_scale": 1.0,
                    "hammer_scale": 1.0,
                    "person_to_hammer_scale": 1.0,
                    "NO_NEW_HANDLE": True
                },
                "image_realization": "NOT_RUN",
                "pixel_audit": "NOT_RUN"
            }
            (root / "candidate_manifest.json").write_text(json.dumps(candidate), encoding="utf-8")
            summary = {"outputs": ["candidate_manifest.json", "stage_a_planted_round_hammer_atlas.md", "stage_b_one_hammer_no_person.md", "stage_d_GATES.md"]}
            (root / "packet_summary.json").write_text(json.dumps(summary), encoding="utf-8")
            index = package_dense_bubble(root, root / "packets", "feat/dense-hammer-bubble-pick", "e" * 40)
            self.assertEqual(index["attempt_count"], 2)
            self.assertEqual(index["source_format"], "dense-bubble")
            self.assertTrue(all(x["pixel_audit_status"] == "NOT_RUN" for x in index["attempts"]))
            manifest = json.loads((root / "packets" / index["attempts"][0]["manifest"]).read_text(encoding="utf-8"))
            self.assertEqual(manifest["topology_id"], "planted_cylinder_side_handle")
            self.assertEqual(manifest["variables_changed"]["selected_candidate_id"], "C13")

    def test_planted_bubble_packet_adapter_uses_stage_requests(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            stage_dir = root / "stage_prompts"
            stage_dir.mkdir()
            req = {
                "stage": "D2_GRIP_EXISTING_HANDLE",
                "attempt_round": 0,
                "authorized_delta_fields": ["hand_pose"],
                "must_preserve": ["side_handle_pixels", "contact_point_P"],
                "mask_policy": {"freeze_all_unauthorized_regions": True},
                "prompt": "Grip the existing side-middle handle only; do not add a rod."
            }
            (stage_dir / "D2_GRIP_EXISTING_HANDLE.json").write_text(json.dumps(req), encoding="utf-8")
            packet = {
                "contract_id": "PLANTED_BUBBLE_TEST",
                "stages": {
                    "D2_GRIP_EXISTING_HANDLE": {
                        "prompt_file": "stage_prompts/D2_GRIP_EXISTING_HANDLE.json",
                        "authorized_delta_fields": ["hand_pose"],
                        "must_preserve": ["side_handle_pixels", "contact_point_P"]
                    }
                }
            }
            packet_path = root / "SHANNON_PLANTED_BUBBLE_PROMPT_PACKET.json"
            packet_path.write_text(json.dumps(packet), encoding="utf-8")
            index = package_planted_bubble(packet_path, root / "packets", "fix/shannon-planted-bubble-closed-loop-20261022", "f" * 40)
            self.assertEqual(index["attempt_count"], 1)
            manifest = json.loads((root / "packets" / index["attempts"][0]["manifest"]).read_text(encoding="utf-8"))
            self.assertEqual(manifest["topology_id"], "planted_cylinder_side_handle")
            self.assertIn("hand_pose", manifest["expected"]["authorized_delta_fields"])
            self.assertIn("do not add a rod", (root / "packets" / index["attempts"][0]["prompt"]).read_text(encoding="utf-8"))

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
