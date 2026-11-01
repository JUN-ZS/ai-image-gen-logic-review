# §0.12.55 PREVENT BLUE INJECTION · PBI（LOCK draft asof 2026-11-01）

> **正名：** 防藍注入 · PREVENT_BLUE_INJECTION  
> **短碼：** PBI  
> **一句：** 升清寫新像素時鎖銀網色度；禁止 SR 把錯誤藍色當細節；事後洗藍≠PASS  

## 0.12.55.A 目標重鎖

| 偽目標 | 真目標 |
|--------|--------|
| 先出有藍斑的高清再修乾淨 | **生成 4×／HR 時不准注入錯誤藍色色度** |
| R9/R10/K holefill 當解決 | 只作測試資料／急救 |
| 藍 residual 全圖為零 | 只殺 **SR 新增、LP 不存在** 的藍噪；保留環境光 |

## 0.12.55.B 生成架構

```
LP/BASE chrom lock
  → SIAX/NCNN 4× (raw SR diagnostic OK)
  → material_chroma_guard: metal = C(LP)×Y(SR)
  → DETAIL6: metal = Y-only HF residual
  → MASTER only if blue-inject gates PASS
```

## 0.12.55.C 程式入口（UP-engine）

| 位 | 檔 | 毒 | 治 |
|----|----|----|----|
| SIAX | `upscale/siax.py` | 全 RGB tile 寫入 | `--apply-material-chroma-guard` |
| DETAIL6 | `upscale/detail6.py` | `source+(source-low)*gain*α` 三通道 | metal → `detail6_y_only_residual` |
| 共用 | `upscale/material_chroma_guard.py` | — | C(LP)×Y(SR) |

## 0.12.55.D 驗收鐵律

1. 銀網區不得超標 **新增** BLUE residual  
2. Connected blotch 面積／最大斑／數量受控  
3. ≥6 固定 mesh ROI + AUTO_WORST  
4. Ten／結構保留絲紋網孔  
5. DETAIL6 不得再注金屬 RGB chroma residual  
6. 失敗 → **拒 MASTER**；禁止事後洗藍冒充 PASS  

## 0.12.55.E 禁碼

| 碼 | 禁 |
|----|-----|
| E-PBI-01 | 全 RGB residual 當正式升清（無 material guard） |
| E-PBI-02 | DETAIL6 metal 走 RGB residual |
| E-PBI-03 | 事後 detox 當正式 ACCEPT／merge |
| E-PBI-04 | 把「藍=0」當目標而洗掉 LP 環境光 |
| E-PBI-05 | 只改 SIAX 不改 DETAIL6（污染下移） |

## 連動

GNP · SWP · S1HL · NCPG · R9/R10（診斷）· UP-engine DETAIL6/SIAX


## 0.12.55.F 連動護絲防黑（§0.12.57）

PBI 解決 **注藍**；仍可能 **拉黑**（G8）。  
定版聯動：**PBI → S1S2** · 樣板 `P0_CHILD_2048_NCNN_PBI_R6c.png`。  
詳 §0.12.57 護絲防黑。
