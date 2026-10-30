# §0.12.45 補擋全機（OCCLU-COMPLETE / ASC · Amodal Solo Complete）
# asof 2026-10-30T18:35:44Z

> **正名：補擋全機** · **短碼 OCCLU-COMPLETE / ASC** · **英** Amodal Solo Complete  
> **族：** OBA §0.12.44 **旁系技能**（補遮擋肢體；落地仍走 OBA 鐵序）  
> **試錯：** `OBA_LEGO_FAILURE_RECORD.md`（E-ASC-01..06 · E-OBA-23）  
> **樣板：** BATTLE6 C 履帶 `ccdec01e` · 變體 `7344994c` · 落地 `SETS/OBA_BATTLE6_MECH/COMPLETE`  
> **禁當：** 母像素真源 · 3D 透視還原

---

## 0.12.45.A 一句

用 **可見 peep 殘形（VER.1）** 生全形（VER.2）→ **反補回 1 之全形同動作（1A）** → **只貼 1A** → peep 量 s≤1 → 遠→近一次一件（**殘相轉生 §0.12.46**）。

---

## 0.12.45.B 地位

| | |
|--|--|
| **相對 peep-LOCK** | peep-LOCK 咬母像素（Δ≈4）· **唔補** 真被擋；ASC **補肢**（Δ↑）再貼序還遮擋 |
| **相對 OBA 主鐵序** | ASC 只擴 **T7 GEN** 與 **T9 閘**（recall 代 IoU 形配）；T0–T6、T8、T10 不變 |
| **非法** | 把 ASC cut 當「母真形」寫入 peep 真源 · 無 peep 量直接全畫布貼 · batch 六機一次 complete |

---

## 0.12.45.C 技能說明 · 點解能自動補不見／被擋肢體

四層（由硬到軟 · **入憲必記**）：

### A. 訓練先驗 · Amodal prior
擴散／圖生圖見過海量完整物件。  
輸入**殘缺輪廓 + 局部紋理** → 機率質量流向完整對稱機體（完形補全 amodal completion）。

### B. 條件鎖形 · shape-cond
OBA peep／shape_pad 提供可見 silhouette、局部 LEGO 紋、大致姿。  
模型沿殘形**外推填洞**，非憑空亂生。

### C. Prompt 指令 · explicit completion
鐵句必須含：
```
Complete FULL unoccluded solo figure
reconstruct any missing/blocked limbs
remove every other mech fragment
pure solid black seamless background
```
= 去遮擋 + 補肢 + 隔離；**禁止**場內 inpaint 留鄰機。

### D. 隔離棚拍 · solo black
去掉鄰機／火花／地面 → 模型只服務「一件商品全身照」先驗 → 手、腿、履帶尾更易補齊。

```
母場遮擋          peep 殘形              ASC solo
[A拳蓋C]    →   [C 半截履帶]    →   [完整C ± 想像肢]
                 ↑ mask+shape_pad        ↑ i2i complete
```

**誠實：** 多生出嚟嘅手臂（如 `7344994c`）係 **prior 想像**，**唔係** 母圖隱藏像素。

---

## 0.12.45.D 鐵序（嵌 OBA）

```
T_asc0  peep 殘形（母 RGB + mask · 可含遮擋缺口）      ← OBA T4–T6
T_asc1  shape_pad 黑底
T_asc1b emit REF 綠 peep on black ＝ 母原本動作（OBA .M）
T_asc2  VER.2 = i2i OCCLU-COMPLETE FROM VER.1（生全形 · 中間 · 禁直貼）  ← RRT V2
T_asc2b VER.1A = 反補（body←2 · action_lock←1 · 動作不變）     ← RRT V3 · **最終 cut**
T_asc3  hard α 退地 cut **只取 1A**
T_asc4  peep 量 s≤1 · 腳錨 · GATE recall(peep⊂1A)≥0.4
T_asc5  遠→近 **只貼 1A** + STEP（1｜2｜1A｜accum）  ← OBA .N · RRT
T_asc6  semi 綠peep vs 紅complete · ALL_STEPS · AUDIT_COMPLETE.json
```

**禁跳：** 無 peep 量 · 無遠近序 · 無 hard α · 無 recall 閘。

---

## 0.12.45.E 三律（硬）

1. **假肢標籤** — ASC 輸出必標 `COMPLETE_IMAGINED` · 母 peep 仍係幾何真源  
2. **peep 獨規** — s 只 peep_h/w · s≤1 · 禁 cut upscale  
3. **一人一刀 + 遮擋序** — 遠→近；低 recall **只重該 STEP**

---

## 0.12.45.F 閘門

