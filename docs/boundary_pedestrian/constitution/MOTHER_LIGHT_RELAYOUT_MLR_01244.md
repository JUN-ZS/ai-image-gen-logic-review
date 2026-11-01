# 母光拾形重框 · MLR（§0.12.44 候選 · **v9 定稿**）

> asof 2026-10-30T20:10+08

## 一句

母圖**只抽形／位／光** → 每人 **重 PROMPT 超越原 DETAIL** → **退地／退背** 銳 α → 貼上 **母重 PROMPT 無人空白版** → 位／光優化。

## 鐵序 v9

```
M0     母圖（只讀 meta）
ES*    母圖 重PROMPT → 無人空白版（同相機／地／光 · 禁鬼影）
SH/POS/LIT  形·座標·受光
HD0    同形同光 GEN
HD+    再 重PROMPT 超越原 DETAIL（mold lines / ABS grain / print razor…）
CUT    退地／退背 hard α（角點 flood bg · 最大連通 · 1px AA）
NW     ES* ×scale 空白底
RL     POS 貼 CUT · LIT gain · 合成接觸影（非母像素）
```

## 禁

| ID | 禁 |
|----|-----|
| E-MLR-M0 | 母圖像素當 LP／拼底 |
| E-MLR-CROP | 軟 crop 帶地／背 → 糊邊（必須 **退地／退背**） |
| E-MLR-EMPTY | 隨便空板 · 必須 **母重 PROMPT 無人版** |
| E-MLR-FLAT | 只 GEN 一次不夠 · 要 **DETAIL 重 PROMPT** |

## 樣板

| | |
|--|--|
| 母 | `99f4368d` |
| ES* | `111b3314` 母重PROMPT無人 |
| HD+×10 | 1152×1728 detail |
| CUT | `cutouts_v9/*_CUT.png` 洋紅檢查 |
| 新維 | `NEW_WORLD_v9_…` 5376×3024 |

*END*

## v9b 除毒

| 錯 | 治 |
|----|-----|
| 灰阈 退地 吃白衣（太空人／護士碎） | **extract_subject 退地／退背**（白膠 OK） |
| 軟 crop 帶地 | 禁 · 必須 hard α / extract |
| 空白非母源 | 必須 **母重 PROMPT 無人版** `111b3314` |
| DETAIL 不足 | 二次 **重 PROMPT 超越原**（mold／ABS／print） |

樣板 v9b：`NEW_WORLD_v9b_EXTRACT_SHARP.jpg` · 10×h=1080 · extract 銳貼


## 母圖VOID · MASK MARK 對位（v10）

| 詞 | 義 |
|----|-----|
| **母圖VOID** | 母重 PROMPT 無人版（同相機／地／光） |
| **MASK MARK** | 母圖每人實例遮罩（COND 框種子 + 框內 母−VOID 差分） |

貼法（網查對齊）：
- ComfyUI **Mask Paste by BBox Mask** / ImagePasteByBBoxMask
- **ImageAlignByMask**（mask bounds → scale + translate）
- FL/D2 **PasteByMask** · `keep_ratio_fit`
- OpenCV instance mask → bbox → paste@coords

鐵序：`母 → MASK_MARK ×N → HD cut 退地 → keep_ratio_fit 進 MASK bbox（腳底錨）→ 母圖VOID`

禁：估座標亂貼 · 母像素當底 · 拉伸 `resize` 破比例

## v12 互相咬 · 雙修（LOCK 候選）

### 1 母圖 × 母圖VOID 比例
- VOID 必須 **cover_fit → 母 W×H**，與 MASK **同一座標系**
- 禁：VOID 另比例／未對齊就量 MASK → 位算錯

### 2 PIXEL 不可改 · 圖中可變小
| | |
|--|--|
| **PIXEL 庫** | native cut（1080 級）只讀 · 不重採樣污染源檔 |
| **drawn size** | = 母 MASK 高 × S · **只可 ≤ native** |
| **變小** | 一次 **LANCZOS downscale** 貼上 VOID |
| **禁** | upscale 發明像素 · 連鎖縮放 · 改源 PIXEL |

網參：display≠resolution · WAS Layer Fit（drawn≠source）· allow_upscale false · downscale from largest once

