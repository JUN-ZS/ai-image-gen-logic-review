# 技名 · face俱圓

| 語 | 名 |
|----|-----|
| **正名** | **face俱圓** |
| **粵／短** | **臉俱圓** · **全臉圓框** · **跟 dens 比** |
| **英／碼** | **FACE_JU_YUAN** · **FJY** · Full-Face Round Framing |
| **一句** | **全臉齊額下巴；plate 比例跟 dens／母 peep 自由取，禁硬鎖錯 ratio；ECC 過才貼** |
| **母招** | §0.12.62 · 連 PATH1E §0.12.17 · DBSS §0.12.61 · dens donor |
| **地位** | **LOCK（命名）** · 比例規則可迭代 |
| **禁稱** | 2:3 長海報當默認 · setS 異姿硬換 · 半臉 peep · 降 PIXEL 貼 |

## 公式

```
FACE_ROI     = full face (forehead → chin, ears/hairline if in mother)
DENS_DONOR   = PATH1E/PBI same-pose dens  (geometry lock)
ID_REF       = optional clean identity plate (same person preferred)
PLATE        = Imagine(ref=DENS first, ID second; aspect=auto|match dens)
              # NEVER force 2:3 when dens ar ≈ 0.9
ECC          = findTransformECC(mother_face_ROI, plate→ROI)
HPP_SKIN    = 畫皮皮 i2i(dens) 生成級皮（S3.5 · 可選近臉）
paste iff ECC ≥ 0.85 (raw) · mother WH locked
SHOW         = free long-edge ≥1920  (contain 1920×1080 is display only, not geometry)
```

## 別名

- face俱圓 · 臉俱圓 · FJY · Full-Face Round Framing
- same-pose dens-aspect face plate
- 真 A8B 級本場臉源（比例自由）

## 對照（不是這些）

| 技 | 差異 |
|----|------|
| DBSS 單白殺升 | 殺白+輕量升清鏈；本技專管**臉源比例／全臉／ECC 可贴** |
| A8B setS 庫存成片 | 他場／異姿，**不可**當本場 donor 硬貼 |
| 2:3 海報 peep | **違本技**（ar 錯 → ECC 死） |
| 半臉 peep | 違「俱」＝不全 |
