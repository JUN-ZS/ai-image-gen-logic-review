# Bubble-Break External Image-Provider Adapter Contract

## Why the runner uses an explicit adapter

The imported Gemini record contains a unified manifest and image rasters, but the repository import notes say the prior `runner.py` / `dual_t_hammer_runner.py` export was missing. The manifest's claimed execution cannot be reproduced from that record alone. This runner therefore exposes an explicit command boundary instead of pretending a model API is already connected.

Entry point:

```cmd
python -m bubble_break.runner --candidate-manifest path/to/candidates.json --outdir out/calibrated_bubble_break_closed_loop --provider-command "python path/to/my_provider_adapter.py"
```

The provider command is optional only when all candidate stages are present. If a stage is missing or rejected and no command is provided, the pipeline blocks rather than fabricating an image.

## Environment variables

The runner writes a JSON request, then invokes the configured command without `shell=True`. It supplies:
- `BUBBLE_BREAK_REQUEST_JSON`: absolute path to the request file.
- `BUBBLE_BREAK_RESPONSE_JSON`: absolute path where the adapter must write its response JSON.

The request includes domain/stage, retry index, parent raster path and SHA-256 (when available), prior rejection errors, stage-specific prompt instructions, and the Shannon-inspired diagnostic experiment ranked by expected information gain per estimated cost. The experiment score is an engineering heuristic, not calibrated model accuracy.

## Required response

Write a JSON object at `BUBBLE_BREAK_RESPONSE_JSON`:

```json
{
  "candidates": [
    {
      "path": "/absolute/path/to/generated-candidate.png",
      "evidence": {
        "stage": "H2_FIRST_CONTACT",
        "raster_sha256": "SHA256_OF_THE_EXACT_FILE_BYTES",
        "parent_raster_sha256": "SHA256_OF_THE_EXACT_PARENT_FILE_BYTES",
        "parent_stage": "H1_PRE_NEAR",
        "calibrated_from_dual_hammer_sha256": "SHA256_OF_APPROVED_CALIBRATION_CONTACT_FRAME",
        "scene_lock_id": "one-stable-scene-id-for-the-sequence",
        "camera_lock_id": "one-stable-camera-id-for-the-sequence",
        "attacking_hammer_identity_id": "one-stable-tracked-hammer-id",
        "bubble_identity_id": "one-stable-tracked-bubble-id",
        "shell_integrity_state": "INITIATED",
        "crack_front_radius_ratio": 0.08,
        "preexisting_cracks": false
      }
    }
  ]
}
```

The schema above is illustrative; each stage must also supply the full geometry and semantic annotation fields required by `frame_pipeline.py` and `raster_bound_collision_audit.py`. Every evidence object must match its actual file bytes and intended stage. Reusing a parent image for a required state transition is rejected.

## Stage requirements

### Upstream dual-T calibration

Stages: `PRE_FAR`, `PRE_NEAR`, `FIRST_CONTACT`, `REACTION`, `RECOIL`. Each frame must identify two distinct tools and the intended end-face contact surface. Every child stage must bind to the actual parent SHA and preserve stable scene/camera/tool identity IDs.

### Bubble-Break

Stages: `H0_PRE_IMPACT`, `H1_PRE_NEAR`, `H2_FIRST_CONTACT`, `H2B_CRACK_PROPAGATION`, `H3_FOLLOWTHROUGH_SHELL_SHATTER`. Each frame binds to its actual immediate parent and the exact SHA of the approved upstream calibration FIRST_CONTACT image. Stable scene/camera/attacker/bubble IDs must not drift across the bubble sequence.

- H0/H1: shell `INTACT`, no pre-existing cracks, `crack_front_radius_ratio=0`, positive gap, no contact.
- H2: shell `INITIATED`, contact at P, no pre-existing cracks, normalized crack-front radius in `(0, 0.15]`.
- H2B: shell `PROPAGATING`, cracks present, crack-front radius strictly greater than H2.
- H3: shell `SHATTERED`, crack-front radius strictly greater than H2B, `shell_only_breach=true`, `inhabitants_unharmed=true`.

The state fields are annotations/evidence inputs, not facts inferred by the runner. A reviewer or semantic vision component must inspect the image and supply them honestly. The validator never labels them as visually verified by code.

## Exit and acceptance semantics

- Exit code 2: missing inputs, provider error, or blocked contract.
- Exit code 0: the structured evidence process completed without a BLOCKED status. This is **not** equivalent to visual acceptance.
- `code_visual_acceptance_status` remains `NOT_VERIFIED_BY_CODE`.
- Final report status, after contract checks pass, is `EVIDENCE_CONTRACTS_PASSED_REQUIRES_VISUAL_REVIEW`, with both visual-approval booleans false.

Do not connect an adapter that fabricates review annotations or marks outputs PASS without inspecting the exact returned raster. That would only move the original false-positive problem into a new process.
