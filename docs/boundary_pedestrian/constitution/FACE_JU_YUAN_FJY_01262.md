# face俱圓 · 過程規格 · FACE_JU_YUAN_FJY_01262


## 全鏈 · ALL（face俱圓 標準序）

```
S1     ROI 全臉（NON-HD · 例 box (920,80)–(1320,520) 依母圖）
S1.5   單白殺 WNK / DBSS 核        ← NON-HD only · 先於 dens
S2/S3  dens 本場同姿（TRUE_A8B 配方 · ar 跟 dens）
S3.4   JLP 近臉皮真
S3.5   HPP 畫皮皮
S3.6   ZNZZP 真女主轉皮
S3.7   YLGS 原臉光鎖（ms_sig8 默認）
S4     SHOW
S5     ECC ≥ 0.85
S6     feather 貼母圖
S7     收據
```

| 槽 | 碼／招 | 一句 |
|----|--------|------|
| S1 | ROI | 全臉俱圓框 · 母圖尺度 |
| **S1.5** | **單白殺 · DBSS/WNK** | **非高清殺白噪 · 不殺合法高光** |
| S2/S3 | dens | 本場同姿 plate |
| S3.4 | JLP | 近臉程序皮真 |
| S3.5 | HPP | 生成級皮 |
| S3.6 | ZNZZP | 女主真皮＋身分 |
| S3.7 | YLGS | 原臉 IC／陰影 |
| S5–S6 | ECC→貼 | 門檻 0.85 · 母圖 WH 鎖死 |

**硬規則**

- 單白殺 **只** 在 dens **之前** 的 NON-HD ROI／臉槽；`hd_face_wnk=false` 為預設。
- dens 之後不再預設 WNK（避免洗掉真皮高頻）。
- 全鏈可跳過可選子招（JLP/HPP/ZNZZP/YLGS），但 **收據必須標 enabled**；S1→S1.5→dens→ECC→貼 為最短含殺白主幹。
- `quality_qualified=false` 直至另開驗收。



## 0. 範圍

| 做 | 不做 |
|----|------|
| 本場同姿全臉 peep／dens 作幾何 | 異姿庫存板硬換本場 |
| plate 比例 **跟 dens／自由** | 默認 2:3 長海報／錯 ar |
| **畫皮皮** dens 框內生成級皮膚 | 錯 ratio 皮硬貼；網紅磨皮 |
| **近臉皮真** 近圖 A±B 皮真實 | 遠景強開 B；磨皮假皮；改 ar |
| **單白殺** NON-HD 殺白 dens 前 | HD plate 上殺白；kill 合法 SPEC |
| **真女主轉皮** 女主 donor 真皮＋身分 | soft-id 冒充；無 donor；跨姿 dens |
| **原臉光鎖** 原 ROI 低頻光＋陰影 | plate 直貼錯光；洗掉高頻真皮 |
| 可選身分 ref（淨臉）合 dens | 身分板改鏡頭／重構姿 |
| ECC ≥0.85 貼回母圖 WH 鎖 | 半臉 peep、降 PIXEL 母圖 |
| SHOW 長邊自由 ≥1920 | 把 1920×1080 letterbox 當幾何 peep |

## 1. 輸入

- **A 母圖**：構圖底（例 1792×1008）
- **FACE_BOX**：全臉 `(x0,y0,x1,y1)`，額→下巴齊（「俱」）
- **DENS_DONOR**：PATH1E±PBI 同姿 dens（例 1280×1400，ar≈ dens_w/dens_h）
- **ID_REF**（可選）：淨臉身分（例戶外證件式 portrait）
- **禁止 donor**：setS 舉錘／他場異姿主圖硬貼

## 2. 比例律（核心 · face俱圓）

```
dens_ar = dens_w / dens_h          # e.g. 1280/1400 ≈ 0.914
plate   = generate(aspect=auto)    # primary ref = dens → 框近 dens_ar
# 允許：1:1 若 dens 近方；自由長邊
# 禁止：未授權強制 2:3 / 9:16 / 16:9 導致 |plate_ar - dens_ar| 過大
```

