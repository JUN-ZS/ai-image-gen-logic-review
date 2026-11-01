# LADDER_PRESS_V2 · 階梯放大再壓回（升清 · 禁一次爆紋）

> asof 2026-10-29T16:40:58Z · §0.12.40 · **LOCK**  
> 正名：**階梯壓回升清** · 碼 **LPV2** / **LADDER_PRESS_V2**  
> 試錯：一次×4 Hybrid 爆紋 · v1 過糊未到位 · v2 密網可讀

---

## 一句

**一次一次：小幅放大 → 輕 SPM 咬 → 壓回穩紋（淨增益）→ 多階累積。**  
禁一次 `PART_SCALE≥4 + g≥1.5 + HF0.95`。

---

## 過程（憲定序 · 不可顛倒）

```
S0  crop / 正衣 donor 板（非病毒母）
for s in 1..STEPS:
  1) UP   = Lanczos(cur, UP_FACTOR)          # 例 1.45
  2) BITE = SPM 輕咬 on UP
            · residual_gain ≈ 1.10
            · rough ≈ 0.70
            · edge/KEEP 為主 · residual clip ±28
            · 禁整面狂咬
  3) PRESS = 壓回至 cur×PRESS_NET（例 1.30）
            · LP = 本階起點升采样（blur≤0.35）
            · HF = (BITE−blur) × HF_KEEP（≥0.62 才「到位」）
            · 邊 USM ≈ 0.22 × edge
  4) cur = PRESS
S_final 可選 終態再一輪 edge SPM 輕咬
```

### 參數卡（v2 定稿）

| 旋鈕 | v1（FAIL 過糊） | **v2 LOCK** |
|------|-----------------|-------------|
| UP_FACTOR | 1.50 | **1.45** |
| PRESS_NET | 1.28 | **1.30** |
| STEPS | 6 | **6**（淨≈4.8×） |
| residual_gain | 0.85 | **1.10** |
| rough | 0.55 | **0.70** |
| HF_KEEP | **0.35** | **0.62** |
| LP blur | **0.8** | **≤0.35** |
| edge USM | 0 | **0.22** |
| final edge bite | 無 | **有** |

### 驗收閘

| 閘 | 過線 | 樣板 v2 CHEST |
|----|------|----------------|
| 非一次爆紋 | 目視密網有序 | PASS |
| HF σ | **> v1 且 不整面炸** | crop21.6 → v1=3.8 FAIL → **v2≈23** |
| edge density | **≥ ~0.10** | v1=0.05 FAIL → **v2≈0.13** |
| 尺寸 | final ≥ crop×3 | 645→**3107** |

---

## 試錯入憲

| 試 | 結果 | 入憲 |
|----|------|------|
| 一次 Hybrid×4 g1.55 HF0.95 | **爆紋** 亂網 | **E-LP-01 禁** |
| ladder v1 HF0.35+LP0.8 | **過糊** 升清未達 | **E-LP-02 禁當定版** |
| ladder v2 HF0.62+USM+終咬 | 密網可讀、有序 | **正招** |
| 配件×2 再 cover 空拉 ROI | 虛、非真升 | 貼身用 ladder 終態 · 禁二次空 cover |

樣板：
- 爆：`SETS/GOU_B_AMP_SCALE/04_CHEST_HYBRID_x4_AMP.jpg`
- v1 糊：`SETS/GOU_B_LADDER_PRESS/FINAL_LADDER.jpg`
- **v2 到位：** `SETS/GOU_B_LADDER_V2/FINAL_V2.jpg` · asset `f90d38e1-…`

---

## 黑名單

- **E-LP-01** 一次過 PART_SCALE≥4 + 重 HF 當主升清  
- **E-LP-02** HF_KEEP≤0.40 且 LP blur≥0.6 當「階梯完成」  
- **E-LP-03** 壓回後不驗 edge density / 目視密網  
- **E-LP-04** 用 Ref 小圖冒充 ladder 大尺寸（F-SIZE-01）  
- **E-LP-05** 整面 residual 不 clip、不限 edge  

---

## 掛載

| 技 | 關係 |
|----|------|
| **SPM-A** §0.12.39 | 每階 BITE 可用探針；ladder 內 gain 跟 v2 表 |
| **S1HL** | 全幅一升仍可 SPM-A；**配件真升**走 LADDER 非一次 Hybrid×4 |
| **GOU** §0.12.25 | **密網 donor 先 GEN**，再 LADDER 升尺寸（見 §0.12.41 棧） |
| **N2R** | residual 當指紋保留，非填場滅 |
| **F-SIZE** | ladder 終態才是 SIZE 母 · 禁 Ref 鎖小圖 |

---

## 一刀參數卡

```
MODE=LADDER_PRESS_V2
BASE_CROP=
UP_FACTOR=1.45
PRESS_NET=1.30
STEPS=6
GAIN=1.10
ROUGH=0.70
HF_KEEP=0.62
LP_BLUR=0.35
EDGE_USM=0.22
FINAL_EDGE_BITE=true
RES_CLIP=28
FAIL_IF=edge_density<0.10 OR oneshot_scale>=4_with_hf095
```

*END LADDER_PRESS_V2 · 2026-10-29T16:40:58Z*
