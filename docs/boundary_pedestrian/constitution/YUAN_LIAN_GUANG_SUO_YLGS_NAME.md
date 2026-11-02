# 技名 · 原臉光鎖

| 語 | 名 |
|----|-----|
| **正名** | **原臉光鎖** |
| **粵／短** | **原臉光鎖** · **光鎖** · **IC 鎖** |
| **英／碼** | **YUAN_LIAN_GUANG_SUO** · **YLGS** · Original-Face Illumination Lock |
| **一句** | **貼前把 plate 低頻光／陰影對齊母圖原臉 ROI；高頻皮材留真女主轉皮** |
| **母招** | face俱圓 **FJY §0.12.62** 子招 · 槽 **S3.7**（S3.6 真女主轉皮 → **S3.7 原臉光鎖** → S5 ECC） |
| **地位** | **LOCK（命名）** · 2026-11-03 |
| **禁稱** | 無 IC 直貼冒充光鎖 · 為對光改構圖／改 ar · 整臉磨掉真皮 |

## 公式

```
aligned = ECC_align(true_skin_plate → mother FACE ROI)   # 幾何先
L_lo, ambient_chroma ← 母圖原 ROI
L_hi, pores          ← 真女主轉皮 plate
peep_ic = L_lo(orig) + L_hi(plate)  + mild chroma pull to orig
assert ic_corr(peep_ic, orig_roi) ≫ ic_corr(plate, orig_roi)
→ S5 ECC gate（對 peep_ic 或已對齊 peep）→ S6 paste
```

## 與前後招

| 招 | 角色 |
|----|------|
| 真女主轉皮 ZNZZP | 女主皮材＋身分 · **可帶錯光** |
| **原臉光鎖 YLGS** | **修 IC／陰影 · 不改身分幾何** |
| ECC S5 | 對位門檻 · 非光照轉移 |
