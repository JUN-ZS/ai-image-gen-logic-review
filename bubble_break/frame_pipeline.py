#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compile image-followable keyframe prompts; this program does not render images."""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path
from typing import Any, Dict, List

VERSION = "1.0.0"
FRAME_IDS = ("H0", "H2", "H3")
FRAME_NAMES = {"H0":"H0_pre_impact", "H2":"H2_first_contact_anchor", "H3":"H3_post_impact"}
NEGATIVE_BASE = (
    "collage, diptych, triptych, storyboard sheet, contact sheet, multi-panel layout, infographic, "
    "labels, captions, typography, watermark, logo, diagram, weapon turntable, duplicate heroine, extra limbs, "
    "spear through sphere center, shaft touching shell, unintended side-wall contact, spikes, studs, mace, flail, chain, "
    "separate hammers in a ring, premature cracks, cracks away from contact point, explosion replacing shell, "
    "shards piercing residents, injured residents, destroyed city"
)
COMMON = (
    "ONE standalone cinematic frame, 16:9 widescreen, photorealistic live-action fantasy still. "
    "One full-bleed image, not a page, not a storyboard, not a comparison, not a collage. No writing, letters, "
    "labels, panel borders, inset images, diagrams or watermark. FIXED SHOT: low three-quarter frontal wide shot, "
    "35mm cinema lens, fixed tripod, same horizon, vanishing lines, architecture landmarks, camera distance, "
    "sphere center and scale in every frame. A giant transparent iridescent bubble encloses a visible floating city "
    "and tiny residents; the lower pole is unobstructed. Heroine stays in the lower-left third, bubble occupies "
    "upper/central frame, P is the exact six-o'clock bottom pole. Keep negative space around P so the gap/contact "
    "can be judged from pixels. ONE realistic East Asian female warrior, long straight center-parted dark-brown hair, "
    "natural makeup, expressive eyes, black leather combat outfit with straps and gloves, consistent face/costume, "
    "both hands on the same handle. No second heroine. CANONICAL WEAPON: ONE long rigid handle + ONE compact "
    "near-spherical dense steel hammer head. The head looks spherical because many broad, flat polygonal sledgehammer "
    "striking faces tile its surface and point radially outward. These are flat faces, not spikes, studs, blades, "
    "a halo, chain, or separate hammers. Keep several flat faces readable. At impact, only the single upper-facing "
    "flat polygon contacts the shell; its outline is visible, while head side walls and other faces remain lateral. "
    "The handle runs diagonally down-left toward the heroine, not through the bubble center like a spear. POWER CUES: "
    "planted wide stance, legs driving from ground, visible hip and torso rotation, shoulders accelerating into late "
    "arm extension, hair/clothing trailing the swing. Do not substitute raised arms or blur for force. Keep contact "
    "geometry sharp. The target is the containment membrane, never the residents; city and residents remain intact."
)

WEAPON_TEXT = {
    "RADIAL": (
        "WEAPON_TOPOLOGY_ID=WEAPON_C_RADIAL_SPHERE. ONE long rigid handle and ONE compact near-spherical dense steel hammer head. "
        "The head looks spherical because many broad, flat polygonal sledgehammer striking faces tile its surface and point radially outward. "
        "These are broad flat faces, not spikes, studs, blades, a halo, chain, or separate hammers. At impact, only the single upper-facing flat polygon contacts the shell."
    ),
    "T": (
        "WEAPON_TOPOLOGY_ID=WEAPON_T. ONE rigid hammer made from one straight horizontal rectangular crossbar and ONE long handle joined "
        "directly at the exact midpoint of the crossbar's underside. The handle itself is the only stem of the capital-T silhouette; "
        "there is no separate short post between head and handle. Crossbar width is about 3.8 times its thickness, with equal left/right ends; "
        "the handle joint is centered. The T silhouette must remain unmistakable. This is not a plus-sign/cross head, radial sphere, mace or spiked ball. "
        "At impact, only the broad upper plane of the horizontal crossbar contacts the exact bottom point P; its center is pinned to P. "
        "The handle can project diagonally down-left through 3D perspective, but its attachment must remain at the exact crossbar midpoint."
    ),
    "CROSS": (
        "WEAPON_TOPOLOGY_ID=WEAPON_PROXY_CROSS. ONE long rigid handle and ONE thick plus-sign/cross-shaped hammer head. "
        "The upper terminal face of the vertical arm is flat and is the only contact surface; its center is pinned to P. "
        "This is a geometry proxy only, not the final radial hammer."
    ),
}

NEGATIVE_BY_TOPOLOGY = {
    "RADIAL": (
        "T-shaped head, plus-sign/cross head, conventional plain rectangular single-bar hammer head, "
        "missing radial faces, rounded featureless ball"
    ),
    "T": (
        "radial spherical hammer head, near-spherical faceted globe head, plus-sign/cross head, X-shaped head, "
        "extra crossbar, missing horizontal crossbar, missing centered stem, off-center stem, bent or diagonal crossbar, "
        "L-shaped head, Y-shaped head, rounded head, separate head pieces"
    ),
    "CROSS": (
        "T-shaped head, radial spherical hammer head, near-spherical faceted globe head, conventional plain rectangular "
        "single-bar hammer head, missing horizontal arm, missing vertical arm"
    ),
}

