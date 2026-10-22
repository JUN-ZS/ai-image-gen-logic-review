# Gemini Provider for the Shannon-Inspired Planted-Cylinder Bubble-Break Loop

## Canonical image task

This adapter is intentionally for `PLANTED_DOUBLE_ENDED_CYLINDER_BUBBLE_CONTACT_V1`, not the earlier flying-hammer/V5.1 task or the separate T-v-T experiment.

The tool is one double-ended solid cylinder planted radially on the containment bubble. Its curved base seat stays fully seated at the same point P; one pre-existing handle attaches at the cylinder side-middle and extends tangentially; the outer circular end cap remains clear. The object does not fly across a gap. The sequence is the seven-stage B → C → D1 → D2 → D3 → E-mid → E-end edit chain.

## What is connected

`bubble_break/gemini_planted_bubble_provider.py` implements the generic provider-command contract already consumed by `planted_bubble_closed_loop.py`.

For each pipeline attempt it makes **two real Gemini Interactions API calls**:

1. **Image generation/edit** with `GEMINI_IMAGE_MODEL` (default `gemini-nano-banana-2.1`). Stage B receives the hash-checked, human-selected source-ROI crop plus atlas context. Later stages receive the last accepted parent raster plus the request's edit/freeze masks and stage prompt.
2. **Semantic vision review** with `GEMINI_REVIEW_MODEL` (default `gemini-3.8-flash`). It inspects the exact generated raster and, when available, its accepted parent, returning structured JSON annotations matching the planted-cylinder validator. A model-generated `FAIL` is preserved as FAIL; it is never upgraded to PASS by adapter code.

The adapter reopens and normalizes the generated output as an actual PNG before hashing. It binds the review to the exact saved image SHA-256, the expected parent SHA, the master-anchor SHA, and the current stage. Invalid/missing model output or annotation records fail closed.

Official references: [Gemini image generation and editing](https://ai.google.dev/gemini-api/docs/image-generation) and [Gemini structured output](https://ai.google.dev/gemini-api/docs/structured-output). The default image model name is listed on Google's current [Gemini Nano Banana 2.1 model page](https://ai.google.dev/gemini-api/docs/models/gemini-nano-banana-2.1).

## Shannon-style feedback policy

`bubble_break/planted_bubble_information_gain.py` separates likely failure causes into source-ROI selection, cylinder seat/P geometry, handle track/axis, grip state, crack causality, sanctuary safety, and raster lineage. It ranks diagnostic actions by expected information gain divided by estimated cost. A failed gate becomes a rejection vector for the next request and selects a targeted inspection/edit emphasis.

The likelihoods are explicitly **`UNVALIDATED_ENGINEERING_PRIORS`**, not measured Gemini accuracy and not a claim that a generative model is a known memoryless communications channel. This ranking can decide *what to inspect or emphasize next*; it cannot override any hard gate, manufacture evidence, or turn a missing/ambiguous frame into PASS. Creativity/novelty scores are only used after all structural, state, and raster-binding gates pass.

## Setup (no key is stored in Git)

Use Python 3.11+, Pillow, and a Google AI Studio API key with access to the selected models. Do not paste the key into source code, a candidate manifest, a GitHub issue, or a commit.

Linux/macOS:

```bash
export GEMINI_API_KEY="YOUR_KEY"
export GEMINI_IMAGE_MODEL="gemini-nano-banana-2.1"
export GEMINI_REVIEW_MODEL="gemini-3.8-flash"
```

Windows CMD:

```cmd
set GEMINI_API_KEY=YOUR_KEY
set GEMINI_IMAGE_MODEL=gemini-nano-banana-2.1
set GEMINI_REVIEW_MODEL=gemini-3.8-flash
```

## Run from the repository root

First inspect the actual source atlas and choose the one intended cylinder by **pixel ROI**, not by the atlas's printed label alone. This command records a source SHA, dimensions, ROI, reviewer, notes, and selected crop SHA:

```bash
python -m bubble_break.create_master_selection_manifest \
  --source-atlas path/to/real-source-atlas.png \
  --roi X0 Y0 X1 Y1 \
  --reviewer "your-reviewer-id" \
  --notes "Selected the single planted double-ended cylinder by image position" \
  --confirm-single-tool \
  --out-json out/master-selection.json \
  --crop-out out/selected-cylinder-roi.png
```

Then run the seven-stage closed loop with Gemini as the external provider:

```bash
python -m bubble_break.planted_bubble_closed_loop \
  --master-selection-json out/master-selection.json \
  --provider-command "python -m bubble_break.gemini_planted_bubble_provider" \
  --outdir out/gemini_planted_bubble_run \
  --max-retries 2
```

The runner invokes the command with a JSON request-file path argument; the adapter prints one JSON object containing the generated image path and the model's raster-bound evidence. Provider requests, generated PNGs, semantic-review JSON, stdout/stderr, and the final run manifest are stored under the output directory.

## Cost and stopping behavior

Each attempted candidate may incur **one image-generation request plus one vision-review request**. With seven stages and up to two retries per stage, the configured maximum can be substantially more than seven image calls. Review the current [Gemini API pricing page](https://ai.google.dev/gemini-api/docs/pricing) and set account limits before running a full batch. No image generation is run by CI.

If `GEMINI_API_KEY` is missing, the API call fails, no image is returned, or the model's structured review cannot be parsed, the adapter exits with an error; the pipeline may retry within `--max-retries`, then BLOCK. It never creates placeholder images or synthetic passes.

## Acceptance boundary

A semantic-model review is an additional noisy-channel detector, not infallible ground truth. The final report must continue to say `visual_acceptance_status=NOT_VERIFIED_BY_CODE`. Humans must inspect the actual generated rasters, especially the base-seat contact at P, existing handle identity through D2/D3, crack origin and outward progression, and sanctuary/resident safety. A complete evidence packet is not the same as approved imagery.

CI tests use local fake API responses only. They verify request composition, mask/parent binding, output SHA binding, and fail-closed behavior; they do not call Gemini or claim any production images were generated.
