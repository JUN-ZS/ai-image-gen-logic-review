# §0.12.44 一人累貼（ONE_BY_ONE_ACCUMULATE / OBA · **LOCK 終極版 + 優化**）
# asof 2026-10-30T18:35:44Z

> **正名：一人累貼** · **短碼 OBA** · **英** One-By-one Accumulate  
> **試錯源：** `OBA_LEGO_FAILURE_RECORD.md`（**E-OBA-01..27** · E-ASC）  
> **樣板：** minifig `99f4368d` · robots `OBA_v2_SCAN` · **BATTLE6** `OBA_SCAN_B132` · **MIX** `OBA_MIX_ROBOT_SHIP/ONE_BY_ONE`  
> **家族：** MLR 母光重鋪 · **OBA＝多物件落地鐵序**  
> **優化入憲：** 黃線格號法（f168）· 母形咬回 · **REF／線對看（.M）** · **殘相轉生 1→2→3→1A（.N · §0.12.46）** · ASC 旁系 §0.12.45

---

## 0.12.44.A 一句

母只出 **位／形／光** → **母圖 VOID** 空台 → **掃瞄綠描邊 peep** → 黃 GRID **座標**（≠人）→ **每件先出 REF（綠 peep＝母原本動作）** → **殘相轉生 1→2→3→1A**（最終貼 **1A** 同動作全形）→ **一次只加一件** peep s≤1 累貼 → **STEP 線對看自審** → 過閘先下一件。

**母必須真用：** 位＋**形／姿 peep** 皆咬母；禁「只 VOID+框 · HD 棚拍另生」（E-OBA-24 有位無形）。  
**重要：** REF **唔係裝飾** · 係 **用嚟生嗰件「原本動作」嘅條件圖**（E-OBA-25/26）。

---

## 0.12.44.B 地位

| 族 | 關係 |
|----|------|
| **MLR** 母光重鋪 | OBA 係其 **多物件落地招**（VOID＋絕對位） |
| GOU／MSR | 管單幀紋理／宏圖 · **不管** 多件絕對位累貼 |
| SWP 升紋金字塔 | 可嵌單件升清 · **之後** 再 OBA 貼 |
| ASC §0.12.45 | 補擋肢體旁系 · 仍走 **REF→HD→一次一件→線對看** · TAG=`COMPLETE_IMAGINED` 或 `OCCLU_COMPLETE_SHAPECOND` |
| HTFC | 時間追尾 · 非本招 |

**非法：** 無 SCAN 鏈嘅「十 HD 一次貼」＝ demo · **唔入 LOCK 成果**（E-OBA-10）。  
**非法：** 最新母只供 VOID+box · HD 無同姿 → **有位無形**（E-OBA-24）。  
**非法：** 無 REF · 自由棚拍 HD · 或 batch 生晒再一齊貼 · 無逐步 STEP 自審（**E-OBA-25/26/27**）。

---

## 0.12.44.C 鐵序（不可顛倒 · 不可 batch）

```
T0  母圖 GEN／選定（最新母必須登記 asset · 全鏈只用此母）
T1  母圖 VOID（重 PROMPT 無人／無物 · 同幅同光 · cover_fit 母）
T2  黃 GRID 劃座標格（格號 1..N · 只座標 · 不是人）     ← .K 黃線格號法
T3  人／機 字母冊 A..（≠格號 · UUID 亦可）
T4  每人獨立：solo crop → rembg + 魔法棒 → peep mask（VORONOI 互斥）
    peep RGB 必取母圖 · mask 可用 mother−VOID diff（E-OBA-21）
T5  綠描邊 stroke（findContours · 2px · 禁 fill 框）
T6  peep 量：peep_w/h · peep_cx · peep_foot · cell occupancy（只註冊 · 永不入 s）
T7  **每件出 REF**（綠 peep 板 · 鎖母「原本動作／姿」）
    · REF 路徑必落碟 · 必登記 · 必入 STEP 左格
T7b **殘相轉生**（§0.12.46 · **.N**）· 禁無 REF 自由棚拍（E-OBA-25）
    VER.1 = REF 殘相原本動作
    VER.2 = 生全形（ASC complete · 中間 · 禁直貼）
    VER.3 = 反補「1 之全形 · 動作不變」
    VER.1A = 1 的沒被擋相同動作 · **唯一 paste cut**
    · 姿脫鉤 → 重該件鏈 · 或 peep 過閘（E-OBA-12/24 · E-RRT-02）
T8  遠→近 排序（peep_foot 升序）
T9  **一次一件**（禁 batch 貼）：
      s = min(peep_h/cut_h, peep_w/cut_w, 1.0)   # 禁格邊長 · 禁 s>1
      腳錨 peep_foot + peep_cx
      IoU 微搜對 peep mask（LOCK 建議 ≥0.55 · 前排 ≥0.75）
      只貼 **當前這一件之 VER.1A** 入 accum（VOID 起步 · 禁貼 VER.2）
      spill 閘
T9b **STEP 線對看自審**（mandatory · 每件必出）：
      三／四格 = [VER.1 REF 原] | [VER.2 全形MID 可選] | [VER.1A 同動作全形] | [accum]
      半透 綠 peep 邊 vs 紅 paste 邊
      過閘 → 先下一件；低 IoU **只重該 STEP**
T10 全齊 · GRID+綠邊+字母 overlay · audit JSON · 全 STEP strips 蒙太奇
    · 母形咬回核：mean|mother−final| 或 peep IoU 自審
    · 線對看板上必齊：母 GRID、彩 peep map、SEMI 綠vs紅
```

