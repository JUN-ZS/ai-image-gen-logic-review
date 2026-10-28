# §0.12.27 細格對換 — GRID_CELL_SWAP / GCS

### 0.12.27 細格對換（GRID_CELL_SWAP / GCS · 貼失敗→分格對換→羽化解毒）

> asof 2026-10-27T19:44:53Z · 用戶：「給這找錯除毒的成功過程給招名(寫入憲)」  
> 樣板鏈：CLEAN L-8dc48986cf31 → GRID48 L-c27dacaa89f4 → FINE32+16+12 L-ea2a6b0f2778 → **CELL8 L-db350bf16fa9**  
> 終態 asset：`092a9e12-286c-4719-af7f-275ace5218e7` · face lap 4935→**9316** · 格均 NCC **0.899**

> **地位：** 整臉／整板硬貼失敗、PATH1E 不收斂、feather 糊邊、病毒底人格歪時的 **正解除毒鏈**。  
> 未過本節 → 不得稱「細格對換完成／GCS 解毒」。

#### 0.12.27.A 招名（寫死）

| 語 | 名 |
|----|-----|
| **正名** | **細格對換** |
| **英／碼** | **GRID_CELL_SWAP** · **GCS** |
| **一句** | 貼整臉不行 → 一小格對一小格；糊邊再分細；feather 縮到 1–3px；對不準就 skip |
| **禁稱** | 整臉 soft wash、大羽化蓋、假 ECC 硬貼當「對準」 |

#### 0.12.27.B 找錯年表（不要重蹈）

| 序 | 錯／症 | 根因 | 解救 |
|----|--------|------|------|
| 1 | 人那格 MAD 高、身份漂 | **VIRUS_LOCAL_BASE**（SELFGEN 當 BASE） | §0.12.23 · BASE=N2LS／全幅 native 自裁 |
| 2 | ratio 拉歪 | EXPAND_BOX 重比例 / 非等向 | isotropic only · §0.12.24.C |
| 3 | 整臉 PATH1E WEAK · RT 大 | F_d 過寬（銅盤／甲當臉）· plate 未咬 | 先 §0.12.14 真臉框；仍失敗 → **進 GCS** |
| 4 | 大 feather 糊邊 | 一刀大 α 暈邊 | **分細格** + feather 2–3px → 1px |
| 5 | 整板 NCC 低仍硬貼 | 無格級閘 | 每格 NCC 閘；低則 **skip** 不拖垮 |

#### 0.12.27.C 成功鏈（正典 GCS）

```text
G0  BASE = 全幅 native（禁病毒局部母）· 可選已 CLEAN 人格
G1  donor = 同構自裁 GEN（N2LS self-fire face／person）· 禁外來假臉
G2  multi-scale 粗定位 donor → face box（tmpl 目標 ≥0.80）
G3  分格對換（由粗到細）:
      P1  CELL 48  feather≤6   step≈32   全臉／上身
      P2  CELL 32  feather 3   step≈20   全臉
      P3  CELL 16  feather 2   眼鼻區
      P4  CELL 12  feather 2   只打 blur_zone（feather 糊邊 DETECT）
      P5  CELL  8  feather 1   只打 髮際∪甲邊∪殘 soft（zone）
G4  每格：local ±R 搜 max NCC → 純 V5 混 → 累加 α 歸一
G5  閘：NCC 分檔 gain；NCC 過低 → skip（禁止硬蓋）
G6  可選 seam HF：out 比 clean 更糊處 → donor HF 微注
G7  PROOF：mean_ncc · lap_face 升 · META + L-
```

#### 0.12.27.D 每格公式（內容）

```
plate_cell = base + α*(gen_MF − base_MF) + β*α*base_HF + γ*α*gen_HF
α = feather(CELL, f_px) * gain(NCC) * [blur_boost if in blur_zone]
```

- **純 V5**（§0.12.24）：禁 full-RGB soft 主蓋（CHEAT_B）  
- feather：**smootherstep**；f 隨 CELL 收：6→3→2→1  
- gain 樣板：NCC≥0.88 → high；≥0.70 → mid；≥min → low；<min → **skip**

