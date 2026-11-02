# 近臉皮真 · 過程規格 · JIN_LIAN_PI_ZHEN_JLP_01262B

## 0. 地位

**face俱圓 FJY_01262 子招** · **S3.4**  
此前對話已論證「可以近臉做皮真實」，但**未 LOCK 正名**；本次正式入憲。  
**畫皮皮 HPP_01262A = S3.5** 承接本招 B 路生成級。

## 0.1 原則（不破 FJY）

| 可 | 不可 |
|----|------|
| 同框、同 ar、同姿 | 改 ratio／重構構圖 |
| 去塑料、回微孔、自然次表面 | 整臉磨皮成網紅假皮 |
| dens／auto plate 上做 | 當 quality PASS |
| 做完再 ECC 貼（仍 ≥0.85） | 為磨皮裁半臉 |

**「圓」**＝全臉框完整 + 比例自洽  
**皮真實**＝框內材質優化，不是另開一張海報臉

## 1. 何時開

| 條件 | 決策 |
|------|------|
| 近圖 face（peep 大、臉細節可辨） | **默認 A**；可加 B/HPP |
| 遠景全身臉小 | **skip** |
| TRUE_A8B dens／畫皮後仍蠟 | 開 A±B |

## 2. A · 程序皮真實（可控、不改 WH/ar）

```
1. bilateral 去 SR 階梯／蠟面
2. 高頻 residual 留毛孔／髮絲
3. 中灰皮膚區 mild grain
4. 中調輕降飽和（減假橙）
5. 只在 Y 做輕 unsharp
assert out.shape == in.shape
backend = "procedural"
```

可直接當 FJY plate 下游。

## 3. B · Imagine 皮真實／畫皮皮

```
prompt 鎖：same crop / aspect / pose / armor
只改：natural skin, subtle pores, less plastic
→ 正式生成級主路見 畫皮皮 HPP_01262A
抽查 ar 與 ECC，防 reframing
```

## 4. 掛進 face俱圓

```
S1  全臉 ROI
S2  dens 幾何（本場同姿；TRUE_A8B 作配方）
S3  FJY plate (auto 跟 dens，可選身分)
S3.4 近臉皮真 JLP   ← 本技（近臉默認 A）
S3.5 畫皮皮 HPP     ← 生成級 B（可選／加分）
S4  SHOW 自由長邊
S5  ECC ≥ 0.85
S6  feather 貼母圖
S7  收據
```

## 5. 收據

```json
{
  "jlp": {
    "enabled": true,
    "near_face": true,
    "layer_A_procedural": true,
    "layer_B_hpp_or_imagine": false,
    "ar_unchanged": true,
    "ecc_after": 0.0,
    "gate_raw_085": false
  }
}
```

## 6. 證據目錄

- `tmp/fjy_skin_real/`（A 程序）
- `tmp/fjy_ratio_skin_gen/` · HPP i2i `b55a53be`（B）
- 對話論證 asof 近臉可做皮真實（本檔 LOCK）
