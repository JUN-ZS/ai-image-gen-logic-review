#!/usr/bin/env python3
"""Compile the legal CROSS-PRODUCT of Boundary Walker's four method axes.

Axes:
  G: geometry/contact state
  C: compatible camera/action pack + artistic style
  V: compatible VIDEO timeline/closed-loop method
  N: six-act narrative route

The compiler produces complete natural-language prompts. It does not call media services and
never marks generated media, pixel geometry, continuity or video physics as accepted.
Large output is streamed directly to gzip JSONL so the full product stays portable.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
from collections import Counter
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Iterable

from bubble_break.boundary_pedestrian_loop_planner import (
    GEO_DESCRIPTIONS,
    STYLE_NAMES,
    WASH_NAMES,
    CONTACT_RULES,
    clean,
    sha256_bytes,
    style_description,
    wash_description,
)

STYLES = ("S01", "S02", "S03")
T_STATES = ("H0", "H1", "H2", "H3")
DUAL_T_STATES = ("H0", "FACE")
MULTI_STATES = ("H0", "H2")
WASHES = tuple(f"W{i:02d}" for i in range(1, 11))
ACTS = {
    "1": ("畫界", "Walk along the luminous boundary and discover that its reflection does not match the ruined city."),
    "2": ("保護", "Hold an open hand beside the transparent sphere; keep the miniature sanctuary and its residents safe."),
    "3": ("試法／碎裂", "Stage this loop's one designated method trial. Geometry is governed only by the selected geometry/contact contract."),
    "4": ("假修", "Show a beautiful but superficial repair bandage that hides, rather than solves, the boundary's fracture."),
    "5": ("一界", "Align reflections from the outside city and inside sanctuary; make the boundary visible as a relation, not only a wall."),
    "6": ("選擇", "Choose to walk the boundary again; end on an incomplete luminous ring and footstep that can match-cut to the next loop."),
}

STORY_ROUTES: dict[str, dict[str, Any]] = {
    "BP6-I20": {
        "label": "original photoreal six-act spine",
        "act_motifs": {
            "1": "a wide industrial ruin and a single drawn light boundary",
            "2": "the heroine shielding a small world inside a glass sphere",
            "3": "the selected method becomes the one physical or symbolic trial",
            "4": "a polished gold repair strip that conceals a wrong reflection",
            "5": "one continuous reflection linking both sides of the sphere",
            "6": "a quiet choice to continue walking, not a triumphant final victory",
        },
        "mv_shots": 24,
    },
    "BP6-I21": {
        "label": "alternate prop-metaphor six-act spine",
        "act_motifs": {
            "1": "a tangled yarn line across an intimate room, reimagined as a world border",
            "2": "a candy-glass cloche sheltering a miniature living city",
            "3": "diamond-rain shards surrounding the boundary while the chosen geometry stays exact",
            "4": "a claw-machine-like repair that looks safe but leaves a visible seam",
            "5": "a pool-blue translucent bandage connecting the two worlds",
            "6": "a rooftop roller-skating circle that leaves the ending open for another loop",
        },
        "mv_shots": 24,
    },
    "BP6-LOOP": {
        "label": "recursive-return story route",
        "act_motifs": {
            "1": "the same first footstep appears in a changed world, like an imperfect memory",
            "2": "the heroine protects the sanctuary but notices a new reflection moving out of sync",
            "3": "the selected method tests the boundary again; a visible trace of the previous loop remains",
            "4": "the world's repair repeats a familiar mistake, with one new clue left uncovered",
            "5": "a thin red thread links the current fracture to a mark seen in the previous loop",
            "6": "the incomplete ring of light matches the first frame, but its reflected side has changed",
        },
        "mv_shots": 24,
    },
    "BP6-SURREAL": {
        "label": "surreal-metaphor story route",
        "act_motifs": {
            "1": "an impossible corridor folds around one precise circle of light",
            "2": "the heroine holds a small universe between two shadows without crushing it",
            "3": "the world becomes symbolically impossible around the nominated contact, but the declared object geometry stays literal",
            "4": "a golden bandage grows into a doorway that cannot close the visible seam",
            "5": "the two cities share one reflection despite existing at impossible scales",
            "6": "the heroine steps through the empty centre of a ring that becomes the next beginning",
        },
        "mv_shots": 24,
    },
    "MV24": {
        "label": "24-card six-act MV edit route",
        "act_motifs": {
            "1": "use the act's wide, line, boundary-walk and pupil/reaction card family",
            "2": "use place, hold, vacuum-space and hand-near-crack card family",
            "3": "use front, low, peak and side impact cards around the one declared test",
            "4": "use panic, claw-repair, false-selfie and reflection-fuse card family",
            "5": "use peel, pain, bandage and red-thread card family",
            "6": "use ask, split, dance and final-footstep card family",
        },
        "mv_shots": 24,
    },
    "MV52": {
        "label": "52-shot six-act MV route (26 source shots × two distinct camera passes)",
        "act_motifs": {
            "1": "expand the wide, line, border-walk and pupil beats into two distinct camera passes",
            "2": "expand place, hold, vacuum-space and crack-hand beats into two distinct camera passes",
            "3": "expand front, low, peak, side, fall and net beats into two distinct camera passes; keep the chosen geometry fixed",
            "4": "expand panic, claw, selfie and fuse beats into two distinct camera passes",
            "5": "expand peel, pain, bandage and red-thread beats into two distinct camera passes",
            "6": "expand ask, split, dance and final beats into two distinct camera passes",
        },
        "mv_shots": 52,
    },
}

SHOT_CARDS_26 = [
    ("1", "MV_1_1_WIDE", "wide boundary reveal"),
    ("1", "MV_1_2_LINE", "a graphic line crossing the frame"),
    ("1", "MV_1_3_BORDER_WALK", "side tracking along the threshold"),
    ("1", "MV_1_4_PUPIL", "a close reaction reflected in the heroine's eye"),
    ("2", "MV_2_1_PLACE", "place the protected miniature sanctuary"),
    ("2", "MV_2_2_HOLD", "hold the sphere with a careful two-handed gesture"),
    ("2", "MV_2_3_VACUUM", "leave negative space between hand and glass"),
    ("2", "MV_2_4_CRACK_HAND", "show a hand near an old crack without causing new contact"),
    ("3", "MV_3_1_FRONT", "front-view geometry inspection"),
    ("3", "MV_3_2_LOW", "low-angle geometry inspection"),
    ("3", "MV_3_3_PEAK", "peak-action geometry frame"),
    ("3", "MV_3_4_SIDE", "side-profile geometry frame"),
    ("3", "MV_3_5_FALL", "outer shell fragments falling after the declared contact state allows it"),
    ("3", "MV_3_6_NET", "a wide aftermath of the boundary's fracture"),
    ("4", "MV_4_1_PANIC", "the crowd reacts to the false repair"),
    ("4", "MV_4_2_CLAW", "a repair mechanism covers the crack without fixing it"),
    ("4", "MV_4_3_SELFIE", "a false-safe reflection is framed like a promotional image"),
    ("4", "MV_4_4_FUSE", "two reflections fuse but the seam remains"),
    ("5", "MV_5_1_PEEL", "the false repair begins to peel"),
    ("5", "MV_5_2_PAIN", "the heroine recognises the cost of the boundary"),
    ("5", "MV_5_3_BANDAGE", "a translucent bandage links the two sides"),
    ("5", "MV_5_4_REDTHREAD", "a red thread crosses both sides of the sphere"),
    ("6", "MV_6_1_ASK", "the heroine asks whether protection became separation"),
    ("6", "MV_6_2_SPLIT", "a choice appears as two reflections"),
    ("6", "MV_6_3_DANCE", "people begin a shared circular step"),
    ("6", "MV_6_4_FINAL", "an incomplete ring invites the next loop"),
]


@dataclass(frozen=True)
class ImageConfig:
    geo_family: str
    contact: str
    camera_pack: str
    camera: str
    wash: str
    style: str
    shot: str
    windup: str = ""
    geometry_catalog: str = ""


def unique_values(rows: list[dict[str, str]], predicate, column: str) -> list[str]:
    return sorted({clean(row.get(column)) for row in rows if predicate(row) and clean(row.get(column))})


def load_catalog(path: Path) -> tuple[list[dict[str, str]], str]:
    raw = path.read_bytes()
    source_sha = sha256_bytes(raw)
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"id", "lane", "media", "act", "geo_family", "contact", "cam", "wash", "style", "shot", "count_bucket"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError("Variant catalogue missing fields: " + ", ".join(sorted(missing)))
        rows = list(reader)
    ids = [clean(row["id"]) for row in rows]
    if any(not value for value in ids):
        raise ValueError("Variant catalogue includes a blank ID")
    if len(ids) != len(set(ids)):
        raise ValueError("Variant catalogue includes duplicate IDs; repair the catalog before expanding products")
    return rows, source_sha


def split_windup(camera: str) -> str:
    return next((part for part in camera.split("__") if part in {"M1", "M2"}), "")


def build_image_configs(rows: list[dict[str, str]]) -> list[ImageConfig]:
    t_cameras = unique_values(rows, lambda r: r["count_bucket"] == "HARD_T_192", "cam")
    t2_cameras = unique_values(rows, lambda r: r["count_bucket"] == "HARD_DUAL48" and r["geo_family"] == "T2", "cam")
    cross_cameras = unique_values(rows, lambda r: r["count_bucket"] == "HARD_DUAL48" and r["geo_family"] == "CROSS", "cam")
    washes = tuple(sorted(set(WASHES)))
    styles = STYLES
    if len(t_cameras) != 192:
        raise ValueError(f"T camera/action matrix must have 192 unique variants; found {len(t_cameras)}")
    if len(t2_cameras) != 48 or len(cross_cameras) != 48:
        raise ValueError(f"Dual/cross matrix must have 48 camera variants each; T2={len(t2_cameras)} CROSS={len(cross_cameras)}")
    if len(washes) != 10:
        raise ValueError("Expected exactly ten independent wash-composition variants")

    configs: list[ImageConfig] = []
    # 8 axes × 12 camera angles × 2 wind-up patterns; independent full-frame trials.
    for contact in T_STATES:
        for camera in t_cameras:
            for style in styles:
                configs.append(ImageConfig("T", contact, "T192", camera, "W00", style,
                                           "FRONT", split_windup(camera), "I-01;I-02..I-05;I-18"))
    # The H2 impact pack has FRONT/LOW/PEAK/SIDE. FRONT is already represented in T192,
    # so retain only the three novel views rather than double-counting an identical front view.
    for camera in t_cameras:
        for style in styles:
            for shot in ("LOW", "PEAK", "SIDE"):
                configs.append(ImageConfig("T", "H2", "T_H2_IMPACT4", camera, "W00", style,
                                           shot, split_windup(camera), "I-01;I-04;I-18;PACK_IMPACT_4"))
    # Double T is a distinct topology. H0 is the positive-gap precursor; FACE is terminal-face contact.
    for contact in DUAL_T_STATES:
        for camera in t2_cameras:
            for style in styles:
                configs.append(ImageConfig("T2", contact, "DUAL48", camera, "W00", style,
                                           "FRONT", "", "I-06;I-07;I-19"))
    # Thick plus-sign heads collide by nominated circular end cap; not T-hammers.
    for camera in cross_cameras:
        for style in styles:
            configs.append(ImageConfig("CROSS", "FACE", "DUAL48", camera, "W00", style,
                                       "FRONT", "", "I-08;I-09;I-19"))
    # The ten framing washes multiply independently over rod control states, plant handle topologies and MULTI states.
    for contact in ("POS", "NEG"):
        for wash in washes:
            for style in styles:
                configs.append(ImageConfig("ROD", contact, "WASH10", "NA", wash, style,
                                           "FRONT", "", "I-10;I-11;I-22"))
    for geo, catalog in (("PLANT_S", "I-13"), ("PLANT_O", "I-14;I-15")):
        for wash in washes:
            for style in styles:
                configs.append(ImageConfig(geo, "PLANTED", "WASH10", "NA", wash, style,
                                           "FRONT", "", catalog))
    for contact in MULTI_STATES:
        for wash in washes:
            for style in styles:
                configs.append(ImageConfig("MULTI", contact, "WASH10", "NA", wash, style,
                                           "PEAK" if contact == "H0" else "FRONT", "", "I-16;I-17;I-22"))

    expected = {"T": 4032, "T2": 288, "CROSS": 144, "ROD": 60, "PLANT_S": 30, "PLANT_O": 30, "MULTI": 60}
    actual = Counter(item.geo_family for item in configs)
    if dict(actual) != expected:
        raise AssertionError(f"Image geometry×camera×style cross product changed: {dict(actual)}")
    return configs


VIDEO_METHODS = {
    "T": ("V-01", "V-02", "V-04", "V-09"),
    "T2": ("V-04", "V-05", "V-09"),
    "CROSS": ("V-04", "V-06", "V-09"),
    "ROD": ("V-04", "V-07", "V-09"),
    "PLANT_S": ("V-03", "V-04", "V-09"),
    "PLANT_O": ("V-03", "V-04", "V-09"),
    "MULTI": ("V-04", "V-08", "V-09"),
}
VIDEO_DESCRIPTIONS = {
    "V-01": "Generate one continuous 10-second scene, not a montage. Use a readable PRE state, approach, nominated contact/event, follow-through if applicable, and aftermath; no teleporting or geometry reset.",
    "V-02": "Use five separately prompted keyframes at 0.0s PRE_FAR, 2.0s PRE_NEAR, 4.5s CONTACT, 7.0s MID_SHOCK, and 10.0s END. Keep parent identity and scene continuity between frames.",
    "V-03": "Use the planted-cylinder fixed-anchor video method. The cylinder's base seat and anchor P remain fixed to the sphere; only the declared handle/character/camera motion may change. Never turn it into a flying hammer.",
    "V-04": "Use image-to-video from the supplied accepted parent raster. Change only the declared action variable; preserve face, outfit, topology, contact anchor, lighting direction, and background landmarks.",
    "V-05": "Use the two independent T-hammer method. Both terminal end faces and both handles remain visible; preserve separate rigid objects and oppose their selected end-face normals at contact.",
    "V-06": "Use the thick plus-sign cross-hammer method. The nominated flat circular cylinder caps meet face-to-face; no barrel, sidewall, corner, joint or handle hits first.",
    "V-07": "Use the line-striker method. The rods remain thin and straight; POS is a face-to-face positive control, while NEG deliberately turns a nominated facet away and must be labelled NEGATIVE CONTROL.",
    "V-08": "Use the one-handle multi-facet rounded-head method. Only the nominated flat facet touches; the handle and other cheeks remain clear.",
    "V-09": "Use the six-act music-video route. Generate independently reviewable act clips and selected shot cards, then edit them into a coherent three-minute loop. Do not pretend a single request generated a verified three-minute continuous take.",
}


def camera_text(config: ImageConfig) -> str:
    if config.camera_pack == "T192":
        bits = config.camera.split("__")
        return f"camera axis {bits[0]}, {next((b for b in bits if b.startswith('CAM')), 'camera unspecified')}, wind-up {config.windup}"
    if config.camera_pack == "T_H2_IMPACT4":
        bits = config.camera.split("__")
        shot_words = {"LOW": "low-angle sweep", "PEAK": "peak-action", "SIDE": "side-profile"}
        return f"{shot_words.get(config.shot, config.shot)}; camera axis {bits[0]}, {next((b for b in bits if b.startswith('CAM')), 'camera unspecified')}, wind-up {config.windup}"
    if config.camera_pack == "DUAL48":
        bits = config.camera.split("__")
        return f"dual-object axis {bits[0]}, {next((b for b in bits if b.startswith('CAM')), 'camera unspecified')}"
    return f"{config.wash}: {wash_description(config.wash)}"


def geometry_contract(geo: str, contact: str) -> str:
    description = GEO_DESCRIPTIONS[geo]
    if geo in {"PLANT_S", "PLANT_O"}:
        handle = (
            "The handle is attached at the side-middle tangent of the cylinder."
            if geo == "PLANT_S"
            else "The handle attaches to the cylinder's outer terminal end along its axis."
        )
        return (
            description + " The cylinder is already planted at anchor P on the spherical shell. "
            + handle
            + " Keep the anchor fixed; this is not a flying strike or a gap-closing impact."
        )
    if geo == "ROD":
        rule = CONTACT_RULES["POS"] if contact == "POS" else CONTACT_RULES["NEG"]
        return description + " " + rule
    if geo == "MULTI":
        if contact == "H0":
            rule = "The nominated flat facet is aligned toward the boundary but remains visibly separated by a positive air gap; no contact effects."
        else:
            rule = "Only the nominated broad planar facet touches the boundary at P; no edge, rounded cheek or handle may touch first. First fine cracks originate at P."
        return description + " " + rule
    if contact == "H0":
        return description + " The nominated contact face is aligned but a clear positive air gap remains. No contact, cracks, sparks or glow."
    if contact == "H1":
        return description + " The whole rigid object has advanced closer but the nominated contact face still has a visible positive air gap. No cracks or contact effects."
    if contact == "H2":
        if geo == "T":
            return description + " The designated flat terminal end face is the one and only first contact at P; zero gap, no interpenetration, opposing normals, first micro-cracks start at P."
        if geo == "T2":
            return description + " The two nominated flat terminal faces meet at one shared contact region with opposing normals. Both sidewalls, corners and handles stay clear."
        if geo == "CROSS":
            return description + " The nominated flat circular outer end caps meet face-to-face at P. No curved barrel, broad side, corner, joint or handle touches first."
    if contact == "H3":
        return description + " Immediate follow-through: the same rigid object advances slightly along the established axis after contact at P; cracks propagate outward from P."
    if contact == "FACE":
        if geo == "T2":
            return description + " Only the two nominated flat terminal end faces touch each other. They remain separate rigid T-hammers with opposing face normals."
        return description + " Only the two nominated flat circular terminal end caps touch; curved barrels and sidewalls remain clear."
    if contact == "PLANTED":
        return description + " The nominated base seat is already in contact at fixed anchor P; no flying impact."
    return description + " Follow only the declared contact state; do not invent a different contact surface."


def story_route_text(route_id: str, act: str) -> str:
    route = STORY_ROUTES[route_id]
    return f"Story route {route_id} ({route['label']}): {route['act_motifs'][act]}"


def make_image_prompt(config: ImageConfig, video_method: str, route_id: str,
                      loop_id: str, try_id: str, act: str, primary: bool,
                      camera_override: str = "") -> str:
    act_title, base_event = ACTS[act]
    route_text = story_route_text(route_id, act)
    style = style_description(config.style)
    if primary:
        selected = geometry_contract(config.geo_family, config.contact)
        view = camera_override or camera_text(config)
        shot_text = f"Selected camera/action method {config.camera_pack}: {view}; selected shot {config.shot}."
        event = (
            f"ACT 3 primary experiment: {selected} "
            f"{shot_text} The primary VIDEO method paired with this image experiment is {video_method}."
        )
    else:
        event = (
            f"{base_event} This is a SOFT narrative companion frame, with no active weapon impact and no new tool topology."
        )
        shot_text = "Use the selected story route's act staging; keep negative space for a later editorial method stamp."
    return (
        f"Create one single full-frame 16:9 cinematic image for THE BOUNDARY WALKER, LOOP {loop_id}, TRY {try_id}, "
        f"ACT {act}: {act_title}. {route_text}. "
        "Use the same approved adult East Asian heroine reference: unchanged identity, long dark-brown hair, body proportions "
        "and canonical outfit. The world is an outer ruined city around a translucent boundary sphere containing a living miniature sanctuary. "
        f"Visual style {config.style}: {style}. {event} {shot_text} "
        "Use coherent lighting, clear focal geometry, meaningful negative space and a recurring circular boundary motif. "
        "For soft acts, keep the sanctuary safe and do not add a weapon impact. "
        "Do not generate letters, numbers, captions, logos, interface labels or watermarks; an exact artistic TRY label will be composited after generation. "
        "One image only, not a collage. Prompt readiness is not image acceptance."
    )


def make_video_prompt(config: ImageConfig, video_method: str, route_id: str,
                      loop_id: str, try_id: str, act: str, primary: bool,
                      shot_label: str = "", camera_pass: str = "") -> str:
    act_title, base_event = ACTS[act]
    route_text = story_route_text(route_id, act)
    style = style_description(config.style)
    selected = geometry_contract(config.geo_family, config.contact)
    if primary:
        method_text = VIDEO_DESCRIPTIONS[video_method]
        if video_method in {"V-01", "V-02"}:
            focus = f"Focus geometry is {selected} The selected contact state {config.contact} is the target still state; preserve it at the matching timeline/keyframe."
        else:
            focus = selected
        event = f"PRIMARY ACT 3 VIDEO METHOD {video_method}. {method_text} {focus}"
        view = camera_text(config)
    else:
        event = (
            "COMPANION NARRATIVE CLIP: use V-09 style as an independently reviewable 5–8 second clip. "
            "No active weapon contact, no new tool topology, and no unexplained impact. " + base_event
        )
        view = "follow the act-specific story route without forcing the ACT 3 weapon into this frame"
    shot_clause = f" Shot card {shot_label}." if shot_label else ""
    pass_clause = f" Camera pass {camera_pass}; it must differ in angle or distance from its companion pass." if camera_pass else ""
    return (
        f"Create one independently reviewable cinematic video clip for THE BOUNDARY WALKER, LOOP {loop_id}, TRY {try_id}, "
        f"ACT {act}: {act_title}. {route_text}. Keep the supplied approved heroine identity, world landmarks, light direction, sphere shape "
        f"and style {config.style} ({style}) consistent. {event} Camera/action selection: {view}.{shot_clause}{pass_clause} "
        "Animate one clear causal event; no teleportation, extra limbs, invented handles, object topology changes, random crack origin, "
        "or resident injury. Do not generate subtitles, logos, letters, numbers or watermarks; exact method typography is added afterward as an ASS layer. "
        "Return a standalone clip, not a claimed verified three-minute movie. Video audit remains NOT_RUN until real frames are inspected."
    )


def make_keyframes(config: ImageConfig, route_id: str, loop_id: str, try_id: str) -> list[dict[str, str]]:
    stages = [
        ("KF1", "0.0s PRE_FAR", "the active face is aligned with a wide positive air gap; pristine boundary, no effects"),
        ("KF2", "2.0s PRE_NEAR", "the rigid object is closer but a positive air gap remains; no contact or cracks"),
        ("KF3", "4.5s CONTACT", "the declared contact face touches at P with zero gap and no penetration; first micro-cracks start at P only"),
        ("KF4", "7.0s MID_SHOCK", "cracks and shock ripple expand from the same P; the same rigid object follows through"),
        ("KF5", "10.0s END", "the outer shell breaks outward only if allowed by the selected state; the inner sanctuary remains safe"),
    ]
    frames = []
    for frame_id, timestamp, state in stages:
        frames.append({
            "keyframe_id": frame_id,
            "timestamp": timestamp,
            "prompt": (
                f"Create one standalone full-frame 16:9 keyframe for THE BOUNDARY WALKER, LOOP {loop_id}, TRY {try_id}, "
                f"video method V-02, {timestamp}. Use the approved heroine and scene references and exact topology: "
                f"{GEO_DESCRIPTIONS[config.geo_family]} Focus experiment contract: {geometry_contract(config.geo_family, config.contact)} "
                f"Required state now: {state}. Story route: {story_route_text(route_id, '3')}. Camera/action: {camera_text(config)}. "
                f"Style: {style_description(config.style)}. Preserve face, outfit, sphere, anchor P, light and landmarks. "
                "No topology change, no fake gap, no hidden contact seam, no text, no watermark. This is one keyframe only; acceptance requires actual image inspection."
            ),
        })
    return frames


def mv_shot_specs(route_id: str) -> list[tuple[str, str, str, str]]:
    cards = SHOT_CARDS_26 if route_id == "MV52" else SHOT_CARDS_26[:]
    if route_id == "MV24":
        cards = [x for x in SHOT_CARDS_26 if x[0] != "3" or x[1] in {"MV_3_1_FRONT", "MV_3_2_LOW", "MV_3_3_PEAK", "MV_3_4_SIDE"}]
    # The 24-card method removes two ACT3 aftermath cards; the 26-source-shot method keeps all cards.
    specs: list[tuple[str, str, str, str]] = []
    for act, shot_id, shot_desc in cards:
        specs.append((act, shot_id, shot_desc, "A"))
        if route_id == "MV52":
            specs.append((act, shot_id, shot_desc, "B"))
    expected = 52 if route_id == "MV52" else 24
    if len(specs) != expected:
        raise AssertionError(f"{route_id} should contain {expected} prompts, got {len(specs)}")
    return specs


def make_mv_shots(config: ImageConfig, video_method: str, route_id: str,
                  loop_id: str, try_id: str) -> list[dict[str, str]]:
    specs = mv_shot_specs(route_id)
    output = []
    for index, (act, shot_id, description, camera_pass) in enumerate(specs, start=1):
        primary = act == "3"
        camera_override = f"story shot {shot_id}: {description}; camera pass {camera_pass}"
        image_prompt = make_image_prompt(
            config, video_method, route_id, loop_id, try_id, act, primary,
            camera_override=camera_override,
        )
        video_prompt = make_video_prompt(
            config, video_method, route_id, loop_id, try_id, act, primary,
            shot_label=f"{shot_id} / {description}", camera_pass=camera_pass,
        )
        output.append({
            "shot_index": f"{index:02d}",
            "act_id": act,
            "shot_id": shot_id,
            "camera_pass": camera_pass,
            "image_prompt": image_prompt,
            "video_prompt": video_prompt,
        })
    return output


def combo_key(config: ImageConfig, video_method: str, route_id: str) -> str:
    fields = asdict(config)
    fields.update({"video_method": video_method, "story_route": route_id})
    return json.dumps(fields, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def compile_product_matrix(catalog_csv: Path, outdir: Path, catalog_doc: Path,
                           start_index: int = 0, limit: int = 0) -> dict[str, Any]:
    rows, source_sha = load_catalog(catalog_csv)
    configs = build_image_configs(rows)
    if route_ids := tuple(STORY_ROUTES.keys()):
        routes = route_ids
    else:
        raise AssertionError("No story routes registered")

    combos: list[tuple[str, ImageConfig, str, str]] = []
    for config in configs:
        for video_method in VIDEO_METHODS[config.geo_family]:
            for route_id in routes:
                key = combo_key(config, video_method, route_id)
                digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
                combos.append((digest, config, video_method, route_id))
    # Stable hash ordering distributes methods, styles, camera packs and story routes through the full queue.
    combos.sort(key=lambda item: item[0])
    total = len(combos)
    if start_index < 0 or start_index >= max(1, total):
        raise ValueError("start_index must be within matrix range")
    selected = combos[start_index:] if limit <= 0 else combos[start_index:start_index + limit]
    if not selected:
        raise ValueError("No cross-product combinations selected")
    outdir.mkdir(parents=True, exist_ok=True)
    package_path = outdir / "boundary_walker_full_product.jsonl.gz"
    index_path = outdir / "boundary_walker_product_index.csv"
    index_fields = [
        "sequence", "combination_id", "loop_id", "try_id", "geo_family", "contact",
        "camera_pack", "camera", "wash", "windup", "shot", "style", "video_method",
        "story_route", "reference_catalog_ids",
    ]
    bucket_count: Counter[str] = Counter()
    geometry_count: Counter[str] = Counter()
    video_count: Counter[str] = Counter()
    story_count: Counter[str] = Counter()
    media_prompt_count = 0
    keyframe_prompt_count = 0
    mv_shot_count = 0
    with index_path.open("w", encoding="utf-8", newline="") as idx, gzip.open(package_path, "wt", encoding="utf-8", newline="\n", compresslevel=9) as package:
        writer = csv.DictWriter(idx, fieldnames=index_fields)
        writer.writeheader()
        for sequence, (digest, config, video_method, route_id) in enumerate(selected, start=start_index + 1):
            combo_id = "BPX-" + digest[:16].upper()
            loop_id = f"LOOP-{sequence:06d}"
            try_id = "TRY-" + digest[:12].upper()
            acts = []
            for act, (title, _) in ACTS.items():
                primary = act == "3"
                acts.append({
                    "act_id": act,
                    "act_title": title,
                    "image_prompt_id": f"{combo_id}-I-ACT{act}",
                    "video_prompt_id": f"{combo_id}-V-ACT{act}",
                    "image_prompt": make_image_prompt(config, video_method, route_id, loop_id, try_id, act, primary),
                    "video_prompt": make_video_prompt(config, video_method, route_id, loop_id, try_id, act, primary),
                    "primary_try": primary,
                })
            keyframes = make_keyframes(config, route_id, loop_id, try_id) if video_method == "V-02" else []
            mv_shots = make_mv_shots(config, video_method, route_id, loop_id, try_id) if video_method == "V-09" else []
            record = {
                "combination_id": combo_id,
                "loop_id": loop_id,
                "try_id": try_id,
                "sweep_id": "FULL-CROSS-PRODUCT-001",
                "axes": {
                    **asdict(config),
                    "video_method": video_method,
                    "story_route": route_id,
                    "story_route_label": STORY_ROUTES[route_id]["label"],
                },
                "geometry_contract": geometry_contract(config.geo_family, config.contact),
                "reference_catalog_ids": config.geometry_catalog,
                "style_description": style_description(config.style),
                "camera_description": camera_text(config),
                "video_method_description": VIDEO_DESCRIPTIONS[video_method],
                "acts": acts,
                "video_keyframes": keyframes,
                "mv_shots": mv_shots,
                "status": "PROMPT_READY",
                "external_generation_called": False,
                "image_realization": "NOT_RUN",
                "video_realization": "NOT_RUN",
                "pixel_audit_status": "NOT_RUN",
                "continuity_audit_status": "NOT_RUN",
                "video_audit_status": "NOT_RUN",
                "visual_acceptance_status": "NOT_VERIFIED",
                "source_variant_csv_sha256": source_sha,
                "source_prompt_catalog_sha256": sha256_bytes(catalog_doc.read_bytes()),
            }
            package.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
            writer.writerow({
                "sequence": sequence,
                "combination_id": combo_id,
                "loop_id": loop_id,
                "try_id": try_id,
                "geo_family": config.geo_family,
                "contact": config.contact,
                "camera_pack": config.camera_pack,
                "camera": config.camera,
                "wash": config.wash,
                "windup": config.windup,
                "shot": config.shot,
                "style": config.style,
                "video_method": video_method,
                "story_route": route_id,
                "reference_catalog_ids": config.geometry_catalog,
            })
            bucket_count[config.camera_pack] += 1
            geometry_count[config.geo_family] += 1
            video_count[video_method] += 1
            story_count[route_id] += 1
            media_prompt_count += len(acts) * 2
            keyframe_prompt_count += len(keyframes)
            mv_shot_count += len(mv_shots)
    summary = {
        "title": "THE BOUNDARY WALKER full legal cross-product",
        "sweep_id": "FULL-CROSS-PRODUCT-001",
        "source_catalog_csv": str(catalog_csv),
        "source_catalog_csv_sha256": source_sha,
        "source_prompt_catalog": str(catalog_doc),
        "source_prompt_catalog_sha256": sha256_bytes(catalog_doc.read_bytes()),
        "source_variant_rows": len(rows),
        "image_geometry_camera_style_configs": len(configs),
        "image_geometry_camera_style_counts": dict(sorted(Counter(c.geo_family for c in configs).items())),
        "compatible_geometry_camera_style_video_configs": sum(len(VIDEO_METHODS[c.geo_family]) for c in configs),
        "story_route_factor": len(STORY_ROUTES),
        "story_routes": {key: {"label": value["label"], "mv_shots_if_v09": value["mv_shots"]} for key, value in STORY_ROUTES.items()},
        "full_cross_product_combinations": total,
        "compiled_start_index_zero_based": start_index,
        "compiled_combinations": len(selected),
        "full_product_compiled": start_index == 0 and len(selected) == total,
        "unique_combination_ids": len({combo[0] for combo in selected}),
        "all_combination_ids_unique": len({combo[0] for combo in selected}) == len(selected),
        "combo_counts_by_camera_pack": dict(sorted(bucket_count.items())),
        "combo_counts_by_geometry": dict(sorted(geometry_count.items())),
        "combo_counts_by_video_method": dict(sorted(video_count.items())),
        "combo_counts_by_story_route": dict(sorted(story_count.items())),
        "act_prompt_pairs_per_combination": 12,
        "compiled_base_image_and_video_prompt_count": media_prompt_count,
        "video_keyframe_prompts_compiled": keyframe_prompt_count,
        "mv_shot_pairs_compiled": mv_shot_count,
        "mv_shot_image_and_video_prompt_count": mv_shot_count * 2,
        "output_packages_gzip": str(package_path),
        "output_index_csv": str(index_path),
        "status": "PROMPT_MATRIX_COMPILED_ONLY",
        "external_generation_called": False,
        "image_realization": "NOT_RUN",
        "video_realization": "NOT_RUN",
        "pixel_audit_status": "NOT_RUN",
        "continuity_audit_status": "NOT_RUN",
        "video_audit_status": "NOT_RUN",
        "visual_acceptance_status": "NOT_VERIFIED",
        "rules": [
            "Each product row selects exactly one geometry/contact state, one compatible camera/action pack, one style, one compatible video method and one narrative route.",
            "Only ACT 3 receives the selected hard geometry; ACTS 1/2/4/5/6 are soft narrative companions and never add a second impact topology.",
            "T H2 FRONT is shared with the standard T192 front frame; H2 impact pack adds LOW/PEAK/SIDE only so identical FRONT pixels are not double-counted.",
            "V-02 expands to five separately written keyframe prompts; V-09 expands into 24 or 52 shot cards with independent image and video prompts.",
            "PROMPT_READY is not equivalent to image/video generation, geometry PASS, continuity PASS or video audit PASS.",
        ],
    }
    (outdir / "boundary_walker_product_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variants-csv", required=True)
    parser.add_argument("--catalog-doc", required=True)
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()
    summary = compile_product_matrix(
        Path(args.variants_csv), Path(args.outdir), Path(args.catalog_doc),
        start_index=args.start_index, limit=args.limit,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
