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
from dataclasses import dataclass, asdict, replace
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
POSE_VARIANTS = ("P01", "P02", "P03", "P04")
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

# A series is a fixed style + world + protagonist + six-act story treatment.
# Styles never change inside a series. Every series has its own world and lead character.
_SERIES_ROWS = [
    ("S01-RAIN-TOKYO", "S01", "WORLD-RAIN-TOKYO", "Rainy Tokyo / 雨夜東京",
     "a rain-soaked Tokyo rail district at blue hour: elevated trains, wet alleys, vending-machine glow, reflections on black asphalt, a translucent boundary sphere suspended between crosswalks",
     "an adult Japanese woman courier with a short rain-dark bob, reflective transit jacket, messenger harness and one scarlet glove",
     "the trains carry memories of earlier loops; each crossing reveals another version of the same boundary", 24),
    ("S01-SNOW-SOCIETY", "S01", "WORLD-SNOW-SOCIETY", "Snow Society / 雪社",
     "a remote snowbound mountain society: timber houses under deep snow, frozen shrine steps, wind-carved ice arches, warm windows behind a crystal boundary",
     "an adult Inuit-inspired female ice-cartographer with a thick white parka, braided dark hair, frost-marked gloves and a map case",
     "the village survives by keeping a storm outside, until its boundary begins reflecting a village that no longer exists", 24),
    ("S01-INDUSTRIAL-RUINS", "S01", "WORLD-INDUSTRIAL-RUINS", "Industrial Ruins / 工業遺城",
     "a vast abandoned industrial city with broken gantries, oxidized steel, hanging cables, furnace haze and a living miniature sanctuary behind translucent glass",
     "an adult East Asian salvage engineer with long dark hair tied low, a graphite flight suit, reinforced boots and a tool belt",
     "a repair engineer discovers that every repair preserves the wall but erases one street from memory", 52),
    ("S01-RED-DUNE", "S01", "WORLD-RED-DUNE", "Red Dune Observatory / 赤沙觀測站",
     "a red-dune desert observatory with wind-buried telescopes, a cracked copper dome, sand-sculpted pillars and a blue-glass world boundary",
     "an adult Black woman astronomer with close-cropped hair, a weathered ochre field coat and brass optical instruments",
     "the observatory has measured the boundary for centuries, but every reading predicts a different ending", 24),
    ("S01-UNDERSEA-METRO", "S01", "WORLD-UNDERSEA-METRO", "Undersea Metro / 海底地鐵",
     "an abandoned underwater metro station, algae-lit tiled tunnels, slow drifting silt, coral growing through train windows and a luminous boundary dome",
     "an adult Filipino woman salvage diver with a close-fitting dive suit, braided hair under a clear helmet and a tethered survey lamp",
     "each passing train returns from a future that the passengers have not yet lived", 24),
    ("S01-ORBITAL-TRAIN", "S01", "WORLD-ORBITAL-TRAIN", "Orbital Train / 軌道列車",
     "a rotating orbital rail terminal above a storm-covered planet, long glass platforms, red safety beacons and a circular habitat boundary",
     "an adult android railway inspector with a porcelain faceplate, dark service coat, exposed brass wrist joints and a luminous eye slit",
     "the station's final train loops forever, carrying one empty seat reserved for the next attempt", 24),

    ("S02-CANDY-GLASS", "S02", "WORLD-CANDY-GLASS", "Candy Glass City / 糖果玻璃城",
     "a candy-colored miniature city beneath a glass cloche, pastel confectionery towers, sugar-glass bridges and soft reflected window lights",
     "an adult woman confectioner with pastel pink twin buns, a mint apron over a lilac work dress and flour-dusted hands",
     "the city looks safe because it is sweet; each repair hides a new crack beneath the icing", 24),
    ("S02-ROOFTOP-ROLLER", "S02", "WORLD-ROOFTOP-ROLLER", "Rooftop Roller Garden / 天台滑輪花園",
     "a rooftop garden city with roller tracks winding through flower beds, little greenhouse domes, ribbon bridges and warm sunset clouds",
     "an adult nonbinary street dancer with a copper undercut, oversized lemon jacket, knee pads and bright roller skates",
     "the protagonist follows circular skate marks left by a future self", 24),
    ("S02-BLOSSOM-SUBURB", "S02", "WORLD-BLOSSOM-SUBURB", "Blossom Suburb / 櫻花郊區",
     "a dreamy spring suburb of blossom tunnels, tiny footbridges, translucent bus shelters and a petal-filled boundary sphere",
     "an adult Japanese florist with a long silver braid, a cream cardigan, sage trousers and a canvas flower satchel",
     "petals cross the boundary even when people cannot, revealing an unexpected shared world", 24),
    ("S02-PAPER-MARKET", "S02", "WORLD-PAPER-MARKET", "Paper Lantern Market / 紙燈市集",
     "a paper-craft market of folded lanterns, layered washi stalls, tiny origami rooftops, hanging thread and a hand-cut circular world gate",
     "an adult older Taiwanese papermaker with silver hair, indigo apron, paper-cutting shears and ink-stained fingertips",
     "every paper lantern carries one forgotten story, and the wrong fold causes the same disaster again", 24),
    ("S02-AQUARIUM-CAFE", "S02", "WORLD-AQUARIUM-CAFE", "Aquarium Café / 水族咖啡館",
     "a pastel aquarium café with a glass floor, drifting jellyfish, coral shelves, rounded tables and a miniature living town inside a spherical tank",
     "an adult Black woman marine biologist with natural curls, a teal café apron and a notebook covered in fish sketches",
     "the café's fish migrate through a wall the customers insist is solid", 24),
    ("S02-AUTUMN-FESTIVAL", "S02", "WORLD-AUTUMN-FESTIVAL", "Autumn Lantern Festival / 秋燈祭",
     "a cozy autumn festival street with maple leaves, hand-painted lanterns, small bridges, food stalls and a warm glowing circular boundary",
     "an adult Korean percussionist with a short auburn bob, a mustard festival coat and a strapped hand drum",
     "the festival repeats every evening, but one lantern moves closer to the exit on each loop", 52),

    ("S03-INK-MOUNTAIN", "S03", "WORLD-INK-MOUNTAIN", "Ink-Wash Mountain Society / 水墨山社",
     "an ink-wash mountain society of layered paper ridges, wet black brush clouds, mineral-blue streams, unpainted mist and a circular ink boundary",
     "an adult Chinese woman wandering calligrapher with a shaved-side bun, layered charcoal robes, a bamboo brush case and ink-stained sleeves",
     "the blank paper beyond the mountain is not empty; it is the previous world waiting to be painted back", 24),
    ("S03-MIRROR-CITY", "S03", "WORLD-MIRROR-CITY", "Mirror City / 鏡面之城",
     "an impossible mirror city with inverted streets, floating staircases, doubled moons, reflective black water and a transparent circular threshold",
     "an adult male stage illusionist with a shaved head, asymmetric black coat, mirrored cuffs and a single white eye patch",
     "every reflection performs a different choice, and only one reflection remembers the true contact point", 24),
    ("S03-ORIGAMI-MOON", "S03", "WORLD-ORIGAMI-MOON", "Origami Moon Station / 摺紙月站",
     "a folded-paper lunar station with paper cranes orbiting a pale moon, sharp geometric cliffs and an impossible thin boundary ring",
     "an adult cyborg lunar mechanic with a ceramic jaw, dark pressure suit and copper foil repairs along one forearm",
     "each folded corner is a possible world; unfolding the wrong corner resets the station", 24),
    ("S03-RED-THREAD-LABYRINTH", "S03", "WORLD-RED-THREAD-LABYRINTH", "Red Thread Labyrinth / 紅線迷宮",
     "a surreal labyrinth woven from red threads, suspended doors, long shadow corridors and glass bubbles containing tiny cities",
     "an adult South Asian woman maze-runner with a shaved head, layered burgundy fabric and a spool of luminous thread",
     "the thread connects failed attempts rather than exits, and the protagonist must read the knots as history", 24),
    ("S03-GLASS-OCEAN", "S03", "WORLD-GLASS-OCEAN", "Glass Ocean Cathedral / 玻璃海堂",
     "a cathedral submerged in a glass ocean, floating pews, crystal kelp, impossible reflections and a huge translucent circular boundary",
     "an adult Black nonbinary sound artist with silver locs, a flowing midnight-blue coat and a small resonant metal instrument",
     "sound travels between worlds while bodies remain separated; the final note changes the reflection, not the wall", 24),
    ("S03-FLOATING-MONASTERY", "S03", "WORLD-FLOATING-MONASTERY", "Floating Stair Monastery / 懸階寺",
     "a floating mountain monastery of endless stairways, suspended stone courtyards, ink-black pines and an open ring of light above clouds",
     "an adult elderly Japanese monk with a weathered face, white brows, a patched indigo robe and a carved walking staff",
     "the stairs always return to the starting gate, but each loop leaves a new footprint in the stone", 52),
]


