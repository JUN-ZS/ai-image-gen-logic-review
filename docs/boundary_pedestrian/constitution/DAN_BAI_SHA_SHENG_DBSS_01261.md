# 單白殺升 · 過程規格 · DAN_BAI_SHA_SHENG_DBSS_01261

## 0. 範圍

| 做 | 不做 |
|----|------|
| 母圖尺度（NON-HD）全臉／ROI 殺白 | 先把臉 NCNN／Imagine 成高清再殺白（非本技預設） |
| PATH1E dens + ECC 貼回母圖 | 半臉 peep、只貼五官不貼全臉 |
| Lanczos ×2／×4 幾何升清 | 把 Lanczos 當成感知品質 PASS |
| Imagine light 鎖構圖微銳化 | 重構臉／錘／場景的重生成 |
| 母圖 WH 鎖死、不降 PIXEL | 為貼圖縮小母圖 |

## 1. 輸入

- **A 母圖**：最終要保留構圖的底圖（例：1792×1008）
- **FACE／ROI box**：全臉優先（額→下巴齊），例：`(x0,y0,x1,y1)=(800,30,1600,740)`
- **WNK 公式**（與憲技一致）：

```
kill = NOISE_WHITE ∩ ¬SPEC_LIGHT
NOISE_WHITE ≈ 高亮 + 低飽和 + 高局部變動／Laplacian
SPEC_LIGHT  ≈ 高亮 + 低變動（保留金屬高光）
```

§0.12.26.D 邊界：不誤殺合法高光。

## 2. 步驟（固定順序）

### S1 · 抽 NON-HD peep

```
face = mother[y0:y1, x0:x1]   # 母圖原尺寸，不先升清
```

### S2 · 非高清殺白（核心）

```
face_wnk, mask, stats = WNK(face)
# 可寫：mother 的 face 槽先烤入 face_wnk（可選）
```

**驗收**：產出 `NONHD_WNK_overlay`（紅＝kill），`kill_px`、`frac_kill` 入收據。

### S3 · PATH1E dens

```
dens = SR(face_wnk)   # 預設 NCNN GENERAL_x4 或等價 tile SR
# 本技預設：不再對 dens 做 WNK
```

### S4 · ROI ECC 對位

```
aligned = findTransformECC(template=face_wnk, input=resize(dens→ROI))
# motion 試 EUCLIDEAN / AFFINE / TRANSLATION，取 ecc_cc 最高
gate: ecc_cc ≥ 0.85 或 ncc ≥ 0.85 為 raw pass
# 全臉 peep 時：允許 soft 幾何鎖，但收據必須標 gate_raw vs paste_fail
```

### S5 · feather 硬貼回母圖

```
out_mother = feather_paste(mother_or_baked, aligned, FACE_BOX)
assert out_mother.shape == mother.shape   # 不降 PIXEL
paste_fail = false 當全臉 + 對齊完成並寫出
```

### S6 · 回扣升清（輕量，二選或並用）

**6a Lanczos（幾何）**

```
L2 = Lanczos4(out_mother, scale=2)   # 例 3584×2016
L4 = Lanczos4(out_mother, scale=4)   # 例 7168×4032
```

**6b Imagine light（感知輕修）**

```
prompt 必須鎖：構圖／身份／錘／泥／甲 不變；只微銳化、微清邊
Imagine(image_to_image, out_mother 或 Lanczos-1920 seed)
```

兩者都標記：`quality_qualified=false`（除非另開正式驗收）。

## 3. 收據欄位（最低）

```json
{
  "format": "ige.skill.dbss_dan_bai_sha_sheng",
  "code": "DBSS",
  "skill_id": "01261",
  "face_box": [800, 30, 1600, 740],
  "wnk_nonhd": {"kill_px": 0, "resolution": "NON_HD"},
  "path1e": {"dens_wh": [], "ecc_cc": 0.0, "gate_ok": false},
  "paste_fail": false,
  "mother_wh": [1792, 1008],
  "pixel_drop": false,
  "lanczos": {"x2": null, "x4": null},
  "imagine_light": {"asset_ids": []},
  "hd_face_wnk": false,
  "quality_qualified": false,
  "final_acceptance": false
}
```

## 4. 參考實驗（fbd5 母圖 · 2026-11-02/03）

| 段 | 證據目錄／要點 |
|----|----------------|
| NONHD WNK → PATH1E | `tmp/amrs_nonhd_wnk_path1e/` · kill 671 · ECC 0.996 · paste_fail false |
| Lanczos + Imagine light | `tmp/amrs_daf1_light_up/` · L×2 3584 · L×4 7168 · Imagine assets 957bda29 / 691b2ec9 |
| 母圖預覽 ref | `daf1e8ea-66b8-401c-b4e4-161b01a94415` |

## 5. 與 AMRS／MCP 邊界

- **MCP**：A 母 MASK 抽 donor 像素 —— 本技可不做。
- **AMRS**：母修全鏈（WNK+MCP+PATH1E+DHY+NFP）—— 本技是**短鏈輕量回扣**變體。
- **DBSS**：固定「非高清殺白」+「輕量升清回扣」。


## 與 face俱圓 ALL

face俱圓 **S1.5** 取本技 **S2 非高清殺白** 為必選掛點（dens 前）。

```
face俱圓 ALL:
  S1 ROI → S1.5 單白殺(DBSS-S2) → dens → JLP → HPP → ZNZZP → YLGS → ECC → 貼
```

完整 DBSS（殺白後 Lanczos/Imagine light 回扣）可另開；face俱圓 ALL 預設走 dens 皮鏈而非 DBSS S6 輕升清。