**禁跳：** T4–T6 掃瞄 · **T7 REF** · **T7b 用 REF 生** · **T9 單件** · **T9b 線對看**。

---

## 0.12.44.D 三律（硬）→ 五律

1. **格人脫鉤** — 黃 GRID 數字 **只係座標** · **唔係人**；s **永不** 跟格邊長（E-OBA-02/14 · **.K**）  
2. **peep 獨規** — s 只來自 peep_h/w · PIXEL 庫 cut 只可縮（E-OBA-04/09/15）  
3. **一人一刀** — 禁 batch；低 IoU **只重該 STEP**（E-OBA-01/10/12）  
4. **母形咬回** — 最新母必須供 **位+形+姿**；禁只 VOID+框（E-OBA-24 · **.L**）  
5. **REF 原本動作** — 每件必出 REF · HD 必由 REF 生 · 一次加一件 · 每件 STEP 線對看（**E-OBA-25/26/27 · .M**）
6. **殘相轉生** — 1→2→3→**1A** · **只貼 1A** · 禁貼 2 · 1A 動作＝1（**E-RRT-01..06 · .N**）

---

## 0.12.44.E 掃瞄對位（終極硬條件）

| 件 | 要 |
|----|----|
| rembg + floodFill 魔法棒 · 或 mother−VOID+Voronoi | 獨立 peep |
| peep RGB＝母像素 | 禁 diff 當地紋當 RGB（E-OBA-21） |
| 綠 stroke | 描邊 only（禁 fill 大框 · E-OBA-06） |
| 黃 GRID on 母 **與** VOID | 同座標繼承 · **格號≠人** |
| **REF 板** | 每件綠 peep · 鎖原本動作 · 落碟 |
| **HD from REF** | i2i shape-cond · 禁無 REF 棚拍 |
| **一次一件 accum** | VOID→+A→+B… · 每步存檔 |
| 半透 peep綠 vs paste紅 | 邊對邊自審 |
| **STEP 三格** | REF｜HD｜accum + s/IoU 文案 |
| IoU / spill | 建議 IoU≥0.55 · 前排≥0.75 |
| 退地 hard α | extract／退背 · 禁軟 crop 帶地 |
| shape-cond 同姿 或 peep 過閘 | 禁純棚拍另生（E-OBA-12/24/25） |

無上表 → **非法 OBA**（E-OBA-10）· 級別＝`ILLEGAL_OBA_DEMO`。

---

## 0.12.44.F 解毒

### F1 · E-OBA-13 clean 層層
```
裸 peep 重貼 · 解毒一刀
  = 只 母 peep 量 + 原生 HD cut + VOID
  · 零 clean 鏈 · 零 OLD MASK · 零 α∩feather 主路
```

### F2 · E-OBA-24 有位無形（最新母「沒用到」）
```
OBA-SCAN 重跑鐵序（BATTLE6 治本）
  1. 每人 solo crop → rembg／wand → 綠 2px stroke peep（禁 fill 框）
  2. 黃 GRID 母＋VOID 同繼承 · 格號只座標
  3. 每件 REF → HD shape-cond 同姿 · 退地
     · 失敗 → peep RGB 過閘（IoU=1.0）優先於假 HD
  4. 一次一件 · peep s≤1 · IoU≥0.55 · STEP 線對看 · 半透綠vs紅
  5. 過閘才入 LOCK 樣
```

