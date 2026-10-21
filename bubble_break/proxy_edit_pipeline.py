#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cross-to-cross contact proxy and target-only sphere edit instructions.

The SVG geometry is deterministic. Pixel fidelity after an external AI edit is not.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

def rect(x, y, w, h, fill, stroke="#dcecff", sw=3):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'

def line(x1, y1, x2, y2, color, sw):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}" stroke-linecap="square"/>'

def svg_base(width, height):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#142d47"/><stop offset="1" stop-color="#060c16"/></linearGradient>',
        '<linearGradient id="metal" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#dbe9f5"/><stop offset=".5" stop-color="#486783"/><stop offset="1" stop-color="#18283a"/></linearGradient>',
        '<radialGradient id="membrane"><stop offset=".78" stop-color="#5dd7ff" stop-opacity=".02"/><stop offset=".96" stop-color="#81e7ff" stop-opacity=".12"/><stop offset="1" stop-color="#d8fbff" stop-opacity=".65"/></radialGradient></defs>',
        f'<rect width="{width}" height="{height}" fill="url(#bg)"/>',
        '<path d="M0 890 L260 800 L440 855 L680 775 L900 855 L1120 790 L1360 850 L1600 770 L1920 860 L1920 1080 L0 1080 Z" fill="#0c1928" stroke="#294761" stroke-width="4"/>',
    ]

def target_plus(cx, cy, r, thickness=44):
    # The target cross center is C; its bottom terminal face is P=(cx, cy+r).
    return "".join([
        rect(cx-thickness/2, cy-r, thickness, 2*r, "#ad783d", "#ffe0a3", 4),
        rect(cx-r, cy-thickness/2, 2*r, thickness, "#ad783d", "#ffe0a3", 4),
        rect(cx-thickness/2-2, cy+r-3, thickness+4, 6, "#fff0bd", "#ffffff", 2),
    ])

def attacker_plus(cx, face_y, center_y, handle_end):
    shaft = line(handle_end[0], handle_end[1], cx, center_y, "#02060a", 34)
    shaft += line(handle_end[0], handle_end[1], cx, center_y, "url(#metal)", 23)
    head = rect(cx-30, face_y, 60, center_y+95-face_y, "#234761", "#e0bd82", 5)
    head += rect(cx-100, center_y-30, 200, 60, "#234761", "#e0bd82", 5)
    head += rect(cx-30, face_y-2, 60, 5, "#fff1c7", "#ffffff", 2)
    head += line(cx-25, face_y+9, cx+25, face_y+9, "#8be7ff", 3)
    return shaft + head

