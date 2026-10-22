# Shannon-Inspired Planted-Cylinder Bubble-Break Closed Loop

## Decision: preserve the latest proven geometry, not the older flying-hammer model

The imported Gemini record in docs/半成HAM.txt documents the pivotal correction: the intended tool is a **double-ended solid cylinder planted radially on the bubble**, with the bubble-side conformal seat fully touching the shell and glowing at the base interface. The single handle grows from the cylinder's side-middle, tangent to the bubble and approximately perpendicular to the cylinder's radial axis. The exposed outer end cap must remain clear. This is neither a hammer flying toward the bubble nor a final T-hammer-versus-T-hammer collision.

The same record says the useful workflow is candidate atlas → explicit ROI selection → isolate one tool → add the miniature person without gripping → grip the already-existing handle → build pose/tension through serial full-frame edits → add glow/cracks → shatter only the shell. It also records repeatable failures: atlas labels can be duplicated/missing; zoom cannot recover a handle that does not exist in the source pixels; a first-grip edit may invent a second/axial handle; and one image containing many unrelated cells weakens per-object pixel locks. The stage history belongs with the source log:
[Stage failure/success/rewrite log](https://github.com/JUN-ZS/ai-image-gen-logic-review/blob/feat/gemini-closed-loop-partial-20261022/bubble_break/logs/STAGE_FAILURE_SUCCESS_REWRITE_LOG.md).

## What Shannon contributes (engineering adaptation, not a claim of a theorem)

Shannon's information theory formalizes reliable message reconstruction when a communication channel introduces noise, and studies the efficiency/reliability trade-off, coding redundancy, and channel feedback. See the [Chinese Wikipedia entry](https://zh.wikipedia.org/wiki/%E5%85%8B%E5%8A%B3%E5%BE%B7%C2%B7%E9%A6%99%E5%86%9C), [IEEE overview of information theory](https://technav.ieee.org/topic/information-theory/), and [IEEE explanation of channel coding](https://technav.ieee.org/area/channel-coding/).

This project borrows those **engineering patterns**. It does not pretend that generative-image behavior is a known memoryless channel or that these gates instantiate Shannon's channel-capacity theorem.

| Communication-engineering idea | Image-workflow application |
|---|---|
| Message/source | One compact, immutable planted-cylinder geometry and story-state contract. |
| Encoder | Compile that contract into one stage prompt, a list of allowed changes, frozen fields, parent-image reference, and hash receipts. |
| Noisy channel | The external image generator/editor, which may omit the side handle, invent an axial rod, move P, distort the base seat, or damage the inner sanctuary. |
| Redundancy / error detection | Repeat critical constraints across prompt, expected annotations, instance IDs, parent SHA, master-anchor SHA, and an external review receipt. A label is not evidence and cannot override conflicting pixels. |
| Decoder / receiver | A named human reviewer or semantic-vision process checks the actual raster and returns an explicit PASS/FAIL receipt tied to that exact raster. This Python code validates the receipt's binding; it does not authenticate the reviewer or recognize the scene by itself. |
| Feedback channel | The rejection list becomes the next attempt's error vector. Regenerate from the last verified PASS parent, not from a failed child. |
| Rate-distortion trade-off | Spend visual variation only in the stage's authorized_delta_fields; freeze everything else. Creativity and novelty rank candidates only after hard geometry/state gates pass. |

The practical rule is: **redundancy in the contract, one authorized edit at a time, explicit feedback, and no propagation of a failed state**. This adapts the reliable-communication idea to a creative pipeline without confusing engineering analogy with proof.

## Canonical state machine

A human must choose the actual tool ROI in the source atlas by position, not just by a printed candidate label. The selected master is then treated as an image anchor.

1. **B — B_LOCKED_TOOL_MASTER:** isolate exactly one selected double-ended cylinder. No person, no cracks. Preserve the conformal base seat, contact point P, exposed outer cap and side-middle tangent handle.
2. **C — C_PERSON_SCALE_NO_GRIP:** add one miniature heroine; her hands do not grip yet. The tool is not redrawn.
3. **D1 — D1_APPROACH_NO_GRIP:** pose the heroine for a readable wind-up, still without grip. The cylinder remains planted; it does not swing across an air gap.
4. **D2 — D2_FIRST_GRIP_EXISTING_HANDLE:** move hands/forearms to the existing side handle. Do not move the handle to the hands and do not invent a new rod or lower stub.
5. **D3 — D3_TENSION_EXISTING_HANDLE:** increase pose, hip/shoulder tension and follow-through. Keep the same handle track and attachment.
6. **E-mid — E_MID_GLOW_CRACKS_FROM_P:** strengthen glow at the **base-to-bubble interface**; cracks spread from P while the shell is not yet fully shattered.
7. **E-end — E_END_SHELL_SHATTER_FROM_P:** shatter the outer shell outward from the same P. The planted cylinder and handle remain; the miniature city and residents stay unharmed.

This is the latest **planted** interaction concept. The earlier V5.1 flying/swinging model's wide-gap-to-zero-gap trajectory is not carried into this contract. T-v-T terminal-face calibration is a different experiment and is not a prerequisite unless a later explicit geometry study demonstrates why it helps this planted-cylinder design.

## Evidence and feedback contract

For each real raster, the validator requires:
- SHA-256 of the exact image bytes and matching image dimensions;
- a parent-raster SHA (except the selected master) and an immutable master-anchor SHA;
- an explicit source-atlas SHA, dimensions and valid pixel ROI for the initial master selection; provider-driven Stage B is blocked without this human ROI selection;
- per-stage binary edit/freeze mask files created from the last accepted parent's annotations. White in edit_mask.png means editable; white in freeze_mask.png means protected. These are conservative bounding-region masks, not semantic segmentation, so hard raster/geometry gates still run after generation;
- a master geometry lock vector containing bubble center/radius, P, cylinder/base/cap coordinates and bounding boxes, the world axis, side-handle axis/attachment, and sanctuary bounds. Later stages cannot inherit the same track ID while secretly moving the handle or changing the bubble geometry;
- the same cylinder instance ID and handle track ID through the chain;
- P on the bubble surface and the conformal seat still at P;
- cylinder axis aligned to the local bubble normal; handle axis transverse to the cylinder axis and tangent to the bubble; side-middle attachment fraction 0.35–0.65;
- outer end cap clear and no added handle/stub;
- correct person/no-grip/grip state for the stage;
- the correct shell/crack state, base-glow origin at P, and the sanctuary/resident safety state;
- an external PASS receipt naming the review mode/reviewer and binding the exact child SHA, parent SHA, master-anchor SHA and stage.

The program blocks on absent/mismatched evidence. It evaluates every candidate in a batch and selects only among candidates that pass the hard gates; creativity/novelty cannot rescue a failed candidate. A failed batch can be retried within a bounded attempt count. A failed image never becomes the next parent.

These gates validate the evidence contract and submitted annotation record. They do not prove that image pixels satisfy those annotations. In particular, the code does not itself detect a hidden extra handle, recognize every shard crossing a resident, or establish semantic continuity. visual_acceptance_status therefore remains NOT_VERIFIED_BY_CODE even when evidence fields are internally consistent.

## Current implementation status

The branch adds:
- bubble_break/planted_bubble_closed_loop.py: planted-cylinder stage contract, prompt compiler, raster/evidence validator, immutable master-geometry vector, per-stage edit/freeze masks, bounded retry loop, source-atlas ROI selection record, SHA-bound parent lineage, structured error feedback, candidate ranking after hard gates, and a generic external command adapter.
- bubble_break/test_planted_bubble_closed_loop.py: regression tests for the source-atlas ROI gate, handle/stub and track locks, crack origin/shell-only requirements, stale raster receipts, and retrying from the last verified parent.
- .github/workflows/shannon-planted-bubble.yml: tests and compiles the prompt/contract packet.

**A Gemini/image-generation provider is not connected by this repository patch.** The command adapter is an interface; it is not a built-in Gemini API. The offline fixtures and CI packet are not newly generated production images. Do not label the sequence generated, visually accepted, or complete until a real provider supplies rasters and a named human/semantic-vision reviewer checks those exact images.

## Reproducible commands

Compile the prompt/contract packet only:

~~~bash
python -m bubble_break.planted_bubble_closed_loop --compile-only --outdir out/shannon_planted_bubble
~~~

Run the regression tests:

~~~bash
python -m unittest bubble_break.test_planted_bubble_closed_loop -v
~~~

For provider-driven runs, first create a human-reviewed master-selection JSON with the exact source atlas path, its SHA-256 and dimensions, the chosen pixel ROI, reviewer, and notes. The fields are the same as the master_selection object accepted in a candidate evidence record. Then pass it explicitly:

~~~bash
python -m bubble_break.planted_bubble_closed_loop --master-selection-json out/master-selection.json --provider-command "python path/to/your_provider_wrapper.py" --outdir out/planted_bubble_run --max-retries 2
~~~

For a fully offline replay, use --candidate-manifest and include evidence records bound to each exact raster. The example provider command is a handoff interface only. The named wrapper must actually call the configured image service, use the request's parent image and edit/freeze masks, save real image bytes, and return evidence/review receipts matching the schema. No image service or credentials are silently assumed.
