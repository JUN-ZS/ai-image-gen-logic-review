# face俱圓 · 過程規格 · FACE_JU_YUAN_FJY_01262

## 0. 範圍

| 做 | 不做 |
|----|------|
| 本場同姿全臉 peep／dens 作幾何 | 異姿庫存板硬換本場 |
| plate 比例 **跟 dens／自由** | 默認 2:3 長海報／錯 ar |
| **畫皮皮** dens 框內生成級皮膚 | 錯 ratio 皮硬貼；網紅磨皮 |
| **近臉皮真** 近圖 A±B 皮真實 | 遠景強開 B；磨皮假皮；改 ar |
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
| **B 生成** | 見 **S3.5 畫皮皮 HPP**（i2i 鎖框） |

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
