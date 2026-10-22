#!/usr/bin/env python3
"""Live Gemini image-generation + semantic-review adapter for the planted-cylinder workflow.

This is an actual provider adapter, not a pre-generated image fixture. It requires GEMINI_API_KEY.
It makes one image-generation/edit request and one separate vision-review request per attempt.
The output is still only a structured evidence packet: the pipeline's final visual status remains
NOT_VERIFIED_BY_CODE, and an external human must review actual outputs before claiming acceptance.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import mimetypes
import math
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from PIL import Image

from bubble_break.planted_bubble_closed_loop import (
    authorized_pixel_delta,
    background_landmarks_sha256,
    compose_masked_edit,
    sha256_file as pipeline_sha256_file,
    validate_frozen_pixels,
)

DEFAULT_API_URL = "https://generativelanguage.googleapis.com/v1beta/interactions"
DEFAULT_IMAGE_MODEL = "gemini-nano-banana-2.1"
DEFAULT_REVIEW_MODEL = "gemini-3.8-flash"
STAGE_ORDER = (
    "B_LOCKED_TOOL_MASTER",
    "C_PERSON_SCALE_NO_GRIP",
    "D1_APPROACH_NO_GRIP",
    "D2_FIRST_GRIP_EXISTING_HANDLE",
    "D3_TENSION_EXISTING_HANDLE",
    "E_MID_GLOW_CRACKS_FROM_P",
    "E_END_SHELL_SHATTER_FROM_P",
)


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _mime_type(path: Path) -> str:
    return mimetypes.guess_type(path.name)[0] or "application/octet-stream"


def _image_input(path: Path, label: str) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"{label} is required but missing: {path}")
    mime_type = _mime_type(path)
    if not mime_type.startswith("image/"):
        raise ValueError(f"{label} is not a recognized image file: {path}")
    return {
        "type": "image",
        "mime_type": mime_type,
        "data": base64.b64encode(path.read_bytes()).decode("ascii"),
        "_label": label,
    }


def _public_input(item: Mapping[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in item.items() if not key.startswith("_")}


def _safe_json_from_interaction(response: dict[str, Any]) -> dict[str, Any]:
    """Extract structured text across the Interactions API's text/output response shapes."""
    text = response.get("output_text")
    if isinstance(text, str) and text.strip():
        return json.loads(text)
    for step in response.get("steps", []) if isinstance(response.get("steps"), list) else []:
        if not isinstance(step, dict) or step.get("type") != "model_output":
            continue
        for block in step.get("content", []) if isinstance(step.get("content"), list) else []:
            if isinstance(block, dict) and block.get("type") == "text" and isinstance(block.get("text"), str):
                candidate = block["text"].strip()
                if candidate:
                    return json.loads(candidate)
    raise ValueError("Gemini review response contained no parseable JSON text")


def _extract_generated_image(response: dict[str, Any]) -> tuple[bytes, str]:
    """Read the documented output_image form, with model_output blocks as a fallback."""
    output = response.get("output_image")
    if isinstance(output, dict) and isinstance(output.get("data"), str):
        try:
            data = base64.b64decode(output["data"], validate=True)
        except ValueError as exc:
            raise ValueError("Gemini output_image.data is not valid base64") from exc
        return data, str(output.get("mime_type") or "image/png")

    for step in response.get("steps", []) if isinstance(response.get("steps"), list) else []:
        if not isinstance(step, dict) or step.get("type") != "model_output":
            continue
        for block in step.get("content", []) if isinstance(step.get("content"), list) else []:
            if isinstance(block, dict) and block.get("type") == "image" and isinstance(block.get("data"), str):
                try:
                    data = base64.b64decode(block["data"], validate=True)
                except ValueError as exc:
                    raise ValueError("Gemini image content block is not valid base64") from exc
                return data, str(block.get("mime_type") or "image/png")
    raise ValueError("Gemini generation response contained no output image")


def _schema_point(length: int) -> dict[str, Any]:
    return {"type": "array", "items": {"type": "number"}, "minItems": length, "maxItems": length}


def _schema_bbox() -> dict[str, Any]:
    return _schema_point(4)