#### 0.12.27.E blur_zone／edge_zone（羽化解毒）

| zone | DETECT | 用途 |
|------|--------|------|
| **blur_zone** | 相對 clean 的 soft-diff 高 ∧ HF 低 | P4 專打大羽化糊 |
| **edge_zone** | 髮際（近膚非膚）∪ 甲邊（暗金+edge）∪ 殘 soft | P5 CELL8 專打 |

> 用戶原意：**再分細，就可以把模糊的 feather 邊界修正** — zone 只服務邊界，不是整臉重塗。

#### 0.12.27.F 閘門 PROOF

| 閘 | 過線 | 樣板 CELL8 |
|----|------|------------|
| virus_local_base | false | false |
| place tmpl | ≥0.75（目標≥0.80） | 0.82 |
| 格均 NCC（末遍） | ≥0.75 | **0.899** |
| lap_face out/in | ≥1.05×（目標明顯升） | 4935→**9316** |
| feather 末遍 | ≤2px（理想 1px） | 1px |
| skip 存在 | 允許且應有 | 低 NCC 不硬貼 |

#### 0.12.27.G 與他節

| 節 | 關係 |
|----|------|
| §0.12.23 VIRUS | G0 母底 |
| §0.12.14 PIXEL_RATIO | 整臉心對心仍優先；**失敗才 GCS** |
| §0.12.17 PATH1E | 整臉 ECC OK 可不用 GCS；WEAK → GCS |
| §0.12.24 WHOLE / V5 | 內容公式；GCS 是 **格級 WHOLE** |
| §0.12.25 GOU | 形狀 α 可與 zone 疊；GCS 單位是格不是勾 |
| §0.12.18 GRID×SIAX | 清晰 donor 可進 G1；不取代分格對位 |

#### 0.12.27.H 黑名單（E-GS 續）

| 代號 | 一句 |
|------|------|
| **E-GS-34** | 整臉大 feather 當完成（糊邊未分細） |
| **E-GS-35** | 格 NCC 低仍全 α 蓋（無 skip） |
| **E-GS-36** | 無粗定位就亂格掃全圖 |
| **E-GS-37** | CELL8 打全臉不打 zone（算力毒+過銳） |
| **E-GS-38** | 用病毒 SELFGEN 底再 GCS（毒未除） |

#### 0.12.27.I 樣板數值（SET-R · 2026-10-27）

| L | 遍 | 要點 |
|---|-----|------|
| L-8dc48986cf31 | CLEAN 人格 | ECC face 0.936 · 解毒 BASE |
| L-c27dacaa89f4 | GRID48 | mean NCC 0.816 · 500 格 |
| L-ea2a6b0f2778 | 32+16+12 | P2 NCC **0.958** · lap 3346→7493 |
| **L-db350bf16fa9** | **CELL8** | **13904** 格 · NCC **0.899** · lap **9316** |

#### 0.12.27.J 一刀參數卡

```
BASE_ASSET=          # 全幅 native / CLEAN
DONOR_FACE_GEN=      # 自裁同構 GEN
CELL_CHAIN=48,32,16,12,8
FEATHER_CHAIN=6,3,2,2,1
NCC_MIN=0.42–0.50
ZONE=blur|hair_armor|both
V5=true  CHEAT_B=false
```

*END §0.12.27 · 細格對換 / GRID_CELL_SWAP · asof 2026-10-27T19:44:53Z*

---

---

## §0.12.27.K → 改掛 §0.12.28（備案）

> asof 2026-10-27T20:40:46Z · 原 TEXT_GCS 試種 **用戶判定全錯** · 不保留「成功樣板」敘事。  
> **技名正典：** **字糊反推對換** / **TEXT_BLUR_REVERSE_SWAP** / **TBRS** → 見 **§0.12.28**  
> 附件：`TEXT_BLUR_REVERSE_SWAP_01228.md` · `TEXT_BLUR_REVERSE_SWAP_NAME.md` · `TEXT_BLUR_REVERSE_SWAP_DO_NOT_REPEAT.md`  
> 舊 L-a545… / L-ce43… 僅作試錯檔，**非**正典樣板。

*END §0.12.27.K 改掛*
