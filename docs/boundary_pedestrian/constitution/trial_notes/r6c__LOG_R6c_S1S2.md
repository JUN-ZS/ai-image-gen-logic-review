# R6c S1/S2 protect · THIS_RUN

## 修
- S1: cell/other 負 residual 硬帽 (cell≤10 · other≤14)
- S2: wire 幾乎不壓暗 (drop≤4) + dilate wire mask
- 禁止 NEW black: y_lp≥18 → y_out≥18.5
- 撤銷弱 floor y_lp-36

## 結果（同 G7/G8 閘 · 未放寬）
- status: **ACCEPT** n_accept=2
- merge_main: NO · 非 clean-checkout 一鍵 · 銀網仍非人工 mask

## peeps
- P0: PASS=True align=0.977 sn=0.990 G7_px=1545 G8_px=492 wire_hit=0
- P1: PASS=True align=0.981 sn=0.991 G7_px=2695 G8_px=945 wire_hit=0
