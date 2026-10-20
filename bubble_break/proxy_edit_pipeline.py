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
    # The long handle itself forms the T stem; do not draw a second short post.
    crossbar_bottom = face_y + 58
    shaft = line(handle_end[0], handle_end[1], cx, crossbar_bottom, "#02060a", 34)
    shaft += line(handle_end[0], handle_end[1], cx, crossbar_bottom, "url(#metal)", 23)
    head = rect(cx-112, face_y+8, 224, 50, "#234761", "#e0bd82", 5)
    # Narrow top-plane bevel; its upper edge stays pinned to the impact coordinate.
    head += f'<polygon points="{cx-112},{face_y+8} {cx+112},{face_y+8} {cx+96},{face_y} {cx-96},{face_y}" fill="#6b9cbd" stroke="#fff0bf" stroke-width="4" stroke-linejoin="round"/>'
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

def build_t_to_t_geometry_svg(projection):
    """Neutral, label-free opposing-T anchor: inverted target T above, attacking T below."""
    width=int(projection["canvas"]["width"]); height=int(projection["canvas"]["height"])
    point=projection["P_six_oclock"]; cx=int(point["x"]); py=int(point["y"])
    bar_width=224; bar_height=58; stem_width=68
    x0=cx-bar_width//2; stem_x=cx-stem_width//2
    target_bar_y=py-bar_height; target_stem_top=max(70,target_bar_y-250)
    handle_end=(690,920)
    parts=[
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" data-contact-p="{cx},{py}" data-stage="A_T_TO_T">',
        '<rect width="100%" height="100%" fill="#e9edf0"/>',
        '<rect x="40" y="40" width="1840" height="1000" rx="12" fill="#f7f8f9" stroke="#aeb8c0" stroke-width="3"/>',
        # Upper target T is inverted: its lower flat face opposes the attacker's upper flat face.
        f'<rect x="{stem_x}" y="{target_stem_top}" width="{stem_width}" height="{target_bar_y-target_stem_top}" fill="#647f95" stroke="#182b38" stroke-width="5"/>',
        f'<rect x="{x0}" y="{target_bar_y}" width="{bar_width}" height="{bar_height}" fill="#647f95" stroke="#182b38" stroke-width="5"/>',
        # Lower attacking T: one straight handle joins the center underside of its crossbar.
        line(handle_end[0],handle_end[1],cx,py+bar_height,"#18232d",34),
        line(handle_end[0],handle_end[1],cx,py+bar_height,"#b3c3ce",21),
        f'<rect x="{x0}" y="{py}" width="{bar_width}" height="{bar_height}" fill="#334f65" stroke="#182b38" stroke-width="5"/>',
        f'<path d="M{x0+5} {py+5} H{cx+bar_width//2-5}" stroke="#b3d7e9" stroke-width="5"/>',
        '</svg>',
    ]
    return "\n".join(parts)


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
    if kind == "t_to_t":
        return build_t_to_t_geometry_svg(projection)
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

def validate_geometry(layout):
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
    return p

