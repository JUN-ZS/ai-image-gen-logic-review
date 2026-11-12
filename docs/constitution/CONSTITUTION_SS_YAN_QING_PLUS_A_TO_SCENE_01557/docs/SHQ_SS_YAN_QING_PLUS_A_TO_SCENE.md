# SS驗.清+A->景

**call**: `SS驗.清+A->景`  
**formal**: `SHQ_SS_YAN_QING_PLUS_A_TO_SCENE_V1`  
**stick**: `STICK_SS_YAN_QING_PLUS_A_TO_SCENE`  
**write**: 01557 · 技能 **shengqing-huiwei**

## 一句
L0→除主→L_bg空景→风景座@L_bg 清锁→L_bg_qing；（可选）物清+A 回贴闭环

## 方程
```
SS验.清+A->景 ≡ L_bg=strip_objects(L0;{L1_i,M_obj_i}); ∀scene: M_seat=band∩¬M_obj; peep=L_bg⊙M_seat; I*=F2(lock(densify(peep))); L_bg_qing=paste(L_bg,I*,M_seat)
```

## vs 清+A
| | 清+A | **清+A->景** |
|--|------|--------------|
| 洞 | 物洞 | 风景座 @ 空景 |
| peep | L0 | **L_bg** |
| 回 | L0 | **L_bg** |
| claim | C2_object | **C_scene** |

## L 链
1. L0 有景有物
2. 清+A 除主 → L1_i / MARK_obj
3. L_bg = 去物件空景
4. M_seat = 风景带 ∩ ¬物件
5. peep 只自 L_bg → densify → 清锁 F2
6. 合众 L_bg_qing
7. 可选：物 清+A 回贴 L_bg_qing

## 金跑
01556 `SETS/PROJ_SS_YAN_PLUS_A_SCENE_SEAT_L_01556`

ACCEPT_FULL_HD=false
