# 密絲晶格 · 正確流程 + 防毒過程（§0.12.42）

> asof 2026-10-29T17:17:16Z · 用戶：技法入憲 · 防毒過程記錄

---

## A. 正名與地位

| | |
|--|--|
| 正名 | **密絲晶格** · **FL** |
| 做什麼 | GOU T3 **表面重生** 成 dense gold-silver wire filigree lattice |
| 不做 | 尺度爬升（那是 LP2）· 全圖 Soft · 毒母 densify |

---

## B. 鐵序（不可顛倒）

```
T0  選 BASE = 乾淨板 ONLY
    ✅ crop 空甲 · 已純 hex GOU 板（da39 類）· 已驗 FL 板
    ❌ LP2/SIAX residual 終板 · f90 ladder 終 · e031 錯紋板 當 BASE densify

T1  （可選）STYLE = 目標紋語圖
    role = style_lock  ONLY
    禁  = 當 BASE · 禁複製 residual chaos

T2  GEN
    Ref(BASE, STYLE?) 或 img2img(BASE)
    只改 SURFACE · 鎖姿／洞／分件／棚灰

T3  閘
    單一可讀拓撲語 · 無菱+hex+三角亂夾
    物格未換 · 無臉

T4  （可選）OUT 作 donor → LP2 爬尺度
    禁反過來：LP2 終再當 GOU 母 densify
```

---

## C. 防毒過程（試錯入憲 · 必記）

| 刀 | 母 / 法 | 結果 | 憲判 |
|----|---------|------|------|
| da39 | crop → GOU T3 有序 hex | **純蜂窩** | ✅ 正 BASE 樣板 |
| f90 LP2 | 階梯 residual 終 | 結晶／多語混 | 可作 **style** 不可作 BASE densify |
| e031 | **f90 當 BASE** +「更密 hex」 | **錯紋夾雜**（hex+菱+網+三角） | **E-FL-01 毒** |
| a992 | **crop BASE** + f90 style_lock | 密絲晶格 · 可讀 | ✅ **FL 正典樣** |
| c87 / 0e62 | da39/c87 乾淨母 + 文字密絲 | hex 加密乾淨 | ✅ 無 style 亦可 |
| d55 / b4fac | 乾淨母 + a992/f90 style | 更近密絲 | ✅ style≠BASE |
| a992 後再「查毒」 | 用戶審計 | 確認 e031 因母毒 | 防毒過程 LOCK |

### 根因公式

```
錯紋夾雜  ⇔  BASE 已含多種 residual 語彙
           ∧  指令只說「更密」無 single-topology
           ∧  模型把各語一齊加密

乾淨密絲  ⇔  BASE 單一／乾淨
           ∧  SURFACE only
           ∧  style 最多 lock 語感
```

---

## D. 一刀 prompt 卡（可直接貼）

### D1 雙圖 Ref（推薦）

```
asset_ids = [BASE, STYLE]   # STYLE 可省則走 D2

The first image is the ONLY BASE: keep exact empty mannequin pose,
silhouette, chest oval cutout, shoulder/arm plate layout, hard seams,
studio gray background.

Rebuild ONLY the armor SURFACE as dense gold-silver wire filigree lattice:
fine crystalline micro-facet metal mesh, dense geometric wire network,
high density readable topology on chest, abs, hips, arms.
Photoreal brushed + polished metal.

Use the second image only as texture-language style lock (density + wire feel).
Do NOT copy residual chaos or mixed wrong patterns.
No face, no person, no retopology of plate cuts.
Keep every plate fully in frame; do not change proportions.
```

### D2 單圖 img2img

```
Keep exact pose, silhouette, chest oval cutout, plate seams, studio gray.
Rebuild ONLY surface into dense gold-silver wire filigree lattice language:
crystalline micro-facet mesh, dense geometric wire cells, ordered high density,
readable topology — not random scribbles, not mixed diamond+hex chaos.
Photoreal metal. No face. No retopology.
```

### D3 中文口令

> crop／乾淨板鎖姿；只重生表面＝**密絲晶格語**；金銀絲·微晶格·密而可讀；禁亂殘、禁換骨、禁 ladder/f90 當母 densify。

---

## E. 黑名單（防毒）

| 碼 | 禁 | 為何 |
|----|-----|------|
| **E-FL-01** | LP2 / SIAX residual / f90 階梯終板 **當 BASE densify** | 多語一齊加密 → 錯紋夾雜（e031） |
| **E-FL-02** | 「更密」無 **single topology / filigree only** | 菱+hex+三角並存 |
| **E-FL-03** | style 圖當 BASE 或 virus 母 | §0.12.23 病毒母 |
| **E-FL-04** | FL 板再叠 densify 無閘（叠叠糊） | 層層毒 |
| **E-FL-05** | 用 FL 冒充 LP2 尺度 | 尺度走 LP2；FL 只表面拓撲 |
| **E-FL-06** | 全圖 Soft「更清晰密網」 | 易改物 · 非 GOU T3 |

---

## F. 樣板索引（2026-10-30）

| id 短 | 角色 |
|-------|------|
| da39d847 | 純 hex GOU · 合法 BASE |
| f90d38e1 | 密絲 **style** 語（禁 BASE densify） |
| e031aaa3 | **毒** 反例 · f90 母 densify |
| a9921fdd | **FL 正典** · crop+style |
| c87e231a | da39-only 密絲試 |
| 0e6238bf | c87 + 文字指令 |
| d55e8018 | c87 + a992 style |
| b4fac29a | da39 + f90 style |

過程包：`SETS/GOU_B_T3_F90_STYLE/` · `SETS/GOU_B_DA39_FILIGREE/` · `SETS/GOU_B_C87_TRY/`

---

## G. 一刀參數卡

```
MODE=GOU_T3_FILIGREE
BASE=                 # crop | da39-class clean ONLY
STYLE=                # optional · role=style_lock
PROMPT=D1 or D2
FORBID=E-FL-01..06
OUT=MESH_PLATE donor
NEXT=optional LP2 on OUT
```
