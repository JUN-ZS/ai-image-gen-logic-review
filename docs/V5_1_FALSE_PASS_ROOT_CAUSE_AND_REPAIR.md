# V5.1 False-PASS Root Cause Audit and Repair

## Scope

Audited branch `feat/v5.1-closed-loop-continuity` at commit `172f665216d95d0756a03c428d0e54b989456bd4`, including `bubble_break/autonomous_pipeline.py`, `bubble_break/stage_d_gates.py`, `.github/workflows/dense-hammer-bubble-workflow.yml`, and `out/v5_1_run/AUTONOMOUS_RUN_MANIFEST.json`.

The conclusions below are code/manifest findings. A manifest PASS is not treated as proof that the pixels are correct.

## Confirmed root causes

1. **Evidence contract was contradictory.** The stored manifest says `evidence_mode=REAL_GENERATIVE_RASTER`, `status=PASSED`, `all_stages_passed=true`, and `synthetic_test_passed=true` at once. The committed production branch in `run_autonomous_pipeline` set `synth_passed = True` even on the real-raster branch. The report had no invariant preventing this contradiction.

2. **D2 could be an unchanged copy of D1 and still pass.** The stored manifest's D1 and D2 have the exact same SHA-256 `4383492de569416281b24e360c239072d2df9909ddb5170557240476f4fee9bc`. D2's `parent_sha256` is also identical to the candidate's SHA. The action-step checker had no required-change/no-op gate; a high NCC score can reward identical frames rather than reject a missing first-grip action.

3. **Keyframe first-generation prompts were placeholders.** Backend calls sent literal strings such as `INITIAL_D1` and `INITIAL_KF2_2S_PRE_NEAR`, not the compiled generation instructions. A connected generator therefore did not receive the necessary scene or physical contract at initial generation.

4. **Repair prompts conflated three distinct story states.** `KF1_0S_PRE_FAR`, `KF2_2S_PRE_NEAR`, and `KF3_4P5S_CONTACT` all received the D3 action prompt in the repair compiler. Thus the prompt compiler itself was flattening far-windup, near-approach and first-contact into one state. `E_MID` and `E_END` also shared the same generic break prompt without a separate middle-vs-final state contract.

5. **The first keyframe was not raster-parented to D2.** The code copied D2's SHA into `kf_prev_sha` but set `kf_prev_img = None`; it then deliberately omitted the parent raster from KF1 audit. That is metadata-only lineage, not a real image-to-image continuity check.

6. **The 4.5-second contact check did not prove contact.** KF3 only tested for a bright region. It did not require a near-zero measured air gap, a bright interface at P, and the planted-head state together. A glow somewhere in the ROI could satisfy the glow condition without proving the intended first-contact geometry.

7. **Continuity gates were too low-resolution to prove semantics.** The main cross-frame metric compresses one broad ROI to 16×16 grayscale pixels and checks NCC/luminance. Static-background stability checks average luminance in only two corner patches. These checks can detect some cuts, but cannot establish same face, same tool topology, correct hand-to-existing-handle contact, correct contact plane, or shell-only failure.

8. **CI was not testing the checked-in contract.** The workflow tried to run `bubble_break/test_stage_d_gates.py`, which is not present in this branch. Its synthetic test assertion also expected `all_stages_passed=true`, contradicting the test and pipeline contract that synthetic evidence must never be production PASS. The workflow asserted a stale `selection_mode` field that the actual candidate manifest does not emit.

## Changes on this repair branch

- Enforce evidence-mode invariants when a report is instantiated; real-raster success cannot also claim a synthetic test passed.
- Add a mandatory measurable action-delta gate for D1/D2/D3, E_MID/E_END and the changing keyframes, so an unchanged D2 cannot be promoted as a successful grip transition.
- Make initial generation use compiled task prompts and attach the state-specific edit mask where available.
- Compile distinct prompt contracts for 0s far-windup, 2s near-approach, 4.5s first contact, 7s mid-shock, and 10s shell-only final blast.
- Parent KF1 to the actual D2 raster and run normal parent continuity/provenance checks.
- Require KF3's measured gap to be near zero and its contact interface to be bright; keep shell/drum criteria.
- Add a no-op regression test and align the workflow's synthetic-evidence assertions and test paths with files actually in the repository.
- Add `bubble_break/dual_t_hammer_collision.py`: explicit HAMMER_A/HAMMER_B rigid-body contract, opposing strike-face normals, normalized gap windows, point-P-on-both-face-disks geometry, forbidden cheek/shaft/handle contacts, and 12 distinct single-frame camera views per phase.
- The legacy single-hammer-on-bubble audit can no longer report production PASSED merely because its old pixel gates pass; without dual-hammer geometry evidence it reports BLOCKED / NOT_VERIFIED.

## Corrected task definition

The old pipeline is the wrong physical task for a T-hammer-vs-T-hammer collision. It locks one planted cylindrical hammer onto a bubble. For the intended two-tool interaction, a valid FIRST_CONTACT frame must establish **both separate T tools**, each with its own head and handle; opposing strike-face normals; positive gap in PRE_FAR/PRE_NEAR; zero gap at FIRST_CONTACT; lateral face alignment; and a point P inside both strike-face disks. A high NCC score or a glow cannot substitute for these geometric conditions. The new module compiles prompts and validates structured geometry evidence, but it does not itself supply the missing image-provider or semantic vision service.

## Limits that remain

These changes harden the pipeline's ability to reject measurable false passes. They do **not** make ordinary pixel statistics understand human identity or causal story semantics. Face/character similarity, correct contact plane/normal, whether hands truly grip the pre-existing rod (rather than a visually similar new rod), radial crack origin, and sanctuary survival still need a semantic vision judge with a calibrated rubric and/or explicit geometry/segmentation evidence plus human review. Until those checks are implemented and tested on real rasters, label visual acceptance `NOT_VERIFIED`; do not equate CI green or high NCC with a correct image.

The repository's abstract/CLI backend interface is not itself a provider integration. The exact external backend that produced the checked-in manifest is not instantiated by the committed CLI (`--cli-generator-cmd` is the only live CLI adapter). Do not describe the run as reproducibly regenerated by this repository unless the exact backend adapter, request/response receipts, parent image, mask and output hashes are attached.
