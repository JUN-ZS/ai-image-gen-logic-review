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

At `TARGET_CAPTURED`: `target_solo`, `target_pose_map`, `target_silhouette`, `design_spec`.

At `TARGET_SPEC_LOCKED`: add `target_landmarks` and `size_contract` with planned scene scale, target silhouette bbox, required native W+H, AR and tolerances.

At `DONOR_READY`: generate against that locked contract; add `donor_rgba`, `donor_mask`, `genfit_report` with generation-output SHA.

At `ANCHORED`: add `donor_landmarks` and `anchor_audit` linking both source SHAs.

At `FIT_DONE`: add `fit_report` with frozen method_id, paired per-anchor residuals and plan-vs-fit scale consistency.

At `POSE_GATE_DONE`: add `pose_report` whose primary reference role is `ORIGINAL_TARGET` and whose reference SHA equals `target_solo`.

At `READY_TO_PASTE`: add `paste_plan`.

At `FINALIZED`: add `paste_report` and `pixel_audit`. Verify actual pixels using:

```bash
python skills/shengqing-huiwei/tools/verify_native_hardpaste.py \
  --donor runs/<RUN_ID>/UNIT_U0/DONOR_RGBA.png \
  --master runs/<RUN_ID>/VIRTUAL_MASTER.png \
  --xy <INTEGER_X> <INTEGER_Y> \
  --out runs/<RUN_ID>/UNIT_U0/PIXEL_AUDIT.json
```

For an overlapped multi-unit donor, also provide a donor-sized `--visible-mask` showing the pixels owned by that unit in the final z-order. The guard checks pixel-audit donor SHA, paste coordinates and final VM SHA against `paste_report`.

For MULTI, all required units must pass before the final common-scene composition is accepted. Any failed unit blocks the whole multi acceptance.
