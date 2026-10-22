# H9 — Grok Imagine Planted-Cylinder Bubble-Break (no Gemini key)

## Why H9 exists

PR #6 (`feat/gemini-planted-bubble-closed-loop-20261022`) correctly restored the
**planted double-ended cylinder** contract and Gemini adapters, but a live
`GEMINI_API_KEY` run is optional and must not block iteration.

**H9** is a parallel closed-loop track:

| | Gemini track (PR #6) | **H9 Imagine track** |
|--|--|--|
| Provider | Google Interactions API | **Grok Imagine** serial full-frame |
| Secret | `GEMINI_API_KEY` | **none** |
| Geometry contract | same `PLANTED_DOUBLE_ENDED_CYLINDER_BUBBLE_CONTACT_V1` | **same** |
| Stages | B→C→D1→D2→D3→E_MID→E_END | **same** |
| Visual acceptance | `NOT_VERIFIED_BY_CODE` until human | **same** |

H9 does **not** claim Shannon channel theorems about transformers; it reuses the
same stage prompt stack and proven locks (side-middle handle, outer-end empty,
P seat glow, no new handle, mini person, serial full-frame).

## Module

- `bubble_break/imagine_planted_bubble_h9.py`
- `bubble_break/test_imagine_planted_bubble_h9.py`

## Commands

```bash
# 1) Compile prompts from B3 master (+ person ref)
python -m bubble_break.imagine_planted_bubble_h9 compile \
  --master-b3 path/to/B3.jpg \
  --person-ref path/to/her.jpg \
  --outdir out/h9_packet

# 2) Agent / Imagine generates one full-frame per stage into a rasters folder
#    named exactly after STAGE_ORDER (see AGENT_PLAYBOOK.md in the packet).

# 3) Ingest hashes + filmstrip
python -m bubble_break.imagine_planted_bubble_h9 ingest \
  --packet-dir out/h9_packet \
  --rasters-dir out/h9_rasters \
  --outdir out/h9_run
```

## Proven geometry law (from dense-hammer LOG)

> 跳過「握既有左柄」會長新柄；鎖左柄像素後可壓住。

H9 playbooks therefore **forbid skipping D1/D2** and forbid multi-cell generation boards.

## Acceptance

Machine ingest PASS ≠ human visual PASS. Always keep
`code_visual_acceptance_status=NOT_VERIFIED_BY_CODE` until pixel review of
planted seat at P, side-middle handle, empty outer cap, and shell-only fracture.
