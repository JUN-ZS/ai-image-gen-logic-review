#!/usr/bin/env python3
"""v5 diegetic typography helpers for Boundary Walker try_art."""
from __future__ import annotations

import base64
import hashlib
import html
import json
from typing import Any, Callable

# Local imports kept loose so try_art can pass helpers

def esc(value: Any) -> str:
    return html.escape(str(value if value is not None else ""), quote=True)


def variable_glyph_text(
    text_fn: Callable,
    x: float,
    y: float,
    value: str,
    base_size: int,
    fill: str,
    *,
    weight: int = 900,
    family: str = "Inter, Noto Sans CJK TC, Microsoft JhengHei, sans-serif",
    min_scale: float = 0.55,
    max_scale: float = 2.40,
    seed: str = "",
    depth: str | None = None,
) -> str:
    if not value:
        return ""
    digest = hashlib.sha256((seed + "|" + value).encode("utf-8")).digest()
    cursor = float(x)
    chunks: list[str] = []
    for i, ch in enumerate(value):
        b = digest[i % len(digest)]
        t = b / 255.0
        scale = min_scale if ch.isspace() else (min_scale + (max_scale - min_scale) * t)
        size = max(8, int(round(base_size * scale)))
        advance = size * (0.62 if not ch.isspace() else 0.35)
        gy = y - (size - base_size) * 0.35
        if depth:
            for layer in range(6, 0, -1):
                chunks.append(text_fn(cursor + layer * 1.4, gy + layer * 1.4, ch, size, depth, weight, family))
        chunks.append(text_fn(cursor, gy, ch, size, fill, weight, family))
        cursor += advance
    return "".join(chunks)


def diegetic_vfx_layer(width: int, height: int, vfx: str, scale: float, conf: dict[str, Any]) -> str:
    if conf.get("opacity", 0) <= 0:
        return ""
    stroke, glow, op = conf["stroke"], conf["glow"], conf["opacity"]
    cx, cy = width * 0.62, height * 0.55
    r = min(width, height) * 0.18
    sw = max(2, round(3 * scale))
    if vfx == "lightning":
        paths = []
        for k in range(5):
            paths.append(
                f'<path d="M {cx + r * 0.2:.1f} {cy - r * 0.1:.1f} '
                f'q {r * (0.4 + 0.1 * k):.1f} {r * (-0.5 + 0.15 * k):.1f} {r * 0.9:.1f} {r * (0.2 * k - 0.3):.1f} '
                f't {r * 0.5:.1f} {r * 0.4:.1f}" fill="none" stroke="{stroke}" stroke-width="{sw}" '
                f'stroke-opacity="{op}" filter="url(#vfxGlow)"/>'
            )
        return f'<g id="diegetic-vfx-lightning" opacity="{op}">' + "".join(paths) + "</g>"
    if vfx == "fire":
        return (
            f'<g id="diegetic-vfx-fire" opacity="{op}">'
            f'<path d="M {cx - r * 0.3:.1f} {cy + r * 0.4:.1f} '
            f'C {cx - r:.1f} {cy - r * 0.2:.1f}, {cx:.1f} {cy - r * 1.1:.1f}, {cx + r * 0.2:.1f} {cy - r * 0.1:.1f} '
            f'C {cx + r * 0.8:.1f} {cy + r * 0.2:.1f}, {cx + r * 0.3:.1f} {cy + r * 0.9:.1f}, {cx - r * 0.3:.1f} {cy + r * 0.4:.1f} Z" '
            f'fill="{glow}" fill-opacity="0.25" stroke="{stroke}" stroke-width="{max(2, round(2 * scale))}"/>'
            f"</g>"
        )
    if vfx == "graffiti":
        return (
            f'<g id="diegetic-vfx-graffiti" opacity="{op}">'
            f'<path d="M {width * 0.08:.1f} {height * 0.82:.1f} L {width * 0.42:.1f} {height * 0.88:.1f} '
            f'L {width * 0.38:.1f} {height * 0.94:.1f} L {width * 0.06:.1f} {height * 0.90:.1f} Z" '
            f'fill="none" stroke="{stroke}" stroke-width="{max(3, round(4 * scale))}" stroke-linejoin="round"/>'
            f'<path d="M {width * 0.10:.1f} {height * 0.86:.1f} Q {width * 0.25:.1f} {height * 0.78:.1f} '
            f'{width * 0.36:.1f} {height * 0.90:.1f}" fill="none" stroke="{glow}" '
            f'stroke-width="{max(2, round(3 * scale))}"/>'
            f"</g>"
        )
    return (
        f'<g id="diegetic-vfx-ice" opacity="{op}">'
        f'<path d="M {cx:.1f} {cy - r:.1f} L {cx + r * 0.3:.1f} {cy - r * 0.2:.1f} '
        f'L {cx + r * 0.05:.1f} {cy + r * 0.2:.1f} L {cx - r * 0.25:.1f} {cy:.1f} Z" '
        f'fill="{glow}" fill-opacity="0.18" stroke="{stroke}" stroke-width="{max(1, round(2 * scale))}"/>'
        f'<path d="M {cx - r * 0.4:.1f} {cy + r * 0.1:.1f} L {cx + r * 0.5:.1f} {cy + r * 0.35:.1f}" '
        f'stroke="{stroke}" stroke-width="{max(1, round(2 * scale))}"/>'
        f"</g>"
    )


