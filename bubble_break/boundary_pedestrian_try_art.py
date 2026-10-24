#!/usr/bin/env python3
"""Compose exact story/method typography over a source frame without altering its raster.

This tool does not generate images or verify geometry. It embeds the original raster in
an SVG and adds a deterministic editorial layer whose words come from explicit CLI values.
An optional ASS subtitle file gives video clips the same title/method identity.
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


def esc(value: Any) -> str:
    return html.escape(str(value if value is not None else ""), quote=True)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


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


def build_svg(
    source_bytes: bytes,
    mime_type: str,
    width: int,
    height: int,
    metadata: dict[str, Any],
) -> str:
    """Return a full-frame SVG with an embedded, unmodified source image."""
    scale = min(width / 1920.0, height / 1080.0)
    scale = max(scale, 0.45)
    title_size = round(47 * scale)
    subtitle_size = round(19 * scale)
    badge_size = round(23 * scale)
    small_size = round(16 * scale)
    pad = round(48 * scale)
    top_h = round(190 * scale)
    bottom_h = round(178 * scale)
    badge_x = round(width * 0.57)
    badge_y = round(height * 0.055)
    badge_w = round(width * 0.39)
    badge_h = round(116 * scale)
    label = (
        f"{metadata['method_id']}  /  {metadata['method_label']}"
        if metadata.get("method_label")
        else str(metadata["method_id"])
    )
    tryline = f"LOOP {metadata['loop_id']}  ·  TRY {metadata['try_id']}"
    promptline = (
        f"PROMPT {metadata.get('prompt_id') or 'UNSPECIFIED'}"
        f"  ·  STYLE {metadata.get('style_id') or 'UNSPECIFIED'}"
        f"  ·  ACT {metadata.get('act_id') or 'UNSPECIFIED'}"
    )
    status = str(metadata["status"]).replace("_", " ")
    note = str(metadata.get("note") or "每一次失敗，都帶來下一個試法。")

    data_uri = "data:" + mime_type + ";base64," + base64.b64encode(source_bytes).decode("ascii")
    title = "邊界行人"
    eng_title = "THE BOUNDARY WALKER"
    # Canvas matches the source raster's exact dimensions and aspect ratio. No crop or
    # resampling of the embedded source is requested; the overlay is a separate vector layer.
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <title>{esc(title)} / {esc(eng_title)}</title>
  <desc>Editorial TRY artwork overlay. The embedded source raster is preserved unchanged.</desc>
  <metadata>{esc(json.dumps(metadata, ensure_ascii=False, sort_keys=True))}</metadata>
  <defs>
    <linearGradient id="topShade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#06111c" stop-opacity="0.90"/>
      <stop offset="1" stop-color="#06111c" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="bottomShade" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0" stop-color="#06111c" stop-opacity="0.92"/>
      <stop offset="1" stop-color="#06111c" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="gold" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#f4cf83"/>
      <stop offset="0.55" stop-color="#fff0c5"/>
      <stop offset="1" stop-color="#8fe7e4"/>
    </linearGradient>
    <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="{max(2, round(3 * scale))}" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <image x="0" y="0" width="{width}" height="{height}"
         preserveAspectRatio="xMidYMid meet"
         href="{data_uri}" xlink:href="{data_uri}"/>
  <g id="editorial-art-layer">
    <rect x="0" y="0" width="{width}" height="{top_h}" fill="url(#topShade)"/>
    <rect x="0" y="{height-bottom_h}" width="{width}" height="{bottom_h}" fill="url(#bottomShade)"/>
    <path d="M {pad} {pad*0.75} H {round(width*0.23)}" stroke="url(#gold)" stroke-width="{max(2, round(2*scale))}" fill="none" filter="url(#softGlow)"/>
    <text x="{pad}" y="{pad+title_size}" fill="#fff7e6" font-family="Noto Serif CJK TC, Microsoft JhengHei, serif"
          font-size="{title_size}" font-weight="700" letter-spacing="{max(1, round(2*scale))}">{esc(title)}</text>
    <text x="{pad}" y="{pad+title_size+round(27*scale)}" fill="#bce8ee" font-family="Inter, Arial, sans-serif"
          font-size="{subtitle_size}" letter-spacing="{max(1, round(3*scale))}">{esc(eng_title)}</text>

    <rect x="{badge_x}" y="{badge_y}" width="{badge_w}" height="{badge_h}" rx="{round(18*scale)}"
          fill="#081825" fill-opacity="0.82" stroke="url(#gold)" stroke-width="{max(2, round(2*scale))}"/>
    <text x="{badge_x+round(22*scale)}" y="{badge_y+round(31*scale)}"
          fill="#e8d09a" font-family="Inter, Arial, sans-serif" font-size="{small_size}" font-weight="700"
          letter-spacing="{max(1, round(2*scale))}">{esc(tryline)}</text>
    <text x="{badge_x+round(22*scale)}" y="{badge_y+round(65*scale)}"
          fill="#f8fbff" font-family="Inter, Noto Sans CJK TC, sans-serif" font-size="{badge_size}" font-weight="700">{esc(label)}</text>
    <text x="{badge_x+round(22*scale)}" y="{badge_y+round(91*scale)}"
          fill="#a8d8e4" font-family="Inter, Noto Sans CJK TC, sans-serif" font-size="{small_size}">{esc(promptline)}</text>

    <path d="M {pad} {height-round(115*scale)} H {round(width*0.58)}" stroke="#81d8d5" stroke-opacity="0.8"
          stroke-width="{max(1, round(1.5*scale))}" fill="none"/>
    <text x="{pad}" y="{height-round(77*scale)}" fill="#fff5dc"
          font-family="Noto Sans CJK TC, Microsoft JhengHei, sans-serif" font-size="{round(22*scale)}">{esc(note)}</text>
    <text x="{pad}" y="{height-round(39*scale)}" fill="#9fc4d3"
          font-family="Inter, Noto Sans CJK TC, sans-serif" font-size="{small_size}">STATUS  {esc(status)}  ·  SOURCE SHA-256  {esc(metadata['source_sha256'][:12])}…</text>

    <rect x="{pad//2}" y="{pad//2}" width="{width-pad}" height="{height-pad}" rx="{round(8*scale)}"
          fill="none" stroke="#e6c982" stroke-opacity="0.35" stroke-width="{max(1, round(1.2*scale))}"/>
    <path d="M {pad//2} {pad*2} V {pad//2} H {pad*2} M {width-pad*2} {pad//2} H {width-pad//2} V {pad*2}
             M {pad//2} {height-pad*2} V {height-pad//2} H {pad*2}
             M {width-pad*2} {height-pad//2} H {width-pad//2} V {height-pad*2}"
          stroke="url(#gold)" stroke-width="{max(2, round(2*scale))}" fill="none"/>
  </g>
</svg>
'''


def ass_time(seconds: float) -> str:
    centiseconds = int(round(max(0.0, seconds) * 100))
    hours, rem = divmod(centiseconds, 360000)
    minutes, rem = divmod(rem, 6000)
    secs, cs = divmod(rem, 100)
    return f"{hours}:{minutes:02d}:{secs:02d}.{cs:02d}"


def ass_escape(value: Any) -> str:
    return str(value if value is not None else "").replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}").replace("\n", "\\N")


def build_ass(metadata: dict[str, Any], duration_seconds: float) -> str:
    """Build optional subtitle/lower-third labels for an independently rendered video clip."""
    if duration_seconds <= 0:
        raise ValueError("duration_seconds must be greater than zero")
    title_end = min(2.6, duration_seconds)
    method = f"{metadata['method_id']}  /  {metadata.get('method_label') or ''}"
    method = ass_escape(method.strip())
    label = ass_escape(
        f"LOOP {metadata['loop_id']}  ·  TRY {metadata['try_id']}   |   {metadata.get('status', DEFAULT_STATUS).replace('_', ' ')}"
    )
    title_text = ass_escape(f"邊界行人 / THE BOUNDARY WALKER   ·   ACT {metadata.get('act_id') or '?'}")
    return "\n".join([
        "[Script Info]",
        "Title: THE BOUNDARY WALKER TRY overlay",
        "ScriptType: v4.00+",
        "WrapStyle: 2",
        "ScaledBorderAndShadow: yes",
        "PlayResX: 1920",
        "PlayResY: 1080",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: Title,Microsoft JhengHei,34,&H00F8F5E8,&H000000FF,&HCC06111C,&H8806111C,1,0,0,0,100,100,1,0,1,3,1,7,52,52,42,1",
        "Style: Method,Arial,25,&H00FFFFFF,&H000000FF,&HCC06111C,&H8806111C,1,0,0,0,100,100,1,0,1,2,1,9,52,52,42,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
        f"Dialogue: 2,{ass_time(0)},{ass_time(title_end)},Title,,0,0,0,,{title_text}",
        f"Dialogue: 2,{ass_time(0)},{ass_time(duration_seconds)},Method,,0,0,0,,{method}\\N{label}",
        "",
    ])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", required=True, help="source PNG/JPEG; pixels are embedded unchanged")
    parser.add_argument("--out", required=True, help="output SVG artwork")
    parser.add_argument("--loop-id", required=True, help="loop/cycle ID, e.g. 001")
    parser.add_argument("--try-id", required=True, help="unique trial ID, e.g. 0001")
    parser.add_argument("--act-id", required=True, help="story act ID, e.g. 3")
    parser.add_argument("--method-id", required=True, help="catalog method ID, e.g. GEO.T")
    parser.add_argument("--method-label", default="", help="human-readable method label")
    parser.add_argument("--prompt-id", default="", help="source prompt ID such as I-04 or V-02")
    parser.add_argument("--style-id", default="", help="style block ID such as S-01")
    parser.add_argument("--note", default="每一次失敗，都帶來下一個試法。", help="short art caption")
    parser.add_argument("--status", default=DEFAULT_STATUS, choices=sorted(ALLOWED_STATUSES))
    parser.add_argument("--manifest-out", default="", help="optional JSON sidecar path")
    parser.add_argument("--ass-out", default="", help="optional ASS label overlay for the matching video clip")
    parser.add_argument("--duration-seconds", type=float, default=6.0, help="duration for optional ASS output")
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
    status = validate_status(args.status)
    metadata: dict[str, Any] = {
        "story": "THE BOUNDARY WALKER",
        "loop_id": args.loop_id,
        "try_id": args.try_id,
        "act_id": args.act_id,
        "method_id": args.method_id,
        "method_label": args.method_label,
        "prompt_id": args.prompt_id,
        "style_id": args.style_id,
        "status": status,
        "note": args.note,
        "source_path": str(source_path),
        "source_sha256": sha256_bytes(source),
        "source_width": width,
        "source_height": height,
        "image_realization": "SOURCE_FILE_ATTACHED",
        "pixel_audit_status": "NOT_RUN",
        "visual_acceptance_status": "NOT_VERIFIED",
        "renderer": "boundary_pedestrian_try_art.py",
    }
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
        "pixel_audit_status": metadata["pixel_audit_status"],
        "visual_acceptance_status": metadata["visual_acceptance_status"],
        "ass_out": args.ass_out or None,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
