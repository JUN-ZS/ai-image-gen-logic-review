# 所有 Prompt Draft 與 Branch 對照表｜2026-10-23

> Repository：JUN-ZS/ai-image-gen-logic-review  
> 核對方式：查閱 main 樹、20 個現存 branch refs、主 Prompt 歷史檔、各路線規格／審查文件與部分 commit metadata。以下 SHA 是本次核對時 branch tip；後續 push 會變動。這份表不代表每個歷史 ZIP 內的二進位資料已全部解包逐項閱讀。

## 1. 統一結論

分支不是同一個 Prompt 的「一代比一代好」。它們處理不同層級：

- 敘事層：將抽象主題轉成可拍事件，編排 6 幕、24 張關鍵卡或 50–54 個 MV 鏡頭。
- 物件拓撲層：T 槌、厚十字槌、雙頭側柄圓柱、線形棒、徑向多面圓頭是不同模型。
- 接觸層：終端端面、泡面底座、外側圓端蓋或刻意錯面，各自有不同接觸契約。
- 生成管線層：幾何／Prompt 編譯、真實出圖、母圖與遮罩、跨幀連續性、像素審查收據。
- 證據層：PROMPT_PASS／geometry-test PASS／SVG proxy PASS 都不能自動代表 IMAGE_GENERATED、PIXEL_AUDIT_PASS 或 VIDEO_AUDIT_PASS。

整合不是將不同句子摻在一起，而是將每個 branch 建成可選模組、使相互矛盾的模組互斥，並統一錯誤分類、回滾方式與證據標籤。

## 2. 20 個 branch tip inventory

| Branch | Tip SHA | 主題／來源 | 整合判斷 |
|---|---|---|---|
| main | 03934ba4f147e5f85937068e1113f2f62198f8e6 | 主線；包含 planted-bubble workflow、T-Hammer multiview spec、失敗改寫 log、L1–L5 layered wash audit | 新文件從此基線分出，不直接改 main |
| feat/cylinder-cross-dense-atlas | 478d023c1c5bd225fd2c9a678dcafe47d3ab92ee | 厚十字／CYLINDER_CROSS 稠密候選 atlas 與端面接觸矩陣 | 雙槌幾何取樣路徑；atlas 不是像素 PASS |
| feat/dense-hammer-bubble-pick | a09451d898ee46d08bbf8e0ca7e2cd55367a4080 | 雙頭圓柱種植泡面、側柄、候選選取、D0–D4、接觸效果與 FAIL/PASS/REWRITE log | planted-cylinder 主路徑；保留 NO_NEW_HANDLE 與既有柄鎖 |
| feat/dual-actor-correct-vs-inverse-strike | 691cc4c8a8ffc1ffc64c851a3ad8c188648521dd | 兩支細直擊打棒以 90° 相交，正確面接觸 vs 刻意錯面負控制 | 幾何判別實驗；不混入主角持槌線 |
| feat/dual-t-hammer-collision-contract | 78e0b2f06284d4b822bb54cd2214cad27ac50c62 | 兩把獨立 T 槌的指定端面相撞契約 | 端面幾何對照；實際 raster 仍需單獨審核 |
| feat/efv-song-story-expansion | 45cd690728a22ca9d9ba6395262276ae484058f5 | 將 EFV／Gumen Rock 敘事動機轉為 Original Sin story prompt compiler | 敘事母層，不可覆蓋物理真值 |
| feat/efv-song-story-expansion-main | c4b13ce327c612c3fac56ba902b1763e123e4cb2 | Story expansion workflow／CI 整合 | 敘事流程整合，非新接觸拓撲 |
| feat/gemini-closed-loop-partial-20261022 | 7601977a7bb9dc2972afb6bb68c58484a5001bf7 | Gemini 多輪匯入、程式 chips、v2–v5.1 ZIP 與 manifest | 來源 provenance；封存 ZIP 未全部展開前不可說成逐項驗收完 |
| feat/gemini-planted-bubble-closed-loop-20261022 | f6646a8cf6a9b1c63ca3be675968f91e50607663 | planted-bubble 七階段產物、manifest、raster／mask | 實際候選證據來源；manifest 把 code visual acceptance 留為 NOT_VERIFIED_BY_CODE |
| feat/imagine-planted-bubble-h9-20261022 | c6b01900cfce92ecf80d6555233dd0d80927902c | H9 planted-bubble 階段 raster alias 相容修正 | 一條候選生成支線；視覺 PASS 必須查當次原始 raster 與 manifest |
| feat/layered-divine-hammer-wash-audit-20261023 | f8a1d2c862d207138e383f5c2c8731c0c247dbd2 | 10 格雙槌洗圖診斷；L1–L5 逐層重審與跨格變量排他 | 稽核程式／文件已見於本次 main；歷史多格輸出不能因描述稱端面就當成端面 PASS |
| feat/original-sin-bubble-break-engine | a7b58d50b59263db35da9c4400724a4487fc1ccc | 故事 engine、H0/H1/H2/H3、P 與 shell-only breach | 敘事因果與 T 槌打泡可複製路線 |
| feat/sphere-cylinder-pick-and-attach | ab8ad2b535b2c83253c95a164c0eb17ccfb85c30 | 25 個球面圓柱候選、選取、加柄／人物、動作、泡泡破裂 | 其柄接在圓柱外端，與側柄中段方案互斥；應視作另一拓撲版本 |
| feat/t-hammer-inversion-pair | d6cefa2ca90f28717e7c0c562ec9bc130afa7f6c | 正確端面接觸 vs 刻意以 broad cheek／sidewall 先接觸的負控制 | 正、負控制分離；EXPECTED_FAIL 不得計 PASS |
| feat/v5-continuity-autonomous | 37e1ec806eae590690acf77e914cca533ec78522 | V5 自主流程與 continuity workflow 同步 | 歷史 lineage；須參照 V5.1 review 對 synthetic raster／未真正重跑的修正 |
| feat/v5.1-closed-loop-continuity | 172f665216d95d0756a03c428d0e54b989456bd4 | SceneState、authorized delta、真實 backend、五關鍵幀與兩層評分 | 影片／跨幀主規格；硬閘門優先於創意排序 |
| fix/gemini-planted-bubble-continuity-gates-20261022 | f951f44297489fd4f240c277247782d5935bcba8 | Gemini provider 回傳被實際審查的 composed raster | 防止審 raw 圖、交付另一張 composed 圖 |
| fix/shannon-closed-loop-integrity-20261022 | 4dec663a3d4733018aff4c07e90a1c49c4f31b25 | Closed-loop provenance、ranking 與 runner contract 測試 | 證據與重跑完整性，不是新幾何模型 |
| fix/shannon-planted-bubble-closed-loop-20261022 | b523337ce5a7a9546429fe249556d6eac2413d1e | 七階段 planted-bubble continuity 失敗與修復審查 | 保留 montage 的跳景、P 不一致與居民安全不可證等 fail evidence |
| fix/v5-continuity-evidence-gates | 636a221e9cb3f06aac2cf60a7aa4816b7dd31dfa | 驗證實際 serial D3 wash JSON artifact | 證據閘門；artifact 存在不等於圖片 PASS |
| fix/v5.1-truthful-keyframe-gates | 1f90e99ae8b2484c0120332218a0fb4ec1247884 | Truthful keyframe／raster-bound collision audit 調整 | 關鍵幀證據綁定；最終仍要審實際 raster |