### F3 · E-OBA-25/26/27 無 REF／batch／無線對看
```
治本鐵序（金樣人仔 verbatim 重要）
  1. 每件 peep → 出 REF（綠描 · 母原本動作）
  2. 用 REF 生 HD（i2i · 同姿）
  3. 只貼一件入 accum
  4. 出 STEP 三格線對看自審
  5. 過閘 → 下一件
  禁：batch 生 HD · batch 貼 · 無 REF · 無 STEP
```

單人診斷：先半透疊母 → 通再搬 VOID（海盜 #03 教例）。

---

## 0.12.44.G 一刀參數卡（終極）

```
MODE=OBA_ONE_BY_ONE
MOTHER=<latest_asset>   # 全鏈登記 · 禁偷換舊母
VOID=reprompt_empty cover_fit mother
GRID=2x5|2x6 coords_only   # 格號=座標 only · NEVER person ID
ID=letters A-J|UUID (not grid numbers)
PEEP=rembg+wand|mother-VOID+Voronoi  RGB=mother  VORONOI_excl
STROKE=findContours thickness=2 no_fill
REF=green_peep_plate per_unit ORIGINAL_POSE   # mandatory · 用嚟生 HD
HD=RRT_chain 1→2→3→1A                         # BAN free_studio · BAN paste_ver2
RRT=VER1_REF → VER2_FULL_MID → VER3_REVERSE → VER1A_FINAL
PASTE_CUT=VER1A_only
SCALE=peep_only s<=1 LANCZOS   # BAN grid_edge_scale
ANCHOR=foot+cx
ALIGN=IoU_microsearch >=0.55
ORDER=peep_foot asc
PASTE=one_unit_only_then_audit   # BAN batch_paste
ACCUM=VOID → +unit step files
AUDIT=STEP_strip REF|HD|accum + semi_green_vs_red + grid + peep_map
CUT=extract_hard_alpha
BAN=batch, mother_as_base, s>1, grid_scale, grid_as_person_id,
    old_mask, red_donor, stroke_fill, soft_crop_bg,
    studio_hd_without_REF, void_box_only, no_STEP_strip, batch_then_paste, paste_ver2, skip_rrt_1a
FAIL→ redo single STEP only
RECORD=OBA_LEGO_FAILURE_RECORD.md
```

---

## 0.12.44.H 連動

- 單件升清：可先 SWP／S1HL／GOU／LP2 再 cut 入 OBA  
- 光：VOID 繼承母 IC · 可選 lit_bias  
- 記錄：每跑必寫 audit · 大失敗追加 E-OBA-*  
- MLR 詞彙：母圖VOID · MASK MARK · peep · 格人脫鉤 一律沿用  
- ASC §0.12.45：補擋後仍 peep 量 · 遠→近 · **仍 REF→一次一件→線對看** · 禁假肢當真（E-OBA-23）

---

## 0.12.44.I 樣板路徑

| | |
|--|--|
| minifig | `SETS/IC_LEGO10_MLR/v32_ONE_BY_ONE` · `v31_GRID_FIX` |
| robots **非法** | `…/MOTHER_ROBOTS10/OBA_v1`（E-OBA-10 示範） |
| robots **LOCK** | `…/MOTHER_ROBOTS10/OBA_v2_SCAN` |
| **BATTLE6 LOCK peep** | `SETS/OBA_SCAN_B132`（母 b1326837 · 母形咬回） |
| **BATTLE6 非法粗貼** | 舊 box+棚拍 HD · `ILLEGAL_OBA_DEMO`（E-OBA-10/05/12/24） |
| **BATTLE6 ASC** | `SETS/OBA_BATTLE6_MECH/COMPLETE`（§0.12.45） |
| **MIX ONE_BY_ONE** | `SETS/OBA_MIX_ROBOT_SHIP/ONE_BY_ONE`（REF→STEP 線對看樣） |
| 錯成 | `OBA_LEGO_FAILURE_RECORD.md` |
| 禁表 | `OBA_DO_NOT_REPEAT.md` |
| 黃線格號法 | `OBA_YELLOW_GRID_CELL_LAW.md` |
| 母形咬回 | `OBA_MOTHER_BITE_POSITION_WITHOUT_SHAPE.md` |
| **REF 原本動作法** | `OBA_REF_ORIGINAL_POSE_LINE_ALIGN.md` |
| **殘相轉生** | `RESIDUAL_REBIRTH_RRT_01246.md` · §0.12.46 · **.N** |

