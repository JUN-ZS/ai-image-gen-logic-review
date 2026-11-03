# 一組完整 TRY  realization

## 唯一 ID

| 欄位 | 值 |
| --- | --- |
| combination_id | `BPX-0007DA681947FB49` |
| loop_id | `LOOP-000014` |
| try_id | `TRY-0007DA681947` |
| 故事路線 | `BP6-I20` · original photoreal six-act spine |
| 幾何 | `T` · contact `H2` |
| 鏡頭包 | `T_H2_IMPACT4` · `Y_DEPTH__CAM02_FRONT_THREE_QUARTER__M1` · shot `LOW` · windup `M1` |
| 風格 | `S01` |
| VIDEO | `V-04` |
| 目錄引用 | `I-01;I-04;I-18;PACK_IMPACT_4` |

## 這組是什麼

從 **107,784** 合法四軸乘積中取出 **1** 組，編譯六幕完整 IMAGE／VIDEO Prompt，並完成六幕 **IMAGE realization**（VIDEO 仍 `NOT_RUN`）。

硬接觸只在 **ACT3**（primary_try）；其餘五幕為 SOFT 敘事伴隨。

## 檔案

- `COMBINATION_PACKAGE.json` — 編譯器原包（含六幕 prompt）
- `prompts/` — 拆出的 IMAGE／VIDEO 全文
- `raw/` — 無字底圖
- `labeled/` — try_art 方法字層（SVG／ASS／可選 PNG）

## 驗收界線

`IMAGE_GENERATED` · **非** `PIXEL_AUDIT_PASS` · VIDEO `NOT_RUN`
