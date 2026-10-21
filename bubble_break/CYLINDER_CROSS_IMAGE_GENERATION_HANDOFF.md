# CYLINDER_CROSS image-generation handoff

## Required task

Generate **48 independent, full-resolution H2 images** to test the CYLINDER_CROSS contact geometry. This is an image-generation task, not a prompt rewrite or an SVG rendering task.

## Authoritative inputs

- Generated prompt/review bundle (GitHub Actions Run #128 artifact): https://github.com/JUN-ZS/ai-image-gen-logic-review/actions/runs/39547187827/artifacts/12322126438
- Run log and CI validation: https://github.com/JUN-ZS/ai-image-gen-logic-review/actions/runs/39547187827
- Matrix generator source: https://github.com/JUN-ZS/ai-image-gen-logic-review/blob/feat/original-sin-bubble-break-engine/bubble_break/cylinder_cross_contact_matrix.py
- Matrix source as raw text: https://raw.githubusercontent.com/JUN-ZS/ai-image-gen-logic-review/feat/original-sin-bubble-break-engine/bubble_break/cylinder_cross_contact_matrix.py

Download and extract the artifact ZIP. Use the files in `wushuang_CYLINDER_CROSS_contact_matrix/`. The source-of-truth map is `contact_matrix_manifest.json`; each variant has its own `H2.txt`, and the matching output filename is the variant's `required_H2_image` in that manifest. The ZIP is a temporary Actions artifact and has a limited retention period; save a local copy before it expires.

## Copy/paste work order for the image-generation AI

> Generate the 48 CYLINDER_CROSS H2 contact-proof images from the provided matrix bundle.
>
> Process every entry in `contact_matrix_manifest.json` exactly once. For each variant, read that variant directory's `H2.txt` and generate **one separate 16:9 image**. Save the result at the exact relative path specified by that variant's `required_H2_image`, retaining the full variant ID in the filename. Return one ZIP preserving the per-variant directory structure.
>
> **Geometry contract:** exactly two separate rigid plus-shaped cross hammers, each with one long straight handle fixed at the exact cross-center joint. The opposite horizontal crossbar ends terminate in short solid cylinders. The only permitted first-contact surfaces are the two outer **flat circular end caps**, meeting flat face to flat face with coincident planes and opposite normals. The curved cylindrical barrel walls, crossbar sides, vertical cross arms, corners and handles must not touch first. No bending, kinking, twisting, telescoping, detaching, or independent rotation of a head and its handle.
>
> Generate one image per H2 prompt. Do not make contact sheets, collages, storyboards, multi-panel images or replacement SVGs. Do not use any legacy T-hammer image as evidence. Do not invent, duplicate, omit, or rename variant IDs. Do not mark any review template PASS. Preserve each original prompt and include a manifest listing every output path and any generation failure.
>
> If a prompt appears physically ambiguous from a camera angle, still return its image and flag the ambiguity; do not silently replace the prescribed contact surface. Image generation alone does not pass the audit.

## Required delivery

1. One ZIP of the 48 generated PNGs with the manifest-prescribed names and directory structure.
2. A generation report listing all 48 variant IDs, output paths, image dimensions, and any failures.
3. No claims of contact PASS. The next stage must inspect each actual H2 PNG against its review checklist and fill the matching review JSON only after visual inspection.

## Acceptance constraints

- Expected images: 48 H2 PNGs, one per matrix variant.
- H0/H3 prompts are included for context but are **not part of this first image-generation batch**.
- The existing audit must remain BLOCKED until all required PNGs exist and every variant has a complete, image-matched manual review record.
- Old T-hammer candidate images are excluded from this evidence set.