def negative_for_weapon(topology: str) -> str:
    topology = topology.upper()
    if topology not in NEGATIVE_BY_TOPOLOGY:
        raise ValueError("weapon_topology must be RADIAL, T, or CROSS")
    return NEGATIVE_BASE + ", " + NEGATIVE_BY_TOPOLOGY[topology]


def common_for_weapon(topology: str) -> str:
    topology = topology.upper()
    if topology not in WEAPON_TEXT:
        raise ValueError("weapon_topology must be RADIAL, T, or CROSS")
    start = COMMON.index("CANONICAL WEAPON:")
    end = COMMON.index("POWER CUES:", start)
    return COMMON[:start] + WEAPON_TEXT[topology] + " The handle runs diagonally down-left toward the heroine. " + COMMON[end:]

STATE = {
"H0": (
    "PRE-IMPACT START FRAME. Bubble membrane perfectly intact: zero cracks, holes, fragments or explosion. Hammer "
    "is pulled back below and slightly left of P in a loaded diagonal backswing. Center of its upper-facing flat "
    "striking polygon aims at P, but a clearly visible continuous band of empty air separates that polygon from "
    "the bottom membrane. No contact, spark or pre-impact crack. Heroine's feet are grounded, knees flexed, hips "
    "and torso coiled, both hands gripping the handle at separated positions. The gap must not be hidden by glare, "
    "hair, ornament or the sphere."
),
"H2": (
    "EXACT FIRST-CONTACT ANCHOR. Show the single instant the upper-facing flat polygonal striking face on the "
    "spherical multi-face hammer head FIRST touches the exact six-o'clock bottom point P of the bubble. Center of "
    "this one flat face meets the shell; the face is square to the local tangent, its normal points upward into the "
    "bubble. Contact patch is unmistakable and unobstructed. Other flat faces and long side walls remain lateral "
    "and do not touch; shaft does not touch shell and stays diagonal down-left, not a spear through sphere center. "
    "Membrane was intact immediately before this instant. Only first tiny fractures now begin at P and radiate "
    "outward from that one contact center; no cracks elsewhere and sphere is not yet fully exploded. Show hip/torso "
    "rotation, both hands on handle, and lower-body response. No light effect may hide the striking face or P."
),
"H3": (
    "POST-IMPACT END FRAME, SAME CAMERA AND SCENE. No continuous unbroken membrane remains. Large iridescent film "
    "fragments and fine light-shards expand outward from the original six-o'clock point P along the original sphere "
    "envelope. Preserve sphere-center projection, P screen position, horizon, city landmarks, heroine identity, "
    "costume, weapon topology, handle length, head size and lighting. Same multi-face head has passed only slightly "
    "beyond P and visibly decelerated; handle, arms and torso continue in believable follow-through along the same "
    "swing path, feet/hips absorbing the reaction. Fragments flow away from residents, not through them. All residents "
    "remain alive and uninjured; city and supporting surfaces stay intact. No second explosion source, new crack "
    "origin, changed camera or text."
)}