def _series_act_motifs(world_name: str, world_id: str, hook: str) -> dict[str, str]:
    return {
        "1": f"Open on {world_name}: reveal the boundary from an unusual insect-eye, bird's-eye or extreme-wide viewpoint; the protagonist is already moving, not posing for a portrait. {hook}.",
        "2": f"Show the protagonist actively protecting the small sanctuary in {world_name}: a distinct crouch, reach, lean or over-the-shoulder gesture, with residents visibly safe.",
        "3": f"Stage this TRY's one precise geometry/contact test in {world_name}; use the locked method contract, a different action pose and its selected camera. {hook}.",
        "4": f"The protagonist attempts a beautiful but false repair in {world_name}; use a Dutch angle or compressed telephoto composition and reveal a new clue in the seam.",
        "5": f"Let {world_name}'s reflections, people or natural elements cross visually while the physical boundary remains; use an overhead, macro or through-glass view rather than repeating ACT 3's setup.",
        "6": f"Give the protagonist a new decision in {world_name}: turn, walk, skate, dive, climb or step through the incomplete luminous ring. End on a match-cut motif, not a copied pose.",
    }


STORY_SERIES: dict[str, dict[str, Any]] = {
    row[0]: {
        "series_id": row[0],
        "style_id": row[1],
        "world_id": row[2],
        "world_name": row[3],
        "world_description": row[4],
        "protagonist_description": row[5],
        "story_hook": row[6],
        "label": f"{row[3]} / {row[1]}",
        "act_motifs": _series_act_motifs(row[3], row[2], row[6]),
        "mv_shots": row[7],
        "visual_rule": f"Series {row[0]} uses style {row[1]} consistently across all six acts; do not mix another series' world, palette or rendering mode.",
    }
    for row in _SERIES_ROWS
}
STORY_ROUTES = STORY_SERIES  # compatibility alias for external notebooks
ACT_CAMERA_PROFILES = {
    "1": "extreme-wide establishing shot from insect-eye curb level or an unusual bird's-eye angle; the protagonist moves through the world",
    "2": "over-the-shoulder close-up or macro detail of hands protecting the sanctuary; vary focal distance from ACT 1",
    "3": "use the selected geometry-specific camera/action method; keep the contact face and state inspectable",
    "4": "Dutch-angle compressed telephoto shot, with the protagonist physically testing or repairing a visible seam",
    "5": "overhead, through-glass or split-reflection composition; show interaction between both sides rather than another frontal portrait",
    "6": "low rear tracking shot or long-lens silhouette; the protagonist turns and moves into the incomplete ring for the next loop",
}
POSE_DESCRIPTIONS = {
    "P01": {
        "HARD": "grounded power brace: wide staggered feet, bent lead knee, hips and shoulders loaded along the declared approach axis",
        "PLANT": "standing calibration stance beside the immovable planted cylinder, one hand on the designated handle and the other tracing the fixed base seam",
    },
    "P02": {
        "HARD": "airborne lunge frozen at the requested contact state: extended lead leg, counterbalancing rear leg and a rigid tool that does not bend or rotate internally",
        "PLANT": "one foot raised on a nearby ledge while reaching toward the anchored cylinder; the planted base and contact point P remain fixed",
    },
    "P03": {
        "HARD": "deep low crouch or kneeling load-up, torso rotated for balance, with the full rigid tool and active face still readable",
        "PLANT": "low kneeling inspection posture beside the fixed cylinder, head and hand close to the contact seam while the anchor stays unchanged",
    },
    "P04": {
        "HARD": "dynamic counter-rotation with a long reach and visible body momentum; only the whole rigid tool moves as one object along the valid path",
        "PLANT": "side-on reach-around inspection pose that changes the person's silhouette but never shifts the planted base or handle attachment topology",
    },
}


