# §0.12.57 護絲防黑 · WIRE_CELL_PROTECT / S1S2（LOCK asof 2026-11-01）

> **正名：** 護絲防黑  
> **短碼：** S1S2 / WCP  
> **樣板圖：** R6c `P0_CHILD_2048_NCNN_PBI_R6c.png`（peep 裙網 · 2048 FULL-RES · PBI+S1S2）  
> **歸因：** `r6c/g8_attrib` commit `07e52d7` · 修：`67b112f`  
> **連動：** PBI §0.12.55 · NCPG §0.12.53–56 · G7/G8  

## 0.12.57.A 這張樣板圖是什麼技（讀圖用）

用戶指 `P0_CHILD_2048…PBI…png` 時，**不是** 單次 text-to-image，而是：

```
母圖 peep 512（NCPG 窗）
  → Lanczos LP 2048
  → NCNN GENERAL_x4v3 · 24 probes · 4× residual（§0.12.56 原生產）
  → PBI：dY only · hyb = C(LP)×(Y_LP+dY)（§0.12.55 防藍）
  → S1S2：護絲防黑（本節）
  → G7 藍斑 / G8 黑斑 同閘驗收
```

| 層 | 技 | 本圖角色 |
|----|-----|----------|
| 窗 | NCPG peep | 固定母座標 peep，非全幅 GEN |
| 升清 | FULL-RES NCNN residual | 4× 細節進 2048 child |
| 防藍 | **PBI** | 禁 RGB residual 注藍 |
| 防黑 | **S1S2** | 禁孔／絲被負 dY 拉穿 |
| 閘 | G7+G8 | 藍／黑分開；FAIL 不升 MASTER |

## 0.12.57.B 一句

**PBI 鎖色之後，仍可能把網孔／銀絲拉成新黑斑；S1 帽負 residual，S2 護 wire，禁止 NEW black——修生成端，不降 G8 閾值。**

## 0.12.57.C 歸因四源（先診斷再開刀）

| 源 | 名 | 本樣板歸因（07e52d7） |
|----|-----|------------------------|
| **S1** | 孔內強負 Y residual | P0 **62%** · P1 **37%** · **全球 winner** |
| **S2** | 新黑落在 LP ridge/wire | P0 20% · P1 **34%** |
| **S3** | Lanczos LP 脆弱帶 Y∈[18,30) | P0 18% · P1 30% |
| **S4** | C(LP)×Y 合成失衡 | **≈0%**（本鏈非主因） |

禁：未歸因就只改 `y_lp-36` 宣告 PASS。

## 0.12.57.D 鐵律公式

```
wire, cell ← edge(LP)
res ← ridge_hard(dY)
res ← max(res, -wire_max_drop)   on wire     # S2  default 4
res ← max(res, -cell_max_drop)   on cell     # S1  default 10
res ← max(res, -other_max_drop)  else        # default 14
Y_out ← Y_LP + res
Y_out ← max(Y_out, Y_LP - region_cap)
# 禁 NEW black（對齊 G8 定義，非放寬閘）
if Y_LP ≥ black_thr:  Y_out ≥ black_thr + 0.5
RGB ← C(LP) × Y_out          # 仍走 PBI
```

| 參數 | 樣板值 | 說明 |
|------|--------|------|
| wire_max_drop | 4 | 絲幾乎不壓暗 |
| cell_max_drop | 10 | 孔負殘差硬帽 |
| other_max_drop | 14 | 其餘 |
| black_thr | 18 | 與 G8 同定義 |
| 撤銷 | `Y_floor = Y_LP − 36` | 歸因證明仍可拉穿 |

## 0.12.57.E 與 G7／G8

| 閘 | 職責 | S1S2 後樣板 |
|----|------|-------------|
| G7 | 新增藍斑 | 仍 PASS（PBI 主責） |
| G8-A | 近黑 + min_drop≥6 | PASS |
| G8-B | 銀 proxy 內新黑 | PASS（35k→492 級） |
| G8-C | 六固定 mesh ROI | PASS · n_fail=0 |
| wire_hit | 絲上新黑 | **0** |

**誠實代價：** Tenengrad 可能下降（負 dY 被帽 → 孔對比弱）；結構 align/sn 仍須 PASS。

## 0.12.57.F 狀態機

```
ATTRIB_G8 (S1–S4 占比)
  → PATCH s1_s2_protect_y
  → THIS_RUN R6c peep children
  → G7/G8 同閾
  → ACCEPT 僅 peep 子板級
  → R7 要 parent PASS 才 FORMAL 否則 DIAGNOSTIC_ONLY
  → merge main NO until 人工銀網 + clean-checkout
```

## 0.12.57.G 樣板檔

| 檔 | 角色 |
|----|------|
| `r6c/complete/P0_CHILD_2048_NCNN_PBI_R6c.png` | **定版 peep 裙** · 本節主樣 |
| `r6c/complete/P1_CHILD_2048_NCNN_PBI_R6c.png` | 胸／甲 peep |
| `ACCEPT_R6c_PBI.json` | round=`R6c_NCNN_PBI_S1S2_PROTECT` |
| `LOG_R6c_S1S2.md` | 修與閘 |
| `r6c/g8_attrib/*` | 歸因證據 |

## 0.12.57.H 禁碼

| 碼 | 禁 |
|----|-----|
| E-S1S2-01 | 無 G8 歸因就亂調 floor |
| E-S1S2-02 | 放寬 G8 閾值換 PASS |
| E-S1S2-03 | 有 S1S2 無 PBI（藍毒回潮） |
| E-S1S2-04 | peep ACCEPT 當全幅 MASTER |
| E-S1S2-05 | P0 G8 FAIL 仍 R7 正式鏈（必須 DIAGNOSTIC_ONLY） |
| E-S1S2-06 | 宣稱「人工銀網 mask」但其實只有 heuristic proxy |

## 連動

PBI · NCPG · GNP · SWP · S1HL · material_chroma_guard · run_r6c_ncnn.py
