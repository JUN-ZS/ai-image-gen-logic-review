# T-Hammer Multi-View / Swing Trial Engine

## Non-negotiable contact rule

The trial matrix varies impact direction, wind-up motion, handle orientation and camera without changing the contact principle.

1. Collision direction is a normalized 3D vector n.
2. Hammer A's active terminal end-face normal is n; hammer B's is -n. Their normal dot product is -1.
3. Each long rectangular head's longitudinal axis is collinear with its active terminal-face normal.
4. Each hammer has one straight long handle attached at the midpoint of a long head side, perpendicular to the head axis. Head and handle form a rigid body; neither can bend or independently rotate.
5. Only terminal end face to terminal end face is a valid Stage-A first contact. Cheeks, upper/lower long surfaces, corners, center joints and handles remain clear.
6. Camera orbit, angle and image roll change only the view transform. They may not change world-space contact normals or break rigid-body topology.
7. Keep both terminal-face boundaries and both long handles inspectable. Avoid a perfect along-normal view when it hides the seam.

## Time chain and distances

- Dual-hammer H0: 50 units total face-to-face gap (25 units per tool). This is not 50 units per tool.
- Dual-hammer H2: active terminal planes coincide at P, with opposite normals and no interpenetration.
- Sphere-scene H0: attacker's terminal face is 50 units from the intact sphere surface.
- Sphere-scene H2: first terminal-face contact at P; micro-fractures begin only at P.
- Sphere-scene H3: same rigid hammer advances 15 units along +n; the head stays aligned and handle stays perpendicular.

## Trial matrix

8 3D impact axes x 12 camera views x 2 genuinely different wind-up profiles = 192 trials. Each trial compiles a Stage-A dual-hammer proof prompt, H0/H2/H3 single-hammer-versus-sphere prompts, and a perspective-projected SVG geometry proxy.

Run from repository root:
python -m unittest bubble_break/test_t_hammer_multiview_swing_engine.py -v
python bubble_break/t_hammer_multiview_swing_engine.py --outdir out/t_hammer_multiview_swing

## Acceptance boundary

Tests validate the geometry model, opposing normals, handle orthogonality, the H0/H2/H3 distance contract, camera frame variety, distinct wind-up profiles, prompt separation between Stage A and sphere scenes, and output counts. Tests do not prove what an image-generation model actually draws. The matrix deliberately records image_realization=NOT_RUN and pixel_audit=NOT_RUN until original raster outputs are attached and each selected image is reviewed.