def pose_description(config: "ImageConfig") -> str:
    family = "PLANT" if config.geo_family in {"PLANT_S", "PLANT_O"} else "HARD"
    return POSE_DESCRIPTIONS[config.pose_id][family]


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
    pose_id: str = "P01"


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
        raise AssertionError(f"Base image geometry×camera×style product changed: {dict(actual)}")
    # Pose is a real independent factor, but each pose preserves the selected geometry/contact contract.
    configs = [replace(config, pose_id=pose_id) for config in configs for pose_id in POSE_VARIANTS]
    expanded_expected = {key: value * len(POSE_VARIANTS) for key, value in expected.items()}
    expanded_actual = Counter(item.geo_family for item in configs)
    if dict(expanded_actual) != expanded_expected:
        raise AssertionError(f"Pose cross-product changed: {dict(expanded_actual)}")
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


METHOD_LABELS = {
    "T": "single T-hammer / nominated terminal end face",
    "T2": "two independent T-hammers / terminal face-to-face",
    "CROSS": "thick plus-sign cross-hammers / flat circular end-cap face-to-face",
    "ROD": "90-degree line-striker rods / positive or negative facet control",
    "PLANT_S": "planted double-ended cylinder / side-middle tangent handle",
    "PLANT_O": "planted double-ended cylinder / axial outer-end handle",
    "MULTI": "single multi-facet rounded head / nominated flat face",
}


