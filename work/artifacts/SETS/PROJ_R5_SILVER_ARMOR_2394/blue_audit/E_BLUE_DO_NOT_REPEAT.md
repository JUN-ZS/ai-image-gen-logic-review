# E-BLUE · 藍噪／色度污染 · 勿再犯

## 現象
銀／金網 peep 升清後，網孔／陰影出現 **深藍／藏青斑**（非母圖結構）。

## 根因碼
| 碼 | 因 |
|----|-----|
| E-BLUE-01 | residual = 全 BGR（SR−LP）· 非 luma-only → 色度漂 |
| E-BLUE-02 | multi-sigma fill 把環境青藍散進 mesh cell |
| E-BLUE-03 | ridge gate 只看幅度 · 不殺 chroma spill |
| E-BLUE-04 | 母圖青藍背景／冷光放大 SR 藍偏 |

## 鐵律
**4× residual 必須 luma 主導**：只注 \(dY\) · 鎖 LP 色度（或 chroma residual ≤5%）。

## 解毒
```
Y_out = Y_LP + (Y_SR − Y_LP)
RGB_out = chromaticity(LP) × Y_out
```
禁：full RGB residual 直貼。
