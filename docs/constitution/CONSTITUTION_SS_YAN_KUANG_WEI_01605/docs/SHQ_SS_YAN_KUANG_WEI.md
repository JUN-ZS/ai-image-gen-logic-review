# 框位回鎖 · SS驗.框位鏈

**call**: `框位回鎖`  
**family**: `SS驗.框位鏈`  
**formal**: `SHQ_SS_YAN_KUANG_WEI_CHAIN_V1`  
**stick**: `STICK_SS_YAN_KUANG_WEI`  
**write**: 01600–01605（鎖 01605）

## 一句
pad 管框全 · 同框 densify 管 freeframe · pad 對位 1:1 管回位；**outside=0 不足證比例**。

## 方程
```
框位回鎖 ≡ peep_pad(touch_sides=0)
         ∧ densify_sameframe|ratio_lock
         ∧ paste_pad_aligned(elev.shape==peep==pad_box)
         ∧ outside_png=0
```

## 系列

| write | call 子名 | 職 |
|-------|-----------|-----|
| 01600 | 離散5 | 離散分區選5→凍座→扣移→BATCH |
| 01601 | 真剪影座 | multi-CC 真剪影替格洞 |
| 01602 | peep比例鎖 | HI 回 peep AR（須接對位） |
| 01603 | 框切診斷 | tight BBOX 切頂 |
| 01604 | 先讀·pad | 5物+水晶球 peep pad（暴露 E-PAD-01） |
| **01605** | **位回** | **paste_pad_aligned + sameframe 去 freeframe** |

## 金路徑
1. MARK 真剪影  
2. peep = tight + PAD → touch_sides=0  
3. densify_sameframe（禁 freeframe 當幾何源）  
4. elev[y,x] → L0[py0+y, px0+x] where M  
5. PNG outside=0 + size_ok  

## 錯誤碼
- **E-PAD-01** peep+pad 壓進 tight MARK → 比例崩  
- **E-FF-01** freeframe 無對應  
- E-DISC5-01..04 離散偽座族  
- E-BBOX-01 框切  

## 與 SS驗.清／清鎖
| | |
|--|--|
| SS驗.清 | 升紋理不改位（F2 金位） |
| SS驗.清鎖 | whole_bite + donor→peep + MARK 反扣 |
| **框位回鎖** | **pad 框全 + 貼回座標契約 + 去 freeframe 幾何** |

## 金句
> pad 擴大 peep 可以；回座必須 pad 對位 1:1。  
> outside=0 ≠ 比例對。freeframe 升清不能當幾何源。

ACCEPT_FULL_HD=false  
asof: 2026-11-11T08:50:40.531570+00:00
