# CYLINDER_CROSS dense-atlas generation handoff

## Goal

Use an image-generation model to produce **one single extremely dense 16:9 image** containing many distinct, independently croppable two-hammer interactions. The revised target is 24 distinct collision pairs and 48 separate long handles, placed as an irregular organic scatter, not a uniform grid. This change responds to the failed first atlas, which repeated nearly identical isometric poses and did not make the two long handles per pair unmistakable. The 24 count is a target, not a guarantee; variation and complete readable tools are more important than an exact count.

## Source and generation bundle

- New branch: `feat/cylinder-cross-dense-atlas`
- Decision record: [CYLINDER_CROSS_DENSE_ATLAS_DECISION.md](./CYLINDER_CROSS_DENSE_ATLAS_DECISION.md)
- Generator: [cylinder_cross_dense_atlas.py](./cylinder_cross_dense_atlas.py)
- CI run: https://github.com/JUN-ZS/ai-image-gen-logic-review/actions/workflows/original-sin-bubble-break.yml
- Failure evidence and observed defects: [FAIL_GROK_EC2EFFf3_DENSE_ATLAS_2026-10-21.md](./reviews/FAIL_GROK_EC2EFFf3_DENSE_ATLAS_2026-10-21.md). Do not reuse or crop the rejected image as evidence.
- The current branch CI artifact is named `cylinder-cross-dense-atlas-and-contact-matrix-review-bundle`. Open the latest successful run on this branch, download its ZIP and use `cylinder_cross_dense_atlas/cylinder_cross_dense_atlas_prompt.txt`. Do not use the older Run #128 artifact because it contains the failed 48-target prompt.

To compile locally:
```bash
python bubble_break/cylinder_cross_dense_atlas.py --outdir ./out/cylinder_cross_dense_atlas
```
This command writes the prompt, a crop-map manifest and a short README. It does not generate images.

## Copy/paste work order for the image-generation model

Generate **one image only**, not a batch of separate files. Use the full contents of `cylinder_cross_dense_atlas_prompt.txt` from the revised branch artifact, not the old 48-target prompt.

- One seamless, very dense 16:9 image.
- Target 24 collision pairs placed as a dense, irregular scatter; no uniform grid, copied tile or repeated stamp pose.
- Every pair contains two separate complete plus-shaped cross hammers, two distinct heads and **two unmistakably long handles**. Each handle attaches at the exact center BACK of its own head and visibly extends at least 2.5 times the head width when framing permits. A central peg or short post is not a handle. The handle is perpendicular to the cross-head plane and is not the vertical cross arm.
- Opposite horizontal crossbar ends terminate in short solid cylinders.
- Only the two outer flat circular end caps may touch first, flat face to flat face, with coincident planes and opposing normals. The contact seam is at the outer cylinder tips, **never the center joint**.
- Curved cylindrical barrels, crossbar sides, vertical cross arms, corners, center joints and handles must not touch first. Keep sparks tiny and away from the cap seam so the circular contact stays visible.
- Every head and handle stays rigid: no bending, kinking, twisting, telescoping, detaching, or independent head/handle rotation.
- Make every pair visibly different in projected collision direction, handle-roll relationship, scale and depth placement. Show horizontal, vertical, rising/falling diagonal and front-to-back collisions; vary cap face-on/foreshortened views and handle projections. At least 16 distinct pair silhouettes are the target.
- Do not satisfy density by repeating one isometric motif or shrinking all tools into tiny icons. If needed, render fewer pairs rather than omit handles or fake variation.
- Return the original full-resolution raster image. Do not return an SVG, redraw, labels or visible grid. Do not claim that the generated image passed contact review.

If the model cannot render 48 unambiguous local examples, return the image as produced and report the uncertainty. Do not invent success or mark any crop as accepted.

## Crop and audit contract

The manifest lists intended instance IDs A01–A24, loose irregular region hints, collision-axis/projection/handle-roll targets and each crop's initial status. These are local composition cues, not grid coordinates or visible labels; the model may not obey them precisely.

The user will scan the actual image and crop promising contacts. Each kept crop must be examined at full resolution for:
1. two designated flat circular end caps really touching face-to-face;
2. visible coincident cap planes and opposite normals, consistent with perspective;
3. no barrel-side, crossbar-side, cross-arm, corner or handle-first contact;
4. exactly two distinct collision partners, with rigid heads and handles and no cross-instance merging.

The atlas stays `IMAGE_REALIZATION_NOT_RUN` until a real image exists; all cropped options start `CROP_CANDIDATES_UNREVIEWED`; the pixel audit stays `PIXEL_AUDIT_NOT_RUN` until actual pixels are inspected.

**Important:** the dense atlas is a discovery/cropping aid and does not satisfy the independent 48-H2 evidence matrix gate. Old T-hammer images remain excluded.