def _build_review_schema() -> dict[str, Any]:
    point2 = _schema_point(2)
    point3 = _schema_point(3)
    nullable_point2 = {"type": ["array", "null"], "items": {"type": "number"}}
    nullable_string = {"type": ["string", "null"]}
    nullable_bbox = {"type": ["array", "null"], "items": {"type": "number"}}
    nullable_long_string = {"type": ["string", "null"]}
    string = {"type": "string"}
    boolean = {"type": "boolean"}
    number = {"type": "number"}
    planted_cylinder = {
        "type": "object",
        "properties": {
            "instance_id": string,
            "body_bbox_xyxy_px": _schema_bbox(),
            "base_seat_center_px": point2,
            "outer_end_cap_center_px": point2,
            "base_seat_surface": string,
            "full_base_contact_verified": boolean,
            "outer_end_cap_clear": boolean,
            "additional_handle_or_stub_detected": boolean,
            "body_axis_world": point3,
            "bubble_surface_normal_world": point3,
            "base_center_world": point3,
            "outer_end_cap_center_world": point3,
            "side_handle": {
                "type": "object",
                "properties": {
                    "track_id": string,
                    "bbox_xyxy_px": _schema_bbox(),
                    "axis_start_px": point2,
                    "axis_end_px": point2,
                    "axis_world": point3,
                    "attachment_world": point3,
                },
                "required": ["track_id", "bbox_xyxy_px", "axis_start_px", "axis_end_px", "axis_world", "attachment_world"],
            },
        },
        "required": [
            "instance_id", "body_bbox_xyxy_px", "base_seat_center_px", "outer_end_cap_center_px",
            "base_seat_surface", "full_base_contact_verified", "outer_end_cap_clear",
            "additional_handle_or_stub_detected", "body_axis_world", "bubble_surface_normal_world",
            "base_center_world", "outer_end_cap_center_world", "side_handle",
        ],
    }
    heroine = {
        "type": "object",
        "properties": {
            "present": boolean,
            "bbox_xyxy_px": nullable_bbox,
            "scale_class": nullable_string,
            "identity_id": nullable_string,
            "pose_signature": nullable_long_string,
            "gripping_handle_track_id": nullable_string,
            "both_hands_on_existing_handle": boolean,
        },
        "required": ["present", "bbox_xyxy_px", "scale_class", "identity_id", "pose_signature", "gripping_handle_track_id", "both_hands_on_existing_handle"],
    }
    shell = {
        "type": "object",
        "properties": {
            "state": string,
            "crack_state": string,
            "base_glow_on_conformal_seat": boolean,
            "base_glow_origin_px": point2,
            "sanctuary_state": string,
            "inhabitants_unharmed": boolean,
            "shell_only_breach": boolean,
            "crack_origin_px": nullable_point2,
            "crack_rays_radial_from_P": boolean,
            "fragments_propagate_outward_from_P": boolean,
        },
        "required": [
            "state", "crack_state", "base_glow_on_conformal_seat", "base_glow_origin_px",
            "sanctuary_state", "inhabitants_unharmed", "shell_only_breach", "crack_origin_px",
            "crack_rays_radial_from_P", "fragments_propagate_outward_from_P",
        ],
    }
    return {
        "type": "object",
        "properties": {
            "decision": {"type": "string", "enum": ["PASS", "FAIL"]},
            "notes": string,
            "scene_id": string,
            "camera_rig_id": string,
            "camera_view_fingerprint": string,
            "creativity_score": number,
            "novelty_score": number,
            "raster_annotations": {
                "type": "object",
                "properties": {
                    "image_width_px": {"type": "integer"},
                    "image_height_px": {"type": "integer"},
                    "bubble": {
                        "type": "object",
                        "properties": {"center_px": point2, "radius_px": number},
                        "required": ["center_px", "radius_px"],
                    },
                    "contact_point_p_px": point2,
                    "sanctuary_bbox_xyxy_px": _schema_bbox(),
                    "planted_cylinder": planted_cylinder,
                    "heroine": heroine,
                    "shell": shell,
                },
                "required": [
                    "image_width_px", "image_height_px", "bubble", "contact_point_p_px",
                    "sanctuary_bbox_xyxy_px", "planted_cylinder", "heroine", "shell",
                ],
            },
        },
        "required": ["decision", "notes", "scene_id", "camera_rig_id", "camera_view_fingerprint", "creativity_score", "novelty_score", "raster_annotations"],
    }


