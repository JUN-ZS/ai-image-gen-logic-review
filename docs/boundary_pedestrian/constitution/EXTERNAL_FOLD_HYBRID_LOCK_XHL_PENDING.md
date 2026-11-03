# 外折混鎖 · XHL · 待解說明

> asof 2026-10-28T16:43:00+08:00 · **PENDING / 待解** · 禁止當完成產線

## 構想源

用戶確認：可於外機用 SUPIR 等生成 **模板／數據包／定位運算子／根因圖**，交回 Grok sandbox **反推** 用於升清；本機無 GPU 不重跑 SUPIR。

## 正名

**外折混鎖** · **XHL** · eXternal-fold Hybrid Lock

## 目標鏈（草案）

```text
supir_pack（或 seedvr_pack…）
  01_src / 02_out / 03_diff? / 04_masks? / 05_params.json
    → Hybrid: out = LP(src) + HF(out_or_diff)×M
    → Ref(hybrid, a8b) 臉鎖
    → 可選 WNK／字法
```

## 紅線（草案 · 待 LOCK）

| ID | 禁 |
|----|-----|
| X-01 | 本 sandbox 安裝／日產全量 SUPIR、SeedVR2 |
| X-02 | SUPIR-Q 輸出直接當最終女主臉 |
| X-03 | 外折產出標成 TRUE SIAX 或「真實還原」 |
| X-04 | 無 params 標 Q/F 仍當完成 |
| X-05 | 字／白噪框只靠生成式超分保真 |

## 待解

- [ ] 首包樣板 + 人眼過閘  
- [ ] g 表與 mask 契約寫死  
- [ ] 升格 LOCK 或維持待解  

*END XHL PENDING*
