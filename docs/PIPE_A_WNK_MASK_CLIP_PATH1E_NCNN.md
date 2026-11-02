# 正典過程 · A母抽白 → MASK → 另母CLIP → 拼回A母 → ROI/PATH1E/ECC/NCNN

你要寫的是**這條**，不是只寫「peep×4 + matchTemplate」。

下列用本輪證據還原；每步有 SHA／尺寸可核。`quality_qualified=false` 全程。

---

## 角色命名（寫程式用常數）

| 符號 | 意思 | 本輪實際檔／asset |
|------|------|-------------------|
| **A母** | 主工作母圖（有白噪、要修） | `@211315eb` · 3584×2016 Siax 噪點圖 |
| **A_WNK** | A母 抽白後 | `OUT_WNK.png` SHA `0d1dd797…831a3d0a` |
| **MASK** | 從 A母 算出的殺白圖（保留） | `WNK_KILL_MASK.png` |
| **B母／另母** | 提供乾淨／好像素的 donor | 目標 `@10d59a3f` 7168；**未 staged** → 用 `FAIR_e283_A_SIAX4X.png` 7168 |
| **CLIP** | MASK 覆在 B母 上抽出的像素 | `CLIP_PIXELS_from_donor_BGRA.png` |
| **A_paste** | CLIP 拼回 A_WNK | `OUT_WNK_MASKPASTE.png` SHA `2d37472a…` |
| **C_polish** | 後續 A8B／PATH1E 場景母 | `@06da88f4` → `@2fa51094` 等 |
| **D_master** | NCNN×4+PBI 不降像素母 | 7168×4032 |
| **E_out** | ROI peep + ECC 硬貼後 | `@e357d601` 7168 SHA `72e7e87f…` |

---

## 總流程（你描述的順序）

```
① A母
    │  WNK §0.12.26.D
    │  kill = NOISE_WHITE ∩ ¬SPEC_LIGHT
    ├──────────────────────────────┐
    ▼                              ▼
② A_WNK（去白結果）           ③ MASK（殺白位置，要永久保留）
    │                              │
    │                              │ scale MASK → B母 尺寸
    │                              ▼
    │                         ④ 另母 B 上 CLIP 像素
    │                         (只取 MASK=1 的 B 像素)
    │                              │
    └──────── ⑤ 拼回 ──────────────┘
              A_paste = A_WNK 的底 + CLIP 像素
                    │
                    │  之後才是精修鏈
                    ▼
⑥ ROI 切 peep（臉／甲）
⑦ PATH1E plate = Ref(face_crop, a8b)   §0.12.17
⑧ （可選）DHY 甲 dens peep             §0.12.51
⑨ ECC 對位 peep → 硬貼回母圖           cc≥0.85
⑩ NCNN×4 memsafe：RAW 寫盤 → strip PBI  （升清；母圖不降）
⑪ 定版 7168 輸出 + RESULT JSON
```

**硬規則：MASK 從 A 來；像素從 B 來；拼回的是 A 的座標空間（必要時先對齊尺寸）。母圖定版不降 PIXEL。**

---

## 分步參數（本輪實測）

### ①→②→③  A母 抽白 + 留 MASK

| 項 | 值 |
|----|-----|
| skill | 白噪殺 **WNK** · §0.12.26.D |
| 公式 | `kill = NOISE_WHITE ∩ ¬SPEC_LIGHT` |
| A母 | `@211315eb` · 3584×2016 · SHA `64756c7d…` |
| A_WNK | `OUT_WNK.png` · SHA **`0d1dd797…831a3d0a`** |
| MASK | 同尺寸 3584×2016 單通道／可視化 RGB |
| stats | kill_frac ≈ **0.21** · noise_frac ≈ 0.57 · spec 保護 ≈ 0.10 |
| strip | 處理可 strip_h=512（省 RAM） |
| 禁 | E-SF-04：不可宣稱「殺光所有白」 |

偽碼：

```python
# Y,S,V or RGB heuristics
noise = near_white & low_chroma & high_local_var   # NOISE_WHITE
spec  = bright & high_grad_or_metal_mask           # SPEC_LIGHT 保護
MASK  = noise & ~spec                              # 0/255
A_WNK = median_or_bilateral_fill(A, MASK)          # 只改 MASK 區
save(MASK)  # 必須保留，後續 CLIP 用
```

---

### ④→⑤  MASK 放到另母 → CLIP → 拼回 A

| 項 | 值 |
|----|-----|
| skill | **wnk_mask_paste** |
| target | A_WNK SHA `0d1dd797…` · 3584×2016 |
| B母 目標 | `@10d59a3f` 7168（user 指定） |
| B母 實用 | `FAIR_e283_A_SIAX4X.png` 7168（10d59 未 staged 的 fallback） |
| scale | MASK ×2 → 7168；CLIP 後再對齊回 3584 貼（或 B 下採樣對齊 A） |
| 產出 CLIP | `CLIP_PIXELS_from_donor_BGRA.png` |
| A_paste | `OUT_WNK_MASKPASTE.png` SHA **`2d37472a…`** · kill 區 ≈ 1.5M px |

