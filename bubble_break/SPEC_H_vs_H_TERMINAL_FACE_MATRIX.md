# ((H) vs (H)) T-to-T Terminal Face Matrix — Acceptance Note

## Contract
- Active surface: rectangular **terminal end face** of crossbar only.
- Rigid body: `u_crossbar · v_shaft = 0` (90° lock).
- Stage A: two T hammers, `n1 · n2 = -1` at P.
- Stage B: replace target T with bubble; same P, opposite shell normal.
- H0 +50px / H2 0px / H3 +15px along impact normal.
- C=(1090,330), R=280; AXIS_01 P=(1090,610), n_attacker=(0,-1).

## Camera matrix
12 cams × 4 axes = 48 variants (see contact_matrix_48_variants.json).

## Gate
| Layer | Status |
| --- | --- |
| Unit geometry + prompts | PASS (local) |
| SVG proxies | PASS (8 axis H0/H2) |
| image_realization | **NOT_RUN** |
| pixel_audit | **NOT_RUN** |

PROMPT_PASS / SVG_PASS ≠ image PASS. Do not unlock story scenes until H2 PNGs pass manual review.

## Relation to t_contact_matrix.py
`bubble_break_contact_matrix.py` is the **rigid-math + Stage A/B + 12 cinematic cam** spec implementation.
Existing `t_contact_matrix.py` remains industrial 12×4 Latin handle-roll matrix; do not merge claims.
