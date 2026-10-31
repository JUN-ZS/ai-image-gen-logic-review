# R6c NCNN PBI Luma Bundle

Independent orphan branch deliverable (not merged to `main` / `work/boundary-walker-canvas`).

## Required set
- `P0_CHILD_2048_NCNN_PBI_R6c.png`
- `P1_CHILD_2048_NCNN_PBI_R6c.png`
- `ACCEPT_R6c_PBI.json`
- `LOG_R6c_PBI.md`
- `MANIFEST_SHA256_PBI.json` / `SHA256SUMS_PBI.txt`
- runners: `work/artifacts/tmp/run_r6c_ncnn.py`, `run_r7_peep2_final.py` (`PBI_MODE=luma_only`)
- optional: `PEEP2_CHILD_4096_NCNN_PBI_R7.png`

## Formula
`hyb = C(LP) × (Y_LP + ridge(multi_sigma_Y(dY)))` — no full RGB residual inject.

## Honest
- P0/P1 structure ACCEPT · blue residual vs old −89.5% (report)
- R7 PARTIAL (align 0.544)
- NO merge main · not live SIAX