def art_label_spec(config: ImageConfig, video_method: str, series_id: str,
                   loop_id: str, try_id: str, combo_id: str) -> dict[str, Any]:
    series = STORY_SERIES[series_id]
    method_name = METHOD_LABELS[config.geo_family]
    contact_label = {
        "H0": "PRE_FAR / positive gap",
        "H1": "PRE_NEAR / positive gap",
        "H2": "first contact at P",
        "H3": "same-axis follow-through",
        "FACE": "nominated faces meet",
        "POS": "positive 90-degree control",
        "NEG": "negative control / expected fail",
        "PLANTED": "fixed planted anchor",
    }.get(config.contact, config.contact)
    return {
        "story": "THE BOUNDARY WALKER",
        "loop_id": loop_id,
        "try_id": try_id,
        "series_id": series_id,
        "world_label": series["world_name"],
        "method_id": f"GEO.{config.geo_family}",
        "method_label": f"{method_name} · {contact_label} · {video_method}",
        "geometry_family": config.geo_family,
        "contact_method": config.contact,
        "camera_id": f"{config.camera_pack}-{config.camera}-{config.windup or config.wash}",
        "pose_id": config.pose_id,
        "style_id": config.style,
        "panel_side": "right",
        "art_direction": "large floating 3D poster; reserved plaque covers ~34.3% of full frame",
        "status": "REVIEW_PENDING",
        "acts": {
            act: {
                "act_id": act,
                "prompt_id": f"{combo_id}-I-ACT{act}",
                "video_prompt_id": f"{combo_id}-V-ACT{act}",
                "note": f"ACT {act}: {ACTS[act][0]} · primary loop method remains {config.geo_family}/{config.contact}",
            }
            for act in ACTS
        },
    }


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


