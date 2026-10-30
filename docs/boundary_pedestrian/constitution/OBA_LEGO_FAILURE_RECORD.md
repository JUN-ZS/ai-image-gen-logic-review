# OBA · LEGO 試錯 RECORD（錯成）
# asof 2026-10-30T15:47:00Z · 母樣：minifig 99f4368d · robots 6fe76290

> **目的：** 把 LEGO 項目（人偶→機械人）一路毒／錯 寫死，更新 **一人累貼 · OBA** 時必讀。  
> **地位：** 入憲備註 · DO_NOT_REPEAT 同源 · 非法跳步＝降智。  
> **連動：** §0.12.44 OBA · MLR 母光重鋪（OBA 多物件落地招）

---

## 0. 一句

OBA 唔係「GEN 十張 HD 一次貼返」；  
係 **母只出位 → VOID 空台 → 掃瞄綠描邊 peep → 格人脫鉤 → 一人一刀 peep 縮放 · IoU 對位累貼**。

---

## 1. 錯成表（按時間／嚴重度）

| ID | 錯 | 症狀 | 治本 |
|----|----|------|------|
| **E-OBA-01** | **一次過全人 batch** | 互染 peep／scale 錯／前後排糊 | **一人一刀** · STEP i 完成先 i+1 |
| **E-OBA-02** | **黃 GRID 格號當人 ID** | 人大小跟格邊長 · 毒 scale | 格號＝**平面座標 only** · 人＝字母/UUID |
| **E-OBA-03** | **用母圖當貼底／LP 母** | 毒 donor · 像素污染 · 疊臉 | 母**只** MARK／peep／光場；底＝**母圖 VOID** |
| **E-OBA-04** | **放大 HD cut（s>1）** | 假清晰 · PIXEL 不可逆 | **s≤1** · 只 LANCZOS 縮 · 禁 upscale cut |
| **E-OBA-05** | **只 bbox／腳錨 · 無掃瞄** | 邊唔貼線 · 半透可見 9 人離邊 | rembg+魔法棒 → **綠描邊 stroke** → 邊對邊／IoU |
| **E-OBA-06** | **綠線變區域大包圍** | 非描邊 · 似舊 donor 毒 | `findContours` **2px stroke only** · 禁 fill 大 blob |
| **E-OBA-07** | **紅線／舊 MASK 重用** | 毒底鎖死 · 無視新對位 | 每刀 **重抽 peep** · 禁 OLD MASK 直接貼 |
| **E-OBA-08** | **VOID 比例未對母** | 位偏 · 前後距離錯 | VOID cover_fit 母幅 · **同 GRID 繼承** 再貼 |
| **E-OBA-09** | **前後排未跟 peep_h／Z** | 大人細人錯 · 海盜等比例錯 | s = **peep_h/w only** · 腳錨 peep_foot · 遠→近 α 序 |
| **E-OBA-10** | **機械人 v1 跳過掃瞄鏈** | 有 HD 無對位 · 同 minifig 缺項 | OBA **非法無 SCAN** · 必須綠邊+GRID+IoU+半透 |
| **E-OBA-11** | **peep 互染（鄰人污染）** | 綠邊咬到鄰機 | Voronoi／owner 互斥 · **一人獨立 rembg crop** |
| **E-OBA-12** | **GEN 姿與 peep 姿差大** | IoU 低 · 肢體 spill | shape-cond 同姿 GEN · 或 peep α 軟閘 · 低 IoU **單人重做** |
| **E-OBA-13** | **clean 層層 overlay 降智** | 「毒 DONOR 層層感染」 | **裸 peep 重貼** 解毒：只母量+原生 cut+VOID · 零 clean 鏈 |
| **E-OBA-14** | **格佔用當 scale** | 跨多格人物被格號放大 | 佔格只 **註冊 cell occupancy** · **永不入 s** |
| **E-OBA-15** | **只鎖腳／h · 無邊對邊 RATIO** | 半透證 9 人唔在線邊 | s=min(線w/cutw, 線h/cuth, 1) · 底咬線 bbox |
| **E-OBA-16** | **線稿+OLD 混座標** | 0.55線+0.45GRID＝無視線稿 | 腳/心/高 **100% peep/線 component** |
| **E-OBA-17** | **MARK.h 當遠近** | 後排黏連 → 反透視 | 遠近用 peep_foot／Z · 非 mean MARK.h |
| **E-OBA-18** | **軟 crop 帶地／背** | 糊邊 · 貼無 SHARP | **退地／退背** hard α · extract_subject |
| **E-OBA-19** | **GEN 只一次無 DETAIL 重PROMPT** | 細節 ≤ 母 · 無超越 | HD+ 二次重 PROMPT（mold／ABS／print） |
| **E-OBA-20** | **VOID 隨便空板** | 光／相機與母脫節 | 必須 **母重 PROMPT 無人版** |

