# R9 FULL-CHAIN · luma-only residual 解毒

> asof 2026-10-31 · E-BLUE-01..04 · 鐵律：4× residual **luma 主導** · 鎖 LP chroma

## 公式
```
Y_out = Y_LP + (Y_SR − Y_LP)
RGB_out = chromaticity(LP) × Y_out
```
禁：full BGR residual 直貼。

## 鏈
| 層 | 毒板 | 解毒 primary |
|----|------|----------------|
| P0 512→2048 | R6c GENERAL | `P0_CHILD_2048_LUMA_R9.png` |
| P1 512→2048 | R6c GENERAL | `P1_CHILD_2048_LUMA_R9.png` |
| PEEP2 1024→4096 | R7 / R7b ridge | `PEEP2_CHILD_4096_RIDGE_LUMA_R9.png` |
| PEEP3 512→2048 | R8 + nested | `PEEP3_CHILD_2048_LUMA_NESTED_R9.png` |

## 閘（R9b）
- chroma B abs ≤50% 或 <0.5
- dark_blue 不升 >1pp
- ten ≥92% 毒板
- sn ≥0.95

## 結果
**ACCEPT** · 全層 PASS（5/5 有閘 job）

| tag | dark poison→detox | Babs→ | ten→ |
|-----|-------------------|-------|------|
| P0 | 0.490→0.451 | 1.027→0.365 | 15698→15641 |
| P1 | 0.537→0.509 | 1.021→0.489 | 13955→13894 |
| PEEP2_R7 | 0.272→0.274 | 0.323→0.121 | 4429→4400 |
| PEEP2_R7b | 0.273→0.274 | 0.405→0.145 | 5160→5113 |
| PEEP3_R8 | 0.015→0.012 | 1.376→0.270 | 7529→7487 |
