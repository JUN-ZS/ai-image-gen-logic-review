# SHQ Execution Contract v1.2 — anti-forgetting / anti-substitution

**Purpose:** stop the agent from remembering the name SHQ while silently changing the method, anchor source, or acceptance meaning.

## 0. Governing rule

A skill document is not proof of execution. Every run must have:
- a fixed `run_id`;
- one selected `method_id` from `SHQ_METHOD_REGISTRY.json`;
- exact source image SHA-256 values;
- a persistent `RUN_STATE.json`;
- machine-checked phase transitions;
- separate evidence for geometry, size, placement and pixel integrity.

No free-text `PREFLIGHT PASS` is accepted without a successful guard execution and its JSON output.

## 1. Do not merge these methods

The v1.1 skill currently describes two related but distinct fit rules. They must be selectable, not blended:

### A. `SHQ_BEST_CORE_V1_1` — single humanoid gold path
- Estimate scale/rotation from trusted Face + Torso/core anchors.
- Use sole/ground to solve translation and horizontal contact.
- Hands, legs and cape are validation groups; do not let a low-confidence limb point distort the core scale.
- Scene expands by approximately `1/a`; donor remains 1.0.

### B. `DDXX_WHOLEBODY_SIMILARITY_V1` — whole-body landmark fit
- Fit paired semantic landmarks with weighted Umeyama + Huber IRLS:
  `q = a * (p @ R) + t`.
- Compare similarity fit with scale+translation-only. Keep rotation only when it is supported by the data.
- Use `S=1/a` and the inverse scene transform. Never apply anisotropic scale/shear to the donor.
- The recorded 11-point contact-sheet case (a≈0.448974, rotation≈4.517°, RMSE≈7.512 target-panel px) is a **solver regression fixture only**. It is not a universal pose threshold and not production proof: points were manually estimated on flattened panels and the donor cape was clipped.

### C. `DDXX_MECHA_CORE_SIMILARITY_V1` — one machine at a time
- Use machine-semantic core anchors: head, chest, pelvis, left/right shoulder joints.
- Validate arms, legs, feet, weapon/shield axes, wings/backpack and silhouette independently.
- Do not use human DWPose semantics on a Gundam.
- Do not relabel arbitrary silhouette contour samples as knees, ankles or feet. A silhouette point touching rubble is not a semantic joint.
- If the pose/weapon/wing articulation differs, reject the donor and regenerate from the pose map. Do not try to fix a different pose with translation or global similarity.

### D. `SHQ_MULTI_RETURN_V1`
- Phase A: N separate SOLO jobs. In SOLO_i, only object i is the subject; the other N−1 objects are scenery/context.
- Each unit gets its own target mask, landmarks, fit, size/aspect audit, pose gate and donor.
- Phase B only after all required SOLO units pass: common EMPTY scene, one declared scene transform, then N hard pastes in audited z-order.
- If a common `S_star=max(S_i)` is used, report every `ratio_i=S_star/S_i`. Any ratio outside tolerance is a composition compromise, not exact slot fit.
- Never use a single Group Plate or one shared fit for multiple independent subjects.

## 2. Phase state machine (no skipping)

Allowed states:
`PREFLIGHT → TARGET_CAPTURED → ANCHORED → FIT_DONE → DONOR_READY → POSE_GATE_DONE → READY_TO_PASTE → FINALIZED`

A failed gate moves to `BLOCKED_<REASON>`; it cannot be bypassed by changing report wording.

Required phase evidence:

| Phase | Required evidence |
|---|---|
| PREFLIGHT | canonical version, method_id, unit count, golden solver regression result, no-repeat list loaded |
| TARGET_CAPTURED | original target SHA, SOLO crop, target mask, target coordinate frame/crop offset, pose/shape maps |
| ANCHORED | target and donor semantic anchor JSON, confidence, source SHA, overlay audit |
| FIT_DONE | method_id, a/R/t, inverse scene transform, per-anchor residual CSV, robust weights, scale-only comparison |
| DONOR_READY | fit-derived required native W+H/AR, independent donor per unit, donor SHA, alpha and design identity |
| POSE_GATE_DONE | target-referenced pose report, silhouette/limb/object-axis residuals |
| READY_TO_PASTE | native size + AR pass, pose pass, fit pass, donor is not resized, all required units pass |
| FINALIZED | exact hard-paste report, donor SHA provenance, core pixel comparison, final dimensions, z-order and composition report |

## 3. Pose reference cannot be circular

For an AI/detail stage, two different checks are required:
1. `TARGET_TO_BASE`: accepted original TARGET → soft/GENFIT pose base. This proves the base preserved the original action.
2. `BASE_TO_DETAIL`: accepted soft base → AI detail output. This proves detail enhancement did not change the accepted base.

