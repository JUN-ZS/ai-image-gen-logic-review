# 同幅姿鎖升紋 · IPSD

> asof 2026-10-30T18:20+08 · **子步驟** · 嵌於 SWP §0.12.43 · 非獨立總招名

| 項 | 值 |
|----|-----|
| **正名** | **同幅姿鎖升紋** |
| **短碼** | **IPSD**（In-Place Same-frame Densify） |
| 母招 | **升紋金字塔 SWP** · GOU · FUB+Z |
| 地位 | densify **核**；SWP 管支母／貼序 |

## 一句

**同比例 · 同構圖 densify**：只換甲面 HF 晶格紋；**LP=該層母 · HF=donor**；禁 reframe／產品板／換拓。

## 與 SWP

```
每層 work = mother_ROI
densify = IPSD(work)
bite   = LP(work) + HF(densify)×M
GATE   = ncc(bite, work) ≥ 0.90
```

## 除毒備註（F6）

reframe donor ncc≈0.43 → 必須 **同比例 IPSD residual 重跑** → 樣板 ncc≈0.982。