**圓** 在此＝框完整、比例自洽、全臉不截——不是強制正圓 mask。

| 失敗例 | ar | ECC（實測） |
|--------|-----|-------------|
| 2:3 強鎖 | 0.67 | ~0.65–0.68 FAIL |
| dens 原框 | 0.914 | ~0.982 PASS |
| auto 跟 dens + 身分 | 0.913 | ~0.978 PASS |
| 1:1 近 dens | 1.00 | ~0.926 PASS |

## 3. 步驟

### S1 · 全臉 ROI

```
face = mother[y0:y1, x0:x1]   # 全臉；不全則不算 FJY
```


### S1.5 · 單白殺（WNK / DBSS 核）

**掛點**：S1 ROI 之後、S2 dens **之前**。  
**技源**：`DAN_BAI_SHA_SHENG_DBSS_01261` 的 **NON-HD 殺白** 段（本槽只取殺白，不強制整段 DBSS 升清回扣）。

```
face = mother[y0:y1, x0:x1]          # NON-HD
face_wnk, mask, stats = WNK(face)    # kill = NOISE_WHITE ∩ ¬SPEC_LIGHT
# dens 輸入 = face_wnk（不是 raw 噪臉）
```

- 紅 overlay／kill_px／frac_kill 入收據  
- **禁止** 默認對 dens／HPP／ZNZZP plate 再殺白  
- 與 DBSS 全鏈（殺白→PATH1E→Lanczos/Imagine light）相容：face俱圓 ALL 在殺白後改走 dens→JLP…→YLGS→ECC

### S2 · dens 幾何源

```
dens = PATH1E(face) [± strip PBI]
# dens 為本場同姿幾何主源；不另用異姿庫存替換
```

### S3 · 真 A8B 級 plate（可選身分）

```
plate = Imagine_reference(
  primary = dens,           # 姿／甲／雨／框
  identity = ID_REF?,       # 可選淨臉
  aspect_ratio = "auto"     # 或 match dens；禁錯 2:3 默認
)
# 驗 ar ≈ dens_ar；偏離過大 → 重抽，勿硬貼
```



### S3.4 · 近臉皮真（JLP · 皮真實）

**子招** `JIN_LIAN_PI_ZHEN_JLP_01262B` · **近圖 face 默認**；遠景 skip。

| 層 | 內容 |
|----|------|
| **A 程序** | bilateral 去蠟 → HF residual → mid grain → 輕 desat → Y unsharp；**WH/ar 不變** |
| **B 生成** | 見 **S3.5 畫皮皮 HPP
S3.6 真女主轉皮 ZNZZP
S3.7 原臉光鎖 YLGS**（i2i 鎖框） |

原則：同框同 ar 同姿；禁網紅磨皮／半臉／當 quality PASS；做完仍 **ECC≥0.85**。

詳見 `JIN_LIAN_PI_ZHEN_JLP_01262B.md`。

### S3.5 · 畫皮皮（HPP · 生成級皮膚）

**子招** `HUA_PI_PI_HPP_01262A` · 近臉／真 A8B dens 框內可選必做。

```
# 主路：生成級，鎖框
skin = Imagine_i2i(geom=dens_or_plate_S3,
  prompt="same crop/aspect/pose/armor; only photoreal pores skin, less plastic")
# 輔路：程序皮真實（bilateral+HF+grain）
# 禁：把 2:3 好皮硬當 paste 主源
assert |skin.ar - dens.ar| 小
# 之後 S5 必須重測 ECC
```

詳見 `HUA_PI_PI_HPP_01262A.md` · `HUA_PI_PI_HPP_NAME.md`。


### S3.6 · 真女主轉皮（ZNZZP）

**子招** `ZHEN_NV_ZHU_ZHUAN_PI_ZNZZP_01262C` · **近臉建議開**。

