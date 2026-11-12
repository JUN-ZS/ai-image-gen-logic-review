# 框牙 · 強心針反推升清全流程
**write:** 01489 · `KUANGYA_BOOST_REVERSE_SHENGQING_FLOW_V1`  
**parent:** 01487 強心針 · 01483 至高 · 外力GROK  

---

## 根方程

```text
[(生,除,洞,扣)×(反)]  ⊕  強心針[部件'認' ∩ 放大 ∩ 升質×物]
        ←  外力GROK 驅動與理解
```

> **抽圖放大 = 全流程中的 1 步（S5+S6），不是升清本身。**

---

## 公理

- **A0** 外力GROK = 唯一主驅動（Imagine）；本地只證不替
- **A1** 強心針 = AND 三關，不是 OR，不是單步捷徑
- **A2** 抽圖放大 ⊂ 放大 ⊂ BOOST；抽圖放大 ≠ 全流程
- **A3** 升清 = 整條 F8 鏈上的質量閉環，不是單獨 elev 一張
- **A4** elev_candidate ≠ 正生（01484）；正生 = seat-born 洞座外力生

---

## 反推（由針要什麼 → 鏈要備什麼）

### 需要：升質×物

- 必須先有「該物」身份 → 需要 部件認
- 必須有可 densify 的整件像素域 → 需要 peep@MARK 或 seat 域
- densify 主路徑 = 外力GROK，產出 elev_candidate
- 升質結果不得直接當 正回 完成圖

### 需要：放大

- scale-lock densify 綁在 認 過的閉合邊
- 抽圖（peep）只是放大的前置取域，不是放大本身
- 放大 ≠ freeframe 主權特寫
- grow_max 鎖；回位時 scale 對齊洞座

### 需要：部件'認'

- 認 = 幾何身份 + 材質歸屬 + 閉合邊
- 認 依賴 扣/洞 MARK 凍 與 除 的差
- 禁 band 切、self_peep bbox 當認

---

## 正向全流程（正確生成）

| 階 | 名 | F8 | 驅動 | 強心針 |
|----|----|----|------|--------|
| S0 | L0 凍 | 反除 參照基 | 凍結原圖 | — |
| S1 | 正除 | 正除 / 反除 | 外力GROK Imagine | 為 認 準備差域 |
| S2 | 正扣 | 正扣 / 反扣 | kou(L0, 除背/除件) · 禁 self_ | 部件'認' 的遮罩前提 |
| S3 | 正洞 | 正洞 / 反洞 | MARK 凍 TRUE_HOLE | 部件'認' 的幾何座 |
| S4 | 部件'認'（BOOST-1） | 跨 扣/洞 身份閘 | 外力理解 + MARK 邊 | BOOST ∩ 第一元 |
| S5 | 取域 peep@MARK | DONOR0 準備 | L0[MARK] bitexact crop | 放大的輸入域（前置） |
| S6 | 放大（BOOST-2） | 反生 scale-lock | scale-lock densify / gro | BOOST ∩ 第二元 |
| S7 | 升質×物（BOOST-3） | 升清 densify plate | 外力GROK elev densify on T | BOOST ∩ 第三元 |
| S8 | BOOST 閘 AND | 生前總閘 | DNA 01487 | 強心針合取 |
| S9 | 正生 | 正生 / 反生 | 外力GROK seat-born 洞座生 | BOOST 通過後才允許帶 BOOST 標的 正生 |
| S10 | 正回 | 正回 / 反回 | hardpaste 證 | 證，不替 生 |
| S11 | 反板收束 | 全 8 格 + 回 反板 | 框牙 F8 + 牙 audit | 全鏈可溯 |

### 逐步

#### S0 · L0 凍

- F8：反除 參照基
- 驅動：凍結原圖
- 同一相機 L0 寫死
- 禁止下游重算場景

#### S1 · 正除

- F8：正除 / 反除
- 驅動：外力GROK Imagine
- 除件/除頭/除背：外力改圖
- 反除 = L0 有 vs 除後無

#### S2 · 正扣

