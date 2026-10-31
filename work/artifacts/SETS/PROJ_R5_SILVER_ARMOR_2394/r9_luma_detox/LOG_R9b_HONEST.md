# R9b · 審核回應 · 撤銷全鏈 ACCEPT

## 審計同意
1. 原 R9 `n_pass=5/6` · Nested 無完整閘 → **不可作最終 primary 驗收**
2. PEEP2 dark-blue 微升 · 僅靠 +1pp soft gate PASS · **不算正式減少藍斑**
3. 公式 \(Y_{LP}+(Y_{SR}-Y_{LP})=Y_{SR}\) → 實為 **鎖 LP 色度 + 保留 SR 亮度** · 非獨立 residual 增益
4. Primary PNG 未入 GitHub → 本機 `child_bytes` ≠ 可下載交付
5. 「全鏈 60–80%」誇大 · P1 僅 **−52.1%**

## 公式澄清
```
Y_out = Y_SR
RGB_out = chromaticity(LP) × Y_SR
```
- 做：砍 SR 新增色度污染
- 不做：清 LP 本身青藍環境光；保彩色 HF 反光

## 閘（誠實）
| 閘 | 定義 |
|----|------|
| **PASS_FORMAL** | chroma B ≥50%↓ 或 absB<0.5 · **dark 不升** · ten≥92% · sn≥0.95 |
| **PASS_EXPERIMENTAL** | 同上但 dark **+1pp 容**（soft） |

## R9b 結果
| 子板 | FORMAL | EXP | B chroma | dark Δ | ten keep |
|------|--------|-----|----------|--------|----------|
| P0 | ✅ | ✅ | −64.5% | −3.98pp | 99.64% |
| P1 | ✅ | ✅ | −52.1% | −2.79pp | 99.57% |
| PEEP2 R7 | ❌ | ✅ | −62.6% | **+0.20pp** | 99.35% |
| PEEP2 R7b | ❌ | ✅ | −64.1% | **+0.07pp** | 99.10% |
| PEEP3 R8 | ✅ | ✅ | −80.4% | −0.31pp | 99.45% |
| **PEEP3 Nested** | ✅ | ✅ | −80.7% | −0.72pp | 98.63% · **已補全閘** |

**status: `EXPERIMENTAL_P0_P1`** · 撤銷全鏈 FORMAL ACCEPT · 不 merge main

## 下一輪
A 全域 luma-only（現有）· B material-aware chroma gate（P0 trial 已產）· C adaptive chroma residual  
固定 ROI + 亮度正規化色度 · 查 PEEP2 為何 dark 微升

## 可重現
- `tmp/run_r9_luma_detox.py`（初跑）
- R9b patch 內嵌於 artifacts 腳本 / ACCEPT_R9b_HONEST.json
- `MANIFEST_SHA256.json` 本機 primary 指紋
