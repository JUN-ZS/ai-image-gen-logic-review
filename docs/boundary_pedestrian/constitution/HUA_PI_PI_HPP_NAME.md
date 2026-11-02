# 技名 · 畫皮皮

| 語 | 名 |
|----|-----|
| **正名** | **畫皮皮** |
| **粵／短** | **畫皮皮** · **生成級皮** · ** dens 上畫皮** |
| **英／碼** | **HUA_PI_PI** · **HPP** · Generative Skin Paint |
| **一句** | **在 dens／face俱圓 正確 ar 框內，用生成級寫真皮膚（i2i 或程序），不改 ratio、不改姿** |
| **母招** | face俱圓 **FJY §0.12.62** 子招 · 接 PATH1E dens |
| **地位** | **LOCK（命名）** · 掛在 FJY S3.5 |
| **禁稱** | 2:3 海報皮當主源硬貼 · 磨皮網紅假皮 · 為皮改構圖 |

## 公式

```
geom   = dens | FJY plate (aspect match dens, full face)
skin   = Imagine_i2i(geom, skin-only)     # 主路 · 生成級
       | OR procedural_skin_real(geom)    # 輔路 · 可控
       | OR ref_skin quality ONLY if primary=geom & ar=auto
gate   = ECC(geom_or_skin → mother_ROI) ≥ 0.85
assert skin.ar ≈ dens.ar  AND  skin.WH 不強制錯 2:3
```

## 別名

- 畫皮皮 · HPP · Generative Skin Paint
- 近臉生成級皮 · dens-locked skin i2i
