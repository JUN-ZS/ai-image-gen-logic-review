# Dense Hammer → Bubble Selection Workflow

Branch: `feat/dense-hammer-bubble-pick` (branched from `main`).

## Intent

Stage A is one image with a single large, intact translucent bubble and **24 complete, small, proportion-locked cylindrical-headed hammers** crowded around it, all aiming inward toward the same bubble. The front circular striking face of every hammer glows. This is a discovery image: the user chooses the one hammer whose position, axis and silhouette are right. That exact visual hammer—not a newly invented proxy—is the source asset for later stages.

This replaces the previous model of many short cylinders growing out of the bubble. Hammers are independent tools outside the shell, with their own rear handles. They do not grow from the bubble, do not have T/cross heads, and do not hit one another.

## Lessons carried forward from the rejected atlas

The prior dense-atlas raster was rejected because its repeated objects collapsed into near-identical isometric stamps, handles were not independently traceable, and bright sparks obscured the contact seam. Do not repeat those conditions.

- No regular grid, tile layout, repeated stamp motif, or identical projected pose.
- Use 24 larger, irregularly distributed candidates around one bubble; count never outranks readability.
- Vary each candidate's actual 3D surface location, local strike axis, perspective scale, projected tilt and handle roll. Do not rely on generic "vary the camera" alone.
- Each complete hammer must show a short cylindrical head, an independently traceable thin straight handle, and its own luminous circular striking face.
- Glow belongs on the **front terminal face aimed at the bubble**, not on the handle joint or an ambiguous sphere-base ring.
- The bubble remains intact in Stage A. No humans, hands, large sparks, cracks, shards or explosion.
- Keep a hairline visual gap (or an unambiguous just-touching plane) so the luminous face boundary remains visible. Hammers are approaching the bubble, not fused into or growing from it.

## Proportion contract for each Stage-A hammer

Let (D_b) be the bubble diameter, (D_h) the cylindrical head diameter, (H_s) the head's axial stub length, (L) the handle length, and (D_g) the handle diameter.

Initial candidate ratio:

- (D_h approx 0.08D_b)
- (H_s approx 1.5D_h)
- (L approx 3H_s)
- (D_g approx (D_h/2)/5 = D_h/10)

These ratios are the starting design grammar, not a claim that generated pixels exactly match a numeric manifest. The visible Stage-A raster is the authority for choosing the actual candidate; inspect the candidate's real projected proportion before locking it.

## Stage flow

### Stage A — dense discovery atlas

- Exactly one intact, translucent bubble dominates the composition.
- 24 independent hammers are crowded around the visible 3D bubble volume, distributed irregularly over depth and direction—not arranged in rows or tiles.
- Each hammer's glowing front circular face is aimed inward at a distinct bubble-surface point; its thin handle extends outward from the rear of the head, away from the shell.
- All 24 handles and faces should remain individually traceable. Candidates can overlap in the 2D projection only if their face and handle remain unambiguous; otherwise separate them.
- Label candidates C01–C24 beside the outer handle tail, never over the luminous face. Raster labels may be imperfect; user selection is based on the actual image and visible hammer, not a presumed match to proxy coordinates.
- Deliver a real generated raster for human selection. The geometry/SVG proxy alone does not pass this gate.

### Stage B — isolate one selected hammer and lock its raster geometry

Input: the exact Stage-A raster as image reference plus selected ID (for example C17). Use image-to-image/inpainting/editing against that raster; do not recompose from text alone.

- Keep the selected hammer's actual visible face center, 3D-facing direction as seen in the raster, local silhouette, and handle-to-head relationship. **The chosen raster hammer outranks generated world-coordinate guesses.**
- Remove all other 23 hammers and all their glows/ghosts completely.
- Keep the single selected hammer, its luminous front face, and the intact bubble. No human, hand, action redesign or large effect yet.
- If bubble/hammer scale is adjusted, scale the selected source asset deliberately and report the ratios. Do not silently move its contact point or flip its strike axis.
- Preserve the proportion grammar unless explicitly overridden: handle length (approx 3H_s), handle diameter (approx D_h/10), head face remains a flat circular terminal face aimed toward the bubble. Handle attaches continuously to the **rear** cap and extends away from the bubble.
- The stage must fail if the glowing face flips outward, handle points through the sphere, the shaft detaches, or the selected raster anchor drifts without authorization.