def attacker_t(cx, face_y, center_y, handle_end):
    # Orthographic projection of one rigid T rotated 90 degrees: end-face normal and
    # crossbar axis point up-screen, so the centered handle projects horizontally.
    # This SVG is only a schematic coordinate proxy, not 3D or pixel-proof evidence.
    bar_width = 58
    bar_length = 224
    head_joint_y = face_y + bar_length // 2
    handle_end = (cx - 440, head_joint_y)
    shaft = line(handle_end[0], handle_end[1], cx, head_joint_y, "#02060a", 34)
    shaft += line(handle_end[0], handle_end[1], cx, head_joint_y, "url(#metal)", 23)
    head = rect(cx-bar_width//2, face_y+8, bar_width, bar_length-8, "#234761", "#e0bd82", 5)
    # The complete terminal END FACE is the horizontal top cap at face_y, not a side strip.
    head += rect(cx-bar_width//2, face_y, bar_width, 8, "#6b9cbd", "#fff0bf", 3)
    return shaft + head

def attacker_radial(cx, face_y, center_y, handle_end):
    shaft = line(handle_end[0], handle_end[1], cx, center_y, "#02060a", 34)
    shaft += line(handle_end[0], handle_end[1], cx, center_y, "url(#metal)", 23)
    # A compact, faceted head with a broad flat upper face—not spikes or a mace.
    points=[(cx-34,face_y),(cx+34,face_y),(cx+68,face_y+24),(cx+80,center_y+6),
            (cx+52,center_y+61),(cx,center_y+80),(cx-52,center_y+61),
            (cx-80,center_y+6),(cx-68,face_y+24)]
    p=" ".join(f"{x},{y}" for x,y in points)
    head=f'<polygon points="{p}" fill="#234761" stroke="#e0bd82" stroke-width="5" stroke-linejoin="round"/>'
    head+=rect(cx-34,face_y,68,5,"#fff1c7","#ffffff",2)
    for x1,y1,x2,y2 in [(cx-34,face_y,cx,center_y+6),(cx+34,face_y,cx,center_y+6),
                         (cx+68,face_y+24,cx,center_y+6),(cx+52,center_y+61,cx,center_y+6),
                         (cx-52,center_y+61,cx,center_y+6),(cx-68,face_y+24,cx,center_y+6)]:
        head+=line(x1,y1,x2,y2,"#81a9c4",2)
    return shaft+head

def build_t_silhouette_reference_svg():
    """Clean, label-free silhouette reference: one crossbar and the same single handle as its stem."""
    width, height = 1000, 900
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="1000" height="900" fill="#f3f5f7"/>',
        '<rect x="300" y="150" width="400" height="105" fill="#263746" stroke="#111a23" stroke-width="8"/>',
        # This is the single handle, directly centered on and attached to the underside of the crossbar.
        '<rect x="465" y="255" width="70" height="520" fill="#334f65" stroke="#111a23" stroke-width="8"/>',
        '<rect x="307" y="158" width="386" height="16" fill="#91b9d2"/>',
        '</svg>',
    ]
    return "\n".join(parts)


def attacker_for_weapon(topology, cx, face_y, center_y, handle_end):
    topology=topology.upper()
    if topology=="CROSS": return attacker_plus(cx,face_y,center_y,handle_end)
    if topology=="T": return attacker_t(cx,face_y,center_y,handle_end)
    if topology=="RADIAL": return attacker_radial(cx,face_y,center_y,handle_end)
    raise ValueError("final_weapon must be CROSS, T, or RADIAL")

def build_t_weapon_master_geometry_svg(projection):
    """Neutral, label-free master geometry: exactly one upright T-headed hammer."""
    width=int(projection["canvas"]["width"]); height=int(projection["canvas"]["height"])
    cx=width//2
    bar_height=int(height*0.085); bar_width=int(bar_height*3.8); stem_width=int(width*0.043)
    bar_x=cx-bar_width//2; bar_y=int(height*0.20)
    stem_y=bar_y+bar_height; stem_bottom=int(height*0.82)
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" data-stage="A_T_WEAPON_MASTER">',
        '<rect width="100%" height="100%" fill="#e9edf0"/>',
        '<rect x="40" y="40" width="1840" height="1000" rx="12" fill="#f7f8f9" stroke="#aeb8c0" stroke-width="3"/>',
        # One straight horizontal bar and one centered handle attached directly underneath.
        f'<rect x="{bar_x}" y="{bar_y}" width="{bar_width}" height="{bar_height}" fill="#647f95" stroke="#182b38" stroke-width="7"/>',
        f'<rect x="{cx-stem_width//2}" y="{stem_y}" width="{stem_width}" height="{stem_bottom-stem_y}" fill="#334f65" stroke="#182b38" stroke-width="7"/>',
        f'<path d="M{bar_x+8} {bar_y+8} H{bar_x+bar_width-8}" stroke="#b3d7e9" stroke-width="6"/>',
        '</svg>',
    ])


