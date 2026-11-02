# feat/r6c-ncnn-pbi-luma · S1/S2 protect

## THIS_RUN after G8 attrib `07e52d7`
- **S1** cell negative residual cap
- **S2** wire protect (max drop 4)
- block new black: y_lp≥18 → y_out≥18.5
- G7/G8 gates **unchanged**

## Result
- R6c status: **ACCEPT** (n_accept=2)
- G8 black: P0 35k→492 · P1 64k→945 · wire_hit 0
- Tenengrad lower (detail tradeoff) · struct still PASS
- merge main: **NO** (no human silver mask · not full clean-checkout chain · R7 not re-FORMAL yet)

---
## Full-frame（非 peep）

全圖請用 **NFP-M §0.12.59**：`run_ncnn_fullframe_pbi.py` · **RAW 先落盤再 strip PBI**。  
見 `docs/boundary_pedestrian/constitution/NCNN_FULLFRAME_PBI_MEMSAFE_01259.md`（branch `docs/ncnn-fullframe-memsafe-nfp-m-20261102`）。
