# SHQ · DNA 系統（01474）— 通用 Project DNA + 獨立性格 DNA 庫

**formal:** `SHQ_DNA_SYSTEM_V1`  
**write_id:** `01474`  
**PY:** `shq_dna_system.py`  
**母:** 01472 Harness · 01473 Audit Force · 01389 Claim  
**ACCEPT_FULL_HD:** false

---

## 0. 一句

> **Project DNA** = 每個獨立出圖 project 的**邊界 + 外接權碼**（通用、可優化掃描）。  
> **Persona DNA** = **性格／身份獨立庫**（跨 project 引用，不併入單一出圖包）。  
> 二者分離：project 主權不吞性格庫；性格庫不綁死單一 run。

---

## 1. 雙庫結構

```text
SETS/PROJ_SHQ_DNA_SYSTEM_01474/lib/
  project_dna/     ← 通用對接權碼副本（優化索引）
  persona_dna/     ← 性格／身份獨立庫
    INDEX.json
    PERSONA_*.json
每個 PROJ_*/PROJECT_DNA.json  ← 該 project 根目錄權威副本
```

---

## 2. PROJECT_DNA（通用）

| 塊 | 義 |
|----|-----|
| **boundary** | empty_mode · outside_basis · FULL_HD · mutex |
| **authority** | AF · claim_max · steal/drift/E |
| **dock** | binds · consumers · harness_preset · **persona_ids** |
| **fingerprints** | keep/empty/hole/summary/dna sha |

外部只認 DNA，不認口頭 PASS。

---

## 3. PERSONA_DNA（獨立性格庫）

| kind | 例 |
|------|-----|
| face | `PERSONA_A8B_STANDARD` |
| character | `PERSONA_HUAN_YA_CLIFF` |
| mecha | `PERSONA_WLF_MECHA_DUAL` |
| custom | `PERSONA_AUDIT_FORCE_SELF`（系統自我審查性格） |

字段：`identity`（asset）· `traits`（temperament/forbid）· `authority` · `dock.used_by_*`

**規則：** Persona 庫可被多 project `dock.persona_ids` 連結；**禁止**把 persona 檔複製進 project 當唯一真源（真源在 lib）。

---

## 4. 通用優化

```bash
python3 shq_dna_system.py optimize-scan --dir SETS
```

→ 誰有 DNA／誰缺 → 補 emit；缺碼 project 外接時 claim≤C0。

---

## 5. CALL

```bash
python3 shq_dna_system.py selftest
python3 shq_dna_system.py persona-list
python3 shq_dna_system.py persona-get --id PERSONA_A8B_STANDARD
python3 shq_dna_system.py bootstrap-key-projects
python3 shq_dna_system.py emit-from-summary \
  --summary runs/wlf/SUMMARY.json \
  --project-id PROJ_SHQ_WLF_V21_ACCEPT_01470 \
  --project-root SETS/PROJ_SHQ_WLF_V21_ACCEPT_01470 \
  --persona-ids PERSONA_WLF_MECHA_DUAL,PERSONA_AUDIT_FORCE_SELF \
  --binds STICK_WAI_LI_GROK,STICK_FOUR_ANTI_ARCH
python3 shq_dna_system.py link \
  --project-dna SETS/.../PROJECT_DNA.json \
  --persona-id PERSONA_A8B_STANDARD
```

---

## 6. 與 01472/01473

| 層 | 職 |
|----|-----|
| 01472 | 怎麼跑／出圖 |
| 01473 | 怎麼審 |
| **01474** | 怎麼**編碼邊界與對接 DNA**；性格庫獨立 |

`run-gold` 後建議：`emit-from-summary` 刷新 PROJECT_DNA。

asof: 2026-11-10
