# SIAX 探針匹配 SPM · 正確流程 · §0.12.37

> asof 2026-10-29T11:00:05Z · HKT 2026-10-29T19:00:00+08:00  
> 正名：**SIAX 探針匹配** · 短碼 **SPM**  
> 實跑母：衣 A `07b1a8f4…` · 對照全幅 `CLOTH_A_HYBRID_*`  
> 連動：N2R · S1HL · GOU · MSR · ZYF

---

## 0. 一句

```
SIAX 只當探針（真 HF 指紋）
→ 模底 = Lanczos(L0)（幾何鎖）
→ residual 場填 + M
→ 可選 GOU/GEN 互構貼
→ 失敗 ROI 才補真 SIAX／全幅 S1HL
```

**SIAX（NMKD-Siax）= ESRGAN 一次前向 · 無擴散 STEP／NOISE／GUIDANCE。**

---

## 1. 與既有技對位

| 技 | 角色 | SPM 怎麼掛 |
|----|------|------------|
| **MSR** | 大圖場先立 → 收細 | L0 場定探針格；SPM 為 L3–L4 的 **省算力 SIAX 預設** |
| **N2R** | 噪 cand → 折射／保留，非純滅 | 探針 residual 高能邊 = **n2r 指紋**；填場 ≠ median 殺光 |
| **S1HL Hybrid** | LP 模底 + HF×M · 一升混 | 全幅貴 → 預設改 **SPM-A 探針 HF**；定版仍可 P0 全幅 |
| **GOU** | 近距真紋理 donor | 探針外空白／閘 fail → **GOU crop GEN 貼**，不硬全幅 SIAX |
| **ZYF** | 正衣先行 | 衣板無臉：SPM-A 默認一升預覽 |

---

## 2. 方案表（探針幾何）

| 碼 | 名 | N × 塊 | 殘 | 填 σ | 時間量級（衣A CPU） | 用途 |
|----|-----|--------|-----|------|---------------------|------|
| **SPM-A ★預設** | MANY_ROUGH | **48 × 64²** | 糙 | 短 4–16 | ~40 s | **一升預設／指紋／預覽** |
| SPM-12 | 中道 | 12 × 96² | 中 | 8–64 | ~44 s | 均衡 |
| SPM-B | FEW_SMOOTH | 8 × 160² | 滑 | 16–96 | ~99 s | 較貼全幅、仍省 |
| S1HL-P0 | 全幅 4× strip | 全圖 | Hybrid | — | 10–15 min | **定版** |

### ★ 預設 SIAX 設定 = **SPM-A**

```text
TILE_N      = 48
TILE_WH     = 64 × 64
GRID        = 8 × 6（邊優先窗）
SIAX_MODEL  = 4x_NMKD-Siax_200k
SCALE_OUT   = HD 2×（residual 在 2× 上對 LP）
residual_gain   = 1.15
rough_boost     = 0.85
fill_sigmas     = [4, 8, 16]
M_lo, M_hi      = 0.45, 1.0
```

**凡寫「一升／預設 SIAX」而未經口令改 PATH → 走 SPM-A，禁止默認全幅 4×。**

---

## 3. 等價旋鈕表（入憲 · 非擴散原生）

> 用戶常問 STEP／NOISE／GUIDANCE —— **Siax 無**；下表為 **SPM 管線等價**。  
> 實跑：TILE 固定 48×64 · SIAX **一次** · 只改後處理（`CLOTH_A_KNOB_*`）。

| 口語名 | 等價參數 | 高 | 低（反比） | 實測（vs Hybrid） |
|--------|----------|----|------------|-------------------|
| **GUIDANCE** | `residual_gain` + `M_lo/M_hi` | 1.45 · M 0.55–1.0 → 過銳、mae↑ | 0.55 · M 0.25–0.55 → **較貼** | GUIDE_lo 勝 |
| **NOISE** | `rough_boost` + `noise_amp` | 1.1 + 0.35 → 花 | 0.08 + 0 → 淨 | NOISE_lo 較穩 |
| **STEP** | `fill_sigmas` 串 | 多短步 [3…24] → 島黏 | 少長步 [48,96] → 場攤滑 | STEP_few 略勝 |

### 預設旋鈕（掛 SPM-A）

| 旋鈕 | 預設 | 備註 |
|------|------|------|
| residual_gain | **1.15** | A 案；定版可降到 1.0 |
| rough_boost | **0.85** | A 殘粗糙 |
| noise_amp | **0** | 預覽指紋可不加；實驗用 |
| fill_sigmas | **[4,8,16]** | A 短距保粒 |
| M | **0.45–1.0** 邊權 | 邊↑ 信 residual |

### 禁

| ID | 禁 | 因 |
|----|-----|-----|
| E-SPM-01 | 稱 SIAX 有 diffusion STEP/CFG | 誤導 |
| E-SPM-02 | 截 SIAX 中間 layer 當半圖 | 不可用 |
| E-SPM-03 | 默認全幅 4× 當「一升預覽」 | 違省算力；改 SPM-A |
| E-SPM-04 | residual 填場當 N2R 殺光 | 違 N2R 折射／保留 |
| E-SPM-05 | SPM VIEW 當 REF_PLATE 病毒母 | §0.12.23 |

---

## 4. 正確流程 T0–T6

| 步 | 做 |
|----|-----|
| T0 | BASE/L0 原生；ZYF 衣板可無臉 |
| T1 | MSR 場／edge 選 **48×64** 探針（SPM-A） |
| T2 | 真 SIAX 4× 僅探針 → residual vs Lanczos |
| T3 | 等價旋鈕（上表）建 residual 場 |
| T4 | out = LP + residual×M |
| T5 | 可選：N2R 區折射保留；GOU 近距貼 fail |
| T6 | 閘 ncc／目視；定版 → S1HL-P0 或 ROI 補 |

---

## 5. 實跑備註（衣A 2026-10-29）

| 實驗 | 結論 |
|------|------|
| SPM-A vs B | A 快 2.5×；B 數字略近 Hybrid |
| 旋鈕反比 | GUIDE_hi 最糟；GUIDE_lo / STEP_few 較親 Hybrid |
| 時間 | 探針 ~40s vs 全幅 ~10–15 min |

---

## 6. 口令

```text
「SPM」／「探針一升」     → SPM-A 48×64
「中道 SPM12」           → 12×96
「SPM-B」               → 8×160 滑
「一升」未指定           → 預設 SPM-A（非全幅）
「定版一升／S1HL 全幅」  → P0 strip
「等價 GUIDE/NOISE/STEP」→ 改旋鈕表，不改 TILE
```

*END §0.12.37 SPM · 2026-10-29T11:00:05Z*