def build_diegetic_svg(
    source_bytes: bytes,
    mime_type: str,
    width: int,
    height: int,
    metadata: dict[str, Any],
    *,
    text_fn: Callable,
    palettes: dict,
    treatments: dict,
    vfx_table: dict,
    canonical_text_payload: Callable,
    text_content_sha256: Callable,
) -> str:
    metadata = dict(metadata)
    metadata.setdefault("layout", "diegetic")
    metadata.setdefault("typography_variant", "middle")
    metadata["poster_panel_area_fraction"] = 0.0
    payload = canonical_text_payload(metadata)
    metadata.setdefault("canonical_text_payload", payload)
    metadata.setdefault("text_content_sha256", text_content_sha256(metadata))
    metadata["l_sha12"] = payload["l_sha12"]
    scale = max(0.45, min(width / 1920.0, height / 1080.0))
    variant = str(metadata.get("typography_variant", "middle"))
    p = treatments.get(variant, palettes.get(str(metadata.get("style_id", "S01")), palettes["S01"]))
    vfx = str(metadata.get("vfx_mode") or "")
    if not vfx:
        vfx = {"before": "ice", "after": "fire"}.get(variant, "lightning")
    conf = vfx_table.get(vfx, vfx_table["none"])
    data_uri = "data:" + mime_type + ";base64," + base64.b64encode(source_bytes).decode("ascii")
    seed = payload["l_sha12"] + "|" + str(metadata.get("try_id") or "")
    title_zh, title_en = "邊界行人", "THE BOUNDARY WALKER"
    method = str(metadata.get("method_label") or metadata.get("method_id") or "")
    cam_pose = (
        f"{metadata.get('camera_id') or 'CAM'} · {metadata.get('pose_id') or 'P'} · "
        f"{metadata.get('style_id') or 'S'} · {metadata.get('prompt_id') or 'PID'}"
    )
    tryline = f"LOOP {metadata.get('loop_id', '')} / TRY {metadata.get('try_id', '')}"
    parts = [
        variable_glyph_text(text_fn, width * 0.04, height * 0.12, title_zh, round(52 * scale), p["ink"],
                            weight=900, family="Noto Serif CJK TC, KaiTi, serif", seed=seed + "|zh", depth=p["shadow"]),
        variable_glyph_text(text_fn, width * 0.04, height * 0.18, title_en, round(22 * scale), p["edge"],
                            weight=800, seed=seed + "|en", min_scale=0.7, max_scale=1.6),
        variable_glyph_text(text_fn, width * 0.48, height * 0.28, method, round(34 * scale), p["metal"],
                            weight=900, seed=seed + "|method", depth=p["shadow"]),
        variable_glyph_text(text_fn, width * 0.48, height * 0.36, tryline, round(24 * scale), p["edge"],
                            weight=800, seed=seed + "|try", min_scale=0.65, max_scale=1.8),
        variable_glyph_text(text_fn, width * 0.05, height * 0.88, cam_pose, round(18 * scale), p["ink"],
                            weight=700, seed=seed + "|cam", min_scale=0.6, max_scale=1.5),
        variable_glyph_text(text_fn, width * 0.05, height * 0.94, payload["world_lsha"], round(20 * scale), p["metal"],
                            weight=800, seed=seed + "|world", min_scale=0.7, max_scale=1.7),
    ]
    vfx_layer = diegetic_vfx_layer(width, height, vfx, scale, conf)
    meta_json = esc(json.dumps(metadata, ensure_ascii=False, sort_keys=True))
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{width}" height="{height}" viewBox="0 0 {width} {height}">\n'
        f'  <title>{esc(title_zh)} / {esc(title_en)} - diegetic v5</title>\n'
        f'  <desc>Diegetic spatial typography (v5): zero backing plate, variable glyph scale 0.55x-2.40x, '
        f'{esc(payload["l_sha12"])}, VFX={esc(conf["label"])}. Exact strings from compiler; source embedded. '
        f'text_content_sha256={esc(metadata.get("text_content_sha256", ""))}.</desc>\n'
        f'  <metadata>{meta_json}</metadata>\n'
        f'  <defs><filter id="vfxGlow" x="-40%" y="-40%" width="180%" height="180%">'
        f'<feGaussianBlur stdDeviation="{round(4 * scale)}" result="b"/>'
        f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>\n'
        f'  <image x="0" y="0" width="{width}" height="{height}" preserveAspectRatio="xMidYMid meet" '
        f'href="{data_uri}" xlink:href="{data_uri}"/>\n'
        f'  {vfx_layer}\n'
        f'  <g id="diegetic-typography">{"".join(parts)}</g>\n'
        f'</svg>\n'
    )
