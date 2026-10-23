# Cross Hammer · Into-Camera Bubble Barrage · L1–L5 Contract

**Branch:** `feat/layered-divine-hammer-wash-audit-20261023`  
**Module:** `bubble_break/cross_hammer_into_camera_bubble_contract.py`  
**Sister:** dual-warrior T-hammer `layered_divine_hammer_wash_audit.py` (does not replace it)

## Visual line (Imagine session anchors)

| Role | Asset id |
|------|----------|
| Cross still | `34eede64-2215-4412-a459-8a27a27daa9a` |
| Violent skill 10s video | `a2fa4cef-704c-4711-aebb-64ecb8754c04` |
| Face id | `6ee74baf-2c16-44e8-aa14-b771002c7ebd` |

Anchors are metadata only. Gates never claim pixel PASS from UUID alone.

## Hard scene rules

1. **十字槌** — four orthogonal arms at a boss; not plain double-ended cylinder.
2. **打不斷** — `stream_never_clears=True`; bubbles keep flying.
3. **飛入鏡頭** — high `into_camera_fraction`; explosions near lens.
4. **暴力招式** — skill_move_id from vocabulary; lever torque, not pure axial spear poke.

## Layers

| Layer | Gate id | Blocks |
|-------|---------|--------|
| L1 | `L1_CROSS_HAMMER_TOPOLOGY` | SHA, 4 arms, NS⊥EW, not cylinder |
| L2 | `L2_TRUE_STRIKE_ANTI_SPEAR_INTO_CAM` | face vs n_cam, SPEAR_HANDLE_INTO_LENS_TRAP |
| L3 | `L3_BARRAGE_AND_LEVER_TORQUE` | barrage unbroken, mirror clone, axial push |
| L4 | `L4_CROSS_PANEL_VARIANCE` | skill/camera/face exclusivity, layout NCC |
| L5 | cumulative re-audit | re-run L1..Lm on panels 1..k before advance |

`visual_acceptance_status` is always **`NOT_VERIFIED_BY_CODE`**.

## Run tests

```bash
PYTHONPATH=. python3 -m unittest bubble_break.test_cross_hammer_into_camera_bubble_contract -v
```

## Rollback

```bash
git revert <this-commit-sha>
```
