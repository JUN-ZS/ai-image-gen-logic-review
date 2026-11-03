# 下一次要試什麼｜Image Formula、圖像教學、Video Prompt 試驗排程

## 目的不是判定「應該改哪裡」

失敗診斷只整理已審查的畫面證據；它不是整個創作流程的下一步，也不能把單張失敗自動當成唯一原因。真正的下一步應該是預先定義的**試驗**：有對照組、有試驗組、一次只改一類變量、保留其他條件、在出圖前寫明判定方式。

入口程式：bubble_break/prompt_trial_planner.py

~~~bash
python bubble_break/prompt_trial_planner.py --outdir out/prompt_trials --limit 3
~~~

這會為第一輪產生三張獨立試驗卡，並輸出每條的 control/treatment 文本、試驗目的、凍結項、樣本數、判定規則和所需證據。預設三條分別涵蓋圖像 Prompt 公式、圖像教學板、影片 Prompt 公式。它只排程，不呼叫圖像／影片後端。

## 第一批應做的三項

### IMG-FORMULA-01 — 圖像公式

- **A 對照：**短版自然語言描述。
- **B 試驗：**明確指定 active surface、接觸點 P、既定碰撞法線 n、H0/H2/H3 幾何狀態，以及禁止槌腰側面／角／柄先碰。
- **只變：**接觸契約文字區塊。
- **凍結：**武器拓撲、角色、球體、鏡頭、場景、光線、種子政策和特效預算。
- **樣本：**每組 3 張實際生成圖。
- **判定：**完整通過物理與拓撲硬閘門的張數；每一種失敗另外計數。試驗組須至少多 2 張全閘門通過，而且不能帶來新的拓撲／受保護居民安全失敗，才算初步勝出。3 張只是篩選，不是統計證明。

### IMG-TEACH-01 — 圖像教學板

- **A 對照：**現有 standard evidence board。
- **B 試驗：**同一 manifest、同一張 source raster 的 formula-first 教學板；先展示「OUTPUT → TOPOLOGY → CONTACT → ACTION → CAMERA → LIGHT/FX → NEGATIVES」，再展示本次試驗變量。
- **只變：**標註板版式。A、B 的來源圖像 SHA 必須相同，不能重新生成圖片。
- **樣本：**3 張實際來源圖，每張都產生兩種版式。
- **判定：**盲讀者能否正確找出拓撲、接觸面、單一試驗變量、預期／觀察差異和下一項試驗；逐張比較，不用美觀喜好代替教學正確性。

生成兩種版式：

~~~bash
python bubble_break/prompt_evidence_board.py --manifest out/TRY-0001/manifest.json --image out/TRY-0001/source.png --teaching-layout standard --out out/TRY-0001/board_standard.svg
python bubble_break/prompt_evidence_board.py --manifest out/TRY-0001/manifest.json --image out/TRY-0001/source.png --teaching-layout formula-first --out out/TRY-0001/board_formula_first.svg
~~~

公式優先版只改教學板的排版文字，不改源圖像素；兩版都必須保存 source-raster SHA 及同一份 review 來源。

### VIDEO-FORMULA-01 — 影片 Prompt 公式

- **A 對照：**單段 10 秒敘述式 Prompt。
- **B 試驗：**五個時間狀態明確分段：0–2 秒 PRE_FAR、2–4.5 秒 PRE_NEAR、4.5 秒 CONTACT、4.5–7 秒 E_MID、7–10 秒 E_END。
- **只變：**時間／狀態契約的組織方式。
- **凍結：**人物身份與服裝、武器拓撲、球體幾何、P、場景地標、鏡頭 rig、光向和安全條件。
- **樣本：**每組 3 條真實影片。若沒有可呼叫的連續影片生成器，可改為五張獨立關鍵幀測狀態遵守度；這不等同影片連續性通過。
- **判定：**接觸時間、接觸前空隙、裂源 P、裂紋向外傳播、身份與場景穩定、內部聖所安全均需逐項檢查。

## 第二批（必須先審查第一批）

- VIDEO-CONTINUITY-02：比較文字式「保持一致」與 parent-frame SHA、master anchor、authorized delta／frozen fields 的連續性契約。
- VIDEO-CAUSALITY-03：比較泛化「槌擊碎泡泡」與有時間順序的「接觸 → P 首裂 → 向外傳播 → 外殼碎裂」。
- IMG-CAMERA-02：僅在圖像公式第一輪完成後，比較現有鏡頭與較易檢查接觸 seam 的三分之四視角；世界座標中的槌、球、P、法線都凍結。

排程器會在 history 提供完整證據後解鎖依賴項；未審查、收據 SHA 不一致或每組樣本不足的試驗不會被當成已完成，也不會因為文字寫了 PASS 就跳到下一批。

## 記錄試驗結果

history 的根物件格式是：

~~~json
{
  "schema_version": 1,
  "reviewed_trials": []
}
~~~

每個已完成 trial 應放入 reviewed_trials，內含 trial_id 與 evidence 陣列。每個 evidence 記錄一個 arm（control 或 treatment）、artifact_sha256 和 review_receipt；收據要有相同的 artifact_sha256 及 verdict（PASS／FAIL）。每組至少 3 份合格收據後，排程器才會把該 trial 視為已審查。SHA 綁定只確保收據聲稱檢查的是哪個 artifact，不會認證審查者身份，也不會讓排程器自動看懂圖像或影片。

~~~bash
python bubble_break/prompt_trial_planner.py --history out/reviewed_trial_history.json --outdir out/prompt_trials_next --limit 3
~~~

所有新計劃都標示 plan_only=true、external_generation_called=false。每個試驗的 control/treatment 文本是待執行的試驗材料，不是生成器已經執行、也不是某一公式已經獲勝的證明。
