# Independent Dual T-Hammer Collision Contract

## Scope boundary

This module is a separate physical-interaction concept: **two distinct T-shaped hammers collide with their actual flat striking end faces**. It is not the Bubble-Break task and must not replace the established bubble-break story, which has one locked hammer striking a containment shell.

The code here compiles generation prompts and validates structured geometry annotations. It does not call an image-generation provider and does not claim that a prompt or a green CI result proves the pixels are correct.

## Hard physical constraints

- HAMMER_A and HAMMER_B are separate rigid-body instances; each has its own head and transverse handle.
- At PRE_FAR and PRE_NEAR, the actual end faces remain apart with a positive shrinking gap.
- At FIRST_CONTACT, opposing end-face normals must align within the configured tolerance, the gap must be effectively zero, and point P must lie inside both striking-face disks.
- Head-cheek, shaft, handle, or handle-joint contact is a rejection, not an alternate interpretation.
- REACTION must originate at the established contact point; RECOIL must show the tools separating again.
- Camera variation can change view, framing, lighting, and perspective, but not the collision-surface contract.

## Raster-bound evidence

`raster_bound_collision_audit.py` binds annotation evidence to the exact raster SHA-256 and dimensions, and checks that the two instance IDs, head/handle axes, handle transverse geometry, strike-face disks, and contact point are internally consistent.

This validator does not infer those annotations from pixels. A semantic vision system or named human reviewer still needs to inspect the exact image; code reports `NOT_VERIFIED_BY_CODE` rather than silently claiming image acceptance.

## Output

Run:

```bash
python -m bubble_break.dual_t_hammer_collision --outdir out/dual_t_hammer_collision --camera-count 12
```

It emits the physical contract and an independent-view prompt matrix for PRE_FAR, PRE_NEAR, FIRST_CONTACT, REACTION, and RECOIL. It generates **zero images**. A generation backend must be connected separately before any generated-raster review can occur.

## Bubble-Break is separate

The separate Bubble-Break workflow remains responsible for the planted double-ended hammer approaching and contacting the bubble at its canonical point, the shell fracture progression, and preservation of the sanctuary inside. It should not require a second hammer, and this dual-tool module must not be treated as its validator.
