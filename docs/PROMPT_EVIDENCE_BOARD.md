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
- **底部：驗收與下一項試驗。** 失敗原因、已註冊的 control/treatment、下一個可驗證假設、審查者、raster SHA-256 與 audit 狀態。

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
  --teaching-layout standard \
  --out out/prompt_packets/THE_ATTEMPT/teaching_board.svg

python bubble_break/prompt_evidence_board.py \
  --manifest out/prompt_packets/THE_ATTEMPT/manifest.json \
  --image out/actual_generated_raster.png \
  --teaching-layout formula-first \
  --out out/prompt_packets/THE_ATTEMPT/teaching_board_formula_first.svg
~~~

- 在 manifest 中只填實際生成／審查後的欄位。沒有看過像素時，observed 值應是 `UNVERIFIED`。
- `pixel_audit_status=PASS` 需要 `review_receipt.verdict=PASS` 且 `review_receipt.raster_sha256` 與所附圖片 SHA-256 完全相同。沒有原圖、SHA 不一致或沒有收據時，畫板會把該 PASS 降為 `UNVERIFIED`。
- 這是來源綁定檢查，不會自行判斷接觸面是否畫正確；真正的像素判讀仍須由指定 reviewer／視覺檢查程序完成。
- `review_receipt` 的 reviewer 身份與結論仍是外部信任輸入；工具不會認證人類身份。

## 「下一次要試什麼」由試驗排程器安排，診斷只提供證據

圖像公式、教學板與影片 Prompt 的第一批對照、命令及判定門檻見 [Prompt Trial Planner](PROMPT_TRIAL_PLANNER.md)。教學板可以輸出 standard 與 formula-first 兩版，用同一張 source raster 做版式盲測。診斷器的失敗原因是試驗假設的輸入，不是自動宣告某個改法有效。

