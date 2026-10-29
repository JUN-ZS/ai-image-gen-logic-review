# GOU_MESH_CORRECT_PROCESS.md
# 勾勾密網升清 · 正確流程（T0→T12）

> asof 2026-10-27T14:38:15Z · 憲：§0.12.23 VIRUS · §0.12.24 WHOLE · §0.12.25 GOU  
> **用戶試出終態：** 全幅母 → 衣裁出 GEN 密網重組 → 放大 → 勾形 DETECT → V5 形狀拼回 FULL  
> 樣板終態：`L-8ed30b6e8fe0`（f5 母 · fill 0.575 · ncc 0.82 · lap↑）

---

## 總覽（一眼）

```
T0  讀憲閘（virus/box/soft 禁）
T1  BASE = 全幅 native only（寫 asset + SHA）
T2  從 BASE 裁衣／甲 ROI（不是外來局部當母）
T3  GEN：Ref( crop , mesh_lock ) 密網重組（真生成紋，不是硬銳化）
T4  可選 2× Lanczos + HF（放大加紋，防 OOM 用 band）
T5  multi-scale template 定 search box（只定位）
T6  AFFINE ECC 整板對位（ncc 目標 ≥0.75）
T7  勾形：GrabCut 自邊界 ∩ DETECT(residual∩mesh∩metal) ∩ 可選綠勾
T8  RANGE = shape · 壓 skin · face oval · weapon lock
T9  內容 = V5（base + α·MFΔ + β·HF）· 反推不進 RGB
T10 plate_SHAPE.png（RGBA）→ composite FULL
T11 閘門 PROOF（fill / ncc / lap / 綠≠紅）
T12 META + L- + 可選 VIEW / ZONE / CONTOUR
```

**不是：** 局部升全圖 · 方框蓋 · soft RGB · 借 OLD 邊。  
**是：** 全幅繼承 + 生成級密網 + 不規則勾形 α。

---

## T0 · 讀憲閘（未過不得動手）

- [ ] 已讀 §0.12.23 禁病毒母底  
- [ ] 已讀 §0.12.24 反推=RANGE · WHOLE  
- [ ] 已讀 §0.12.25 形≠框 · DETECT  
- [ ] 本刀目標寫一句（例：只升甲網 · 武器 Δ≈0）

## T1 · BASE 鎖定

| 必須 | 禁止 |
|------|------|
| 全幅海報（含頭／石／字／球） | torso-only · 已拼假底 · 1152 縮圖當母 |
| META 寫 `base_asset` · `virus_local_base=false` | 無 asset 號硬稱 native |

**SET-R 合法例：** `f5c6a555…` · `947cf5b2…` · `aee81db8…` 升後全幅 · 等。

## T2 · 從 BASE 裁 ROI

```
box_i = search_or_user_roi on BASE coordinates
crop_i = BASE[box_i]     # 唯一合法 crop 源
```

- 可略擴肩／裙；**不可**把 crop 另存當新 BASE。

## T3 · GEN 密網重組（生成級）

```
gen = RefToImage(
  [ crop_i , mesh_density_lock ],   # 例 7f5 蜂窩鎖
  prompt = keep pose/hands/weapon topology;
           rebuild armor surface as dense honeycomb + gold filigree;
           photoreal metal · no oily skin · no face change
)
```

- **要：** 真生成網孔／金線走勢  
- **不要：** 只 USM／只描邊

## T4 · 放大加紋（可選 · 防 OOM）

- 2× Lanczos + 輕 HF 注入  
- 大圖用 **band／memmap**，禁一次載滿再雙倍無 cap  
- 放大後再 warp 到 box（先 up 再 down to box 可保細節）

## T5 · search box（只定位）

- multi-scale `matchTemplate` / 用戶框  
- **box 永遠不是拼貼形狀**（紅框標註）

## T6 · 對位

| 步 | 要求 |
|----|------|
| AFFINE ECC | 優於 euclid-only 當完成 |
| ncc | **≥ 0.75** 才進 T7（樣板 0.82） |
| phase | 可選亞像素補 |

ncc<0.55 → **STOP** 重 GEN 或重裁，禁止硬貼。

