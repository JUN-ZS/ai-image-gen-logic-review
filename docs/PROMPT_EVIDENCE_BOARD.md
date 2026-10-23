# Prompt Evidence Board｜一張圖兼顧作品、教學與驗收

## 目的

每一次打泡嘗試產生一組可追溯資產，而不是單獨一張無法辨識來源的圖：

~~~text
attempt/
├── prompt.txt             原始可複製 Prompt
├── manifest.json          本次變量、預期、實際觀察與審核資料
└── teaching_board.svg     打擊原圖 + 確定性排版的教學／驗收標註
~~~

當真實圖片產生後，將原始 raster 附在 manifest 對應的 attempt 上，再渲染教學板。源圖與標註板要同時保存；標註不覆蓋原始 raster，也不冒充生成器本身的輸出。

## 畫面版型（16:9）

- **左側約 2/3：**真實打擊畫面；可用虛線框標出接觸點 P／review ROI，不重繪或改動原 raster 的像素。
- **右上：來源追溯。** Attempt ID、stage、branch、source commit、topology、prompt ID、variant ID。
- **右中：公式與數值。** 這次更動的撞擊軸、鏡頭角度／焦距、windup、柄向，以及 H0 gap／H2 gap／H3 advance 等與該公式有關的數字。
- **右下：預期 vs 實際。** 預期接觸面、P、法線、間距，與真正檢查畫面後記錄的接觸面／位置／剛性。
- **底部：驗收與下一輪。** 失敗原因、下一輪只改哪個變量、審查者、raster SHA-256 與 audit 狀態。

色碼：青色為來源／公式欄位；綠色只代表有綁定相同 raster SHA 的 PASS 收據；紅色顯示明確 FAIL；琥珀色顯示等待或未驗證。無原圖時以 NO SOURCE RASTER ATTACHED 顯示，不會放一張 proxy 假扮成出圖。

## 為什麼不讓圖片模型直接把數字畫在圖上？

圖像模型可把端面、泡泡、角色、特效與構圖畫出來，但精確的 attempt ID、數值、中文字、commit SHA、狀態碼必須由程式排版。否則模型可能把 `H2 gap=0` 寫錯、漏字或把 FAIL 畫成 PASS。這些標註必須來自 machine-readable manifest，不能由模型補猜。

因此標準交付會有：
1. **SOURCE RASTER：**無字、無標籤的原始圖片，用來判定實際幾何。
2. **TEACHING／ACCEPTANCE BOARD：**原圖嵌入 SVG，旁邊疊加 manifest 的精確數據與檢查結果。

如果需要發佈版影片，不要把教學板直接塞進最終影片素材；可以另做教學版片尾或畫中畫。所有審查以乾淨原始 keyframe／影片為準。

## 從 T-Hammer 矩陣直接產生 Prompt 封包

先產生現有矩陣（本身只產生 prompts 與 geometry proxies，不生成圖像）：

~~~bash
python bubble_break/t_hammer_multiview_swing_engine.py --outdir out/t_hammer_multiview_swing
~~~

再打包每個 variant 的各條 Prompt：

~~~bash
python bubble_break/prompt_attempt_packet.py \
  --matrix out/t_hammer_multiview_swing/t_hammer_multiview_swing_matrix.json \
  --outdir out/prompt_packets/t_hammer_192 \
  --branch feat/dual-t-hammer-collision-contract \
  --commit-sha 03934ba4f147e5f85937068e1113f2f62198f8e6
~~~

`--branch` 和 `--commit-sha` 必須改成真正編譯來源所對應的 branch／commit；上例 commit 僅為說明當前 main 基準，不應在不同版本生成結果中重複照抄。

對目前的 T-Hammer multiview matrix，每個 variant 包含四種提示（雙槌幾何證明、H0、H2、H3），因此在完整 192 variants 的矩陣下，預期編譯 192 × 4 = 768 個 per-prompt 封包。封包階段的 `image_realization` 與 `pixel_audit` 都保持 `NOT_RUN`。之後每個實際生成的 raster 才能綁到其 attempt，填入真實的 observed fields 與 review receipt。

## 一張已生成圖怎樣加入標註

~~~bash
python bubble_break/prompt_evidence_board.py \
  --manifest out/prompt_packets/THE_ATTEMPT/manifest.json \
  --image out/actual_generated_raster.png \
  --out out/prompt_packets/THE_ATTEMPT/teaching_board.svg
~~~

- 在 manifest 中只填實際生成／審查後的欄位。沒有看過像素時，observed 值應是 `UNVERIFIED`。
- `pixel_audit_status=PASS` 需要 `review_receipt.verdict=PASS` 且 `review_receipt.raster_sha256` 與所附圖片 SHA-256 完全相同。沒有原圖、SHA 不一致或沒有收據時，畫板會把該 PASS 降為 `UNVERIFIED`。
- 這是來源綁定檢查，不會自行判斷接觸面是否畫正確；真正的像素判讀仍須由指定 reviewer／視覺檢查程序完成。
- `review_receipt` 的 reviewer 身份與結論仍是外部信任輸入；工具不會認證人類身份。

## 已知涵蓋範圍

此版 packet compiler 已有 T-Hammer multiview 的 `variants[].prompts` adapter。其他 branch 的輸出格式不完全相同（例如 Original Sin JSONL、CYLINDER_CROSS 的單張 dense-atlas prompt、planted-bubble 階段 request），需要各自的 adapter 映射至同一個 manifest schema；未適配的輸出不可宣稱已自動整合。Branch／Draft 對照表用於記錄這些來源、互斥拓撲與驗收邊界。
