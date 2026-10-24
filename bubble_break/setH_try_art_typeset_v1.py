#!/usr/bin/env python3
"""Deterministic SVG poster layer for SET-H. No model spelling. No TRY count. No REVIEW PENDING."""
# Full implementation lives in session artifacts; this stub documents the contract.
# Run path: clean frame → SVG (WenQuanYi) → cairosvg → TYPESET.jpg + .manifest.json
CONTRACT = {
    "forbidden_on_image": ["TRY_count", "REVIEW PENDING"],
    "loop_id": "L-{mid_sha256[:12]}",
    "variants": {"before": "PRE cold", "middle": "MID", "after": "POST hot"},
    "font": "WenQuanYi Zen Hei",
    "heroine_lock_required": True,
    "heroine_id": "BW_HEROINE_SET_H_V1",
}
if __name__ == "__main__":
    import json
    print(json.dumps(CONTRACT, ensure_ascii=False, indent=2))
