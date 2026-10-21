# CYLINDER_CROSS dense-atlas generation handoff

## Goal

Use an image-generation model to produce **one single extremely dense 16:9 image** containing many distinct, independently croppable two-hammer interactions. The intended sampling layout is an implicit 8-column by 6-row field (48 target local collision pairs, 96 target hammer instances). This is a target composition, **not a claim that the image model will render all 48 correctly**.

## Source and generation bundle

- New branch: `feat/cylinder-cross-dense-atlas`
- Decision record: [CYLINDER_CROSS_DENSE_ATLAS_DECISION.md](./CYLINDER_CROSS_DENSE_ATLAS_DECISION.md)
- Generator: [cylinder_cross_dense_atlas.py](./cylinder_cross_dense_atlas.py)
- CI run: https://github.com/JUN-ZS/ai-image-gen-logic-review/actions/workflows/original-sin-bubble-break.yml
- The latest successful run's artifact is named `cylinder-cross-dense-atlas-and-contact-matrix-review-bundle`. Open the run, download its artifact ZIP, and use `cylinder_cross_dense_atlas/cylinder_cross_dense_atlas_prompt.txt` as the image prompt.

To compile locally:
```bash
python bubble_break/cylinder_cross_dense_atlas.py --outdir ./out/cylinder_cross_dense_atlas
```
This command writes the prompt, a crop-map manifest and a short README. It does not generate images.

## Copy/paste work order for the image-generation model

Generate **one image only**, not a batch of separate files. Use the full contents of `cylinder_cross_dense_atlas_prompt.txt`.

- One seamless, very dense 16:9 image.
- Target 48 local collision pairs in an implicit 8-by-6 field; no visible borders, grid lines, labels or dividers.
- Every intended pair is two separate plus-shaped cross hammers with one rigid straight handle fixed at each head's center.
- Opposite horizontal arms terminate in short solid cylinders.
- The only valid first-contact surfaces are the two outer flat circular end caps, touching flat face to flat face, with coincident planes and opposing normals.
- Curved cylindrical barrels, crossbar sides, vertical cross arms, corners and handles must not touch first.
- Every head and handle stays rigid: no bending, kinking, twisting, telescoping, detaching, or independent head/handle rotation.
- Keep neighboring pairs visually separate enough to crop; never merge a handle or head across neighboring instances.
- Vary horizontal, vertical, rising-diagonal and front-to-back collisions, plus camera angles and rigid handle rolls.
- Return the original full-resolution raster image. Do not return an SVG, redraw, storyboard, framed contact sheet, or claim that the generated image passed contact review.

If the model cannot render 48 unambiguous local examples, return the image as produced and report the uncertainty. Do not invent success or mark any crop as accepted.

## Crop and audit contract

The manifest lists intended instance IDs A01–A48, a nominal row/column location, camera/axis/handle-roll targets and each crop's initial status. These locations are planning aids; the model may not obey them precisely.

The user will scan the actual image and crop promising contacts. Each kept crop must be examined at full resolution for:
1. two designated flat circular end caps really touching face-to-face;
2. visible coincident cap planes and opposite normals, consistent with perspective;
3. no barrel-side, crossbar-side, cross-arm, corner or handle-first contact;
4. exactly two distinct collision partners, with rigid heads and handles and no cross-instance merging.

The atlas stays `IMAGE_REALIZATION_NOT_RUN` until a real image exists; all cropped options start `CROP_CANDIDATES_UNREVIEWED`; the pixel audit stays `PIXEL_AUDIT_NOT_RUN` until actual pixels are inspected.

**Important:** the dense atlas is a discovery/cropping aid and does not satisfy the independent 48-H2 evidence matrix gate. Old T-hammer images remain excluded.