S = min(native_h / mother_mask_h)  capped · 保證全員只縮不放

## v14 遠近 ZOOM · 毒註

**毒非 PIXEL donor**（native 全員 ~1237–1385 同檔，無遠近）。

**毒 = MARK.h 當大小**：後排 mask 黏連/帽高 → mean MARK.h 後 486 > 前 454 = **反透視**。

**修**：`drawn_h = target_h(foot_y)` 透視  
`t=(foot−f_min)/(f_max−f_min)` · `target = base*(0.84 + 0.22*t)`  
→ 後 ZOOM OUT · 前 ZOOM IN · 位仍鎖 MARK foot/cx · PIXEL 只縮不放

## v16 描線稿 SCAN → MASK 位

**為何要試**：純差分 MASK 易黏連/吞背景；**外勾線稿**更貼「形」。

```
母圖 → Canny+Sobel 描線稿 SCAN
  → 編號格內 findContours 填實
  → MASK 腳/心（線 0.55 + GRID 0.45 防漂）
  → 導入 VOID → 逐號貼
  → 大小仍 × ZOE scale_depth
```

## v17 殺毒
v16 毒：`foot=0.55*線+0.45*GRID` → 仍用 OLD MASK 位，無視 e75 線稿對位。
修：位/高 **100% 純線 component**；seed 只作編號對人，不當座標。

## v17 殺毒（e75 線稿對位）

**毒底（v16）**：雖出描線稿，但
```
foot/cx = 0.55×線 + 0.45×OLD GRID
```
= **無視線稿對位 · 回用 OLD MASK 位**。

**修（v17c）**：
- e75 同源綠線 + Canny → 編號 ROI 窗內填 MASK
- **腳/心/高 = 100% MASK 量度** · 禁 OLD 混
- ROI/seed 只負責「拆開 10 人」，不當最終座標

## v19 線框邊對邊 RATIO
毒：只鎖腳/h → 半透疊可見 9 人外框不在母線邊。
修：s=min(line_w/cut_w, line_h/cut_h, 1)·LANCZOS只縮·底邊咬線bbox。

## v20 線邊輪廓 α 互咬 + MASK 掃毒
1. clean MASK = 差分∩線帶∩mark窗 · 前排互斥
2. s = min(proj_w_line/proj_w_cut, proj_h_line/proj_h_cut, 1)  # 投影邊非空 bbox
3. 底咬 line α 底 · 心咬 line α 心 · LANCZOS 只縮

## v21 peep h_min + flood-fill 閉合
- peep h 自母−VOID；h_min=peep×0.92
- 線稿 wall flood-fill 閉合 · 投影 h < h_min → 強制 peep 柱
- s 保證 drawn_h ≥ h_min（禁放大超過 native）

## v22 s_w 壓寬 + α∩clean 裁邊
- mother_w = clean/綠 中段水平投影
- s_w=mother_w/cut_w · s_h=peep_h/cut_h · s=min(s_w,s_h,1)
- h_min 優先若衝突
- 貼後 α *= feather(clean) 裁溢出肢體

## v23 單人 peep 重咬
- mark窗 largest blob → 獨立 h/w/cx/foot
- #07白塊清 #10 tw略放

## v24 裸 peep 重貼 · 解毒一刀（LOCK 備註）
毒：v16–v23 clean/Voronoi/α∩mask 層層自鎖 → 白豎條／降智
解毒：
- 母差分 peep 只量 h/w/cx/foot（不輸出貼圖 mask）
- native cut 只 LANCZOS s=min(s_h,s_w,1)
- VOID 腳錨裸貼 · cut 自身 α 唯一
- 禁 clean／Voronoi／flood-fill／α∩mask／feather_floor 主路

## v27 GRID + 綠線邊繼承（LOCK 方向）
```
母：GRID 編號 1..N 對位 + 綠線 peep 邊（框死 bbox）
VOID：同 GRID 同號 + 繼承綠線（座標/大小一字不改）
貼：cut LANCZOS fit 入綠框 · 心對框心 · 腳對框底
自審：IoU(α, peep) · spill out-of-box · fill；不過閘 → 提示方法（重GEN姿／重抽綠／h優先／in-box ECC）
```
禁：無 GRID 繼承亂 peep；禁 clean 裁綠框當 donor 毒。
