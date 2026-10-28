# 同姿換對衣 · HOW TO（反推 a6eca7c8 成功）

## 一句
**姿/臉/手/杖 = BASE 硬鎖；衣 = 另源真生成覆蓋。不是先開新構圖，也不是只 V5 貼皮。**

## 成功條件（量）
| 區 | 現象 | 意 |
|----|------|-----|
| 臉 | ncc 高 · mae 低 | identity+角度鎖死 |
| 手/杖 | ncc 高 | OTL0 握姿+開月頭不漂 |
| 甲/裙/披 | ncc 低 · mae 高 | 衣真換（含披風等新拓） |

## HOW（可複用配方）

### 路徑 S1 · 同框 Ref 換衣（最接近 a6ec）
```
asset[0] = BASE 全幅（姿·臉·杖·鏡·場 主）
asset[1] = 正衣／目標衣 板（語系 donor · role=lock）
prompt  =
  Keep first image EXACT pose, face, hair, hands, staff topology, camera.
  Replace ONLY the outfit with the armor dress language of the second image
  (materials, filigree, silhouette extras like cape if in donor or requested).
  Photoreal. Do not redraw face or weapon.
aspect = same as BASE
```
**關鍵：** asset[0] 必須是 **有人全幅姿**，不是空衣；空衣只當 [1]。

### 路徑 S2 · GOU 密網合（憲 T2–T10）
```
BASE 全幅
→ 裁甲 ROI（含肩披若要）
→ GEN Ref(crop, 正衣_lock) 真重建甲面
→ ECC ncc≥0.75 對回 crop
→ 勾形 RANGE（非方框）
→ V5 α 拼 FULL · 臉/杖 α≈0
```
適合「升清+微換語系」；大換披風拓用 S1 更穩。

### 路徑 S3 · MSR-ZYF
```
L0 場 → L2 正衣一次 OK → 合新 = Ref(BASE骨架, 正衣)
訊號 KEEP 只管噪 · 不正衣再亂改拓
```

## 禁（導致你前面「錯」）
| 錯 | 為何失敗 |
|----|----------|
| 正衣當 asset[0] 開新姿 | 姿漂·臉漂·杖格漂 |
| 只 Soft 全圖修對稱 | 治標 · 衣拓不真換 |
| GOU fill 過肥無勾形 | 邊界糊 · 像貼膜 |
| 空衣 REF 舊框當「新構」 | 仍鎖舊裁 or 亂構 |

## 一刀參數卡
```
MODE=同姿換衣 S1|S2|S3
BASE_ASSET=   # 姿主 · 必全幅有人
DRESS_LOCK=   # 正衣 · role=lock 非 base
LOCK= face, hands, staff_OTL0, camera
FREE= garment surface + optional cape/skirt topo
PROOF= face_ncc高 · weapon_Δ低 · torso_Δ高
```

---
## 姿漂（F-POSE-01）備註 · asof 2026-10-29
同姿換衣 **失敗判** 不只「衣不對」：若衣對而姿／構／杖位變 → 仍 FAIL。
必寫：EXACT same pose, crop, head turn, staff height and grip。
GOU-B 新構（姿可Ω）與 同姿掃衣 **分軌** · 見 SCD §0.12.37.E。
