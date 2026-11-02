# 技名 · 近臉皮真

| 語 | 名 |
|----|-----|
| **正名** | **近臉皮真** |
| **粵／短** | **近臉皮真** · **皮真實** · **近圖開皮** |
| **英／碼** | **JIN_LIAN_PI_ZHEN** · **JLP** · Near-Face Skin Realism |
| **一句** | **近圖 face 在 face俱圓 框內做皮膚真實感（程序 A ± 生成 B），同框同 ar 同姿；遠景可跳過** |
| **母招** | face俱圓 **FJY §0.12.62** 子招 · 槽 **S3.4**（接 **S3.5 畫皮皮**） |
| **地位** | **LOCK（命名）** · 2026-11-03 補入（此前只口頭／HPP 輔路） |
| **禁稱** | 網紅磨皮 · 為皮改 ratio · 半臉 · 當 quality PASS |

## 公式

```
IF near_face (peep 大、臉佔畫幅高):
  A = procedural_skin_real(plate)   # 默認開
  B = Imagine_i2i skin OR 畫皮皮 HPP  # 加分／生成級
ELSE:
  skip 近臉皮真
assert same crop · same ar · same pose
then ECC ≥ 0.85 → paste
```

## 與畫皮皮邊界

| 招 | 角色 |
|----|------|
| **近臉皮真 JLP** | **何時做** + **A 程序皮** + 是否上 B |
| **畫皮皮 HPP** | **B 的生成級主路**（i2i dens 鎖框） |

近臉皮真 **A 可單獨**；要生成級則 **A→B(HPP)** 或直接 B。

## 別名

- 近臉皮真 · 皮真實 · JLP · Near-Face Skin Realism
