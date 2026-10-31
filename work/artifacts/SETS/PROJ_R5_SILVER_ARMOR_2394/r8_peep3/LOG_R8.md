# R8 · ② PEEP3 512→2048 FULL-RES

## 鏈
R7b 4096 → 高能窗 `(2276,28)` 512 → NCNN GENERAL 4× residual → **2048 主交付**

## 閘 · ACCEPT
| 項 | 值 |
|----|-----|
| align | **0.977** ✅ ≥0.65 |
| sn | **0.998** ✅ ≥0.97 |
| ten | 3618 → **7529** |
| probes | 48 · cov 0.632 · infer 1.74s |
| child | 2048 PNG · 3.00 MB |
| engine | NCNN_GENERAL_x4v3_PIXEL_RGB |
| ridge | thr_k=0.20 dil5 cellkill0.90 |

## 鐵律
- 2048 為 PEEP3 primary · 禁縮回 512
- 註冊 relative_to PEEP2_4096 · scale=4
- 嵌套：P0_2048 → PEEP2_1024→4096 → PEEP3_512→2048