偽碼：

```python
# A space: Ha,Wa ; B space: Hb,Wb
scale = Wb / Wa   # e.g. 2.0
MASK_B = resize(MASK_A, (Wb, Hb), nearest)   # mask 用 nearest
CLIP = B.copy()
CLIP[~MASK_B] = 0   # 或 BGRA alpha=MASK

# paste back onto A space:
CLIP_A = resize(CLIP, (Wa, Ha), lanczos)     # 只縮 CLIP，不是縮定版母圖哲學
MASK_A = MASK  # already A size
A_paste = A_WNK.copy()
A_paste[MASK_A>0] = CLIP_A[MASK_A>0]         # 硬貼：只寫 MASK 像素
```

**這才是「用另母圖放 MASK 抽 PIXEL 拼到 A母」** —— 上一答的 e357 ECC 腳本**沒有**這段。

---

### ⑥⑦⑧  ROI + PATH1E + DHY（A_paste 或後續 polish 母上）

本輪有兩段精修證據（可選接在 ⑤ 後）：

**分支 X · 對 `@06da88f4` 場景**
1. face_crop from 06da  
2. PATH1E plate = Ref(face_crop, a8b) → plate asset  
3. DHY dens armor peep  
4. full Ref(a8b + plate + scene + dens)  
→ 產出鏈到 `@2fa51094` 等 polish 圖  

**分支 Y · 直接升清**
- 輸入 `@2fa51094` 1792×1008  
- NCNN GENERAL_x4v3 tile=64 pad=8  
- memsafe: **RAW 先寫盤** → strip PBI  
- OUT 7168 SHA `0703915d…`  

憲：
- PATH1E §0.12.17：`plate=Ref(face_crop,a8b)` 再 ECC；**禁止棚拍 a8b 直 ECC**（E-GS-12）
- DHY §0.12.51：甲 dens peep  
- S1HL §0.12.15.L：臉鎖  
- 禁止二次 SIAX 當完成（E-GS-47）

---

### ⑨ ECC 硬貼 peep（不降 PIXEL）

| 項 | 值 |
|----|-----|
| master | e107 NCNN PBI 7168 SHA `c743e3dc…` |
| peep 來源 | 同構圖 donor 1792 ROI ×4 LANCZOS |
| face box donor | 680,60,1111,423 → place 2720,240 · cc **0.959** |
| armor box | 537,181,1254,584 → place 2148,724 · cc **0.967** |
| 閘 | cc ≥ 0.85 才強貼 |
| 輸出 | `@e357d601` 7168 SHA **`72e7e87f…`** |

---

### ⑩ NCNN（升清 · 獨立可插在 ⑤ 後或 ⑨ 前）

```
write RAW (uint8 full) first
→ strip PBI luma-only: hyb = C(LP)×(Y_LP + ridge(dY))
→ 母圖 7168 不降
```

---

## 與你點名的 5 張圖怎麼接

| asset | 在鏈上的位置 |
|-------|----------------|
| `@06da88f4` | 精修場景母（A8B/PATH1E 入口） |
| `@2fa51094` | polish 後 1792 · **NCNN 輸入** |
| `@0c5d6732` | e357 **half 預覽** 1792（不是定版） |
| `@e357d601` | **定版 7168** ECC 硬貼 OUT |
| `@7e78f3bd` | 請你確認是否 MASK/CLIP 中間圖；寫程式時當 optional 中間 artifact |

---

## 程式模組切分（建議你照這個寫）

```
tools/
  wnk_kill.py              # ①②③  → A_WNK + MASK
  mask_clip_paste.py       # ④⑤    → CLIP + A_paste
  path1e_plate.py          # ⑥⑦    → face plate (Ref or offline)
  dhy_armor_peep.py        # ⑧
  ecc_hardpaste.py         # ⑨
  ncnn_fullframe_pbi.py    # ⑩ memsafe RAW→PBI
  run_pipe_a_master.py     # 編排 + RESULT.json
```

### RESULT 契約（每步都要）

```json
{
  "step": "05_mask_clip_paste",
  "A_sha": "...",
  "MASK_sha": "...",
  "B_sha": "...",
  "CLIP_sha": "...",
  "out_sha": "...",
  "out_wh": [W, H],
  "pixel_drop": false,
  "quality_qualified": false
}
```

---

## 最小可跑：④⑤ MASK CLIP PASTE

見 `pipe_mask_clip_paste.py`（不依賴 NCNN／Imagine）。

---

## 誠實邊界（寫進你的 DO_NOT）

1. `@10d59a3f` 當時**未在磁碟**，CLIP 用了 FAIR e283 同構 7168 fallback —— 程式應 fail 或明確 `--donor-fallback`。  
2. Imagine PATH1E plate **≠** 幾何 ECC 硬貼；日誌已寫。  
3. e357 最後一步是 **同構圖 peep ECC**，不是再抽一次 WNK。  
4. half 預覽 ≠ 定版。  
5. 全程 `quality_qualified=false`。
