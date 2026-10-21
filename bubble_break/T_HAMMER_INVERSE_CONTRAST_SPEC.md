# T-Hammer Inverse-Contrast Pair Engine

## What this experiment is for

This is a deliberate contrast experiment, not a prompt that says every contact is correct. Two adults attack two distinct points on the same large transparent containment sphere in one cinematic scene:

- **Positive control:** an airborne fighter whose rigid T-hammer approaches with its narrow terminal end face first.
- **Negative control ("反者之動"):** a grounded fighter in a deep low stance who intentionally presents the broad cheek/sidewall first. This is an engineered failure case, not a valid alternative technique.

The contrast can teach and audit both the target rule and the identifiable visual failure. The two rules must never be blended into an ambiguous average.

## Locked contact physics

### Positive control — terminal end face first

At a local sphere pole P, let s be the outward sphere normal. The permitted terminal end-face normal is -s, so its dot product with s equals -1. The head's long axis points radially toward the sphere center. The head and one straight long handle are a rigid T; the handle attaches at its defined midpoint joint at 90 degrees and remains outside the collision zone. No cheek, corner, long upper/lower surface or handle may contact first.

### Negative control — wrong broad cheek/sidewall first

At a different sphere pole Q, the crossbar's long axis lies tangent to the local sphere surface, not along the inward normal. Its broad cheek/sidewall is deliberately presented to the sphere and is the first-contact surface. The terminal end face is explicitly not the contacting surface. The handle remains straight, attached, and perpendicular to the head's long axis. This must be stored and reviewed as \`EXPECTED_FAIL_NEGATIVE_CONTROL\`, never \`PASS\`.

This distinction is based on the identity of the first-contact surface, not sparks, pose drama, color, or whether the overall image looks convincing.

## Action diversity

The airborne fighter varies between diagonal diving, flying side sweep, spin-finish and inverted drop actions. The floor-level fighter varies between deep-crouch uppercut, one-knee low sweep, reverse low sweep and compact crouching thrust. Each pair has 12 camera views: grazing audit, low hero, high crane, side profile, front/reverse three-quarter, Dutch roll, two over-shoulder directions, macro depth and left/right orbit.

Every action may have a curved wind-up, but the final approach has to obey its assigned positive or negative contact rule. Camera orbit, pitch, roll and focal length change what is seen, not the contact geometry. Both impact locations must remain distinct and inspectable.

## Matrix size and output

4 airborne actions x 4 ground-low actions x 12 cameras = **192 paired trials**. Each variant emits:
- a combined two-fighter contrast prompt;
- a positive-only crop prompt for the correct terminal-cap case;
- a negative-only crop prompt for the deliberate wrong cheek case;
- a structured contact-geometry manifest;
- a camera-projected SVG proxy marked \`NOT pixel proof\`.

Run from the repository root:

\`python -m unittest bubble_break/test_t_hammer_inverse_contrast_engine.py -v\`

\`python bubble_break/t_hammer_inverse_contrast_engine.py --outdir out/t_hammer_inverse_contrast\`

## Acceptance gate

Image-generation prompts and SVG proxies are not image evidence. Until the generated raster images are attached and reviewed:
- \`image_realization=NOT_RUN\`;
- \`pixel_audit=NOT_RUN\`;
- accepted positive images remain uncounted;
- wrong-face examples remain negative controls, even when they are perfectly depicted.

A mixed paired image is a **contrast experiment**, not a single pass/fail image. Review the positive and negative contact points independently.
