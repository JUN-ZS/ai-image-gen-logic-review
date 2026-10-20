# Original Sin / Wushuang Bubble-Break Prompt Engine

This subproject turns the useful narrative/compiler ideas in EFV V6.4 and Gumen Rock V7.0 into a specialized story-image prompt compiler. It does not copy the songs' lyrics. It borrows semantic motifs and structure: three-order meaning extraction, QCTH-F nine-cell beats, alpha/beta foreshadowing, front/side/inversion operators, and 55/30/15 continuity as a prompt-design heuristic.

## Why this is not just a prompt pile

Every concept starts with a distinct systemic flaw ("original sin"), the containment mechanism that enforces it, the human cost, evidence that reveals it, and a voluntary choice after the shell breaks. Visual axes vary shell construction, environment, scale, hammer finish, fracture appearance, camera rig, palette, and aftermath.

Each story exports four connected keyframes:

- H0: intact shell, no cracks, hammer face visibly separated from the exact six-o'clock bottom point.
- H1: reveal the containment mechanism; still no contact and no cracks.
- H2: first contact only between the hammer's thick upper terminal face and the shell's bottom point; cracks start there and propagate outward.
- H3: the shell is broken, residents remain alive and uninjured, and they regain the right to choose what happens next.

H0 and H3 share a locked camera, horizon, sphere center, environment landmarks, character identity, hammer dimensions, and light direction. The prompts carry an explicit coordinate contract:

- world up: +Y
- sphere center: C=(0,R,0)
- bottom contact: P=C+(0,-R,0)=(0,0,0)
- shell outward normal: n_target=(0,-1,0)
- hammer striking-face normal: n_hammer=(0,+1,0)=-n_target
- hammer velocity: v=(0,+V,0), V>0

The striking end-face is the only first contact. No shaft or side-head contact is allowed. The people are not targets; the containment mechanism is.

## Run

Python 3.10+; standard library only.

Windows CMD:

~~~cmd
python bubble_break\generate.py --count 100 --seed 20261020 --mode heroine --format jsonl --out out\stories.jsonl
python bubble_break\generate.py --count 1000 --seed 20261021 --mode dual --format csv --out out\stories.csv
python -m unittest discover -s bubble_break -p "test_*.py"
~~~

Linux/macOS:

~~~bash
python3 bubble_break/generate.py --count 1000 --seed 20261021 --mode heroine --format jsonl --out out/stories.jsonl
python3 -m unittest discover -s bubble_break -p 'test_*.py'
~~~

Formats: json, jsonl, csv, and md. One run is capped at 250,000 concepts. Valid combination count includes only permitted shell/fracture pairs. Sampling is stratified by SIN in shuffled rounds: any batch of at least 20 covers all 20 root-cause kernels, and counts per kernel differ by at most one. RAW Cartesian index space and filtered compatible-space count are separate; never use the latter as the decoder's raw-index upper bound.

### Modes

- heroine: same East Asian female Boundary Walker, long center-parted dark-brown hair, one mole under the left eye.
- abstract: removes the foreground heroine while retaining clear resident silhouettes and the hammer/shell geometry, so survival cannot disappear from the story.
- dual: emits separately addressable heroine and abstract variants. Do not feed the two variants as one combined prompt.


## Cross-to-cross anchor edit method

New experimental method: first register two thick plus-sign bodies face-to-face at exactly the same terminal plane. The target cross origin C and lower terminal face define the future bubble center and six-o'clock point P. Then edit only the target cross into a transparent sphere while preserving the attacking cross, contact face, handle and camera. After that edit passes pixel review, edit only the attacking cross into the final radial multi-face hammer. Run the generated proxy pipeline against an emitted layout.json; it produces two SVG references, separate target and attacker masks, and two separate edit prompts. The vector proxy mathematically fixes the terminal-face gap to zero; an external image editor can still shift pixels, so edited images must be reviewed and measured.


## Bulk-to-proxy realization bridge

