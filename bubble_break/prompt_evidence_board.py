#!/usr/bin/env python3
"""Render an exact, traceable SVG teaching/acceptance board for one image attempt.

The generator does not call an image model and never infers visual PASS from prompt text.
It embeds the supplied raster unchanged inside an SVG and adds deterministic metadata labels.
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


W, H = 1920, 1080
VALID_AUDIT = {"NOT_RUN", "PENDING", "PASS", "FAIL", "UNVERIFIED"}
VALID_IMAGE = {"NOT_RUN", "IMAGE_GENERATED", "BLOCKED", "SYNTHETIC_TEST_ONLY", "UNKNOWN"}


def esc(value: Any) -> str:
    return html.escape(str(value if value is not None else ""), quote=True)


def wrap_words(value: Any, limit: int = 50, max_lines: int = 3) -> list[str]:
    raw = str(value if value is not None else "").replace("\n", " ").strip()
    if not raw:
        return ["—"]
    # A character-wrap is deliberate: it works for Chinese text and machine IDs without
    # requiring external locale/font libraries. Preserve complete content in the JSON manifest.
    lines: list[str] = []
    while raw and len(lines) < max_lines:
        if len(raw) <= limit:
            lines.append(raw)
            raw = ""
        else:
            split = raw.rfind(" ", 0, limit + 1)
            if split < max(1, limit // 3):
                split = limit
            lines.append(raw[:split].rstrip())
            raw = raw[split:].lstrip()
    if raw and lines:
        lines[-1] = lines[-1][: max(1, limit - 1)] + "…"
    return lines or ["—"]


def text_el(x: float, y: float, value: Any, size: int = 22,
            color: str = "#e8f0fa", weight: int = 400,
            family: str = "Inter, Noto Sans CJK TC, Microsoft JhengHei, sans-serif") -> str:
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{color}">{esc(value)}</text>')


def multiline(x: float, y: float, value: Any, limit: int = 44,
              max_lines: int = 2, size: int = 21,
              color: str = "#e8f0fa", weight: int = 400,
              line_height: int = 27) -> str:
    return "".join(text_el(x, y + i * line_height, line, size, color, weight)
                   for i, line in enumerate(wrap_words(value, limit, max_lines)))


def rect(x: float, y: float, w: float, h: float, fill: str,
         stroke: str = "none", radius: int = 18, sw: int = 1) -> str:
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')


def image_size(path: Path, manifest: dict[str, Any]) -> tuple[int, int]:
    if manifest.get("image_width") and manifest.get("image_height"):
        return int(manifest["image_width"]), int(manifest["image_height"])
    data = path.read_bytes()
    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        return struct.unpack(">II", data[16:24])
    if data[:2] == b"\xff\xd8":
        i = 2
        sof = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
        while i + 4 <= len(data):
            if data[i] != 0xFF:
                i += 1
                continue
            while i < len(data) and data[i] == 0xFF:
                i += 1
            if i >= len(data):
                break
            marker = data[i]
            i += 1
            if marker in {0xD8, 0xD9, 0x01} or 0xD0 <= marker <= 0xD7:
                continue
            if i + 2 > len(data):
                break
            seg_len = int.from_bytes(data[i:i + 2], "big")
            if seg_len < 2 or i + seg_len > len(data):
                break
            if marker in sof and seg_len >= 7:
                h = int.from_bytes(data[i + 3:i + 5], "big")
                w = int.from_bytes(data[i + 5:i + 7], "big")
                return w, h
            i += seg_len
    return int(manifest.get("image_width", 16)), int(manifest.get("image_height", 9))


def audit_state(manifest: dict[str, Any], image_sha: str | None) -> tuple[str, str, str]:
    image_status = str(manifest.get("image_realization_status", "UNKNOWN")).upper()
    if image_status not in VALID_IMAGE:
        image_status = "UNKNOWN"
    audit = str(manifest.get("pixel_audit_status", "NOT_RUN")).upper()
    if audit not in VALID_AUDIT:
        audit = "UNVERIFIED"
    receipt = manifest.get("review_receipt")
    reason = ""
    if audit == "PASS":
        receipt_sha = str((receipt or {}).get("raster_sha256", "")).lower()
        verdict = str((receipt or {}).get("verdict", "")).upper()
        if not image_sha:
            audit, reason = "UNVERIFIED", "PASS rejected: no source raster attached"
        elif receipt_sha != image_sha.lower() or verdict != "PASS":
            audit, reason = "UNVERIFIED", "PASS rejected: reviewer receipt missing or raster SHA mismatch"
    if audit == "FAIL" and not image_sha:
        reason = "FAIL label retained from manifest; source raster is not attached"
    return image_status, audit, reason


def build_svg(manifest: dict[str, Any], image_path: Path | None) -> str:
    attempt = str(manifest.get("attempt_id", "ATTEMPT-ID-MISSING"))
    branch = str(manifest.get("branch", "UNSPECIFIED"))
    commit = str(manifest.get("source_commit_sha", "UNPINNED"))
    topology = str(manifest.get("topology_id", "UNSPECIFIED"))
    prompt_id = str(manifest.get("prompt_id", manifest.get("variant_id", "UNSPECIFIED")))
    stage = str(manifest.get("stage_id", "UNSPECIFIED"))
    variables = manifest.get("variables_changed", {})
    if isinstance(variables, dict):
        variables_text = " · ".join(f"{k}={v}" for k, v in variables.items()) or "未記錄"
    elif isinstance(variables, list):
        variables_text = " · ".join(map(str, variables)) or "未記錄"
    else:
        variables_text = str(variables or "未記錄")
    expected = manifest.get("expected", {}) if isinstance(manifest.get("expected", {}), dict) else {}
    observed = manifest.get("observed", {}) if isinstance(manifest.get("observed", {}), dict) else {}
    failures = manifest.get("failure_reasons", [])
    if isinstance(failures, str):
        failures = [failures] if failures else []
    next_change = manifest.get("next_change", "未記錄")
    prompt_excerpt = manifest.get("prompt_excerpt", "未附 Prompt 摘要")
    image_sha = hashlib.sha256(image_path.read_bytes()).hexdigest() if image_path and image_path.is_file() else None
    image_status, audit_status, audit_reason = audit_state(manifest, image_sha)

    status_color = {
        "PASS": "#39d98a", "FAIL": "#ff5d6c", "PENDING": "#ffc857",
        "NOT_RUN": "#91a4ba", "UNVERIFIED": "#ff9f43"
    }.get(audit_status, "#91a4ba")

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#071425"/><stop offset="1" stop-color="#142b43"/></linearGradient>',
        '<linearGradient id="header" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#102a43"/><stop offset="1" stop-color="#173b55"/></linearGradient></defs>',
        '<rect width="1920" height="1080" fill="url(#bg)"/>',
        rect(36, 28, 1848, 112, "url(#header)", "#36516d", 24, 2),
        text_el(62, 72, "打泡實驗板  /  PROMPT → IMAGE → AUDIT", 33, "#f4f8ff", 700),
        text_el(64, 111, f"{attempt}   ·   {stage}   ·   {prompt_id}", 21, "#a6c2db", 500),
        rect(1510, 48, 340, 62, status_color, "none", 18),
        text_el(1532, 87, f"PIXEL AUDIT  ·  {audit_status}", 23, "#071425", 800),
    ]

    # Left: source raster. The image is embedded byte-for-byte; the overlay is a separate SVG.
    ix, iy, iw, ih = 58, 166, 1190, 666
    parts += [rect(ix, iy, iw, ih, "#08101a", "#44617b", 18, 2)]
    if image_path and image_path.is_file():
        raw = image_path.read_bytes()
        mime = mimetypes.guess_type(image_path.name)[0] or "application/octet-stream"
        uri = f"data:{mime};base64,{base64.b64encode(raw).decode('ascii')}"
        src_w, src_h = image_size(image_path, manifest)
        scale = min((iw - 18) / max(1, src_w), (ih - 18) / max(1, src_h))
        dw, dh = src_w * scale, src_h * scale
        dx, dy = ix + (iw - dw) / 2, iy + (ih - dh) / 2
        parts.append(f'<image href="{uri}" x="{dx:.2f}" y="{dy:.2f}" width="{dw:.2f}" height="{dh:.2f}" preserveAspectRatio="xMidYMid meet"/>')
        roi = manifest.get("contact_roi_norm")
        if isinstance(roi, dict) and all(k in roi for k in ("x", "y", "w", "h")):
            rx = dx + float(roi["x"]) * dw
            ry = dy + float(roi["y"]) * dh
            rw = float(roi["w"]) * dw
            rh = float(roi["h"]) * dh
            if 0 <= rx <= ix + iw and 0 <= ry <= iy + ih and rw > 0 and rh > 0:
                roi_color = "#39d98a" if audit_status == "PASS" else "#ff5d6c" if audit_status == "FAIL" else "#ffc857"
                parts.append(f'<rect x="{rx:.2f}" y="{ry:.2f}" width="{rw:.2f}" height="{rh:.2f}" fill="none" stroke="{roi_color}" stroke-width="4" stroke-dasharray="12 7"/>')
                parts.append(text_el(rx, max(iy + 28, ry - 10), "P / REVIEW ROI", 18, roi_color, 800))
        parts.append(text_el(ix + 18, iy + ih - 18, f"RASTER SHA-256  {image_sha[:24]}…", 17, "#e0eaf5", 500))
    else:
        parts += [
            rect(ix + 24, iy + 24, iw - 48, ih - 48, "#0d1b2b", "#536c83", 14, 2),
            text_el(ix + 100, iy + 280, "NO SOURCE RASTER ATTACHED", 34, "#ffc857", 800),
            text_el(ix + 100, iy + 326, "Prompt / geometry proxy alone is not image evidence.", 22, "#d4dfeb", 500),
            text_el(ix + 100, iy + 369, f"IMAGE REALIZATION  ·  {image_status}", 21, "#91a4ba", 700),
        ]

    # Right-side structured cards.
    rx, rw = 1270, 592
    parts += [rect(rx, 166, rw, 196, "#102238", "#294864", 16, 1),
              text_el(rx + 22, 201, "01  TRACE / 來源追溯", 22, "#80d5ff", 800),
              multiline(rx + 22, 237, f"Branch: {branch}", 49, 1, 18),
              multiline(rx + 22, 267, f"Commit: {commit}", 50, 1, 17, "#c2d2e2"),
              multiline(rx + 22, 299, f"Topology: {topology}", 49, 1, 19, "#f4f8ff", 600),
              multiline(rx + 22, 332, f"Prompt: {prompt_id}  |  Variant: {manifest.get('variant_id', '—')}", 50, 1, 17)]

    parts += [rect(rx, 378, rw, 192, "#102238", "#294864", 16, 1),
              text_el(rx + 22, 413, "02  VARIABLES / 本次改了什麼", 22, "#80d5ff", 800),
              multiline(rx + 22, 451, f"Changed: {variables_text}", 47, 3, 19),
              multiline(rx + 22, 535, f"Stage: {stage}  |  Image: {image_status}", 49, 1, 17, "#b8c9da")]

    expected_text = " · ".join(f"{k}={v}" for k, v in expected.items()) or "未填：不能從 Prompt 推定"
    observed_text = " · ".join(f"{k}={v}" for k, v in observed.items()) or "UNVERIFIED：尚無像素審查紀錄"
    parts += [rect(rx, 586, rw, 220, "#102238", "#294864", 16, 1),
              text_el(rx + 22, 621, "03  EXPECTED vs OBSERVED / 預期與實際", 22, "#80d5ff", 800),
              text_el(rx + 22, 657, "EXPECTED  / 公式預期", 18, "#8be0bb", 700),
              multiline(rx + 22, 685, expected_text, 47, 2, 19),
              text_el(rx + 22, 737, "OBSERVED  / 實際畫面", 18, "#ffbf69", 700),
              multiline(rx + 22, 765, observed_text, 47, 2, 19)]

    # Bottom row: fail diagnosis, next experiment and audit/provenance boundary.
    parts += [rect(58, 854, 580, 184, "#251b28", "#71404c", 16, 1),
              text_el(80, 890, "04  FAILURE REASONS / 失敗原因", 21, "#ff8792", 800)]
    fail_text = "；".join(str(x) for x in failures) if failures else "未記錄（不能自動判為成功）"
    parts.append(multiline(80, 926, fail_text, 42, 3, 20))
    parts += [rect(656, 854, 590, 184, "#102a33", "#28645c", 16, 1),
              text_el(678, 890, "05  NEXT CHANGE / 下一輪只改", 21, "#69e6c2", 800),
              multiline(678, 926, next_change, 44, 3, 20)]
    parts += [rect(1270, 822, 592, 216, "#162435", "#52657a", 16, 1),
              text_el(1292, 858, "06  AUDIT / 驗收證據", 21, "#e4edf7", 800),
              multiline(1292, 891, f"Pixel audit: {audit_status}", 48, 1, 19, status_color, 800),
              multiline(1292, 922, f"Review receipt: {(manifest.get('review_receipt') or {}).get('reviewer', 'MISSING')}", 48, 1, 17),
              multiline(1292, 951, f"Receipt SHA: {(manifest.get('review_receipt') or {}).get('raster_sha256', 'MISSING')}", 48, 1, 16, "#b8c9da"),
              multiline(1292, 983, audit_reason or "PASS 只在收據綁定相同 raster SHA 時顯示。", 49, 2, 16, "#b8c9da")]

    parts += [text_el(60, 1065, f"PROMPT EXCERPT: {prompt_excerpt}", 15, "#91a4ba", 400),
              text_el(1625, 1065, "FORMULA ≠ PIXEL PROOF", 15, "#91a4ba", 700),
              '</svg>']
    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, help="JSON attempt manifest")
    parser.add_argument("--image", help="actual source raster (PNG/JPEG etc.); omitted means no-image board")
    parser.add_argument("--out", required=True, help="output SVG evidence board")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise SystemExit("manifest root must be a JSON object")
    image_path = Path(args.image) if args.image else None
    if image_path is not None and not image_path.is_file():
        raise SystemExit(f"source raster does not exist: {image_path}")
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_svg(manifest, image_path), encoding="utf-8")
    print(json.dumps({
        "output_svg": str(output),
        "attempt_id": manifest.get("attempt_id", "ATTEMPT-ID-MISSING"),
        "source_raster_attached": bool(image_path),
        "source_raster_sha256": hashlib.sha256(image_path.read_bytes()).hexdigest() if image_path else None,
        "pixel_audit_displayed": audit_state(manifest, hashlib.sha256(image_path.read_bytes()).hexdigest() if image_path else None)[1],
        "note": "SVG board annotates evidence; it does not generate an image or validate pixels itself."
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
