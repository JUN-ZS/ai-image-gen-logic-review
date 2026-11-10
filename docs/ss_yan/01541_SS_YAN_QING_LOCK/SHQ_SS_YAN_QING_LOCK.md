# SS驗.清鎖

**call**: `SS驗.清鎖`  
**formal**: `SHQ_SS_YAN_QING_LOCK_WHOLE_BITE_V1`  
**stick**: `STICK_SS_YAN_QING_LOCK`  
**write**: 01541

## 一句
外力 densify/elev 必契约锁回 peep；EDIT 写死整件边界；MARK 反扣 outside=0 + 面积比

## 方程
```
SS验.清锁 ≡ SS验.清(F2) ∧ elev_donor_contract_lock(peep) ∧ whole_bite_EDIT_prompt ∧ MARK_anti_kou(outside=0, area_ratio)
```

## 為什麼需要
`whole_subject` preset **不是**外力語義。外力 freeframe densify/elev 常只框局部。  
本技三件 AND：

1. **EDIT prompt** 寫死整件邊界（`[[WHOLE_BITE_CONTRACT]]`）
2. **donor 契約鎖回 peep**（`elev_donor_contract_lock`）
3. **MARK 反扣** outside=0 + 面積比 + peep 比例

## API
- `build_whole_bite_edit_prompt(subject, action)`
- `elev_donor_contract_lock(peep, pm, elev)`
- `mark_anti_kou_verify(L0, other, M)`
- `ss_yan_qing_lock_run(...)`

## 與 SS驗.清
| | |
|--|--|
| SS驗.清 | F2 洞座硬鎖升紋理 |
| **SS驗.清鎖** | 清 + **whole 咬合契約 + MARK 反扣 + donor 鎖回** |

ACCEPT_FULL_HD=false
