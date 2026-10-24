# SET-G · Axis A Full · Settings drop

- `../USER_REQUIREMENTS_LOCKED.md` — 用戶硬規則
- `../CURRENT_SETTINGS_SETG_AXIS_A.json` — 當前 SET 設定
- `axis_a_full/AXIS_A_FULL_MAP.csv` — 11 法 · 打擊面/受面/力/隙
- `METHOD_TEXT_MANIFEST.csv` — 字樣冷熱與 LOOP
- `LOOP_SHA_INDEX.txt` — L- 與 MID SHA
- `FACE_ANALYSIS_HUB.json` — 面分析模板
- `axis_a_full/SHA256_PRE_MID_POST_LABELED.txt` — 標字三幀指紋

**說明：** 本分支優先推設定與映射。大圖 JPEG 留在 Grok artifacts（`boundary_pedestrian_setG_gold/`），避免 repo 膨脹；需要時再 LFS／Release。

每法固定 **PRE | MID | POST**；字 PRE 冷 / POST 熱；HUB 分析行寫進畫面。
