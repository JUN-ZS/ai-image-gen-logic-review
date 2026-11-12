# DNA 框内闸 · write 01634

## 问题（你指 trio APPLE）
除背 freeframe 苹果在中栏「完整」，右栏 peep 上 **绿影只盖一部分／像框外错扣**，
但旧跑仍 **PASS**（因为 outside=0）。

## 为什么能假 PASS？
```text
outside = max|RETURN−base| on (1−M)
```
M 若是小椭圆／错影：
- 洞外绝大部分仍是 base → outside=0
- **从不检查**「peep 内真物有没有被 M 盖住」
- **从不检查**「除背 freeframe 是否还在 peep 框语义内」

→ **E-OUTSIDE-ALONE-01**（与 01485 D_OUTSIDE_ALONE_NOT_PASS 同族）

## DNA 闸（不改影、不改序）
| 闸 | 义 | 阈值 |
|----|----|------|
| G1 | 影面积占比 | [0.04,0.92] |
| G2 | cover = \|M∩S\|/\|S\| | ≥ 0.72 |
| G3 | 影在 peep 窗内 | contain ≥ 0.98 |
| G5 | 影面积不得远小于 peep 主体 | pix_m ≥ 0.55·pix_s |
| **F8** | G1∧G2∧G3∧G5 | **否则不得 PASS** |

## APPLE 本测
- cover = **0.619**
- contain = **1.0**
- undercover_area = **False**
- codes = ['E-MARK-UNDERCOVER', 'E-OUTSIDE-ALONE-01']
- **F8_PASS = False**  ← 旧 outside 逻辑会绿，新 DNA 应 FAIL

## 金句
1. outside=0  alone 不足 PASS。
2. 影必须盖住 peep 内真物（cover）。
3. 框外/半影 → E-MARK-UNDERCOVER / E-SUBJECT-OUTSIDE-PEEP，F8=FAIL。
4. 闸只判，不 rewrite（守 01633）。
