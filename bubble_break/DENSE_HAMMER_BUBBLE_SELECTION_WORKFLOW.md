# Double-Headed Round Hammer Planted on Bubble — Formula Prompt Workflow

Branch: `feat/dense-hammer-bubble-pick`, from `main`.

## Correct object grammar

The hammer is **not** a projectile pointing toward the bubble and its head is **not** aimed end-on at the sphere.

The visual grammar is like many trees planted on a spherical surface:

1. A short, solid, double-ended cylindrical round-hammer head stands outward from the bubble at a surface anchor. Its two axial ends are both circular caps; the head is a cylinder, not a ball, spike, T-crossbar, or single flat disc.
2. The bubble-facing base cap is seated fully against the bubble at the chosen anchor. No floating gap. Represent the interface as a flush, sphere-conforming contact seat / small conformal pad so the contact footprint follows the bubble's local curvature rather than pretending a flat disk can perfectly mate to a curved sphere.
3. The circular contact footprint / seam at the base cap glows. This is the selected contact surface. The glow belongs where the cylinder is planted on the bubble—not on the upper cap and not at the handle joint.
4. A single long, thin, straight handle grows **sideways from the cylindrical head's side**, near its middle. The handle direction lies in the local tangent plane and is perpendicular to the head's radial axis: a clear sideways branch from the planted cylinder. It is not coaxial with the head, not attached at the bubble's contact base, and not pointed through the sphere.
5. In Stage A, this makes 24 complete planted round-hammer assemblies resemble many individually oriented trees growing out of one bubble. No people yet.

## Proportion formula — common master scale

Let:
- (D_b): bubble diameter
- (D_h): cylindrical hammer-head diameter
- (H_h): hammer-head axial length ("stub" height)
- (L_g): sideways handle length
- (D_g): handle diameter

Initial master ratios:
- (D_h = 0.08D_b)
- (H_h = 1.5D_h)
- (L_g = 3H_h)
- (D_g = D_h/10), i.e. approximately one fifth of the head radius

All Stage-A candidates use the same ratios. Candidate differences are their sphere anchor, local radial/head axis, tangent handle direction and projection—not arbitrary per-hammer scale changes.

These are parametric design targets. A real generated raster can deviate. The SVG and JSON are navigation/geometry aids, **not** proof that the image pixels match the coordinates.

## Stage A — dense planted-hammer atlas (no people)

- Exactly one large, intact, translucent spherical bubble.
- 24 complete double-ended cylindrical round hammers are densely distributed at irregular points over the visible bubble surface, like planted trunks.
- Each head's long axis follows the local outward sphere normal. The bubble-facing circular base cap is fully seated at the bubble by a sphere-conforming contact footprint; the contact seam glows clean white/cyan/amber.
- Each head has a clearly visible outer circular cap as well. Do not replace the cylinder with a sphere or hide the two-ended cylinder identity.
- One thin straight handle attaches to the **side-middle** of each head. It extends sideways in the local tangent plane, approximately 90° to the radial head axis. Vary its tangent direction around the sphere to produce genuinely varied projected orientations.
- Each full head, side joint and full handle must be independently traceable. Labels C01–C24 sit near handle tips and never cover the glowing base interface.
- No people, hands, swing motion, hammer-to-hammer collisions, cracks, shards, blast, smoke, or huge sparks. The bubble remains intact.
- Do not use a regular grid, repeated isometric stamps or a contact-sheet/tile composition. Count never outranks visibility.

## Stage B — select one real raster hammer and isolate it

Input: actual Stage-A generated raster + chosen visible ID (for example C17). This is an image-reference / edit / inpainting stage, not a fresh text-only redraw.

- Use the selected hammer as it actually appears in the raster. The source raster outranks proxy coordinates if they differ.
- Preserve its planted anchor, bubble-facing base cap, luminous contact seam, full cylinder head, side-middle handle joint and sideways handle direction.
- Remove the other 23 hammer heads, handles, IDs, glows and ghost components completely.
- Keep the bubble intact; still no person or action redesign.
- Lock the master ratios: (H_h=1.5D_h), (L_g=3H_h), (D_g=D_h/10), unless the user explicitly asks for a new scale.
- If the candidate ID/position is ambiguous, BLOCK and ask for the source image region; do not silently map a proxy ID to a different pixel object.

## Stage C — adjust bubble/hammer ratio, then add one person

After Stage B is accepted:
- Use the isolated Stage-B image as the reference. Choose explicit bubble and hammer scale factors and record them in the manifest; do not silently move the anchor.
- Add exactly one person after the object proportions are stable. Person height is configurable relative to bubble diameter. Ensure their hand(s) visibly grip the **same sideways handle** with plausible wrist/arm connections.
- Preserve the double-ended cylindrical head, glowing bubble-facing base contact, side-middle handle attachment and selected tangent handle direction.
- No other hammers return. Do not add the person in Stage A/B because it distorts object scale and makes candidate selection harder.

## Stage D — action refinement

Improve stance, torso/shoulder rotation, grip, weight transfer, and motion around the selected planted-hammer assembly. Any intentional handle lift/removal from the contact surface must be a separate state, not hidden in a frame claimed as still planted. Do not bend or detach the handle, flip the head, silently move the anchor, or grow duplicate handles.

## Stage E — contact glow and bubble-break effects

Start from the accepted Stage-D raster:
- The first bright source is the selected **bubble-facing base contact footprint**, not the outer cap and not the handle joint.
- Build a clean contact core and rim, then surface ripples and cracks that originate at that anchor.
- For the spectacle frame, show the translucent bubble shell breaking outward from the selected base contact, with a shock ring and coherent curved shards.
- Keep one clean frame where the base seam is visible before the maximum bloom/debris. Effects must not obscure the joint/base boundary in every frame.
- The remaining 23 hammers remain absent.

## Evidence and gates

| Gate | Pass condition |
|---|---|
| `DOUBLE_HEADED_PLANTED_ATLAS` | 24 cylindrical double-ended heads planted on the bubble; base interfaces glow; side handles are tangent/perpendicular and individually readable |
| `RASTER_SELECTION` | User selects one hammer from the actual Stage-A raster, by ID and visible position |
| `RASTER_ANCHOR_LOCK` | Stage B uses the actual raster reference; no proxy-only claim of pixel alignment |
| `SINGLE_HAMMER_ISOLATION` | One selected hammer remains; the other 23 fully disappear |
| `RATIO_LOCK` | (H_h=1.5D_h), (L_g=3H_h), (D_g=D_h/10) unless explicitly revised |
| `PERSON_ATTACHMENT` | Stage C adds one person gripping the same lateral handle |
| `ACTION_LOCK` | Pose refinement does not silently detach the planted base or distort the rigid assembly |
| `CONTACT_EFFECT` | Glow/cracks originate at the planted base contact; a clean seam frame is kept |
| `PIXEL_AUDIT` | Human review of real generated rasters; prompt/unit tests alone never count as image PASS |

## Run the prompt compiler

```cmd
python bubble_break/dense_hammer_bubble_workflow.py --outdir out/dense_hammer_bubble
python bubble_break/dense_hammer_bubble_workflow.py --outdir out/dense_hammer_C17 --select C17
python -m unittest bubble_break/test_dense_hammer_bubble_workflow.py -v
```

The compiler emits a Stage-A formula prompt, stable candidate metadata, an SVG proxy and, after a selection, Stage B–E formula prompts. It does not call an image-generation model. Until real rasters are generated and inspected, `image_realization=NOT_RUN` and `pixel_audit=NOT_RUN`.
