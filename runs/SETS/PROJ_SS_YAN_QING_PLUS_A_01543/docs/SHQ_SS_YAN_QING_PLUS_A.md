# SS驗.清+A

**call**: `SS驗.清+A`  
**formal**: `SHQ_SS_YAN_QING_PLUS_A_SEMANTIC_MARK_V1`  
**write**: 01543

## 一句
同机位 EDIT 除主→空景 L1；|L0−L1| 得 MARK_semantic；面积闸+反扣后接 SS验.清 F2（外力定义 whole 的可落点）

## 方程
```
SS验.清+A ≡ EDIT_除主(L0)→L1_empty → MARK_sem = f(|L0−L1|) → anti_kou(area,outside) → peep=MARK_sem bbox → [可选] elev_lock + SS验.清(F2)
```

## 路径 A
同机位 EDIT **除主** → L1 空景 → `|L0−L1|` → **MARK_semantic** → 面积闸 → peep → SS验.清 F2

## 与 SS验.清 / 清锁
| | |
|--|--|
| SS验.清 | F2 洞座硬锁升纹理 |
| SS验.清锁 | whole prompt + donor 锁 peep + MARK 反扣 |
| **SS验.清+A** | **外力除主定义 whole → 语义 MARK**，再接清/清锁 |

## 金句
外力定义「是谁」→ 冻成 MARK；preset `whole_subject` 只作校驗，不作语义源。

ACCEPT_FULL_HD=false