def build_svg(kind, projection, final_weapon="RADIAL"):
    width = int(projection["canvas"]["width"])
    height = int(projection["canvas"]["height"])
    cx = int(projection["sphere_center"]["x"])
    cy = int(projection["sphere_center"]["y"])
    r = int(projection["sphere_radius"])
    px = int(projection["P_six_oclock"]["x"])
    py = int(projection["P_six_oclock"]["y"])
    h2 = projection["frames"]["H2"]
    hx = int(h2["head_center"]["x"])
    hy = int(h2["head_center"]["y"])
    face_y = int(h2["top_face_y"])
    handle = (690, 920)
    if kind == "t_weapon_master":
        return build_t_weapon_master_geometry_svg(projection)
    if kind == "mask":
        # White = the complete target bubble footprint plus rim; black = protect everything else.
        parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
                 f'<rect width="{width}" height="{height}" fill="#000000"/>',
                 f'<circle cx="{cx}" cy="{cy}" r="{r+16}" fill="#ffffff" stroke="#ffffff" stroke-width="18"/>']
        import re
        protected = attacker_for_weapon(final_weapon,hx,face_y,hy,handle)
        protected = re.sub(r'fill="[^"]+"', 'fill="#000000"', protected)
        protected = re.sub(r'stroke="[^"]+"', 'stroke="#000000"', protected)
        protected = re.sub(r'stroke-width="[^"]+"', 'stroke-width="34"', protected)
        parts.append(protected)
        parts.append("</svg>")
        return "\n".join(parts)
    if kind == "attacker_mask":
        # White = the complete selected weapon; black = preserve all other pixels.
        import re
        weapon = attacker_for_weapon(final_weapon,hx,face_y,hy,handle)
        weapon = re.sub(r'fill="[^"]+"', 'fill="#ffffff"', weapon)
        weapon = re.sub(r'stroke="[^"]+"', 'stroke="#ffffff"', weapon)
        weapon = re.sub(r'stroke-width="[^"]+"', 'stroke-width="34"', weapon)
        parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
                 f'<rect width="{width}" height="{height}" fill="#000000"/>', weapon, "</svg>"]
        return "\n".join(parts)
    parts = svg_base(width, height)
    for x in range(80, width, 160):
        parts.append(line(x, 120, x, 1000, "#35536d", 1))
    for y in range(180, 1000, 120):
        parts.append(line(0, y, width, y, "#35536d", 1))
    if kind == "cross":
        parts.append(target_plus(cx, cy, r))
    elif kind in ("sphere","final_weapon"):
        parts += [
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#membrane)" stroke="#a4f2ff" stroke-width="8"/>',
            f'<circle cx="{cx}" cy="{cy}" r="{r-12}" fill="none" stroke="#7bdfff" stroke-opacity=".45" stroke-width="2"/>',
            f'<path d="M{cx-r+40} {cy+r-25} L{cx-r+80} {cy+65} L{cx-120} {cy+10} L{cx-65} {cy-50} L{cx-15} {cy+40} L{cx+40} {cy-80} L{cx+92} {cy+10} L{cx+140} {cy-25} L{cx+r-35} {cy+r-25} Z" fill="#234764" fill-opacity=".62" stroke="#77cfe9" stroke-opacity=".55" stroke-width="3"/>',
            f'<circle cx="{cx-95}" cy="{cy+110}" r="5" fill="#ffe1a3"/><circle cx="{cx+35}" cy="{cy+135}" r="5" fill="#ffe1a3"/><circle cx="{cx+112}" cy="{cy+80}" r="5" fill="#ffe1a3"/>',
        ]
    else:
        raise ValueError("kind must be cross, sphere, or mask")
    if kind == "final_weapon" or (kind == "sphere" and final_weapon == "T"):
        parts.append(attacker_for_weapon(final_weapon,hx,face_y,hy,handle))
    else:
        parts.append(attacker_plus(hx, face_y, hy, handle))
    parts.append(line(px-30, py, px+30, py, "#ffffff", 4))
    parts.append(f'<circle cx="{px}" cy="{py}" r="5" fill="#ffffff"/>')
    parts.append("</svg>")
    return "\n".join(parts)

