# PIXEL_RATIO 臉回原圖

## 輸入
- 臉格 HD: `569e285b-fd05-4a51-8200-26e32809ecee` (1600×1232)
- 原圖 M1: `e51cdaa3-af68-4fe7-8487-bbd4b939c267` (1792×1008)
- 全幅 ref: `63fe27ba-3c2c-408a-a2f1-ac2944ad8828`

## 像素比例表（FACE → M1）

| 量 | 臉格 (src) | 原圖 (dst) | 比值 |
|----|------------|------------|------|
| 圖尺寸 | 1600×1232 | 1792×1008 | — |
| 臉框 px | 520×520 @(525,350) | 88×88 @(668,139) | scale_x=0.1692 scale_y=0.1692 |
| 臉中心 px | (785.0,610.0) | (712.0,183.0) | — |
| 臉中心 norm | (0.4906,0.4951) | (0.3973,0.1815) | — |
| **scale_iso** | — | — | **0.169231** |
| place_tl | — | — | (579.15, 79.77) |
| paste ROI | — | (637, 90, 786, 253) | expand face |

## 公式
```
scale_iso = 0.5 * (dst_w/src_w + dst_h/src_h)
place_tl  = dst_center - src_center * scale_iso
paste     = expand(dst_face) with ellipse feather
```

## 步驟
1. Haar 偵測臉格／原圖臉框
2. 算 scale_iso、place_tl（中心對齊）
3. 縮放臉格 → 取 paste ROI 對應切片
4. 顏色均值/方差匹配
5. 橢圓羽化貼回（無 ECC 硬扭，避疊影）