def story_route_text(series_id: str, act: str) -> str:
    series = STORY_SERIES[series_id]
    return (
        f"SERIES {series_id} / WORLD {series['world_id']} — {series['world_name']}. "
        f"Series style: {series['style_id']}. {series['visual_rule']} "
        f"World bible: {series['world_description']}. Protagonist for this series: {series['protagonist_description']}. "
        f"Story hook: {series['story_hook']}. ACT {act}: {series['act_motifs'][act]}"
    )


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
    series = STORY_SERIES[route_id]
    pose_text = pose_description(config) if primary else ""
    action_profile = f"Primary action/body pose: {pose_text}" if primary else f"Act-specific camera/action profile: {ACT_CAMERA_PROFILES[act]}"
    return (
        f"Create one single full-frame 16:9 cinematic image for THE BOUNDARY WALKER, LOOP {loop_id}, TRY {try_id}, "
        f"SERIES {route_id}, WORLD {series['world_id']}, PROMPT {config.geometry_catalog or 'STORY-SPINE'}; ACT {act}: {act_title}. {route_text}. "
        f"Character bible: {series['protagonist_description']}. Keep this protagonist recognizably consistent across this series' six acts, but allow other series to use different characters. "
        f"Set dressing and world: {series['world_description']}. Visual style {config.style}: {style}. {event} {shot_text} "
        f"{action_profile}. Make each act visually distinct: alter body silhouette, camera height, focal length, distance and screen direction according to the act profile; never reuse the same neutral standing pose across six acts. "
        "The selected geometry/contact contract is the only locked variable for this TRY: preserve its nominated active face, contact point, object relationship and causal state exactly. Across different TRYs and series, freely redesign the protagonist, costume, props, world, narrative, lighting, palette and composition. Within this selected series alone, keep one consistent art direction, world bible and protagonist identity across its six connected acts. "
        "Use rich 3D cinematic depth, atmospheric perspective, believable material response and a recurring boundary motif. Keep the sanctuary safe in soft acts. "
        "Do not generate letters, numbers, captions, logos, interface labels or watermarks; a large exact 3D poster-style TRY typography layer will be composited afterward and may occupy up to one-third of the frame. Leave a clear planned title/method zone without hiding the active contact surface. "
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
    series = STORY_SERIES[route_id]
    pose_text = pose_description(config) if primary else ACT_CAMERA_PROFILES[act]
    return (
        f"Create one independently reviewable cinematic video clip for THE BOUNDARY WALKER, LOOP {loop_id}, TRY {try_id}, "
        f"SERIES {route_id}, WORLD {series['world_id']}, ACT {act}: {act_title}. {route_text}. "
        f"Keep the series protagonist consistent: {series['protagonist_description']}. Preserve the declared world: {series['world_description']}. "
        f"Keep series style {config.style} ({style}) unchanged in every shot of this series. {event} Camera/action selection: {view}; pose: {pose_text}.{shot_clause}{pass_clause} "
        "Animate one clear causal event; vary camera position and action staging between acts, but never vary away from this TRY's nominated geometry/contact contract. No teleportation, extra limbs, invented handles, object topology changes, random crack origin, or resident injury. "
        "Do not generate subtitles, logos, letters, numbers or watermarks; exact method typography will be composited afterward as a designed 3D-poster ASS layer. "
        "Return a standalone clip, not a claimed verified three-minute movie. Video audit remains NOT_RUN until real frames are inspected."
    )


def make_keyframes(config: ImageConfig, route_id: str, loop_id: str, try_id: str) -> list[dict[str, Any]]:
    """Compile one corrected H2 master first, then reference-locked temporal derivatives."""
    stages = [
        ("KF1", "0.0s PRE_FAR", "H0", "the same rigid hammer is farther back along the established approach axis; a wide positive air gap remains, with no cracks, sparks or contact shadow"),
        ("KF2", "2.0s PRE_NEAR", "H1", "the same rigid hammer is only slightly farther back along the established approach axis; a small but clearly positive air gap remains, with no contact effects"),
        ("KF3", "4.5s CONTACT", "H2", "the corrected nominated terminal end face touches at P with zero gap and no interpenetration; first fine cracks originate at P only"),
        ("KF4", "7.0s MID_SHOCK", "H3", "the exact same rigid hammer follows through a small distance along the existing approach axis; cracks expand from the same P"),
        ("KF5", "10.0s END", "H3", "show the later aftermath from the same locked camera and hammer master; only the already-established crack propagation may advance from P"),
    ]
    series = STORY_SERIES[route_id]
    frames: list[dict[str, Any]] = []
    for frame_id, timestamp, contact_state, required_state in stages:
        is_master = frame_id == "KF3"
        if is_master:
            temporal_prompt = (
                "MASTER GENERATION ORDER 1 — correct the H2 middle frame first. Use the provided candidate H2 image as an image-edit source, "
                "not as loose inspiration. Correct only T-hammer topology and contact: exactly one rigid T-hammer, a straight crossbar and "
                "one straight handle attached at the crossbar midpoint at 90 degrees; only the nominated flat terminal face touches at P; "
                "zero gap and no interpenetration; first fine cracks start at P. Preserve the candidate camera, crop, lens perspective, world, "
                "character, grip, lighting, sphere and all background landmarks. Do not redesign, re-angle, reframe or change the weapon proportions. "
                "If the geometry cannot be corrected without changing the camera or hammer shape, stop for human review."
            )
            frame_status = "MID_CORRECTION_REQUIRED"
            parent_frame_id = None
            generation_order = 1
        else:
            direction = "rewind the exact same rigid hammer/connected grip along the existing approach axis" if frame_id in {"KF1", "KF2"} else "advance the exact same rigid hammer/connected grip along the established approach axis"
            temporal_prompt = (
                f"DERIVATIVE GENERATION — MUST use accepted KF3 H2 raster {loop_id}/{try_id} as the sole parent/reference image; do not generate this frame independently from text. "
                "Generation is blocked until the corrected H2 master has a SHA-bound HUMAN_ACCEPTED review receipt for terminal-face contact at P, zero gap, no interpenetration, correct T topology, and locked camera/hammer silhouette. "
                "Keep the master camera position/orientation, perspective, focal length, 16:9 crop, framing, horizon, sphere size/location, character identity, world landmarks, lighting direction, color grade, material, hand grip and T-hammer shape identical. "
                f"Only advance the temporal state: {direction} by the minimum physically plausible amount needed to show the requested state. "
                "Do not rotate the camera, zoom, reframe, alter the T crossbar or handle dimensions, create a new hammer, change the grip arbitrarily, or invent a second contact point. "
                "PRE frames must have a positive air gap and absolutely no contact effects. POST frames retain the same original contact point P and show only same-axis follow-through / crack progression. "
                "If camera or hammer-silhouette registration cannot be maintained, mark this derivative BLOCKED instead of inventing a replacement composition."
            )
            frame_status = "BLOCKED_UNTIL_KF3_H2_ACCEPTED"
            parent_frame_id = "KF3"
            generation_order = 2 if frame_id in {"KF1", "KF2"} else 3
        stage_contract = geometry_contract(config.geo_family, contact_state)
        prompt = (
            f"THE BOUNDARY WALKER, SERIES {route_id}, LOOP {loop_id}, TRY {try_id}; {frame_id} at {timestamp}. "
            f"Use this series' protagonist and world references, not a universal fixed heroine: {series['protagonist_description']}. "
            f"World bible: {series['world_description']}. Style {config.style}: {style_description(config.style)}. "
            f"Exact geometry: {GEO_DESCRIPTIONS[config.geo_family]}. State contract: {stage_contract}. "
            f"Required temporal state: {required_state}. Camera/action lock: {camera_text(config)}; pose: {pose_description(config)}. "
            f"{temporal_prompt} "
            "No lettering is generated in the raster; use the exact same canonical text payload from the TRY manifest for all frames and the video. "
            "Still-frame typography may use separate BEFORE / MIDDLE / AFTER material treatments after generation, but must not change any words or IDs. "
            "The video itself uses one stable VIDEO-LOCK typography treatment and one unchanged text-content SHA-256. "
            "This is a prompt package, not a claim that an image was generated or approved."
        )
        frames.append({
            "keyframe_id": frame_id,
            "timestamp": timestamp,
            "contact_state": contact_state,
            "generation_order": generation_order,
            "parent_keyframe_id": parent_frame_id,
            "is_h2_master": is_master,
            "requires_human_review_of_h2_master": not is_master,
            "typography_variant": {"KF1": "before", "KF2": "before", "KF3": "middle", "KF4": "after", "KF5": "after"}[frame_id],
            "text_content_sha256": label_text_sha256(art_label_spec(config, "V-02", route_id, loop_id, try_id, f"KEYFRAME-{frame_id}"), "3"),
            "status": frame_status,
            "prompt": prompt,
        })
    return frames

def mv_shot_specs(route_id: str) -> list[tuple[str, str, str, str]]:
    cards = SHOT_CARDS_26[:]
    is_52 = STORY_SERIES[route_id]["mv_shots"] == 52
    if not is_52:
        cards = [x for x in SHOT_CARDS_26 if x[0] != "3" or x[1] in {"MV_3_1_FRONT", "MV_3_2_LOW", "MV_3_3_PEAK", "MV_3_4_SIDE"}]
    # Routes other than MV52 use four cards per act (24 total); MV52 keeps the two ACT3 aftermath cards and adds a distinct second camera pass.
    specs: list[tuple[str, str, str, str]] = []
    for act, shot_id, shot_desc in cards:
        specs.append((act, shot_id, shot_desc, "A"))
        if is_52:
            specs.append((act, shot_id, shot_desc, "B"))
    expected = 52 if is_52 else 24
    if len(specs) != expected:
        raise AssertionError(f"{route_id} should contain {expected} prompts, got {len(specs)}")
    return specs


def make_mv_shots(config: ImageConfig, video_method: str, route_id: str,
                  loop_id: str, try_id: str) -> list[dict[str, str]]:
    specs = mv_shot_specs(route_id)
    output = []
    for index, (act, shot_id, description, camera_pass) in enumerate(specs, start=1):
        primary = act == "3"
        camera_override = f"story shot {shot_id}: {description}; camera pass {camera_pass}; action pose {pose_description(config)}"
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


def combo_key(config: ImageConfig, video_method: str, series_id: str) -> str:
    fields = asdict(config)
    series = STORY_SERIES[series_id]
    fields.update({"video_method": video_method, "series_id": series_id, "world_id": series["world_id"], "protagonist": series["protagonist_description"]})
    return json.dumps(fields, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def compile_product_matrix(catalog_csv: Path, outdir: Path, catalog_doc: Path,
                           start_index: int = 0, limit: int = 0) -> dict[str, Any]:
    rows, source_sha = load_catalog(catalog_csv)
    configs = build_image_configs(rows)
    if not STORY_SERIES:
        raise AssertionError("No story series registered")

    combos: list[tuple[str, ImageConfig, str, str]] = []
    for config in configs:
        # Only series with the matching visual style are eligible. A series' style/world/character
        # remain fixed across its six acts, while another series may change all of them.
        compatible_series = [sid for sid, series in STORY_SERIES.items() if series["style_id"] == config.style]
        for video_method in VIDEO_METHODS[config.geo_family]:
            for series_id in compatible_series:
                key = combo_key(config, video_method, series_id)
                digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
                combos.append((digest, config, video_method, series_id))
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
        "camera_pack", "camera", "wash", "windup", "pose_id", "shot", "style", "video_method",
        "series_id", "world_id", "world_name", "protagonist", "reference_catalog_ids",
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
        for sequence, (digest, config, video_method, series_id) in enumerate(selected, start=start_index + 1):
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
                    "image_prompt": make_image_prompt(config, video_method, series_id, loop_id, try_id, act, primary),
                    "video_prompt": make_video_prompt(config, video_method, series_id, loop_id, try_id, act, primary),
                    "primary_try": primary,
                })
            keyframes = make_keyframes(config, series_id, loop_id, try_id) if video_method == "V-02" else []
            mv_shots = make_mv_shots(config, video_method, series_id, loop_id, try_id) if video_method == "V-09" else []
            record = {
                "combination_id": combo_id,
                "loop_id": loop_id,
                "try_id": try_id,
                "sweep_id": "FULL-CROSS-PRODUCT-001",
                "axes": {
                    **asdict(config),
                    "video_method": video_method,
                    "series_id": series_id,
                    "series_label": STORY_SERIES[series_id]["label"],
                    "world_id": STORY_SERIES[series_id]["world_id"],
                    "world_name": STORY_SERIES[series_id]["world_name"],
                    "protagonist_description": STORY_SERIES[series_id]["protagonist_description"],
                    "story_hook": STORY_SERIES[series_id]["story_hook"],
                },
                "art_label_spec": art_label_spec(config, video_method, series_id, loop_id, try_id, combo_id),
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
                "series_id": series_id,
                "world_id": STORY_SERIES[series_id]["world_id"],
                "world_name": STORY_SERIES[series_id]["world_name"],
                "protagonist": STORY_SERIES[series_id]["protagonist_description"],
                "pose_id": config.pose_id,
                "reference_catalog_ids": config.geometry_catalog,
            })
            bucket_count[config.camera_pack] += 1
            geometry_count[config.geo_family] += 1
            video_count[video_method] += 1
            story_count[series_id] += 1
            media_prompt_count += len(acts) * 2
            keyframe_prompt_count += len(keyframes)
            mv_shot_count += len(mv_shots)
    summary = {
        "title": "THE BOUNDARY WALKER high-diversity style/world/character cross-product",
        "sweep_id": "FULL-CROSS-PRODUCT-001",
        "source_catalog_csv": str(catalog_csv),
        "source_catalog_csv_sha256": source_sha,
        "source_prompt_catalog": str(catalog_doc),
        "source_prompt_catalog_sha256": sha256_bytes(catalog_doc.read_bytes()),
        "source_variant_rows": len(rows),
        "image_geometry_camera_style_pose_configs": len(configs),
        "image_geometry_camera_style_pose_counts": dict(sorted(Counter(c.geo_family for c in configs).items())),
        "compatible_geometry_camera_style_pose_video_configs": sum(len(VIDEO_METHODS[c.geo_family]) for c in configs),
        "cross_product_combinations_after_style_matched_series": total if "total" in locals() else 0,
        "pose_factor": len(POSE_VARIANTS),
        "pose_variants": {key: value for key, value in POSE_DESCRIPTIONS.items()},
        "story_series_factor_total": len(STORY_SERIES),
        "story_series_per_style": dict(Counter(series["style_id"] for series in STORY_SERIES.values())),
        "story_series": {key: {"label": value["label"], "style_id": value["style_id"], "world_id": value["world_id"], "world_name": value["world_name"], "protagonist": value["protagonist_description"], "mv_shots_if_v09": value["mv_shots"]} for key, value in STORY_SERIES.items()},
        "full_cross_product_combinations": total,
        "compiled_start_index_zero_based": start_index,
        "compiled_combinations": len(selected),
        "full_product_compiled": start_index == 0 and len(selected) == total,
        "unique_combination_ids": len({combo[0] for combo in selected}),
        "all_combination_ids_unique": len({combo[0] for combo in selected}) == len(selected),
        "combo_counts_by_camera_pack": dict(sorted(bucket_count.items())),
        "combo_counts_by_geometry": dict(sorted(geometry_count.items())),
        "combo_counts_by_video_method": dict(sorted(video_count.items())),
        "combo_counts_by_story_series": dict(sorted(story_count.items())),
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
            "Each product row selects one geometry/contact state, one compatible camera/action pack, one of four poses, one style-locked world/character series, and one compatible video method.",
            "A series locks its style, world and protagonist across all six acts; other series may change style, world, protagonist, props and narrative treatment.",
            "Pose varies as an independent factor; character/body action may vary freely only outside the exact geometry/contact contract, which remains locked.",
            "Each six-act story uses visibly different camera/action profiles by act; the TRY method label is composited as a large 3D poster title and source/artwork SHA values are recorded in manifests.",
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
