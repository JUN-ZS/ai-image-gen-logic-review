# §0.12.51 解毒化衣 · DETOX_HUA_YI / DHY（**LOCK**）
# asof 2026-10-31T07:45+08

> 用戶正名：**解毒化衣** · 短碼 **DHY**  
> 試錯源：BW 海報 `1d5a8392` · dens `08cd6ede` 弱 · MATCH ECC 後 FULL Δ≈**1.45** · 用戶「中毒了,沒改」  
> 成功樣：`SETS/OBA_BW_POSTER_TEX4/DETOX_VISIBLE/` · `COMPLETE/FINAL_DETOX_VISIBLE.jpg` · ROI Δ≈**15.6**  
> 連動：§0.12.50 TEX4 · ZSC · §0.12.43 SWP · GOU ECC · E-GS-02/03 · E-ZSC-01

---

## 0.12.51.A 一句

**dens 先改到肉眼見到衣差 → peep 硬換 α≈0.9 · 禁 soft residual 洗死 → PROOF（ROI meanΔ≥12）→ 才 LOCK 化衣。**

---

## 0.12.51.B 失敗→成功鏈（入技能備註 · 必讀）

| # | 失敗（中毒） | 現象 | 憲碼 | 成功（解毒） |
|---|--------------|------|------|--------------|
| F1 | dens≈母（同色同拓微升） | 再貼也「沒改」 | E-ZSC-05 · E-DHY-01 | dens **可見 rewrite**（厚金／換色／拓變） |
| F2 | soft `LP+M·HF` 或弱 hard residual | dens HF 洗返 L1 | E-ZSC-04 | **peep 硬換** `(1-α)母+α dens` · α peep≈0.9 |
| F3 | ECC／template **只對位** 就稱成功 | ncc↑ · FULL Δ≈1 | **E-GS-02/03** · E-DHY-02 | ECC 只鎖人；**有改靠 DHY 貼** |
| F4 | α 過淡／radial 太緊 | 中心幾乎不貼 | E-SWP-04 · F3 | 甲 peep **強 α** · 橢圓覆蓋人衣 |
| F5 | FULL meanΔ≪2 仍口稱「有變」 | 用戶不信 · 成立 | **E-GS-03** · E-ZSC-01 · E-DHY-03 | **PROOF 閘** 先過再稱 |
| F6 | 半修當 master 再升 | 疊毒 spiral | E-TEX-05 | 回 **原母 peep** 再開 dens |
| F7 | L2 直貼全幅 | 對位漂＋毒灌 | E-SWP-01 | 經 peep 人槽 · 可 ECC 後 **硬 peep 貼** |

### 成功鐵序（LOCK）

```
T0  底 = 原母 FULL（禁半修）
T1  人槽 ROI peep（L0 box · 綠形／橢圓）
T2  dens = 可見化衣板
      · 影分身合 IP衣 或
      · 同 peep i2i 但 **肉眼必見** 厚金／換色／順紋
      · 閘：vs 母 peep meanΔ 宜 ≥15（未貼前）
T3  （可）template + ECC 把 dens **對準大圖人**（只姿／位）
T4  **解毒化衣貼**：
      out = (1-α)·母_peep + α·dens_aligned
      α peep 衣/甲 ≈ 0.85–0.95 · 邊 feather
      禁：weak residual 當主路（可輔 · 不得單獨當成功）
T5  PROOF
      ROI meanΔ ≥ 12
      frac(Δ>10) ≥ 0.12
      肉眼 peep 左右可辨
      FAIL → 不稱成功 · 回 T2 加 dens rewrite
T6  可嵌 SWP 升清 **after** 可見化衣 · 仍要 Δ 閘
```

---

## 0.12.51.C 與舊招關係（改錯）

| 舊招／檔 | 曾錯 | 更新 |
|----------|------|------|
| ZSC `FORMULA_ZOOM_SWAP_CLOTH` | soft LP 主式 · 弱 hard 仍 Δ 低 | 主落地改 **DHY 硬 peep**；hard residual 僅當 dens 已可見 |
| SWP §0.12.43 | dens ncc 低仍貼 · 或 residual 咬死後無可見 | 貼前加 **DHY 可見閘**；ncc 與 Δ **雙閘** |
| GOU／ECC MATCH | 對準人 = 完成 | **MATCH ≠ 化衣**；MATCH 後必 DHY |
| TEX4 §0.12.50 | 可報 ncc 當對紋完成 | 化衣／換紋落地必 **DHY PROOF** |
| 紅衣鐵證 | 證明鏈通但非日常升清 | 紅衣＝DHY 可見極端樣；厚金＝日常樣 |

---

## 0.12.51.D 閘

| 閘 | 過 | 殺 |
|----|-----|-----|
| dens vs 母 peep（貼前）meanΔ | ≥15 優 | ≪8 = 無 rewrite |
| ROI 貼後 meanΔ | **≥12** | <5 = E-DHY-03 |
| frac Δ>10 | ≥0.12 | <0.05 = 沒改 |
| 肉眼 peep 對照 | 可辨衣差 | 「同張」= FAIL |
| ECC cc（若用） | ≥0.5 姿鎖 | 不可代替 Δ 閘 |

---

## 0.12.51.E 一刀參數卡

```
MODE=DETOX_HUA_YI
BASE=mother_peep_only
DENS=visible_rewrite   # IP衣 or i2i 厚金/換色
MATCH=optional_ECC     # 只對人
PASTE=hard_peep_alpha  # α≈0.9 · (1-α)M+α dens
BAN_residual_as_main=true
BAN_claim_if_FULL_d_lt_2=true
GATE_ROI_D=12
GATE_FRAC10=0.12
SAMPLE=SETS/OBA_BW_POSTER_TEX4/DETOX_VISIBLE/
```

## 0.12.51.F 樣板

| 角色 | id／路徑 |
|------|----------|
| 母 | `1d5a8392-2fe4-425b-ad80-9aa8d0f5b577` |
| 毒 MATCH | FULL Δ≈1.45 · `FINAL_MATCH_ECC` |
| dens 可見 | `831dac7f` 厚金 · `d369e759` 粗金 |
| 成功 FULL | `FINAL_DETOX_VISIBLE.jpg` · ROI Δ≈15.6 |

*END §0.12.51 · 解毒化衣 · LOCK · asof 2026-10-31T07:45+08*