T_STATE = {
    "H0": (
        "PRE-IMPACT START FRAME. Bubble membrane perfectly intact: zero cracks, holes, fragments or explosion. "
        "The weapon MUST have one unmistakable capital-T silhouette: exactly one straight horizontal rectangular crossbar "
        "and exactly one long rigid handle joined directly to the midpoint of its underside; the handle itself forms the "
        "single stem of the T. Do not add a separate short post between the crossbar and handle. The left and right bar ends "
        "are symmetric, equal and remain in one straight line. The head is a T, not a round object with facets and not a cross. "
        "The broad flat TOP PLANE "
        "of the horizontal crossbar is the designated striking surface; do not reinterpret a side wall as the striking face. "
        "This top plane aims at P but remains separated from the bubble's six-o'clock bottom point by a clearly visible "
        "continuous band of empty air. No contact, spark or pre-impact crack. Heroine's feet are grounded, knees flexed, "
        "hips and torso coiled, both hands gripping the handle at separated positions. The gap must not be hidden."
    ),
    "H2": (
        "EXACT FIRST-CONTACT ANCHOR. Keep one unmistakable capital-T hammer in the same shape as H0: one straight horizontal "
        "rectangular crossbar and the same single long handle joined directly beneath its midpoint; the handle itself forms "
        "the single stem of the T, with no separate short post or extra shaft. "
        "The broad flat TOP PLANE on the crossbar FIRST touches the exact six-o'clock bottom point P of the bubble. "
        "The center of that upper plane is pinned to P; its normal points upward into the bubble. This topology uses the "
        "crossbar's upper plane as its active striking surface; do not rotate the head, substitute an end-side face, or "
        "change the T into a sphere. The left and right crossbar ends remain symmetric and visibly horizontal; the centered "
        "stem remains attached and readable. The contact patch is unmistakable and unobstructed; the handle and side walls "
        "do not touch first. The membrane was intact immediately before contact. Only first tiny fractures now begin at P "
        "and radiate outward from that one contact center; no cracks elsewhere and the sphere is not yet fully exploded. "
        "Show hip/torso rotation, both hands on the handle, and lower-body response. No light effect may hide the face or P."
    ),
    "H3": (
        "POST-IMPACT END FRAME, SAME CAMERA AND SCENE. No continuous unbroken membrane remains. Large iridescent film "
        "fragments and fine light-shards expand outward from the original six-o'clock point P along the original sphere "
        "envelope. Preserve sphere-center projection, P screen position, horizon, city landmarks, heroine identity, costume, "
        "handle length, camera and lighting. Preserve the EXACT same T topology: a straight horizontal rectangular crossbar "
        "with two symmetric ends and the same single long handle attached directly at the underside midpoint; the handle is the T's "
        "only stem. Do not introduce a separate stub or second shaft. The hammer head must not become spherical, radial-faceted, "
        "cross-shaped, L-shaped or multi-headed "
        "during follow-through. The same T head has passed only slightly beyond P and visibly decelerated; handle, arms and "
        "torso continue in believable follow-through along the same swing path, feet/hips absorbing the reaction. Fragments "
        "flow away from residents, not through them. All residents remain alive and uninjured; city and supporting surfaces "
        "stay intact. No second explosion source, new crack origin, changed camera or text."
    ),
}

CROSS_STATE = {
    "H0": (
        "PRE-IMPACT START FRAME. Bubble membrane perfectly intact: zero cracks, holes, fragments or explosion. "
        "The weapon head is one rigid plus-sign cross made from one vertical rectangular arm and one horizontal rectangular "
        "arm crossing at their centers; all four arms are connected and clearly visible. One long handle is attached to "
        "the center. The upper terminal face of the vertical arm aims at P but remains separated from the bubble by a "
        "clearly visible band of empty air. No contact, spark or pre-impact crack. Heroine's feet are grounded, knees flexed, "
        "hips and torso coiled, both hands gripping the handle at separated positions. The gap must not be hidden."
    ),
    "H2": (
        "EXACT FIRST-CONTACT ANCHOR. The same single rigid plus-sign cross head FIRST touches the exact six-o'clock bottom "
        "point P using only the flat upper terminal face at the top of its vertical arm. The arm's face center is pinned to P "
        "and its normal points upward into the bubble. The horizontal crossbar remains centered and visibly connected; the "
        "head must not become a sphere or an ordinary single rectangular hammer. No other arm, side wall or shaft touches first. "
        "The membrane was intact immediately before contact. Only first tiny fractures now begin at P and radiate outward from "
        "that one contact center; no cracks elsewhere and the sphere is not yet fully exploded. Show hip/torso rotation and "
        "both hands on the handle. No effect may hide the contact face or P."
    ),
    "H3": (
        "POST-IMPACT END FRAME, SAME CAMERA AND SCENE. No continuous unbroken membrane remains. Fragments expand outward "
        "from the original six-o'clock point P. Preserve camera, scene, heroine, handle, and the same connected plus-sign head: "
        "one vertical rectangular arm and one horizontal rectangular arm crossing at their centers. The hammer head must not "
        "become spherical, a T, or a conventional single rectangular block. Same swing path and believable deceleration. "
        "All residents remain alive and uninjured; city and supporting surfaces stay intact. No second explosion source, "
        "new crack origin, changed camera or text."
    ),
}

STATE_BY_TOPOLOGY = {
    "RADIAL": STATE,
    "T": T_STATE,
    "CROSS": CROSS_STATE,
}

def axis_text(record: Dict[str, Any], key: str, fallback: str) -> str:
    axes = record.get("axes", {})
    value = axes.get(key, {}) if isinstance(axes, dict) else {}
    if isinstance(value, dict):
        desc, ident = value.get("description"), value.get("id")
        if desc and ident: return f"{ident}: {desc}"
        if desc: return str(desc)
    return fallback

def safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("._")[:100] or "story"

FRAME_PROJECTION = {
    "canvas": {"width": 1920, "height": 1080},
    "camera_id": "LOCKED_LOW_THREE_QUARTER_35MM",
    "sphere_center": {"x": 1090, "y": 330},
    "sphere_radius": 280,
    "P_six_oclock": {"x": 1090, "y": 610},
    "heroine_anchor": {"x": 610, "y": 790},
    "hammer_head_radius": 80,
    "frames": {
        "H0": {"head_center": {"x": 1090, "y": 740}, "top_face_y": 660,
               "gap_px": 50, "state": "intact_preimpact"},
        "H2": {"head_center": {"x": 1090, "y": 690}, "top_face_y": 610,
               "gap_px": 0, "state": "first_contact"},
        "H3": {"head_center": {"x": 1090, "y": 675}, "top_face_y": 595,
               "gap_px": -15, "state": "postimpact_followthrough"},
    },
}

