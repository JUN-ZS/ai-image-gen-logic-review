#!/usr/bin/env python3
"""Compile every legal Boundary Walker variant ID into a six-act looping story prompt pack.

This is a prompt compiler only: it does not call image/video models and cannot mark geometry
or continuity accepted. One catalog variant becomes one LOOP episode, and the variant's
declared act is the primary TRY. Five companion act prompts preserve the six-act story spine.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any, Iterable

REQUIRED_COLUMNS = {
    "id", "lane", "media", "act", "geo_family", "geo_catalog", "contact",
    "cam", "wash", "style", "shot", "video_method", "count_bucket",
}
ACTS = {
    "1": ("畫界", "The heroine walks along a luminous boundary line and notices that its reflection does not match the world behind her."),
    "2": ("保護", "The heroine holds an open hand beside the translucent boundary sphere; the miniature sanctuary and its residents remain safe and visible."),
    "3": ("試法／碎裂", "The boundary reveals the consequence of this loop's primary attempt. Only the designated primary TRY may show a physical contact event; a companion frame shows a symbolic trace, not a new impact."),
    "4": ("假修", "A beautiful golden repair bandage covers the fracture, but a faint seam and a wrong reflection reveal that this repair is superficial."),
    "5": ("一界", "Reflections from the outer ruined city and inner sanctuary align; the boundary is still visible, while the residents remain safe."),
    "6": ("選擇", "The heroine chooses to return to the boundary. Her final footstep forms an incomplete luminous ring that can match-cut to the next loop's opening step."),
}
STYLE_NAMES = {
    "S01": "photoreal cinematic live action, rainy neo-Tokyo or motivated urban night light, restrained bloom and believable materials",
    "S02": "cute pastel INS editorial art, soft candy colors and refined social-magazine composition",
    "S03": "surrealist cinematic art, symbolic impossible space but clear central silhouette",
    "S04": "high-contrast Japanese winter cinema, vermilion torii colonnade in powder snow, cold moonlight and warm paper lanterns",
    "S05": "cursive ink wuxia cinema, splash-ink bamboo abyss, cinnabar seal accents, wind-swept martial robes",
    "S06": "Caravaggio lava cathedral tenebrism, magma veins, single golden shaft of light, gilded bronze and basalt materials",
}
VIDEO_METHOD_SPECS = {
    "V-01": "10-second single-scene continuous impact short; one unbroken camera; contact physics continuous; no hard cuts.",
    "V-02": "Five complete keyframes KF1..KF5 with MID/H2 as sole master (KF3). KF1-KF2 are pre-states; KF4-KF5 are post-states derived only from KF3. Do not invent separate weapons/worlds per KF.",
    "V-03": "Planted-cylinder fixed-anchor clip; contact seat never drifts; no flying swing.",
    "V-04": "Image-to-video from accepted mother still; motion only; lock geometry identity and world.",
    "V-05": "Dual T-hammer FACE collision temporal clip; two independent T hammers; end-faces meet; never fuse into H.",
    "V-06": "Thick CROSS rounded end-cap collision temporal clip.",
    "V-07": "Linear rod POS/NEG control temporal clip; 90-degree center-line rules hold.",
    "V-08": "Multi-facet head selected-face temporal clip.",
    "V-09": "Six-act narrative MV segment montage; story spine only unless a bound topology is named; no unbound precise geometry proof.",
    "V-10": "Extended continuity pack; preserve match-cut footstep ring between acts.",
}
WASH_NAMES = {
    "W00": "neutral baseline framing; keep the whole declared event clearly visible",
    "W01": "two-tone gold/cyan face-edge light that outlines the active faces without hiding the seam",
    "W02": "high vertical leap or overhead strike composition; preserve the declared approach axis",
    "W03": "45-degree diagonal upswing; move the rigid object as a single body",
    "W04": "ground-skimming low lateral sweep with readable body balance and the active surface visible",
    "W05": "single frozen instant after a wind-up; do not create a ghosted duplicate of the object",
    "W06": "retro arena material language; preserve the selected planar contact surface",
    "W07": "over-the-shoulder contact view that keeps hands, joints, active face and boundary seam visible",
    "W08": "low-angle lava-abyss environmental lighting while preserving all geometry",
    "W09": "side backlight to reveal object thickness without hiding the contact seam in silhouette",
    "W10": "ultra-wide broken-bridge environment while keeping heroine, object and boundary inspectable",
}
GEO_DESCRIPTIONS = {
    "T": "Exactly one rigid T-hammer: a straight rectangular crossbar and one straight handle attached at the midpoint at a right angle.",
    "T2": "Exactly two separate rigid T-hammers, each with its own straight crossbar and midpoint handle joint. They never fuse into one H-shaped object.",
    "CROSS": "Exactly two separate thick plus-sign cross hammers. Each has four orthogonal arms, cylindrical terminal barrels and nominated flat circular outer end caps.",
    "ROD": "Two thin rigid line-striker rods with small planar impact facets. Do not render hammers.",
    "MULTI": "Exactly one multi-facet rounded hammer head with one handle and several broad flat faces; choose only the nominated face.",
    "PLANT_O": "One double-ended cylinder planted against the sphere, with its handle attached at the cylinder's outer terminal end along the declared axis. It is anchored, not a flying hammer.",
    "PLANT_S": "One double-ended cylinder planted against the sphere with a conformal base seat and one handle attached at the cylinder's side-middle tangent. It is anchored, not a flying hammer.",
    "T_OR_MULTI": "The V-09 narrative-MV catalog row does not specify one precise contact topology. Treat this as a story-level montage only; do not show a precise weapon contact or claim geometric proof until a separate T or MULTI sub-try is selected.",
    "NONE": "No weapon impact. Use a soft narrative image with hands, footsteps, reflections, thread, flower, gate, glass or dance as appropriate.",
}
CONTACT_RULES = {
    "H0": "PRE_FAR: the nominated active face is aligned toward the boundary but a wide positive air gap remains. The sphere is pristine; no cracks, glow, sparks or impact shadow.",
    "H1": "PRE_NEAR: move the whole declared rigid object closer, but retain a visible positive air gap. No contact glow or cracks yet.",
    "H2": "FIRST CONTACT: only the nominated terminal striking face touches the sphere at point P, with opposing normals, zero gap and no interpenetration. The first fine cracks originate at P only.",
    "H3": "FOLLOW-THROUGH: continue the same rigid object a small distance along the established axis after contact at P. Cracks propagate outward from P; do not reset the pose or invent a new impact point.",
    "FACE": "FACE-TO-FACE CONTACT: the two nominated planar terminal faces meet at one shared contact region with opposing normals. All sidewalls, corners, joints and handles remain clear.",
    "POS": "POSITIVE CONTROL: the rod centre-lines cross at 90 degrees and the nominated planar facets face each other with opposing normals at the shared contact point.",
    "NEG": "NEGATIVE CONTROL: deliberately turn one nominated planar facet away so the required face-to-face contact is absent. Clearly treat this as an expected failure, never as acceptance.",
    "TEACH": "TEACHING OUTPUT only. Separate the clean source artwork from the label/teaching board; this row is not geometric proof.",
    "NA": "No hard-contact state applies in this soft narrative frame.",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def clean(value: Any) -> str:
    return str(value if value is not None else "").strip()


def short_camera(camera: str) -> str:
    if not camera or camera == "NA":
        return "CAM-NA"
    parts = camera.split("__")
    axis = parts[0]
    cam_id = next((p.split("_")[0] for p in parts[1:] if p.startswith("CAM")), "")
    wind = next((p for p in parts[1:] if p in {"M1", "M2"}), "")
    return "/".join(p for p in (axis, cam_id, wind) if p)


def style_description(style: str) -> str:
    return STYLE_NAMES.get(style, f"catalog style {style}; preserve the approved style recipe without changing the physical contract")


def wash_description(wash: str) -> str:
    return WASH_NAMES.get(wash, f"catalog framing wash {wash}; apply only that named framing method")


def method_label(row: dict[str, str]) -> str:
    media = clean(row.get("media")).upper()
    geo = clean(row.get("geo_family")) or "NONE"
    contact = clean(row.get("contact")) or "NA"
    style = clean(row.get("style")) or "S01"
    cam = short_camera(clean(row.get("cam")))
    wash = clean(row.get("wash")) or "W00"
    shot = clean(row.get("shot")) or "UNSPECIFIED"
    video = clean(row.get("video_method"))
    if media == "VIDEO":
        parts = ["VIDEO", video or "METHOD-UNSPECIFIED"]
        if geo != "NONE":
            parts.append("GEO." + geo)
        if contact not in {"", "NA"}:
            parts.append(contact)
        parts.append(style)
        return " · ".join(parts)
    if geo != "NONE":
        return " · ".join(["GEO." + geo, contact, cam, wash, style])
    return " · ".join(["SHOT." + shot, cam, wash, style])


def method_description(row: dict[str, str]) -> str:
    geo = clean(row.get("geo_family")) or "NONE"
    contact = clean(row.get("contact")) or "NA"
    description = GEO_DESCRIPTIONS.get(geo, f"Use the exact object topology registered as {geo}; do not add another topology.")
    contact_rule = CONTACT_RULES.get(contact, "Use a soft narrative state; no physical contact is implied.")
    if geo in {"PLANT_O", "PLANT_S"}:
        contact_rule = (
            "ANCHOR CONTACT: the cylinder's nominated seat is already conformally planted against the sphere at P. "
            "This is a fixed anchor, not a flying impact; do not show a swing, a gap-closing hit or a newly invented "
            "terminal-face strike. Preserve the exact handle attachment location for this family."
        )
    elif geo == "MULTI":
        contact_rule = (
            "SELECTED FLAT-FACE CONTACT: only the nominated broad planar facet of the one multi-facet head meets "
            "the boundary at P. The handle, head edge, rounded cheek and other facets remain clear; do not turn the "
            "head into a T-hammer or a plus-sign cross."
        )
    if geo == "ROD":
        if contact == "NEG":
            contact_rule += " The image/video must be filed as NEGATIVE_CONTROL."
        elif contact == "POS":
            contact_rule += " This is a candidate positive control, not proof of success until the actual raster is reviewed."
    if geo == "T_OR_MULTI":
        return description
    return description + " " + contact_rule


def act_story_text(act: str) -> tuple[str, str]:
    if act not in ACTS:
        raise ValueError(f"Act must be one of 1..6; got {act!r}")
    return ACTS[act]


def _base_prompt(row: dict[str, str], loop_id: str, try_id: str, act: str,
                 is_primary: bool, source_sha: str) -> str:
    act_title, event = act_story_text(act)
    style = clean(row.get("style")) or "S01"
    style_text = style_description(style)
    primary_label = method_label(row)
    shot = clean(row.get("shot")) or "UNSPECIFIED"
    cam = short_camera(clean(row.get("cam")))
    wash = clean(row.get("wash")) or "W00"
    geo = clean(row.get("geo_family")) or "NONE"
    contact = clean(row.get("contact")) or "NA"
    lane = clean(row.get("lane")) or "SOFT"
    row_media = clean(row.get("media")).upper()
    catalog_methods = clean(row.get("geo_catalog")) or clean(row.get("video_method")) or "story spine"
    header = (
        f"STORY: THE BOUNDARY WALKER. LOOP {loop_id}. TRY {try_id}. ACT {act}: {act_title}. "
        f"PRIMARY TRY METHOD FOR THIS LOOP: {primary_label}. SOURCE VARIANT ID: {clean(row.get('id'))}. "
        f"CATALOG METHOD REFERENCES: {catalog_methods}. SOURCE CATALOG SHA-256: {source_sha}."
    )
    identity_world = (
        "Identity lock: THE BOUNDARY WALKER / 邊界行人. Keep the same adult East Asian female Boundary Walker from the "
        "approved face reference: long dark-brown hair, unchanged face, body proportions and series costume. "
        "World lock: outer series world (style package) plus a translucent BOUNDARY SPHERE that contains a LIVING "
        "miniature sanctuary with warm interior lights (never an empty glass planet). A luminous boundary line or ring "
        "must remain readable. Preserve the moral question: is the boundary protecting life, or separating the two sides? "
        "Heroine, landmarks, light direction and circular boundary motif stay continuous with previous and next acts. "
    )
    editorial = (
        f"Visual style: {style_text}. Framing method: {wash_description(wash)}. "
        f"Camera variant: {cam}. Shot variant: {shot}. The episode's method label is {primary_label}. "
        "Do not bake text, letters, numbers, subtitles, logos, UI or watermarks into the generated media; "
        "v5 diegetic typography (variable glyph scale, zero plate, optional lightning/fire/graffiti/ice VFX, L-SHA12) "
        "is composited afterward by boundary_pedestrian_try_art --layout diegetic from the same loop manifest. "
        "Keep corner negative-space available for that layer without covering the heroine's face, active contact "
        "surface, handles, boundary or fracture origin. One full-frame image, never a collage or contact sheet. "
    )
    if not is_primary:
        companion = (
            f"This is a COMPANION STORY-SPINE FRAME, not the primary method demonstration. "
            f"The primary method for the episode is {primary_label}, but do not place that tool/contact into this act "
            "unless this act is the selected target. Follow the act event only, with no new weapon impact. "
        )
        if act == "3":
            companion += (
                "Show a symbolic memory of prior fractures reflected on the boundary, with no active weapon touching "
                "the sphere and no claim that a contact geometry has been validated. Keep the sanctuary unharmed. "
            )
        return header + " " + identity_world + event + " " + editorial + companion

    if row_media == "VIDEO":
        video_method = clean(row.get("video_method")) or "UNSPECIFIED"
        video_spec = VIDEO_METHOD_SPECS.get(video_method, f"Catalog video method {video_method}; follow declared pipeline only.")
        video_intro = (
            f"Create one standalone 5–8 second cinematic clip, not an unbroken six-act movie. "
            f"The target media for this primary TRY is VIDEO using method {video_method}. "
            f"Pipeline contract: {video_spec} "
            f"Do not change the method or silently substitute a different video workflow. "
        )
        if geo == "T_OR_MULTI":
            action = (
                "This V-09 clip is a narrative montage for the chosen story act, not an exact geometry test. "
                "Use symbolic, story-driven fracture imagery only; do not depict a precise weapon/sphere contact. "
                "The contact topology is intentionally unbound in this catalog row."
            )
        elif lane == "HARD":
            action = f"Selected physical method: {method_description(row)}"
        else:
            action = "Keep this as a soft narrative clip with no weapon impact. " + event
        timeline = (
            "Maintain continuous character identity, world landmarks, light direction and boundary shape. "
            "Animate only the event for this act. Preserve causal ordering; no teleporting objects, unexplained cuts, "
            "extra limbs, invented handles, random cracks or changes to sanctuary residents. End on an image that can "
            "match-cut into the next act. The loop/method text is an editorial overlay, not generative text."
        )
        return header + " " + identity_world + video_intro + action + " " + editorial + timeline

    image_intro = "Create one single full-frame cinematic 16:9 image for this act of the looping story. "
    if lane == "HARD" and act == "3":
        action = f"Primary physical trial in the fracture act. Selected method: {method_description(row)}"
        if geo == "T_OR_MULTI":
            action = "Story-level ACT 3 montage only: do not depict precise geometry contact until a T or MULTI sub-try is selected."
    else:
        action = event
        if lane == "HARD":
            action += " Keep the nominated tool and contact contract as the only object method; never add a second topology."
        else:
            action += " This is a soft narrative act with no weapon contact."
    continuity = (
        "Keep the full story readable through this one frame. The title/method typography is added afterward by the "
        "deterministic SVG renderer, so the generated image itself must contain no readable text or false labels. "
        "Use a motivated cinematic composition, meaningful negative space, a recurring circular line and restrained "
        "effects. Do not hide the focal event behind bloom or debris. Render the requested state only; actual geometry "
        "and pixel acceptance are decided by inspection of the saved raster, not by the prompt text."
    )
    return header + " " + identity_world + image_intro + action + " " + editorial + continuity


def build_episode(row: dict[str, str], index: int, source_sha: str) -> dict[str, Any]:
    act = clean(row.get("act"))
    if act not in ACTS:
        raise ValueError(f"Variant {row.get('id')} has invalid act {act!r}")
    variant_id = clean(row.get("id"))
    if not variant_id:
        raise ValueError("Variant ID may not be empty")
    loop_id = f"LOOP-{index:04d}"
    try_id = f"TRY-{index:04d}"
    primary_label = method_label(row)
    acts = []
    for act_id in ACTS:
        is_primary = act_id == act
        target_media = clean(row.get("media")).upper() if is_primary else "IMAGE"
        # Only the target act receives the specific variant's tool/camera/contact behavior.
        prompt = _base_prompt(row, loop_id, try_id, act_id, is_primary, source_sha)
        acts.append({
            "act_id": act_id,
            "act_title": ACTS[act_id][0],
            "media": target_media,
            "is_primary_try": is_primary,
            "variant_id": variant_id if is_primary else None,
            "prompt_id": (
                clean(row.get("geo_catalog")) or clean(row.get("video_method")) or "STORY_SPINE"
            ) if is_primary else f"STORY_SPINE_ACT{act_id}",
            "prompt": prompt,
        })
    method_fp = hashlib.sha256(
        json.dumps({k: clean(row.get(k)) for k in sorted(REQUIRED_COLUMNS)}, sort_keys=True).encode("utf-8")
    ).hexdigest()
    l_sha = method_fp[:12]
    art_label_spec = {
        "story": "THE BOUNDARY WALKER",
        "loop_id": loop_id,
        "try_id": try_id,
        "series_id": clean(row.get("style")) or "S01",
        "world_label": style_description(clean(row.get("style")) or "S01")[:80],
        "method_id": f"GEO.{clean(row.get('geo_family')) or 'NONE'}",
        "method_label": primary_label,
        "geometry_family": clean(row.get("geo_family")) or "NONE",
        "contact_method": clean(row.get("contact")) or "NA",
        "camera_id": short_camera(clean(row.get("cam"))),
        "pose_id": clean(row.get("shot")) or "UNSPECIFIED",
        "style_id": clean(row.get("style")) or "S01",
        "prompt_id": clean(row.get("geo_catalog")) or clean(row.get("video_method")) or "STORY_SPINE",
        "layout": "diegetic",
        "vfx_mode": "lightning" if clean(row.get("lane")) == "HARD" else "ice",
        "l_sha12": f"L-{l_sha}",
        "status": "PROMPT_READY",
        "acts": {a["act_id"]: {"act_id": a["act_id"], "prompt_id": a["prompt_id"]} for a in acts},
    }
    # PRE/MID/POST phase prompts only for HARD primary ACT3 geometry (v5 triad contract notes)
    phases = None
    if clean(row.get("lane")) == "HARD" and act == "3" and clean(row.get("geo_family")) not in {"NONE", "T_OR_MULTI", ""}:
        mid_body = _base_prompt(row, loop_id, try_id, "3", True, source_sha)
        phases = {
            "MID_H2": {
                "generation_order": 1,
                "role": "CONTACT_MASTER",
                "prompt": (
                    "PHASE MID (t0 master). " + mid_body +
                    " This raster becomes the sole parent for PRE and POST. "
                    "Typography: clean master plate (no generative text); L-" + l_sha + "."
                ),
            },
            "PRE_H1": {
                "generation_order": 2,
                "role": "PRE_NEAR",
                "status_if_unlocked": "BLOCKED_UNTIL_MID_H2_ACCEPTED",
                "prompt": (
                    "PHASE PRE. Derive ONLY from accepted MID master. Same camera, crop, hammer topology, world, heroine. "
                    "Only rewind along approach axis to leave a clear positive air gap; no contact, cracks, sparks. "
                    "Same text payload will be overlaid with ice/glass diegetic treatment (before). L-" + l_sha + "."
                ),
            },
            "POST_H3": {
                "generation_order": 3,
                "role": "FOLLOW_THROUGH",
                "status_if_unlocked": "BLOCKED_UNTIL_MID_H2_ACCEPTED",
                "prompt": (
                    "PHASE POST. Derive ONLY from the same accepted MID master. Same camera and hammer. "
                    "Small same-axis follow-through; cracks propagate from original P only. "
                    "Same text payload overlaid with molten/fire diegetic treatment (after). L-" + l_sha + "."
                ),
            },
        }
    return {
        "story": "THE BOUNDARY WALKER",
        "loop_id": loop_id,
        "try_id": try_id,
        "sweep_id": "SWEEP-001",
        "variant_id": variant_id,
        "primary_act": act,
        "primary_media": clean(row.get("media")).upper(),
        "lane": clean(row.get("lane")),
        "method_label": primary_label,
        "method_fingerprint": method_fp,
        "l_sha12": f"L-{l_sha}",
        "art_label_spec": art_label_spec,
        "frame_phases": phases,
        "catalog_row": {k: clean(v) for k, v in row.items()},
        "acts": acts,
        "status": "PROMPT_READY",
        "formula_edition": "MASTER_PROMPT_v5_20261025",
        "image_realization": "NOT_RUN",
        "video_realization": "NOT_RUN",
        "pixel_audit_status": "NOT_RUN",
        "continuity_audit_status": "NOT_RUN",
        "visual_acceptance_status": "NOT_VERIFIED",
        "source_catalog_sha256": source_sha,
        "external_generation_called": False,
    }


def load_rows(csv_path: Path) -> tuple[list[dict[str, str]], str]:
    raw = csv_path.read_bytes()
    digest = sha256_bytes(raw)
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("Variant CSV is empty")
        missing = REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing:
            raise ValueError("Variant CSV is missing required columns: " + ", ".join(sorted(missing)))
        rows = list(reader)
    ids = [clean(r.get("id")) for r in rows]
    if any(not item for item in ids):
        raise ValueError("Variant CSV contains an empty ID")
    duplicates = [key for key, value in Counter(ids).items() if value > 1]
    if duplicates:
        raise ValueError("Duplicate variant IDs: " + ", ".join(duplicates[:5]))
    for row in rows:
        media = clean(row.get("media")).upper()
        lane = clean(row.get("lane")).upper()
        act = clean(row.get("act"))
        if media not in {"IMAGE", "VIDEO"}:
            raise ValueError(f"Variant {row['id']} has invalid media {media!r}")
        if lane not in {"SOFT", "HARD"}:
            raise ValueError(f"Variant {row['id']} has invalid lane {lane!r}")
        if act not in ACTS:
            raise ValueError(f"Variant {row['id']} has invalid act {act!r}")
        if lane == "HARD" and act != "3":
            raise ValueError(f"Hard contact variant {row['id']} must be in ACT 3")
    return rows, digest


def interleave_buckets(rows: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    """Round-robin legal method buckets so the opening tries visibly change approach."""
    buckets: dict[str, deque[dict[str, str]]] = defaultdict(deque)
    for row in rows:
        buckets[clean(row.get("count_bucket")) or "UNBUCKETED"].append(row)
    bucket_order = list(buckets)
    output: list[dict[str, str]] = []
    while any(buckets[key] for key in bucket_order):
        for key in bucket_order:
            if buckets[key]:
                output.append(buckets[key].popleft())
    return output


def compile_csv(
    csv_path: Path,
    outdir: Path,
    start_index: int = 0,
    limit: int = 0,
    buckets: list[str] | None = None,
) -> dict[str, Any]:
    rows, source_sha = load_rows(csv_path)
    if buckets:
        wanted = {b.strip() for b in buckets if b.strip()}
        rows = [r for r in rows if clean(r.get("count_bucket")) in wanted]
        if not rows:
            raise ValueError("No rows match buckets: " + ", ".join(sorted(wanted)))
    ordered = interleave_buckets(rows)
    if start_index < 0 or start_index >= max(1, len(ordered)):
        raise ValueError("start_index must be within the catalog index range")
    selected = ordered[start_index:] if limit <= 0 else ordered[start_index:start_index + limit]
    if not selected:
        raise ValueError("No variant rows selected")
    outdir.mkdir(parents=True, exist_ok=True)
    jsonl_path = outdir / "loop_prompt_packets.jsonl"
    index_path = outdir / "loop_index.csv"
    with jsonl_path.open("w", encoding="utf-8", newline="\n") as handle:
        for relative, row in enumerate(selected, start=start_index + 1):
            handle.write(json.dumps(build_episode(row, relative, source_sha), ensure_ascii=False, separators=(",", ":")) + "\n")
    index_columns = [
        "loop_id", "try_id", "variant_id", "act", "lane", "media", "geo_family",
        "contact", "cam", "wash", "style", "shot", "video_method", "count_bucket", "method_label",
    ]
    with index_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=index_columns)
        writer.writeheader()
        for relative, row in enumerate(selected, start=start_index + 1):
            record = build_episode(row, relative, source_sha)
            item = {
                "loop_id": record["loop_id"],
                "try_id": record["try_id"],
                "variant_id": clean(row.get("id")),
                "act": clean(row.get("act")),
                "lane": clean(row.get("lane")),
                "media": clean(row.get("media")),
                "geo_family": clean(row.get("geo_family")),
                "contact": clean(row.get("contact")),
                "cam": clean(row.get("cam")),
                "wash": clean(row.get("wash")),
                "style": clean(row.get("style")),
                "shot": clean(row.get("shot")),
                "video_method": clean(row.get("video_method")),
                "count_bucket": clean(row.get("count_bucket")),
                "method_label": record["method_label"],
            }
            writer.writerow(item)
    bucket_counts = Counter(clean(row.get("count_bucket")) or "UNBUCKETED" for row in selected)
    act_counts = Counter(clean(row.get("act")) for row in selected)
    media_counts = Counter(clean(row.get("media")).upper() for row in selected)
    summary = {
        "story": "THE BOUNDARY WALKER",
        "sweep_id": "SWEEP-001",
        "source_catalog": str(csv_path),
        "source_catalog_sha256": source_sha,
        "source_total_variants": len(rows),
        "selected_start_index_zero_based": start_index,
        "buckets_filter": list(buckets) if buckets else None,
        "compiled_variant_count": len(selected),
        "formula_edition": "MASTER_PROMPT_v5_20261025",
        "full_sweep_compiled": start_index == 0 and len(selected) == len(rows),
        "unique_variant_ids": len({clean(r.get("id")) for r in selected}),
        "all_selected_variant_ids_once": len({clean(r.get("id")) for r in selected}) == len(selected),
        "prompts_per_loop": 6,
        "bucket_counts": dict(sorted(bucket_counts.items())),
        "act_counts": dict(sorted(act_counts.items())),
        "media_counts": dict(sorted(media_counts.items())),
        "loop_prompt_packets": str(jsonl_path),
        "loop_index": str(index_path),
        "prompt_compiled": True,
        "external_generation_called": False,
        "image_realization": "NOT_RUN",
        "video_realization": "NOT_RUN",
        "pixel_audit_status": "NOT_RUN",
        "continuity_audit_status": "NOT_RUN",
        "visual_acceptance_status": "NOT_VERIFIED",
    }
    summary_path = outdir / "loop_plan_summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variants-csv", required=True, help="full legal variant ID CSV")
    parser.add_argument("--outdir", required=True, help="folder for JSONL prompt packages, CSV index and summary")
    parser.add_argument("--start-index", type=int, default=0, help="zero-based offset into the deterministic interleaved queue")
    parser.add_argument("--limit", type=int, default=0, help="max variants to compile; 0 compiles every legal ID")
    parser.add_argument(
        "--bucket",
        action="append",
        default=[],
        help="repeatable count_bucket filter, e.g. --bucket VIDEO_GEO --bucket HARD_DUAL48",
    )
    args = parser.parse_args()
    summary = compile_csv(
        Path(args.variants_csv),
        Path(args.outdir),
        args.start_index,
        args.limit,
        buckets=args.bucket or None,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


def export_primary_prompt_table(jsonl_path: Path, out_csv: Path, out_md: Path) -> dict[str, Any]:
    """Flatten primary-act prompts from compiled JSONL into a review table (no media generation)."""
    rows: list[dict[str, str]] = []
    with jsonl_path.open(encoding="utf-8") as handle:
        for line in handle:
            packet = json.loads(line)
            primary = next(a for a in packet["acts"] if a.get("is_primary_try"))
            phases = packet.get("frame_phases") or {}
            rows.append({
                "loop_id": packet["loop_id"],
                "try_id": packet["try_id"],
                "variant_id": packet["variant_id"],
                "lane": packet.get("lane", ""),
                "media": packet.get("primary_media", ""),
                "method_label": packet.get("method_label", ""),
                "l_sha12": packet.get("l_sha12", ""),
                "video_method": (packet.get("catalog_row") or {}).get("video_method", ""),
                "geo_family": (packet.get("catalog_row") or {}).get("geo_family", ""),
                "contact": (packet.get("catalog_row") or {}).get("contact", ""),
                "style": (packet.get("catalog_row") or {}).get("style", ""),
                "count_bucket": (packet.get("catalog_row") or {}).get("count_bucket", ""),
                "primary_prompt": primary.get("prompt", ""),
                "mid_phase_prompt": (phases.get("MID_H2") or {}).get("prompt", ""),
                "pre_phase_prompt": (phases.get("PRE_H1") or {}).get("prompt", ""),
                "post_phase_prompt": (phases.get("POST_H3") or {}).get("prompt", ""),
                "status": packet.get("status", "PROMPT_READY"),
                "external_generation_called": str(packet.get("external_generation_called", False)),
            })
    fieldnames = list(rows[0].keys()) if rows else []
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    lines = [
        "# Primary prompt table",
        "",
        f"Rows: **{len(rows)}** · status PROMPT_READY · external_generation_called false",
        "",
        "| # | variant_id | method | l_sha12 | media |",
        "| --- | --- | --- | --- | --- |",
    ]
    for i, r in enumerate(rows, 1):
        lines.append(
            f"| {i} | `{r['variant_id']}` | {r['method_label'][:60]} | `{r['l_sha12']}` | {r['media']} |"
        )
    lines.append("")
    lines.append("Full English prompts are in the companion CSV (`primary_prompt` column).")
    out_md.write_text(chr(10).join(lines) + chr(10), encoding="utf-8")
    return {"rows": len(rows), "csv": str(out_csv), "md": str(out_md)}