Branch tips 有分歧與先後；這是來源索引，不代表各 branch 都已合併、Actions 全 PASS 或所有外部圖片都驗收過。

## 3. Draft／對話存檔的統一對照

### 槌1.txt — 早期 50 鏡故事草稿
價值：六幕隱喻與可拍物件——保護、窒息、共業、止痛、覺醒、選擇。限制：文字能提供敘事，但不能鎖住槌頭第一接觸面。

### 槌2.txt — Prompt 成長記錄與可複製公式
價值：S0–S13 演進、L0–L6 層次、角色／影像契約、k=0 核心、武器 A/B/C 選項、負面詞和像素審查。主公式：

~~~text
SHOT = CONTRACT + HERO + GEAR + ACTION + WEAPON + TARGET + SET + CAM + LIGHT + GRADE
~~~

同一 Prompt 的 WEAPON 只能選一項：正交厚十字、乾淨 plus-sign，或多向平坦槌面圓頭。後來的 planted-cylinder 與 T-Hammer 是新增而且互斥的拓撲模組，不能用舊草稿抹平其差異。

### 問.txt — 第三方盲讀／Seed-Field 設計
價值：陌生讀者從 repo、Git history、seed、field 與既有 outputs 獨立發現未明寫關係，而不是複述期待答案。可當作 Prompt 手冊的盲測：先提供目標和原圖，不提示正確接觸面答案，再記錄盲讀者辨認出的關係與分歧。

### Gemini / Shannon / V5 / V5.1 資料
- Gemini import 記錄記載 v2、v3 anthology、v4 full-lock、v5 continuity、v5.1 closed-loop 等 ZIP 保留原始封存。未展開的 ZIP 不能宣稱已逐頁解讀。
- V5.1 review 的方向是從最後 PASS 母圖、真實 backend、edit/freeze mask、每幀授權變更欄位與真實生成結果做 closed loop。
- Shannon-inspired 文件只借用冗餘、雜訊、回饋與回滾的工程類比；不宣稱圖像模型已被證明為具已知容量的 Shannon channel。
- Shannon 七階段 audit 明確拒絕把構圖跳變、接觸點不一致或內部聖所狀態不明的 strip 當作 continuity 證據。

