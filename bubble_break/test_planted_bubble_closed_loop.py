from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from bubble_break.planted_bubble_closed_loop import (
    CONTRACT_ID,
    STAGE_ORDER,
    Candidate,
    build_stage_masks,
    compose_masked_edit,
    compile_prompt_packet,
    compute_background_landmarks_sha256,
    contract_fingerprint,
    run_planted_bubble_closed_loop,
    sha256_file,
    validate_frozen_pixels,
    validate_planted_bubble_frame,
)


class PlantedBubbleClosedLoopTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.atlas = self.root / "source_atlas.png"
        Image.new("RGB", (400, 300), (12, 18, 24)).save(self.atlas)
        self.atlas_sha = sha256_file(self.atlas)

    def make_image(self, name: str, color: tuple[int, int, int]) -> Path:
        path = self.root / name
        Image.new("RGB", (400, 300), color).save(path)
        return path

    def make_master_selection(self) -> dict:
        return {
            "selection_mode": "HUMAN_ROI",
            "selection_reviewer": "test-human",
            "selection_notes": "Selected by visible position, not printed label",
            "source_atlas_image_path": str(self.atlas),
            "source_atlas_raster_sha256": self.atlas_sha,
            "source_atlas_width_px": 400,
            "source_atlas_height_px": 300,
            "selected_roi_xyxy_px": [180, 70, 300, 250],
            "selected_tool_is_single_instance": True,
        }

    def make_evidence(
        self,
        stage: str,
        image_path: Path,
        *,
        parent_sha: str | None,
        anchor_sha: str | None,
        handle_id: str = "HANDLE_01",
        add_stub: bool = False,
        grip_wrong_handle: bool = False,
        crack_origin: tuple[float, float] | None = None,
        shell_only: bool = True,
        selection_mode: str = "HUMAN_ROI",
        mask_path: Path | None = None,
        camera_view: str = "CAMERA_VIEW_FIXED_001",
        hero_box: tuple[int, int, int, int] = (20, 100, 70, 180),
        pose_signature: str | None = None,
    ) -> dict:
        spec_actor = stage != "B_LOCKED_TOOL_MASTER"
        grip = stage in {
            "D2_FIRST_GRIP_EXISTING_HANDLE",
            "D3_TENSION_EXISTING_HANDLE",
            "E_MID_GLOW_CRACKS_FROM_P",
            "E_END_SHELL_SHATTER_FROM_P",
        }
        shell_state = {
            "B_LOCKED_TOOL_MASTER": "INTACT",
            "C_PERSON_SCALE_NO_GRIP": "INTACT",
            "D1_APPROACH_NO_GRIP": "INTACT",
            "D2_FIRST_GRIP_EXISTING_HANDLE": "INTACT",
            "D3_TENSION_EXISTING_HANDLE": "INTACT",
            "E_MID_GLOW_CRACKS_FROM_P": "CRACKING_NOT_SHATTERED",
            "E_END_SHELL_SHATTER_FROM_P": "SHATTERED",
        }[stage]
        crack_state = {
            "B_LOCKED_TOOL_MASTER": "NONE",
            "C_PERSON_SCALE_NO_GRIP": "NONE",
            "D1_APPROACH_NO_GRIP": "NONE",
            "D2_FIRST_GRIP_EXISTING_HANDLE": "NONE",
            "D3_TENSION_EXISTING_HANDLE": "NONE",
            "E_MID_GLOW_CRACKS_FROM_P": "RADIAL_FROM_P",
            "E_END_SHELL_SHATTER_FROM_P": "SHATTERED_OUTWARD_FROM_P",
        }[stage]
        digest = sha256_file(image_path)
        anchor = digest if stage == "B_LOCKED_TOOL_MASTER" else anchor_sha
        review = {
            "decision": "PASS",
            "mode": "HUMAN_PIXEL_REVIEW",
            "reviewer_or_model": "test-human-review-record",
            "reviewed_raster_sha256": digest,
            "reviewed_parent_sha256": parent_sha,
            "reviewed_scene_anchor_sha256": anchor,
            "stage": stage,
            "notes": "Test fixture only; receipt/hash binding is under test, not visual correctness.",
        }
        evidence = {
            "contract_id": CONTRACT_ID,
            "contract_sha256": contract_fingerprint(),
            "stage": stage,
            "raster_sha256": digest,
            "parent_raster_sha256": parent_sha,
            "scene_anchor_raster_sha256": anchor,
            "scene_id": "BUBBLE_SCENE_001",
            "camera_rig_id": "CAMERA_RIG_001",
            "camera_view_fingerprint": camera_view,
            "background_landmarks_sha256": compute_background_landmarks_sha256(image_path),
            "review": review,
            "selection_metrics": {"creativity_score": 0.0, "novelty_score": 0.0},
            "raster_annotations": {
                "image_width_px": 400,
                "image_height_px": 300,
                "bubble": {"center_px": [260, 120], "radius_px": 80},
                "contact_point_p_px": [260, 200],
                "sanctuary_bbox_xyxy_px": [238, 100, 282, 142],
                "planted_cylinder": {
                    "instance_id": "CYLINDER_01",
                    "body_bbox_xyxy_px": [240, 198, 280, 270],
                    "base_seat_center_px": [260, 200],
                    "outer_end_cap_center_px": [260, 262],
                    "base_seat_surface": "CONFORMAL_CURVED_SEAT_TO_BUBBLE",
                    "full_base_contact_verified": True,
                    "outer_end_cap_clear": True,
                    "additional_handle_or_stub_detected": add_stub,
                    "body_axis_world": [0, 1, 0],
                    "bubble_surface_normal_world": [0, 1, 0],
                    "base_center_world": [0, 0, 0],
                    "outer_end_cap_center_world": [0, 1, 0],
                    "side_handle": {
                        "track_id": handle_id,
                        "bbox_xyxy_px": [165, 194, 260, 206],
                        "axis_start_px": [165, 200],
                        "axis_end_px": [260, 200],
                        "axis_world": [1, 0, 0],
                        "attachment_world": [0, 0.5, 0],
                    },
                },
                "heroine": {
                    "present": spec_actor,
                    "bbox_xyxy_px": list(hero_box) if spec_actor else None,
                    "scale_class": "MINIATURE" if spec_actor else None,
                    "identity_id": "HEROINE_001" if spec_actor else None,
                    "pose_signature": pose_signature or ("POSE_" + stage + "_UNIQUE") if spec_actor else None,
                    "gripping_handle_track_id": (
                        "HANDLE_WRONG" if grip_wrong_handle else (handle_id if grip else None)
                    ),
                    "both_hands_on_existing_handle": grip,
                },
                "shell": {
                    "state": shell_state,
                    "crack_state": crack_state,
                    "base_glow_on_conformal_seat": True,
                    "base_glow_origin_px": [260, 200],
                    "sanctuary_state": "INTACT",
                    "inhabitants_unharmed": True,
                    "shell_only_breach": shell_only,
                    "crack_origin_px": list(crack_origin) if crack_origin else ([260, 200] if stage.startswith("E_") else None),
                    "crack_rays_radial_from_P": stage in {"E_MID_GLOW_CRACKS_FROM_P", "E_END_SHELL_SHATTER_FROM_P"},
                    "fragments_propagate_outward_from_P": stage == "E_END_SHELL_SHATTER_FROM_P",
                },
            },
        }
        if stage != "B_LOCKED_TOOL_MASTER" and mask_path is not None:
            evidence["edit_mask_path"] = str(mask_path.resolve())
            evidence["edit_mask_parent_sha256"] = parent_sha
        if stage == "B_LOCKED_TOOL_MASTER":
            evidence["master_selection"] = {
                "selection_mode": selection_mode,
                "selection_reviewer": "test-human",
                "selection_notes": "ROI reviewed, chosen by position rather than label",
                "source_atlas_image_path": str(self.atlas),
                "source_atlas_raster_sha256": self.atlas_sha,
                "source_atlas_width_px": 400,
                "source_atlas_height_px": 300,
                "selected_roi_xyxy_px": [180, 70, 300, 250],
                "selected_tool_is_single_instance": True,
            }
        return evidence

    def test_prompt_packet_has_correct_planted_geometry_not_flying_hammer(self):
        packet = compile_prompt_packet(self.root / "packet")
        self.assertEqual(len(packet["stages"]), 7)
        self.assertEqual(packet["image_realization"], "NOT_RUN_BY_PROMPT_COMPILER")
        d2 = (self.root / "packet" / packet["stages"]["D2_FIRST_GRIP_EXISTING_HANDLE"]["prompt_file"]).read_text(encoding="utf-8")
        self.assertIn("Move hands/forearms to the existing rod", d2)
        self.assertIn("never move the rod to the hands", d2)
        e = (self.root / "packet" / packet["stages"]["E_MID_GLOW_CRACKS_FROM_P"]["prompt_file"]).read_text(encoding="utf-8")
        self.assertIn("base-interface glow", e.lower())
        self.assertIn("planted", e.lower())

    def test_master_selection_must_be_roi_based_and_raster_bound(self):
        image = self.make_image("B.png", (10, 20, 30))
        evidence = self.make_evidence("B_LOCKED_TOOL_MASTER", image, parent_sha=None, anchor_sha=None)
        result = validate_planted_bubble_frame(image, evidence, expected_stage="B_LOCKED_TOOL_MASTER")
        self.assertTrue(result["contract_valid"], result["errors"])
        self.assertEqual(result["visual_acceptance_status"], "NOT_VERIFIED_BY_CODE")
        evidence["master_selection"]["selection_mode"] = "LABEL_ONLY"
        result = validate_planted_bubble_frame(image, evidence, expected_stage="B_LOCKED_TOOL_MASTER")
        self.assertFalse(result["contract_valid"])
        self.assertIn("MASTER_SELECTION_MUST_USE_EXPLICIT_HUMAN_ROI_NOT_LABEL_ONLY", result["errors"])

    def test_side_handle_track_and_no_new_stub_are_hard_locks(self):
        parent = self.make_image("B.png", (10, 20, 30))
        parent_sha = sha256_file(parent)
        image = self.make_image("D2.png", (40, 50, 60))
        evidence = self.make_evidence("D2_FIRST_GRIP_EXISTING_HANDLE", image, parent_sha=parent_sha, anchor_sha=parent_sha, add_stub=True)
        result = validate_planted_bubble_frame(image, evidence, expected_stage="D2_FIRST_GRIP_EXISTING_HANDLE", expected_parent_sha256=parent_sha, expected_anchor_sha256=parent_sha, expected_cylinder_instance_id="CYLINDER_01", expected_handle_track_id="HANDLE_01")
        self.assertFalse(result["contract_valid"])
        self.assertIn("NEW_HANDLE_OR_STUB_DETECTED_OR_UNVERIFIED", result["errors"])

        evidence = self.make_evidence("D2_FIRST_GRIP_EXISTING_HANDLE", image, parent_sha=parent_sha, anchor_sha=parent_sha, grip_wrong_handle=True)
        result = validate_planted_bubble_frame(image, evidence, expected_stage="D2_FIRST_GRIP_EXISTING_HANDLE", expected_parent_sha256=parent_sha, expected_anchor_sha256=parent_sha, expected_cylinder_instance_id="CYLINDER_01", expected_handle_track_id="HANDLE_01")
        self.assertFalse(result["contract_valid"])
        self.assertIn("HEROINE_NOT_GRIPPING_THE_LOCKED_HANDLE_INSTANCE", result["errors"])

    def test_later_frame_cannot_shift_handle_even_if_it_reuses_the_same_track_id(self):
        master = self.make_image("B_lock.png", (10, 20, 30))
        master_ev = self.make_evidence("B_LOCKED_TOOL_MASTER", master, parent_sha=None, anchor_sha=None)
        master_result = validate_planted_bubble_frame(master, master_ev, expected_stage="B_LOCKED_TOOL_MASTER")
        self.assertTrue(master_result["contract_valid"], master_result["errors"])

        child = self.make_image("D1_handle_shift.png", (30, 40, 50))
        child_sha = sha256_file(child)
        master_sha = sha256_file(master)
        child_ev = self.make_evidence("D1_APPROACH_NO_GRIP", child, parent_sha=master_sha, anchor_sha=master_sha)
        handle = child_ev["raster_annotations"]["planted_cylinder"]["side_handle"]
        handle["bbox_xyxy_px"] = [175, 194, 270, 206]
        handle["axis_start_px"] = [175, 200]
        handle["axis_end_px"] = [270, 200]
        child_ev["raster_sha256"] = child_sha
        child_ev["parent_raster_sha256"] = master_sha
        child_ev["scene_anchor_raster_sha256"] = master_sha
        child_ev["review"]["reviewed_raster_sha256"] = child_sha
        child_ev["review"]["reviewed_parent_sha256"] = master_sha
        child_ev["review"]["reviewed_scene_anchor_sha256"] = master_sha

        result = validate_planted_bubble_frame(
            child,
            child_ev,
            expected_stage="D1_APPROACH_NO_GRIP",
            expected_parent_sha256=master_sha,
            expected_anchor_sha256=master_sha,
            locked_contact_point_px=(260, 200),
            expected_cylinder_instance_id="CYLINDER_01",
            expected_handle_track_id="HANDLE_01",
            expected_locked_geometry=master_result["locked_geometry"],
        )
        self.assertFalse(result["contract_valid"])
        self.assertIn("HANDLE_AXIS_START_DRIFTED", result["errors"])
        self.assertIn("HANDLE_BBOX_CHANGED_FROM_MASTER", result["errors"])

    def test_e_mid_requires_cracks_from_same_p_and_shell_only_breach(self):
        parent = self.make_image("D3.png", (10, 20, 30))
        parent_sha = sha256_file(parent)
        image = self.make_image("E_mid.png", (40, 50, 60))
        evidence = self.make_evidence("E_MID_GLOW_CRACKS_FROM_P", image, parent_sha=parent_sha, anchor_sha=parent_sha, crack_origin=(310, 250), shell_only=False)
        result = validate_planted_bubble_frame(image, evidence, expected_stage="E_MID_GLOW_CRACKS_FROM_P", expected_parent_sha256=parent_sha, expected_anchor_sha256=parent_sha, expected_cylinder_instance_id="CYLINDER_01", expected_handle_track_id="HANDLE_01")
        self.assertFalse(result["contract_valid"])
        self.assertIn("CRACKS_DO_NOT_ORIGINATE_AT_P", result["errors"])
        self.assertIn("BREACH_IS_NOT_SHELL_ONLY", result["errors"])

    def test_stage_masks_are_real_binary_artifacts_and_freeze_the_planted_cylinder(self):
        parent = self.make_image("D1_for_mask.png", (10, 20, 30))
        parent_sha = sha256_file(parent)
        evidence = self.make_evidence("D1_APPROACH_NO_GRIP", parent, parent_sha=parent_sha, anchor_sha=parent_sha)
        masks = build_stage_masks(parent, evidence, "D2_FIRST_GRIP_EXISTING_HANDLE", self.root / "mask_packet")
        edit = Image.open(masks["edit_mask_path"]).convert("L")
        freeze = Image.open(masks["freeze_mask_path"]).convert("L")
        edit_values = set(edit.getdata())
        freeze_values = set(freeze.getdata())
        self.assertLessEqual(edit_values, {0, 255})
        self.assertLessEqual(freeze_values, {0, 255})
        self.assertGreater(sum(1 for v in edit.getdata() if v == 255), 100)
        self.assertEqual(edit.getpixel((260, 230)), 0)  # cylinder body is protected
        self.assertEqual(edit.getpixel((210, 200)), 255)  # existing handle can be occluded by the gripping hands
        self.assertEqual(edit.getpixel((260, 230)) + freeze.getpixel((260, 230)), 255)
        self.assertIn("mask_status", masks)
        self.assertTrue(Path(masks["edit_mask_path"]).is_file())
        self.assertTrue(Path(masks["freeze_mask_path"]).is_file())

    def test_changed_raster_cannot_reuse_old_review_receipt(self):
        image = self.make_image("B.png", (10, 20, 30))
        evidence = self.make_evidence("B_LOCKED_TOOL_MASTER", image, parent_sha=None, anchor_sha=None)
        image.write_bytes(image.read_bytes() + b"tamper")
        result = validate_planted_bubble_frame(image, evidence, expected_stage="B_LOCKED_TOOL_MASTER")
        self.assertFalse(result["contract_valid"])
        self.assertIn("RASTER_SHA256_MISMATCH", result["errors"])

    def test_provider_run_blocks_without_explicit_master_roi_selection(self):
        outdir = self.root / "missing_selection_run"
        calls = []

        def provider(request: dict, request_dir: Path):
            calls.append(request)
            return []

        report = run_planted_bubble_closed_loop(outdir, rerun_provider=provider, max_retries=1)
        self.assertFalse(report["next_stage_allowed"])
        self.assertEqual(report["accepted_stage_count"], 0)
        self.assertEqual(calls, [])
        self.assertIn("BLOCKED", report["status"])

    def test_pipeline_uses_feedback_and_retries_from_last_pass_parent(self):
        outdir = self.root / "run"
        calls = []
        counter = 0

        def provider(request: dict, request_dir: Path):
            nonlocal counter
            calls.append(dict(request))
            stage = request["stage"]
            attempt = request["attempt_round"]
            parent_path = Path(request["parent_image_path"]) if request.get("parent_image_path") else None
            parent_sha = request.get("parent_raster_sha256")
            anchor_sha = request.get("scene_anchor_raster_sha256")
            raw_image = self.make_image(f"{stage}_R{attempt}_raw.png", (20 + len(calls), 40, 60))
            mask_for_evidence = None
            image = raw_image
            if stage != "B_LOCKED_TOOL_MASTER":
                self.assertTrue(parent_path and parent_path.is_file(), request)
                edit_path = Path(request["edit_mask_path"])
                freeze_path = Path(request["freeze_mask_path"])
                self.assertTrue(edit_path.is_file(), request)
                self.assertTrue(freeze_path.is_file(), request)
                self.assertEqual(request["mask_provenance_parent_sha256"], parent_sha)
                composed = request_dir / f"{stage}_R{attempt}_composed.png"
                compose_masked_edit(parent_path, raw_image, edit_path, composed)
                frozen = validate_frozen_pixels(parent_path, composed, edit_path)
                self.assertTrue(frozen["passed"], frozen)
                mask_for_evidence = edit_path
                image = composed
            evidence = self.make_evidence(stage, image, parent_sha=parent_sha, anchor_sha=anchor_sha, mask_path=mask_for_evidence)
            if stage == "D2_FIRST_GRIP_EXISTING_HANDLE" and attempt == 0:
                evidence["raster_annotations"]["planted_cylinder"]["additional_handle_or_stub_detected"] = True
            return [Candidate(image, evidence)]

        report = run_planted_bubble_closed_loop(
            outdir,
            rerun_provider=provider,
            max_retries=2,
            master_selection=self.make_master_selection(),
        )
        self.assertTrue(report["next_stage_allowed"], report["status"])
        self.assertEqual(report["accepted_stage_count"], len(STAGE_ORDER))
        d2_calls = [r for r in calls if r["stage"] == "D2_FIRST_GRIP_EXISTING_HANDLE"]
        self.assertEqual([r["attempt_round"] for r in d2_calls], [0, 1])
        self.assertEqual(d2_calls[1]["parent_raster_sha256"], d2_calls[0]["parent_raster_sha256"])
        self.assertEqual(d2_calls[1]["parent_image_path"], d2_calls[0]["parent_image_path"])
        d2_second = next(x for x in report["attempt_log"] if x["stage"] == "D2_FIRST_GRIP_EXISTING_HANDLE" and x["attempt_round"] == 1)
        self.assertTrue(d2_second["eligible_for_next_stage"])
        self.assertTrue(d2_second["selected"])
        self.assertFalse(any(x["selected"] for x in report["attempt_log"] if x["stage"] == "D2_FIRST_GRIP_EXISTING_HANDLE" and x["attempt_round"] == 0))
        self.assertIn("NEW_HANDLE_OR_STUB_DETECTED_OR_UNVERIFIED", d2_calls[1].get("repair_error_vector", []))
        self.assertEqual(calls[0]["master_selection"]["selected_roi_xyxy_px"], [180, 70, 300, 250])
        self.assertTrue(d2_calls[1].get("diagnostic_experiment"), d2_calls[1])
        self.assertEqual(
            d2_calls[1]["diagnostic_experiment"]["action_id"],
            "EXISTING_HANDLE_TRACK_AUDIT",
        )
        self.assertIn(
            "SHANNON-STYLE NEXT DIAGNOSTIC",
            d2_calls[1]["prompt"],
        )