## T7 · 勾勾形狀（核心）

形狀來源可疊（§0.12.25）：

1. **自邊界** GrabCut / rembg 衣板 silhouette  
2. **DETECT** residual ∩ mesh ∩ metal ∩ hf_delta（改了什麼）  
3. **勾概念** 綠輪廓內域（若用戶給 e61 類圖）

```
keep = morph( self_bound ∪ armor_core ) − fire − skin
shape = distance_feather(keep)     # 不規則
RANGE = shape * changed * (1-skin) * (1-weapon_lock)
```

## T8 · 鎖

- face oval 高抑制  
- weapon softlock（Δ≈0 或 α 極低）  
- 可選 stone 不碰

## T9 · V5 內容

```
out = base
    + α * (gen_MF − base_MF)
    + β_base * α * base_HF
    + β_gen  * α * gen_HF
```

- α 由 RANGE 映射（樣板 mean α≈0.3 · 可再抬）  
- **禁止** full-RGB soft cover

## T10 · 拼回 FULL

```
plate_SHAPE.png  # RGB=V5 · A=RANGE
FULL_out = composite(FULL_base, plate_SHAPE @ (x0,y0))
```

- magick `compose over` 可；禁整框無 α 蓋

## T11 · 閘門 PROOF

| 閘 | 過線 | 樣板 L-8ed30b6e8fe0 |
|----|------|---------------------|
| virus_local_base | false | false |
| shape_fill_ratio | [0.30, 0.75] | **0.575** |
| affine_ncc | ≥ 0.75 | **0.824** |
| lap_armor out/in | ≥ 0.95 | 1178→**1609** |
| 綠形≠紅框 | 目視 + 圖 | CONTOUR 有 |
| weapon / face | 無大漂 | 鎖 |

未過 → 標 TRY 不標 FINAL。

## T12 · 產物

```
SET_R_*_FULL_q100.jpg   # ≥ 超 MB 可
*_VIEW.jpg
*_ZONE.jpg              # 母|GEN|V5|勾|DETECT
*_CONTOUR.jpg           # 綠勾 vs 紅框
*_ARMOR.jpg             # before|gen|paste
*_META.json             # 全參數 + L-
```

---

## 與舊節對照

| 節 | 本流程對應 |
|----|------------|
| §0.12.23 | T1 母底 |
| §0.12.24 | T5–T6 · T9 WHOLE/V5 |
| §0.12.25 | T7–T8 勾形 |
| MESH V5 | T9 公式 |
| GRID×SIAX | 可選 HF donor；不取代 GEN 密網 |

## 一刀參數卡（下次生圖可提）

```
BASE_ASSET=
MESH_LOCK_ASSET=          # 例 7f5
ALPHA_GAIN=0.90–0.95      # 要更咬可抬
WEAPON_LOCK=soft|hard
FACE_OVAL=on
FILL_TARGET=0.45–0.65
NCC_MIN=0.75
UPSCALE=2x_lanczos_hf|none
```

*END CORRECT_PROCESS · 2026-10-27T14:38:15Z*

---

## 預設 SIAX · SPM-A 探針（2026-10-29T19:00:00+08:00）

> 掛：§0.12.37 SPM

| 步 | 預設 |
|----|------|
| 近距前全幅預覽升清 | **SPM-A 48×64** 非全幅 4× |
| ROI GEN 後要 HF 對位 | 同 ROI 真 SIAX 或繼承 SPM residual |
| 合體前 | SPM／S1HL 二選一：預覽 SPM-A · 定版 P0 |

GOU 主幹仍是 **近距 GEN + 勾形貼**；SPM 只省 **外圈全幅 SIAX**。

<!-- SPM_DEFAULT_SIAX §0.12.39 -->
## 預設 SIAX（§0.12.39 SPM-A）

- 近距 ROI 可真 SIAX；**全幅／外圈預覽一升 = SPM-A 48×64²**
- 探針外 fail → GOU crop GEN 貼，不硬全幅 SIAX
- 與 Hybrid：`LP + SPM residual×M`；定版再 P0
<!-- END_SPM_DEFAULT -->

