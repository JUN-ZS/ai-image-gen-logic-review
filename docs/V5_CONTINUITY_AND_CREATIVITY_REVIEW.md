# V5 continuity / creativity audit: root causes and corrective design

Audit target: branch feat/v5-continuity-autonomous, including bubble_break/autonomous_pipeline.py, test_autonomous_pipeline.py, the committed five-keyframe strip and audit board, and the latest Actions logs.

## Executive verdict

**No: the main defect is not simply "it refuses to RERUN with every lock".** Strong reference locking is necessary, but the current implementation conflates four very different things:

1. generating a new image,
2. checking a pre-generated raster candidate,
3. constructing a synthetic/composited test raster,
4. proving that a five-frame story is visually and causally continuous.

The code reliably performed some software geometry checks but previously presented those checks as if they demonstrated an end-to-end image-generation rerun. They do not. The five-frame strip itself also makes the failure visible: the 0s/2s pre-contact pair changes subject scale/composition sharply, and the 2s frame contains a conspicuous vertical seam/composite edge. Meanwhile, the middle/contact/effect frames share a much more stable composition. That is a real timeline-construction defect, not something a higher NCC number can fix.

This branch adds fail-closed input requirements, labels synthetic tests as synthetic, and checks the four adjacent keyframe backgrounds. **It still does not connect an image-generation model, and automated gate PASS is not final human image acceptance.**

## Source-supported findings

### 1. The "autonomous" script does not invoke an image model

In run_autonomous_pipeline, the real-model interface is currently only a stage_candidates_map of raster file paths. If that map is absent, the old implementation called render_synthetic_stage_raster to draw schematic shapes and then passed those local files through the gates. The helper is explicitly a Pillow-based procedural raster, not an image model.

When a candidate fails, compile_elevation_prompt_repair writes a repair prompt file. It does not submit that prompt to a generator. The script therefore had no true closed loop of:

generate → audit → targeted repair → generate again → select accepted raster.

It had only:

read supplied file(s) → audit → save repair text if rejected.

The phrase "RERUN" must refer to an actual connected image-generation adapter, not just another pass through this Python program.

**Change in this branch:** no supplied real candidate map now raises BLOCK; procedural candidates require the explicit --synthetic-test-mode. The manifest reports generation_backend_status=NOT_CONNECTED_BY_THIS_SCRIPT. Synthetic test runs can pass contract tests but cannot report all_stages_passed=true or claim visual acceptance.

### 2. PRE_NEAR did not use PRE_FAR as a temporal parent

The previous synthesize_connected_pre_near_frame(pre_far_path, d3_contact_path, ...) opened pre_far_path but then constructed the output from a copy of D3, darkened pixels around a hard-coded seam, and shifted a slice of the sphere 42 pixels. The loaded PRE_FAR image was never used to estimate or preserve the actual moving object state. This can manufacture a gap in the raster, but it is not temporal interpolation and can leave a hard compositing boundary.

The old five-keyframe sequence also did not run an adjacent-frame continuity gate across PRE_FAR→PRE_NEAR and PRE_NEAR→D3. Gate #9 was used only on some canonical-spine stages.

**Change in this branch:** a production run must supply both real PRE_FAR and real PRE_NEAR rasters. The compositing helper remains only a synthetic test fixture. The five adjacent keyframe pairs now get a separate static-background comparison, and PRE_FAR/PRE_NEAR each run their per-frame state gates.

### 3. Gate #9 was too weak to mean "the frames are connected"

The old gate:
- compared one fixed left-side ROI,
- converted it to grayscale,
- downsampled the ROI to only 16×16 before computing NCC,
- used luminance difference as a second scalar,
- and was silently omitted if a parent image was not passed.

That is a useful cheap alarm for a gross scene/background jump, but it is not a proof of same face, same object pose, same tool axis, same bubble geometry, or same story state. It can miss defects outside the ROI and can score a largely unchanged dark background while an important subject changes. A literal SHA-256 in prompt text is only provenance: it does not force an image model to preserve pixels.

**Change in this branch:** a required Gate #9 now fails closed if its parent raster is missing; every transition in the exported five-frame strip also receives an explicitly named static-background-only check. The output does not call that semantic continuity or pixel-perfect proof.

### 4. Candidate selection previously stopped at the first PASS

For a stage with several supplied raster candidates, the prior loop broke immediately on the first candidate that passed. It was not a best-candidate selection among all passing candidates. If every candidate failed, the previous function could retain the highest-scoring failed image in the canonical sequence and continue. That is incompatible with "roll back and never pass a FAIL asset to the next step."

**Change in this branch:** the full supplied candidate wash is evaluated; the highest-scoring passing candidate is selected. If a stage has no passing candidate, the run is blocked before subsequent stages consume it. The script records a repair prompt but still does not pretend to execute a model rerun.

### 5. The current V5 branch is a hammer/bubble continuity engine, not an Original Sin story engine

This branch's generator-facing path is centered on a fixed candidate (C13), hammer topology, the bubble, character placement, contact state and effects. It does not consume a story-level Original Sin record containing the promise, hidden mechanism, human cost, evidence, revelation, voluntary choice and restored agency. It does not compile the EFV song-semantic layer as part of its actual run.

That is why the output can be mechanically recognizable yet lack a creative, causally progressing story. Changing color, lighting, camera crop or adding "原罪" to a prompt would still be decoration if the visible world-rule and the character's choice never change the events.

## Is "Transformer" the original sin?

