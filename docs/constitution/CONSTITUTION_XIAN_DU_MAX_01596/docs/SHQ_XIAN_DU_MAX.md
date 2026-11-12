# 先讀MAX · SHQ_XIAN_DU_MAX_V1
write: 01596 · stick: STICK_XIAN_DU_MAX · call: **先讀MAX**

## 0. 是什麼
先讀MAX = 先讀₁（≤N_max discovery）+ 先讀₂（elev 上再 multi-CC discovery · M_max）
的**配額與 densify 時序**總技；掛 勤力DNA · 層層回鎖。

母源：01580 先讀 · 01590 層層回鎖 · 01594 先讀₂必經 · 01595 N≤50 / M_max。

## 1. 金方程
```
先读MAX =
  先读1(discovery ≤ N_MAX)
    ⊕  Imagine生成级 densify₁   ← 勤力：先读1 时已生效
  → 先读2(discovery multi-CC ≤ M_MAX on elev₁)
    ⊕  Imagine生成级 densify₂   ← 勤力：放大/开箱后再 densify
  → 层回锁 本线 S11（冻 M · outside=0）
```

**禁止**：先读1 只 peep 不 densify，把 Imagine 全推到回座前。  
**禁止**：elev 后跳过先读2（E-CC-06）。  
**禁止**：先读2 后不再 densify 却宣称「开箱后再升清」（可声明 C1 仅结构，不得冒 C2 densify₂）。

## 2. 配额闸（先讀MAX 数字）
| 闸 | 默认 | 义 |
|----|------|-----|
| **N_MAX** | 50 | 先读1 最多物件（grid+local CC / multi-CC） |
| **M_MAX** | 6 | 先读2 每 elev 最多子洞 discovery |
| **depth** | 2 | 先读1→2 止；先读3 须新 claim |
| **Imagine_top_k₁** | 可配置 | 先读1 后 densify₁ 外力件数（余下 local 须标 I-PROCESS=local） |
| **Imagine_top_k₂** | 可配置 | 先读2 子洞 densify₂ 外力件数 |

扇出上界：`N_MAX × M_MAX` 清锁级（01595 实证 ~298/300）。

## 3. densify 时序（勤力 · 两发）
| 步 | 何时 | 输入 | 输出 | 勤力 |
|----|------|------|------|------|
| **densify₁** | **先读1 名单已定后立刻** | peep₀ from M₁ | elev₁ 高像素 | I-PROCESS 在先读1 段生效 |
| **densify₂** | **先读2 子洞名单已定后立刻** | peep₂ from M₂ on elev₁ | elev₂ | 放大后再 densify；不得跳 |

```
错：  先读1 → 先读2 → （最后才）Imagine
对：  先读1 → densify₁ → 先读2 → densify₂ → 层回锁
```

理由：先读2 是「开箱后再认」；若 densify₁ 未做，先读2 认的是糊 peep，**发现量假小**。  
 densify₂：子洞又放大，可再生成级 densify 而不换座。

## 4. 与 层回锁 / 勤力 合闸
| 码 | 义 |
|----|-----|
| I-ID-BAN | densify₁/₂ 血缘 = 本线 peep/MARK |
| I-PROCESS | densify₁ 先读1 生效；densify₂ 先读2 再生效 |
| I-SEAT | 层回锁 冻 M₁（父座）回 S11；子洞不另开终极 S11 |
| E-CC-06 | elev 后无先读2 |
| **E-CC-08** | 先读1 后无 densify₁ 就先读2（假开箱） |
| **E-CC-09** | 宣称 densify₂ 却未先读2 discovery |
| D2-01 | 先读2 必须 true discovery（禁死 4 带冒 discovery） |
| D2-02 | M_MAX |
| D2-03 | depth≤2 |

## 5. claim 级
| claim | 条件 |
|-------|------|
| C2_XIAN_DU_MAX | N≤N_MAX · densify₁ 在先读1 · 先读2 discovery · densify₂（或诚实 local 标）· 层回锁 out=0 |
| C1_XIAN1_ONLY | 仅先读1 结构，未 densify₁ |
| FAIL E-CC-08 | 先读2 吃的是未 densify₁ 的 peep 却称开箱 |

## 6. 与 01595 关系
01595 跑通 **N=50 · kids=298 · 层回锁 PASS**，但 elev 为 **local peep×3**（诚实）。  
先讀MAX 宪要求：**目标态 densify₁/₂ = Imagine 生成级**；批量时 top-k Imagine + 余 local 必须分栏写 REPORT，不得全称 Imagine。

## 7. 金句
1. **先讀MAX = 先读1≤N + densify₁ + 先读2≤M + densify₂ + 层回锁。**
2. **Imagine 生成级 densify 在先读1 就生效，先读2 再生效一次（放大后再 densify）。**
3. 先读2 发现量依赖 densify₁；跳 densify₁ = 假开箱（E-CC-08）。
4. 扇出是 Σ discovery，用 N_MAX×M_MAX 封顶，不是取消 densify。
