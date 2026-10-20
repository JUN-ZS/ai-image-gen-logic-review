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
    # Upper terminal striking face is fixed exactly to P.
    shaft = line(handle_end[0], handle_end[1], cx, center_y, "#02060a", 34)
    shaft += line(handle_end[0], handle_end[1], cx, center_y, "url(#metal)", 23)
    head = rect(cx-30, face_y, 60, center_y+95-face_y, "#234761", "#e0bd82", 5)
    head += rect(cx-100, center_y-30, 200, 60, "#234761", "#e0bd82", 5)
    head += rect(cx-30, face_y-2, 60, 5, "#fff1c7", "#ffffff", 2)
    head += line(cx-25, face_y+9, cx+25, face_y+9, "#8be7ff", 3)
    return shaft + head

def build_svg(kind, projection):
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
    if kind == "mask":
        # White = target geometry to replace; black = protect the attacker.
        parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
                 f'<rect width="{width}" height="{height}" fill="#000000"/>',
                 rect(cx-22, cy-r, 44, 2*r, "#ffffff", "#ffffff", 0),
                 rect(cx-r, cy-22, 2*r, 44, "#ffffff", "#ffffff", 0),
                 f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#ffffff" stroke-width="18"/>']
        import re
        protected = attacker_plus(hx, face_y, hy, handle)
        protected = re.sub(r'fill="[^"]+"', 'fill="#000000"', protected)
        protected = re.sub(r'stroke="[^"]+"', 'stroke="#000000"', protected)
        protected = re.sub(r'stroke-width="[^"]+"', 'stroke-width="34"', protected)
        parts.append(protected)
        parts.append("</svg>")
        return "\n".join(parts)
    if kind == "attacker_mask":
        # White = the attacker to edit; black = preserve the target bubble and scene.
        parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
                 f'<rect width="{width}" height="{height}" fill="#000000"/>',
                 line(handle[0], handle[1], hx, hy, "#ffffff", 42),
                 rect(hx-30, face_y, 60, hy+95-face_y, "#ffffff", "#ffffff", 3),
                 rect(hx-100, hy-30, 200, 60, "#ffffff", "#ffffff", 3),
                 rect(hx-30, face_y-2, 60, 5, "#ffffff", "#ffffff", 2),
                 "</svg>"]
        return "\n".join(parts)
    parts = svg_base(width, height)
    for x in range(80, width, 160):
        parts.append(line(x, 120, x, 1000, "#35536d", 1))
    for y in range(180, 1000, 120):
        parts.append(line(0, y, width, y, "#35536d", 1))
    if kind == "cross":
        parts.append(target_plus(cx, cy, r))
    elif kind == "sphere":
        parts += [
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#membrane)" stroke="#a4f2ff" stroke-width="8"/>',
            f'<circle cx="{cx}" cy="{cy}" r="{r-12}" fill="none" stroke="#7bdfff" stroke-opacity=".45" stroke-width="2"/>',
            f'<path d="M{cx-r+40} {cy+r-25} L{cx-r+80} {cy+65} L{cx-120} {cy+10} L{cx-65} {cy-50} L{cx-15} {cy+40} L{cx+40} {cy-80} L{cx+92} {cy+10} L{cx+140} {cy-25} L{cx+r-35} {cy+r-25} Z" fill="#234764" fill-opacity=".62" stroke="#77cfe9" stroke-opacity=".55" stroke-width="3"/>',
            f'<circle cx="{cx-95}" cy="{cy+110}" r="5" fill="#ffe1a3"/><circle cx="{cx+35}" cy="{cy+135}" r="5" fill="#ffe1a3"/><circle cx="{cx+112}" cy="{cy+80}" r="5" fill="#ffe1a3"/>',
        ]
    else:
        raise ValueError("kind must be cross, sphere, or mask")
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

def write_packet(layout_path: Path, outdir: Path):
    layout = json.loads(layout_path.read_text(encoding="utf-8"))
    projection = validate_geometry(layout)
    outdir.mkdir(parents=True, exist_ok=True)
    files = {
        "proxy": "00_cross_to_cross_proxy.svg",
        "target_replaced": "01_target_cross_replaced_by_sphere.svg",
        "mask": "02_target_cross_edit_mask.svg",
        "attacker_mask": "03_attacker_edit_mask.svg",
        "target_edit_prompt": "edit_target_plus_to_bubble.txt",
        "weapon_edit_prompt": "edit_attacker_plus_to_radial_hammer.txt",
    }
    for name, kind in [(files["proxy"], "cross"), (files["target_replaced"], "sphere"),
                       (files["mask"], "mask"), (files["attacker_mask"], "attacker_mask")]:
        (outdir/name).write_text(build_svg(kind, projection)+"\n", encoding="utf-8")
    c, point, radius = projection["sphere_center"], projection["P_six_oclock"], projection["sphere_radius"]
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
    plan = {
        "method":"CROSS_TO_CROSS_THEN_TARGET_ONLY_SPHERE_EDIT",
        "status":"GEOMETRY_PROXY_VALID",
        "projection_lock":projection,
        "terminal_face_gap_px":0,
        "face_normals":{"attacker":"UP (+Y)","target":"DOWN (-Y)"},
        "sequence":[
            "A: verify both plus-sign terminal faces meet at exactly P in the vector proxy",
            "B: edit only the target plus into a sphere centered at C with radius R; preserve the attacker and camera",
            "C: after B passes pixel review, edit only the attacker into the radial multi-face sphere hammer",
        ],
        "pixel_truth":{"vector_proxy":"GEOMETRY_VALID","edited_images":"NOT_RUN",
                       "warning":"The zero-gap guarantee applies to vector coordinates, not to pixels produced by an external image editor."},
        "files":files,
    }
    (outdir/"edit_plan.json").write_text(json.dumps(plan,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (outdir/"README.md").write_text(
        "Cross-to-cross geometry proxy. First validate the two flat terminal faces. Then edit only the target plus into a bubble. "
        "Only after reviewing that result, edit only the attacking plus into the radial multi-face hammer. "
        "Do not edit both objects in the same pass. SVGs are deterministic geometry references, not final cinematic artwork. "
        "AI edit pixel fidelity is not guaranteed; measure the actual edited output.\n", encoding="utf-8")
    return {"status":plan["status"],"terminal_face_gap_px":0,"files":list(files.values())+["edit_plan.json","README.md"],
            "edited_images":"NOT_RUN","outdir":str(outdir)}

def main(argv=None):
    parser=argparse.ArgumentParser(description="Generate cross-to-cross anchor SVGs and target-only bubble-edit instructions.")
    parser.add_argument("--input-layout",required=True)
    parser.add_argument("--outdir",required=True)
    args=parser.parse_args(argv)
    try:
        result=write_packet(Path(args.input_layout),Path(args.outdir))
    except (OSError,ValueError,json.JSONDecodeError) as exc:
        print("BLOCK: "+str(exc),file=sys.stderr)
        return 2
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
