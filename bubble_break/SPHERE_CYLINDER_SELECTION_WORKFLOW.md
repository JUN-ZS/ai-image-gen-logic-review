# Sphere-surface cylinder selection → handle/person → impact → bubble-break workflow

Branch: `feat/sphere-cylinder-pick-and-attach`, created from `main`.

## Why this replaces the all-at-once prompt

Do not ask an image model to invent the bubble, many cylinders, correct contact geometry, a weapon handle, a person's grip, a dynamic pose, and a large destruction effect in one pass. That mixes too many unknowns and encourages repeated camera angles, missing handles, false contact, and effects that hide the contact patch.

Use four gated stages. The human selects a stable candidate before later details are introduced.

## Stage 1 — candidate surface atlas (no people, no handles)

- Start with one intact, clearly spherical translucent bubble/shell.
- Place 25 **short cylindrical stubs** at distinct, well-spaced points across the visible hemisphere. Each has a flat circular base patch mounted directly against the bubble surface; cylinder centerlines point generally outward, with deliberate but modest differences in tilt.
- The **base-to-bubble interface** is the contact surface. Make that circular/elliptical interface emit a bright, clean rim glow. Do not confuse it with the cylinder's outer end cap.
- Keep every stub short. No long handles, hands, people, hammer heads, crosses, T-shapes, impact cracks, or major break effects in this stage.
- A deterministic candidate manifest and SVG geometry proxy label C01–C25. The proxy is an aid for choosing position/angle, not proof that an image model will rasterize the scene identically.
- Candidate IDs map to a world-space anchor and axis. The same manifest must be reused downstream; do not regenerate or renumber candidates after selection.

## Stage 2 — select exactly one candidate, then attach handle and person

Input: `--select Cxx`.

- Lock the chosen candidate's anchor, cylinder axis, local circular contact patch, and camera/view metadata.
- Keep the selected short cylinder as the striking head. Attach one long, straight handle concentrically to the cylinder's **outer/free end cap**, extending away from the bubble; this makes the person's push/swing direction traceable back to the selected contact patch.
- Add exactly one person whose hands visibly grip that long handle. The grip must be physically connected, anatomically plausible, and consistent with the locked handle axis.
- Remove all unselected cylinders entirely. No faint leftovers, duplicate heads, extra poles, phantom handles, or additional people.
- Preserve the intact bubble in this stage. The base contact ring may glow, but no large burst yet.

## Stage 3 — action refinement with geometry lock

Improve the person's whole-body action (wind-up, push, pivot, shoulder/hip rotation, foot placement, and follow-through) without moving the chosen contact anchor or changing the selected cylinder axis unless the user explicitly chooses a new candidate. Handle and cylinder remain one rigid, continuous assembly with no gap or bend at their joint. Use camera changes only as view changes; do not use a camera change to conceal a geometry error.

## Stage 4 — contact bloom and bubble-shell break

Only after Stage 2/3 is accepted:

- Intensify emission precisely at the chosen cylinder-base/bubble interface. Show a tight high-energy white-hot core, colored halo, concentric surface ripples, and cracks radiating across the bubble shell from that anchor.
- For the major break frame, the bubble surface fractures and bursts outward from the selected anchor; shards and luminous shock rings follow believable trajectories. Keep the selected cylinder, handle joint, hands, and person's pose readable.
- Effects must not cover the actual interface for the entire contact sequence. Provide at least one clean contact frame before the maximum bloom/debris frame.
- Delete all other candidate cylinders in the final image. The final bubble may be cracked/broken, but no unused candidate stubs remain.

## Data contract

Every candidate contains: stable ID, anchor point on the sphere, outward axis, tilt, glow style, and atlas projection coordinate. The selected candidate is immutable across stages. Prompts must include a negative-constraint block to prevent unselected cylinders and handles from reappearing.

## Acceptance gates

| Gate | Pass condition |
|---|---|
| `CANDIDATE_ATLAS` | intact bubble + distinct short stubs + legible base-interface glows; no people/handles |
| `SELECTION_LOCK` | a valid C01–C25 ID resolves to exactly one stored anchor/axis |
| `HANDLE_ATTACHMENT` | one long handle joins the selected stub's outer cap; no joint gap; one visible gripping person |
| `UNSELECTED_REMOVAL` | no other cylinder, handle, or ghost candidate remains after selection |
| `ACTION_LOCK` | dynamic body pose changes without unintended anchor/axis drift |
| `CONTACT_EFFECT` | glow/cracks originate at the selected base interface |
| `PIXEL_AUDIT` | actual generated raster is reviewed separately; prompt/unit tests do not count as image success |

If the chosen cylinder does not align with the action that the user wants, return to Stage 1 or choose another ID. Do not try to rescue a bad choice by deforming the handle or moving the contact point silently.

## Running the prompt pack

```cmd
python bubble_break/sphere_cylinder_selection_workflow.py --outdir out/sphere_cylinder_workflow
python bubble_break/sphere_cylinder_selection_workflow.py --outdir out/sphere_cylinder_workflow --select C07
python -m unittest bubble_break/test_sphere_cylinder_selection_workflow.py -v
```

The program produces prompts, a candidate JSON manifest, and an SVG position/angle proxy. It does **not** call an image model; actual generation and pixel review remain explicit downstream steps.
