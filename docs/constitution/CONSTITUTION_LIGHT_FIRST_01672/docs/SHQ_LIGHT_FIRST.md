# 先光 01672

## 应变
参考 B1 正（f7045d67）：**程序先走光，再做之后的处理**。

## 序
```
S0
 → ① 先光 L1 = soft_relight + residual_specular(ENV正/追B1)
 → ② 剪影结构叠在 L1（禁框）
 → ③ 内腔 aperture = L1（镂空）
 → S11
```

## BAN
先座后光、事后补光当主光、方框死贴。

PASS=True dL S11→GOLD 30.70 < S0→GOLD 33.21
