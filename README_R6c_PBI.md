# feat/r6c-ncnn-pbi-luma · PBI + G7/G8

## Two layers (do not mix)
1. **cc9c113** frozen first PBI push (structure gates only)
2. **THIS_RUN** (post-f9d45e2): regenerated P0/P1/PEEP2 with G7/G8 + fail-closed R7

## THIS_RUN honest gates
- P0/P1 **struct PASS** · **G7 blue PASS** · **G8 black FAIL** → overall PARTIAL
- R7 PARTIAL align≈0.57 < 0.65 · fail_closed_no_general_fallback=true
- merge main: **NO**

## Run (needs /workspace models)
```
python3 work/scripts/r6c_pbi/run_r6c_ncnn.py
python3 work/scripts/r6c_pbi/run_r7_peep2_final.py
```
PBI_MODE is in-code (`luma_only`), not a CLI flag.
