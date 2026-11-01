# feat/r6c-ncnn-pbi-luma · G8-A/B/C + R7 parent lock

## Honest
- G7 BLUE PASS
- G8 BLACK: G8-A full + G8-B silver_proxy + G8-C 6 ROIs → **FAIL**
- R7: `DIAGNOSTIC_ONLY` when P0 formal PASS false (G8)
- production_ok: false · merge main: **NO**

## G8 design (not threshold gaming)
- G8-A: near-black **and** min_drop≥6
- G8-B: heuristic silver/mesh proxy scope (not human mask)
- G8-C: 6 fixed mesh ROIs
- G8-D: blotch + wire_hit

## Scripts
- `work/scripts/r6c_pbi/run_r6c_ncnn.py`
- `work/scripts/r6c_pbi/run_r7_peep2_final.py` (parent ACCEPT/SHA/G8 lock)
- `work/scripts/r6c_pbi/finalize_pbi_bundle.py` (unified SHA)
