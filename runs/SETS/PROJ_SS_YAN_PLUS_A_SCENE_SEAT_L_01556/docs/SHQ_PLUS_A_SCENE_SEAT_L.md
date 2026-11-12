# SS驗.清+A·风景洞座锁（L流程变体）

**write** 01556

## 在哪做
**去物件后的背景图 L_bg**，不是在 L0 带物上硬咬风景。

## L 链
1. L0
2. 清+A 除主 → L1 / M_obj
3. L_bg = 洞位贴空景
4. 风景座 M = 风景带 ∩ ¬物件
5. peep@L_bg → 清锁 → L_bg_qing
6. 可选物回 L_bg_qing

## 方程
```
L_bg = strip_objects(L0; {L1_i,M_obj_i}); ∀ scene: M_seat = band ∩ ¬M_obj; peep = L_bg⊙M_seat; I* = F2(lock(densify(peep))); L_bg_qing = exclusive_paste(L_bg, I*, M_seat); FINAL = hezhong_objects(L_bg_qing)  # optional
```

outside_scene=0 final_out=0
