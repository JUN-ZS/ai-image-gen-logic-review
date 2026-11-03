# SHQ v1.2 — Operator Quick Start

Run from the repository root.

## 1. Golden solver regression

```bash
python skills/shengqing-huiwei/tools/test_ddxx_golden_regression.py \
  --out runs/<RUN_ID>/DDXX_GOLDEN_REGRESSION_REPORT.json
```

This checks only the weighted Umeyama implementation against the recorded 11-point panel fixture. It does not approve a new image pair.

## 2. Pin canonical version hashes

```bash
python skills/shengqing-huiwei/tools/shq_preflight_guard.py --print-canonical-hashes
```

Copy the three hashes into `RUN_STATE.json`. This makes a stale local skill copy fail preflight.

## 3. Create state

Copy:
- `references/RUN_STATE_TEMPLATE_SINGLE.json` for one person/object.
- `references/RUN_STATE_TEMPLATE_MULTI6.json` for six independent units.

Change `run_id`, select one `method_id`, fill the actual hash fields, and keep the selected method frozen.

## 4. Run guard

```bash
python skills/shengqing-huiwei/tools/shq_preflight_guard.py runs/<RUN_ID>/RUN_STATE.json \
  --out runs/<RUN_ID>/PREFLIGHT_REPORT.json
```

Exit code 0 = gate pass for the declared phase. Exit code 2 = BLOCK. Never override with a text status.

## 5. Evidence paths per unit

At `TARGET_CAPTURED`: `target_solo`, `target_pose_map`, `target_silhouette`, `target_landmarks`, `design_spec`.

At `DONOR_READY`: add `donor_rgba`, `donor_mask`, `donor_landmarks`, `genfit_report`.

At `FIT_DONE`: add `fit_report` with frozen method_id, per-anchor residuals and semantic-anchor audit.

At `POSE_GATE_DONE`: add `pose_report` whose primary reference role is `ORIGINAL_TARGET` and whose reference SHA equals `target_solo`.

At `READY_TO_PASTE`: add `paste_plan`.

At `FINALIZED`: add `paste_report` proving donor SHA, hardpaste, unit_scale=1.0 and core integrity.

For MULTI, all required units must pass before the final common-scene composition is accepted. Any failed unit blocks the whole multi acceptance.