### Stage C — scale contract and add the person

Only after Stage B is approved:

- Use Stage B as the reference image. Add exactly one full person at the rear end of the existing handle, with visible, physically plausible hand grip.
- Preserve selected hammer head, glowing face, bubble surface and handle direction. Do not rebuild the tool.
- Apply configurable relative scale: bubble scale, hammer scale, and person height relative to bubble diameter. Default person height is a user-adjustable fraction of (D_b); no person is present in Stages A/B.
- A hand must visibly grip the shaft; do not let the body replace, bend or obscure the handle. Keep human anatomy and tool axis compatible.
- Record scale choices in the stage manifest; if geometry changes to improve framing, record it as a deliberate revision, not as a hidden success.

### Stage D — action refinement

Refine grip, stance, step, torso/shoulder rotation, attack wind-up and follow-through around the approved selected tool. Do not change the chosen face center, the direction the glowing face points, the rear-handle attachment, or the head/handle ratio unless the user explicitly requests a geometry change. No extra hammers return.

### Stage E — contact light and bubble-break spectacle

- Start from the approved Stage-D image.
- Intensify light from the selected circular face: a clean bright face core, controlled rim glow, a localized shell-contact bloom, and waves spreading across the sphere.
- Radial fractures must originate at the selected bubble contact point. For the break frame, shell fragments and luminous shock rings expand outward from that point.
- Provide a clean contact frame before the maximum bloom/debris frame. At least one frame must leave the glowing face boundary, rear handle connection and the person's grip readable.
- The other 23 hammers must remain absent in every later stage.

## Raster lock versus geometry proxy

The generator emits candidate coordinates and an SVG only to help organize the discovery atlas. **The proxy is not pixel evidence.** Image models can vary label placement, perspective and exact positions. After a real Stage-A raster exists, selection is confirmed from that raster; Stage B must use it as the image reference. Never claim that C17 is pixel-locked just because the program assigned C17 a 3D coordinate.

For stronger traceability, optionally provide `--source-raster` and `--roi x,y,width,height` when compiling a selected candidate. The compiler records the source image SHA-256 and actual selected image region. It still does not perform image generation or pixel audits.

## Acceptance gates

| Gate | Pass condition |
|---|---|
| `DENSE_HAMMER_ATLAS` | One intact bubble + 24 independent complete hammers + individually visible glowing front faces and traceable handles |
| `RASTER_SELECTION` | User identifies one real candidate in the generated raster; ID and visible location agree |
| `RASTER_GEOMETRY_LOCK` | Stage B uses the exact source raster/reference; selected face center, direction and scale do not drift silently |
| `SINGLE_HAMMER_ISOLATION` | Exactly one hammer remains, all other heads/handles/glows removed |
| `PROPORTION_LOCK` | Handle/head and bubble/hammer ratios are stated and checked in raster review |
| `PERSON_ATTACHMENT` | Exactly one person grips the same unaltered handle in Stage C |
| `ACTION_LOCK` | Pose can improve without unrequested tool-axis/contact drift |
| `CONTACT_EFFECT` | Glow and shell breaks originate at the selected face-to-bubble point; clean seam frame retained |
| `PIXEL_AUDIT` | Human review of actual generated rasters; prompt/unit tests are never image PASS |

## Run

```cmd
python bubble_break/dense_hammer_bubble_workflow.py --outdir out/dense_hammer_bubble
python bubble_break/dense_hammer_bubble_workflow.py --outdir out/dense_hammer_bubble_c17 --select C17
python -m unittest bubble_break/test_dense_hammer_bubble_workflow.py -v
```

The generator outputs prompt packets, deterministic candidate metadata, and a projection SVG. It does not call an image model. Until real raster images are generated and reviewed, image realization and pixel audit remain `NOT_RUN`.
