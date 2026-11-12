# 虚回×SS验.清+A · PART 多 RERUN 01572

## 妙法
除主留景 在 peep 内 = **除该 PART（主）→ 留 peep 其余为背景** → 升清该 PART → 自座洞锁回。

有 N 个 PART → **RERUN N 次**（每次指定不同 PART）。全 PART PASS 后组 I_inner，再虚回外层。

```
for PART_i in PARTS:   # 独立
  peep0
    → 除 PART_i 主 · L1 留其余背景
    → 升清 elev(PART_i)
    → I_i 自座洞 · outside_i=0
    claim C2_INNER_PART
I_inner = assemble(I_i)
虚回 → L_bg_qing
```
