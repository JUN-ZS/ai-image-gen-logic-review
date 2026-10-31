# R10 BLUE DETOX INDEPENDENT VALIDATION

## 審計要求對應
| 要求 | 本跑 |
|------|------|
| 單一 runner 同產 PNG+JSON+ROI+SHA | ✅ `run_r10_blue_validate.py` |
| 固定 inputs/ | ✅ staged + release 小 L0 |
| ROI Lab a,b formal（非 HSV） | ✅ |
| Nested N1 vs N2 分開 | ✅ |
| A/B/C 同源 | ✅ P0/P1 full；PEEP2 **僅 A_luma full**（B/C 全幅 4096 OOM · 本 minimal runner 不做） |
| merge main | **NO** |

## 結果
**PARTIAL** · formal **9/10** · elapsed 24.86s

### Champions
- **P0**: A_luma FORMAL=True ab↑61.45% blue↑89.82%
- **P1**: A_luma FORMAL=True ab↑51.2% blue↑90.26%
- **PEEP2_R7b**: A_luma FORMAL=True ab↑50.12% blue↑85.81%
- **PEEP3**: N2_REBASE FORMAL=True ab↑86.24% blue↑68.84%
- **PEEP3_origLP**: A_luma FORMAL=False ab↑67.06% blue↑31.25%

### FORMAL fails
- PEEP3_origLP/A_luma: ab↑67.06% blue↑31.25% (PASS_blue=False)

### 誠實限制
- 1.9GB RAM · PEEP2 全幅 B/C 會 OOM → minimal runner **只跑 A_luma full**
- ten/sn 用 ROI（大圖）
- poison 大圖（2048/4096）未入 git tree · 需本機 inputs/ 或 R9 release 同源
- **不 merge main**

### 閉環路徑
```
r10_blue_validate/  + r10_STAGED/ (immutable copy)
  run_r10_blue_validate.py
  inputs/
  complete/ ACCEPT · MANIFEST · ROI_REPORT · PNGs
  roi/
```