---

## 0.12.44.K 黃線 GRID 格號法（f168 優化 · verbatim 入憲）

> **黃線 GRID 中的格的數字是 GRID 的座標，不是人的數字標記；人用其他方法記；格號用錯 → 毒錯人的大小規格。**

| 項 | 法 |
|----|-----|
| **格數字** | ＝ **GRID 平面座標** only（格心標 1..N 或行列號） |
| **不是** | 人／機 的 ID、序號、scale 來源 |
| **人點記** | **字母 A..J** 或 UUID · 掛 peep／REGISTRY · 唔寫入格號 |
| **s 來源** | **只** peep_h／peep_w · **永不** 格邊長、格佔用數 |
| **毒** | 格號當人 → 人大小跟格走 → **毒 scale**（E-OBA-02） |
| **毒** | 跨多格「佔格數」入 s → 被格號放大（E-OBA-14） |
| **自審** | 數字在**格心** · 字母在 **peep** · 二者唔可互換 |
| **禁句** | 「格號就係人號」「跟 GRID 格放大」 |

```
T2  GRID 劃格 · 格號=座標
T3  字母冊   · 人=字母 ≠ 格號
T6  occupancy 只註冊 · 永不入 s
T9  s=peep only · 禁格邊長
```

**連碼：** E-OBA-02 · E-OBA-14 · 三律·1 格人脫鉤 · 參數卡 `GRID=coords_only` `ID=letters` `BAN=grid_scale`

---

## 0.12.44.L 母形咬回法 · 有位無形解毒（BATTLE6 毒審優化）

### 毒症狀（用戶句）
> 「那最新的圖為什麼沒有用到？」

### 毒審卡（分層）

| 層 | 最新母有無用 | 半毒實況 |
|----|-------------|---------|
| 底 | ✓ | 底＝VOID · 非母當底（E-OBA-03 PASS） |
| 位 | △ | 只有**粗 box** 腳錨 · 非綠描邊 peep |
| 形／姿 | ✗ | HD＝**棚拍重 GEN** · 非母同姿 shape-cond |
| 像素 | ✗ | 非母 peep cut · 另一套機身 |

→ 場地／站位像母 · 機身姿像新圖 → **看起來最新互戰圖沒用進去**。

### 違憲碼（BATTLE6 粗貼級）

| 碼 | 判 | 證據 |
|----|-----|------|
| **E-OBA-24** | **FAIL · 有位無形** | 母只供 VOID+box；HD 無同姿；形／姿未咬母 |
| E-OBA-10 | FAIL · 非法 OBA | 無綠 stroke／無 GRID 繼承／無半透／無 IoU |
| E-OBA-05 | FAIL | 只 peep box · 無邊對邊 |
| E-OBA-06 | 半毒 | 綠**框** fill · 非 2px 描邊 |
| E-OBA-12 | FAIL | 母互戰姿 vs HD 棚拍姿 脫鉤 |
| rembg 崩 | 半 | 小件改 box（須 mother−VOID+Voronoi · E-OBA-22） |

**總判級：** `ILLEGAL_OBA_DEMO`（同 robots OBA_v1）· 憲樣板只認 **SCAN LOCK**。

### 根因一句
最新母只被拿來做 **VOID + 框位**；**SCAN 鏈跳空**；HD 另生棚拍再貼 → **有位無形** → 最新圖「沒用到」。

### 治本（入憲強制）
見 **.F2 OBA-SCAN 重跑鐵序** · 過閘才 LOCK。  
**LOCK 核：** peep IoU 過閘 **或** 母 peep 過閘（shape-cond 失敗時）· audit 記 `mother_bite`。

### 與 ASC 邊界
ASC（§0.12.45）**故意** 補想像肢 → Δ↑ · 必須 TAG=`COMPLETE_IMAGINED` 或 `OCCLU_COMPLETE_SHAPECOND`。  
**有位無形** 係**未聲明**嘅假形 → 毒；ASC 係**聲明**補形 → 合法旁系。

---

## 0.12.44.M REF 原本動作法 · 一次一件 · 線對看自審（**重要 · 金樣人仔入憲**）

### 用戶句（verbatim）
> 而且他是一次一次加物件入圖啊, 每次都對位自審, 並會在每物件都出一REF出來的圖去蛹那物件「原本」的動作 — **重要**

### 法（LOCK）

