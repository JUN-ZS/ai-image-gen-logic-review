# feat/r6c-ncnn-pbi-luma · independent branch

**NOT merge-to-main.** Local sandbox PBI rerun pushed for remote image acceptance.

## Provenance
- Source: sandbox `/workspace/artifacts/SETS/PROJ_R5_SILVER_ARMOR_2394`
- Formula: `hyb = C(LP)×(Y_LP + ridge(multi_sigma_Y(dY)))`
- NCNN residual was poison; engine MAE≈0 vs PT
- SIAX live not included; UP-engine PR#6 has generation-side guard only

## Contents
```
work/artifacts/SETS/PROJ_R5_SILVER_ARMOR_2394/
  r6c/complete/P0_CHILD_2048_NCNN_PBI_R6c.png
  r6c/complete/P1_CHILD_2048_NCNN_PBI_R6c.png
  r6c/complete/ACCEPT_R6c_PBI.json
  r6c/complete/MANIFEST_SHA256_R6c_PBI.json
  r6c/LOG_R6c_PBI.md
  r7_peep2/complete/PEEP2_CHILD_4096_NCNN_PBI_R7.png
work/scripts/r6c_pbi/run_r6c_ncnn.py
work/scripts/r6c_pbi/run_r7_peep2_final.py
```

## SHA256
See `work/artifacts/.../r6c/complete/MANIFEST_SHA256_R6c_PBI.json`

## Gates
- P0/P1: ACCEPT structure (align/sn)
- Blue residual vs old GENERAL: −89.5% (same peep metric)
- R7: PARTIAL (sn 0.993, align 0.544 < 0.65 Y-ridge scale)


## Audit fix (follow-up, keep branch)

- ACCEPT scripts → `work/scripts/r6c_pbi/*`
- Runners write `*_PBI` ACCEPT/LOG names
- SHA256: `SHA256SUMS_PBI.txt` sidecar; MANIFEST **no self-hash**
- R7 still PARTIAL · merge main **NO** · clean-checkout full rerun **not claimed**