A pass on check 2 cannot substitute for check 1. A pose report must record `primary_reference_role=ORIGINAL_TARGET` and the exact TARGET SHA. Comparing AI output only with its own soft extract/soft GENFIT is not a target-pose pass.

## 4. Acceptance is a vector, not one boolean

Never infer one dimension from another:

- `ANCHOR_VALIDITY`: points lie on the intended semantic feature and source frame is known.
- `POSE_GEOMETRY`: pose/shape/object axes match the original target.
- `NATIVE_SIZE_AND_ASPECT`: both W and H and alpha bbox/AR are checked.
- `PLACEMENT`: donor_xy / feet / ground placement is correct.
- `PIXEL_PROVENANCE`: donor source pixels are unchanged; hash/core comparison is grounded.
- `LAYER_AND_OCCLUSION`: overlap ownership and far-to-near order are correct.
- `FINAL_COMPOSITION`: final scene reads correctly.

`feet_lock < 1px` only passes PLACEMENT. `core_exact=1.0` only passes a pixel-integrity subtest. Neither can set POSE or FULL to true.

## 5. Multi-unit hard block

For N>1:
- `unit_count` must equal the number of unique unit IDs.
- every unit must have an independent TARGET, POSE_MAP, DESIGN_SPEC, DONOR and report;
- all donor SHA values must be recorded; accidental identical donors are blocked unless explicitly allowed;
- one failed unit blocks `ACCEPT_MULTI_FULL`;
- any `SIZE_REJECT`, `POSE_WARN`, `ANCHOR_INVALID`, missing donor or AR drift blocks final acceptance;
- group generation is diagnostic only and cannot be substituted for N independent SOLO jobs.

## 6. No-repeat rules added from the supplied V6/V14/V15/V16 evidence

- **E-SHQ-24 KNOWLEDGE_EXECUTION_DISCONNECT:** skill is not loaded/verified at run start → BLOCK.
- **E-SHQ-25 METHOD_COLLAPSE:** silently mixing SHQ core-fit and DDXX whole-body fit → select one method_id and freeze it.
- **E-SHQ-26 ANCHOR_SEMANTIC_DRIFT:** arbitrary silhouette/rubble samples passed as joints → use semantic annotations and overlay audit.
- **E-SHQ-27 CIRCULAR_POSE_GATE:** AI compared only to its own soft extract/base → require TARGET_TO_BASE and BASE_TO_DETAIL separately.
- **E-SHQ-28 ONE_DIMENSION_GENFIT:** only H locked while W/AR drifts → lock both W and H and donor alpha bbox.
- **E-SHQ-29 PLACEMENT_POSE_SUBSTITUTION:** foot lock/core exact called pose pass → separate acceptance dimensions.
- **E-SHQ-30 MULTI_GROUP_SUBSTITUTION:** N subjects treated as one group → N SOLO runs.
- **E-SHQ-31 COMMON_SCALE_HIDDEN_COMPROMISE:** S_star used without each ratio_i → report compromise or block.
- **E-SHQ-32 LAYER_PROVENANCE_MIX:** soft peep and AI donor mixed without layer class/provenance → normalize donor class or keep output diagnostic.
- **E-SHQ-33 PARTIAL_UNIT_LEAK:** one SIZE_REJECT/WARN unit still enters accepted MULTI → any required unit failure blocks full assembly.
- **E-SHQ-34 ACCEPTANCE_STATUS_INFLATION:** a partial/core status upgraded to FULL in prose → statuses must be computed from evidence, not authored manually.
- **E-SHQ-35 GOLDEN_THRESHOLD_MISUSE:** human screenshot residual reused as a mecha threshold → golden fixture tests solver math only; thresholds are calibrated by object class and annotation source.

## 7. Golden regression — what it proves and what it does not

Run the supplied `DDXX_MANUAL_PANEL_GOLD_01` fixture before changing the solver. It should reproduce the recorded similarity parameters within fixture tolerance (approximately a=0.448974, rotation=4.517°, weighted RMSE=7.512px in that panel coordinate system).

This checks that the implementation has not changed. It does **not** prove a new target/donor pair is aligned, does not certify annotations, and does not establish a universal RMSE cutoff.

## 8. Session resume / anti-amnesia

At every new session:
1. Read the canonical SKILL, this contract, method registry and DO_NOT_REPEAT.
2. Load the last `RUN_STATE.json`; verify its input/output SHAs.
3. Resume from the last artifact-backed phase, not from conversational memory.
4. Do not rerun or replace a frozen `a,R,t,S,donor_xy` unless a new run_id is created and the reason is recorded.
5. If the previous evidence is absent, status is `STATE_NOT_REPRODUCIBLE`; never reconstruct a PASS from prose.

**Hard principle:** memory is a convenience; artifacts + hashes + executable gates are the authority.