- F8：正扣 / 反扣
- 驅動：kou(L0, 除背/除件) · 禁 self_peep
- CLIP/M_subj 從 除背 扣
- 反扣：禁 peep 冒 CLIP

#### S3 · 正洞

- F8：正洞 / 反洞
- 驅動：MARK 凍 TRUE_HOLE
- 洞 = 可改區凍
- 反洞：洞外 bitexact

#### S4 · 部件'認'（BOOST-1）

- F8：跨 扣/洞 身份閘
- 驅動：外力理解 + MARK 邊
- 把 peep 當整件：閉合邊 + 身份 + 材質歸屬
- 非 head/torso/leg 比例 band
- 認失敗 → 禁 放大/升質/生
- **注意：** 這不是抽圖；這是認件

#### S5 · 取域 peep@MARK

- F8：DONOR0 準備
- 驅動：L0[MARK] bitexact crop
- 毒素自由 DONOR0 = peep@MARK
- 非整圖 freeframe
- **注意：** 抽圖 ⊂ 此步；只是取域

#### S6 · 放大（BOOST-2）

- F8：反生 scale-lock
- 驅動：scale-lock densify / grow_max
- 在 認 過的整件邊上放大
- scale-lock；禁 freeframe 主權
- 抽圖放大 = S5+S6 的合稱之一，仍只是 BOOST 一關
- **注意：** ★ 用戶所提「抽圖放大」= 此處 1 步，不是全流程

#### S7 · 升質×物（BOOST-3）

- F8：升清 densify plate
- 驅動：外力GROK elev densify on THIS object
- 對 該物 材質/細節 外力升質
- 產出 elev_candidate / densify plate
- 角色 = DONOR1 候選，默認 ≠ 正生

#### S8 · BOOST 閘 AND

- F8：生前總閘
- 驅動：DNA 01487
- 認 ∩ 放大 ∩ 升質×物 全過
- 缺一 E-KY-BOOST-04

#### S9 · 正生

- F8：正生 / 反生
- 驅動：外力GROK seat-born 洞座生
- base = L_empty（除後）或 洞座
- 只填洞；同相機
- 反生：scale-lock；禁 freeframe 當完成

#### S10 · 正回

- F8：正回 / 反回
- 驅動：hardpaste 證
- R[M]=I_sheng[M]；outside=0 vs base
- outside=0 alone ≠ PASS（需 seat_born）
- 反回：洞外≡base；洞內≠空

#### S11 · 反板收束

- F8：全 8 格 + 回 反板
- 驅動：框牙 F8 + 牙 audit
- 八格皆有 正/反 定義
- 牙 stamp claim 分級

---

## 單步 vs 全鏈

- 用戶例：**抽圖放大** → ['S5 取域 peep@MARK', 'S6 放大 scale-lock']
- **≠** 全 F8 升清, 正生, 正回, BOOST 三關, 外力除/扣/洞
- 律：任何單步（含抽圖放大）都不得冒充 [(生,除,洞,扣)×(反)] ⊕ BOOST 全流程

---

## 假捷徑

- ~~只抽圖放大 → 叫升清完成~~ → `E-KY-BOOST-04 + E-KY-SUPREME-02`
- ~~elev 特寫 → 叫 正生~~ → `E-KY-ATX-01 / BOOST-05`
- ~~freeframe hardpaste → 叫 正回~~ → `E-POLLUTE-HOLE_RETURN`
- ~~self_peep band → 叫 部件認~~ → `E-DNA-CANCER-SELF_PEEP / BOOST-01`
- ~~無外力除生 → 本地 HF 全鏈~~ → `E-WLG-DRIVE-01`

---

## 金句

> 強心針反推：要升質×物，必先認件；要放大，必先有整件域；要認，必先有外力除扣洞。  
> 抽圖放大只是 S5+S6；升清是 S0→S11 全鏈。  
> [(生,除,洞,扣)×(反)] ⊕ BOOST ← 外力GROK；缺鏈缺針皆假。  
> 外力理解每格，強心針加固生/升清，本地只證回。  

`ACCEPT_FULL_HD=false`
