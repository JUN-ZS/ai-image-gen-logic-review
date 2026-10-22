# V5.1 Bubble-Break False-PASS Root Cause Audit and Repair

## Scope

Audited `feat/v5.1-closed-loop-continuity` at the time of review, including `bubble_break/autonomous_pipeline.py`, `bubble_break/stage_d_gates.py`, the GitHub Actions workflow, the committed run manifest, and the rendered image `out/v5_1_run/keyframe_sample.jfif`.

This audit concerns the **Bubble-Break image sequence**: one correctly constructed T-topology / multi-face hammer strikes the containment bubble at the specified bottom contact point; the bubble then fractures outward while the inner sanctuary and its inhabitants remain safe. The T-hammer-to-T-hammer contact matrix is a separate upstream geometry-calibration stage from the larger Bubble-Break story output. It is not a replacement for the bubble scene.

A green manifest or CI workflow is not treated as visual proof.

## Confirmed code and manifest defects

1. **Contradictory evidence flags.** The stored manifest says `evidence_mode=REAL_GENERATIVE_RASTER`, `status=PASSED`, `all_stages_passed=true`, and `synthetic_test_passed=true` together. A real raster run cannot also claim that its synthetic test passed.

2. **D1 and D2 can be identical and still pass.** The stored manifest has identical SHA-256 values for D1 and D2. The action-stage gate did not require a meaningful change, so a no-op image could be accepted as an action transition.

3. **Initial-generation prompts were placeholders.** Backend calls passed strings such as `INITIAL_D1` and `INITIAL_KF2_2S_PRE_NEAR`, not fully compiled stage instructions. A real generation adapter receiving those values would not receive the required scene contract.

4. **Distinct bubble-story states were conflated during repair.** The 0s far-precontact, 2s near-precontact, and 4.5s first-contact keyframes could be repaired with the same generic D3 action prompt. E_MID and E_END likewise lacked distinct enough state-specific instructions.

5. **The first keyframe lacked a real parent raster.** The code copied the D2 SHA into the keyframe provenance field but set the actual parent image path to `None`. A matching hash string is not a substitute for raster-to-raster comparison.

6. **The first-contact check could be satisfied by glow.** A bright patch is not proof that the intended thick terminal striking face is the first part to touch the bubble at the exact six-o'clock point P. Correct contact requires the proper hammer topology, the face normal aimed at P, zero gap at H2, and no shaft/side-head collision.

7. **Continuity metrics cannot prove the required geometry or story semantics.** The branch reduces a broad ROI to 16×16 grayscale pixels for NCC and compares average luminance in two background corners. Those checks can detect some cuts or large changes; they cannot establish the exact striking face, the T-hammer head/handle joint, the contact surface at P, shell-only failure, or the continued safety of the inner sanctuary.

8. **CI did not match the checked-in contract.** The workflow called a missing `bubble_break/test_stage_d_gates.py`, expected a stale candidate-manifest field, and contained a synthetic-run assertion inconsistent with the intended honest evidence contract. These defects were corrected on the repair branch.

## Direct visual review of `out/v5_1_run/keyframe_sample.jfif`

The JFIF contains five panels labelled 0s, 2s, 4.5s, 7s, and 10s. Direct review of the pixels—not the green PASS borders—finds:

- **The intended T-topology is not clearly depicted.** The main object reads as a long cylindrical ram, with a large circular cap facing the viewer at lower-left and the long body approaching the bubble. The required transverse T-handle / rigid head topology and its actual striking end face are not legible enough to accept.
- **The active contact face appears wrong or unproven.** The cylinder seems to meet the bubble around its side wall. The 4.5s glow ring does not prove that the designated flat terminal striking face alone first contacts P at the bubble's six-o'clock pole. A glow cannot make an incorrect face correct.
- **0s → 2s does not communicate the required progression strongly enough.** The same large ram and bubble remain in nearly the same composition; even if a pixel gap has changed, the visual evidence for a deliberate rigid-body approach with the exact striking face aimed at P is weak.
- **The 7s frame is dominated by luminous rings.** It does not clearly demonstrate radial cracks propagating outward from the already established physical contact point P.
- **The 10s panel has a broken-shell spectacle and a bright miniature interior,** but that downstream image alone cannot prove the preceding first contact was physically correct or that the sanctuary stayed unchanged across the entire sequence.
- **Hand-to-handle force transfer is not clear enough to certify.** The image does not reliably show both hands gripping the pre-existing handle at its specified joint/orientation while keeping the shaft and non-striking head surfaces off the bubble.

Accordingly, this sample is **rejected for Bubble-Break visual acceptance** even though the manifest reports PASS. This is not rejection for failing to show two hammers in the final bubble scene; the bubble scene uses one attacking hammer. The two-T-hammer terminal-face matrix is an upstream geometry-calibration step whose result must not be confused with the final bubble-breaking frame.

## Repair-branch changes

- Enforce consistent evidence-mode invariants; a real-raster run cannot simultaneously claim synthetic-test acceptance.
- Reject unchanged/no-op action frames at action-required stages.
- Use compiled initial prompts and distinct stage contracts for far precontact, near precontact, first contact, mid-shock, and shell-only final break.
- Parent the first keyframe to the actual D2 raster and run parent-image checks.
- Keep missing or inadequate evidence blocked rather than promoting a raster on NCC, luminance, or a glow alone.
- Align CI test paths, manifest assertions, and artifact paths with files that actually exist.
- Preserve an explicit `visual_acceptance_status=NOT_VERIFIED` until the exact real raster has adequate Bubble-Break geometry evidence and visual review.

## Correct Bubble-Break physical contract

The scene has **one attacking hammer** and one containment bubble. The intended weapon is a rigid 3D T-topology / multi-face hammer with its prescribed terminal striking face and existing transverse handle. The canonical contact point is the sphere's six-o'clock pole P.

- **H0 / precontact:** bubble intact, no cracks, striking end face clearly separated from P; the face normal is aimed at P; shaft and side heads remain clear.
- **H1 / approach or mechanism reveal:** the same hammer, target bubble, camera, and scene identity remain locked; still no contact or premature cracks.
- **H2 / first contact:** only the designated thick terminal end face touches P; gap is zero; no cheek, shaft, handle, or side-head contact substitutes for it.
- **H3 / fracture and release:** cracks originate at P and propagate outward; the bubble shell is what breaks; inner sanctuary/residents remain safe and regain agency.

The separate T-vs-T contact matrix can be used to calibrate the end-face geometry and camera recognizability before replacing the target hammer with the bubble at the same P. It is not permission to generate a final frame showing two hammers colliding with one another instead of the bubble.

## Remaining limit

The repaired pixel-gate pipeline is not a semantic vision service. It must not claim that it can automatically identify the correct T-head, distinguish all end-face/cheek collisions, or certify shell-only failure unless those checks are backed by a calibrated image model/segmentation evidence or an explicit human review tied to the exact raster bytes. The external generator adapter, its request/response receipts, and actual accepted Bubble-Break rasters also need to be available for a reproducible generation claim.

Until that is connected and real images pass, the honest result is `BLOCKED` / `NOT_VERIFIED`, not PASS.