def validate_geometry(layout, final_weapon="RADIAL"):
    p = layout.get("projection_lock", layout)
    required = ("canvas", "sphere_center", "sphere_radius", "P_six_oclock", "frames")
    if any(k not in p for k in required):
        raise ValueError("layout is missing projection_lock fields")
    c, point, radius = p["sphere_center"], p["P_six_oclock"], int(p["sphere_radius"])
    if int(c["x"]) != int(point["x"]) or int(c["y"])+radius != int(point["y"]):
        raise ValueError("geometry mismatch: sphere bottom pole is not P")
    h2 = p["frames"]["H2"]
    if int(h2["top_face_y"]) != int(point["y"]) or int(h2["head_center"]["x"]) != int(point["x"]):
        raise ValueError("geometry mismatch: attack cross face is not aligned with target cross face")
    if str(final_weapon).upper() == "T":
        # Fail closed if the T projection shows a vertical head but a separately diagonal stem.
        for frame_id in ("H0", "H2", "H3"):
            frame = p["frames"][frame_id]
            basis = frame.get("rigid_T_projection")
            if not isinstance(basis, dict):
                raise ValueError(f"geometry mismatch: missing rigid_T_projection basis for {frame_id}")
            crossbar = basis.get("crossbar_axis_screen", {})
            normal = basis.get("terminal_face_normal_screen", {})
            stem = basis.get("handle_axis_screen", {})
            if crossbar != {"x": 0, "y": -1} or normal != {"x": 0, "y": -1}:
                raise ValueError(f"geometry mismatch: T end-face normal/crossbar axis must project upward for {frame_id}")
            if stem != {"x": -1, "y": 0}:
                raise ValueError(f"geometry mismatch: T stem must project laterally in canonical view for {frame_id}")
            if crossbar["x"] * stem["x"] + crossbar["y"] * stem["y"] != 0:
                raise ValueError(f"geometry mismatch: projected T crossbar and stem are not perpendicular for {frame_id}")
            joint = frame.get("handle_joint")
            head_center = frame.get("head_center")
            handle_ref = frame.get("handle_reference_point")
            if joint != head_center or not isinstance(handle_ref, dict):
                raise ValueError(f"geometry mismatch: T handle joint is not at the crossbar midpoint for {frame_id}")
            if handle_ref.get("y") != joint.get("y") or handle_ref.get("x", point["x"]) >= joint.get("x", point["x"]):
                raise ValueError(f"geometry mismatch: T handle reference is not lateral to the joint for {frame_id}")
            if basis.get("joint_at_crossbar_midpoint") is not True or basis.get("handle_centerline_passes_through_joint") is not True:
                raise ValueError(f"geometry mismatch: T stem is not locked to the midpoint for {frame_id}")
    return p

