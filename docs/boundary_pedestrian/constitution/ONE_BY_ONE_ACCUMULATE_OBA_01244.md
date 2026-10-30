# §0.12.44 一人累貼（ONE_BY_ONE_ACCUMULATE / OBA · **LOCK 終極版**）
# asof 2026-10-30T15:47:00Z

> **正名：一人累貼** · **短碼 OBA** · **英** One-By-one Accumulate  
> **試錯源：** `OBA_LEGO_FAILURE_RECORD.md`（**E-OBA-01..20**）  
> **樣板：** minifig `99f4368d` · robots `6fe76290` · VOID · **`OBA_v2_SCAN`（唯一合法 robots 樣）**  
> **家族：** MLR 母光重鋪 · **OBA＝多物件落地鐵序**

---

## 0.12.44.A 一句

母只出 **位／形／光** → **母圖 VOID** 空台 → **掃瞄綠描邊 peep** → 黃 GRID **座標**（≠人）→ 各件 **獨立 GEN HD（s≤1 · 退地）** → **一人一刀** peep 縮放 · IoU 對位 · **累積** 貼上 VOID。

---

## 0.12.44.B 地位

| 族 | 關係 |
|----|------|
| **MLR** 母光重鋪 | OBA 係其 **多物件落地招**（VOID＋絕對位） |
| GOU／MSR | 管單幀紋理／宏圖 · **不管** 多件絕對位累貼 |
| SWP 升紋金字塔 | 可嵌單件升清 · **之後** 再 OBA 貼 |
| HTFC | 時間追尾 · 非本招 |

**非法：** 無 SCAN 鏈嘅「十 HD 一次貼」＝ demo · **唔入 LOCK 成果**（E-OBA-10）。

---

## 0.12.44.C 鐵序（不可顛倒 · 不可 batch）

```
T0  母圖 GEN／選定
T1  母圖 VOID（重 PROMPT 無人／無物 · 同幅同光 · cover_fit 母）
T2  黃 GRID 劃座標格（格號 1..N · 只座標）
T3  人／機 字母冊 A..（≠格號）
T4  每人獨立：solo crop → rembg + 魔法棒 → peep mask（VORONOI 互斥）
T5  綠描邊 stroke（findContours · 2px · 禁 fill）
T6  peep 量：peep_w/h · peep_cx · peep_foot · cell occupancy（只註冊 · 永不入 s）
T7  獨立 GEN HD + 退地（重 PROMPT 超細節 · shape-cond 同姿優先）
T8  遠→近 排序（peep_foot 升序）
T9  一人一刀：
      s = min(peep_h/cut_h, peep_w/cut_w, 1.0)   # 禁格邊長 · 禁 s>1
      腳錨 peep_foot + peep_cx
      IoU 微搜對 peep mask
      spill 閘 · 半透自審（綠 peep vs 紅 paste）
      累積 alpha_composite → VOID
T10 全齊 · GRID+綠邊+字母 overlay · audit JSON · step strips
```

**禁跳：** T4–T6 掃瞄 · T9 單人。

---

## 0.12.44.D 三律（硬）

1. **格人脫鉤** — GRID 數字 ≠ 人；s **永不** 跟格邊長（E-OBA-02/14）  
2. **peep 獨規** — s 只來自 peep_h/w · PIXEL 庫 cut 只可縮（E-OBA-04/09/15）  
3. **一人一刀** — 禁 batch；低 IoU **只重該 STEP**（E-OBA-01/10/12）

---

## 0.12.44.E 掃瞄對位（前項目必帶 · 機械人 v1 曾缺 · 終極硬條件）

| 件 | 要 |
|----|----|
| rembg + floodFill 魔法棒 | 獨立 peep |
| 綠 stroke | 描邊 only（禁 fill） |
| 黃 GRID on 母 **與** VOID | 同座標繼承 |
| 半透 peep綠 vs paste紅 | 邊對邊自審 |
| IoU / spill | 建議 IoU≥0.55 · 前排≥0.75 |
| step strip | peep綠｜HD｜累積 |
| 退地 hard α | extract／退背 · 禁軟 crop 帶地 |

無上表 → **非法 OBA**（E-OBA-10）。

---

## 0.12.44.F 解毒（E-OBA-13）

若 clean／舊 MASK／紅 donor 層層鎖死：

```
裸 peep 重貼 · 解毒一刀
  = 只 母 peep 量 + 原生 HD cut + VOID
  · 零 clean 鏈 · 零 OLD MASK · 零 α∩feather 主路
```

單人診斷：先半透疊母 → 通再搬 VOID（海盜 #03 教例）。

---

## 0.12.44.G 一刀參數卡（終極）

```
MODE=OBA_ONE_BY_ONE
MOTHER=<asset>
VOID=reprompt_empty cover_fit mother
GRID=2x5|2x6 coords_only
ID=letters A-J (not grid numbers)
PEEP=rembg+wand solo_crop VORONOI_excl
STROKE=findContours thickness=2 no_fill
SCALE=peep_only s<=1 LANCZOS
ANCHOR=foot+cx
ALIGN=IoU_microsearch
ORDER=peep_foot asc
PASTE=alpha_composite accumulate
AUDIT=semi+strip+IoU+spill+grid_cells
CUT=extract_hard_alpha
BAN=batch, mother_as_base, s>1, grid_scale, old_mask, red_donor, stroke_fill, soft_crop_bg
FAIL→ redo single STEP only
RECORD=OBA_LEGO_FAILURE_RECORD.md
```

---

## 0.12.44.H 連動

- 單件升清：可先 SWP／S1HL／GOU／LP2 再 cut 入 OBA  
- 光：VOID 繼承母 IC · 可選 lit_bias  
- 記錄：每跑必寫 audit · 大失敗追加 E-OBA-*  
- MLR 詞彙：母圖VOID · MASK MARK · peep · 格人脫鉤 一律沿用  

---

## 0.12.44.I 樣板路徑

| | |
|--|--|
| minifig | `SETS/IC_LEGO10_MLR/v32_ONE_BY_ONE` · `v31_GRID_FIX` |
| robots **非法** | `…/MOTHER_ROBOTS10/OBA_v1`（E-OBA-10 示範） |
| robots **LOCK** | `…/MOTHER_ROBOTS10/OBA_v2_SCAN` |
| 錯成 | `OBA_LEGO_FAILURE_RECORD.md` |
| 禁表 | `OBA_DO_NOT_REPEAT.md` |

---

*END §0.12.44 · 一人累貼 / OBA · LOCK 終極版 · asof 2026-10-30T15:47:00Z*