\`bubble_break/prompt_failure_diagnosis.py\` 會根據已審查的結構化欄位，選出一個優先失敗原因，輸出：

- \`primary_failure_code\` 與全部已識別失敗；
- \`edit_only\`：下一輪允許改的最小變量；
- \`freeze\`：必須保持不變的拓撲／相機／接觸點等欄位；
- \`repair_prompt_delta\`：附加到原 Prompt 的具體修正指令；
- \`expected_after_change\`：下一張圖必須驗證的可觀察結果。

### 例：側面接觸是觀察證據，不是唯一試驗答案

在 reviewer 檢查這張原圖後，將該圖的 SHA-256 寫入 \`review_receipt.raster_sha256\`，將 \`review_receipt.verdict\` 設為 \`FAIL\`，並記錄 \`observed.active_surface = "broad_sidewall"\`。同時應寫入 reviewer 身份、時間及失敗理由。然後：

~~~bash
python bubble_break/prompt_failure_diagnosis.py \
  --manifest out/attempts/TRY-0042/manifest.json \
  --prompt out/attempts/TRY-0042/prompt.txt \
  --image out/attempts/TRY-0042/source.png \
  --outdir out/attempts/TRY-0042/repair
~~~

此例預期選中 \`WRONG_CONTACT_FACE\`：下輪調整整把剛性武器的姿態／進入方向，使指定端面先接觸；凍結武器拓撲、頭柄接點、目標幾何、相機、人物與場景。它不會用「加強特效」掩飾側面碰撞，也不會把拓撲改成另一把槌。

其他已定義類型包括：\`GAP_REMAINS\`、\`INTERPENETRATION\`、\`WRONG_CRACK_ORIGIN\`、\`EARLY_CRACKS\`、\`HANDLE_TOPOLOGY_FAIL\`、\`CAMERA_OBSCURES_CONTACT\`、\`SCENE_CONTINUITY_FAIL\`、\`IDENTITY_DRIFT\`、\`RESIDENT_SAFETY_FAIL\` 和 \`FOLLOWTHROUGH_MISMATCH\`。有多個失敗時，診斷器列出全部原因，但先安排一個優先修正；其他失敗不能從報告中刪除。

### 證據邊界

診斷器**不會自己看懂像素**。它要求 reviewer 或經驗證的視覺審查程序提供結構化觀察，並要求 \`--image\` 指向的原圖 SHA-256 與 FAIL 收據完全一致。沒有原圖、收據遺失／不匹配、或觀察欄位仍是 \`UNVERIFIED\` 時，結果必須是 \`HOLD\`，不生成冒充有根據的修正方向。

本工具會產生 \`diagnosis.json\` 和附加修正段落的 \`repair_prompt.txt\`；它**不會自動呼叫外部圖像模型**。真正的下一輪仍須執行生成，之後以新 raster 重做同一套審查。若修正後問題未消失，不能升級為 PASS，也不能刪除上一輪失敗記錄。

## 已知涵蓋範圍與 CLI 選項

bubble_break/prompt_attempt_packet.py 已有五種輸入格式適配器：

| --format | 輸入 | 對應來源／用途 |
|---|---|---|
| matrix | variants[].prompts JSON | T-Hammer multiview 矩陣；每個 variant 的雙槌證明、H0、H2、H3 分別打包 |
| original-sin-jsonl | Original Sin generate.py 輸出的 JSONL | 每個 story/mode 的 H0–H3 與 storyboard cells |
| dense-atlas | CYLINDER_CROSS atlas manifest JSON | 單張密集候選圖 Prompt，核對 manifest 記載的 prompt SHA |
| dense-bubble | dense-hammer 的輸出目錄或 packet_summary.json | Stage A–E 與 D0–D4 的階段 Prompt Markdown |
| planted-bubble-packet | SHANNON_PLANTED_BUBBLE_PROMPT_PACKET.json | 每階段 request JSON 的 prompt、授權變量與必須保留欄位 |

例子（branch 和 commit 必須用真正產生輸入檔的版本，不可照抄示例值；以下路徑是按各生成器輸出位置示意）：

~~~bash
python bubble_break/prompt_attempt_packet.py --format original-sin-jsonl --input out/original_sin_bubble_break.jsonl --outdir out/prompt_packets/original_sin --branch feat/original-sin-bubble-break-engine --commit-sha ACTUAL_SOURCE_COMMIT_SHA
python bubble_break/prompt_attempt_packet.py --format dense-atlas --input out/cylinder_cross_dense_atlas/cylinder_cross_dense_atlas_manifest.json --outdir out/prompt_packets/cylinder_cross_atlas --branch feat/cylinder-cross-dense-atlas --commit-sha ACTUAL_SOURCE_COMMIT_SHA
python bubble_break/prompt_attempt_packet.py --format dense-bubble --input out/dense_hammer_bubble/packet_summary.json --outdir out/prompt_packets/planted_cylinder --branch feat/dense-hammer-bubble-pick --commit-sha ACTUAL_SOURCE_COMMIT_SHA
python bubble_break/prompt_attempt_packet.py --format planted-bubble-packet --input out/shannon_planted_bubble/SHANNON_PLANTED_BUBBLE_PROMPT_PACKET.json --outdir out/prompt_packets/shannon_planted_bubble --branch feat/gemini-planted-bubble-closed-loop-20261022 --commit-sha ACTUAL_SOURCE_COMMIT_SHA
~~~

These adapters normalize prompts, source paths/hashes, stage/topology IDs, expected geometry, numeric variables, and unverified observation fields into one manifest contract. They do not merge contradictory geometries; each adapter preserves its source topology. A branch with a different output schema still needs an explicit adapter and test before it can be called integrated.


## 試驗排程輸出

執行 `python bubble_break/prompt_trial_planner.py --outdir out/prompt_trials --limit 3`，會產生圖像公式、教學板與影片公式三張初始試驗卡及對照／試驗文字。這些是預先註冊的實驗計劃，不代表外部生成或像素審核已完成。