| 閘 | 通過 |
|----|------|
| hard α · 無地無鄰機 | cut RGBA |
| s≤1 · 來源 peep | audit |
| recall peep≥0.4（建議≥0.55） | peep 像素被 paste 覆蓋 |
| spill≈0 | 無大溢出 peep 擴 bbox |
| 遠→近 foot 序 | B→D→C→F→A→E 類 |
| 半透自審 | 綠 peep 邊 vs 紅 complete |

---

## 0.12.45.G 一刀參數卡

```
MODE=OCCLU_COMPLETE_ASC
SECTION=0.12.45
INPUT=peep|shape_pad (occluded ok)
PROMPT=full unoccluded solo + reconstruct blocked limbs + no other mechs + black bg
OUT=hard_alpha_cut
SCALE=peep_only s<=1 LANCZOS
PLACE=foot+cx
GATE=recall_peep>=0.4 spill=0
ORDER=foot_y asc far_to_near
AUDIT=semi+strip+AUDIT_COMPLETE.json
TAG=COMPLETE_IMAGINED|OCCLU_COMPLETE_SHAPECOND
REF=green_peep_original_pose
HD_FROM=REF_only
STEP_AUDIT=REF|HD|accum
BAN=claim_true_hidden_pixels, mother_as_base, batch, s>1, skip_peep_scale, use_ASC_as_peep_truth, free_asc_without_ref, batch_complete_paste
FAIL→ redo single STEP only
RECORD=OBA_LEGO_FAILURE_RECORD.md
SAMPLE=SETS/OBA_BATTLE6_MECH/COMPLETE
```

---

## 0.12.45.H 錯成（E-ASC）

| ID | 禁 |
|----|-----|
| **E-ASC-01** | 把 ASC 肢體當母真像素／寫入 peep 真源 |
| **E-ASC-02** | 場內 inpaint 留鄰機 · 唔做 solo black |
| **E-ASC-03** | 無 peep 量 · 全畫布自由貼 complete |
| **E-ASC-04** | batch 多機一次 complete 再一次貼 |
| **E-ASC-05** | 用 IoU 形配硬閘 ASC（應 recall；形必大於 peep） |
| **E-ASC-06** | 無遠→近序 · 後排蓋前排 |
| **E-ASC-07** | **ASC 無 REF 綠 peep 同姿** · 自由棚拍補肢 |
| **E-ASC-08** | **只交 VER.2 complete 當貼** · 無反補 1A 同動作 |
| **E-OBA-23** | 混淆 peep-LOCK 與 ASC（用 Δ 解讀錯） |
| **E-OBA-25..27** | 見 OBA .M（batch 貼／缺線對看／無 REF） |

---

## 0.12.45.I 樣板路徑

| | |
|--|--|
| 母 | b1326837 · `SETS/OBA_SCAN_B132/MOTHER.jpg` |
| peep 殘 | `OBA_SCAN_B132/peep/*` |
| ASC C | asset `ccdec01e-755a-4aa5-8403-5474391344ce` · `COMPLETE/hd/C_COMPLETE.jpg` |
| 變體多肢 | asset `7344994c-8436-49ee-9f3a-8a36ef3ee992` |
| 落地 FINAL | `SETS/OBA_BATTLE6_MECH/COMPLETE/FINAL_COMPLETE_OBA.jpg` |
| 序 | B→D→C→F→A→E |
| 說明全文 | `OCCLU_COMPLETE_ASC.md`（本節為入憲正文） |

---

## 0.12.45.J 連動

- 主路 peep-LOCK 仍優先於「要咬母形」時  
- 要肢體完整／可再戰姿 → 開 ASC 分支  
- 可後嵌 SWP／GOU 升清 ASC cut · 再 OBA 貼  
- MLR 母光 · VOID 繼承不變  
- **OBA .M 強制：** REF 原本動作 · 一次一件 · STEP 線對看（E-ASC-07 / E-OBA-25..27）

---

*END §0.12.45 · 補擋全機 / OCCLU-COMPLETE / ASC · + REF 同姿 · asof 2026-10-30T18:30:45Z*

---

## ASC × OBA .M 嵌接（asof 2026-10-30T18:26:00Z · 入憲）

ASC 補擋 **仍受** §0.12.44.**M** 約束：

```
每件：母 peep 綠描 REF（原本動作）
  → OCCLU-COMPLETE i2i from REF（同姿 · 禁自由棚拍）
  → peep s≤1 腳／心錨
  → **一次一件** 遠→近累貼
  → STEP 線對看自審（REF｜HD complete｜accum）
```

| TAG | 用法 |
|-----|------|
| `COMPLETE_IMAGINED` | 自由補全（舊） |
| `OCCLU_COMPLETE_SHAPECOND` | **f168／.M 正路** · REF shape-cond 同姿 |

禁：E-OBA-25/26/27 對 ASC 同樣生效 · 禁 batch ASC 無 STEP。