def write_packet(layout_path: Path, outdir: Path, final_weapon: str = "RADIAL"):
    layout = json.loads(layout_path.read_text(encoding="utf-8"))
    final_weapon = final_weapon.upper()
    projection = validate_geometry(layout, final_weapon)
    if final_weapon not in ("CROSS","T","RADIAL"):
        raise ValueError("final_weapon must be CROSS, T, or RADIAL")
    outdir.mkdir(parents=True, exist_ok=True)
    files = {
        "proxy": "00_cross_to_cross_proxy.svg",
        "target_replaced": "01_target_cross_replaced_by_sphere.svg",
        "final_weapon_preview": "04_final_weapon_preview.svg",
        "mask": "02_target_cross_edit_mask.svg",
        "attacker_mask": "03_attacker_edit_mask.svg",
        "target_edit_prompt": "edit_target_plus_to_bubble.txt",
        "weapon_edit_prompt": "edit_attacker_plus_to_radial_hammer.txt",
    }
    if final_weapon == "T":
        files.update({
            "proxy": "00_T_weapon_master_geometry.svg",
            "target_replaced": "01_T_terminal_end_face_contact_schematic.svg",
            "final_weapon_preview": "04_T_final_weapon_preview.svg",
            "mask": "02_target_bubble_edit_mask.svg",
            "attacker_mask": "03_attacker_T_protect_mask.svg",
            "target_edit_prompt": "generate_scene_with_T_master.txt",
            "weapon_edit_prompt": "T_weapon_shape_lock.txt",
        })
    proxy_kind = "t_weapon_master" if final_weapon == "T" else "cross"
    for name, kind in [(files["proxy"], proxy_kind), (files["target_replaced"], "sphere"),
                       (files["final_weapon_preview"], "final_weapon"),
                       (files["mask"], "mask"), (files["attacker_mask"], "attacker_mask")]:
        (outdir/name).write_text(build_svg(kind, projection, final_weapon)+"\n", encoding="utf-8")
    if final_weapon == "T":
        files["t_shape_reference"] = "05_T_silhouette_reference.svg"
        (outdir/files["t_shape_reference"]).write_text(build_t_silhouette_reference_svg()+"\n", encoding="utf-8")
        files["t_weapon_master_generation_prompt"] = "00_generate_T_weapon_master.txt"
        (outdir/files["t_weapon_master_generation_prompt"]).write_text(
            "STAGE A — WEAPON-SHAPE MASTER ONLY. Generate ONE standalone photorealistic 16:9 product-reference image of exactly ONE T-headed hammer. "
            "Show the complete hammer from the left end of its head to the end of its handle. The head is one straight rigid horizontal rectangular crossbar; "
            "one single long handle attaches directly to the exact midpoint of the crossbar's underside and forms the only stem of the capital T. "
            "Use a level, near-front product view so the crossbar remains straight and horizontal, its left/right ends are equal, and the centered joint is obvious. "
            "A slight realistic metal bevel is fine, but do not bend, tilt, twist, round, split or duplicate the bar. Neutral studio background only. "
            "NO second hammer, NO inverted/upper T, NO bubble, NO heroine, NO city, NO debris, NO cracks, NO text, NO collage, NO extra shaft or short post. "
            "This is a weapon-geometry reference only, not the composition for the later cinematic scene. Save the reviewed real image as A_T_weapon_master.png.\n",
            encoding="utf-8")
        files["master_review_template"] = "A_T_weapon_master_review.template.json"
        master_review_template = {
            "stage_id": "A_T_WEAPON_MASTER",
            "status": "UNASSESSED",
            "image": "A_T_weapon_master.png",
            "manual_pixel_review": False,
            "checks": {
                "exactly_one_T_hammer": False,
                "horizontal_straight_crossbar": False,
                "handle_attached_at_underside_midpoint": False,
                "entire_weapon_visible": False,
                "no_second_or_inverted_T": False,
            },
            "notes": "",
            "warning": "Fill this out only after inspecting the actual generated A_T_weapon_master.png. Never mark PASS from the prompt or SVG alone.",
        }
        (outdir/files["master_review_template"]).write_text(json.dumps(master_review_template, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
        files["stage_gate"] = "stage_gate.json"
        stage_gate = {
            "required_order": ["A_T_WEAPON_MASTER", "B_T_TO_T_END_FACE_CONTACT_MATRIX", "C_STORY_SPECIFIC_SCENE_CAMERA_SWEEPS"],
            "current_stage": "A_T_WEAPON_MASTER_AND_T_CONTACT_MATRIX_REQUIRED",
            "status": "BLOCKED_UNTIL_T_CONTACT_MATRIX_APPROVED",
            "required_stage_a_artifact": "A_T_weapon_master.png",
            "required_contact_matrix_manifest": "contact_matrix_manifest.json",
            "required_contact_matrix_h2_images": 48,
            "required_contact_matrix_h2_reviews": "one manual review JSON per camera/axis variant",
            "manual_visual_approval_required": True,
            "stage_a_checks": [
                "exactly one T-headed hammer is present",
                "one straight horizontal crossbar with equal left and right ends",
                "one handle attaches directly at the exact underside midpoint and is the only stem",
                "the entire weapon is visible and unmistakably capital-T shaped",
                "no second or inverted T, bubble, heroine, city, debris or text",
            ],
            "not_proven_by_this_proxy": ["actual generated pixels", "face-to-face contact on any actual image", "cinematic scene quality", "real-image contact location", "story continuity"],
            "do_not_mark_pass_from_prompt_or_svg_alone": True,
            "reference_scope": "weapon topology only; the contact matrix proves active-face geometry; never copy this neutral background or composition into story scenes",
        }
        (outdir/files["stage_gate"]).write_text(json.dumps(stage_gate,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    c, point, radius = projection["sphere_center"], projection["P_six_oclock"], projection["sphere_radius"]
    if final_weapon == "T":
        target_prompt = (
            "STAGE C — STORY-SPECIFIC CINEMATIC SCENE GENERATION, ONLY AFTER THE T MASTER AND ALL 48 END-FACE CONTACT-MATRIX H2 IMAGES ARE VISUALLY APPROVED. "
            "Use A_T_weapon_master.png as a WEAPON-SHAPE reference only, and the approved 48-view terminal-END-FACE contact matrix as the active-plane reference; never treat either as a layout, camera, pose or background reference. "
            "Generate H0, H2 and H3 as THREE separate full-bleed images using the corresponding prompt files in this story's frame packet. "
            "Keep exactly ONE T-headed hammer held by the heroine. Aim its designated TERMINAL END STRIKING FACE at the bubble's six-o'clock point P; never substitute the broad upper/lower crossbar surface, long cheek, corner or handle. The contact matrix defines which plane is active. "
            "For the canonical bottom-pole orthographic view, the active face normal and crossbar project upward/vertically while the centered handle projects laterally through the midpoint. Rotate the entire T as one rigid object. "
            "An oblique scene camera may make both projected axes oblique only through one coherent 3D transform; never force a down-left handle while keeping the crossbar vertical, and never rotate the head independently. Reposition/reframe the heroine to follow the handle axis. "
            "The straight crossbar must not twist into an X, plus, L, sphere or diagonal bar. The BUBBLE is the target; never draw an upper inverted T "
            "or a second hammer and never replace one hammer with a bubble. Preserve the story-specific environment, scale, shell, palette, symbolism, "
            "motion and cinematic style from the provided frame prompts. Different story IDs should retain their distinct scene concepts; within one story, "
            "H0/H2/H3 share continuity and camera. Do not copy the neutral studio composition of the weapon master."
        )
        weapon_prompt = (
            "T-WEAPON SHAPE LOCK: exactly one straight rigid rectangular crossbar and one single long handle attached at the "
            "defined central underside joint. The handle itself is the T stem; there is no separate short post. Keep equal left/right bar ends, "
            "a centered joint and clear T topology in the weapon's own local orientation. The active contact face is a terminal END FACE at one end of the crossbar, not its cheek or upper/lower surface. Perspective may project the handle diagonally only when that angle follows the same rigid 3D transform as the crossbar. "
            "Never force a diagonal handle while the crossbar projects vertically, and never pivot the handle or head independently. No second or inverted T, no sphere head, no plus/X/L head, no extra bar, no extra shaft."
        )
    else:
        target_prompt = (
            "EDIT ONLY THE TARGET PLUS-SIGN in the provided cross-to-cross proxy. "
            f"Pin sphere center C=({c['x']},{c['y']}) and radius R={radius} px; "
            f"pin the sphere's six-o'clock bottom P=({point['x']},{point['y']}). "
            "Replace the large target plus with a transparent iridescent bubble centered exactly at C. "
            "The target cross's lower terminal face becomes the bubble's six-o'clock point P. "
            "Preserve the attacking plus-sign, its upward-facing flat terminal face, handle, background, camera, horizon and all coordinates. "
            "Do not repaint or move the attacking object. No writing, labels, guides, added cracks or effects."
        )
        weapon_prompt = (
            "EDIT ONLY THE ATTACKING PLUS-SIGN after the target bubble edit has passed review. "
            "Replace the attacking plus head with ONE compact near-spherical hammer head tiled with broad, flat striking faces "
            "pointing radially outward in many directions. Retain ONE rigid long handle. Preserve the upward-facing flat terminal "
            f"striking face at P=({point['x']},{point['y']}), head center, handle joint, handle direction, bubble, contact patch, camera and background. "
            "Do not edit the bubble. Do not change the weapon into spikes, a mace, chain, halo or multiple hammers."
        )
    (outdir/files["target_edit_prompt"]).write_text(target_prompt+"\n",encoding="utf-8")
    (outdir/files["weapon_edit_prompt"]).write_text(weapon_prompt+"\n",encoding="utf-8")
    weapon_prompt_t = (
        "WEAPON SHAPE LOCK ONLY. One straight horizontal rigid rectangular crossbar, equal left/right ends, and one single long handle attached "
        "directly to the exact underside midpoint. The handle itself is the T stem; do not add a short post. Preserve this capital-T topology while "
        "allowing the complete weapon to rotate as a rigid object in perspective. No second/inverted T, sphere, plus/X/L shape, extra bar or extra shaft."
    )
    weapon_prompt_cross = (
        "EDIT ONLY THE ATTACKING PLUS-SIGN. Keep the cross proxy unchanged; do not edit the bubble, contact point, handle, camera or background."
    )
    (outdir/"edit_attacker_to_T.txt").write_text(weapon_prompt_t+"\n",encoding="utf-8")
    (outdir/"edit_attacker_keep_cross.txt").write_text(weapon_prompt_cross+"\n",encoding="utf-8")
    (outdir/"edit_attacker_keep_T.txt").write_text(weapon_prompt+"\n",encoding="utf-8")
    selected_prompt=files["target_edit_prompt"] if final_weapon=="T" else {"RADIAL":files["weapon_edit_prompt"],"CROSS":"edit_attacker_keep_cross.txt"}[final_weapon]
    shape_contract = {
        "RADIAL":"one long handle + one near-spherical head tiled with outward flat faces",
        "T":"one straight horizontal crossbar + one long handle joined exactly at the crossbar underside midpoint; the handle itself forms the single stem of the T; no separate short post",
        "CROSS":"one long handle + one connected plus-sign head with vertical and horizontal arms",
    }[final_weapon]
    if final_weapon == "T":
        plan = {
            "method":"T_MASTER_THEN_T_END_FACE_CONTACT_MATRIX_THEN_STORY_SCENE_GENERATION",
            "status":"BLOCKED_UNTIL_T_CONTACT_MATRIX_APPROVED",
            "vector_proxy_status":"T_WEAPON_MASTER_SHAPE_PROXY_VALID",
            "stage_gate_status":"BLOCKED_UNTIL_T_CONTACT_MATRIX_APPROVED",
            "final_weapon":final_weapon,
            "shape_contract":shape_contract,
            "active_striking_surface":"the selected terminal END STRIKING FACE at one end of the rigid T crossbar; the bubble is the target, never a second T",
            "selected_edit_prompt":selected_prompt,
            "projection_lock":projection,
            "vector_proxy_terminal_face_gap_px":0,
            "terminal_face_gap_px":None,
            "face_normals":{"attacker":"END_FACE_NORMAL_PINNED_TO_LOCAL_SPHERE_NORMAL","target":"OPPOSING_LOCAL_SURFACE_NORMAL"},
            "required_order":[
                "A: generate ONE isolated T weapon master using 00_generate_T_weapon_master.txt",
                "A_GATE: manually review and approve A_T_weapon_master.png; do not infer approval from the prompt or SVG",
                "B: generate 144 T-to-T H0/H2/H3 contact-matrix prompts over 12 views x 4 collision axes; balance all four handle-roll relationships across the 48 variants",
                "B_GATE: manually review all 48 H2 contact proofs; each must show terminal END FACE to END FACE, coincident planes and opposing normals",
                "C: generate each story's H0/H2/H3 across the 12 camera variants; preserve continuity within each camera trio",
                "C: keep scene concepts varied across story IDs, preserve continuity within each camera trio, then audit actual image pixels",
            ],
            "required_artifacts":{
                "stage_a_image":"A_T_weapon_master.png",
                "stage_a_review":"A_T_weapon_master_review.json",
                "stage_a_review_template":"A_T_weapon_master_review.template.json",
                "contact_matrix_manifest":"contact_matrix_manifest.json",
                "contact_matrix_h2_image_count":48,
                "contact_matrix_h2_review_pattern":"one manually reviewed JSON per variant",
                "scene_camera_variant_count":12,
                "scene_prompts":["H0_pre_impact.txt","H2_first_contact_anchor.txt","H3_post_impact.txt"],
            },
            "stage_gate_file":files["stage_gate"],
            "pixel_truth":{"vector_proxy":"T_WEAPON_MASTER_SHAPE_PROXY_VALID","contact_matrix_images":"NOT_RUN","edited_images":"NOT_RUN",
                           "warning":"This repository compiles prompts and SVG references only. It does not generate images or certify end-face contact; the 48 actual H2 images must pass manual pixel review."},
            "files":files,
        }
    else:
        plan = {
            "method":"CROSS_TO_CROSS_THEN_TARGET_ONLY_SPHERE_EDIT",
            "status":"GEOMETRY_PROXY_VALID",
            "final_weapon":final_weapon,
            "shape_contract":shape_contract,
            "active_striking_surface":{
                "RADIAL":"one upward-facing flat polygon on the radial head",
                "CROSS":"the upper terminal face of the vertical arm",
            }[final_weapon],
            "selected_edit_prompt":selected_prompt,
            "projection_lock":projection,
            "terminal_face_gap_px":0,
            "face_normals":{"attacker":"UP (+Y)","target":"DOWN (-Y)"},
            "sequence":[
                "A: verify both plus-sign terminal faces meet at exactly P in the vector proxy",
                "B: edit only the target plus into a sphere centered at C with radius R; preserve the attacker and camera",
                f"C: after B passes pixel review, edit only the attacker into {final_weapon}; use the selected edit prompt and keep target P/camera locked",
            ],
            "pixel_truth":{"vector_proxy":"GEOMETRY_VALID","edited_images":"NOT_RUN",
                           "warning":"The zero-gap guarantee applies to vector coordinates, not to pixels produced by an external image editor."},
            "files":files,
        }
    (outdir/"edit_plan.json").write_text(json.dumps(plan,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    readme_text = (
        "T weapon master plus end-face matrix workflow. Generate and manually approve A_T_weapon_master.png, then generate and manually review 48 T-to-T END-FACE collision variants before scenes; "
        "then use generate_scene_with_T_master.txt and each story's H0/H2/H3 camera-sweep prompts. The master controls weapon topology only, "
        "not scene composition. The bubble is the target; never add an upside-down second T or replace a hammer with a bubble. "
        "Do not claim an image PASS from these SVGs or prompts."
        if final_weapon == "T" else
        "Cross-to-cross geometry proxy. First validate the two flat terminal faces. Then edit only the target plus into a bubble. "
        "Only after reviewing that result, edit only the attacking object into the selected final weapon. "
        "Do not edit both objects in the same pass. SVGs are deterministic geometry references, not final cinematic artwork. "
        "AI edit pixel fidelity is not guaranteed; measure the actual edited output."
    )
    (outdir/"README.md").write_text(readme_text+"\n",encoding="utf-8")
    return {"status":plan["status"],"terminal_face_gap_px":(None if final_weapon=="T" else 0),"files":list(files.values())+["edit_plan.json","README.md"],
            "edited_images":"NOT_RUN","outdir":str(outdir)}

def main(argv=None):
    parser=argparse.ArgumentParser(description="Generate geometry/edit packets; T mode uses one approved T-weapon master for story-specific scene prompts.")
    parser.add_argument("--input-layout",required=True)
    parser.add_argument("--outdir",required=True)
    parser.add_argument("--final-weapon",choices=("CROSS","T","RADIAL"),default="RADIAL")
    args=parser.parse_args(argv)
    try:
        result=write_packet(Path(args.input_layout),Path(args.outdir),args.final_weapon)
    except (OSError,ValueError,json.JSONDecodeError) as exc:
        print("BLOCK: "+str(exc),file=sys.stderr)
        return 2
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
