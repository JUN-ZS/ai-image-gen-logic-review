# PAD加大鎖

**call**: `PAD加大鎖`  
**formal**: `SHQ_PAD_EXPAND_SEAT_LOCK_V1`  
**stick**: `STICK_PAD_JIA_DA_SUO`  
**write**: 01606  
**parent**: 框位回鎖 · SS驗.框位鏈（01605）

## 一句
tight 易切邊 → **PAD 加大** peep 管框全；回座 **pad 對位 1:1 鎖**；禁止 peep→tight 壓扁。

## 方程
```
PAD加大鎖 ≡ peep:=pad(tight,δ) ∧ touch_sides=0
           ∧ elev.shape=peep=pad_box
           ∧ paste_pad_aligned
           ∧ ¬paste_fill(→tight)
           ∧ outside_png=0 ∧ size_ok
```

## 兩半必須 AND
| 半 | 職 |
|----|-----|
| **加大** | expand(tight, PAD_FRAC) → 物完整在 peep |
| **鎖** | elev 同 peep 形；貼回 L0[pad_box] where M |

缺「鎖」= E-PAD-01（01604 錯比例教材）。

## 與族
```
SS驗.框位鏈（框位回鎖）
  └─ PAD加大鎖   ← 本 call（原子）
       暴露: 01604 先讀·pad
       閉合: 01605 位回
```

## 金句
> 加大可以；回必須對位。  
> pad 擴大 peep ≠ 把 peep 壓回 tight。

ACCEPT_FULL_HD=false  
asof: 2026-11-11T15:48:24.294840+00:00