def write_packet(layout_path: Path, outdir: Path, final_weapon: str = "RADIAL"):
    layout = json.loads(layout_path.read_text(encoding="utf-8"))
    projection = validate_geometry(layout)
    final_weapon = final_weapon.upper()
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
            "proxy": "00_T_to_T_geometry_proxy.svg",
            "target_replaced": "01_target_T_replaced_by_sphere.svg",
            "final_weapon_preview": "04_T_final_weapon_preview.svg",
            "mask": "02_target_bubble_edit_mask.svg",
            "attacker_mask": "03_attacker_T_protect_mask.svg",
            "target_edit_prompt": "edit_target_T_to_bubble.txt",
            "weapon_edit_prompt": "edit_attacker_keep_T.txt",
        })
    proxy_kind = "t_to_t" if final_weapon == "T" else "cross"
    for name, kind in [(files["proxy"], proxy_kind), (files["target_replaced"], "sphere"),
                       (files["final_weapon_preview"], "final_weapon"),
                       (files["mask"], "mask"), (files["attacker_mask"], "attacker_mask")]:
        (outdir/name).write_text(build_svg(kind, projection, final_weapon)+"\n", encoding="utf-8")
    if final_weapon == "T":
        files["t_shape_reference"] = "05_T_silhouette_reference.svg"
        (outdir/files["t_shape_reference"]).write_text(build_t_silhouette_reference_svg()+"\n", encoding="utf-8")
        files["t_to_t_generation_prompt"] = "00_generate_T_to_T_anchor.txt"
        (outdir/files["t_to_t_generation_prompt"]).write_text(
            "STAGE A — REQUIRED BEFORE ANY BUBBLE OR HEROINE IMAGE. Generate ONE standalone photorealistic 16:9 industrial-design image "
            "of exactly TWO enormous T-headed hammers facing each other on the same vertical contact plane. The lower attacker T is upright: "
            "one straight horizontal rectangular crossbar and one long rigid handle joined directly at its underside midpoint, the handle itself "
            "forms its only stem and extends down-left. The upper target T is inverted: one straight horizontal rectangular crossbar, with one centered "
            "rigid stem extending upward from the crossbar. Their broad flat faces oppose each other vertically and meet at exactly the same center P; "
            "the lower T's upper crossbar face touches only the upper T's lower crossbar face. Both T silhouettes must be fully visible and unmistakable. "
            "Match the supplied 00_T_to_T_geometry_proxy.svg and 05_T_silhouette_reference.svg for geometry. Neutral simple background only: NO bubble, "
            "NO person, NO city, NO debris, NO cracks, NO text, NO collage, NO extra weapon. This image is the mandatory geometry gate; do not proceed "
            "to a bubble replacement unless the actual generated image is manually reviewed and approved.\n", encoding="utf-8")
        files["stage_gate"] = "stage_gate.json"
        stage_gate = {
            "required_order": ["A_T_TO_T_ANCHOR", "B_REPLACE_TARGET_T_WITH_BUBBLE", "C_BUILD_REAL_SCENE_FRAMES"],
            "current_stage": "A_T_TO_T_ANCHOR_REQUIRED",
            "status": "BLOCKED_UNTIL_T_TO_T_IMAGE_APPROVED",
            "required_stage_a_artifact": "A_T_to_T_anchor.png",
            "manual_visual_approval_required": True,
            "stage_a_checks": [
                "two and only two T-shaped hammers are present",
                "lower attacker and upper inverted target are both clearly T-shaped",
                "their broad faces oppose and meet at the same center P",
                "there is no bubble, heroine, city, debris or text",
                "crossbars remain straight/horizontal and each handle is centered",
            ],
            "not_proven_by_this_proxy": ["actual generated pixels", "correct real-image contact location", "scene/hero continuity"],
            "do_not_mark_pass_from_prompt_or_svg_alone": True,
        }
        (outdir/files["stage_gate"]).write_text(json.dumps(stage_gate,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    c, point, radius = projection["sphere_center"], projection["P_six_oclock"], projection["sphere_radius"]
    if final_weapon == "T":
        target_prompt = (
            "STAGE B — ONLY AFTER STAGE A IS MANUALLY APPROVED. Use the actual approved A_T_to_T_anchor.png as the input image, "
            "not the vector proxy alone. Edit ONLY the UPPER INVERTED TARGET T (the hammer above the shared contact plane). "
            f"Replace that upper target T with ONE intact transparent iridescent bubble whose center is C=({c['x']},{c['y']}) "
            f"and radius R={radius}px, so its exact six-o'clock bottom pole is P=({point['x']},{point['y']}). "
            "The bubble's bottom pole must stay on the same contact point as the lower attacking T's broad upper crossbar face. "
            "Preserve the LOWER ATTACKING T pixel-for-pixel: straight horizontal crossbar, equal left/right ends, one long handle attached "
            "at the exact underside midpoint, no extra post. Preserve the camera, background and perspective. The bubble is whole: no cracks, "
            "no shards, no explosion. Do not add a heroine or cinematic scene yet. If the upper T cannot be replaced without moving the lower "
            "T's contact face or shifting P, reject the edit and return to Stage A."
        )
        weapon_prompt = (
            "STAGE B LOCK: do not edit the lower attacking T. It is already the approved final T weapon. "
            "Keep the crossbar straight and horizontal, the single long handle joined at the exact underside midpoint, and preserve P. "
            "No extra post, no sphere head, no plus/X/L/Y shape. No weapon edit is allowed in this stage."
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
        "EDIT ONLY THE ATTACKING PLUS-SIGN after the target bubble edit has passed pixel review. "
        "Use 05_T_silhouette_reference.svg as the authoritative T-shape guide; it defines topology only, not camera pose. "
        "Convert only the masked weapon into ONE unmistakable T-shaped hammer with a capital-T silhouette: exactly one straight, horizontal, rigid rectangular crossbar "
        "with equal left/right ends, and exactly ONE long handle joined to the exact midpoint of the crossbar's underside. "
        "The long handle itself forms the single stem of the T; do NOT add a second short vertical post between head and handle. "
        "Keep the crossbar width about 3.8 times its thickness and the handle joint centered. The bar remains a straight line; "
        "do not round it into a globe, rotate it into a diagonal bar, turn it into a plus/X/L/Y shape, or invent extra head parts. "
        "For this topology, the active striking surface is the BROAD UPPER PLANE of the crossbar, not a side wall or a pretend spherical face. "
        f"Pin the center of that upper plane at P=({point['x']},{point['y']}); its upper edge/contact coordinate must not move. "
        "The single handle must remain rigid and connected at the center; its apparent diagonal is only 3D perspective toward the heroine. "
        "Preserve the bubble outline, city, contact point, camera, background and every pixel outside the attacker mask. "
        "No radial/faceted ball head, plus-sign/cross head, X head, spikes, studs, mace, extra bar, extra shaft, disconnected handle or extra weapon."
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
            "method":"T_TO_T_THEN_TARGET_T_ONLY_SPHERE_EDIT",
            "status":"BLOCKED_UNTIL_T_TO_T_IMAGE_APPROVED",
            "vector_proxy_status":"GEOMETRY_PROXY_VALID",
            "stage_gate_status":"BLOCKED_UNTIL_T_TO_T_IMAGE_APPROVED",
            "final_weapon":final_weapon,
            "shape_contract":shape_contract,
            "active_striking_surface":"the broad upper plane of the lower T crossbar, facing the lower plane of the upper inverted T crossbar in Stage A; after Stage B it touches the bubble's bottom pole P",
            "selected_edit_prompt":selected_prompt,
            "projection_lock":projection,
            "terminal_face_gap_px":0,
            "face_normals":{"attacker":"UP (+Y)","target":"DOWN (-Y)"},
            "required_order":[
                "A: generate a photorealistic T-to-T anchor using 00_generate_T_to_T_anchor.txt and the geometry references",
                "A_GATE: manually inspect and approve the actual A_T_to_T_anchor.png; do not infer approval from the prompt or SVG",
                "B: only after A_GATE passes, edit only the upper inverted target T into one intact bubble; keep lower T and P fixed",
                "C: create real-scene H0/H2/H3 as separate branches from the approved geometry, and audit actual pixels",
            ],
            "required_artifacts":{
                "stage_a_image":"A_T_to_T_anchor.png",
                "stage_a_review":"A_T_to_T_review.json",
                "stage_b_image":"B_target_T_replaced_by_bubble.png",
            },
            "stage_gate_file":files["stage_gate"],
            "pixel_truth":{"vector_proxy":"GEOMETRY_VALID","edited_images":"NOT_RUN",
                           "warning":"The pipeline cannot certify external generated pixels. Stage A remains BLOCKED until its real image and manual review record exist."},
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
        "T-to-T geometry proxy. REQUIRED ORDER: generate and manually approve the real A_T_to_T_anchor.png first; "
        "only then use edit_target_T_to_bubble.txt to replace the upper inverted target T with a bubble. "
        "The current packet remains BLOCKED_UNTIL_T_TO_T_IMAGE_APPROVED. Do not claim a real-image PASS from these SVGs or prompts. "
        "Preserve the lower attacking T and verify the true contact pixel location."
        if final_weapon == "T" else
        "Cross-to-cross geometry proxy. First validate the two flat terminal faces. Then edit only the target plus into a bubble. "
        "Only after reviewing that result, edit only the attacking object into the selected final weapon. "
        "Do not edit both objects in the same pass. SVGs are deterministic geometry references, not final cinematic artwork. "
        "AI edit pixel fidelity is not guaranteed; measure the actual edited output."
    )
    (outdir/"README.md").write_text(readme_text+"\n",encoding="utf-8")
    return {"status":plan["status"],"terminal_face_gap_px":0,"files":list(files.values())+["edit_plan.json","README.md"],
            "edited_images":"NOT_RUN","outdir":str(outdir)}

def main(argv=None):
    parser=argparse.ArgumentParser(description="Generate geometry/edit packets; T mode requires an approved T-to-T anchor before bubble editing.")
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
