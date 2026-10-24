#!/usr/bin/env python3
"""Create a SHA-gated, single-master H2 PRE/MID/POST frame triad.

Only a human-reviewed H2 MID image may unlock its PRE and POST derivatives. The derivatives
are instructed to use the MID raster as the same camera/hammer/world reference and alter only
the time/contact state. This planner never calls an image model or claims a frame was generated.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

REQUIRED_H2_CHECKS = (
    "one_rigid_T_hammer",
    "nominated_terminal_end_face_is_first_contact",
    "zero_gap_at_P",
    "no_interpenetration",
    "crossbar_and_handle_topology_correct",
    "camera_crop_perspective_locked",
    "hammer_shape_and_scale_locked",
    "scene_lighting_background_locked",
)
STABLE_TEXT_FIELDS = (
    "story", "loop_id", "try_id", "method_id", "method_label",
    "geometry_family", "contact_method", "camera_id", "pose_id",
    "style_id", "series_id", "world_label",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_text_payload(label: dict[str, Any], act_id: str = "3") -> dict[str, str]:
    act = (label.get("acts") or {}).get(str(act_id), {})
    return {
        "title": "邊界行人 / THE BOUNDARY WALKER",
        "loop_try": f"LOOP {label.get('loop_id', '')} / TRY {label.get('try_id', '')}",
        "method": str(label.get("method_label") or label.get("method_id") or ""),
        "geometry_contact": f"{label.get('geometry_family', '')} / {label.get('contact_method', '')}",
        "camera_pose": f"{label.get('camera_id', '')} / {label.get('pose_id', '')}",
        "style_series_world": " / ".join(
            str(label.get(key) or "") for key in ("style_id", "series_id", "world_label")
        ),
        "prompt_id": str(act.get("prompt_id") or label.get("prompt_id") or ""),
    }


def label_text_sha256(label: dict[str, Any], act_id: str = "3") -> str:
    payload = canonical_text_payload(label, act_id)
    return hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _resolve_package(raw: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    axes = raw.get("axes") or {}
    label = raw.get("art_label_spec") or raw
    # Some callers provide art_label_spec alone. Do not fabricate missing geometry state.
    geometry = axes.get("geo_family", label.get("geometry_family"))
    contact = axes.get("contact", label.get("contact_method"))
    if geometry != "T" or contact != "H2":
        raise ValueError(
            f"This strict first implementation is for T-hammer H2 master frames only; got {geometry}/{contact}. "
            "Other topologies need their own state-transition contract."
        )
    if not label.get("loop_id") or not label.get("try_id") or not label.get("method_id"):
        raise ValueError("package must include loop_id, try_id and method_id/art_label_spec")
    return axes, label


def validate_mid_review(mid_image: Path | None, receipt: dict[str, Any] | None) -> tuple[bool, list[str], str | None]:
    reasons: list[str] = []
    if mid_image is None:
        return False, ["H2 mid-frame image file not supplied"], None
    if not mid_image.is_file():
        return False, [f"H2 mid-frame image not found: {mid_image}"], None
    image_sha = sha256_file(mid_image)
    if receipt is None:
        return False, ["SHA-bound human geometry review receipt not supplied"], image_sha
    if receipt.get("review_status") != "HUMAN_ACCEPTED":
        reasons.append("review_status must be HUMAN_ACCEPTED")
    if receipt.get("image_sha256") != image_sha:
        reasons.append("receipt image_sha256 does not match the exact mid-frame file")
    checks = receipt.get("geometry_checks") or {}
    for field in REQUIRED_H2_CHECKS:
        if checks.get(field) is not True:
            reasons.append(f"geometry_checks.{field} must be true")
    return not reasons, reasons, image_sha


def build_triad(raw_package: dict[str, Any], mid_image: Path | None = None,
                review_receipt: dict[str, Any] | None = None) -> dict[str, Any]:
    axes, label = _resolve_package(raw_package)
    accepted, blocked_reasons, mid_sha = validate_mid_review(mid_image, review_receipt)
    text_payload = canonical_text_payload(label, "3")
    text_hash = label_text_sha256(label, "3")
    camera_lock = {
        "camera_id": axes.get("camera") or label.get("camera_id") or "UNSPECIFIED_CAMERA",
        "camera_pack": axes.get("camera_pack") or "UNSPECIFIED_CAMERA_PACK",
        "canvas": "16:9",
        "crop": "pixel-identical framing to the accepted H2 master",
        "lens_perspective": "locked",
        "camera_position_and_orientation": "locked",
        "background_registration": "locked",
        "lighting_direction": "locked",
    }
    hammer_lock = {
        "topology": "Exactly one rigid T-hammer: one straight rectangular crossbar and one straight handle joined at the crossbar midpoint at 90 degrees.",
        "dimensions_and_proportions": "identical to the accepted H2 master raster; no redesign, rescale, bend, extra head, extra handle or topology substitution",
        "active_face": "the nominated flat terminal end face of the crossbar",
        "handle_attachment": "crossbar midpoint, 90-degree attachment; fixed across all three frames",
        "rigid_body": "hammer remains one rigid body; no internal bending or changing silhouette",
    }
    shared_frame_lock = {
        "camera_lock": camera_lock,
        "hammer_lock": hammer_lock,
        "character_pose": "same character, same grip and same body silhouette; only the minimum physically required hand/arm follow-through along the declared path",
        "world_and_props": "pixel-registered; no new props, no environment redesign",
        "text_payload": text_payload,
        "text_content_sha256": text_hash,
        "video_text_rule": "the canonical word content and IDs are identical across PRE/MID/POST and throughout the video; only still-frame typography treatment may change",
    }

    mid_prompt = (
        "H2 MID MASTER — CORRECT THIS FRAME FIRST. Use the supplied candidate H2 raster as an image-edit source, "
        "not as a loose inspiration and not as a fresh scene-generation request. Preserve the current camera, crop, "
        "perspective, scene, character identity, grip, lighting, color grade, sphere and all background landmarks. "
        "Correct only the local T-hammer geometry/contact defect: exactly one rigid T-hammer, a straight rectangular "
        "crossbar with one straight handle attached at the crossbar midpoint at 90 degrees; preserve the candidate's "
        "hammer proportions and material. The nominated flat terminal end face is the only first contact at P. "
        "The active face and sphere have zero gap at P, opposing normals, and no interpenetration. First fine cracks "
        "originate only at P. Do not let the side cheek, shaft, handle, corner or another surface touch first. "
        "Do not add/remove a handle, rotate the camera, change focal length, reframe, move the sphere, redesign the "
        "character, or change world details. If correcting the contact requires changing the camera or hammer shape, "
        "stop and flag for a human correction rather than inventing an alternative. This image becomes the sole master "
        "for both derived temporal frames. Do not add typography in the generated raster; typography is overlaid later."
    )
    pre_prompt = (
        "PRE FRAME — DERIVE FROM THE ACCEPTED H2 MID MASTER ONLY. Use the exact accepted H2 mid-frame raster as the "
        "mandatory image-to-image parent/reference. Do not generate independently from text. Preserve pixel-registered "
        "camera position/orientation, 16:9 crop, perspective, sphere position/shape, character identity, costume, "
        "background landmarks, lighting direction, world, material and the T-hammer's exact silhouette, dimensions, "
        "crossbar/handle proportions, 90-degree midpoint handle attachment and hand grip. The only temporal change is "
        "rewinding the same rigid hammer/connected grip slightly backward along its already-established approach axis "
        "to H1 PRE_NEAR: leave a clear positive air gap between the same nominated terminal face and point P; no contact, "
        "cracks, sparks, glow, shadow-contact or interpenetration. Keep face normals and perspective consistent with the "
        "mid master. No camera move, zoom, re-angle, new pose, weapon redesign, background redraw or independent "
        "composition. Preserve the same exact text payload; apply still typography treatment BEFORE (cold glass/ice "
        "edge, restrained cyan refraction and thin engraved bevel). Typography styling may differ, but every word, "
        "LOOP/TRY ID, method name and prompt ID must remain byte-for-byte identical to the canonical payload. "
        "Do not generate text in the raster; composite it afterward."
    )
    post_prompt = (
        "POST FRAME — DERIVE FROM THE SAME ACCEPTED H2 MID MASTER ONLY. Use the exact same accepted H2 mid-frame raster "
        "as mandatory image-to-image parent/reference. Do not generate independently from text or use the PRE frame as "
        "a new composition source. Preserve pixel-registered camera, 16:9 crop, perspective, sphere, character identity, "
        "costume, background landmarks, lighting, world, materials and the T-hammer's exact silhouette, dimensions, "
        "crossbar/handle proportions, 90-degree midpoint handle attachment and grip. The only temporal change is the "
        "small same-axis H3 follow-through after contact at P: the same rigid hammer advances a small distance along "
        "the established collision axis; cracks propagate outward from the original P. No second impact point, no "
        "side-first contact, no handle-through-sphere, no topology change, no extra rotation or invented camera motion. "
        "Keep the same text payload, words, LOOP/TRY ID, method name and prompt ID; apply still typography treatment "
        "AFTER (warm molten-metal/amber foil, deeper embossed 3D extrusion and ember highlight). It must visibly differ "
        "in material/style from PRE while the text content SHA remains the same. Do not generate text in the raster; "
        "composite it afterward."
    )
    ready = accepted and mid_sha is not None
    frames = [
        {
            "frame_id": "MID_H2",
            "time_role": "CONTACT",
            "generation_order": 1,
            "source": "candidate H2 image-edit source",
            "typography_variant": "middle",
            "prompt": mid_prompt,
            "status": "HUMAN_ACCEPTED" if accepted else "MID_CORRECTION_REQUIRED",
            "image_sha256": mid_sha,
        },
        {
            "frame_id": "PRE_H1",
            "time_role": "PRE_NEAR",
            "generation_order": 2,
            "parent_frame_id": "MID_H2",
            "parent_sha256": mid_sha if ready else None,
            "typography_variant": "before",
            "prompt": pre_prompt,
            "status": "PROMPT_READY" if ready else "BLOCKED_UNTIL_MID_H2_ACCEPTED",
        },
        {
            "frame_id": "POST_H3",
            "time_role": "FOLLOW_THROUGH",
            "generation_order": 3,
            "parent_frame_id": "MID_H2",
            "parent_sha256": mid_sha if ready else None,
            "typography_variant": "after",
            "prompt": post_prompt,
            "status": "PROMPT_READY" if ready else "BLOCKED_UNTIL_MID_H2_ACCEPTED",
        },
    ]
    triad_key = {
        "loop_id": label["loop_id"],
        "try_id": label["try_id"],
        "method_id": label["method_id"],
        "contact": "T/H2 master; H1 pre; H3 post",
        "camera_lock": camera_lock,
        "hammer_lock": hammer_lock,
        "text_content_sha256": text_hash,
        "mid_sha256": mid_sha,
    }
    return {
        "schema_version": "BW-FRAME-TRIAD-1.0",
        "triad_id": "TRIAD-" + hashlib.sha256(
            json.dumps(triad_key, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()[:16].upper(),
        "loop_id": label["loop_id"],
        "try_id": label["try_id"],
        "method_id": label["method_id"],
        "transition": ["PRE_H1", "MID_H2", "POST_H3"],
        "generation_order": ["MID_H2_CORRECT_AND_REVIEW", "PRE_H1_FROM_ACCEPTED_MID", "POST_H3_FROM_ACCEPTED_MID"],
        "only_temporal_state_may_change": True,
        "mid_master_sha256": mid_sha,
        "mid_geometry_review_accepted": accepted,
        "blocked_reasons": blocked_reasons,
        "shared_frame_lock": shared_frame_lock,
        "frame_typography": {
            "text_content_sha256": text_hash,
            "pre_frame_variant": "before",
            "mid_frame_variant": "middle",
            "post_frame_variant": "after",
            "video_variant": "video-lock",
            "same_words_across_all_frames_and_video": True,
            "pre_and_post_visual_treatment_differs": True,
            "text_is_rendered_by_svg_ass_not_image_model": True,
        },
        "frames": frames,
        "status": "TRIAD_READY_AFTER_MID_REVIEW" if ready else "HOLD_MID_CORRECTION_AND_REVIEW",
        "external_generation_called": False,
        "image_realization": "NOT_RUN",
        "continuity_audit_status": "NOT_RUN",
        "visual_acceptance_status": "NOT_VERIFIED",
        "rule": (
            "Do not generate PRE/POST until the corrected H2 master raster has an exact SHA-bound HUMAN_ACCEPTED "
            "receipt with every required geometry check true. Both frames derive from that same raster."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", required=True, help="JSON product package containing axes and art_label_spec")
    parser.add_argument("--mid-image", default="", help="candidate/corrected H2 master raster file")
    parser.add_argument("--review-receipt", default="", help="SHA-bound human review JSON; unlocks PRE/POST")
    parser.add_argument("--outdir", required=True)
    args = parser.parse_args()
    package_path = Path(args.package)
    package = json.loads(package_path.read_text(encoding="utf-8"))
    mid_path = Path(args.mid_image) if args.mid_image else None
    receipt_path = Path(args.review_receipt) if args.review_receipt else None
    receipt = json.loads(receipt_path.read_text(encoding="utf-8")) if receipt_path and receipt_path.is_file() else None
    result = build_triad(package, mid_path, receipt)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "frame_triad.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for frame in result["frames"]:
        (outdir / f"{frame['frame_id'].lower()}_prompt.txt").write_text(frame["prompt"] + "\n", encoding="utf-8")
    summary = {
        "triad_id": result["triad_id"],
        "status": result["status"],
        "mid_master_sha256": result["mid_master_sha256"],
        "mid_geometry_review_accepted": result["mid_geometry_review_accepted"],
        "pre_status": result["frames"][1]["status"],
        "post_status": result["frames"][2]["status"],
        "text_content_sha256": result["frame_typography"]["text_content_sha256"],
        "external_generation_called": False,
        "continuity_audit_status": "NOT_RUN",
        "visual_acceptance_status": "NOT_VERIFIED",
    }
    (outdir / "frame_triad_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
