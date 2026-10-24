# 《邊界行人》四軸真正交叉乘積

> **這份矩陣才是 IMAGE 幾何／鏡頭美術／VIDEO 方法／六幕敘事的相容交叉乘積。**  
> 舊的 3,723 個 ID 是各方法的來源目錄，不是四軸完整乘積；不得把它說成全量組合數。

## 四個相乘維度

1. **G — IMAGE 物件幾何與接觸狀態**：T 槌 H0/H1/H2/H3、雙 T 槌 H0／端面互撞、厚十字圓端蓋互撞、線形棒 POS／NEG、側柄種植圓柱、外端接柄圓柱、多向扁平面圓頭。T 槌母版 I-01 及各物件母 Prompt 仍是對應拓撲的參考源；MASTER 不會被冒充成物理接觸狀態。
2. **C — IMAGE 鏡頭／動作／美術**：T 槌 192 軸／鏡頭／蓄力組合；H2 的 FRONT／LOW／PEAK／SIDE 取景補充；雙槌／厚十字 48 接觸矩陣；十種獨立 WASH 構圖；S01 寫實、S02 粉彩 INS、S03 超現實。H2 的 FRONT 已由標準 T192 前視覆蓋，補充包只新增 LOW／PEAK／SIDE，避免把完全相同的 FRONT 再計一次。
3. **V — VIDEO 時間軸／閉環**：V-01 十秒單場景、V-02 五個獨立關鍵幀、V-03 固定錨點 planted-cylinder、V-04 母圖 I2V、V-05 雙 T、V-06 厚十字、V-07 線形棒正反控制、V-08 多向扁平面圓頭、V-09 六幕／MV 逐段製作。
4. **N — 敘事 IMAGE／VIDEO**：同一六幕因果骨幹下的六種故事處理路線：I-20 原始電影事件、I-21 替代道具隱喻、輪迴回聲、超現實隱喻、24 卡 MV 編排、52 段獨立鏡頭 MV 編排。每種處理仍包含完整六幕；不是只選一幕就結束故事。

乘積遵守合法相容表：T192 只用於 T；48 矩陣用於雙 T／厚十字；WASH10 用於線形棒／種植圓柱／多向圓頭；V-03 只用於種植圓柱家族；V-05／06／07／08 分別對應雙 T／厚十字／線形棒／多向圓頭。所有硬接觸只出現在 ACT 3；ACT 1／2／4／5／6 是柔性敘事，不會偷加第二種碰撞拓撲。

## 真正乘積數量

### G × C（先按幾何相容性拆分）

| 幾何家族 | IMAGE 幾何狀態 × 相機／動作 × 風格 | 組合數 |
|---|---:|---:|
| T 槌 | 4 個接觸態 × 192 × 3；另加 H2 3 種新增構圖 × 192 × 3 | 4,032 |
| 雙 T 槌 | H0／FACE × 48 × 3 | 288 |
| 厚十字雙槌 | FACE × 48 × 3 | 144 |
| 線形棒 | POS／NEG × 10 種 WASH × 3 | 60 |
| 側柄種植圓柱 | PLANTED × 10 種 WASH × 3 | 30 |
| 外端接柄圓柱 | PLANTED × 10 種 WASH × 3 | 30 |
| 多向扁平面圓頭 | H0／H2 × 10 種 WASH × 3 | 60 |
| **合計** |  | **4,644** |

### G × C × 相容 V

| 幾何家族 | 相容影片方法 | 組合數 |
|---|---|---:|
| T 槌 | V-01／V-02／V-04／V-09 | 4,032 × 4 = 16,128 |
| 雙 T 槌 | V-04／V-05／V-09 | 288 × 3 = 864 |
| 厚十字雙槌 | V-04／V-06／V-09 | 144 × 3 = 432 |
| 線形棒 | V-04／V-07／V-09 | 60 × 3 = 180 |
| 側柄種植圓柱 | V-03／V-04／V-09 | 30 × 3 = 90 |
| 外端接柄圓柱 | V-03／V-04／V-09 | 30 × 3 = 90 |
| 多向扁平面圓頭 | V-04／V-08／V-09 | 60 × 3 = 180 |
| **合計** |  | **17,964** |

### G × C × V × N

| 項目 | 數量 |
|---|---:|
| 相容幾何／鏡頭美術／影片方法組合 | 17,964 |
| 故事處理路線 | 6 |
| **完整 LOOP／TRY 組合** | **107,784** |
| 每個組合的六幕 IMAGE + 六幕 VIDEO 基本 Prompt | 12 |
| 六幕基本完整 Prompt 數 | 1,293,408 |
| V-02 五關鍵幀額外完整 Prompt | 120,960 |
| V-09 24／52 鏡頭卡 | 798,768 組 shot |
| V-09 每個 shot 各自完整 IMAGE + VIDEO Prompt | 1,597,536 |
| **合計編譯 Prompt 字串** | **3,011,904** |

此數量是按上面的可重現相容規則算出的**完整提示詞矩陣**，不是已生成媒體數。舊變體清單是一個來源方法目錄；交叉產品才會把同一幾何方法與所有相容鏡頭／風格、影片方法、故事路線相乘。

## 實際生成的資料檔

執行：

~~~bash
python bubble_break/boundary_pedestrian_product_matrix.py \
  --variants-csv docs/boundary_pedestrian/variants/VARIANT_IDS_FULL.csv \
  --catalog-doc docs/IMAGE_VIDEO_PROMPT_CATALOG.md \
  --outdir out/boundary_pedestrian/product_matrix
~~~

輸出：

- boundary_walker_full_product.jsonl.gz：每個組合一個 JSON 封包，含六幕完整 IMAGE／VIDEO Prompt；V-02 封包另有五個完整 keyframe Prompt；V-09 封包另有 24／52 組各自獨立的鏡頭 IMAGE／VIDEO Prompt。
- boundary_walker_product_index.csv：107,784 個組合的唯一 ID、幾何、接觸態、相機／蓄力／WASH、風格、影片方法、故事路線。
- boundary_walker_product_summary.json：來源 SHA-256、各軸計數、總數、輸出數和媒體／審核狀態。

排序由完整軸值的 SHA-256 決定，所以在同一份來源清單下可以重現，也不會先把同一家族的所有結果全部排在最前面。來源 CSV 有重複 ID 會立即報錯；任何新產品組合都由完整軸值產生獨立指紋。

## 輸出與驗收界線

每個 prompt package 都會寫：

- PROMPT_READY
- image_realization = NOT_RUN
- video_realization = NOT_RUN
- pixel_audit_status = NOT_RUN
- continuity_audit_status = NOT_RUN
- video_audit_status = NOT_RUN
- visual_acceptance_status = NOT_VERIFIED

底圖不生成文字；精確的 LOOP／TRY／方法藝術字由 boundary_pedestrian_try_art.py 作後期 SVG／ASS 疊加。把所有可能性相乘不代表每張畫都成功，也不會把 H0 間隙、H2 首次接觸、H3 跟進，或種植錨點的物理條件互相放寬。真正生成後仍須檢查原始 raster／影片及對應 SHA。