def _polygon(points: List[tuple], fill: str, stroke: str = "#182b42", width: int = 4) -> str:
    pts = " ".join(f"{x},{y}" for x, y in points)
    return f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linejoin="round"/>'

def _line(x1: int, y1: int, x2: int, y2: int, color: str, width: int = 8) -> str:
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>'

def _svg_frame(frame_id: str, weapon_topology: str = "RADIAL") -> str:
    """Draw a deterministic, label-free 2D camera blockout. It is not a final artwork."""
    width, height = 1920, 1080
    cx, cy, radius = 1090, 330, 280
    px, py = 1090, 610
    geo = FRAME_PROJECTION["frames"][frame_id]
    hx, hy = geo["head_center"]["x"], geo["head_center"]["y"]
    top_y = geo["top_face_y"]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" data-contact-p="{FRAME_PROJECTION["P_six_oclock"]["x"]},{FRAME_PROJECTION["P_six_oclock"]["y"]}" data-frame="{frame_id}">',
        '<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#102b4a"/><stop offset="1" stop-color="#050b18"/></linearGradient>',
        '<radialGradient id="membrane"><stop offset="0" stop-color="#9eeaff" stop-opacity=".08"/><stop offset=".8" stop-color="#5ad7ff" stop-opacity=".10"/><stop offset="1" stop-color="#d5faff" stop-opacity=".28"/></radialGradient>',
        '<linearGradient id="shaft" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#b0c3d4"/><stop offset=".45" stop-color="#23334c"/><stop offset="1" stop-color="#d4a75e"/></linearGradient>',
        f'<clipPath id="bubbleClip"><circle cx="{cx}" cy="{cy}" r="{radius}"/></clipPath></defs>',
        '<rect width="1920" height="1080" fill="url(#sky)"/>',
        '<path d="M0 860 L170 790 L260 832 L390 760 L520 845 L700 795 L860 860 L1080 800 L1260 842 L1440 760 L1630 825 L1780 780 L1920 830 L1920 1080 L0 1080 Z" fill="#0c1727" stroke="#203a55" stroke-width="4"/>',
        '<path d="M0 1000 L1920 1000" stroke="#25425c" stroke-width="4"/>',
    ]
    # Stable distant skyline outside the bubble.
    for x, y, bw, bh in [(40,760,80,190),(150,720,95,230),(275,795,70,155),(1360,770,90,180),(1480,710,110,240),(1635,780,70,170),(1745,735,110,215)]:
        parts.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" fill="#17283b" stroke="#39516a" stroke-width="3"/>')
        for wy in range(y+20,y+bh-15,35):
            parts.append(f'<path d="M{x+14} {wy} h{bw-28}" stroke="#5e8ba4" stroke-opacity=".55" stroke-width="3"/>')
    # City remains in the same spherical volume for all three states.
    parts += [
        '<g clip-path="url(#bubbleClip)">',
        f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="url(#membrane)"/>',
        '<path d="M790 520 L850 450 L900 500 L970 390 L1030 475 L1105 410 L1160 470 L1220 390 L1300 500 L1380 455 L1400 650 L780 650 Z" fill="#294761" fill-opacity=".82" stroke="#83d9ed" stroke-opacity=".45" stroke-width="3"/>',
        '<path d="M800 560 L880 530 L920 570 L980 515 L1050 560 L1120 500 L1180 555 L1260 510 L1360 570 L1390 650 L790 650 Z" fill="#0d2b44" fill-opacity=".80"/>',
    ]
    for x,y,bw,bh in [(845,470,46,165),(915,505,58,130),(1000,435,50,205),(1060,486,55,155),(1142,452,48,190),(1205,490,60,150),(1290,430,48,210)]:
        parts.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" fill="#365b75" stroke="#a1d9e6" stroke-opacity=".7" stroke-width="3"/>')
        for wy in range(y+25,y+bh-12,31):
            parts.append(f'<rect x="{x+12}" y="{wy}" width="{bw-24}" height="8" fill="#ffdca0" fill-opacity=".75"/>')
    # Residents: simple intact human silhouettes, fixed well away from P.
    for x,y in [(930,555),(985,570),(1168,560),(1224,548),(1032,595)]:
        parts.append(f'<circle cx="{x}" cy="{y}" r="7" fill="#ffe3a6"/>')
        parts.append(_line(x,y+8,x,y+25,"#ffe3a6",5))
        parts.append(_line(x,y+14,x-8,y+20,"#ffe3a6",3))
        parts.append(_line(x,y+14,x+8,y+20,"#ffe3a6",3))
    parts.append('</g>')
    if frame_id in ("H0","H2"):
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="#b5f3ff" stroke-width="9"/>')
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{radius-11}" fill="none" stroke="#7bd7ff" stroke-opacity=".55" stroke-width="2"/>')
    else:
        # Only broken fragments remain; a faint broken arc indicates the previous envelope.
        parts.append(f'<path d="M{cx-radius+30} {cy-70} A{radius} {radius} 0 0 1 {cx+radius-15} {cy-35}" fill="none" stroke="#91e9ff" stroke-opacity=".35" stroke-width="8" stroke-dasharray="36 28"/>')
        parts.append(f'<path d="M{cx-radius+50} {cy+50} A{radius} {radius} 0 0 0 {cx-50} {py-8}" fill="none" stroke="#91e9ff" stroke-opacity=".30" stroke-width="8" stroke-dasharray="22 25"/>')
    if frame_id == "H2":
        # Every crack begins at the exact P coordinate.
        parts += [
            f'<path d="M{px} {py} Q1050 565 1025 520 Q1000 482 970 458" fill="none" stroke="#ffffff" stroke-width="6"/>',
            f'<path d="M{px} {py} Q1125 566 1155 525 Q1180 490 1215 467" fill="none" stroke="#ffffff" stroke-width="6"/>',
            f'<path d="M{px} {py} Q1085 560 1072 515 Q1065 475 1068 445" fill="none" stroke="#b7f2ff" stroke-width="4"/>',
            f'<path d="M{px} {py} Q1140 575 1190 560 Q1235 550 1260 520" fill="none" stroke="#b7f2ff" stroke-width="4"/>',
        ]
    if frame_id == "H3":
        # Fragments travel away from P; no fragment intersects the residents' region.
        fragments = [
            [(1042,590),(1060,555),(1080,577),(1070,610)],
            [(1102,578),(1120,545),(1140,565),(1128,600)],
            [(1010,572),(1025,535),(1043,555),(1034,586)],
            [(1150,570),(1172,530),(1193,550),(1177,582)],
            [(990,545),(1002,515),(1022,530),(1018,557)],
            [(1196,535),(1212,500),(1236,518),(1220,548)],
            [(1058,518),(1070,485),(1087,500),(1080,535)],
            [(1134,500),(1155,470),(1172,488),(1156,518)],
            [(970,500),(985,470),(1003,486),(990,510)],
            [(1230,488),(1250,455),(1268,475),(1250,500)],
        ]
        colors=["#8de9ff","#f7c9ff","#ffd58a","#a9caff"]
        for i,poly in enumerate(fragments):
            parts.append(_polygon(poly,colors[i%len(colors)],"#e4fbff",3))
        parts.append(f'<path d="M{px} {py} L1065 573 L1040 545" stroke="#ffffff" stroke-opacity=".8" stroke-width="3" fill="none"/>')
        parts.append(f'<path d="M{px} {py} L1122 570 L1150 540" stroke="#ffffff" stroke-opacity=".8" stroke-width="3" fill="none"/>')
    # Hammer shaft: one diagonal, rigid handle, never a spear through the sphere centre.
    handle_end=(690,920)
    weapon_topology=weapon_topology.upper()
    head_attach=(hx,top_y+58) if weapon_topology=="T" else (hx-42,hy+40)
    parts.append(_line(handle_end[0],handle_end[1],head_attach[0],head_attach[1],"#050a11",32))
    parts.append(_line(handle_end[0],handle_end[1],head_attach[0],head_attach[1],"url(#shaft)",21))
    for gx,gy in [(760,890),(820,866)]:
        parts.append(f'<ellipse cx="{gx}" cy="{gy}" rx="18" ry="13" transform="rotate(-20 {gx} {gy})" fill="#c89c69" stroke="#ffe0a6" stroke-width="4"/>')
    if weapon_topology == "T":
        # One straight crossbar; the single long handle attaches at its underside midpoint and forms the T stem.
        parts.append(_polygon([(hx-112,top_y+8),(hx+112,top_y+8),(hx+112,top_y+58),(hx-112,top_y+58)],
                              "#203d56","#e0c18a",6))
        parts.append(_polygon([(hx-112,top_y),(hx+112,top_y),(hx+96,top_y+8),(hx-96,top_y+8)],
                              "#6b9cbd","#fff0bf",4))
    elif weapon_topology == "CROSS":
        parts.append(_polygon([(hx-30,top_y),(hx+30,top_y),(hx+30,hy+85),(hx-30,hy+85)],
                              "#203d56","#e0c18a",5))
        parts.append(_polygon([(hx-100,hy-30),(hx+100,hy-30),(hx+100,hy+30),(hx-100,hy+30)],
                              "#203d56","#e0c18a",5))
        parts.append(_line(hx-28,top_y,hx+28,top_y,"#fff0bf",5))
    elif weapon_topology == "RADIAL":
        # Approximate a many-flat-face radial head while retaining one broad top contact face.
        ring=[(hx-34,top_y),(hx+34,top_y),(hx+68,top_y+24),(hx+80,hy+6),
              (hx+52,hy+61),(hx,hy+80),(hx-52,hy+61),(hx-80,hy+6),(hx-68,top_y+24)]
        center=(hx,hy+6)
        parts.append(_polygon(ring,"#15283b","#d7b478",7))
        fills=["#294d6b","#101d30","#34536a","#172638"]
        for i in range(len(ring)):
            parts.append(_polygon([ring[i],ring[(i+1)%len(ring)],center],fills[i%len(fills)],"#7ba3bd",2))
        parts.append(_polygon([(hx-34,top_y),(hx+34,top_y),(hx+28,top_y+18),(hx,top_y+24),(hx-28,top_y+18)],
                              "#5e8eaf","#fff0bf",5))
    else:
        raise ValueError("weapon_topology must be RADIAL, T, or CROSS")
    # Simple heroine blockout; pose changes slightly with the event, but camera/landmarks stay fixed.
    if frame_id=="H0":
        headx,heady,shoulderx,shouldery,hipx,hipy=560,704,616,757,646,830
    elif frame_id=="H2":
        headx,heady,shoulderx,shouldery,hipx,hipy=575,700,638,755,665,826
    else:
        headx,heady,shoulderx,shouldery,hipx,hipy=590,698,658,752,684,818
    parts.append(f'<path d="M{headx-27} {heady-5} Q{headx-44} {heady-48} {headx-10} {heady-54} Q{headx+31} {heady-58} {headx+30} {heady-7} L{headx+17} {heady+24} L{headx-27} {heady+15} Z" fill="#111a29" stroke="#6f97ae" stroke-width="4"/>')
    parts.append(f'<ellipse cx="{headx}" cy="{heady}" rx="25" ry="31" fill="#e0b48f" stroke="#ffd8b0" stroke-width="3"/>')
    parts.append(f'<path d="M{headx-24} {heady-12} Q{headx-8} {heady-52} {headx+23} {heady-25} L{headx+30} {heady+30} L{headx+13} {heady+48} L{headx+7} {heady+10} Z" fill="#171a26"/>')
    torso=[(shoulderx-24,shouldery-8),(shoulderx+25,shouldery-12),(hipx+25,hipy+10),(hipx-23,hipy+12)]
    parts.append(_polygon(torso,"#151d2b","#8393a3",5))
    parts.append(_line(shoulderx-13,shouldery,hipx-10,hipy,"#c8a066",4))
    # arms extend to two grip points on the same handle
    parts.append(_line(shoulderx+12,shouldery+5,760,890,"#e0b48f",18))
    parts.append(_line(shoulderx+18,shouldery+12,820,866,"#e0b48f",18))
    # legs and boots in an offset, braced stance
    parts.append(_line(hipx-12,hipy+6,headx-35,976,"#101722",30))
    parts.append(_line(hipx+18,hipy+6,headx+100,966,"#101722",30))
    parts.append(_line(headx-53,977,headx-11,977,"#b6c8d8",17))
    parts.append(_line(headx+76,966,headx+123,966,"#b6c8d8",17))
    # Only the contact frame gets an impact glint; H0 must remain visually pre-contact.
    if frame_id == "H2":
        parts.append(f'<circle cx="{px}" cy="{py}" r="9" fill="#ffffff" fill-opacity=".95"/>')
        parts.append(f'<circle cx="{px}" cy="{py}" r="22" fill="none" stroke="#9deaff" stroke-width="3" stroke-opacity=".7"/>')
    parts.append("</svg>")
    return "\n".join(parts)

