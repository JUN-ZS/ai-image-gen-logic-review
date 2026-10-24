#!/usr/bin/env python3
"""Compose a large, floating 3D-poster TRY typography layer over a source frame.

The source PNG/JPEG is embedded unchanged. Exact title/method words come from CLI/manifest,
never from the image model. Full source/artwork SHA-256 values are written to the JSON sidecar.
The renderer does not generate media and does not certify geometry, continuity or video physics.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import html
import json
import mimetypes
import struct
from pathlib import Path
from typing import Any

ALLOWED_STATUSES = {
    "PROMPT_READY",
    "IMAGE_GENERATED",
    "VIDEO_GENERATED",
    "REVIEW_PENDING",
    "HUMAN_ACCEPTED",
    "REJECTED",
    "NEGATIVE_CONTROL",
}
DEFAULT_STATUS = "REVIEW_PENDING"
PALETTES = {
    "S01": {"deep": "#071421", "edge": "#8fe8ed", "metal": "#f5cd7a", "ink": "#fff5dc", "shadow": "#7b3c16"},
    "S02": {"deep": "#311e42", "edge": "#ffb2cf", "metal": "#ffe49a", "ink": "#fff8ff", "shadow": "#9d5fba"},
    "S03": {"deep": "#101018", "edge": "#b9a4ff", "metal": "#f7d5ff", "ink": "#fff8ff", "shadow": "#473080"},
    "S04": {"deep": "#171f1b", "edge": "#a4d4ba", "metal": "#f1e6c5", "ink": "#f8f3e7", "shadow": "#3f5b4a"},
    "S05": {"deep": "#120f0c", "edge": "#c45c4a", "metal": "#e8d5a3", "ink": "#f4efe6", "shadow": "#5a2a22"},
    "S06": {"deep": "#0a0608", "edge": "#e8a040", "metal": "#f0d080", "ink": "#fff4d8", "shadow": "#6a2010"},
}
DIEGETIC_VFX = {
    "none": {"stroke": "#ffffff", "glow": "#ffffff", "opacity": 0.0, "label": "NONE"},
    "lightning": {"stroke": "#7ef0ff", "glow": "#3ad0ff", "opacity": 0.92, "label": "COILED_HAMMER_NEON_LIGHTNING"},
    "fire": {"stroke": "#ff7a2a", "glow": "#ffd060", "opacity": 0.95, "label": "COMBUSTION_FIRE_MORPH"},
    "graffiti": {"stroke": "#ff4fd8", "glow": "#7a5cff", "opacity": 0.88, "label": "PERSPECTIVE_STREET_GRAFFITI"},
    "ice": {"stroke": "#b8f0ff", "glow": "#e8fbff", "opacity": 0.90, "label": "SHATTERED_ICE_RELIEF"},
}


def esc(value: Any) -> str:
    return html.escape(str(value if value is not None else ""), quote=True)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def l_sha12(metadata: dict[str, Any]) -> str:
    raw = str(
        metadata.get("mid_master_sha256")
        or metadata.get("source_sha256")
        or metadata.get("method_fingerprint")
        or ""
    ).strip().lower()
    if not raw:
        return "000000000000"
    if raw.startswith("l-"):
        return raw[2:14]
    return raw[:12]


def canonical_text_payload(metadata: dict[str, Any]) -> dict[str, str]:
    """Words/IDs identical across PRE/MID/POST. v5 includes L-SHA12; omits status noise."""
    sha12 = l_sha12(metadata)
    world = str(metadata.get("world_label") or metadata.get("series_id") or "WORLD")
    return {
        "title": "邊界行人 / THE BOUNDARY WALKER",
        "loop_try": f"LOOP {metadata.get('loop_id', '')}  /  TRY {metadata.get('try_id', '')}",
        "method": str(metadata.get("method_label") or metadata.get("method_id") or ""),
        "geometry_contact": f"{metadata.get('geometry_family', '')} / {metadata.get('contact_method', '')}",
        "camera_pose": f"{metadata.get('camera_id', '')} / {metadata.get('pose_id', '')}",
        "style_series_world": " / ".join(
            str(metadata.get(key) or "")
            for key in ("style_id", "series_id", "world_label")
        ),
        "prompt_id": str(metadata.get("prompt_id") or ""),
        "world_lsha": f"WORLD: {world} · L-{sha12}",
        "l_sha12": f"L-{sha12}",
    }



def text_content_sha256(metadata: dict[str, Any]) -> str:
    payload = canonical_text_payload(metadata)
    return sha256_bytes(json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8"))


TYPOGRAPHY_TREATMENTS = {
    "before": {
        "deep": "#061a2a", "edge": "#8aeaff", "metal": "#c7faff",
        "ink": "#f2fdff", "shadow": "#174e78",
    },
    "middle": {
        "deep": "#101b28", "edge": "#8fcbd2", "metal": "#d5dce2",
        "ink": "#fffaf1", "shadow": "#46596e",
    },
    "after": {
        "deep": "#26120d", "edge": "#ff9a50", "metal": "#ffd079",
        "ink": "#fff5d5", "shadow": "#873014",
    },
    "video-lock": {
        "deep": "#101b28", "edge": "#6fd6d4", "metal": "#f3dc98",
        "ink": "#fdf6e8", "shadow": "#293d55",
    },
}


def image_size(data: bytes) -> tuple[int, int]:
    """Read dimensions from PNG or JPEG headers without re-encoding the source."""
    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24 and data[12:16] == b"IHDR":
        width, height = struct.unpack(">II", data[16:24])
        if width > 0 and height > 0:
            return width, height
        raise ValueError("PNG has invalid dimensions")
    if data.startswith(b"\xff\xd8"):
        offset = 2
        sof_markers = {
            0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
            0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF,
        }
        while offset + 4 <= len(data):
            if data[offset] != 0xFF:
                offset += 1
                continue
            while offset < len(data) and data[offset] == 0xFF:
                offset += 1
            if offset >= len(data):
                break
            marker = data[offset]
            offset += 1
            if marker in {0xD8, 0xD9, 0x01} or 0xD0 <= marker <= 0xD7:
                continue
            if offset + 2 > len(data):
                break
            length = int.from_bytes(data[offset:offset + 2], "big")
            if length < 2 or offset + length > len(data):
                break
            if marker in sof_markers and length >= 7:
                height = int.from_bytes(data[offset + 3:offset + 5], "big")
                width = int.from_bytes(data[offset + 5:offset + 7], "big")
                if width > 0 and height > 0:
                    return width, height
                break
            offset += length
    raise ValueError("Unsupported or unreadable image header; use PNG or JPEG")


def validate_status(status: str) -> str:
    if status not in ALLOWED_STATUSES:
        raise ValueError(
            f"Unsupported status {status!r}; choose one of {', '.join(sorted(ALLOWED_STATUSES))}. "
            "Plain PASS is intentionally unavailable."
        )
    return status


def _text(x: float, y: float, value: str, size: int, fill: str,
          weight: int = 500, family: str = "Inter, Noto Sans CJK TC, Microsoft JhengHei, sans-serif",
          spacing: float = 0, anchor: str = "start", opacity: float = 1.0) -> str:
    return (
        f'<text x="{x:.2f}" y="{y:.2f}" font-family="{family}" font-size="{size}" '
        f'font-weight="{weight}" letter-spacing="{spacing}" text-anchor="{anchor}" '
        f'fill="{fill}" opacity="{opacity}">{esc(value)}</text>'
    )


def _extruded_text(x: float, y: float, value: str, size: int, fill: str, depth: str,
                   weight: int = 900, family: str = "Inter, Noto Sans CJK TC, Microsoft JhengHei, sans-serif",
                   layers: int = 9, dx: int = 2, dy: int = 2) -> str:
    """Layer exact glyphs into a deterministic faux-3D extrusion and metallic face."""
    chunks = []
    for i in range(layers, 0, -1):
        chunks.append(_text(x + dx * i, y + dy * i, value, size, depth, weight, family, spacing=1.1))
    chunks.append(
        f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
        f'letter-spacing="1.1" fill="{fill}" stroke="#fff9e9" stroke-opacity="0.72" stroke-width="1.2">'
        f'<title>{esc(value)}</title>{esc(value)}</text>'
    )
    return "".join(chunks)


def build_svg(
    source_bytes: bytes,
    mime_type: str,
    width: int,
    height: int,
    metadata: dict[str, Any],
) -> str:
    metadata = dict(metadata)
    if str(metadata.get("layout") or "plaque") == "diegetic":
        from bubble_break.boundary_pedestrian_diegetic_text import build_diegetic_svg
        return build_diegetic_svg(
            source_bytes, mime_type, width, height, metadata,
            text_fn=_text,
            palettes=PALETTES,
            treatments=TYPOGRAPHY_TREATMENTS,
            vfx_table=DIEGETIC_VFX,
            canonical_text_payload=canonical_text_payload,
            text_content_sha256=text_content_sha256,
        )
    metadata.setdefault("poster_panel_area_fraction", 0.44 * 0.78)
    metadata.setdefault("typography_variant", "middle")
    payload = canonical_text_payload(metadata)
    metadata.setdefault("canonical_text_payload", payload)
    metadata.setdefault("text_content_sha256", text_content_sha256(metadata))
    scale = max(0.45, min(width / 1920.0, height / 1080.0))
    variant = str(metadata.get("typography_variant", "middle"))
    p = TYPOGRAPHY_TREATMENTS.get(
        variant,
        PALETTES.get(str(metadata.get("style_id", "S01")), PALETTES["S01"]),
    )
    pad = max(18, round(36 * scale))
    panel_w = round(width * 0.44)
    panel_h = round(height * 0.78)
    panel_y = round(height * 0.10)
    panel_x = pad if metadata.get("panel_side") == "left" else width - panel_w - pad
    inset = round(30 * scale)
    tx = panel_x + inset
    max_tx = panel_x + panel_w - inset
    panel_right = panel_x + panel_w

    title_size = round(48 * scale)
    hero_size = round(87 * scale)
    label_size = round(22 * scale)
    small_size = round(16 * scale)
    line_gap = round(38 * scale)
    tryline = f"LOOP {metadata['loop_id']}   /   TRY {metadata['try_id']}"
    title_zh = "邊界行人"
    title_en = "THE BOUNDARY WALKER"
    series_line = f"{metadata.get('series_id') or 'SERIES-UNASSIGNED'}  ·  {metadata.get('world_label') or 'WORLD UNASSIGNED'}"
    method_line = f"{metadata.get('geometry_family') or 'GEO.?'}  /  {metadata.get('contact_method') or '?'}  ·  {metadata.get('method_label') or metadata['method_id']}"
    camera_pose_line = f"CAM {metadata.get('camera_id') or 'CAM-NA'}  ·  POSE {metadata.get('pose_id') or 'P-NA'}"
    style_prompt_line = f"STYLE {metadata.get('style_id') or 'S-NA'}  ·  PROMPT {metadata.get('prompt_id') or 'PROMPT-NA'}"
    status_line = str(metadata["status"]).replace("_", " ")
    note = str(metadata.get("note") or "每一次失敗，都帶來下一個試法。")
    data_uri = "data:" + mime_type + ";base64," + base64.b64encode(source_bytes).decode("ascii")

    # The plaque is deliberately ~32% of the full canvas area, not a tiny corner watermark.
    # It is a floating glass/metal 3D-poster composition with a large, extruded TRY wordmark.
    plaque = f'''
    <g id="floating-3d-poster" filter="url(#panelShadow)">
      <path d="M {panel_x+12} {panel_y+32}
               L {panel_x+panel_w-22} {panel_y}
               L {panel_x+panel_w} {panel_y+panel_h-34}
               L {panel_x+38} {panel_y+panel_h}
               Z"
            fill="{p['deep']}" fill-opacity="0.82" stroke="{p['edge']}" stroke-width="{max(2,round(3*scale))}"/>
      <path d="M {panel_x+27} {panel_y+52}
               L {panel_x+panel_w-39} {panel_y+22}
               L {panel_x+panel_w-20} {panel_y+panel_h-55}"
            fill="none" stroke="{p['metal']}" stroke-opacity="0.88" stroke-width="{max(2,round(3*scale))}"/>
      <path d="M {panel_x+31} {panel_y+panel_h-34} L {panel_x+panel_w-43} {panel_y+panel_h-70}"
            fill="none" stroke="{p['edge']}" stroke-width="{max(1,round(2*scale))}" stroke-opacity="0.75"/>
      <path d="M {panel_x+panel_w-65} {panel_y+75} l 25 -12 l 12 25 l -25 12 Z"
            fill="{p['metal']}" fill-opacity="0.86"/>
      <circle cx="{panel_x+panel_w-48}" cy="{panel_y+90}" r="{round(18*scale)}"
              fill="none" stroke="{p['deep']}" stroke-width="{max(2,round(4*scale))}"/>
      <text x="{panel_right-inset}" y="{panel_y+round(40*scale)}" text-anchor="end"
            fill="{p['edge']}" font-family="Inter, Arial, sans-serif" font-size="{small_size}" font-weight="800"
            letter-spacing="{max(1,round(3*scale))}">ART / METHOD / LOOP</text>
      {_extruded_text(tx, panel_y+round(98*scale), title_zh, title_size, p['ink'], p['shadow'], family="Noto Serif CJK TC, KaiTi, serif", layers=10, dx=2, dy=3)}
      {_text(tx, panel_y+round(130*scale), title_en, small_size, p['edge'], 850, spacing=2.5)}
      {_extruded_text(tx, panel_y+round(230*scale), tryline, round(38*scale), p['metal'], p['shadow'], layers=8, dx=2, dy=2)}
      {_text(tx, panel_y+round(276*scale), "THIS LOOP'S PHYSICAL METHOD", small_size, p['edge'], 800, spacing=2.1)}
      {_extruded_text(tx, panel_y+round(331*scale), str(metadata['method_id']), hero_size, p['ink'], p['shadow'], layers=10, dx=2, dy=3)}
      {_text(tx, panel_y+round(378*scale), method_line, label_size, p['metal'], 850)}
      {_text(tx, panel_y+round(420*scale), camera_pose_line, label_size, p['edge'], 750)}
      {_text(tx, panel_y+round(462*scale), style_prompt_line, label_size, p['ink'], 700)}
      {_text(tx, panel_y+round(510*scale), series_line, small_size, p['metal'], 750)}
      {_text(tx, panel_y+round(535*scale), payload.get('l_sha12', ''), small_size, p['edge'], 800)}
      <path d="M {tx} {panel_y+round(555*scale)} L {panel_right-inset} {panel_y+round(555*scale)}"
            stroke="{p['edge']}" stroke-opacity="0.7" stroke-width="{max(1,round(1.5*scale))}"/>
      {_text(tx, panel_y+round(578*scale), f"STATUS  {status_line}", label_size, p['ink'], 850)}
      {_text(tx, panel_y+round(619*scale), f"SHA-256  {metadata['source_sha256'][:18]}…", small_size, p['edge'], 700)}
      {_text(tx, panel_y+round(660*scale), note, small_size, p['ink'], 500)}
      <text x="{panel_x+panel_w-round(26*scale)}" y="{panel_y+panel_h-round(20*scale)}"
            font-family="Inter, Arial, sans-serif" font-size="{small_size}" fill="{p['edge']}" text-anchor="end"
            letter-spacing="2">BW / {esc(metadata['loop_id'])}</text>
    </g>
    '''
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <title>{esc(title_zh)} / {esc(title_en)} — {esc(tryline)}</title>
  <desc>Floating 3D poster artwork layer. Exact method typography is deterministic; source image pixels are embedded unchanged. Frame typography variant: {esc(metadata.get("typography_variant", "middle"))}; stable text SHA-256: {esc(metadata.get("text_content_sha256", ""))}.</desc>
  <metadata>{esc(json.dumps(metadata, ensure_ascii=False, sort_keys=True))}</metadata>
  <defs>
    <linearGradient id="metalFace" x1="0" y1="0" x2="0.9" y2="1">
      <stop offset="0" stop-color="#fffbe8"/>
      <stop offset="0.24" stop-color="{p['metal']}"/>
      <stop offset="0.55" stop-color="{p['edge']}"/>
      <stop offset="0.78" stop-color="{p['ink']}"/>
      <stop offset="1" stop-color="{p['metal']}"/>
    </linearGradient>
    <linearGradient id="glass" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.30"/>
      <stop offset="0.45" stop-color="{p['edge']}" stop-opacity="0.08"/>
      <stop offset="1" stop-color="{p['deep']}" stop-opacity="0.70"/>
    </linearGradient>
    <filter id="panelShadow" x="-25%" y="-20%" width="155%" height="150%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="{round(16*scale)}" result="blur"/>
      <feOffset in="blur" dx="{round(12*scale)}" dy="{round(20*scale)}" result="offsetBlur"/>
      <feColorMatrix in="offsetBlur" type="matrix"
        values="0 0 0 0 0.01  0 0 0 0 0.02  0 0 0 0 0.08  0 0 0 0.85 0" result="shadow"/>
      <feMerge><feMergeNode in="shadow"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="titleGlow" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="{round(3*scale)}" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <image x="0" y="0" width="{width}" height="{height}" preserveAspectRatio="xMidYMid meet"
         href="{data_uri}" xlink:href="{data_uri}"/>
  <rect x="0" y="0" width="{width}" height="{height}" fill="url(#glass)" opacity="0.08"/>
  {plaque}
  <g id="floating-poster-accent" fill="none" stroke="{p['metal']}" stroke-opacity="0.82" stroke-width="{max(1,round(2*scale))}">
    <path d="M {panel_x} {panel_y+round(30*scale)} C {panel_x-round(100*scale)} {panel_y-round(35*scale)}, {panel_x-round(120*scale)} {panel_y+round(120*scale)}, {panel_x-round(50*scale)} {panel_y+round(155*scale)}" />
    <circle cx="{panel_x+round(26*scale)}" cy="{panel_y+round(70*scale)}" r="{round(38*scale)}" stroke="{p['edge']}" stroke-width="{max(2,round(4*scale))}"/>
    <path d="M {panel_x+round(8*scale)} {panel_y+round(70*scale)} h {round(36*scale)} M {panel_x+round(26*scale)} {panel_y+round(52*scale)} v {round(36*scale)}" />
  </g>
</svg>
'''
    return svg


def ass_escape(value: Any) -> str:
    return str(value if value is not None else "").replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}").replace("\n", "\\N")


def ass_time(seconds: float) -> str:
    centiseconds = int(round(max(0.0, seconds) * 100))
    hours, rem = divmod(centiseconds, 360000)
    minutes, rem = divmod(rem, 6000)
    secs, cs = divmod(rem, 100)
    return f"{hours}:{minutes:02d}:{secs:02d}.{cs:02d}"


def build_ass(metadata: dict[str, Any], duration_seconds: float) -> str:
    """Build a large, beveled-looking title/method lower-third layer for a video clip."""
    if duration_seconds <= 0:
        raise ValueError("duration_seconds must be greater than zero")
    title_end = min(3.5, duration_seconds)
    title_text = ass_escape("邊界行人 / THE BOUNDARY WALKER")
    tryline = ass_escape(f"LOOP {metadata['loop_id']}  ·  TRY {metadata['try_id']}")
    method = ass_escape(f"{metadata['method_id']}  /  {metadata.get('method_label') or ''}")
    world = ass_escape(
        f"{metadata.get('series_id') or 'SERIES'}  ·  {metadata.get('world_label') or 'WORLD'}"
        f"  ·  {canonical_text_payload(metadata).get('l_sha12', '')}"
    )
    content_hash = str(metadata.get("text_content_sha256") or text_content_sha256(metadata))
    meta = ass_escape(
        f"GEO {metadata.get('geometry_family') or '?'} / CONTACT {metadata.get('contact_method') or '?'}"
        f" / CAM {metadata.get('camera_id') or '?'} / POSE {metadata.get('pose_id') or '?'}"
        f" / STYLE {metadata.get('style_id') or '?'} / PROMPT {metadata.get('prompt_id') or '?'}"
        f" / TEXT SHA-256 {content_hash}"
    )
    status = ass_escape(str(metadata.get("status", DEFAULT_STATUS)).replace("_", " "))
    return "\n".join([
        "[Script Info]",
        "Title: THE BOUNDARY WALKER — 3D TRY TITLE",
        "ScriptType: v4.00+",
        "WrapStyle: 2",
        "ScaledBorderAndShadow: yes",
        "PlayResX: 1920",
        "PlayResY: 1080",
        "",
        "[V4+ Styles]",
        "Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding",
        "Style: Title,Microsoft JhengHei,48,&H00F8F5E8,&H000000FF,&HCC06111C,&HAA06111C,1,0,0,0,100,100,2,0,1,4,6,7,54,54,48,1",
        "Style: Try,Arial,44,&H007ACDFF,&H00FFFFFF,&HCC06111C,&HAA06111C,1,0,0,0,100,100,2,0,1,4,6,7,54,54,48,1",
        "Style: Meta,Arial,24,&H00FFFFFF,&H000000FF,&HCC06111C,&HAA06111C,1,0,0,0,100,100,1,0,1,3,4,7,54,54,48,1",
        "Style: Status,Arial,20,&H00B0E8E8,&H000000FF,&HCC06111C,&HAA06111C,1,0,0,0,100,100,1,0,1,3,4,7,54,54,48,1",
        "",
        "[Events]",
        "Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text",
        f"Dialogue: 2,{ass_time(0)},{ass_time(title_end)},Title,,0,0,0,,{title_text}\\N{{\\fs27\\c&H00D8E6FF&}}{world}",
        f"Dialogue: 2,{ass_time(0)},{ass_time(duration_seconds)},Try,,0,0,0,,{tryline}\\N{method}",
        f"Dialogue: 1,{ass_time(0)},{ass_time(duration_seconds)},Meta,,0,0,0,,{meta}\\N{{\\fs18}}SHA-256 {metadata['source_sha256'][:18]}…  ·  {status}",
        "",
    ])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", required=True, help="source PNG/JPEG; source pixels are embedded unchanged")
    parser.add_argument("--out", required=True, help="output SVG poster artwork")
    parser.add_argument("--label-manifest", default="", help="JSON containing art_label_spec, such as one line exported from the product matrix")
    parser.add_argument("--loop-id", default="")
    parser.add_argument("--try-id", default="")
    parser.add_argument("--act-id", default="")
    parser.add_argument("--method-id", default="")
    parser.add_argument("--method-label", default="")
    parser.add_argument("--series-id", default="")
    parser.add_argument("--world-label", default="")
    parser.add_argument("--geometry-family", default="")
    parser.add_argument("--contact-method", default="")
    parser.add_argument("--camera-id", default="")
    parser.add_argument("--pose-id", default="")
    parser.add_argument("--prompt-id", default="")
    parser.add_argument("--style-id", default="")
    parser.add_argument("--typography-variant", choices=["", "before", "middle", "after", "video-lock"], default="")
    parser.add_argument("--layout", choices=["", "plaque", "diegetic"], default="")
    parser.add_argument("--vfx-mode", choices=["", "none", "lightning", "fire", "graffiti", "ice"], default="")
    parser.add_argument("--mid-master-sha256", default="")
    parser.add_argument("--note", default="")
    parser.add_argument("--panel-side", choices=["left", "right"], default="")
    parser.add_argument("--status", default="", choices=["", *sorted(ALLOWED_STATUSES)])
    parser.add_argument("--manifest-out", default="")
    parser.add_argument("--ass-out", default="", help="optional video TRY typography layer")
    parser.add_argument("--duration-seconds", type=float, default=6.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_path = Path(args.image)
    output_path = Path(args.out)
    if not source_path.is_file():
        raise FileNotFoundError(f"Source image does not exist: {source_path}")
    source = source_path.read_bytes()
    width, height = image_size(source)
    mime_type = mimetypes.guess_type(source_path.name)[0]
    if mime_type not in {"image/png", "image/jpeg"}:
        raise ValueError("Only PNG and JPEG sources are supported")
    label_spec: dict[str, Any] = {}
    act_spec: dict[str, Any] = {}
    if args.label_manifest:
        manifest_path = Path(args.label_manifest)
        if not manifest_path.is_file():
            raise FileNotFoundError(f"Label manifest does not exist: {manifest_path}")
        loaded = json.loads(manifest_path.read_text(encoding="utf-8"))
        label_spec = loaded.get("art_label_spec", loaded)
        selected_act = args.act_id or str(label_spec.get("act_id") or "3")
        acts = label_spec.get("acts") or {}
        act_spec = acts.get(selected_act) or acts.get(str(selected_act)) or {}
    else:
        selected_act = args.act_id
    def choose(cli_value: Any, spec_key: str, fallback: Any = "") -> Any:
        if cli_value not in (None, ""):
            return cli_value
        return act_spec.get(spec_key) or label_spec.get(spec_key) or fallback

    loop_id = choose(args.loop_id, "loop_id")
    try_id = choose(args.try_id, "try_id")
    act_id = choose(args.act_id, "act_id", selected_act)
    method_id = choose(args.method_id, "method_id")
    if not loop_id or not try_id or not act_id or not method_id:
        raise ValueError("Provide --loop-id/--try-id/--act-id/--method-id or pass --label-manifest with these fields")
    status = validate_status(args.status or choose("", "status", DEFAULT_STATUS))
    metadata: dict[str, Any] = {
        "story": label_spec.get("story") or "THE BOUNDARY WALKER",
        "loop_id": loop_id,
        "try_id": try_id,
        "act_id": str(act_id),
        "method_id": method_id,
        "method_label": choose(args.method_label, "method_label"),
        "series_id": choose(args.series_id, "series_id", "SERIES-UNASSIGNED"),
        "world_label": choose(args.world_label, "world_label", "WORLD-UNASSIGNED"),
        "geometry_family": choose(args.geometry_family, "geometry_family"),
        "contact_method": choose(args.contact_method, "contact_method"),
        "camera_id": choose(args.camera_id, "camera_id"),
        "pose_id": choose(args.pose_id, "pose_id"),
        "prompt_id": choose(args.prompt_id, "prompt_id"),
        "style_id": choose(args.style_id, "style_id", "S01"),
        "typography_variant": choose(args.typography_variant, "typography_variant", "middle"),
        "layout": choose(args.layout, "layout", "plaque"),
        "vfx_mode": choose(args.vfx_mode, "vfx_mode", ""),
        "mid_master_sha256": choose(args.mid_master_sha256, "mid_master_sha256", ""),
        "panel_side": choose(args.panel_side, "panel_side", "right"),
        "status": status,
        "note": choose(args.note, "note", "每一次失敗，都帶來下一個試法。"),
        "source_path": str(source_path),
        "source_sha256": sha256_bytes(source),
        "source_width": width,
        "source_height": height,
        "poster_panel_area_fraction": 0.0 if choose(args.layout, "layout", "plaque") == "diegetic" else 0.44 * 0.78,
        "image_realization": "SOURCE_FILE_ATTACHED",
        "pixel_audit_status": "NOT_RUN",
        "visual_acceptance_status": "NOT_VERIFIED",
        "renderer": "boundary_pedestrian_try_art.py",
    }
    metadata["canonical_text_payload"] = canonical_text_payload(metadata)
    metadata["text_content_sha256"] = text_content_sha256(metadata)
    metadata["l_sha12"] = metadata["canonical_text_payload"]["l_sha12"]
    svg = build_svg(source, mime_type, width, height, metadata)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(svg, encoding="utf-8")
    metadata["artwork_path"] = str(output_path)
    metadata["artwork_sha256"] = sha256_bytes(svg.encode("utf-8"))
    manifest_path = Path(args.manifest_out) if args.manifest_out else output_path.with_suffix(".manifest.json")
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.ass_out:
        ass_path = Path(args.ass_out)
        ass_path.parent.mkdir(parents=True, exist_ok=True)
        ass_path.write_text(build_ass(metadata, args.duration_seconds), encoding="utf-8")
    print(json.dumps({
        "artwork": str(output_path),
        "manifest": str(manifest_path),
        "source_sha256": metadata["source_sha256"],
        "artwork_sha256": metadata["artwork_sha256"],
        "poster_panel_area_fraction": metadata["poster_panel_area_fraction"],
        "layout": metadata.get("layout"),
        "l_sha12": metadata.get("l_sha12"),
        "vfx_mode": metadata.get("vfx_mode") or None,
        "pixel_audit_status": metadata["pixel_audit_status"],
        "visual_acceptance_status": metadata["visual_acceptance_status"],
        "ass_out": args.ass_out or None,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
