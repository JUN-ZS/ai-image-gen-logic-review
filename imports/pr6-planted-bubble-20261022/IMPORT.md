# PR #6 planted-bubble closed-loop import (2026-10-22)

Source: real seven-stage Gemini run evidence aligned to PR #6 head `0f849421`.

## Laid into this branch

- `out/planted_bubble_closed_loop/` — gates (parent/raw/masks/composited/audit), locked rasters, strip, evidence board, manifest
- `imports/pr6-planted-bubble-20261022/ai-image-gen-logic-review-pr6-planted-bubble.zip` — full package archive
- `imports/pr6-planted-bubble-20261022/chips/` — chat attachments as-received (alternate py snapshots + jfif + manifest)

## Explicitly NOT applied

Chat/zip `bubble_break/*.py` snapshots are **not** copied over live `bubble_break/` on this branch.
PR head already has the live Gemini Interactions API adapter and closed-loop engine at `0f849421`; overwriting would regress that.

`visual_acceptance_status` / `code_visual_acceptance_status` remain human-gated (`NOT_VERIFIED_BY_CODE`).
