# SS驗.清+C·格框

**call**: `SS驗.清+C·格框`  
**formal**: `SHQ_SS_YAN_QING_PLUS_C_GRID_CELLS_V1`  
**write**: 01548  
**stick**: `STICK_SS_YAN_QING_PLUS_C_GRID`

## 一句
Detect/认全图 → 每物一格 peep cell（黄框卡）；WHOLE hardpaste 回 L0；PART 只入格不独立回洞

## 方程
```
∀i: cell_i = frame(peep(box_i)); RETURN = hardpaste(WHOLE only, exclusive); PART ⊏ grid only
```

## 两层
| 态 | 作用 |
|----|------|
| 格框 | 认物展示 · 每物一 peep cell |
| 回图 | 仅 WHOLE hardpaste · outside=0 |
| PART | 只入格 |

## 金句
格框认万物；WHOLE 才回洞；PART 只入格不独立回。

## 证明 01548
- 6 格：3 WHOLE + 3 PART
- outside_return = 0

ACCEPT_FULL_HD=false