## 4. 主要來源路徑

主線：
- [雙頭圓柱泡泡選取與 D0–E 工作流](../bubble_break/DENSE_HAMMER_BUBBLE_SELECTION_WORKFLOW.md)
- [T-Hammer 多視角／擺動規格](../bubble_break/T_HAMMER_MULTIVIEW_SWING_ENGINE_SPEC.md)
- [歷次 FAIL／PASS／Rewrite log](../bubble_break/logs/STAGE_FAILURE_SUCCESS_REWRITE_LOG.md)
- [10 格雙槌洗圖自審規格](../docs/layered_divine_hammer_wash/self_audit_10wash_failure_and_layered_lock_spec.md)

分支資料：
- [CYLINDER_CROSS dense atlas handoff](https://github.com/JUN-ZS/ai-image-gen-logic-review/blob/feat/cylinder-cross-dense-atlas/bubble_break/CYLINDER_CROSS_DENSE_ATLAS_HANDOFF.md)
- [T 槌對泡泡真實場景工作流](https://github.com/JUN-ZS/ai-image-gen-logic-review/blob/feat/cylinder-cross-dense-atlas/docs/REAL_SCENE_BUBBLE_BREAK_WORKFLOW.md)
- [T-Hammer 正／負控制規格](https://github.com/JUN-ZS/ai-image-gen-logic-review/blob/feat/t-hammer-inversion-pair/bubble_break/T_HAMMER_INVERSE_CONTRAST_SPEC.md)
- [線形棒 correct-vs-inverse 公式](https://github.com/JUN-ZS/ai-image-gen-logic-review/blob/feat/dual-actor-correct-vs-inverse-strike/bubble_break/DUAL_ACTOR_CORRECT_VS_INVERSE_FORMULA.md)
- [V5 → V5.1 continuity／real rerun review](https://github.com/JUN-ZS/ai-image-gen-logic-review/blob/feat/gemini-planted-bubble-closed-loop-20261022/bubble_break/V5_CONTINUITY_AND_CREATIVITY_REVIEW.md)
- [Shannon planted-bubble continuity audit](https://github.com/JUN-ZS/ai-image-gen-logic-review/blob/fix/shannon-planted-bubble-closed-loop-20261022/docs/SHANNON_PLANTED_BUBBLE_CONTINUITY_AUDIT.md)
- [Prompt 歷史主檔：槌2.txt](https://github.com/JUN-ZS/ai-image-gen-logic-review/blob/main/%E6%A7%8C2.txt)
- [早期 50 鏡草稿：槌1.txt](https://github.com/JUN-ZS/ai-image-gen-logic-review/blob/main/%E6%A7%8C1.txt)
- [盲讀／Seed-Field 筆記：問.txt](https://github.com/JUN-ZS/ai-image-gen-logic-review/blob/main/%E5%95%8F.txt)

## 5. 狀態標籤：不能互相冒充

- PROMPT_COMPILED：Prompt 含有規定欄位與文字。
- GEOMETRY_TEST_PASS：程式的向量、距離或資料契約檢查通過。
- SVG_PROXY_PASS：幾何代理可生成。
- IMAGE_GENERATED：存在真實外部生成的原始 raster。
- PIXEL_AUDIT_PASS：reviewer 審查的是同一張最終 raster，且收據綁定其 SHA-256。
- CONTINUITY_PASS：身份、場景、錨點、父圖與授權變更通過跨幀檢查。
- VIDEO_RENDERED：實際影片檔存在且可播放；不代表物理接觸已通過。
- VIDEO_AUDIT_PASS：影片的關鍵幀／時間因果審查通過。

任何狀態不可自動推導為下一個狀態，尤其不能用綠色 CI 代替實際像素驗收。

## 6. 後續工程落點

若把公式轉成 JSON/YAML schema，按拓撲分開，避免互相矛盾：

~~~text
planted_cylinder_side_handle
t_hammer_terminal_face
cylinder_cross_cap_pair
line_striker_orthogonal_negative_control
radial_multi_face_round_head
~~~

每個 run 建議記錄 topology_id、parent_raster_sha256、authorized_delta_fields、contact_point_id、image_realization、pixel_audit 和 rejection_reasons。如此可以測出哪種分支假設真能提高命中率，而不是把所有歷史 Prompt 連成一條越來越長、互相打架的文字。
