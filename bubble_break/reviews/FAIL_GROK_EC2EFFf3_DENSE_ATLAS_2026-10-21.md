# User visual rejection: dense CYLINDER_CROSS atlas

- Review date: 2026-10-21
- Branch under revision: `feat/cylinder-cross-dense-atlas`
- Source image: https://github.com/JUN-ZS/ai-image-gen-logic-review/blob/main/grok-ec2efff3-9206-447e-8436-3041078398a8.jpg
- Result: `USER_REVIEW_FAIL_ALL`
- Prior prompt revision: dense 48-target / implicit 8-column by 6-row atlas
- Do not use this image or its crops as geometry evidence.

## Observed failure

Visual inspection of the submitted image shows a dense repeated pattern of near-identical isometric objects. The field has little meaningful variation in the projected collision direction, hammer orientation, handle projection or framing. Most instances read as repetitions of one object arrangement rather than a deliberately varied sample of distinct 3D collision configurations.

The shafts/stems are not unmistakably legible as one long, separate handle attached to each individual hammer. The apparent central upright/post and diagonal rods collapse into a repeated shape; the image does not clearly establish two complete, independent tools with two clearly identifiable long handles per pair. The bright sparks also dominate the seam region, so the circular flat-cap planes and the exact cap-to-cap first-contact location are not consistently inspectable.

User acceptance result: all instances rejected. This is not a minor score deduction; the atlas fails its core purpose of producing varied, scannable collision candidates.

## Root cause hypothesis

The prompt made the model optimize for a large exact count in an implicit regular 8x6 layout, while also demanding one image with dozens of tiny interactions and many different camera descriptions. The model appears to have resolved that conflict by copying one compact isometric motif across the canvas. The imported single-pair negative prompt and general topology prose did not force the rendered result to preserve visibly long, separate handles or unique per-instance 3D orientations.

This is a prompt/layout failure, not evidence that the user should manually accept a subset of the current image.

## Mandatory corrective changes

1. Remove the implicit 8x6/tile-like arrangement and do not state exact row/column positions in the prompt.
2. Lower the first retry target to 24 larger, irregularly distributed collision pairs, with interaction readability and pose diversity taking priority over count.
3. Give each pair an explicit unique local collision axis, projected orientation, handle-roll relation, scale/framing and approximate region. Do not rely on generic "vary camera angle" wording alone.
4. Every single hammer must have an unmistakable long straight handle, attached at its own center joint, visibly extending far beyond the cross-head width. Both handles in every pair must be separately traceable and must not appear as tiny center pegs.
5. The horizontal crossbar ends must show short cylinders; each permitted contact occurs at the two outer flat circular end caps. Keep a visible, uncensored cap-to-cap seam. Contact sparks are small and peripheral, not a bright flare that hides the face geometry.
6. No copied/repeated object stamps, no uniform isometric orientation, no duplicate pair silhouette, no intersections between adjacent pairs, and no central-joint/handle contact.
7. Keep the original 48-image matrix path independent. An atlas image remains only a discovery aid and cannot pass the 48-H2 gate.

## Status

The submitted image remains `USER_REVIEW_FAIL_ALL`.
Any corrected prompt is `ATLAS_PROMPT_READY` only until a new real image is generated. After regeneration, the user must scan/crop promising regions; all crops start `CROP_CANDIDATES_UNREVIEWED`.
