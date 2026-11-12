# 洞座硬锁升清公式

## 问题
上轮 densify/ROI 仍改洞内形位（相对金位 RET 结构漂）。

## 硬锁
金位 seat = 公式回洞 RET。donor 只供纹理，必须先 warp 对齐。

## 公式
```
T' = ECC_affine(TEX → seat)
F2: I* = seat + α · HF(T')     # 推荐：像素位=金，只加高频
F3: I* = seat + clip(α·HF, ±τ)
F1: I* = LF(seat) + HF(T')
S9 = S0A ⊙ (1-M) + I* ⊙ M
```

## 验收
dx=dy=0 · struct_lf_mad<5 · outside=0 · tex_gain 可升

best=F2_seat_plus_aHF
