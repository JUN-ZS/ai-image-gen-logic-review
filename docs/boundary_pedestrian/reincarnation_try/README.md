# 《邊界行人》輪迴 TRY 圖鑑

> **同一故事不斷輪迴；每次 TRY 的方法不完全一樣。**  
> 畫面內用**藝術字**標出本次用了總庫哪條方法（不是 HUD 作弊字，是海報／片尾字幕美學）。

## 概念

```text
LOOP n:  畫界 → 保護 → 碎裂 → 假修 → 一界 → 選擇
              ↑________________________________↓
         方法軸輪換：GEO / 鏡頭 / 洗圖 / 風格 / VIDEO 心智
```

- 柔性幕（1/2/4/5/6）默認 `GEO.NONE`，字標 `SOFT`
- 碎裂幕（3）才掛硬幾何：`MULTI` / `T` / `ROD` / `CROSS` / `PLANT_O`…
- 下一輪換風格：`S-01` → `S-02` → `S-03`…
- 圖上字格式例：`TRY · I-16/I-17 · H2 · I-22 W01 · S-01`

## 本批 15 張

| 檔 | 輪 | 幕 | 方法（圖上可見） |
| --- | --- | --- | --- |
| `00_title_ring.jpg` | META | — | 輪迴 TRY 開場環 |
| `L1_ACT1…6` | LOOP1 | 1–6 | I-20 · S-01 · 柔／MULTI／T |
| `L2_ACT1…` `L2_ACT3…` | LOOP2 | 1,3 | I-21 · S-02 · 粉彩輪迴 |
| `L3_ACT3_ROD/CROSS/PLANT` | LOOP3 | 3 | I-10 / I-08 / I-15 硬方法輪換 |
| `L4_ACT6_SURREAL` | LOOP4 | 6 | S-03 超現實 · 輪迴再開 |
| `META_methods_as_karma.jpg` | META | — | 方法當業力總覽 |

完整表：`ATLAS.csv` · `MANIFEST.json`  
完整輪迴規格與 IMAGE／VIDEO 完整 Prompt：[`../LOOPING_TRY_STORY.md`](../LOOPING_TRY_STORY.md)  
全量 3,723 ID 六幕 Prompt 編譯器：[`../../../bubble_break/boundary_pedestrian_loop_planner.py`](../../../bubble_break/boundary_pedestrian_loop_planner.py)  
精確排版藝術字：[`../../../bubble_break/boundary_pedestrian_try_art.py`](../../../../bubble_break/boundary_pedestrian_try_art.py)

## 與 3.7k ID 的關係

本圖鑑是 **敘事可讀的 15 張抽樣輪迴**，不是全量乘積。  
真正的四軸乘積與 18 個風格／世界／角色系列見 [`../FULL_PRODUCT_MATRIX.md`](../FULL_PRODUCT_MATRIX.md)；全量產物包含 431,136 個合法 LOOP／TRY 組合，不等於已生成媒體。  
新的藝術字工具由確定字串疊加大型浮動 3D 海報字牌（約佔畫面 34.32%），並在 sidecar 記錄來源／作品 SHA-256；工具本身不生成媒體，不判定幾何 PASS。
全量 ID 見 [`../variants/`](../variants/)。  
要把某一 ID 變成下一輪 TRY：複製該 ID 的 geo/contact/cam/style 槽，疊六幕 spine，並在 Prompt 要求藝術字標出 `TRY · …`。

## 證據級別

`IMAGE_GENERATED_IN_SESSION` · **非正式** `PIXEL_AUDIT_PASS`  
部分幾何（CROSS 端蓋、PLANT 錨點）仍為 TRY 級，字標代表**意圖方法**，不代表像素驗收通過。
