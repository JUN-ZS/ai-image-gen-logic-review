# FULL MESH TEX · 非噪點修

## 用戶
試是全網紋都改，而不是點出噪位才改

## 對照
| 舊 S1S2 | 本輪 FULLMESH |
|---------|----------------|
| ~24 high-edge probes | stride 32 dense · 全 peep 覆蓋 |
| 主効=消黑斑 | 主効=整片網紋 HF 注入 |
| 紅 mask residual 思維 | mesh mask 全域 boost |

## 結果
- P0: ten_lp→ten 5515→22678 sn=0.979 n=225
- P1: ten_lp→ten 3659→16136 sn=0.983 n=225