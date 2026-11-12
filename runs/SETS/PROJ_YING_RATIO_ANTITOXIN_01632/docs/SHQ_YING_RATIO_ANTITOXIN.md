# 影扣回 · RATIO 杀毒 DNA · write 01632

## 毒（再杀）

| 码 | 名 | 现象 |
|----|----|------|
| E-RATIO-01 | CHUBEI_FREEFRAME_MARK_RESIZE | 除背 freeframe 影直接 resize 成 peep MARK → 绿框比例错（苹果小椭圆） |
| E-PAD-01 | PAD_TIGHT_PASTE_SCALE | pad 窗与 tight 影不一致硬贴 → 1.3–1.7× 压扁 |
| E-FF-01 | FREEFRAME_NO_CORRESPONDENCE | freeframe 无 peep 像素对应 |

## 曾解决 → 再入链

- peep ratio lock（01602）
- PAD align / AntiFF（01605）
- scale-lock ≤ 1.15
- 影扣回主链（01631）但 **未过 RATIO 闸** → 本写补闸

## 杀法

```text
除背影 raw
  → 与 peep 参考物框比 sx,sy
  → 若超 [1/1.15,1.15] 或 AR 漂
      → REGISTER 影 → peep bbox（等比中心）
      → 仍败 → FALLBACK peep-lock 辅影（声明 E-FF-01）
fill := elev(peep0)  尺寸 ≡ peep0（禁压扁）
影扣回 base⊙(1-M)+fill⊙M
```

中心轴仍只虚回认位。
