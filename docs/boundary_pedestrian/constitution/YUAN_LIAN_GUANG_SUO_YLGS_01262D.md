# 原臉光鎖 · 過程規格 · YUAN_LIAN_GUANG_SUO_YLGS_01262D

## 0. 地位

**face俱圓 FJY_01262 子招** · **S3.7**  
接在 **S3.6 真女主轉皮** 之後、**S5 ECC** 之前。

問題：真女主轉皮 plate 常帶棚拍／平光，直貼後 **臉陰影／IC 不像母圖原臉**（雷雨側光、泥雨遮罩）。

證據：`tmp/fjy_ic_match/RESULT_IC_MATCH.json`  
- true_no_ic ≈ **0.975**  
- ms_sig8 後 ≈ **0.9999**  
主推母圖例：`cd98b954`（ms_sig8）

## 1. 輸入

| 輸入 | 要求 |
|------|------|
| **mother FACE ROI** | 原圖光源／陰影真值 |
| **true_skin_plate** | S3.6 輸出（或 dens/HPP 若跳過轉皮） |
| **FACE_BOX** | 與 S1 同一框 |

## 2. 算法契約（程序 · 默認）

```
1. aligned = findTransformECC(ROI, resize(plate))  # AFFINE 優先
2. LAB 分解 plate 與 ROI
3. L_roi_lo = GaussianBlur(L_roi, sigma)
   L_pl_hi  = L_plate - GaussianBlur(L_plate, sigma)
4. L_out = clip(L_roi_lo + detail_gain * L_pl_hi)
5. a,b   = lerp(a_plate, a_roi, chroma_src)   # 環境色輕拉
6. peep_ic = LAB→BGR(L_out, a, b)
```

### 推薦參數（近臉）

| 變體 | sigma | detail_gain | chroma_src | 用途 |
|------|-------|-------------|------------|------|
| **ms_sig8** | 8 | 1.0–1.05 | 0.22 | **主推** · 陰影緊跟原臉 |
| ms_sig12 | 12 | 1.0 | 0.28 | 較柔 |
| ms_ic_strong | 16 | 0.88 | 0.40 | IC 更重、皮略讓 |

禁止：只做全圖 Reinhard 且不保留 plate 高頻。

## 3. 驗收

```
ic_corr(peep, roi_lo)  ≥  明顯高於 plate 直比（目標 ≥0.99 近臉）
detail_std 不崩（≥ ~0.4 × plate 高頻 std）
再進 S5：ECC ≥ 0.85 才貼
```

## 4. face俱圓 全鏈（更新）

```
S1   全臉 ROI
S2   dens 本場同姿
S3   plate auto 跟 dens
S3.4 近臉皮真 JLP
S3.5 畫皮皮 HPP
S3.6 真女主轉皮 ZNZZP
S3.7 原臉光鎖 YLGS     ← 本技（IC／陰影）
S4   SHOW（可對 peep_ic）
S5   ECC ≥ 0.85
S6   feather 貼母圖
S7   收據
```

## 5. 收據

```json
{
  "ylgs": {
    "enabled": true,
    "method": "ms_lab_L_lo_from_roi_hi_from_plate",
    "sigma": 8,
    "detail_gain": 1.05,
    "chroma_src": 0.22,
    "ic_corr_before": 0.975,
    "ic_corr_after": 0.9999,
    "ecc_after_align": 0.97,
    "variant": "ms_sig8"
  }
}
```

## 6. 與 ZNZZP

- ZNZZP 解決 **誰的皮／誰的臉**  
- YLGS 解決 **光從哪裡來**  
- 兩者都開才接近「像原場裡的那個女主」
