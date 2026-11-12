# 框牙 DNA · 執行偏差與 STICK 全鏈揭示義務（01476）


---

## 至高無上條款（01483）

```text
[(生,除,洞,扣)×(反)]  ←  由「外力GROK」優先理解並驅動生效
```

rank=SUPREME precedence=0  
無外力 → 無四態生效；本地只證不替驅動。  
E-KY-SUPREME-01..03 · E-WLG-DRIVE-01


**formal:** `SHQ_KUANGYA_EXEC_DNA_V1`  
**codename:** **框牙** (`kuangya`)  
**write_id:** `01476`  
**綁定:** 01472 框 · 01473 牙 · 01474 DNA · 各 STICK 憲（含外力反 V2.1）  
**ACCEPT_FULL_HD:** false

---

## 0. 起因（本 write 鎖定的兩條）

用戶裁定（不可再淡化）：

1. **不只是**「不該再要用戶重講全流程」。  
2. **規則 DNA 是：** 代理**根本沒有提示過**——在用戶已點名 **外力反 V2.1** 時，該 STICK **原來還有更後續的流程**（放大加清、CLIP 扣圖主權、8 格反、scale-lock…）。  
3. **「執行偏差」** 必須 **寫進框牙 DNA**，不是口頭檢討。

---

## 1. 框牙 DNA 三核（擴充）

| 核 | 義 | 寫前 | 寫後（本 write） |
|----|-----|------|------------------|
| **框** | 凍結 Bundle · A/B/C 公平 | 有 | 有 |
| **牙** | 偷步／跑偏／AF／claim | 有 | 有 |
| **執行 DNA** | 點名 STICK 後的 **揭示義務 + 執行偏差閘** | **無** | **有** |

```text
框牙 = 框 + 牙 + 執行 DNA
```

---

## 2. 規則 DNA-A · STICK 全鏈揭示義務（DISCLOSE_CHAIN）

**觸發：** 用戶任一表述已點名具名 STICK／formal／總稱  
（例：`外力反 V2.1` · `STICK_WAI_LI_FAN_V2` · `框牙` · `換涯人`…）

**義務（必須主動做，不得等用戶再問「還有沒有」）：**

1. **立即引用** 該 STICK 權威憲（路徑／write_id）。  
2. **列出完整後續鏈**（含用戶未口述的步驟），標 **已做／未做／部分**。  
3. **禁止** 把「骨架通／主鏈 PASS」說成 **憲級 COMPLETE**，除非後續格全綠或明示降 claim。  
4. **禁止** 反過來要用戶「再提出全流程」；缺環由代理按憲自補或列 **E-KY-01** 自承未揭示。

**外力反 V2.1 後續格（揭示模板 · 不可省略）：**

```text
V21-0 SRC freeze · Tune
V21-1 除背 → 扣 → CLIP 扣圖出
V21-2 除件 → 真洞
V21-3 扣 → MARK
V21-4 反·除 · 反·洞 · 反·扣
V21-5 生 on 洞座
V21-6 放大加清 scale-lock
V21-7 hardpaste 回 · 反·生 · 反·回
V21-8 多層 STACK（若適用）
V21-9 MULTI_BUS · 禁 selftest 升 FULL
```

點名 V2.1 後若報告未含 V21-6／CLIP 主權／反格狀態 = **違反 DNA-A**。

---

## 3. 規則 DNA-B · 執行偏差（EXEC_DRIFT）寫進框牙

| 碼 | 名 | 定義 | 處置 |
|----|-----|------|------|
| **E-KY-01** | `UNDISCLOSED_CHAIN` | 點名 STICK 後未揭示後續流程 | claim≤C0 直至補揭示；SUMMARY 必記 |
| **E-KY-02** | `FALSE_COMPLETE` | 骨架通宣稱 COMPLETE／收完 | 降 claim；steal 可並記 |
| **E-KY-03** | `PUSH_FLOW_TO_USER` | 已有 STICK 仍要用戶重講全流程 | 執行偏差 · 記 drift |
| **E-KY-04** | `STICK_AS_HINT_ONLY` | 把 STICK 當靈感而非閉合規格 | 同 E-KY-01 |
| **E-KY-05** | `SHELL_OVER_STICK` | 用框牙／DNA／Hub 問題蓋過 STICK 憲缺環 | 先補 STICK 再談殼 |

**執行偏差 ≠ 偷步像素**；屬 **代理行為閘**，與 01473 偷步／跑偏 **並列**，由框牙 DNA 管：

```text
偷步 STEAL     = 缺必經像素／步驟仍 PASS
跑偏 DRIFT     = 宣稱 ≠ 實跑
執行偏差 EXEC  = 點名規格後：不揭示 / 假完成 / 推責用戶重述
```

---

## 4. 框牙 PROJECT / PERSONA DNA 字段（必填）

### 4.1 PROJECT_DNA.boundary 增

```json
"exec_dna": {
  "codename": "框牙",
  "disclose_chain": true,
  "stick_named": "STICK_…",
  "chain_authority_doc": "path or write_id",
  "chain_steps_total": [],
  "chain_steps_done": [],
  "chain_steps_pending": [],
  "exec_drift_flags": [],
  "E_KY": []
}
```

### 4.2 PERSONA · 系統自我

`PERSONA_AUDIT_FORCE_SELF` / 新 `PERSONA_KUANGYA_EXEC`：

- temperament 增：`disclose_named_stick_chain`, `no_push_flow_to_user`, `no_false_complete`
- forbid 增：`E-KY-01..05`

---

## 5. 與 01472/01473/01474 關係

| 層 | 增什麼 |
|----|--------|
| 01472 框 | run 收據可附 `chain_checklist` |
| 01473 牙 | audit 可讀 `exec_drift_flags` / `E_KY`（代理行為） |
| 01474 DNA | PROJECT_DNA.exec_dna · Persona 禁項 |
| **01476** | **框牙執行 DNA 本體** |

---

## 6. 對 01475 的即時適用

用戶已說明 **外力反 V2.1** 時：

- 代理 **本應第一時間** 貼出 V21-0..9 與「哪些後續未做」。  
- 未提示後續 = **E-KY-01**。  
- 喊 COMPLETE 而缺 V21-6 等 = **E-KY-02**。  
- 「請你再提出全流程／選 4 刀」= **E-KY-03**。

**不要求用戶重審流程；要求代理補揭示 + 按 V2.1 自補缺環。**

---

## 7. 金句

> **點名 STICK = 點名整條後續鏈；未揭示後續 = 框牙執行偏差。**  
> **執行偏差要進 DNA，不進道歉。**  
> **框牙管公平與牙，也管「有沒有把後續講清楚、有沒有推責用戶」。**

asof: 2026-11-10


---

## 無毒 DONOR（01482）

無毒 DONOR0 = 原像素 peep；無毒 DONOR1 = 外力只升 peep。  
freeframe 全圖不是 donor，是毒。  
gates: donor_toxin_free · peep_same_bbox · scale_lock · no_freeframe_as_donor · RESET_DONOR