REVIEW_SCHEMA = _build_review_schema()


class GeminiPlantedBubbleProvider:
    """Real Google Gemini API adapter for the planted-cylinder stage request protocol.

    The generator and semantic reviewer are separate interactions. Both are fallible models;
    their output cannot self-authenticate. The surrounding pipeline binds model annotations to
    exact hashes and still leaves final human visual acceptance unverified by code.
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        image_model: str | None = None,
        review_model: str | None = None,
        api_url: str | None = None,
        timeout_seconds: int = 240,
        post_json: Callable[[dict[str, Any]], dict[str, Any]] | None = None,
    ) -> None:
        self.api_key = api_key if api_key is not None else os.environ.get("GEMINI_API_KEY", "")
        if not self.api_key.strip():
            raise ValueError("GEMINI_API_KEY is required; refusing to fabricate a candidate")
        self.image_model = image_model or os.environ.get("GEMINI_IMAGE_MODEL", DEFAULT_IMAGE_MODEL)
        self.review_model = review_model or os.environ.get("GEMINI_REVIEW_MODEL", DEFAULT_REVIEW_MODEL)
        self.api_url = api_url or os.environ.get("GEMINI_INTERACTIONS_URL", DEFAULT_API_URL)
        self.timeout_seconds = int(timeout_seconds)
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        self._post_json_override = post_json

    def _post_json(self, payload: dict[str, Any]) -> dict[str, Any]:
        if self._post_json_override is not None:
            return self._post_json_override(payload)
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        request = urllib.request.Request(
            self.api_url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": self.api_key,
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                raw = response.read()
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")[:1200]
            raise RuntimeError(f"Gemini API HTTP {exc.code}: {body}") from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            raise RuntimeError(f"Gemini API request failed: {exc}") from exc
        try:
            decoded = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Gemini API returned a non-JSON response") from exc
        if not isinstance(decoded, dict):
            raise ValueError("Gemini API response must be a JSON object")
        return decoded

    def _resolve(self, value: str | None, request_dir: Path, label: str) -> Path | None:
        if not value:
            return None
        path = Path(value)
        if not path.is_absolute():
            path = request_dir / path
        path = path.resolve()
        if not path.is_file():
            raise FileNotFoundError(f"{label} does not exist: {path}")
        return path

    def _stage_inputs(self, request: dict[str, Any], request_dir: Path, stage: str) -> list[dict[str, Any]]:
        refs: list[dict[str, Any]] = []
        if stage == "B_LOCKED_TOOL_MASTER":
            selection = request.get("master_selection")
            if not isinstance(selection, dict):
                raise ValueError("B_LOCKED_TOOL_MASTER requires a human master_selection ROI manifest")
            atlas = self._resolve(selection.get("source_atlas_image_path"), request_dir, "selected source atlas")
            if atlas is None:
                raise ValueError("source_atlas_image_path is required")
            if sha256_file(atlas) != selection.get("source_atlas_raster_sha256"):
                raise ValueError("source atlas SHA-256 does not match the human selection manifest")
            with Image.open(atlas) as im:
                im.load()
                size = im.size
            expected = (selection.get("source_atlas_width_px"), selection.get("source_atlas_height_px"))
            if size != expected:
                raise ValueError(f"source atlas size {size} does not match selection manifest {expected}")
            crop_path = self._resolve(selection.get("selected_roi_crop_path"), request_dir, "selected ROI crop")
            expected_crop_sha = selection.get("selected_roi_crop_sha256")
            if crop_path is not None and expected_crop_sha and sha256_file(crop_path) != expected_crop_sha:
                raise ValueError("selected ROI crop SHA-256 mismatch")
            if crop_path is None:
                roi = selection.get("selected_roi_xyxy_px")
                if not isinstance(roi, list) or len(roi) != 4:
                    raise ValueError("selected_roi_xyxy_px must be [x0,y0,x1,y1]")
                x0, y0, x1, y1 = (int(value) for value in roi)
                with Image.open(atlas) as im:
                    if not (0 <= x0 < x1 <= im.width and 0 <= y0 < y1 <= im.height):
                        raise ValueError("selected ROI lies outside the source atlas")
                    crop = im.crop((x0, y0, x1, y1))
                    crop_path = request_dir / "selected_roi_reviewed_crop.png"
                    crop.save(crop_path)
            # Supply the selected crop first. The full atlas is context only, never the selection key.
            refs.append(_image_input(crop_path, "human-selected master ROI crop"))
            refs.append(_image_input(atlas, "full source atlas context; use the explicit ROI only"))
        else:
            parent = self._resolve(request.get("parent_image_path"), request_dir, "accepted parent raster")
            if parent is None:
                raise ValueError(f"{stage} requires the last accepted parent image")
            expected_parent = request.get("parent_raster_sha256")
            if not expected_parent or sha256_file(parent) != expected_parent:
                raise ValueError("parent raster SHA-256 is missing or mismatched")
            refs.append(_image_input(parent, "last verified PASS parent raster"))
            # Masks are advisory edit/freeze regions, not segmentation. Still, pass both masks to the provider.
            for key, label in (("edit_mask_path", "white=editable mask"), ("freeze_mask_path", "white=protected freeze mask")):
                mask = self._resolve(request.get(key), request_dir, label)
                if mask is None:
                    raise ValueError(f"{stage} requires {key} and its matching mask artifact")
                expected_mask_parent = request.get("mask_provenance_parent_sha256")
                if expected_mask_parent and expected_mask_parent != expected_parent:
                    raise ValueError(f"{key} was built from a different parent SHA")
                refs.append(_image_input(mask, label))
        return refs

    def _generate(self, request: dict[str, Any], stage: str, request_dir: Path) -> Path:
        prompt = str(request.get("prompt", "")).strip()
        if not prompt:
            raise ValueError("stage prompt is missing")
        if request.get("contract_id") != "PLANTED_DOUBLE_ENDED_CYLINDER_BUBBLE_CONTACT_V1":
            raise ValueError("provider only accepts the planted-cylinder Bubble-Break contract")
        if request.get("stage") != stage:
            raise ValueError("request stage does not match payload stage")
        refs = self._stage_inputs(request, request_dir, stage)
        input_manifest = [f"Image {index}: {ref['_label']}" for index, ref in enumerate(refs, start=1)]
        if stage != "B_LOCKED_TOOL_MASTER":
            input_manifest.extend([
                "Edit mask convention: white pixels are editable; black pixels are frozen.",
                "Freeze mask convention: white pixels are protected; black pixels are not marked protected.",
                "Masks are conservative ROI hints, not semantic segmentation and not permission to change unapproved regions.",
            ])
        inputs = [{
            "type": "text",
            "text": prompt + "\n\nIMAGE INPUT MANIFEST:\n" + "\n".join(input_manifest),
        }]
        inputs.extend(_public_input(ref) for ref in refs)
        # Keep the policy explicit in the actual provider request, not merely in a side document.
        inputs.append({
            "type": "text",
            "text": (
                "Return exactly one full-frame 16:9 image, not a contact sheet. Follow the supplied "
                "human-selected ROI/approved parent and stage prompt. Treat masks only as edit/freeze hints, "
                "then obey the hard locks even if the requested edit seems easier by changing geometry. "
                "Do not invent evidence or annotations; a separate review model will assess the actual output."
            ),
        })
        payload = {
            "model": self.image_model,
            "input": inputs,
            "response_format": {
                "type": "image",
                "mime_type": "image/png",
                "aspect_ratio": "16:9",
                "image_size": os.environ.get("GEMINI_IMAGE_SIZE", "2K"),
            },
        }
        response = self._post_json(payload)
        image_bytes, _reported_mime = _extract_generated_image(response)
        out_path = request_dir / f"generated_{stage}_attempt_{int(request.get('attempt_round', 0)):02d}.png"
        try:
            # Normalize the provider bytes to a true PNG instead of trusting the response MIME
            # or filename; downstream hashing and the review request bind these exact output bytes.
            from io import BytesIO
            with Image.open(BytesIO(image_bytes)) as image:
                image.load()
                normalized = image.convert("RGB")
                normalized.save(out_path, format="PNG", optimize=True)
        except Exception as exc:
            out_path.unlink(missing_ok=True)
            raise ValueError(f"Gemini output is not a readable image: {exc}") from exc
        return out_path

    def _review(self, request: dict[str, Any], stage: str, raster: Path, request_dir: Path) -> dict[str, Any]:
        with Image.open(raster) as image:
            width, height = image.size
        refs = [_image_input(raster, "exact generated candidate raster to review")]
        parent_path = self._resolve(request.get("parent_image_path"), request_dir, "parent raster")
        if parent_path is not None:
            refs.append(_image_input(parent_path, "last accepted parent raster for comparison"))
        mask_context = []
        for key, label in (("edit_mask_path", "editable mask context"), ("freeze_mask_path", "protected mask context")):
            path = self._resolve(request.get(key), request_dir, label)
            if path:
                mask_context.append(_image_input(path, label))
        refs.extend(mask_context)
        ref_manifest = [f"Image {index}: {ref['_label']}" for index, ref in enumerate(refs, start=1)]
        ref_manifest = [f"Image {index}: {ref['_label']}" for index, ref in enumerate(refs, start=1)]
        review_prompt = (
            "You are the semantic-vision reviewer for a high-constraint planted-cylinder Bubble-Break frame. "
            "Inspect the ACTUAL candidate pixels, not only the prompt. The planted tool is a double-ended solid "
            "cylinder whose curved conformal base seat stays on the bubble at P. One existing straight handle "
            "attaches at the cylinder side-middle and runs tangent/transverse; the exposed outer circular cap is "
            "clear. This is NOT a flying hammer or T-v-T collision. Return the requested JSON annotation for the "
            "candidate, comparing to the accepted parent and honoring the supplied stage specification. Never "
            "copy coordinates from a prompt if they don't match the rendered pixels. Estimate pixel coordinates "
            f"and world directions carefully in the raster of size {width}x{height}. If any required geometric or "
            "semantic fact is ambiguous or cannot be seen, set decision=FAIL and explain the missing/ambiguous "
            "evidence. PASS only if all invariants required at this stage are visibly supported by the image.\n\n"
            f"STAGE: {stage}\n"
            f"STAGE SPECIFICATION: {json.dumps(request, ensure_ascii=False, separators=(',', ':'))}\n\n"
            "IMAGE INPUT MANIFEST (candidate is Image 1): " + "; ".join(ref_manifest) + ".\n"
            "Annotation rules: image_width_px/image_height_px must equal actual size; coordinates are pixels "
            "(x grows right, y grows down); boxes are [x0,y0,x1,y1]; world vectors are finite 3D vectors. "
            "Always report the cylinder/head, bubble center/radius, P, side handle and sanctuary boxes/axes. "
            "For B/C/D1/D2/D3 crack_origin_px must be null and shell crack_state NONE; for E-mid report "
            "CRACKING_NOT_SHATTERED and RADIAL_FROM_P; for E-end report SHATTERED and SHATTERED_OUTWARD_FROM_P. "
            "Also set crack_rays_radial_from_P=true only when the visible rays genuinely spread outward from the same P; "
            "set fragments_propagate_outward_from_P=true at E-end only when visible shell fragments travel outward from P. "
            "For D1/D2/D3, identity_id must track the same heroine and pose_signature must describe the actual visible pose, not copy the stage name. "
            "For child stages copy the exact scene_id, camera_rig_id and camera_view_fingerprint from parent_scene_identity in the request; if the raster visibly changes camera/view, set decision FAIL. "
            "For B, establish stable non-empty scene_id, camera_rig_id and camera_view_fingerprint values for this shot. "
            "The code calculates background_landmarks_sha256 from the final raster's protected edge pixels; do not invent that hash. "
            "base_glow_origin_px must be the visible conformal-seat glow. sanctuary_state is INTACT; "
            "inhabitants_unharmed must be true only when all visible residents are unharmed; uncertainty or visible harm "
            "must produce decision FAIL. In D2 and later, only the same existing side handle is allowed as the grip target. "
            "Score creativity/novelty 0..1 only after checking the physical locks; do not let style compensate for a failed physical contract."
        )
        input_items = [{"type": "text", "text": review_prompt}]
        input_items.extend(_public_input(ref) for ref in refs)
        payload = {
            "model": self.review_model,
            "input": input_items,
            "response_format": {"type": "text", "mime_type": "application/json", "schema": REVIEW_SCHEMA},
        }
        response = self._post_json(payload)
        reviewed = _safe_json_from_interaction(response)
        if not isinstance(reviewed, dict):
            raise ValueError("Gemini review JSON must be an object")
        if reviewed.get("decision") not in {"PASS", "FAIL"}:
            reviewed["decision"] = "FAIL"
            reviewed["notes"] = str(reviewed.get("notes", "")) + " Reviewer omitted a valid PASS/FAIL decision; fail-closed."
        # Child stages must preserve scene/camera identity; never silently accept a viewpoint reset.
        parent_identity = request.get("parent_scene_identity") if stage != "B_LOCKED_TOOL_MASTER" else None
        if stage != "B_LOCKED_TOOL_MASTER":
            if not isinstance(parent_identity, dict):
                reviewed["decision"] = "FAIL"
                reviewed["notes"] = str(reviewed.get("notes", "")) + " Missing parent scene/camera identity; continuity cannot be proven."
            else:
                for key in ("scene_id", "camera_rig_id", "camera_view_fingerprint"):
                    if reviewed.get(key) != parent_identity.get(key):
                        reviewed["decision"] = "FAIL"
                        reviewed["notes"] = str(reviewed.get("notes", "")) + f" {key} differs from the accepted parent; camera/scene continuity FAIL."
        # Software binds the model's visual observations to exact final raster bytes; it never changes FAIL to PASS.
        digest = sha256_file(raster)
        bg_digest = background_landmarks_sha256(raster)
        parent_sha = request.get("parent_raster_sha256")
        anchor_sha = digest if stage == "B_LOCKED_TOOL_MASTER" else request.get("scene_anchor_raster_sha256")
        evidence = {
            "contract_id": request["contract_id"],
            "contract_sha256": request["contract_sha256"],
            "stage": stage,
            "raster_sha256": digest,
            "parent_raster_sha256": parent_sha,
            "scene_anchor_raster_sha256": anchor_sha,
            "scene_id": str((parent_identity or {}).get("scene_id")) if parent_identity else str(reviewed.get("scene_id", "")).strip(),
            "camera_rig_id": str((parent_identity or {}).get("camera_rig_id")) if parent_identity else str(reviewed.get("camera_rig_id", "")).strip(),
            "camera_view_fingerprint": str((parent_identity or {}).get("camera_view_fingerprint")) if parent_identity else str(reviewed.get("camera_view_fingerprint", "")).strip(),
            "background_landmarks_sha256": bg_digest,
            "raster_annotations": reviewed.get("raster_annotations"),
            "review": {
                "decision": reviewed["decision"],
                "mode": "SEMANTIC_VISION_REVIEW",
                "reviewer_or_model": f"Google Gemini ({self.review_model})",
                "reviewed_raster_sha256": digest,
                "reviewed_parent_sha256": parent_sha,
                "reviewed_scene_anchor_sha256": anchor_sha,
                "stage": stage,
                "notes": str(reviewed.get("notes", "")).strip() or "No review notes returned; fail-closed review receipt.",
            },
            "selection_metrics": {
                "creativity_score": _bounded_score(reviewed.get("creativity_score")),
                "novelty_score": _bounded_score(reviewed.get("novelty_score")),
            },
        }
        if stage == "B_LOCKED_TOOL_MASTER":
            evidence["master_selection"] = dict(request["master_selection"])
        else:
            evidence["edit_mask_path"] = str(Path(request["edit_mask_path"]).resolve())
            evidence["edit_mask_parent_sha256"] = request.get("mask_provenance_parent_sha256")
        (request_dir / "semantic_review.json").write_text(json.dumps({
            "review_model": self.review_model,
            "decision": reviewed["decision"],
            "notes": evidence["review"]["notes"],
            "raster_sha256": digest,
            "reviewer_limit": "Model-generated semantic review is not independent proof or human visual acceptance.",
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return evidence

    def __call__(self, request: dict[str, Any], request_dir: Path) -> Sequence[Any]:
        request_dir.mkdir(parents=True, exist_ok=True)
        stage = str(request.get("stage", "")).upper()
        if stage not in STAGE_ORDER:
            raise ValueError(f"unsupported planted-cylinder stage: {stage!r}")
        generated = self._generate(request, stage, request_dir)
        final_raster = generated
        if stage != "B_LOCKED_TOOL_MASTER":
            parent_path = self._resolve(request.get("parent_image_path"), request_dir, "last accepted parent raster")
            edit_mask = self._resolve(request.get("edit_mask_path"), request_dir, "authorized edit mask")
            freeze_mask = self._resolve(request.get("freeze_mask_path"), request_dir, "protected freeze mask")
            if parent_path is None or edit_mask is None or freeze_mask is None:
                raise ValueError(f"{stage} requires a parent raster and both masks")
            parent_sha = request.get("parent_raster_sha256")
            if not parent_sha or pipeline_sha256_file(parent_path) != parent_sha:
                raise ValueError("parent raster SHA-256 mismatch before mask compositing")
            if request.get("mask_provenance_parent_sha256") != parent_sha:
                raise ValueError("mask provenance does not match the last accepted parent")
            with Image.open(edit_mask) as e_im, Image.open(freeze_mask) as f_im:
                edit_values = e_im.convert("L")
                freeze_values = f_im.convert("L")
                if edit_values.size != freeze_values.size:
                    raise ValueError("edit/freeze mask dimensions differ")
                if ImageChops.difference(edit_values.point(lambda v: 255 if v >= 128 else 0), freeze_values.point(lambda v: 255 if v >= 128 else 0).point(lambda v: 255-v)).getbbox():
                    raise ValueError("edit/freeze masks are not exact complements")
            final_raster = request_dir / f"final_{stage}_attempt_{int(request.get('attempt_round', 0)):02d}.png"
            compose_masked_edit(parent_path, generated, edit_mask, final_raster)
            frozen_audit = validate_frozen_pixels(parent_path, final_raster, edit_mask)
            if not frozen_audit.get("passed", False):
                raise ValueError(f"unauthorized pixel drift after composition: {frozen_audit}")
            delta_audit = authorized_pixel_delta(parent_path, final_raster, edit_mask)
            if not delta_audit.get("passed", False):
                raise ValueError(f"generated child contains no authorized pixel change: {delta_audit}")
        evidence = self._review(request, stage, final_raster, request_dir)
        # The caller's command_provider accepts {"image": path, "evidence": object}.
        return_json_path = request_dir / "candidate_response.json"
        return_json_path.write_text(json.dumps({
            "candidates": [{"image": str(generated.resolve()), "evidence": evidence}]
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return [{"image": str(generated.resolve()), "evidence": evidence}]


def _bounded_score(value: Any) -> float:
    try:
        score = float(value)
    except (TypeError, ValueError):
        return 0.0
    if not math.isfinite(score):
        return 0.0
    return max(0.0, min(1.0, score))


def run_request(request_path: str | Path) -> dict[str, Any]:
    path = Path(request_path).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"request JSON not found: {path}")
    request = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(request, dict):
        raise ValueError("request JSON must be an object")
    provider = GeminiPlantedBubbleProvider()
    results = provider(request, path.parent)
    return {"candidates": list(results), "provider": "GeminiPlantedBubbleProvider", "visual_acceptance_status": "NOT_VERIFIED_BY_CODE"}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request_json", type=Path, help="request.json emitted by planted_bubble_closed_loop.py")
    args = parser.parse_args(argv)
    try:
        result = run_request(args.request_json)
    except (OSError, ValueError, RuntimeError, urllib.error.URLError) as exc:
        print(f"GEMINI_PROVIDER_BLOCKED: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
