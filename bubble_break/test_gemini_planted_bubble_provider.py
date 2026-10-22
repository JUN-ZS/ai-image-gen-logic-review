from __future__ import annotations

import base64
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from bubble_break.gemini_planted_bubble_provider import (
    DEFAULT_API_URL,
    DEFAULT_IMAGE_MODEL,
    DEFAULT_REVIEW_MODEL,
    GeminiPlantedBubbleProvider,
    sha256_file,
)


def png_bytes(size=(400, 300), colour=(30, 40, 50)) -> bytes:
    image = Image.new("RGB", size, colour)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def review_fixture(stage: str, image_bytes: bytes, decision="FAIL") -> dict:
    with Image.open(io.BytesIO(image_bytes)) as image:
        width, height = image.size
    grip = stage in {
        "D2_FIRST_GRIP_EXISTING_HANDLE", "D3_TENSION_EXISTING_HANDLE",
        "E_MID_GLOW_CRACKS_FROM_P", "E_END_SHELL_SHATTER_FROM_P",
    }
    has_cracks = stage in {"E_MID_GLOW_CRACKS_FROM_P", "E_END_SHELL_SHATTER_FROM_P"}
    shell_state = {
        "B_LOCKED_TOOL_MASTER": "INTACT",
        "C_PERSON_SCALE_NO_GRIP": "INTACT",
        "D1_APPROACH_NO_GRIP": "INTACT",
        "D2_FIRST_GRIP_EXISTING_HANDLE": "INTACT",
        "D3_TENSION_EXISTING_HANDLE": "INTACT",
        "E_MID_GLOW_CRACKS_FROM_P": "CRACKING_NOT_SHATTERED",
        "E_END_SHELL_SHATTER_FROM_P": "SHATTERED",
    }[stage]
    crack_state = "RADIAL_FROM_P" if stage == "E_MID_GLOW_CRACKS_FROM_P" else ("SHATTERED_OUTWARD_FROM_P" if stage == "E_END_SHELL_SHATTER_FROM_P" else "NONE")
    return {
        "decision": decision,
        "notes": "Test fixture only; model review was deliberately FAIL to verify fail-closed behavior.",
        "creativity_score": 0.65,
        "novelty_score": 0.55,
        "raster_annotations": {
            "image_width_px": width,
            "image_height_px": height,
            "bubble": {"center_px": [260, 120], "radius_px": 80},
            "contact_point_p_px": [260, 200],
            "sanctuary_bbox_xyxy_px": [230, 90, 290, 150],
            "planted_cylinder": {
                "instance_id": "CYLINDER_TEST",
                "body_bbox_xyxy_px": [240, 198, 280, 270],
                "base_seat_center_px": [260, 200],
                "outer_end_cap_center_px": [260, 262],
                "base_seat_surface": "CONFORMAL_CURVED_SEAT_TO_BUBBLE",
                "full_base_contact_verified": True,
                "outer_end_cap_clear": True,
                "additional_handle_or_stub_detected": False,
                "body_axis_world": [0, 1, 0],
                "bubble_surface_normal_world": [0, 1, 0],
                "base_center_world": [0, 0, 0],
                "outer_end_cap_center_world": [0, 1, 0],
                "side_handle": {
                    "track_id": "HANDLE_TEST",
                    "bbox_xyxy_px": [165, 194, 260, 206],
                    "axis_start_px": [165, 200],
                    "axis_end_px": [260, 200],
                    "axis_world": [1, 0, 0],
                    "attachment_world": [0, 0.5, 0],
                },
            },
            "heroine": {
                "present": stage != "B_LOCKED_TOOL_MASTER",
                "bbox_xyxy_px": [20, 100, 120, 280] if stage != "B_LOCKED_TOOL_MASTER" else None,
                "scale_class": "MINIATURE" if stage != "B_LOCKED_TOOL_MASTER" else None,
                "gripping_handle_track_id": "HANDLE_TEST" if grip else None,
                "both_hands_on_existing_handle": grip,
            },
            "shell": {
                "state": shell_state,
                "crack_state": crack_state,
                "base_glow_on_conformal_seat": True,
                "base_glow_origin_px": [260, 200],
                "sanctuary_state": "INTACT",
                "inhabitants_unharmed": True,
                "shell_only_breach": has_cracks,
                "crack_origin_px": [260, 200] if has_cracks else None,
            },
        },
    }


class GeminiPlantedBubbleProviderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.generated_bytes = png_bytes()
        self.reviews = []
        self.requests = []

        def fake_post(payload):
            self.requests.append(payload)
            if payload.get("model") == DEFAULT_IMAGE_MODEL:
                return {
                    "output_image": {
                        "data": base64.b64encode(self.generated_bytes).decode("ascii"),
                        "mime_type": "image/png",
                    }
                }
            # Extract stage from the review's prompt; production prompts deliberately name this field.
            input_items = payload.get("input", [])
            prompt = " ".join(item.get("text", "") for item in input_items if isinstance(item, dict))
            stage = next(
                s for s in (
                    "B_LOCKED_TOOL_MASTER", "C_PERSON_SCALE_NO_GRIP", "D1_APPROACH_NO_GRIP",
                    "D2_FIRST_GRIP_EXISTING_HANDLE", "D3_TENSION_EXISTING_HANDLE",
                    "E_MID_GLOW_CRACKS_FROM_P", "E_END_SHELL_SHATTER_FROM_P",
                ) if f"STAGE: {s}" in prompt
            )
            review = review_fixture(stage, self.generated_bytes, decision="FAIL")
            self.reviews.append(review)
            return {"output_text": json.dumps(review)}

        self.provider = GeminiPlantedBubbleProvider(api_key="unit-test-key", post_json=fake_post)

    def master_request(self) -> dict:
        atlas = self.root / "source_atlas.png"
        Image.new("RGB", (400, 300), (22, 25, 35)).save(atlas)
        roi = self.root / "selected_roi.png"
        Image.new("RGB", (120, 180), (50, 60, 70)).save(roi)
        return {
            "contract_id": "PLANTED_DOUBLE_ENDED_CYLINDER_BUBBLE_CONTACT_V1",
            "contract_sha256": "test-contract-fingerprint",
            "stage": "B_LOCKED_TOOL_MASTER",
            "attempt_round": 0,
            "prompt": "Isolate only the double-ended planted cylinder within the explicit selected ROI.",
            "parent_image_path": None,
            "parent_raster_sha256": None,
            "scene_anchor_raster_sha256": None,
            "master_selection": {
                "selection_mode": "HUMAN_ROI",
                "selection_reviewer": "test-human",
                "selection_notes": "Explicit ROI selected in this test fixture",
                "source_atlas_image_path": str(atlas),
                "source_atlas_raster_sha256": sha256_file(atlas),
                "source_atlas_width_px": 400,
                "source_atlas_height_px": 300,
                "selected_roi_xyxy_px": [50, 40, 170, 220],
                "selected_roi_crop_path": str(roi),
                "selected_roi_crop_sha256": sha256_file(roi),
                "selected_tool_is_single_instance": True,
            },
        }

    def test_master_stage_sends_selected_roi_and_preserves_model_fail(self):
        request = self.master_request()
        request_path = self.root / "request.json"
        request_path.write_text(json.dumps(request), encoding="utf-8")
        response = self.provider(request, self.root / "attempt_B")
        self.assertEqual(len(response), 1)
        candidate = response[0]
        image_path = Path(candidate["image"])
        self.assertTrue(image_path.is_file())
        with Image.open(image_path) as saved_image, Image.open(io.BytesIO(self.generated_bytes)) as source_image:
            self.assertEqual(saved_image.format, "PNG")
            self.assertEqual(saved_image.size, source_image.size)
            self.assertEqual(list(saved_image.convert("RGB").getdata()), list(source_image.convert("RGB").getdata()))
        evidence = candidate["evidence"]
        self.assertEqual(sha256_file(image_path), evidence["raster_sha256"])
        self.assertEqual(evidence["review"]["decision"], "FAIL")
        self.assertEqual(evidence["review"]["mode"], "SEMANTIC_VISION_REVIEW")
        self.assertEqual(evidence["review"]["reviewed_raster_sha256"], evidence["raster_sha256"])
        self.assertEqual(evidence["scene_anchor_raster_sha256"], evidence["raster_sha256"])
        self.assertEqual(evidence["master_selection"], request["master_selection"])
        self.assertEqual(self.requests[0]["model"], DEFAULT_IMAGE_MODEL)
        input_images = [x for x in self.requests[0]["input"] if x.get("type") == "image"]
        self.assertEqual(len(input_images), 2)  # selected crop first, entire source atlas as context
        self.assertEqual(self.requests[1]["model"], DEFAULT_REVIEW_MODEL)
        self.assertEqual(self.requests[1]["response_format"]["mime_type"], "application/json")
        audit = json.loads((self.root / "attempt_B" / "semantic_review.json").read_text(encoding="utf-8"))
        self.assertEqual(audit["decision"], "FAIL")
        self.assertEqual(audit["raster_sha256"], evidence["raster_sha256"])

    def test_followup_stage_includes_parent_and_both_masks(self):
        parent = self.root / "parent.png"
        edit = self.root / "edit_mask.png"
        freeze = self.root / "freeze_mask.png"
        Image.new("RGB", (400, 300), (10, 20, 30)).save(parent)
        Image.new("L", (400, 300), 255).save(edit)
        Image.new("L", (400, 300), 0).save(freeze)
        parent_sha = sha256_file(parent)
        request = {
            "contract_id": "PLANTED_DOUBLE_ENDED_CYLINDER_BUBBLE_CONTACT_V1",
            "contract_sha256": "test-contract-fingerprint",
            "stage": "D2_FIRST_GRIP_EXISTING_HANDLE",
            "attempt_round": 1,
            "prompt": "Move only hands/forearms to grip the same existing handle.",
            "parent_image_path": str(parent),
            "parent_raster_sha256": parent_sha,
            "scene_anchor_raster_sha256": "locked-master-sha",
            "edit_mask_path": str(edit),
            "freeze_mask_path": str(freeze),
            "mask_provenance_parent_sha256": parent_sha,
            "repair_error_vector": ["NEW_HANDLE_OR_STUB_DETECTED_OR_UNVERIFIED"],
            "authorized_delta_fields": ["heroine_hands_and_forearms"],
            "must_preserve": ["side_handle_instance_and_axis"],
        }
        response = self.provider(request, self.root / "attempt_D2")
        self.assertEqual(len(response), 1)
        gen_images = [x for x in self.requests[0]["input"] if x.get("type") == "image"]
        self.assertEqual(len(gen_images), 3)
        self.assertEqual(self.requests[0]["model"], DEFAULT_IMAGE_MODEL)
        self.assertIn("Move only hands/forearms", self.requests[0]["input"][0]["text"])
        evidence = response[0]["evidence"]
        self.assertEqual(evidence["parent_raster_sha256"], parent_sha)
        self.assertEqual(evidence["scene_anchor_raster_sha256"], "locked-master-sha")
        self.assertEqual(evidence["review"]["reviewed_parent_sha256"], parent_sha)
        self.assertEqual(evidence["review"]["reviewed_scene_anchor_sha256"], "locked-master-sha")

    def test_missing_key_and_image_free_response_block(self):
        with self.assertRaisesRegex(ValueError, "GEMINI_API_KEY"):
            GeminiPlantedBubbleProvider(api_key="")

        provider = GeminiPlantedBubbleProvider(api_key="unit-test-key", post_json=lambda _payload: {"output_text": "no image"})
        request = self.master_request()
        with self.assertRaisesRegex(ValueError, "no output image"):
            provider._generate(request, "B_LOCKED_TOOL_MASTER", self.root / "no_image")


if __name__ == "__main__":
    unittest.main(verbosity=2)
