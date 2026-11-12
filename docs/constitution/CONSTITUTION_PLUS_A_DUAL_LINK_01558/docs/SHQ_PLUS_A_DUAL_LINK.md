# 清+A × 清+A->景 联动不乱

**write** 01558  
**formal** `SHQ_PLUS_A_DUAL_LINK_QINLI_V1`  
**勤力** 合闸

## 一句
先 A 得物洞与 L_bg；再 A->景 只动 L_bg；最后 A 物回贴升清景；claim 分轨；勤力合闸

## 强制相位
```
P0 冻L0
P1 清+A 物叶（L1/M_obj）
P2 合成 L_bg
P3 清+A->景（只动 L_bg → L_bg_qing）
P4 清+A 物回贴 L_bg_qing
P5 勤力合闸
```

## 所有权
- **A**：物洞 · peep@L0 · C2_object
- **A->景**：L_bg · peep@L_bg · C_scene
- 禁交换 peep 源与 claim 轨

## 三种试法
| 策略 | 路径 |
|------|------|
| S_SEQ_FULL | 全序联动（推荐） |
| S_A_ONLY | 只物 |
| S_A2S_ONLY | 只景（停 L_bg_qing） |

## 反乱 R1–R7
见 DNA `anti_chaos_rules`

ACCEPT_FULL_HD=false