| 項 | 法 |
|----|-----|
| **一次一件** | VOID 起步 · 每輪只 paste **一件** · 存 `accum/NN_AFTER_L.jpg` |
| **每物件出 REF** | 綠描 peep 板 = 母 peep **原本動作／姿** · 落碟 `REF/L_REF_ORIGINAL_POSE.jpg` |
| **用 REF 蛹／生** | HD **必須** i2i from REF · shape-cond 同姿 · **禁**無 REF 自由棚拍 |
| **每次對位自審** | STEP 三格 **mandatory**：`REF peep 原本動作` \| `HD from REF` \| `accum +L` + s/recall/spill |
| **線對看** | 半透綠 peep 邊 vs 紅 paste 邊 · 母 GRID+字母 · 彩 peep map · 全 STEP 蒙太奇 |
| **過閘** | 該件 pass → 先下一件 · fail → **只重該 STEP** |

### 鐵序一刀
```
for L in far→near:
  1. emit REF(L)           # 綠 peep = 母原本動作
  2. HD = i2i_from_REF(L)  # 蛹同姿
  3. cut · peep s≤1 · paste ONE onto accum
  4. STEP 線對看自審
  5. pass → next L
```

### 毒碼
| 碼 | 文 |
|----|-----|
| **E-OBA-25** | 無 REF 或 HD 非由 REF 生 · 自由棚拍（脫離原本動作） |
| **E-OBA-26** | batch 生 HD 再一齊貼 · 非一次一件 |
| **E-OBA-27** | 無 STEP 線對看自審 · 只交 final／圖冊 |

### 與舊 T7/T9 關係
- 舊「獨立 GEN HD」**升格**為 **T7 REF + T7b 用 REF 生**  
- 舊「一人一刀」**升格**為 **T9 貼一件 + T9b 線對看**  
- 金樣人仔 STEP 板 = 本節 **mandatory 產物** · 唔係可選 audit

### 樣
`SETS/OBA_MIX_ROBOT_SHIP/ONE_BY_ONE/` · minifig 金樣 STEP 三格

---


---

## 0.12.44.N 殘相轉生（RRT · §0.12.46 · **重要**）

> **verbatim：** 最後仍是用物件的 **VER.1A**，即  
> **1(原) → 2(生全形) → 3(反補出1的全形,但動作不變) → 1A (1的沒被擋的相同動作)**

| VER | 名 | 用途 |
|-----|-----|------|
| **1** | 原 | peep 殘相 REF · 母原本動作 · 可被擋 |
| **2** | 生全形 | ASC complete · **中間產** · 禁直貼 |
| **3** | 反補 | 全形知識回寫 · **動作鎖 1** |
| **1A** | 落地 | 1 之無擋同動作 · **唯一 paste cut** |

```
for L in far→near:
  V1 = REF peep 原本動作
  V2 = complete FROM V1          # 生全形
  V1A = reverse_fill(V2, action_lock=V1)  # 反補 · 動作不變
  paste V1A only → STEP 線對看 → next
```

**毒：** E-RRT-01 貼2 · E-RRT-02 1A改動作 · E-ASC-08 只交2  
**全文：** `RESIDUAL_REBIRTH_RRT_01246.md`

---
## 0.12.44.J 旁系技能 · OCCLU-COMPLETE / ASC（§0.12.45）

**憲位：** 獨立節 **§0.12.45** · 全文 `OCCLU_COMPLETE_ASC_01245.md`

| | |
|--|--|
| 正名 | 補擋全機 |
| 短碼 | OCCLU-COMPLETE / ASC |
| 一句 | peep 殘形 **RRT 1→2→3→1A** → **只貼 1A** · peep 量 s≤1 · 一次一件 · 線對看 |
| 閘 | recall peep≥0.4 · TAG=`COMPLETE_IMAGINED` 或 `OCCLU_COMPLETE_SHAPECOND` |
| 樣 | `SETS/OBA_BATTLE6_MECH/COMPLETE` · `OBA_MIX_ROBOT_SHIP/ONE_BY_ONE` |
| 禁 | E-ASC-01..06 · E-OBA-23 · **仍受 E-OBA-25/26/27 約束** |

**嵌點：** 擴 T7b（complete unoccluded from REF）+ T9；T0–T6 掃瞄 · 格人脫鉤 · 母 peep 真源 · **REF 原本動作** **不變**。

---

*END §0.12.44 · 一人累貼 / OBA · + 殘相轉生 1→2→3→1A · asof 2026-10-30T18:35:44Z*
