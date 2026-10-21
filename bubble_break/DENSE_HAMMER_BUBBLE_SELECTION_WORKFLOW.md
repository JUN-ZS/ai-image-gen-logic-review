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

## Stage C — add one person (hard locks)

After Stage B is accepted:

### HARD LOCK A — `NO_NEW_HANDLE`
- **Do not add, grow, extrude, or invent any new handle / shaft / rod.**
- Do not convert the tool into (head + coaxial long shaft).
- Do not attach any rod to the outer end cap or through the glowing base.
- The **only** handle is the existing single thin **side-middle lateral** rod on the Stage-B raster.
- Hands grip **that same existing** lateral handle only. If grip is hard, move the person — never grow a new shaft for convenience.
- Growing a new handle or changing handle axis is **REJECT** (same error class as outer-end quasi-axial shaft).

### HARD LOCK B — person : hammer = **1 : 1**（人變迷你）
- `person:hammer = 1:1` means the person's **full body** and the locked **hammer assembly** occupy roughly the **same visual area** in the frame — the person is **mini** beside the large bubble（全身面積 ≈ 槌面積）.
- `person_to_hammer_scale = 1.0` default hard lock.
- **REJECT** if person is life-size / much larger than the hammer (`person >> hammer`).
- **REJECT** if person is an ant-speck much smaller than the hammer (`person << hammer`).
- **Not** `k × bubble diameter`. Scale the mini person to the hammer area; do not enlarge the hammer.

Also:
- Use the isolated Stage-B image as the reference. Record bubble/hammer/person ratios; do not silently move the anchor.
- Add exactly one person after object proportions are stable. Plausible wrist/arm connections on the **existing** sideways handle.
- Preserve double-ended cylindrical head, glowing base contact, side-middle handle attachment and tangent handle direction.
- No other hammers return. Do not add the person in Stage A/B.



## Script gates after every full RUN step (mandatory)

**Root cause locked into formula:** the error step was *skipping D1/D2*, or *first grip (D2) without hard-locking the previous frame's side-handle pixels*. Under correct IMG→IMG chain, a new outer-end handle must not appear; if it does, the step gate FAILs.

### Chain (no skip)
`D0 → D1 → D2 → D3 → D4` only. `validate_step_transition` rejects jumps.

### First grip (D2)
- `prev_raster_sha256` = accepted **D1** SHA
- Hands move only onto **existing side-handle pixels** in that D1 raster
- Prompt includes `PIXEL LOCK (FIRST GRIP / D2)`

### Pixel gates (block_next on FAIL)
After each IMG→IMG, before next step:
1. `outer_end_empty` — outer-cap ROI must not show a rod-like protrusion
2. `side_handle_present` — side-handle ROI must show elongated rod
3. Overall FAIL → write `BLOCK_NEXT_AFTER_Dx` and **do not proceed**; roll back

```bash
python -m bubble_break.stage_d_gates --step D2 --from D1 \
  --image D2.jpg --prev-sha <D1_sha256> --use-default-rois \
  --out D2_gate.json
```

Module: `bubble_break/stage_d_gates.py`.

## Stage D stepwise protocol (mandatory — 一步步)

Outer-end / coaxial **new handle must not appear** under the layered formula stack. If it appears, the step is **REJECT** and must be redone — do not proceed.

Do **not** jump to full action+grip in one shot. Order is fixed:

| Step | Name | Allowed change | Frozen |
| --- | --- | --- | --- |
| D0 | Topology freeze | none (re-show B master only) | head, base glow, outer cap empty, side-middle lateral handle only |
| D1 | Mini person place | add mini person (full-body area ≈ hammer area); **hands not gripping** | all hammer topology; `NO_NEW_HANDLE` |
| D2 | Grip existing handle only | move hands onto **existing** side-middle lateral rod only | person scale; outer cap empty; no new shaft |
| D3 | 找／持槌氣勢＋動作 | stance, weight, eyes, intent (still planted) | topology + grip on existing handle only |
| D4 | Optional polish | clothing/lighting only | everything above |

**Kill rule:** any outer-end rod, second shaft, or handle-axis rewrite → REJECT that step; roll back to last PASS step. Formula pressure layers: B topology lock → `NO_NEW_HANDLE` → person:hammer 1:1 mini → grip-only-existing → then action.

## Stage D — action refinement

Improve stance, torso/shoulder rotation, grip, weight transfer, and motion around the selected planted-hammer assembly. Any intentional handle lift/removal from the contact surface must be a separate state, not hidden in a frame claimed as still planted. Do not bend or detach the handle, flip the head, silently move the anchor, grow duplicate handles, or grow any new outer-end coaxial shaft (`NO_NEW_HANDLE` remains locked).

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
| `PERSON_ATTACHMENT` | Stage C adds one mini person (full-body area ≈ hammer area) gripping the **same existing** lateral handle; `NO_NEW_HANDLE`; person:hammer = 1:1 |
| `ACTION_LOCK` | Pose refinement does not silently detach the planted base or distort the rigid assembly |
| `CONTACT_EFFECT` | Glow/cracks originate at the planted base contact; a clean seam frame is kept |
| `PIXEL_AUDIT` | Human review of real generated rasters; prompt/unit tests alone never count as image PASS |


## Stage C failure class (observed 2026-10-21)

When a person is added, image models often rewrite the tool as `head + coaxial long shaft` so hands have a familiar hammer grip. That **outer-end / quasi-axial shaft** is the same topology error as a rejected Stage-B handle-axis failure.

Mitigation written into Stage-C prompts and gates:
1. `NO_NEW_HANDLE` — only the existing side-middle lateral rod may be gripped.
2. `person_to_hammer_scale = 1.0` — mini person: full-body visual area ≈ hammer area (人變迷你), not life-size vs bubble, not k×bubble.

## Topology repair note (Stage B)

If Stage B isolation loses the lateral handle, repair in two steps: (1) ensure a **lateral** (non-axial) rod exists; (2) move the joint to **side-middle**. Do not invent a handle from the outer end cap in one shot.

## Run the prompt compiler

```cmd
python bubble_break/dense_hammer_bubble_workflow.py --outdir out/dense_hammer_bubble
python bubble_break/dense_hammer_bubble_workflow.py --outdir out/dense_hammer_C17 --select C17
python -m unittest bubble_break/test_dense_hammer_bubble_workflow.py -v
```

The compiler emits a Stage-A formula prompt, stable candidate metadata, an SVG proxy and, after a selection, Stage B–E formula prompts. It does not call an image-generation model. Until real rasters are generated and inspected, `image_realization=NOT_RUN` and `pixel_audit=NOT_RUN`.
