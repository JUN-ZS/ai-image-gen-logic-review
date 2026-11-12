# 虛回

**call:** `虛回`  
**formal:** `SHQ_XU_HUI_VIRTUAL_RETURN_V1`  
**stick:** `STICK_XU_HUI`  
**write:** 01563  
**母 call:** SS 聯動  
**金试:** 01562

## 一句
升清图 ≔ 虚拟(SS联动 已抽出放大升清未回 peep)；回位只信 联动 MARK·frame·L_bg_qing；禁自开补给计划

## 方程
```
虛回(I_elev | Bus_SS) := I_elev 虚拟 peep↑；lock = elev_donor_contract_lock(peep0, pm, I_elev)；I* = seat_hardlock_sheng(peep0, lock, pm, F2)；RETURN = hardpaste(L_bg_qing, I*, M)  洞外 bitexact
```

## 为何有此技
01561 自开「材质补给」= 偷计划。  
正确：升清图**虚拟**成 SS联动 已抽出放大升清未回，**只跟**联动锁位回。

## 禁
- 另写回位策略
- 重开洞 / 重算 MARK
- 洞外非 0 报 C2

## 流程
1. I_elev  
2. 虚拟角色声明  
3. 读联动 Bus 锁  
4. 现成 lock+F2+hardpaste  
5. outside=0

ACCEPT_FULL_HD=false