---

## 2. 項目時間線（minifig → robots · 全段）

```
【母光 MLR 族 · 開發期】
v5–v8   母像素當底／LP 混          → E-OBA-03
v9      定稿：VOID + 退地 + HD+     但仍 batch 味
v9b     extract 退地（白衣毒）      → E-OBA-18
v10     母圖VOID 正名 + MASK MARK
v11–v13 比例／PIXEL 不可改
v12     VOID cover_fit · drawn≤native → E-OBA-04/08
v14     遠近 ZOOM 毒＝MARK.h        → E-OBA-17
v15     GRID + ZOE_DEPTH 對位嘗試
v16     描線稿 SCAN → 仍 0.55+0.45 OLD → E-OBA-16
v17     純線 component 殺毒
v18     VOID 比例再咬母
v19     線框邊對邊 RATIO            → E-OBA-15
v20     線邊 α 互咬 + MASK 掃毒
v21     peep h_min + flood-fill
v22     s_w 壓寬 + α∩clean 裁邊     （開始 clean 堆疊）
v23     單人 peep 重咬
v24     裸 peep 解毒一刀            → E-OBA-13 LOCK
v25–v26 海盜 #03 半透診斷 · shape-cond 重 GEN
v27     GRID + 綠線繼承
v28     綠邊框死貼 · IoU/spill 自審
v28b–c  修 03/05 · 禁紅 donor 大包圍  → E-OBA-06/07
v29     綠 stroke only
v30     一人獨立 魔法棒／CLIP
v31     格號≠人 · 字母 A–J          → E-OBA-02
v31_PASTE 貼 HD 上 VOID
v32     **一人累貼** 正名 OBA       → E-OBA-01 解

【機械人新母 · 6fe76290】
  VOID 65e9 · HD atlas 10 件
  OBA v1  跳 SCAN 粗貼             → E-OBA-10 致命
  診斷：缺綠邊／GRID繼承／半透／IoU／strip
  OBA_v2_SCAN 補回全套
    mean IoU≈0.63 · 前排 F/G/H/J≈0.9 · D/B 弱單人重
```

---

## 3. 對照：前項目「有」· 機械人 v1「無」

| # | 掃瞄對位件 | minifig 終 | robots v1 | robots v2_SCAN |
|---|------------|------------|-----------|----------------|
| 1 | 綠描邊 peep stroke | ✓ | ✗ | ✓ |
| 2 | 黃 GRID 座標 · 繼承 VOID | ✓ | 弱 | ✓ |
| 3 | 每步 peep｜HD｜累積 strip | ✓ | ✗ | ✓ |
| 4 | 半透 peep綠 vs paste紅 | ✓ | ✗ | ✓ |
| 5 | IoU／spill 閘 | ✓ | ✗ | ✓ |
| 6 | rembg+wand 掃瞄 peep | ✓ | 半 | ✓ |
| 7 | 格人脫鉤（字母≠格號） | ✓ | 弱 | ✓ |
| 8 | 一人一刀累積 | ✓ v32 | 一次 batch 味 | ✓ |

**裁定：** 無 1–7 = **非法 OBA** · 只算「粗貼 demo」。

---

## 4. 成功判據（自審 · 終極）

| 閘 | 通過 |
|----|------|
| 綠 stroke 存在 · 非 fill blob | 目視 + stroke 像素帶狀 |
| 格號 ≠ 人號 | 數字在格心 · 字母在 peep |
| s≤1 · 來源 peep_h/w | audit JSON |
| 半透綠 peep 邊 ≈ 紅 paste 邊 | 邊對邊 |
| IoU（建議）≥0.55 前排 ≥0.75 | 低者 **單人重 STEP** |
| VOID 無母 RGB 滲入 | 目視空台 |
| PIXEL 庫未 upscale | cut native · 只 LANCZOS 縮 |
| 遠近 ≈ peep_foot 序 | 後細前大（或 peep 真高） |

