# H9 Imagine agent playbook

1. Start from `sources/B3_MASTER…` as the Stage-B parent (or isolate to B if atlas was denser).
2. For each stage in order, open `prompts/<STAGE>.md` and run **one** full-frame Imagine
   image-to-image (or reference-to-image when person is introduced) edit.
3. Never skip D1/D2. First grip must lock existing side-handle pixels.
4. Save outputs as `rasters/<STAGE>.jpg` (or `.png`) with exact STAGE_ORDER names.
5. Run `python -m bubble_break.imagine_planted_bubble_h9 ingest …` to hash + filmstrip.

Aspect target: **16:9**
Contract: `PLANTED_DOUBLE_ENDED_CYLINDER_BUBBLE_CONTACT_V1` / fingerprint `7298dd8221fbe9b6372a1285d1d65df5de2b63aea5a4da9bbbf6137c2866aa41`
No `GEMINI_API_KEY` is used in H9.
