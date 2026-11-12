# 3D SS

**call**: `3D SS` · **formal**: `SHQ_3D_SS_MICRO_PARALLAX_V1` · **stick**: `STICK_3D_SS`

## 源
用户对 S01 反回图（`@a793b46e`）指出：微错位有立体效果 → 正式命名。

## 定义
回洞后，洞缘/洞内仍有微残差（剪切、亮度、JPEG、升清），视觉上像浅浮雕/假视差 = **3D SS**。

## 方程
```
3D_SS ⇔ outside ≤ MICRO_OUT(16)
       ∧ (inside_p95≥8 ∨ edge_p95≥6)
```

## 本图实测
- outside=7 · inside_p95=33.0 · edge_p95=26.0
- detected=True · band=MICRO

## 关系
SS验=硬闸；3D SS=硬闸附近微残差的**效果名**。outside 大 = 真错位，不叫 3D SS。