**Model prior is one cause; it is not the whole cause and not specific to Transformer architectures.** Image generation is commonly a fresh conditional synthesis/edit operation rather than a persistent 3D scene with durable object IDs. A text phrase such as "keep the same hammer" or a SHA string is a soft condition, not an enforceable pixel constraint. If an edit asks the model to solve grip, stance, scene lighting, weapon geometry, camera, and new effects all at once, the model can satisfy its familiar hammer prior by redesigning the object.

But the control design magnifies that prior: too much global re-generation, no region-level edit mask, weak automated checks, an un-gated pre-contact pair, and no connected rerun adapter. The engineering failure is therefore **stateless full-frame re-synthesis plus insufficient state/evidence control**, not "the Transformer is inherently unable to make a continuous story."

## The proper lock model: lock state, not every pixel indiscriminately

A single continuity contract should describe the same scene while explicitly allowing the intended state transition.

### Immutable within one five-frame shot

- scene/camera/horizon and stable environmental landmarks;
- protagonist identity, face/hair/outfit reference;
- bubble identity, sphere center/radius envelope and persistent surface signature;
- hammer head dimensions, side-middle handle joint, radial-axis / lateral-handle relationship;
- same story-level cause, same alpha motif and the same target mechanism;
- one bubble, one intended impact, residents unharmed.

### Authorized changes by keyframe

| Frame | Authorized change | Must remain fixed |
|---|---|---|
| 0s PRE_FAR | body winds up; hammer-to-bubble gap is largest | camera and identities; tool topology; bubble intact |
| 2s PRE_NEAR | rigid-body approach; gap shrinks but remains positive | same camera/background; same face/outfit; same tool geometry; bubble intact |
| 4.5s CONTACT | gap reaches zero at the specified contact point; one contact event | same tool/head/handle; same scene and identities |
| 7s E_MID | crack/front and contained shock effect appear after contact | crack origin at contact; tool and people protected |
| 10s E_END | shell resolves into the selected material-compatible shatter | same shot and character; no shard hits people; agency is restored |

Do not use the same global NCC threshold as the sole rule for every row. Contact and shatter are supposed to change target pixels. Compare protected static areas separately from authorized change masks, and separately audit object geometry/state.

## Recommended V5.1 architecture

1. **Real-raster gate.** Every actual frame input must have a path, SHA-256, source/parent ID and generation attempt ID. No generated raster means BLOCK; synthetic test fixtures cannot count as rendered acceptance.
2. **State manifest before prompts.** Keep a JSON SceneState per time point: camera ID, background-landmark coordinates, protagonist reference ID / bbox, bubble center and radius, hammer-head and handle axes, contact point, signed gap in pixels, fracture state, current story cause, alpha and beta. A frame compiler reads state deltas instead of freehand-rewriting the whole scene.
3. **Reference + masks.** Preserve frozen pixels outside a declared edit mask by image compositing, not by asking a generative model to "remember" them. The model is asked to change one permitted region/field only. For moved people/tools, use explicit object masks/rigid transforms or pose/depth/edge conditioning, and verify the actual raster after compositing.
4. **True per-stage rerun adapter.** For every stage, generate a bounded candidate batch from the last PASS raster. Audit all candidates. If none passes, compile a repair focused on the failed gate, invoke the generator again with the same accepted parent, and retry under a finite budget. Never continue from a FAIL frame. This adapter is not currently connected in this repository and must be implemented/configured by the actual image service.
5. **Multi-signal gates.** Keep topology gates, but add separate checks for protected-background alignment, face/outfit consistency, tool-mask/joint geometry, bubble contour, signed gap progression, and crack origin/state. NCC may be one signal, never the whole verdict. Automated vision metrics need explicit limits and should not claim a human review happened.
6. **Original Sin causal transformer.** Every story must encode: promise → hidden mechanism → visible symptom → human cost → evidence/alpha clue → protagonist's discovery → one physical action against the mechanism → shell-only consequence → voluntary choice. The song-inspired motifs act as persistent visual evidence across the sequence, not as disconnected decorative words. Vary the mechanism, evidence, environment, scale and fracture style across stories; freeze their identity and causal meaning inside each individual story.
7. **Two objectives, one selection gate.** First reject all candidates that violate continuity/physics. Among passing candidates only, rank (a) state transition clarity, (b) motif/story relevance, (c) visual novelty relative to prior accepted story variants, and (d) composition/readability. Do not maximize novelty by breaking the same-story lock; do not maximize NCC by freezing every frame into the same pose.

## What this branch now corrects

- no silent synthetic fallback in production mode;
- missing real pre-contact rasters block rather than get patched into an apparent 5-frame run;
- missing parent raster blocks Gate #9;
- all supplied candidates are audited before choosing the best PASS;
- any stage with zero PASS candidates stops before the next stage;
- every adjacent keyframe pair has a static-background-only continuity report;
- synthetic CI run is explicitly marked SYNTHETIC_TEST_ONLY, with real visual acceptance kept unverified;
- removed a stale CI reference to a test file that does not exist.

## Remaining blockers (do not call these solved)

- **No image-generation backend is connected in this script.** Repair prompts are compiled, not executed as real reruns.
- The coarse background-strip metric does not establish same-character identity or complete story continuity.
- Per-frame visual gates remain heuristic; contact point / crack origin and human survival still need real-image inspection.
- Original Sin story semantics are not yet wired into this V5 pipeline. Integrate the causal story compiler only after the five-frame mechanical state gates are honest and stable.
- Final PASS requires the real five rasters and review evidence. A successful unit test is only a software-contract PASS.
