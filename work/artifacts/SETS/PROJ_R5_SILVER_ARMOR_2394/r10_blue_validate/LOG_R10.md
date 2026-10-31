# R10 · BLUE DETOX INDEPENDENT VALIDATION

## 審計回應
- 不再「改 JSON 稱 PASS」：單一 `run_r10_blue_validate.py` 同跑產 PNG+JSON+ROI+SHA
- Nested **N1_DIRECT** 與 **N2_REBASE** 分開定義與閘
- Formal 指標：**ROI Lab a,b** + **luma-norm blue opponent** · HSV dark 僅 legacy
- PEEP2 B/C：`scope=ROI_paste`（全幅 4096 OOM → 記錄限制）
- ten/sn 量度 scope：**ROI_only**（全幅 4096 OOM）
- merge main：**NO**

## 結果
**PARTIAL** · formal **11/14**

| Champion | method | FORMAL | ROI Lab ab ↑ | blue_opp ↑ | ten keep |
|----------|--------|--------|--------------|------------|----------|
| P0 | A_luma | ✅ | 61.45% | 89.82% | 99.54% |
| P1 | A_luma | ✅ | 51.20% | 90.26% | 99.57% |
| PEEP2_R7b | A_luma | ✅ | 50.12% | 85.81% | 98.82% |
| PEEP3 Nested | **N2_REBASE** | ✅ | 86.24% | 68.84% | 97.92% |
| PEEP3_origLP | A_luma | ❌ | 67.06% | **31.25%** (閘失敗) | 98.96% |

Material-aware / adaptive 未勝出 A_luma（ROI ab 略差或相近）。

## 閉環路徑
```
r10_blue_validate/
  run_r10_blue_validate.py
  inputs/   # staged poison+LP
  complete/ ACCEPT_R10.json · MANIFEST · ROI_REPORT · PNGs
  roi/      *_ROI.jpg
```