The large JSONL generator remains story/cause sampling only. \`realize_batch.py\` selects a bounded number of records per causal kernel, then compiles topology-matched H0/H2/H3 prompts and geometry references, and builds the A/B/C proxy/edit packet. It defaults to T as the simple C test; pass \`--final-weapon RADIAL\` to test the canonical multi-face head or \`CROSS\` to preserve the plus proxy. No image service is called by this batch wrapper.

~~~cmd
python bubble_break\generate.py --count 1000 --seed 20261020 --mode dual --format jsonl --out out\wushuang_1000.jsonl
python bubble_break\realize_batch.py --input out\wushuang_1000.jsonl --outdir out\realize_T --per-kernel 1 --limit 20 --final-weapon T
python bubble_break\realize_batch.py --input out\wushuang_1000.jsonl --outdir out\realize_RADIAL --per-kernel 1 --limit 20 --final-weapon RADIAL
~~~

T and RADIAL are separate realization paths, not a claim they are equally faithful. The T head has a simpler silhouette and should be tested as a lower-complexity comparator. Every package retains \`image_realization=NOT_RUN\` and \`pixel_audit_status=NOT_RUN\` until real edited image files have been inspected. The pixel PASS claims from any external workspace are not accepted by this repository unless its image files and audit evidence are actually attached or reproducibly reachable.

## Front/end-frame workflow (visual compiler)

Do not ask the image model to place H0–H3 on one infographic. The frame compiler emits **three independent, standalone prompts** for the same shot: H0 (pre-impact endpoint), H2 (single-contact validation anchor), and H3 (post-impact endpoint). The primary before/after pair is H0 + H3; H2 exists to validate the contact geometry.

Windows CMD:

~~~cmd
python bubble_break\generate.py --count 1 --seed 20261020 --mode heroine --format jsonl --out out\one_story.jsonl
python bubble_break\frame_pipeline.py --input out\one_story.jsonl --outdir out\frame_packet --limit 1
python -m unittest discover -s bubble_break -p "test_*.py"
~~~

Linux/macOS:

~~~bash
python3 bubble_break/generate.py --count 1 --seed 20261020 --mode heroine --format jsonl --out out/one_story.jsonl
python3 bubble_break/frame_pipeline.py --input out/one_story.jsonl --outdir out/frame_packet --limit 1
python3 -m unittest discover -s bubble_break -p 'test_*.py'
~~~

Each story directory contains separate H0, H2 and H3 prompt files, a JSON manifest, a pixel-audit checklist, a machine-readable layout.json, and three separate deterministic SVG geometry blockouts. The SVGs use the same canvas and exact P projection; the hammer-face gap is fixed at 50 pixels in H0, 0 pixels in H2, and a 15-pixel follow-through past P in H3. They are geometry references, not final artwork. The compiler expresses geometry as visible primitives: silhouette, position, overlap, empty gap, contact patch, striking-face outline, fracture origin and fragment direction. The canonical weapon now follows `WEAPON_C_RADIAL_SPHERE`: one handle and one near-spherical head tiled with broad, flat, radially oriented striking faces, not the previous four-headed cross hammer.

Important boundary: shared prompts do not guarantee identical pixels. `PROMPT_CONTRACT_PASS` is text-only; the packet deliberately keeps `image_realization=NOT_RUN` and `pixel_audit_status=NOT_RUN` until real images are generated and checked side by side. Independent text-to-image endpoints can drift, so no software-only guarantee of perfect continuity is possible.

## Self-audit boundary

Each record contains an audit status and explicitly separates:

- PROMPT_CONTRACT_PASS: required geometry/state/survival clauses exist in the generated prompt text.
- image_realization: NOT_RUN: no image has been rendered or visually audited by this script.
- causal_kernel_id / causal_signature: root mechanism/cost/choice signature, distinct from visual-variant story_id.

That difference is intentional. A prompt checker cannot prove that an image model obeyed a prompt. The real acceptance loop is: generate H0/H1/H2/H3, compare shared geometry, reject any frame with early cracks or wrong contact, then re-render or correct only the failed frame.

## What 55/30/15 means here

It is used as a narrative attention budget (55% current subject, 30% transformed prior motif, 15% next-story foreshadowing), not as actual pixel compositing, calibrated model attention, or a physical constraint. The prompt compiler cannot enforce collision physics in the image model. For strict production, a 3D blockout/render, depth/normal/segmentation controls, or manual image correction can become the geometry source of truth, with the image model used for materials, atmosphere, and controlled detail.

## Inspiration lineage

- EFV V6.4: persistent electric pulse, broken signal, glassy traces, breath, tape-noise filaments, and a surviving flower-like light.
- Gumen Rock V7.0: old gates, well mist, copper mirrors, jade lamps, iron feathers, cracked-moon light, soul-fire, bells, ash, and thresholds.
- The new story engine repurposes these as alpha/beta visual seeds rather than copying lyric lines.

See also:
- https://github.com/JUN-ZS/efv-infinity-v6.4
- https://github.com/JUN-ZS/efv-gumen-rock-v7.0