def projection_lock() -> Dict[str, Any]:
    return json.loads(json.dumps(FRAME_PROJECTION))

def compile_frame_set(record: Dict[str, Any], weapon_topology: str = "RADIAL") -> Dict[str, Any]:
    weapon_topology = weapon_topology.upper()
    common = common_for_weapon(weapon_topology)
    story_id = str(record.get("story_id") or "STORY-UNKNOWN")
    scene = axis_text(record, "environment", "a monumental surreal city plaza")
    scale = axis_text(record, "scale", "a giant bubble enclosing a floating city")
    shell = axis_text(record, "shell", "transparent iridescent membrane")
    palette = axis_text(record, "palette", "cold silver, electric cyan, restrained amber")
    lock = {
        "version": VERSION, "story_id": story_id, "scene": scene, "scale": scale, "shell": shell,
        "palette": palette, "weapon": {"RADIAL":"WEAPON_C_RADIAL_SPHERE","T":"WEAPON_T","CROSS":"WEAPON_PROXY_CROSS"}[weapon_topology], "camera": "locked low 3/4 35mm",
        "contact": "exact six-o'clock bottom pole P"
    }
    shot_id = "SHOT-" + hashlib.sha256(json.dumps(lock,sort_keys=True,ensure_ascii=False).encode()).hexdigest()[:12].upper()
    narrative = (
        f"Story kernel shown only through visible objects, never printed text: {record.get('root_sin','unassigned')}. "
        f"Mechanism: {record.get('root_mechanism','coercive containment')}. "
        f"Human cost: {record.get('human_cost','loss of meaningful choice')}. "
        f"Scene: {scene}. Scale: {scale}. Shell: {shell}. Palette: {palette}. "
    )
    prompts = {fid: common + "\n\nSHOT LOCK ID (metadata only; do not render as text): " + shot_id + ".\n"
               + narrative + STATE_BY_TOPOLOGY[weapon_topology][fid] + "\nUse visible silhouette, position, overlap, gap/contact and fragment direction; "
               "no labels, arrows, formulas or diagrams.\nNEGATIVE PROMPT: " + negative_for_weapon(weapon_topology) for fid in FRAME_IDS}
    errors=[]
    checks = [
        ("H0","clearly visible continuous band of empty air"),
        ("H2","FIRST touches the exact six-o'clock bottom point P"),
        ("H2","radiate outward from that one contact center"),
        ("H3","No continuous unbroken membrane remains"),
        ("H3","All residents remain alive and uninjured"),
    ]
    for fid,token in checks:
        if token not in prompts[fid]: errors.append(f"{fid}: missing {token}")
    if weapon_topology == "T":
        for fid in FRAME_IDS:
            positive = prompts[fid].split("NEGATIVE PROMPT:", 1)[0]
            if "spherical multi-face hammer head" in positive or "polygonal sledgehammer" in positive:
                errors.append(f"{fid}: T topology conflicts with radial-head wording")
            if "horizontal rectangular crossbar" not in positive or "centered" not in positive:
                errors.append(f"{fid}: T silhouette lock is incomplete")
    shape_check = {
        "RADIAL": "一柄一頭；近球形槌頭由多向寬扁平槌面構成，不是刺球或普通長方槌",
        "T": "一柄一頭；單一水平直橫杠 + 橫杠中點下方唯一中央直柄／短頸，兩端對稱，禁止球形／十字／L形漂移",
        "CROSS": "一柄一頭；單一連體加號頭，水平臂與垂直臂穿過同一中心，不是 T 或球形槌頭",
    }[weapon_topology]
    face_check = {
        "RADIAL": "H0 保持間隙；H2 只有一塊向上的扁平多面槌面首次接觸 P",
        "T": "H0 保持間隙；H2 只有 T 橫杠的寬扁平上平面首次接觸 P，橫杠及中央柄保持 T 輪廓",
        "CROSS": "H0 保持間隙；H2 只有加號頭垂直臂最上端的平面首次接觸 P",
    }[weapon_topology]
    visual_checks=[
        ("V01","每張都是單張成片，不是拼貼／分格／資訊圖"),
        ("V02","H0/H2/H3 鏡位、地平線、地標、球心及 P 投影位置一致"),
        ("V03","女主臉、服裝一致，且只有一位女主"),
        ("V04",shape_check),
        ("V05","H0 球膜完整無裂，指定接觸面與 P 之間有空隙"),
        ("V06",face_check),
        ("V07","首裂只從 P 起始向外傳播"),
        ("V08","H3 球膜已解體，碎片對應原球面並從 P 向外分佈"),
        ("V09","雙手、寬站、腿、髖、軀幹、肩臂形成可讀動力鏈與跟進"),
        ("V10","居民與承載面無傷；碎片遠離居民"),
    ]
    return {
        "pipeline_version":VERSION,"story_id":story_id,"shot_lock_id":shot_id,
        "canonical_weapon":{"RADIAL":"WEAPON_C_RADIAL_SPHERE","T":"WEAPON_T","CROSS":"WEAPON_PROXY_CROSS"}[weapon_topology],
        "weapon_topology":weapon_topology,
        "weapon_shape_contract":{
            "RADIAL":"one handle + one near-spherical multi-face head",
            "T":"one straight horizontal crossbar + one long handle joined at its underside midpoint; the handle itself is the only stem; no separate post, spherical head or cross-head substitution",
            "CROSS":"one connected plus-sign head with one horizontal and one vertical rectangular arm",
        }[weapon_topology],
        "active_striking_surface":{
            "RADIAL":"one upward-facing flat polygon on the radial head",
            "T":"the broad upper plane of the horizontal crossbar",
            "CROSS":"the upper terminal face of the vertical arm",
        }[weapon_topology],
        "frame_order":list(FRAME_IDS),
        "projection_lock":projection_lock(),
        "workflow":{"endpoint_frames":["H0","H3"],"contact_validation_anchor":"H2",
          "generation_policy":"Generate each frame as a separate single image; never request all frames on one canvas.",
          "continuity_warning":"Shared prompts do not guarantee identical pixels; independently generated endpoints can drift. Review actual images before interpolation."},
        "prompts":prompts,"prompt_contract_status":"PROMPT_CONTRACT_PASS" if not errors else "BLOCK",
        "prompt_contract_errors":errors,"image_realization":"NOT_RUN","pixel_audit_status":"NOT_RUN",
        "pixel_audit_checks":[{"id":i,"criterion":c,"result":"UNASSESSED"} for i,c in visual_checks]
    }

