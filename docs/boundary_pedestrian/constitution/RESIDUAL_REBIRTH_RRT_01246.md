# §0.12.46 殘相轉生（RESIDUAL REBIRTH / RRT）
# asof 2026-10-30T18:35:44Z

> **正名：殘相轉生** · **短碼 RRT** · **英** Residual Rebirth / Residual-Form Transmigration  
> **族：** OBA §0.12.44 · ASC §0.12.45 **鐵嵌子技**（每物件 HD 必走 · 最終只貼 1A）  
> **試錯：** `OBA_LEGO_FAILURE_RECORD.md`（E-RRT-01..06 · E-ASC-08 · E-OBA-25/27）  
> **用戶鐵句（verbatim · 重要）：**  
> 並會在每物件都出一 REF 出來的圖去**補**那物件「原本」的動作  
> — 注意是**最後仍是用物件的 VER.1A**，即  
> **1(原) → 2(生全形) → 3(反補出1的全形,但動作不變) → 1A (1的沒被擋的相同動作)**

---

## 0.12.46.A 一句

**殘相（1）** 鎖原本動作 → **生全形（2）** 補被擋肢 → **反補（3）** 用全形知識**回寫**成「1 的全形但動作不變」→ 得 **1A** → **只貼 1A**（唔貼 2）。

```
VER.1   原     = peep 殘相／REF · 母原本動作 · 可被擋
VER.2   生全形 = amodal complete 全形（中間產 · 可能姿漂）
VER.3   反補   = 以 1 動作為鎖 · 反補出「1 之全形」· 動作不變
VER.1A  落地   = 1 的**沒被擋**相同動作 · **最終 paste 唯一合法 cut**
```

**關鍵：** 最後落地 **仍是 1 的動作版本**（1A）· **唔係** 2 的自由全形棚拍。

---

## 0.12.46.B 地位

| 與 | 關係 |
|----|------|
| OBA .M REF | VER.1 ＝ REF 綠 peep 原本動作板 |
| ASC §0.12.45 | VER.2 ＝ ASC 生全形；**不足** → 必須再走 3→1A |
| peep-LOCK | 可跳 2–3 只貼 1（不補擋）· 一開補擋必走殘相轉生 |
| 線對看 | STEP 可擴四格：1｜2｜1A｜accum · 或 1｜1A｜accum |

**非法：** 用 VER.2 當最終貼（E-RRT-01）· 反補改動作（E-RRT-02）· 無 1 直接生 2（E-RRT-03）。

---

## 0.12.46.C 鐵序（每物件 · 不可顛倒）

```
V1  emit VER.1 = 母 peep 殘相 + 綠 2px stroke on black
    = REF_ORIGINAL_POSE · 鎖「原本動作」
    落碟：REF/L_VER1_ORIGINAL.jpg

V2  VER.2 = i2i OCCLU-COMPLETE FROM VER.1
    = 生全形 · 補被擋肢 · solo black
    落碟：hd/L_VER2_FULL_BODY.jpg
    TAG 暫：COMPLETE_MID（中間產 · 禁直接貼）

V3  VER.3 / 1A 反補：
    條件雙鎖：
      · shape / detail 可來自 VER.2（全形知識）
      · **動作／姿 必須鎖死 VER.1**（原本動作不變）
    作法（擇一 · 可疊）：
      a. i2i：主圖 VER.1 · ref VER.2 · prompt「complete occluded limbs only · keep EXACT pose/action of first image」
      b. i2i：主圖 VER.2 · ref VER.1 · prompt「match pose/action of second image exactly · keep full unoccluded body」
      c. 像素：VER.1 可見區硬鎖 + VER.2 只填 peep 缺口（inpaint mask=缺失）
    落碟：hd/L_VER1A_FULL_SAME_ACTION.jpg
    TAG 終：`VER1A_SAME_ACTION` / `OCCLU_COMPLETE_SHAPECOND`

V4  hard α 退地 cut **只取 1A**
V5  peep 量 s≤1 · 腳／心錨 · recall(peep⊂1A)≥0.4
V6  **只貼 1A** 入 accum · STEP 線對看 · 過閘先下件
```

**交付禁：** 把 VER.2 當 paste cut（E-RRT-01）。  
**FAIL：** 只重該件 V1–V6 · 唔重全場。

---

## 0.12.46.D 三律（硬）

1. **1A 唯一落地** — paste cut **必須** VER.1A · 禁 VER.2 直貼（E-RRT-01）  
2. **動作鎖 1** — 反補／1A 動作 **＝ VER.1 原本** · 禁換姿棚拍（E-RRT-02 · E-OBA-25）  
3. **2 只係中間** — VER.2 可姿漂 · 只供全形知識 · 必經 3 反補回 1 動作（E-RRT-04）

