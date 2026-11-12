# 正追 · write 01665

## call
**正追** · formal `SHQ_ZHENG_ZHUI_MIN_B1_V1`

## 最小链（最小集）
```
S0 + MARK_NEAR + ENV(μ=正) + 追·B1
```

## 方程
```
B1_正追 = densify( sample( S0 ± tint_正, M_NEAR, ENV_正, mode ) )
```
mode ∈ metal | glass | diffuse

## 是 / 否
| 是 | 否 |
|----|----|
| B1 叶 · 独补给 intermediate | S11 / RETURN |
| 可单独出图（教学/VDIR） | 应 全链完成 |
| 座内写 ENV_正 反射 | freeframe 换景 |
| claim C1_LEAF | claim C2 outside=0 终闸 |

## 前设表
| 项 | 硬 | 说明 |
|----|----|------|
| S0 | ✓ | 同机位 |
| MARK_NEAR | ✓ | 座冻 |
| ENV_正 | ✓ | 本光正向 |
| 追·B1 | ✓ | sample+densify |
| B2/B3/hardpaste |  | 仅升到 S11 |
| 正×独 |  | 仅 应 PRIMARY |

## 与父技
- **追** ⊃ **正追**（B1 叶 + μ 锁正）
- **正** → ENV 源
- **应** | μ=正 截到 B1 = **正追**

## 错误码
- E-ZZ-01 无 S0
- E-ZZ-02 无 MARK_NEAR
- E-ZZ-03 ENV 非正
- E-ZZ-04 B1 冒 S11
- E-FF-01 freeframe

## 金句
1. 正追 = 最小可出的「正·追」叶。
2. 能单独贴；不能单独封金。
3. 升金要回 应 全式 hardpaste outside=0。

asof 2026-11-12T03:56:28.752975+00:00
ACCEPT_FULL_HD=false

## 01666 修
 densify **只在 peep/座内**，再 hardpaste 回 S0；全帧 densify → E-FF 洞外漂。

## 01668 改正 FORMULA V2（换材毒）

### BAN
```
peep' = (1-w)*peep0 + w*ENV   + CLAHE   // E-ZZ-08
```

### V2
```
R_spec = s(g) * (ENV_正 - mean(ENV))
peep'  = LockAB(peep0) + alpha * R_spec
B1     = hardpaste(S0, peep', M)
```
- alpha metal≈0.16 · diffuse≈0.10
- densify：轻 highpass；**禁 CLAHE on metal**
- 闸：outside=0 ∧ Δsat≤0.12 ∧ Δgray≤18 ∧ mad≤22

### 同景 3P3O 重跑
PASS=True n_ok=3 asof 2026-11-12T04:13:46.411405+00:00
