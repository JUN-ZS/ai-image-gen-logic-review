# Shannon-Inspired Information Gain for Bubble-Break

## What is borrowed, and what is not

Claude Shannon's information theory models uncertainty and how much information an observation can provide. This implementation borrows that mathematical lens; it does **not** claim Shannon himself proposed image-generation feedback loops, nor does it claim the current engineering likelihoods are empirically calibrated.

Sources:
- Claude Shannon: https://zh.wikipedia.org/wiki/克劳德·香农
- Information theory / entropy: https://zh.wikipedia.org/wiki/信息论

## The image generator is a noisy channel

For this workflow, the intended scene contract is the source message, the prompt/reference/mask are the encoding, the image model is a noisy channel, and the raster is the received output. The output can distort physical semantics even when the prompt contains the right words. Therefore:

- A prompt passing text checks is not image acceptance.
- A green pixel gate is not proof of terminal-face contact or resident safety.
- The exact raster bytes, stage ID, parent-raster SHA, upstream calibration SHA, and evidence record must be bound together.
- Missing, mismatched, stale, or unverifiable evidence blocks the stage.

This creates redundancy across independent channels: a textual contract, parent-raster lineage, structured geometry annotations, measured pixels, and explicit visual review. Redundancy is meant to catch contradictions, not let multiple copies of the same unsupported claim count as independent proof.

## Entropy selects the next diagnostic—not the PASS status

`bubble_break/shannon_information_gain.py` computes Shannon entropy and expected mutual information for candidate diagnostic experiments. Each action defines explicit likelihood assumptions (P(O \mid H)), where (H) is a possible failure class and (O) is the experiment's binary diagnostic outcome.

The planner ranks experiments by expected information gain divided by estimated cost. Examples include:
- topology-wide view to distinguish a malformed T-head/handle from a correct rigid tool;
- grazing macro to reveal end-face versus cheek contact;
- parent-pair provenance audit to detect stale/identical images and camera/scene identity drift;
- pole/scale calibration to localize P and sphere geometry;
- crack-origin/front audit to test whether the crack front grows outward from P;
- sanctuary-focused review to check shell-only damage and intact residents.

The current action likelihoods are engineering assumptions, so results carry `UNVALIDATED_ENGINEERING_PRIORS`. They are not model accuracy estimates, confidence intervals, or evidence that a generated image is correct. Replace them with measured rates only after building an image-matched reviewed dataset.

## How the controller fits the closed loop

1. A candidate raster is checked against the expected stage, actual parent-raster SHA, stable scene/camera/object IDs, and—on bubble frames—the exact upstream dual-T FIRST_CONTACT SHA.
2. The geometry/pixel contract is evaluated. A missing or wrong field cannot be cured by a high score.
3. For a rejection, the controller records classified failure hypotheses and selects a targeted next diagnostic / repair experiment.
4. The provider receives the prior raster, gate errors, a stage-specific prompt, and the selected information-gain experiment. It must return actual raster files and annotations tied to those exact bytes.
5. Every retry is audited. The pipeline halts BLOCKED when no candidate meets the hard contract or retry budget is exhausted.
6. When structured evidence passes, status remains `EVIDENCE_CONTRACTS_PASSED_REQUIRES_VISUAL_REVIEW`; code does not declare visual acceptance.

## Hard physical sequence

Upstream calibration uses two separate T-hammers and verifies flat terminal end-face to end-face contact. The final Bubble-Break sequence still contains **one attacking calibrated T-hammer and one containment bubble**:

`CAL: PRE_FAR → PRE_NEAR → FIRST_CONTACT → REACTION → RECOIL`

`BUBBLE: H0_PRE_IMPACT → H1_PRE_NEAR → H2_FIRST_CONTACT → H2B_CRACK_PROPAGATION → H3_FOLLOWTHROUGH_SHELL_SHATTER`

H0/H1 must have an intact, crack-free shell and a positive gap. H2 must establish contact at P with only initial fracture. H2B and H3 must show a strictly larger normalized crack-front radius than the previous stage, with origin at P. H3 must declare shell-only breach and unharmed inhabitants. The final scene must not show two hammers colliding.

## Honest execution status

`bubble_break/runner.py` is now the executable orchestration entry point. It accepts existing candidate rasters and optionally an external provider command implementing the request/response contract in `docs/CLOSED_LOOP_PROVIDER_ADAPTER.md`. No image provider, API key, or live generation endpoint is bundled here.

If no provider is supplied and candidate stages are missing, the runner returns BLOCKED. Supplying an external command makes the adapter executable; it does not mean that provider has been configured or that any image has already been generated. All visual status remains `NOT_VERIFIED_BY_CODE` until an image-matched semantic/human review is attached.