def write_packet(packet: Dict[str, Any], outdir: Path) -> Dict[str, Any]:
    story_dir=outdir/safe_name(packet["story_id"]); story_dir.mkdir(parents=True,exist_ok=True)
    names={}
    for fid in FRAME_IDS:
        name=FRAME_NAMES[fid]+".txt"; (story_dir/name).write_text(packet["prompts"][fid]+"\n",encoding="utf-8"); names[fid]=name
    geometry_names={}
    for fid in FRAME_IDS:
        svg_name=FRAME_NAMES[fid]+"_geometry.svg"
        (story_dir/svg_name).write_text(_svg_frame(fid,packet.get("weapon_topology","RADIAL"))+"\n",encoding="utf-8")
        geometry_names[fid]=svg_name
    layout={"shot_lock_id":packet["shot_lock_id"],"projection_lock":packet["projection_lock"],
            "frame_order":list(FRAME_IDS),"geometry_files":geometry_names,
            "note":"Deterministic 2D geometry blockout/reference only; not a photorealistic rendered frame."}
    (story_dir/"layout.json").write_text(json.dumps(layout,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    manifest=dict(packet); manifest["prompt_files"]=names; manifest["geometry_files"]=geometry_names
    manifest["layout_file"]="layout.json"
    (story_dir/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    lines=[f"# Pixel audit — {packet['story_id']}","",f"Shot lock: {packet['shot_lock_id']}",
           f"Prompt contract: {packet['prompt_contract_status']}","Image realization: NOT_RUN","Pixel audit: NOT_RUN","",
           "Only mark PASS/FAIL after reviewing actual H0/H2/H3 images side by side. Prompt text is not pixel evidence.","",
           "| ID | Visual criterion | Result |","|---|---|---|"]
    lines.extend(f"| {x['id']} | {x['criterion']} | UNASSESSED |" for x in packet["pixel_audit_checks"])
    (story_dir/"pixel_audit.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    return {"story_id":packet["story_id"],"shot_lock_id":packet["shot_lock_id"],
            "prompt_contract_status":packet["prompt_contract_status"],"image_realization":"NOT_RUN",
            "pixel_audit_status":"NOT_RUN","directory":str(story_dir)}

def build_packets(input_path: Path, outdir: Path, limit: int=1, story_id_filter: str|None=None,
                  weapon_topology: str = "RADIAL") -> Dict[str, Any]:
    if limit < 1: raise ValueError("--limit must be >= 1")
    summaries=[]
    with input_path.open("r",encoding="utf-8") as handle:
        for line in handle:
            if not line.strip(): continue
            record=json.loads(line)
            if story_id_filter and record.get("story_id") != story_id_filter: continue
            summaries.append(write_packet(compile_frame_set(record,weapon_topology),outdir))
            if len(summaries)>=limit: break
    if not summaries: raise ValueError("no story records selected from input JSONL")
    batch={"pipeline_version":VERSION,"input":str(input_path),"requested_limit":limit,
           "weapon_topology":weapon_topology.upper(),
           "written_story_packets":len(summaries),"image_realization":"NOT_RUN",
           "pixel_audit_status":"NOT_RUN","packets":summaries}
    outdir.mkdir(parents=True,exist_ok=True)
    (outdir/"batch_manifest.json").write_text(json.dumps(batch,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return batch

def main(argv: List[str]|None=None) -> int:
    parser=argparse.ArgumentParser(description="Compile separate H0/H2/H3 prompts; does not render images.")
    parser.add_argument("--input",required=True,help="story JSONL from bubble_break/generate.py")
    parser.add_argument("--outdir",required=True,help="directory for prompts and pixel-audit packet")
    parser.add_argument("--limit",type=int,default=1,help="maximum story packets; default 1")
    parser.add_argument("--story-id",default=None,help="select one exact story_id")
    parser.add_argument("--weapon-topology",choices=("RADIAL","T","CROSS"),default="RADIAL")
    args=parser.parse_args(argv)
    try: batch=build_packets(Path(args.input),Path(args.outdir),args.limit,args.story_id,args.weapon_topology)
    except (OSError,ValueError,json.JSONDecodeError) as exc:
        print(f"BLOCK: {exc}",file=sys.stderr); return 2
    print(json.dumps({"written_story_packets":batch["written_story_packets"],
      "image_realization":batch["image_realization"],"pixel_audit_status":batch["pixel_audit_status"],
      "manifest":str(Path(args.outdir)/"batch_manifest.json")},ensure_ascii=False,indent=2),file=sys.stderr)
    return 0

if __name__=="__main__": raise SystemExit(main())