---

## 5. 禁句／禁路

- 「一次貼晒十個」  
- 「跟 GRID 格放大」  
- 「用母圖做底再貼」  
- 「先 clean 再 clean」  
- 「有 HD 就夠 · 唔使掃瞄」  
- 「格號就係人號」  
- 「s 可以 >1 再清晰啲」  
- 「舊 MASK 重用快啲」  

---

## 6. 路徑索引（artifacts）

| 項 | 路徑／asset |
|----|-------------|
| minifig 母 | `99f4368d-6fa9-49a8-8972-25efccb0e0c6` |
| robots 母 | `6fe76290-12ba-440d-86b0-bb90545a0d3c` |
| robots VOID | `65e9def9-2de7-4e96-826d-58e2e8fa2a1c` |
| minifig OBA | `SETS/IC_LEGO10_MLR/v32_ONE_BY_ONE` |
| robots 非法 v1 | `SETS/IC_LEGO10_MLR/MOTHER_ROBOTS10/OBA_v1` |
| robots LOCK 樣 | `SETS/IC_LEGO10_MLR/MOTHER_ROBOTS10/OBA_v2_SCAN` |
| 診斷卡 | `OBA_v2_SCAN/00_DIAGNOSIS.jpg` |
| 半透自審 | `OBA_v2_SCAN/03_SEMI_PEEP_vs_PASTE.jpg` |

---

*END RECORD · LEGO→OBA 錯成 E-OBA-01..20 · asof 2026-10-30T15:47:00Z*


---

## 2. BATTLE6 / b132 毒→治（asof 2026-10-30T16:49:24Z）

| ID | 錯 | 症狀 | 治本 |
|----|----|------|------|
| **E-OBA-10** | battle6 跳 SCAN | 無綠描邊／無 IoU／無半透自審 | 全鏈 T0–T10 · `OBA_SCAN_B132` |
| **E-OBA-05** | 只 box 位 | 最終像新棚拼場 | peep＝母 RGB + mother−VOID diff mask · 綠 2px stroke |
| **E-OBA-12** | HD 棚拍無同姿 | 有位無形 | shape-cond 失敗時 **peep 過閘**（IoU=1.0）優先於假 HD |
| **E-OBA-21** | peep 用 diff 當 RGB | 只剩地紋剪影 | **mask 用 diff · RGB 必取母圖** |
| **E-OBA-22** | rembg 小件崩 | B/C 面積過細 | seed crop + mother−VOID + Voronoi 互斥 |

**LOCK 成果：** `SETS/OBA_SCAN_B132/FINAL_OBA_SCAN.jpg` · 全 peep IoU=1.0 · 樣板名 **BATTLE6**  
**非法示範：** `OBA_BATTLE6_MECH` 舊 FINAL_OBA6（已覆寫為 SCAN LOCK）



---

## 3. OCCLU-COMPLETE / ASC 入憲（asof 2026-10-30T17:13:34Z）

**憲位 §0.12.45** · 技能四層 + 鐵序 + 閘 已入 `OCCLU_COMPLETE_ASC_01245.md`

| ID | 錯 | 症狀 | 治本 |
|----|----|------|------|
| **E-ASC-01** | ASC 當母真像素 | peep 真源被假肢污染 | TAG=`COMPLETE_IMAGINED` · peep 仍真源 |
| **E-ASC-02** | 場內 inpaint 留鄰 | 補肢帶鄰機碎片 | solo black + remove other mechs |
| **E-ASC-03** | 無 peep 量亂貼 | 位飄 · 前後比例崩 | s≤1 peep_h/w · foot 錨 |
| **E-ASC-04** | batch complete | 互染 · 無單 STEP 重做 | 一人一刀 ASC |
| **E-ASC-05** | IoU 硬閘 complete | 形>peep 永遠 FAIL | **recall** 閘 peep⊂paste |
| **E-ASC-06** | 無遠近序 | 後蓋前 · 遮擋反 | foot_y asc 近後貼 |
| **E-OBA-23** | LOCK↔ASC 混 | Δ 解讀錯 · 假咬母 | peep-LOCK≠ASC · 分交付 |

**技能說明（點解識補肢）：** amodal prior · shape-cond · complete prompt · solo isolation  
**LOCK 樣：** `COMPLETE/FINAL_COMPLETE_OBA.jpg` · 序 B→D→C→F→A→E · C=`ccdec01e`