---

## 0.12.46.E 圖示

```
母場遮擋              VER.1 殘相              VER.2 全形(中)
[拳蓋履帶]  →  [半截機 · 原姿]  →  [全身機 ±姿漂]
                      ↑ peep+綠描              ↑ ASC complete
                            \                    |
                             \    VER.3 反補     |
                              \   動作鎖1        v
                               `→ [全身機 · 原姿] = VER.1A
                                        ↓
                                 paste 1A only → accum
```

---

## 0.12.46.F 線對看（mandatory 擴）

| 格 | 內容 | 色 |
|----|------|-----|
| 1 | VER.1 REF 殘相 · 原本動作 | 綠 |
| 2 | VER.2 生全形（中間 · 可標 MID） | 黃 |
| 3 | **VER.1A** 全形同動作（落地 cut） | 青 |
| 4 | accum 加此件 | 紅 |

最少三格亦可：`1｜1A｜accum` · 但 audit 必須存 VER.2 檔備查。

半透終審：綠 peep 邊 vs 紅 **1A** paste 邊。

---

## 0.12.46.G 一刀參數卡

```
MODE=RESIDUAL_REBIRTH_RRT
SECTION=0.12.46
CHAIN=1_ORIGINAL → 2_FULL_BODY → 3_REVERSE_FILL → 1A_SAME_ACTION
VER1=peep_green_stroke ORIGINAL_ACTION
VER2=i2i_complete FROM_VER1 TAG=COMPLETE_MID BAN_paste
VER3=reverse_fill action_lock=VER1 body_from=VER2
VER1A=unoccluded_same_action FINAL_CUT
PASTE=VER1A_only
SCALE=peep_only s<=1
GATE=recall_peep_in_1A>=0.4
STEP=1|2|1A|accum or 1|1A|accum
TAG_FINAL=VER1A_SAME_ACTION
BAN=paste_ver2, action_drift_in_1A, skip_ver1, skip_reverse,
    free_studio, batch_without_1A
FAIL→ redo single unit chain only
RECORD=OBA_LEGO_FAILURE_RECORD.md
NEST=OBA.M + ASC.0.12.45
```

---

## 0.12.46.H 錯成（E-RRT）

| ID | 禁 |
|----|-----|
| **E-RRT-01** | **用 VER.2 當最終貼** · 跳過反補／1A |
| **E-RRT-02** | 反補／1A **改動作** · 脫離 VER.1 原本姿 |
| **E-RRT-03** | 無 VER.1 · 直接自由生全形 |
| **E-RRT-04** | 把 VER.2 標成 final TAG · 當母真形 |
| **E-RRT-05** | 反補無雙鎖（無 1 動作 或 無 2 全形） |
| **E-RRT-06** | 鏈未落碟 · 無 VER1/2/1A 檔 · 無法線對看 |
| **E-ASC-08** | ASC 只交 complete(2) · 無 1A 同動作落地 |
| **E-OBA-25** | 無 REF/VER.1 棚拍（連碼） |

---

## 0.12.46.I 與 OBA／ASC 嵌點

```
OBA T7  REF     = VER.1
OBA T7b HD 鏈   = VER.2 → VER.3 → VER.1A   ← 殘相轉生
OBA T9  paste   = **只 1A**
ASC T_asc2      = VER.2 only（中）
ASC 擴          = 必加 V3→1A 先貼
```

**ASC 舊路「complete 即貼」升格為非法（E-ASC-08）** · 除非 peep-LOCK 不補擋。

---

## 0.12.46.J 樣板／命名

| | |
|--|--|
| 正名檔 | `RESIDUAL_REBIRTH_RRT_01246.md`（本節） |
| 名卡 | `RESIDUAL_REBIRTH_RRT_NAME.md` |
| 禁表 | `RESIDUAL_REBIRTH_RRT_DO_NOT_REPEAT.md` |
| 嵌主憲 | OBA §0.12.44.**N** · ASC §0.12.45.**K** |
| 路徑例 | `…/RRT/L_VER1.jpg` · `L_VER2_FULL.jpg` · `L_VER1A.jpg` |

---

*END §0.12.46 · 殘相轉生 / RRT · 1→2→3→1A · asof 2026-10-30T18:35:44Z*


---

## 0.12.46.K 聯動 OBA · 回母 VOID（asof 2026-10-30T18:54:59Z）

殘相轉生產出 **1A** 之後：

```
accum 底 = 母 VOID（唔係母）
paste   = 1A only
STEP 右格 = VOID 累積（金樣 66a6568a）
```

全序見 `OBA_RRT_LINK_RETURN_MOTHER_VOID.md` · OBA **.O**。
