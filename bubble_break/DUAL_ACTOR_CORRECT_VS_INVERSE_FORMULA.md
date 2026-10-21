# Dual-actor correct vs inverse-face strike formula

Branch: `feat/dual-actor-correct-vs-inverse-strike` (created from `main`).

## Invariant
Let `n` be the unit outward normal of the target at the contact point, and `f` the unit normal of the hammer's intended flat striking face. A valid face-on strike requires:

`dot(f, -n) >= cos(tolerance_degrees)`

Default tolerance: 8 degrees. A deliberately reversed face uses `f = n`; it must be classified as `NEGATIVE_CONTROL_INVERSE_FACE` and FAIL, never counted as a valid sample.

## Paired scene
- Actor A is airborne, with a distinct attack trajectory.
- Actor B is grounded in a low crouch/kneel, with a different trajectory.
- One actor is assigned the valid face orientation; the other is assigned the inverse-face negative control. Alternate which actor is correct across trials.
- Vary camera azimuth/elevation independently from contact geometry.
- Preserve rigid head/handle geometry; show the full long handle and contact seam.
- Sparks must not obscure the contact. Side, edge, corner, rear-face, or handle-first contact is FAIL.

## Acceptance
The generator's formula/unit tests are separate from image realization and pixel audit. Until generated images are reviewed, `IMAGE_REALIZATION=NOT_RUN` and `PIXEL_AUDIT=NOT_RUN`.
