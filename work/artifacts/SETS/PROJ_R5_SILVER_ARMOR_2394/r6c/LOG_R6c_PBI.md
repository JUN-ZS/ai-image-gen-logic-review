# R6c／R7 · residual 改 PBI 默認 · 重跑 P0／P1

## 改了什麼
`run_r6c_ncnn.py` · `run_r7_peep2_final.py`

| 舊（毒） | 新（PBI 默認） |
|----------|----------------|
| `r = sr - lp` 全 RGB | `dY = Y(sr)-Y(lp)` |
| multi_sigma 三通道 | multi_sigma **只 Y** |
| `hyb = LP + residual_rgb` | `hyb = C(LP)×(Y_LP + ridge(dY))` |
| PIXEL 可能 BGR2RGB 雙換 | 先 BGR→RGB + `PIXEL_RGB` |

`PBI_MODE = "luma_only"`（可改 `legacy_rgb` 回毒路徑）

## P0／P1 結果
| 板 | align | sn | ten | PASS |
|----|-------|----|----|------|
| P0 PBI | 0.977 | 0.975 | 15480 | **是** |
| P1 PBI | 0.981 | 0.983 | 13314 | **是** |

## 藍噪 vs 舊 full-RGB（同 peep 量度）
| | blue residual vs LP | chromΔ | 相對舊改善 |
|--|---------------------|--------|-----------|
| OLD GENERAL（=R10 poison） | 3.05 | 0.068 | — |
| **PBI luma** | **0.32** | **0.010** | **−89.5% blue residual** |

## R7 PEEP2
- 父板：P0 PBI
- child 4096 · 14.5MB · sn **0.993** · ten 4381（LP 1908）
- align 0.544 → 結構閘 PASS，**align 閘 FAIL**（Y residual 的 align 定義與 RGB 幅值閘不同 · 需另校）
- status **PARTIAL**

## 誠實
- 非 live SIAX 權重
- metal mask 仍啟發式 peep 窗（非 SAM2 人審）
- 不 merge main
- 舊 GENERAL 檔保留作毒對照；新檔名 `*_PBI_*`
