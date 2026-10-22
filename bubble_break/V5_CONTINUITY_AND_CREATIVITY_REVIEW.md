# V5 → V5.1 Continuity, Real Generative Rerun & Causal Creativity Review

## 1. Executive Summary of Root Causes Identified in PR #3 & Solved in V5.1

In V5 (`autonomous_pipeline.py`), the pipeline appeared to enforce multi-stage locks and output `PASS` scores, yet exhibited four structural breaks between specification and execution:

| Problem Dimension | Legacy V5 Behavior | V5.1 Closed-Loop Engineering Solution |
| :--- | :--- | :--- |
| **Image Generation & `FAIL → RERUN`** | Read pre-existing paths or silently synthesized Pillow test rasters (`render_synthetic_stage_raster`) and marked `all_stages_passed=True`. On `FAIL`, wrote `REJECTED_*_repair_prompt.txt` to disk without invoking an image generator. | Requires a real `ImageGenerationBackend` (`backend.generate_candidates(...)`) or explicit verified rasters in production. If missing, halts with `evidence_mode="BLOCKED"` and `all_stages_passed=False`. On `FAIL`, compiles a targeted repair prompt + regional masks (`freeze_mask.png`, `edit_mask.png`) from the **last verified `PASS` parent raster** and calls `backend.generate_candidates(...)` in a true closed loop up to `max_rerun_rounds`. |
| **Synthetic Test vs. Production Evidence** | Allowed Pillow synthetic test rasters to pass as production runs (`all_stages_passed=True`). | Enforces strict separation: synthetic unit-test runs require `allow_synthetic_test_only=True`, set `evidence_mode="SYNTHETIC_TEST_ONLY"`, and hard-lock `all_stages_passed=False` (`synthetic_test_passed=True`). |
| **Batch Evaluation & Rollback** | Stopped at the first `PASS` candidate in a stage; if all candidates failed, allowed the highest-scoring `FAIL` image to propagate to the next stage. | Evaluates **100% of candidates** in every batch, filters to Layer-1 `PASS` candidates, and ranks them by Layer-2 Creativity & Pose Evolution (`layer2_creativity_score`). If all candidates fail after `max_rerun_rounds`, strictly **BLOCKS** the pipeline and never propagates a `FAIL` raster. |
| **5-Keyframe Timeline (`0s → 2s → 4.5s → 7s → 10s`)** | Synthesized `2.0s PRE_NEAR` via a Pillow pixel-shift splice (`shifted_far.paste(far_img, (36, -22))` + horizontal sigmoid ramp), leaving a visible vertical splice seam and composition jump, while skipping full cross-frame gates on `0s → 2s → 4.5s`. | Eliminates Pillow pixel-shift splicing for production runs. Every keyframe (`KF1_0S_PRE_FAR`, `KF2_2S_PRE_NEAR`, `KF3_4P5S_CONTACT`, `KF4_7S_E_MID_SHOCK`, `KF5_10S_E_END_BLAST`) is generated from the parent `PASS` keyframe via the generative backend and audited by all Layer-1 physical state gates, `gate_no_vertical_splice_seam`, `gate_static_background_stability`, and `gate_cross_frame_continuity`. |

## 2. Five Core Architectural Pillars of V5.1

