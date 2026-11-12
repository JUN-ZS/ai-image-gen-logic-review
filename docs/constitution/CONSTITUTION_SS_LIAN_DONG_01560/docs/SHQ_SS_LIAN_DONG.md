# SS 聯動

**call:** `SS 聯動`  
**formal:** `SHQ_SS_LIAN_DONG_V1`  
**stick:** `STICK_SS_LIAN_DONG`  
**write:** 01560

## 一句
先 A 得物洞与 L_bg；再 A->景 只动 L_bg；最后 A 物回贴升清景；claim 分轨；勤力合闸

## 方程
```
SS联动 ≡ S_SEQ_FULL: P0 L0 → P1 清+A(L1,M_obj) → P2 L_bg → P3 清+A->景(L_bg_qing,C_scene) → P4 清+A 物回@L_bg_qing(C2_object_on_qing_scene) → P5 勤力合闸
```

## 相位
P0 冻L0 → P1 清+A 物叶 → P2 L_bg → P3 清+A->景 → P4 物回 L_bg_qing → P5 勤力

## 分轨
| | 清+A | 清+A->景 |
|--|------|----------|
| peep | L0 | L_bg |
| claim | C2_object* | C_scene |

## 金试
01559 新图 PASS_LINK=True outside scn/final = 0/0

## 试法
- S_SEQ_FULL 全序联动
- S_A_ONLY 只物
- S_A2S_ONLY 只景

ACCEPT_FULL_HD=false
