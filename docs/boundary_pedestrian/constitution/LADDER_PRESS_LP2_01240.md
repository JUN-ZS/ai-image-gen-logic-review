# 階梯放大壓回 · 正確流程（LADDER_PRESS v2 / LP2）

> asof 2026-10-29T16:40:37Z · 憲：§0.12.40 · 連動 §0.12.39 SPM · §0.12.25 GOU  
> **樣板：** crop `P1_CHEST` · v2 終 `SETS/GOU_B_LADDER_V2/FINAL_V2.jpg` · 3107×2332

---

## 過程總覽（用戶確認後入憲）

```
0  一次×4 Hybrid HF0.95     → 爆紋 FAIL（PART_AMP oneshot）
1  階梯 v1 HF_KEEP=0.35     → 過糊 FAIL（升清未達）
2  階梯 v2 HF_KEEP=0.62     → 密網可讀 · 邊密度回升 · LOCK 默認
3  （下）v2 + GOU 密網 donor → 有序蜂窩再階梯
```

## 鐵序（不可顛倒）

```
cur = PART crop（或 GOU 密網板）
for s in 1..STEPS:
  1) UP:     cur × UP_FACTOR（Lanczos · 默認 1.45）
  2) BITE:   SPM 輕 residual · edge-led · clip residual
  3) PRESS:  壓回至 cur×PRESS_NET（默認 1.30）
             LP = 本階起點升采样（blur≤0.35）
             HF = up_bitten 壓回後 × HF_KEEP
             + edge USM 輕
  4) cur = PRESS 結果
終態: 可再一輪 edge SPM 輕咬
貼身: 用 ladder 終態 · 禁 cover 二次空拉
```

## ★ 默認參數（v2 LOCK）

| 旋鈕 | v1（作廢） | **v2 LOCK** | 禁 |
|------|-----------|-------------|-----|
| UP_FACTOR | 1.50 | **1.45** | 單階 ≥2.0 當主路 |
| PRESS_NET | 1.28 | **1.30** | 壓回後仍 ≥UP（無壓） |
| STEPS | 6 | **6**（淨≈×4.8） | 0 階＝一次過 |
| residual_gain | 0.85 | **1.10** | ≥1.5 全圖面咬 |
| rough_boost | 0.55 | **0.70** | 無 clip |
| HF_KEEP | **0.35** | **0.62** | ≤0.4 當定版（過糊） |
| LP_blur | 0.8 | **0.35** | ≥0.8 抹平 |
| edge_USM | 0 | **0.22** | 全圖 USM 當主 |
| residual clip | ±24 | **±28** | 無 clip |
| 咬域 | edge-only | edge + mid-contrast | 整面 fill 當主 |
| SPM 探針 | 24×48² | 28×48² | 與全幅 SPM-A 48×64 分層 |
| 終態 edge 咬 | 無 | **有（輕）** | 終態再 ×4 Hybrid |

## 閘門（PROOF）

| 指標 | v1 FAIL | v2 目標 | 一次爆 |
|------|---------|---------|--------|
| HF σ | ~3.8（死） | ~crop～略高 · 密網可讀 | 高亂 |
| edge density | ~0.05 | **≥0.10**（樣板 0.13） | ~0.14 但拓亂 |
| 觀感 | 糊 | 有序密 · 不炸 | 亂網／油紋 |

## 與其它招

| 招 | 關係 |
|----|------|
| **SPM-A** | 每階 bite 用輕量 SPM（非默認全幅 48×64 一次） |
| **S1HL** | 一升混圖仍 SPM-A；**尺度爬升**改 LP2 |
| **GOU** | 要 93db 式有序蜂窩：先 T3 GEN 密網 donor → 再 LP2 |
| **N2R** | residual 當指紋折射／保留 · 非滅場 |
| **PART_AMP oneshot** | **廢** 作 PART 默認 |
| **漩聯動** | 大圖⇄位標⇄壓細⇄**出新** · 禁回毒母 |

## 一刀參數卡

```
MODE=LADDER_PRESS_V2
BASE_PART=          # crop or GOU plate
UP_FACTOR=1.45
PRESS_NET=1.30
STEPS=6
GAIN=1.10
ROUGH=0.70
HF_KEEP=0.62
LP_BLUR=0.35
EDGE_USM=0.22
RES_CLIP=28
FINAL_EDGE_BITE=true
FAIL_if=HF_sigma≈v1 or edge_dens<0.08
FORBID=oneshot_x4_HF095, cover_empty_up
```

## 樣板路徑

- 過程包：`SETS/GOU_B_LADDER_V2/` · `SETS/GOU_B_LADDER_PRESS/`（v1 反例）
- 爆紋反例：`SETS/GOU_B_AMP_SCALE/04_CHEST_HYBRID_x4_AMP.jpg`
- META：`SETS/GOU_B_LADDER_V2/META.json`
