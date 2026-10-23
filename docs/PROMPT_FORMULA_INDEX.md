# 打泡圖像／影片 Prompt 公式總入口

本目錄將歷史草稿、武器拓撲分支、圖像生成公式和影片連續性規則整理成可選模組。先選物件拓撲，再選生成模式；不要把互相矛盾的武器描述混入同一個 Prompt。

## 新增：公式圖像 + 教學／驗收的雙輸出

每次嘗試的原始打擊圖保持乾淨；再用 `bubble_break/prompt_evidence_board.py` 把真實 attempt manifest 排版到教學／驗收板。這樣同一張圖可同時服務作品瀏覽、公式教學、變量比較與失敗追蹤，而數字不靠圖像模型手寫。

## 建議閱讀順序

0. [下一輪試驗排程器](PROMPT_TRIAL_PLANNER.md)：先決定要比較哪兩個公式／版式、一次測哪個因素、需要多少真實樣本和什麼證據才能判定。
1. [Prompt Evidence Board 使用指南](PROMPT_EVIDENCE_BOARD.md)：每次生成的原始圖、變量封包和教學／驗收板；可輸出 standard／formula-first 版式。
2. [圖像 Prompt 公式教學](PROMPT_FORMULA_PLAYBOOK.md)：各互斥武器拓撲、單圖公式、負面約束和像素驗收。
3. [影片 Prompt 公式教學](VIDEO_PROMPT_FORMULA_PLAYBOOK.md)：10 秒時間軸、五個狀態、母圖與遮罩、連續性硬閘門和 MV 敘事公式。
4. [失敗診斷器](../bubble_break/prompt_failure_diagnosis.py)：整理 SHA 綁定的觀察；它是設計試驗的證據輸入，不是全流程的「下一步答案」。
5. [所有 Draft 與 Branch 對照表](PROMPT_BRANCH_DRAFT_CROSSWALK.md)：歷史 Prompt 草稿、互斥拓撲和證據狀態。

## 三個常見任務的正確入口

| 你現在要做什麼 | 選用路線 | 不要犯的混用錯誤 |
|---|---|---|
| 角色揮動 T 槌，指定端面打中泡泡 | B 線 T-Hammer H0/H1/H2/H3 | 不可用槌腰側面接觸，也不能讓柄像長矛穿過球心 |
| 圓柱底座貼住泡面，側柄中段施力 | A 線 planted-cylinder | 不可偷偷加外端同軸柄；不可同時聲稱底座貼住又有遠距空隙 |
| 先建立 10 秒連續動作，再做影片 | 影片公式 + 真實 keyframe closed loop | 不可用 montage／SVG proxy／synthetic raster 宣稱影片物理驗收通過 |

## 第一輪不是一句「改這裡」，而是三條可比較的試驗

預設先比較：圖像的簡短接觸描述 vs 明確幾何契約；同一 raster 的 standard vs formula-first 教學板；以及單段 10 秒影片描述 vs 五個定時狀態契約。每條都固定其餘條件、分出 control/treatment，並預先寫明硬閘門和判定規則。真正生成與真實媒體審查仍是獨立步驟。

## 證據狀態不可混用

PROMPT_COMPILED ≠ GEOMETRY_TEST_PASS ≠ IMAGE_GENERATED ≠ PIXEL_AUDIT_PASS ≠ CONTINUITY_PASS ≠ VIDEO_AUDIT_PASS。

每次失敗都應保留原圖、SHA、失敗分類與修正變量；新一輪必須從最後一張 PASS 母圖開始。若所有候選都不合格，就 BLOCK，不可以降低接觸規則。
