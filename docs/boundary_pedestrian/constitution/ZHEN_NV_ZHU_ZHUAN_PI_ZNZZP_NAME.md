# 技名 · 真女主轉皮

| 語 | 名 |
|----|-----|
| **正名** | **真女主轉皮** |
| **粵／短** | **真女主轉皮** · **女主真皮** · **轉皮** |
| **英／碼** | **ZHEN_NV_ZHU_ZHUAN_PI** · **ZNZZP** · Heroine True-Skin Transfer |
| **一句** | **用女主真臉圖當皮材＋身分 donor，轉到同姿全臉 plate；不是輕量身分 soft-mix** |
| **母招** | face俱圓 **FJY §0.12.62** 子招 · 槽 **S3.6**（接 畫皮皮 S3.5 後、ECC 前） |
| **地位** | **LOCK（命名）** · 2026-11-03 |
| **禁稱** | soft-id 冒充轉皮 · setS 異姿硬換 · 只磨皮無女主 donor |

## 公式

```
pose_plate   = dens / JLP / HPP 同姿全臉（幾何鎖）
heroine_face = TRUE_A8B identity_ref（本場默認 @f670）
真女主轉皮 plate = ref(pose_plate, heroine_face)
  要求：皮材+身分來自女主；構圖/ar/姿/甲來自 pose_plate
assert ar ≈ dens_ar
ECC ≥ 0.85 → paste
```

## 與前後招邊界

| 招 | 角色 |
|----|------|
| 近臉皮真 JLP | A 程序皮 · 可無女主 donor |
| 畫皮皮 HPP | 生成級皮 · 可無特定女主 |
| **真女主轉皮 ZNZZP** | **必須**女主真臉 donor · 皮材＋身分強轉 |

## 別名

- 真女主轉皮 · 女主真皮 · ZNZZP · Heroine True-Skin Transfer
