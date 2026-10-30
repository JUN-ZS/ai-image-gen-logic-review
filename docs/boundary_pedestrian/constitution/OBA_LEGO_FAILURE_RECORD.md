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