```
pose_plate（dens/JLP/HPP）+ heroine_face（TRUE_A8B identity_ref，默認 f670）
→ 真皮＋身分強轉 plate（非 soft-id）
→ 同 ar · ECC≥0.85 才貼
```

詳見 `ZHEN_NV_ZHU_ZHUAN_PI_ZNZZP_01262C.md`。


### S3.7 · 原臉光鎖（YLGS）

**子招** `YUAN_LIAN_GUANG_SUO_YLGS_01262D` · **近臉建議開**（陰影／IC 與原 ROI 不符時必開）。

```
真女主轉皮 plate → ECC_align 到 FACE ROI
→ 低頻 L + 環境色 ← 母圖原臉
→ 高頻細節 ← plate
→ peep_ic → S5 ECC → 貼
```

詳見 `YUAN_LIAN_GUANG_SUO_YLGS_01262D.md`。證據：`tmp/fjy_ic_match`（ms_sig8 ic≈0.9999）。

### S4 · SHOW（展示，非幾何）

```
SHOW_long = scale(plate, long_edge>=1920)   # 保持 plate 原 ar
SHOW_1920x1080_contain = optional display only
```

### S5 · ECC

```
aligned = findTransformECC(template=face, input=resize(plate→ROI))
# EUCLIDEAN / AFFINE / …
gate_raw = (ecc_cc ≥ 0.85) or (ncc ≥ 0.85)
```

### S6 · 貼回

```
out = feather_paste(mother, aligned, FACE_BOX)
assert out.shape == mother.shape
# 半解預覽 ≠ 母圖降 PIXEL
```

### S7 · 收據

分欄：`face_full`、`dens_ar`、`plate_ar`、`aspect_forced`、`ecc`、`gate_raw`、`setS_hard_swap=false`、`pixel_drop=false`。

## 4. 收據最低欄

```json
{
  "format": "ige.skill.face_ju_yuan_fjy",
  "code": "FJY",
  "skill_id": "01262",
  "title_zh": "face俱圓",
  "face_box": [],
  "face_full": true,
  "dens_wh": [],
  "dens_ar": 0.0,
  "plate_wh": [],
  "plate_ar": 0.0,
  "aspect_mode": "auto",
  "aspect_forced_wrong": false,
  "ecc_cc": 0.0,
  "gate_raw_085": false,
  "paste_fail": false,
  "mother_wh": [],
  "pixel_drop": false,
  "setS_hard_swap": false,
  "quality_qualified": false,
  "final_acceptance": false
}
```

## 5. 參考實驗（揮錘 5c00 · 2026-11-03）

| 段 | 要點 |
|----|------|
| dens donor | `97cfa7e1` · 1280×1400 · ECC 0.982 |
| 錯 2:3 plate | `66b3`/`4713`/`2037` · 1152×1728 · ECC FAIL |
| auto 身分 plate | `43863809` · 1344×1472 ar0.913 · ECC **0.978 PASS** |
| 1:1 | `0dc9c769` · ECC 0.926 PASS |
| 母圖貼回 | 1792×1008 鎖 · `tmp/a8b_ratio_fixed/` |

## 6. 與他技邊界

| 技 | 關係 |
|----|------|
| PATH1E | dens 產線；FJY 管全臉框＋比例＋可贴 |
| DBSS | 殺白輕升鏈；FJY 可接在 dens 後作真臉源 |
| AMRS／MCP | 母修／掩抽；FJY 不替代 MASK 抽像素 |
| A8B 庫存 setS | 僅參考；異姿禁止硬貼（本技明確） |
| **近臉皮真 JLP** | **S3.4 子招**；近臉 A 程序 ± B；遠景 skip |
| **畫皮皮 HPP** | **S3.5 子招**；生成級皮；主路 i2i(dens) |
| **真女主轉皮 ZNZZP** | **S3.6 子招**；女主真臉皮材＋身分強轉 |
| **原臉光鎖 YLGS** | **S3.7 子招**；貼前對齊原臉 IC／陰影 |
