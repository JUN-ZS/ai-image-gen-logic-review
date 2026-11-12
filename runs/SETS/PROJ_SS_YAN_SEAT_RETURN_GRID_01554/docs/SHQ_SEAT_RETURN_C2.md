# 风景主体回格 · 必经 SS验.清 洞座锁回

**write** 01554  
**formal** `SHQ_SS_YAN_GRID_SCENE_SUBJECT_RETURN_SEAT_V2`

## C2 必经
```
MARK_seat + 清锁(elev_lock + seat_hardlock F2) + I-PROCESS + I-ID-BAN + outside=0
```

## 方程
```
C2_WHOLE ⇔ MARK_seat ∧ 清锁 ∧ densify_donor ∧ seat_born ∧ outside=0 ∧ tex_gain≥τ ∧ ¬identity; RETURN = L0⊙(1−M) + F2(lock(densify))⊙M; 禁 bbox-only paste 冒 C2
```

## 证明
outside=0 C2_all=True
