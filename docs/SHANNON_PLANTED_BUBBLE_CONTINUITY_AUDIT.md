# Seven-stage planted-bubble continuity audit

## What the submitted seven-panel strip proves—and does not prove

The supplied montage visibly breaks continuity in multiple places: the person/hammer composition changes drastically between C and D2; B, D1 and D3 read like repeated isolated tool frames rather than a continuous action progression; the mid-frame adds glow and crack patterns without proving that the crack origin follows the same base contact point P; the end-frame changes composition enough that shell-only destruction and resident safety cannot be inferred from the montage itself.

This is a human visual review of the montage, not a claim that every original raster has been independently re-opened and pixel-audited.

## Correct concept lock

This pipeline uses the recorded planted-cylinder concept, not a flying hammer and not a final-scene T-v-T collision:
- a double-ended solid cylinder is planted radially on the bubble surface;
- a conformal curved base seat stays in contact at the same P;
- the one handle attaches at the cylinder side-middle, along the local tangent and transverse to the cylinder axis;
- the opposite outer circular end cap remains clear;
- the handle is not invented or moved when the heroine first grips it;
- the shell state advances only from intact → cracks from P → shell-only shatter, while the sanctuary and inhabitants remain intact.

The T-v-T end-face matrix can be used as a separate geometry experiment. It is not a replacement for this planted-cylinder target geometry.

## Why continuity is failing in the image

1. **Scene/camera/background are not hard cross-frame invariants.** A hash-bound tool annotation is not enough if camera, scene ID, or background landmarks change between frames.
2. **The heroine scale claim is categorical, not measured.** A text value saying MINIATURE cannot stop a frame where the heroine grows to nearly the bubble's diameter.
3. **Pose evolution is not verified.** The D1/D3 frame can reuse the same pose signature and still be called an action stage.
4. **Masks were being compiled without an enforceable frozen-pixel condition.** A prompt saying “freeze background” does not prove those pixels survived the edit.
5. **Effect causality is underspecified.** A glow or bright crack near P is not enough; the review receipt must mark radial crack propagation from P and outward shell fragments at the end stage.

## Implemented gates on the repair branch

- Same scene ID, camera rig, camera-view fingerprint and background-landmark SHA-256 across all seven stages.
- Exact prior-PASS parent raster SHA and master anchor SHA for each child.
- Geometry coordinates/axes, base seat, bubble center/radius, cylinder, handle track and world attachment compared with the accepted master; track IDs alone are not trusted.
- Heroine must remain below 60% of bubble diameter by annotated bounding-box height, keep the same identity, stay within an 18% scale change from the previous person frame, and avoid a large unapproved position jump.
- D1, D2 and D3 must declare distinct pose signatures; repeating the previous pose signature is blocked.
- Every child raster must be accompanied by an edit mask bound to the last PASS parent. compose_masked_edit composites generated pixels only inside the edit mask and saves losslessly as PNG. validate_frozen_pixels then rejects changes outside that mask.
- A no-op image cannot pass as an edited stage.
- E-mid requires radial crack propagation from P; E-end additionally requires fragments propagating outward from P and shell-only breach.
- Creativity/novelty only rank candidates after all hard continuity/geometry/review-receipt gates pass; they can never rescue a failed candidate.

## Shannon-inspired engineering mapping

This is an engineering analogy, not a claim that an image model is a Shannon communication channel with known capacity.
- **Signal:** the selected tool master, P, the conformal base, the one side-handle track, camera/background identity and sanctuary.
- **Noise:** newly invented handles, scene re-layout, changing scale, collage grids, excess glow obscuring the contact, and unauthorized edits.
- **Rate/distortion policy:** one full-frame request per stage, explicit authorized deltas, and preserve every pixel outside the edit mask. Spend change budget on the intended stage event rather than redrawing the entire scene.
- **Feedback:** each failed gate returns a concrete error vector; the next attempt inherits the last accepted parent, never the failed child.
- **Decision policy:** first satisfy physical/continuity constraints; only then choose the most creative candidate among the eligible set.

## Important limits

The code validates the submitted geometry annotations and review receipt, but it does not discover all annotations by itself or authenticate the named reviewer/model. Camera/background fingerprints and pose signatures must come from a real human-pixel reviewer or a semantic vision service that inspected the exact raster bytes. The branch does not contain a connected Gemini image-generation API client. A green unit-test run validates this software contract, not the successful generation of new images.

## Acceptance state

The provided seven-panel strip is **REJECTED as a continuity proof**. The correct next run must regenerate the failed child stage from its immediate accepted parent, apply the authorized region mask, bind the review to the final lossless raster SHA, and fail closed if any gate remains unmet.