### Pillar 1: Structured `SceneState` & Per-Frame `authorized_delta_fields`
Instead of treating each frame as an unconstrained text-to-image prompt, `SceneState` locks invariant scene parameters across the entire 10-second sequence:
- **Camera & Background Landmarks**: Locked 16:9 eye-level three-quarter framing, left dark basalt cliff pillar, upper-right distant citadel spire, and right obsidian pediment.
- **Protagonist Identity & Attire**: Same 1:1 miniature East Asian female warrior in matte charcoal-black tactical armor with subtle cyan seam trim.
- **Tool Geometry (`C13`)**: Dark-steel double-ended cylinder with 100% bare lower-left circular outer cap (`C_outer`) and a single straight metal rod attached flush at `90°` to the upper-left side-middle (`\`).
- **Per-Frame `authorized_delta_fields`**: Each keyframe only authorizes specific state transitions (`0.0s` wide air gap → `2.0s` narrowed positive air gap + forward lunge → `4.5s` zero air gap + first conformal cyan-white contact glow at `P` → `7.0s` radial cracks & concentric shockwaves from `P` → `10.0s` shell-only shatter revealing the intact warm interior sanctuary).

### Pillar 2: Parent-Image + Regional Mask-Protected Editing (`MaskProtectedEditor`)
For every stage and keyframe transition, `MaskProtectedEditor.build_stage_masks(...)` generates explicit binary/alpha masks (`freeze_mask.png` and `edit_mask.png`) saved alongside the candidate audit logs:
- **Frozen Regions (`freeze_mask`)**: Static background landmarks, lower-left bare circular end cap exterior, and unathorized regions.
- **Authorized Edit Regions (`edit_mask`)**: Active air-gap corridor, warrior articulation zone, contact interface `P`, and (for `7.0s`/`10.0s`) the fracturing outer bubble shell.

### Pillar 3: True Closed-Loop Rerun (`ImageGenerationBackend`)
- `CallableImageGenerationBackend` wraps any real image generation/editing model endpoint (`image_gen:generate_image` or custom diffusion/inpainting backend) behind a deterministic contract receiving `SceneState`, `parent_image_path`, `freeze_mask_path`, `edit_mask_path`, `prompt`, `attempt_round`, and `rejection_reasons`.
- On any Layer-1 gate failure, `compile_elevation_prompt_repair(...)` diagnoses the exact failed gate metrics and triggers a live backend rerun inheriting the **last verified `PASS` parent raster**.

### Pillar 4: `OriginalSinCausalEngine` (9-Step Narrative Causal Chain)
Transforms "Original Sin" from decorative text into a physical and visual causal engine verified at `10.0s`:
1. **Institutional Promise (`制度承諾`)**: Sealed crystalline dome marketed as "Eternal Harmonic Protection" for the miniature terraced sanctuary city.
2. **Hidden Mechanism (`隱藏機制`)**: Parasitic resonance lattice siphoning warmth, memory, and agency from the inhabitants into the shell's outer refraction layer.
3. **Visible Symptom (`可見症狀`)**: Cold cyan-violet refractive glaze on the outer shell while the interior city grows dim and muted.
4. **Human Cost (`人的代價`)**: Citizens inside are frozen in repetitive loops, deprived of choice and open sky.
5. **Clue (`線索`)**: A phase-lock nodal seam at upper-left surface point `P` where the lattice's structural tension concentrates.
6. **Protagonist Discovery (`主角發現`)**: The warrior identifies that axial end-cap strikes bounce off the dome, whereas a normal-aligned radial cylinder pinned at `P` and torqued via a `90°` side-middle lever disrupts the lattice phase.
7. **Physical Action (`針對機制的物理行動`)**: From `0s` windup (`PRE_FAR`) through `2s` approach (`PRE_NEAR`) to `4.5s` flush contact (`CONTACT`), she plants the cylinder head at `P` and drives torque through the upper-left side rod.
8. **Shell-Only Breach (`只破除泡殼`)**: At `7s` (`E_MID`), radial cracks fracture only the parasitic outer shell; at `10s` (`E_END`), brittle refractive shards burst outward into the dark void without harming the interior city.
9. **Restored Agency (`居民重新取得選擇權`)**: Warm golden-amber lantern light and open air return to the intact miniature terraced sanctuary as citizens look up freely.

### Pillar 5: Two-Layer Evaluation (`先過連貫，再比創意`)
- **Layer 1 (Hard Continuity & Physical State Gates)**: Rejects any candidate that fails single-frame/no-grid check, parent SHA provenance, `C13` outer-end empty check, `90°` upper-left handle slope check, exact time-axis air-gap state (`0s` wide gap, `2s` narrower positive gap, `4.5s+` zero gap + contact glow), causal fracture progression, `gate_no_vertical_splice_seam`, `gate_static_background_stability`, or `gate_cross_frame_continuity`.
- **Layer 2 (Creativity, Pose Evolution & Sanctuary Agency Ranking)**: Among candidates that pass 100% of Layer-1 gates, computes `layer2_creativity_score` rewarding genuine warrior pose progression (`pose_delta` inside the warrior ROI, preventing high-NCC statue freezing) and `10.0s` interior sanctuary warmth/visibility (`warmth`).
