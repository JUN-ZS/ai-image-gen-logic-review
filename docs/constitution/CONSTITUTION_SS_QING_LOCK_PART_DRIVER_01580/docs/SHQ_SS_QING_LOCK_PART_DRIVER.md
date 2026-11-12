# SS验.清锁·件 · 结构前置驱动（write 01580）

> **先读（PREFLIGHT）**  
> 凡要跑批量「SS验.清锁·件」、PART 清锁、vehicle/person/mecha 分件升清回位，  
> **必须先读本宪 + DNA + LOCK**，再执行 `structure`，后才 `batch`。

## 一句

先智能定义物件部件结构（`PART_STRUCTURE`），再批量生效 SS验.清锁·件；框主权在 MARK/peep，elev 只是可换 donor。

## formal / stick / py

| 项 | 值 |
|----|-----|
| formal | `SHQ_SS_QING_LOCK_PART_STRUCTURE_DRIVER_V1` |
| stick | `STICK_SS_QING_LOCK_PART` |
| call | `SS验.清锁·件` |
| py | `shq_ss_qing_lock_part_driver.py` |
| LOCK | `CONSTITUTION_LOCK_01580.json` |

## 两段

```text
[P0 structure]  whole_subject_CV（几何整洞 ≠ GROK 语义）
              + profile（vehicle|person|mecha|auto）
              + 互斥 MARK/peep/xN
              → PART_STRUCTURE.json

[P1 batch]     ∀p: MARK→peep→elev→B_direct hard
              RETURN = L0⊙(1−M)+elev⊙M · outside=0
```

## 方程

\[
\forall p:\;
\mathrm{RETURN}_p = L_0\odot(1-M_p) + \mathrm{elev}_p\odot M_p,\quad
\|R-L_0\|_{\mathrm{outside}}=0
\]

## 主权

| 层 | 归谁 |
|----|------|
| whole / PART 框·洞·位 | **MARK + peep（CV 程式）** |
| 洞内纹理 | elev donor（local_USM / elev-dir / 虚回 / F2…） |
| preset 名 whole_subject / WHEEL | **模型不读** |

## 金句

1. **先读 01580**：无 `PART_STRUCTURE` 禁 batch。  
2. whole_subject（程式）≠ GROK 语义 whole subject。  
3. 真·部件回位 = 金框 + 清锁，不靠模型懂词。  
4. 1 PART = 1 金框 + 1 清锁；批量 = N×同构。  
5. elev-dir 只是 donor 槽之一。

## CLI（先读后执行）

```bash
python3 shq_ss_qing_lock_part_driver.py selftest
python3 shq_ss_qing_lock_part_driver.py structure --l0 L0.jpg --out RUN --profile vehicle
python3 shq_ss_qing_lock_part_driver.py batch --structure RUN/PART_STRUCTURE.json --out RUN
python3 shq_ss_qing_lock_part_driver.py run-full --l0 L0.jpg --out RUN --profile vehicle
```

## 金跑

- selftest PASS  
- `SETS/PROJ_SS_QING_LOCK_DRIVER_ROBOT_01580` · 4 PART · outside_union=0 · `C2_SS_QING_LOCK_PART_BATCH`

## E

| 码 | 义 |
|----|-----|
| E-QLP-01 | 无 PART_STRUCTURE 就 batch |
| E-QLP-02 | 下游重开洞 / 弃金框 |
| E-QLP-03 | outside≠0 报 C2 |
| E-QLP-04 | GROK 词冒 MARK 主权 |
| E-QLP-05 | freeframe elev 无 peep 契约 |

## ACCEPT_FULL_HD

`false`

## 母源

01578 清锁·件（WHEEL）· 01579 BODY 同程序验证 · 01577 SS验.清