---

## 4. 優化入憲 · 黃線格號法 + 有位無形（asof 2026-10-30T17:17:12Z）

### 4.1 黃線 GRID 格號法（f168 · §0.12.44.K）

**verbatim 入憲：**
> 黃線 GRID 中的格的數字是 GRID 的座標，不是人的數字標記；人用其他方法記；格號用錯 → 毒錯人的大小規格。

| 碼 | 已有治本（加強） |
|----|------------------|
| E-OBA-02 | 格號＝平面座標 only · 人＝字母/UUID · s 永不跟格 |
| E-OBA-14 | 佔格只註冊 · 永不入 s |
| 自審 | 數字在格心 · 字母在 peep |
| 禁句 | 「格號就係人號」「跟 GRID 格放大」 |

專文：`OBA_YELLOW_GRID_CELL_LAW.md`

### 4.2 有位無形 · 最新母沒用到（BATTLE6 毒審 · §0.12.44.L）

| 碼 | 錯 | 症狀 | 治本 |
|----|----|------|------|
| **E-OBA-24** | **有位無形** | 母只 VOID+粗 box；HD 棚拍另生；姿脫鉤；用戶覺「最新圖沒用」 | OBA-SCAN 全鏈 · shape-cond 同姿 · 失敗 peep 過閘 · 過閘才 LOCK |
| E-OBA-10 | 跳 SCAN | 無綠邊／半透／IoU | T0–T10 全 |
| E-OBA-05 | 只 box | 無邊對邊 | 綠 2px peep |
| E-OBA-12 | 姿脫鉤 | 互戰姿 vs 棚拍 | shape-cond 或 peep gate |
| E-OBA-06 | 綠框 fill | 非描邊 | stroke only |

**毒審分層：** 底✓ 位△ 形✗ 像素✗ → 級 `ILLEGAL_OBA_DEMO`  
**根因：** 最新母只供 VOID+框 · SCAN 跳空 · HD 另生 → 有位無形  
**LOCK 樣：** `SETS/OBA_SCAN_B132` · 母 b1326837  
**專文：** `OBA_MOTHER_BITE_POSITION_WITHOUT_SHAPE.md`

### 4.3 與 ASC 分界
| | peep-LOCK | 有位無形毒 | ASC 補擋 |
|--|-----------|-----------|----------|
| 形來源 | 母 peep | 假棚拍未聲明 | 聲明想像肢 |
| Δ vs 母 | ≈4 | ≈28 無標 | ≈28 有 TAG |
| 合法 | ✓ | ✗ E-OBA-24 | ✓ §0.12.45 |

---

## E-OBA-25 / 26 / 27 · REF 原本動作／一次一件／線對看（asof 2026-10-30T18:26:00Z）

| 碼 | 毒 | 治本 |
|----|-----|------|
| E-OBA-25 | 無 REF · HD 自由棚拍 · 脫離母原本動作 | 每件綠 peep REF → i2i from REF |
| E-OBA-26 | batch 生 HD 再一齊貼 | 一次一件 accum · 存逐步 |
| E-OBA-27 | 只交 final · 無 STEP 線對看 | mandatory STEP 三格 + 半透綠vs紅 |

**用戶重要句：** 一次一次加 · 每次對位自審 · 每物件出 REF 用原本動作。  
**樣：** MIX `ONE_BY_ONE` · 金樣人仔 STEP。  
**憲位：** §0.12.44.**M**


---

## 6. 殘相轉生 RRT（asof 2026-10-30T18:35:44Z）

**憲位 §0.12.46 / OBA .N** · 正名 **殘相轉生**

**用戶鐵句：**
> 最後仍是用物件的 VER.1A，即 1(原)→2(生全形)→3(反補出1的全形,但動作不變)→1A(1的沒被擋的相同動作)

| ID | 錯 | 治本 |
|----|-----|------|
| E-RRT-01 | 貼 VER.2 | 只貼 1A |
| E-RRT-02 | 1A 改動作 | action_lock=VER.1 |
| E-RRT-03 | 無 VER.1 | 必出 peep REF |
| E-ASC-08 | ASC 只交 2 | 強制 2→3→1A |

**鏈：** 1 原 → 2 生全形 → 3 反補 · 動作不變 → **1A 落地**
