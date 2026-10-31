# R10_1_ATOMIC_CLOSED_LOOP

- status: **PARTIAL** formal 6/10 ok · skip 2
- runner sha256: `80bcb8f76273c7f9322f82dc64f2d777da593a9fbce2ceae49d49f5a19a2cad7`
- accept sha256: `d5cca3e7e3cae3bd708b3473f8a09a298d0b7842a1181fd76a0b3a5e596c0bcd`
- jobs: 12 == JOB_PLAN (locked)
- dual ROI: FIXED_MESH + AUTO_WORST
- merge main: **NO**
- elapsed: 28.43s

## Nested head-to-head (same FIXED_MESH ROI)
- Lab champion: **N2_REBASE**
- Blue champion: **N1_DIRECT**

## Champions (mesh Lab)
- P0: A_luma lab↑61.62% FORMAL=True
- P1: A_luma lab↑72.65% FORMAL=True
- PEEP2_R7b: A_luma lab↑47.45% FORMAL=False
- PEEP3: N2_REBASE lab↑87.76% FORMAL=False
- PEEP3_origLP: A_luma lab↑64.74% FORMAL=False

## Champions (mesh Blue)
- P0: A_luma blue↑90.45% FORMAL=True
- P1: A_luma blue↑94.15% FORMAL=True
- PEEP2_R7b: A_luma blue↑85.1% FORMAL=False
- PEEP3: N1_DIRECT blue↑44.31% FORMAL=False
- PEEP3_origLP: A_luma blue↑5.93% FORMAL=False

## Skips
- PEEP2_R7b/B_material: full 4096 B/C float32 peak exceeds 1.9GB host; not ROI-paste substitute
- PEEP2_R7b/C_adaptive: full 4096 B/C float32 peak exceeds 1.9GB host; not ROI-paste substitute
