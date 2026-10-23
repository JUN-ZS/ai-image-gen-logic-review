# 打泡圖像／影片 Prompt 公式總入口

本目錄將歷史草稿、武器拓撲分支、圖像生成公式和影片連續性規則整理成可選模組。先選物件拓撲，再選生成模式；不要把互相矛盾的武器描述混入同一個 Prompt。

## 新增：公式圖像 + 教學／驗收的雙輸出

每次嘗試的原始打擊圖保持乾淨；再用 `bubble_break/prompt_evidence_board.py` 把真實 attempt manifest 排版到教學／驗收板。這樣同一張圖可同時服務作品瀏覽、公式教學、變量比較與失敗追蹤，而數字不靠圖像模型手寫。

## 建議閱讀順序

1. [圖像 Prompt 公式教學](PROMPT_FORMULA_PLAYBOOK.md)：所有武器／打泡模式、可複製單圖 Prompt、負面約束與像素驗收。
2. [影片 Prompt 公式教學](VIDEO_PROMPT_FORMULA_PLAYBOOK.md)：10 秒時間軸、五個關鍵幀、母圖與遮罩、連續性硬閘門，以及三分鐘 MV 的敘事公式。
3. [所有 Draft 與 Branch 對照表](PROMPT_BRANCH_DRAFT_CROSSWALK.md)：21 個 branch refs、歷史 Prompt 草稿、互斥拓撲和證據狀態。

## 三個常見任務的正確入口

| 你現在要做什麼 | 選用路線 | 不要犯的混用錯誤 |
|---|---|---|
| 角色揮動 T 槌，指定端面打中泡泡 | B 線 T-Hammer H0/H1/H2/H3 | 不可用槌腰側面接觸，也不能讓柄像長矛穿過球心 |
| 圓柱底座貼住泡面，側柄中段施力 | A 線 planted-cylinder | 不可偷偷加外端同軸柄；不可同時聲稱底座貼住又有遠距空隙 |
| 先建立 10 秒連續動作，再做影片 | 影片公式 + 真實 keyframe closed loop | 不可用 montage／SVG proxy／synthetic raster 宣稱影片物理驗收通過 |

## 證據狀態不可混用

PROMPT_COMPILED ≠ GEOMETRY_TEST_PASS ≠ IMAGE_GENERATED ≠ PIXEL_AUDIT_PASS ≠ CONTINUITY_PASS ≠ VIDEO_AUDIT_PASS。

每次失敗都應保留原圖、SHA、失敗分類與修正變量；新一輪必須從最後一張 PASS 母圖開始。若所有候選都不合格，就 BLOCK，不可以降低接觸規則。
