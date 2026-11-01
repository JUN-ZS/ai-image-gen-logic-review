# 噪折成光 N2R 正確流程 · §0.12.26.O

asof: 2026-10-27T21:20:07Z

## 定位
§0.12.26 白分層（噪殺／反光留）之 **轉化支**：高能邊框白噪 → 微面折射，**不**當純 median 消滅。

## T0 母底
- 全幅 native only（§0.12.23）
- 優先「最多噪」同構圖板（META mother 級）作 cand 源

## T1 反推 cand
```
residual = |I − median/bilateral|
NOISE_WHITE_cand = residual高 ∧ 亮 ∧ 低結構 ∧ edge_fringe
SPEC_map = peak × light × edge − noise_snow
kill_pure = cand ∩ ¬spec          # 可殺
n2r_zone = cand ∩ (近光 ∨ 高 energy) ∧ 邊框線  # 轉
```
輸出：`NOISE_CANDIDATE_OVERLAY` + `MAPS`


<!-- SPM_DEFAULT_SIAX §0.12.39 -->
## 與 SPM 預設 SIAX（§0.12.39）

- 探針 residual 高能邊 = **N2R cand 指紋源**（折射／保留，**非**純滅）
- 預設探針幾何：**SPM-A 48×64²**
- 填場互構 ≠ median 殺光（E-SPM-04）
- 等價 NOISE 旋鈕（rough_boost）調的是 residual 糙度，不是擴散 noise schedule
<!-- END_SPM_DEFAULT -->


## T2 轉化（非消滅）
| 區 | 處置 |
|----|------|
| n2r_zone | energy → 暖 microfacet glint／折射高光（非 #FFF 雪） |
| kill_pure | median／bilateral（¬spec） |
| SPEC_true | **不動** |
| 可選 | 最多噪圖 GEN 正反推微面，再 fuse 回 cand 區 |

## T3 fuse + 鎖
- cand 區 **fuse 非刪**
- HF／拓樸鎖母（人／甲／武器 identity）
- banded 大圖防 OOM
- 禁整圖 GEN 重寫當「去噪」

## T4 PROOF
| 閘 | 要求 |
|----|------|
| 外框白噪線 | 視覺↓；殘 cand 為暖 glint 非雪絲 |
| SPEC 近火／甲棱 | 仍在（E-SF-04 禁殺光） |
| mean\|Δ\| 全局 | 小（只動 cand） |
| OVERLAY/MAPS | 可稽 |
| L- | 寫 META |

## 停
外框線消、真反光在、身份未漂 → 停。不為「再白淨一點」開 E-SF-04。

## 樣板
L-06f22d5402af · technique=`NOISE→REFRACT (轉化 not 消滅)`

---

## 預設 SIAX 指紋 · SPM-A（2026-10-29T19:00:00+08:00）

> 掛：§0.12.37 SPM

N2R 要 **噪 cand 指紋** 時：

| 原 | 現預設 |
|----|--------|
| 易觸發全幅重升 | **SPM-A 48×64 residual** 作 cand／HF 真值 |
| 純 median 滅 | **禁**；探針高能邊 → 折射／保留（n2r_zone） |
| 填場 | residual 場 = **保留向**，非殺光 |

`rough_boost` 高 → 接近 NOISE 等價；殺光仍只走 kill_pure ∩ ¬spec。
