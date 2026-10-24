

---

*User prompt: 你明白我想要的極致VIDEO 幀的 故事變體嗎 https\://chatgpt.com/share/6adcdd6a-b328-83ec-9ef3-c98746074119 我已把《邊界行人》從「不同方法的圖片集合」推進成同一故事不斷輪迴、每輪試法不同、畫面內有藝術字標示方法的完整提示詞工作流。 1\. 六幕故事持續輪迴 《邊界行人》無限輪迴故事規格 畫界 → 保護 → 試法／碎裂 → 假修 → 一界 → 選擇，再由結尾接回開場。角色、世界和因果保持連續，每輪改變拓撲、接觸狀態、鏡頭、風格或影片方法。 2\. 全量 3,723 個變體編成六幕故事 新增 輪迴 Prompt 編譯器，將每個合法變體編成獨立 LOOP／TRY，輸出六幕各自完整的 IMAGE／VIDEO Prompt。 3,723 個變體編號 22,338 幕級完整提示詞 每輪只把主試法放進相應的那一幕，其他五幕延續故事，不會把互相矛盾的武器或接觸規則混在一起。 3\. 方法名稱直接成為作品中的藝術字 新增 TRY 藝術字疊加器。它會把確定的文字排版成 SVG 圖層，影片則可使用 ASS 字幕層。 每張作品可以標出故事名、LOOP 編號、TRY 編號、幾何／接觸方法、鏡頭、風格、Prompt ID 和審核狀態。原始圖片與藝術字版分開保存，並記錄 SHA-256。 關鍵是：由排版器精確寫出方法名稱，不靠生成模型自行拼字。未經實際檢查的作品會保留待審狀態，不會因為有漂亮標籤就被當成成功。 審核結果 GitHub Actions：SUCCESS Run \#40095092956 · HEAD SHA：73fc397376357297107f51384f540e1772476920 查看完整執行紀錄與產物 實際執行已確認 3,723 個變體全部編譯，並產出 22,338 個幕級 Prompt；新增的測試和藝術字示例渲染均通過。 下載完整輪迴 Prompt 封包 封包包含 loop\_prompt\_packets.jsonl、loop\_index.csv、loop\_plan\_summary.json，以及藝術字 SVG 和影片 ASS 示例。 編譯器第一次全量執行時，還找出 192 個重複的 FRONT 變體 ID。我已將 H2 四鏡包的相關 ID 加上 \-IMPACT4-FRONT 後綴，並同步修改兩份 CSV；現在是 3,723 列、3,723 個唯一 ID，完整編譯通過。 目前仍須清楚區分：這代表全部變體的六幕提示詞已編譯，不是 3,723 組圖片或影片已全部生成、也不是幾何接觸已全部驗收。既有的 15 張輪迴故事抽樣圖鑑 是故事示例，與全量 Prompt 封包不同。 整個變更留在 PR \#9，仍是 Draft，沒有合併到 main。 github.com/JUN-ZS/ai-image-gen-logic-review/blob/docs/docs/boundary\_pedestrian/LOOPING\_TRY\_STORY.md github.com/JUN-ZS/ai-image-gen-logic-review/blob/docs/bubble\_break/boundary\_pedestrian\_loop\_planner.py github.com/JUN-ZS/ai-image-gen-logic-review/blob/docs/bubble\_break/boundary\_pedestrian\_try\_art.py github.com/JUN-ZS/ai-image-gen-logic-review/actions/runs api.github.com/repos/JUN-ZS/ai-image-gen-logic-review/actions/artifacts/zip github.com/JUN-ZS/ai-image-gen-logic-review/tree/docs/docs/boundary\_pedestrian/reincarnation\_try \#9 顯示更多 這是《邊界行人》輪迴 TRY 工作流的重大推進。我先讀 JUN-ZS 場憲與相關技能，再對照你給的 PR \#9、編譯結果與連結，確認狀態與下一步。 正在從 GitHub 拉取 PR \#9、Actions 與關鍵文件的實況。 狀態對照（已從 GitHub 實拉） 項目 結果 PR \#9 open · Draft · 未 merge · mergeable\_state: clean HEAD 73fc397376357297107f51384f540e1772476920 branch docs/unified-image-video-prompt-formulas-20261023 → main Actions \#40095092956 completed / success · workflow: Prompt Evidence Board and Trial Planner Artifact prompt-trial-plan-and-teaching-board · \~7.3 MB · 未過期 全量 ID VARIANT\_IDS\_FULL\_SUMMARY.json → total\_ids: 3723 · 含 \-IMPACT4-FRONT 註記 你的宣稱與倉庫現況對得上，且證據等級分得清楚——這是關鍵。 已鎖定（OBSERVED） 六幕輪迴 DNA 畫界 → 保護 → 試法／碎裂 → 假修 → 一界 → 選擇，ACT6 match-cut 接 ACT1。 文件：docs/boundary\_pedestrian/LOOPING\_TRY\_STORY.md Prompt 編譯器 bubble\_break/boundary\_pedestrian\_loop\_planner.py 一變體 \= 一 LOOP/TRY；僅主試法所在幕承載該方法；其餘五幕是故事脊柱，不混武器／接觸規則。 CI 斷言：3723 packets × 6 acts \= 22338 幕級 prompt；PROMPT\_READY；external\_generation\_called: false TRY 藝術字層 boundary\_pedestrian\_try\_art.py：SVG \+ ASS \+ sidecar SHA-256 字由排版器寫死，不靠模型拼字；預設 REVIEW\_PENDING / NOT\_RUN / NOT\_VERIFIED ID 完整性 192 個 H2 四鏡 FRONT 與 T192 FRONT 碰撞 → 已加 \-IMPACT4-FRONT；現 3723 列 / 3723 唯一 ID 桶分布（摘要） SOFT 81 · T192 2304 · H2\_IMPACT4 768 · DUAL48 288 · ROD/MULTI/PLANT… · VIDEO 桶合計 60 明確未宣稱（與你文案一致） 狀態 現況 3723 組 IMAGE/VIDEO 已生成 否 · NOT\_RUN 幾何接觸驗收 否 · PIXEL\_AUDIT NOT\_RUN 視覺通過 否 · VISUAL\_ACCEPTANCE NOT\_VERIFIED 15 張輪迴抽樣圖鑑 故事示例，≠ 全量封包 merge to main 否 · 仍 Draft 這符合場憲：Hyp ≠ Obs；PROMPT\_READY 不可冒充 PIXEL\_AUDIT\_PASS。 證據鏈入口 PR：https\://github.com/JUN-ZS/ai-image-gen-logic-review/pull/9 Run：https\://github.com/JUN-ZS/ai-image-gen-logic-review/actions/runs/40095092956 聖經：LOOPING\_TRY\_STORY.md 編譯器 / 字牌：boundary\_pedestrian\_loop\_planner.py · boundary\_pedestrian\_try\_art.py 可選下一閘（你點名才動） Ready for review — 標 PR 出 Draft（仍不 merge） 抽樣生成 — 先跑小 limit（例如每桶 1–2 個）→ 底圖 \+ 藝術字 → 人審 SHA 下載 artifact 本地核對 loop\_plan\_summary.json 計數 SWEEP-001 排程表 — 交錯桶順序的實際出圖佇列（仍標 NOT\_RUN） 需要我做哪一項，直接說編號即可。 試出一輪迴 好，先從倉庫拉一輪完整 LOOP 的編譯材料與角色參考，再產出六幕畫面。 下載角色參考、樣本變體與編譯器，編成一輪 LOOP 後再出六幕圖。 選 LOOP-0003（GEO.T · H2 首次接觸）作為本輪主試法，接著用角色參考出六幕圖。 開始生成 LOOP-0001 六幕；ACT3 為主試法 GEO.T · H2。 六幕底圖已出。接著存檔、寫 manifest，並為主試法 ACT3 疊上確定性藝術字。 LOOP-0001 已試出一輪 主試法（ACT 3）：GEO.T · H2 · X\_RIGHT/CAM01/M1 · S-01 變體：BP-3H-T-H2-…-IMPACT4-FRONT 狀態：IMAGE\_GENERATED · REVIEW\_PENDING · PIXEL\_AUDIT NOT\_RUN · 不宣稱幾何 PASS 六幕總覽 幕 事件 角色 ACT 1 畫界 — 沿發光邊界行走 脊柱 ACT 2 保護 — 捧住內在生命球 脊柱 ACT 3 試法／碎裂 — T 槌端面首次接觸 主試法 ACT 4 假修 — 金箔假繃帶 \+ 社交假安全 脊柱 ACT 5 一界 — 天台紅線與包紮 脊柱 ACT 6 選擇 — 不閉合光環，接下一輪 脊柱 ACT 1 · 畫界 ACT 2 · 保護 ACT 3 · 試法／碎裂（主試法 · 底圖） ACT 3 · 藝術字版（確定性疊字 · 非模型拼字） ACT 4 · 假修 ACT 5 · 一界 ACT 6 · 選擇（match-cut 接口） 誠實邊界 已做 未做 編譯器抽出 1 輪 HARD H2 封包 像素幾何驗收 角色參考鎖定臉 連續性正式審 六幕 IMAGE 生成 \+ SHA 3723 全量出圖 ACT3 SVG/ASS 字牌 \+ raster 標籤 標 HUMAN ACCEPTED 產物目錄：boundary\_pedestrian\_loop0001/ （底圖、prompt、generation\_manifest.json、labeled SVG/ASS） 可下一步（你點名） 人審 ACT3 — 查 T 槌拓撲、端面接觸、裂紋起點 下一輪 — 換 GEO.PLANT\_S / ROD / T2 等 ACT3 短片 — 由底圖做 6s I2V 補標 — 其餘五幕也疊 TRY 藝術字 要哪一項直接說。 下一輪 下一輪改主試法：GEO.T2 · FACE（雙 T 槌端面相對）。先抽出封包並沿用 LOOP-0001 角色連續性。 下一輪主試法為 雙 T 槌端面相對（GEO.T2 · FACE）。以 LOOP-0001 連續性為基準生成六幕。 ACT3 出現雙女主（違反「同一人」DNA）。重試一版：單女主 \+ 雙 T 槌端面相對。 LOOP-0002 已出 接在 LOOP-0001 · GEO.T · H2 之後。 本輪主試法差異：拓撲 T → T2（兩把獨立 T 槌）· 接觸 H2 → FACE（兩端平面對面相接，不融成 H） 變體 BP-3H-T2-FACE-H\_LR\_\_CAM01\_GRAZING\_FACE-W00-S01-FRONT METHOD GEO.T2 · FACE · H\_LR/CAM01 · W00 · S01 狀態 IMAGE\_GENERATED · REVIEW\_PENDING · 不宣稱幾何 PASS 六幕總覽 ACT 1 · 畫界（接上一輪不閉合光環再返） ACT 2 · 保護 ACT 3 · 試法／碎裂（主試法 · 底圖） ACT 3 · 藝術字版 ACT 4 · 假修 ACT 5 · 一界 ACT 6 · 選擇（再留 match-cut 接口） 本輪誠實紀錄 項目 說明 相對 LOOP-0001 單 T 端面打球 → 雙 T 端面相對；故事脊柱延續 ACT3 第一次 產出雙女主 → 違反「同一人」DNA → 標 REJECT 存檔 ACT3 重試 單女主 \+ 兩把獨立 T · 端面相接 · 球在接觸區 待人審 是否仍像「兩把獨立 T」而非 H；柄與端面是否乾淨；是否無穿透 產物：boundary\_pedestrian\_loop0002/（含 generation\_manifest.json、REJECT 雙人版） 下一輪候選（交錯桶） GEO.ROD · POS GEO.MULTI · H0 GEO.PLANT\_O GEO.PLANT\_S 要第幾輪直接說；或指定方法 ID。 太單一了, 是要 : 'IMAGE｜物件幾何與接觸方式 包括 T 槌母版、H0／H1／H2／H3，雙 T 槌端面互撞、厚十字槌圓端蓋互撞、90° 線形棒正反控制、側柄種植圓柱、外端接柄圓柱，以及多向扁平面圓頭。每種保持各自獨立的完整 Prompt。' X ' 'IMAGE｜鏡頭、動作與美術變體 包括 192 種 T 槌多視角／蓄力組合的選擇方式、48 種雙槌接觸矩陣、十種獨立洗圖構圖，以及寫實電影、可愛 INS／粉彩和超現實隱喻的風格段落。鏡頭變化不能偷偷改掉接觸幾何。 ' X 'VIDEO｜時間軸與閉環生成 包括 10 秒單場景短片、五張各自完整的關鍵幀 Prompt、以通過母圖為基礎的 Image-to-Video、固定泡面接觸點的 planted-cylinder 影片、雙槌／厚十字／線形棒影片，以及三分鐘 MV 的六幕逐段生成路線。' X '敘事 IMAGE／VIDEO｜《邊界行人》 六幕各有完整的圖像 Prompt 與影片片段 Prompt：畫界、保護、碎裂、假修、一界、選擇。柔性敘事畫面不會硬塞武器接觸，真正打擊場景則使用專用幾何 Prompt。' 的 邊界行人 全部可一起乘出來的大量變體 顯示更多 明白：先前兩輪太像同一套敘事分鏡，不是「方法空間相乘」的大量變體。我先對齊全量合法乘積結構，再按桶抽樣展開。 對齊了：全量是 方法空間相乘（3,723 合法變體），不是同一套六幕故事複印。正在生成「方法矩陣抽樣板」——每格一種獨立幾何／接觸／風格，互不混用。 生成硬幾何矩陣抽樣（各方法獨立 Prompt，不混接觸規則）。 你要的不是「同一故事複印」，是 方法空間相乘 先前 LOOP-0001／0002 確實太單一：同一套六幕敘事外殼，只換一個 ACT3 試法。 你要的是這四層 可合法一起乘 的全量變體（倉庫已編成 3,723 個唯一 ID）： 乘積公式（已對齊 VARIANT\_IDS\_FULL） 軸 內容 規模（合法列） A · 物件幾何 × 接觸 T×H0/H1/H2/H3 · 雙T FACE · 厚十字 FACE · ROD POS/NEG · PLANT\_S · PLANT\_O · MULTI 見下桶 B · 鏡頭／蓄力／洗圖／風格 T192（8軸×12鏡×2蓄力）· DUAL48 · WASH W01–W10 · S01寫實／S02粉彩／S03超現實 相機不得改寫接觸律 C · VIDEO 時間軸 V-01 10s · V-02 KF5 · V-03 plant · V-04 I2V · 各拓撲片 · V-09 六幕MV段 60 VIDEO 列 D · 敘事六幕 畫界→保護→試法→假修→一界→選擇；硬接觸只在主試法幕，柔性幕不塞武器 編譯後 3,723 × 6 \= 22,338 幕級 Prompt 桶計數（= 3,723） HARD\_T\_192        2304   ← 4H × 8軸 × 12鏡 × 2蓄力 × 3風格 HARD\_T\_H2\_IMPACT4  768   ← H2 四鏡包（含 \-IMPACT4-FRONT 消歧） HARD\_DUAL48        288   ← T2 \+ CROSS 接觸矩陣 SOFT\_IMAGE          81   ← 六幕柔性 × 風格／分鏡 HARD\_PLANT\_S        72 HARD\_ROD            60 HARD\_MULTI          60 HARD\_PLANT\_O        30 VIDEO\_GEO           24 VIDEO\_I2V           18 VIDEO\_BP            18 規則仍是： 一變體 \= 一組獨立完整 Prompt · 硬幾何互不混用 · 輪迴編譯時只把主試法放進指定幕。 方法矩陣抽樣板（跨軸 · 不是再跑一輪同一六幕） 格 方法（各有獨立契約） 01–04 T · H0 → H1 → H2 → H3（遠隙／近隙／首次端面／跟進） 05 T2 · FACE 雙獨立 T 端面相對（不融 H） 06 CROSS · FACE 厚十字圓端蓋互撞 07–08 ROD · POS／NEG 90° 正控制 vs 預期失敗 09–10 PLANT\_S 側柄 vs PLANT\_O 外端柄（錨定≠飛槌） 11 MULTI 多向扁平頭選面 H2 12–13 SOFT S02 粉彩／S03 超現實（柔性，不塞武器） 14 WASH W04 低掃構圖 × ROD（鏡頭變，接觸律不變） 單格展開 T · H0 / H1 / H2 / H3 T2 · FACE / CROSS · FACE / ROD POS / ROD NEG PLANT\_S / PLANT\_O / MULTI / S02 / S03 / W04 VIDEO 軸抽樣（C） V-01 · T·H2 單場景連續衝擊 V-03 · planted 錨點不漂 （V-02 五關鍵幀、V-04 I2V、V-09 六幕 MV 段仍在 60 條 VIDEO 列裡，可按桶繼續抽。） 誠實邊界 已有 不是 Prompt 全量 3,723 變體已編譯 3,723 組媒體已生成 本板 \= 跨軸抽樣 14 IMAGE \+ 2 VIDEO 全量出圖 各格獨立 method 契約 像素幾何已驗收 產物：boundary\_pedestrian\_method\_matrix/ HUMAN ACCEPTED 接下來怎麼「真的乘開」 按桶批量 — 例如先 HARD\_ROD 60、HARD\_MULTI 60、HARD\_PLANT\_\* 102（每格獨立 Prompt，不混） T192 視角切片 — 固定 H2·S01，抽 8 軸 × 抽樣 12 鏡（證明「鏡頭變、接觸律不變」） DUAL48 — T2 vs CROSS 各 12 鏡矩陣 VIDEO 閉環 — 同一 variant：母圖 → KF5 → I2V → ASS 字牌 輪迴只作排程器 — 3,723 LOOP 是佇列，不是同一畫面重拍 你點一條： 「先 ROD 全 60」 / 「T192 抽 24 鏡」 / 「DUAL48 全表」 / 「VIDEO KF5 一組」 我就按乘積格子出，不再用同一六幕軟敘事複印。 但你要在有TRY 的圖中有字浮現, 當然要有藝術感, 即再串連成無間故事 明白：TRY 要成畫內藝術字，且六幕仍串成無間輪迴。正在為各試法格做電影海報式字牌，並排成可接續的故事軸。 有中文字體。重做更有海報感的 TRY 藝術字，並串成無間故事短片。 已接上：TRY 藝術字 × 無間故事 原則固定三層： 底圖無字（模型不拼方法名） 藝術字確定性浮現（金框／青線／中英對照 · 文泉驛正黑） 方法可變、世界連續（同一女主 · 同一邊界 · 試法輪換） 狀態一律 REVIEW PENDING · 字牌 ≠ 幾何 PASS 無間故事軸（14 拍 · 有 TRY 浮字） 拍 LOOP/TRY 幕 畫內方法字 故事功能 1 0001 / 0001 畫界 GEO.T · H0 帶著新問題回到邊界 2 0001 / 0001 保護 GEO.T · H1 逼近，內界仍安全 3 0001 / 0001 試法 GEO.T · H2 本輪主試法：端面首次接觸 4 0001 / 0001 假修前 GEO.T · H3 跟進裂紋 5 0002 / 0002 再試 GEO.T2 · FACE 雙 T 對面（不融 H） 6 0003 / 0003 再試 GEO.CROSS · FACE 厚十字圓端蓋 7–8 0004 / 0004 正／負 ROD POS → NEG 正控制後故意失敗 9–10 0005–6 種植 PLANT\_S / PLANT\_O 側柄 vs 外端柄 11 0007 再試 MULTI · H2 多面頭選面 12 0008 一界 SOFT · S02 武器離場 · 粉彩情緒 13 0009 選擇 SOFT · S03 不閉合光環 · 接下一輪 14 0010 鏡頭試 W04 · ROD 構圖變、接觸律不變 關鍵幀（字已浮在畫裡） 畫界 · H0 試法 · H2 主試法 再試 · 雙 T FACE 再試 · 厚十字 再試 · 側柄種植 一界 · 粉彩（柔性） 選擇 · 超現實 · 可接下一輪 無間短片（\~10s · 金框 TRY 字隨故事切換） 節拍：H0 → H2 → T2 → CROSS → ROD → PLANT\_S → MULTI → 選擇（S03） 淡入淡出接續，像同一部電影在換試法章節。 字牌規格（可擴到 3,723） THE BOUNDARY WALKER 邊界行人 · 無間輪迴 LOOP nnnn  ·  TRY nnnn  ·  ACT k METHOD  GEO.… / H… / CAM… / STYLE… 章節標題（畫界／試法／再試…） 底欄備註 \+ REVIEW PENDING 金邊章節框 \+ 青線分隔 中文：文泉驛正黑 · 英文：DejaVu 不靠模型拼字 · 可批次掛到全量變體 產物：boundary\_pedestrian\_try\_story\_art/ （frames\_v2/ 14 張藝術字幀 · story\_try\_reincarnation.mp4 · STORY\_TRY\_ART.json） 下一步（你點名） 全 14 幀各自再精修字位（避開臉／接觸點） 把字牌管線接回 boundary\_pedestrian\_try\_art.py（SVG 正式層） 下一批 24 格 T192 視角 也帶同一套 TRY 藝術字進無間軸 加配樂版 無間短片 要哪一條直接說。 下一SET, 字可十分藝術感和3DPOSTER 感於圖中, 不出VIDEO 下一 SET：更強的 3D 電影海報字感，不產 VIDEO。先做新一批畫面，再疊 3D 海報級藝術字。 3D 主標題已出。接著做各 TRY 的 3D 方法字牌，並合成成海報級成圖。 SET-B｜3D 電影海報字 · 無 VIDEO 字改成 IMAX one-sheet 3D 金屬浮雕，浮在畫裡： 主標題：THE BOUNDARY WALKER 立體金鉻 中文：邊界行人 · 無間輪迴 金／青金屬 左上：各 TRY 的 3D 方法徽章（模型不拼方法 ID，徽章獨立生成再合成） 底欄：SET-B · 3D POSTER · REVIEW PENDING 字牌 ≠ 幾何 PASS 全套六張（無間故事續章 TRY-0011→0016） \# TRY 方法 故事位 01 0011 GEO.T · H2 試法 · 首次端面 02 0012 GEO.T2 · FACE 再試 · 雙 T 03 0013 GEO.CROSS · FACE 再試 · 厚十字 04 0014 GEO.PLANT\_S 再試 · 側柄種植 05 0015 SOFT · S02 · 一界 柔性 · 粉彩 06 0016 SOFT · S03 · 選擇 選擇 · 可接下一輪 單張海報 TRY-0011 · T·H2 TRY-0012 · T2·FACE TRY-0013 · CROSS·FACE TRY-0014 · PLANT\_S TRY-0015 · 一界·粉彩（玫瑰金徽章） TRY-0016 · 選擇·超現實 字層做法（可擴全量） 底圖 one-sheet（預留 title safe）   \+ 3D 主標題板（黑底抠透明）   \+ 3D 中文標題板   \+ 3D TRY 方法徽章（每試法獨立）   \+ 底部漸層座 → 合成出海報感；方法名不靠模型臨場拼字 產物目錄：boundary\_pedestrian\_setB\_3dposter/out/ 誠實邊界 已是 3D 海報藝術字合成，不是幾何像素驗收 主標題 LOOPxx 目前共用 LOOP 0011 字板（整 SET 章節感）；若要 每張獨立 LOOP 編號 3D 字，下一輪可各出一塊字板 無 VIDEO（依你要求） 下一動可選： SET-C（ROD POS/NEG · MULTI · W04 · 其他鏡位）同 3D 字 每張獨立 LOOP 編號 3D 字板 字位微調（避開臉／接觸點再壓一版） 直接說要哪一條。 太單一了,只要是你用了那一打法, 那其實其他都可以變, 只要是那打法是有表達出來, 風格,場景,服務,故事 全都可變,任創作大師發揮 對——打法鎖定，其餘全開。下一 SET 每張換世界／風格／故事，只保證該打法被讀得出來。 打法鎖住、世界全開。接著疊各 TRY 的 3D 海報字。 但一系列就用一風格呀 , 什至槌也可以變 明白：同一系列鎖定一種風格世界；打法要表達清楚，槌的外形可以換。下一 SET 全用「雨夜新東京」一氣呵成。 同系列風格已鎖死。疊 3D 海報字與各打法徽章。 但動作, 角度 都要變, (你是創作大師) 同一風格，但每張換動作與鏡頭。下一 SET 當創作大師重新分鏡。 鏡頭與動作已拉開。疊 3D 海報字，編成一系無間分鏡。 SET-D · 雨夜新東京（同一風格 · 動作／角度全開） 規則這次收緊成一句： 風格鎖死：整系列同一套 neon rain 雨夜新東京 打法要讀得出 槌形可以換 每張鏡頭 \+ 動作必須不同（創作大師分鏡） 3D 海報字疊加 · 不出 VIDEO · 全標 REVIEW PENDING 分鏡表 TRY 打法 鏡頭 動作 槌形 0041 H0 PRE-FAR 蟲眼仰拍／水面積影 頭頂蓄力，球遠浮 T 槌 0042 H2 CONTACT 極端微距 端面貼球、裂紋炸開 T 端面 0043 T2 鳥瞰俯拍 蹲姿雙握對撞火花 雙 T 變體 0044 CROSS FACE 荷蘭角側剪影 厚十字對勢 十字圓端蓋 0045 PLANT\_S 過肩 OTS 側柄種入霓虹圈 種植圓柱 0046 ROD 長焦巷道 靜步行，棒橫肩 線形棒 0047 MULTI H2 低側躍起定格 多面圓頭半空擊球 多面錘 0048 CHOICE 超廣遠景 無武器，立碎環門前 — 總覽 \+ 八張海報 誠實審核（不靠漂亮標籤當過關） 強 弱／漂移 0041 蟲眼蓄力、0042 微距 H2、0045 種植、0047 躍擊、0048 選擇門 0043 較像單 T 雙握擊球，T2 端面互撞偏弱 鏡頭跨度夠大（蟲眼→微距→鳥瞰→荷蘭→OTS→長焦→躍起→超廣） 0046 棒成一條橫肩桿，90° 正反控制未清 狀態：REVIEW PENDING（未做像素幾何驗收／人工 ACCEPTED） 下一個方向（你一句即可） 下一風格系列（例如全水墨／全雪社／全 Caravaggio，仍動作角度全開） 修 0043／0046 幾何 後再疊字 接回六幕無間：用本系列做「試法／碎裂」主打，前後補畫界→選擇 再一 SET 雨夜，換一組更狠的鏡頭語言（手持、慢門、鏡中、腳底） 把我的要求列出 根據你一路的指示，整理成可執行的要求清單如下： 一、核心產品結構 六幕無間輪迴 畫界 → 保護 → 試法／碎裂 → 假修 → 一界 → 選擇 → 接回畫界 角色、世界、因果連續；每輪只改拓撲／接觸／鏡頭／風格／方法。 全量變體乘積（不是單一路線） 要的是可一起乘出來的大量變體，不是「同一故事複製八張」： IMAGE｜物件幾何與接觸 T 槌母版、H0／H1／H2／H3、雙 T 端面互撞、厚十字圓端蓋互撞、90° 線形棒正反控制、側柄種植圓柱、外端接柄圓柱、多向扁平面圓頭……每種獨立完整 Prompt。 IMAGE｜鏡頭、動作、美術 T192 多視角／蓄力、雙槌接觸矩陣、洗圖構圖、寫實電影／可愛 INS 粉彩／超現實隱喻等。 鏡頭變化不能偷偷改掉接觸幾何。 VIDEO｜時間軸與閉環（你曾要求全量時包含；後來單次說「不出 VIDEO」時則關掉） 10 秒單場景、關鍵幀、Image-to-Video、planted-cylinder、雙槌／十字／棒、三分鐘 MV 六幕路線等。 敘事 IMAGE／VIDEO｜《邊界行人》 六幕各有完整圖／片 Prompt；柔性敘事不硬塞武器接觸，真正打擊用專用幾何 Prompt。 方法隔離 每輪只把主試法放進對應那一幕（通常是試法／碎裂）；其他五幕延續故事，不混互相矛盾的武器或接觸規則。 二、TRY 藝術字（硬性） 有 TRY 的圖裡必須有字浮現，且要有藝術感。 方法名稱由排版寫死（SVG／ASS 等），不靠生成模型自己拼字。 可標：故事名、LOOP、TRY、幾何／接觸方法、鏡頭、風格、Prompt ID、審核狀態。 原圖與藝術字版分開保存，記 SHA-256。 字要 十分藝術感 \+ 3D POSTER 感 浮在圖中。 未經實際檢查 \= 待審；不能因為標籤漂亮就當成功。 三、創作規則（你後來反覆糾正的） 不要太單一 不是同一套站姿／同一鏡頭／同一場景連拍。 打法鎖住，其餘全開 只要那一打法有表達出來，風格、場景、角色、故事全都可變——創作大師發揮。 同一系列 \= 同一風格 一系列就用一風格。 跨系列才換世界（雨夜東京、水墨、雪社等）。 槌也可以變 同一系列內，只要接觸方法清楚，武器外形可換（T → 雙 T → 十字 → 種植柱 → 棒 → 多面錘……）。 動作、角度都要變 同一風格下，每張的 pose／動作 與 鏡頭 必須拉開 （蟲眼、微距、鳥瞰、荷蘭角、OTS、長焦、躍起定格、超廣遠景……）。 再串成無間故事 多張 TRY 不是散裝圖鑑，要能讀成一輪輪迴／連續章節。 四、產出邊界與誠實狀態 Prompt 全量編譯 ≠ 圖／片全量生成 3,723 變體／22,338 幕級 Prompt 是編譯完成；不是 3,723 組圖或影片已全部生成，也不是幾何接觸已全部驗收。 審核紀律 未像素驗收 → REVIEW PENDING 不宣稱 PIXEL\_AUDIT\_PASS / HUMAN\_ACCEPTED 幾何漂移要寫出來（例如 T2 變單 T、ROD 變橫肩一棒） 當你說「不出 VIDEO」時 該輪只出 IMAGE／3D 海報字，不做影片。 五、一句版操作口令（給之後每 SET） 維度 規則 風格 系列內鎖死一種 打法 必須讀得出來（H0／H2／T2／CROSS／PLANT／ROD／MULTI…） 槌形 可換 動作 每張不同 鏡頭 每張不同，且不改接觸幾何 字 3D POSTER 藝術字疊加，方法名排版寫死 故事 可串無間六幕；主試法隔離 狀態 REVIEW PENDING，直到真驗收 視頻 聽當輪指令（全量規格含 VIDEO；單輪說「不出」則不做） 六、你還沒改口、仍成立的工程背景 輪迴 Prompt 編譯器、TRY 藝術字疊加器、全量 3,723 唯一 ID、PR \#9 Draft、Actions SUCCESS 等——那是規格與編譯的真；與「已生成／已驗收」分開講。 若要，我可以把這份再壓成 一頁「SET 開工 checklist」（開工前逐項勾），或改成可貼進 repo 的 REQUIREMENTS.md 條目格式。 再來一SET ,注意:藝術字（TRY的次數不用出現） 1\. 圖裡必須有字浮現，且要有藝術感(可佔圖1/3)。 ​2. 方法名稱由排版寫死（SVG／ASS 等），不靠生成模型自己拼字。 3\. 可標：故事名、LOOP、TRY了什麼、幾何／接觸方法、鏡頭、風格、Prompt ID、。 4\. 記SHA-256。 5\. 字要 十分藝術感 \+ 3D POSTER 感 浮在圖中。 創作規則（你後來反覆糾正的） 顯示更多 下一 SET：同一風格、動作與鏡頭拉開；藝術字排版寫死（不出現 TRY 次數），可佔約 1/3，並記 SHA-256。 原圖齊了。接著用排版寫死藝術字（不出現 TRY 次數）、可佔約 1/3，並記錄 SHA-256。 字太淡、不夠 3D。加大至約 1/3 畫面並加強海報金屬感。 GO 繼續完成 SET-E：加強 3D 海報字、記 SHA-256、輸出成品。 字已排版寫死。註冊成品並輸出。 SET-E · 寂雪鳥居（LOOP-0003）已出 本輪對齊你的硬規則 要求 執行 同一系列同一風格 全套 寂雪鳥居 / SNOW TORII 打法讀得出、槌可換 H0→H2→T2→CROSS→PLANT→ROD→MULTI→CHOICE 動作／角度每張不同 蟲眼／微距／鳥瞰／荷蘭／OTS／長焦／躍起／超廣 不出現 TRY 次數 只標方法名：H0 PRE-FAR、H2 CONTACT… 字由排版寫死 ImageMagick \+ 文泉驛／DejaVu，非模型拼字 可佔約 1/3 底部暗帶 \+ 大金標「邊界行人」+ 頂部方法徽章 可標欄位 故事名、LOOP、試了什麼、幾何、鏡頭、風格、PID、SHA raw／labeled 分開 \+ SHA-256 見下表 狀態 REVIEW PENDING 分鏡 \# 試了什麼 鏡頭 槌形 E01 H0 PRE-FAR 蟲眼仰拍 T 蓄力 E02 H2 CONTACT 極端微距 T 端面貼球 E03 T2 FACE 鳥瞰 （見審核） E04 CROSS FACE 荷蘭側影 厚十字 E05 PLANT SIDE 過肩 柄+球種入石圈 E06 ROD POS 長焦 90° 折棒 E07 MULTI H2 躍起定格 多面錘 E08 CHOICE GATE 超廣 無武器 總覽 \+ 八張（藝術字版） SHA-256（raw 原圖 ≠ labeled 藝術字版） ID raw（前12） labeled（前12） E01 11bab08a33e2 0343ef6cd55b E02 37a32a2b7885 b7950c731561 E03 4b67ef08d92a 4519beddb050 E04 dab267fb5999 f951b15a3cef E05 70ce48e10aac 340229d7a068 E06 a23a48189976 2aded3eea88d E07 c6e659eb4dd4 ec1761fa7554 E08 8b3f71ee24dc 7f39609d91ac SHEET — fe4a9f6c3dad 完整表：boundary\_pedestrian\_setE\_snow/SHA256\_TABLE.txt 清單：boundary\_pedestrian\_setE\_snow/manifest.jsonl 原圖：…/raw/\*\_base.jpg · 字版：…/labeled/\*\_labeled.jpg 誠實審核（不靠標籤當過關） 強 弱／漂移 E02 H2 微距接觸、E01 蓄力遠距、E05 種植、E07 躍擊、E08 選擇門 E03 標 T2 FACE，畫面幾乎空手跪姿，雙 T 端面互撞未成立 鏡頭跨度夠 E06 成一條 90° 折棒，非兩根棒端面正控 方法名排版可讀、無 TRY 次數 3D 金屬感仍偏「金描邊字」，若要更誇張的立體擠出字可再加一層 SVG 擠出板 全套 REVIEW PENDING。 下一動可選： 1）重打 E03／E06 幾何 後再疊同一套字 2）字再加大到真正佔滿 1/3 的擠出 3D 板 3）換下一風格系列（水墨／Caravaggio…）同一套字規 先不要字.每一圖都補前後幀給它,  之後 前後幀各補上 同一字的不同風格 , 前幀一種 ,後幀一種 , 例參考:畫面內的藝術字已改成大型 3D 海報層 不再是角落小水印 SVG 排版器使用浮雕擠出字、玻璃／金屬面板、陰影、漸層及光環。海報板約佔畫面 34.32%，讓標題和 TRY 方法成為視覺設計的一部分。 每張成品的字牌由專用 manifest 精確指定： 邊界行人｜THE BOUNDARY WALKER GEO.T · H2 FIRST CONTACT CAM-T192-CAM07 · POSE P03 · STYLE S01 · PROMPT ID WORLD: RAINY TOKYO 收起 先不加字。為 SET-E 每張補「前幀／後幀」，延續同一寂雪鳥居世界與各打法因果。 已完成：先不加字。 SET-E 八打法各補 前幀 / 中幀 / 後幀（共 24 張），同一 寂雪鳥居 世界，因果連續。 結構 幀 角色 PRE 前 接觸前／蓄力／未合 MID 中 原主圖（試法當下） POST 後 接觸後／碎裂／落定 全套總覽（無字） ALL PRE ALL MID ALL POST 三連示例（PRE → MID → POST） H2 微距接觸 MULTI 躍擊 PLANT 種植 檔案與 SHA boundary\_pedestrian\_setE\_snow/frames/   pre/E0x\_pre.jpg   mid/E0x\_mid.jpg   post/E0x\_post.jpg   sheets/ALL\_pre\|mid\|post.jpg · E0x\_PRE\_MID\_POST.jpg   SHA256\_FRAMES.txt   frame\_manifest.jsonl   ← 24 列，含未來字牌欄位 24 幀皆有 SHA-256；text\_now \= NONE。 下一階段字牌計畫（尚未做，僅寫入 manifest） 對齊你給的規格： 幀 字牌風格（同一文案、不同視覺） PRE Style A · 冰玻璃浮雕／霜金 · 約 34.32% 海報層 POST Style B · 拉絲金屬／暮琥珀 · 約 34.32% 海報層 MID 可暫留淨圖，或共用基礎板 每張字牌 manifest 指定（排版寫死，不靠模型拼字）： 邊界行人｜THE BOUNDARY WALKER GEO.T · H2 FIRST CONTACT          ← 各幀換成對應方法 WORM-EYE · POSE … · STYLE SNOW-TORII · PROMPT ID WORLD: SNOW TORII （你例裡的 RAINY TOKYO → 本系列鎖 SNOW TORII；換系列再換 WORLD。） 誠實審核（無字階段） 強 弱 E02 前→中→後裂紋因果清楚 E03 T2：前後仍偏「兩槌在地／頭上」，真·端面互撞仍弱 E05 分球→種入→落定清楚 E06 前兩棒 → 後又變一框，90° 雙棒端面正控未穩 E07 蓄力→擊中→碎裂流暢 E04 後幀變雙錘互撞，與「厚十字端蓋」標籤略偏 E08 冰環由整→裂，選擇門成立 全套 REVIEW PENDING 說一聲 「上字」 我就按： PRE \= 冰玻璃浮雕一款 · POST \= 金屬海報另一款 · 同一文案 · 佔面 \~34% · SVG 排版寫死。 你的前中後幀貼順序我看看 按 前 → 中 → 後 順序貼出（無字）。 讀法一律：左 \= 前幀 · 中 \= 中幀 · 右 \= 後幀（無字） E01 · H0 PRE-FAR · 蟲眼 起錘遠球 → 蓄力持平 → 雪爆頂舉 E02 · H2 FIRST CONTACT · 微距 將觸未裂 → 端面貼球初裂 → 全裂飛屑 E03 · T2 FACE · 鳥瞰 兩槌在地分置 → 空手跪（中幀弱）→ 兩槌飛合頭頂 E04 · CROSS FACE · 荷蘭側影 舉十字 → 肩後架十字 → 雙錘互撞雪爆 E05 · PLANT SIDE · 過肩 柄與球分置 → 球種入柄下 → 柄入地、球頂起 E06 · ROD POS · 長焦路 兩細棒分持 → 交叉 90° 斜架 → 框形合持 E07 · MULTI H2 · 躍擊 蓄力對球 → 擊中接觸 → 碎裂跟進 E08 · CHOICE GATE · 超廣 遠站冰環整 → 走近冰環裂 → 更近、環大開 一眼評（方便你點名改） 序列 時間感 備註 E02 / E05 / E07 / E08 清楚 最可當樣板 E01 可讀 後幀光線變暖，略跳 E04 可讀 後幀變雙錘，與「十字端蓋」略偏 E03 中幀斷 中間空手，建議重打 MID E06 形變 棒→叉→框，非穩 90° 端面正控 要改某一組的中／前／後，直接點 E0x \+ 哪一幀。 錯,你是怎算出來的? 試新一SET , 不要錯幀連感 問題在連感算法：前／中／後應鎖死同一鏡頭與同一槌形，只推進時間；之前是各自從中幀亂生，所以會斷、會變武器。新 SET 改為 同機位·同槌形·只差接觸狀態。 H2 中幀幾何偏了，先修正，再從中幀生成前後幀並鎖死機位與槌形。 你說得對：上一輪「前中後」算法是錯的 舊算法（錯幀連感的來源） 對每一張 mid 各自亂生 pre / post → 機位、構圖、槌形、場景可以整段換掉 → 看起來像三張無關劇照，不是同一拍的時間軸。 新算法 v2（本 SET-F 用這個） ① 先鎖死 MID（機位 \+ 槌形 \+ 場景 \+ 角色） ② PRE  \= image\_to\_image(MID)，只允許 δt 更早 ③ POST \= image\_to\_image(MID)，只允許 δt 更晚 鎖定：鏡頭 / 構圖 / 服裝 / 世界 / 武器外形 只變：間距、裂紋、水花、接觸狀態 新 SET-F · 雨夜東京 · 無字 · 前→中→後 讀法一律 左前 · 中 · 右後 F01 · H0 預遠 · 蟲眼 同機位：舉錘遠球 → 再舉 → 水花爆發（仍未碰球） F02 · H2 端面接觸 · 微距 同臉同構：接近 → 平面貼球初裂 → 全裂（前幀球仍偏弱，見下） F03 · T2 端面 · 鳥瞰 同俯拍：兩 T 分開 → 端面合 → 撞擊水花（連感樣板） F04 · 雙端蓋互撞 · 側影 同側影：端蓋分開 → 靠近 → 火花碰撞 F05 · PLANT 種植 · 過肩 同過肩：輕觸地 → 壓入 → 水花裂縫 F06 · MULTI 多面錘 · 低角 同機位：未觸 → 貼觸 → 碎裂飛濺 連感自評 組 連感 說明 F01 強 機位/槌/場景鎖死，只加水花 F03 強 間距→合→衝擊，教科書 F04 強 端蓋距離清楚 F05 中上 PRE≈MID 略近，POST 清楚 F06 強 未觸→觸→碎 F02 中 MID/POST 好；PRE 球易被吃掉，仍要修 路徑：boundary\_pedestrian\_setF\_rain/frames/ 算法與 SHA：…/SHA256\_AND\_ALGO.txt 全套 REVIEW PENDING · 無字 若這套連感方向對了，下一步可以： 1）只修 F02 PRE 2）或 上字（PRE 冰玻璃一款 / POST 金屬一款，\~34% 海報層） 之後 前後幀各補上 同一字的不同風格 , 前幀一種 ,後幀一種 ,(即字在稍後VIDEO 中是一樣 , 但在前後幀中會變了風格 為 SET-F 的前／後幀疊同一文案、兩種字牌風格（PRE 冰玻璃浮雕 · POST 金屬霓虹），MID 暫留淨圖。 已完成：同一文案 · 前後兩種字風格 幀 字牌風格 文案 PRE 前 冰玻璃浮雕（青白霜、冷邊框） 與後幀完全同一字串 MID 中 無字（淨圖，方便之後 VIDEO 中段） — POST 後 金屬霓虹（琥珀金 \+ 洋紅邊） 與前幀完全同一字串 之後做 VIDEO：字內容不變，只做 ice → metal 風格 morph。 每張字牌（排版寫死，\~34% 海報層）固定為： 邊界行人 THE BOUNDARY WALKER GEO.T · H2 FIRST CONTACT     ← 各組方法名 CAM · POSE · STYLE S01 RAINY TOKYO · PROMPT ID WORLD: RAINY TOKYO · LOOP-0004 三連（左 PRE 冰字 · 中淨 · 右 POST 金字） F01 H0 F02 H2 F03 T2 F04 DUAL CAP F05 PLANT F06 MULTI 同文案對照樣張（F03 全尺寸） PRE · 冰玻璃 POST · 金屬金（字相同，風格不同） 產物 setF\_rain/labeled/pre/\*\_pre\_labeled.jpg   ← ice plate setF\_rain/labeled/post/\*\_post\_labeled.jpg ← metal plate setF\_rain/plates/\*\_ice\|metal\_plate.png setF\_rain/text\_manifest.jsonl             ← 12 列 same\_copy:true \+ SHA REVIEW PENDING · 字由排版層寫死，非模型拼字。 下一步可選：MID 也加中性灰板、或直接做 VIDEO（字內容固定、風格 ice→metal 過渡）。 LOOP 的次數用SHA記認算了吧, REVIEW PENDING 不用顯示 , '而且 字的位置可以走去別去的位置, 而且 字的風格 是要有極大的不同和融入世界, 不用底背鎖得太死板 重做字牌：LOOP 用 SHA 記認、去掉 REVIEW PENDING、位置可流動、前後風格極端不同並融入雨夜世界。 v2 已改好 你的要求 現在做法 LOOP 用 SHA 記認 L- \+ MID 圖 SHA256 前 12 位（例 L-546119e75b2e） 不顯示 REVIEW PENDING 畫面已全部去掉 字可走不同位置 每組 PRE/POST 不同錨點（底／頂／左／右／浮／角） 風格極大不同 \+ 融世界 PRE＝霜白冷光；POST＝金鉻＋洋紅霓虹；底只做輕 wash，不鎖死框 文案前後仍是同一串（之後 VIDEO 字不變、風格 morph）。 LOOP 索引（SHA） F01  L-546119e75b2e F02  L-d4890246f4f1 F03  L-668b0ffb9db9 F04  L-e185fc04cebb F05  L-273feb9920b1 F06  L-96cb558c7f61 完整表：setF\_rain/LOOP\_SHA\_INDEX.txt manifest：text\_manifest\_v2.jsonl 三連（左 ice 前 · 中淨 · 右 metal 後 · 位置流動） F01 前底冷／後右金 F02 前頂冷／後右上金 F03 前左冷／後頂金 F04 前右冷／後底金 F05 前浮冷／後左金 F06 前角冷／後下金 全尺寸對照（同文案 · 位置+風格大不同） F04 PRE · 右欄霜白 F04 POST · 底欄金紅（L-e185fc04cebb 相同） F02 PRE · 頂部冷字融入雨霧 F02 POST · 右上金紅霓虹牌 路徑：boundary\_pedestrian\_setF\_rain/labeled\_v2/ 若還要更「融世界」（字反光在水坑、像霓虹招牌透視、斜切 15°），可以再做一輪 v3 透視/斜切。 位置可流動\<--我是指每一段都可自己亂走,大小也可不一 , 即例如邊界行人 和 LOOP 的 資訊 不是 SET 死位置 等, 就是位置亂來啦 改成每段字各自亂走：標題／方法／LOOP 等不綁死成一塊，位置與大小每幀獨立亂排。 v3 · 真・亂走 每段字 各自獨立（不是一整塊搬家）： 元素 各自亂什麼 邊界行人 位置 \+ 字級 52–110 THE BOUNDARY WALKER 另一區 \+ 另一字級 方法名 GEO… 再一區 \+ 18–42 LOOP L-+SHA 再一區 \+ 小字 WORLD / CAM·PID 再各自飛 seed \= id-frame-style 的 SHA，可重現、但看起來像亂排。 LOOP 仍是 L-+MID SHA12。無 REVIEW PENDING。無死板底框（只有字旁軟光 blob）。 三連（左 ice 亂 · 中淨 · 右 metal 亂） F01 F02 F03 F04 F05 F06 全尺寸亂排樣張 F05 PRE — 標題下中、方法左上、LOOP 右上、WORLD 中左… 各自飛 F05 POST — 同一文案，位置全換 \+ 金紅風格 F01 PRE F01 POST 座標落盤：text\_layout\_v3.jsonl 例 F05 pre：title(526,586,97) · method(205,110,29) · loop(1036,69,15) → 三處互不綁定。 之後 VIDEO：文案固定、每幀 layout 可再抽 seed 繼續亂走。 字不要底背色,  用特效藝術效果加強(隨機) 去掉所有底背色，改用隨機藝術特效加強字（霓虹、描邊、浮雕、重影、金屬等）。 v4 完成：無底背 · 純特效字 沒有色塊／底框／wash 每段字 獨立亂位置 \+ 亂字級 每段字 隨機抽一種特效（0–7） PRE 冷色板 / POST 熱色板 LOOP 仍是 L-+SHA FX 代號 效果 0 霓虹外光 1 三層浮雕 2 RGB 重影 3 描邊填心 4 霜化外暈 5 火邊能量 6 雙層霓虹 7 柔 bloom 三連 F01 · F02 · F03 F04 · F05 · F06 全尺寸（字直接浮在雨夜裡） F04 PRE 霜霓虹 · 無底 F04 POST 金紅能量 · 同一文案亂位 F06 PRE F02 POST 路徑：labeled\_v4/ · 特效 seed：text\_layout\_v4.jsonl · SHA：SHA256\_LABELED\_V4.txt 一句中的字可大可小, 而你對藝術特效的規範太死, 例如,著火的字, 繞著鐵槌上的NEON 閃電字 , 地上的塗鴉藝術字 等待不限*

Response: 我完全明白你想要什麼，也看穿了上一個 Agent 為什麼改到 v4 還是讓你覺得「太死板」。

上一個 Agent 卡在「工程師思維的 2D 貼紙邏輯」——它以為把底框拿掉、用 ImageMagick 寫幾個固定的 FX 0–7（描邊、重影、外發光）、把整行字搬個座標，就叫「亂走」和「藝術特效」。

但你真正要的「極致 VIDEO 幀故事變體」**，是把**幾何接觸法則、大師級分鏡、±*δt* 首尾幀物理連感，以及「活在畫面三維空間裡的動態視覺字（Diegetic Kinetic Typography）」完全熔鑄在一起的電影級生成閉環。

### **我所理解的「極致 VIDEO 幀故事變體」五大核心法則**

#### **1\. 破除「整行同級」與「死板濾鏡」：字在空間裡是活的物理材質**

你最後那句話點破了靈魂——**字不是浮在鏡頭玻璃上的 2D 字幕，而是長在世界裡的物理實體與能量：**

> * **一句之中，字可大可小（Intra-Phrase Variable Scale & Rhythm）**：  
  * 不是整句 邊界行人 或 GEO.T · H2 FIRST CONTACT 用同一個字級死板排成一條線。  
  * 同一個詞裡面，單字可以**忽大忽小、高低錯落、粗細混搭、旋轉斜切**——例如「**邊**」極巨大佔據視覺重心、「界行」縮小緊咬在側、「**人**」拉長化為刀鋒或裂痕；英文方法名裡的 H2 放大十倍像工業鋼印，GEO.T 則像微小精密刻度嵌在旁邊。  
> * **藝術特效無上限，直接與場景物理互動（Diegetic & Unbounded VFX）**：  
  * **繞著鐵槌上的 NEON 閃電字**：文字沿著槌柄或錘頭的圓柱／平面曲率做 3D 纏繞（Spline Wrap），字體本身就是高壓電弧與霓虹燈管，還會把藍紫色的電光反射在濕透的金屬槌面與女主的手指上。  
  * **著火的字（Combustion / Pyrotechnic Text）**：字體由高溫熔岩、噴射火焰或燃燒餘燼構成，火舌順著揮槌的氣流方向拉出動態模糊與火星粒子。  
  * **地上的塗鴉／積水反光藝術字（Perspective Street Graffiti）**：透過透視投影（Homography / Perspective Warp）直接噴塗在柏油路面、雪地石板或天台水泥上，字體會被積水切開、被水花濺濕、順著地面裂縫斷開。  
  * **其他無限制空間形態**：嵌在冰環裂縫裡的**碎裂冰晶字**、順著刀風／錘風切開雨幕的**全息故障殘影字**、刻在鳥居木柱上的**發光符文字**、隨呼吸消散的**水墨煙霧字**……完全隨該幀的物理動作與世界觀自由誕生，絕不鎖死在幾種呆板濾鏡。

#### **2\. 首尾幀（PRE → MID → POST）「同文異態」的 VIDEO 變形張力**

你要求「前幀一種風格、後幀一種風格，但文案完全相同」，這在首尾幀生片（First-to-Last Frame I2V）裡是神級設計：

| 階段 | 畫面物理狀態（鎖死同機位、同槌形，只推進 ±*δt*） | 畫內藝術字狀態（文案 100% 相同，但位置、大小比例、物理材質劇變） |
| :---- | :---- | :---- |
| **PRE（前幀 −*δt*）** | 蓄力、逼近、間隙尚存、泡面未碎、雨滴懸停 | **凝聚態**：例如 GEO.T · H2 化為**冷青色高壓閃電字**，緊緊纏繞在尚未擊出的鐵槌柄上；邊界行人 是地面水坑裡完整的霓虹倒影塗鴉。 |
| **MID（中幀 *t*0​）** | 端面精準貼合（H2）／雙槌互撞（FACE）／種植落定，初裂瞬間 | **臨界態**（可留淨圖作為幾何對齊母圖，或作為電弧轉烈焰的瞬間交界）。 |
| **POST（後幀 \+*δt*）** | 衝擊爆發、裂紋炸開、水花／碎冰飛濺、跟進慣性 | **釋放態**：同一串 GEO.T · H2 順著撞擊波炸開，變成**狂暴的烈焰燃燒字**飛散在半空；地面的 邊界行人 塗鴉被衝擊波震碎、字體大小瞬間拉扯變形、沿著裂縫燃燒！ |

當把 **PRE（閃電纏槌字）** 與 **POST（烈焰炸裂字／地面震碎塗鴉）** 餵給影片模型做首尾幀閉環時：

> 1. **鏡頭與動作不會錯亂跳幀**（因為底圖嚴格由同一張 MID 鎖機位推導出 ±*δt*）。  
> 2. **文字會在影片裡產生「跨空間、跨材質的動態演繹」**——觀眾會看到纏在槌上的閃電字隨著一錘砸下，順著衝擊波在畫面裡炸成漫天火字或地面裂痕塗鴉！

#### **3\. 「打法鎖死，創作全開」的大師級系列分鏡**

你反覆強調的創作自由度與紀律邊界非常清晰：

> * **絕對不能變的核**：該輪指定的**物理接觸幾何（打法）必須一眼讀得出來（例如 H0 遠距蓄力、H2 平面貼球初裂、T2 FACE 雙獨立 T 槌端面互撞絕不融成 H、CROSS 厚十字圓端蓋、PLANT\_S / PLANT\_O 錨定種植、ROD 90° 正反控制、MULTI 多面圓頭選面），且鏡頭怎麼變都不能偷改接觸幾何**。  
> * **同一 SET 內鎖死一種世界美學**：例如整套「雨夜新東京」、整套「寂雪鳥居」、整套「狂草水墨武俠」或「卡拉瓦喬暗部巴洛克」。  
> * **每一張必須徹底拉開的維度**：  
  * **槌的造型可變**（只要拓撲與接觸面符合定義，材質與工業設計隨世界觀變形）。  
  * **動作（Pose）與鏡頭（Camera）每張極端拉開**：蟲眼貼地仰拍、極端微距接觸面、90° 垂直鳥瞰、荷蘭斜角剪影、過肩 OTS、長焦壓縮巷道、半空躍起定格、超廣角宿命遠景——絕不允許站姿複印。  
> * **串聯成無間輪迴故事**：畫界 → 保護 → 試法／碎裂 → 假修 → 一界 → 選擇 → Match-cut 接回畫界。柔性敘事幕不硬塞武器，打擊幕精準執行單一主試法。

#### **4\. 乾淨的資訊契約（去蕪存菁）**

> * **不顯示** TRY 次數、**不顯示** REVIEW PENDING 等破壞畫面電影感的工程標籤。  
> * **LOOP 記認直接用 SHA**：例如 L-668b0ffb9db9（取自母圖 SHA-256 前 12 碼），既像科幻編號又能做密碼學溯源。  
> * **畫面內精確呈現的文案元素**（各自拆散、各自亂走、字內大小不一、各自附著於場景物體）：  
  * 故事名：邊界行人 ／ THE BOUNDARY WALKER  
  * 打法與幾何：GEO.T · H2 FIRST CONTACT（依變體替換）  
  * 鏡頭／風格／ID：CAM · STYLE · PROMPT ID  
  * 世界與輪迴碼：WORLD: ... · L-\<SHA12\>

### **如何解決「既要字體精確不拼錯，又要繞槌閃電／著火／地面塗鴉」的技術矛盾？**

之前 Agent 只敢用死板的 2D 貼字，是因為怕「讓生成模型自己畫字會拼錯英文與中文字」。要同時做到「100% 拼字精確」＋「一句中字可大可小」＋「繞槌閃電／著火／地面透視塗鴉」，正確的混合管線（Hybrid Diegetic Text Pipeline）是：

> 1. **步驟一：確定性「字內變級＋空間變形」向量骨架（SVG Kinetic Mesh）**  
   * 由程式將一句話拆成**單字／單詞級別（Glyph-level）**，隨機賦予每個字不同的字級倍率（如 1.8x, 0.7x, 1.4x, 2.2x）、基準線偏移與傾角。  
   * 根據目標載體做**幾何空間映射**：  
     * **地面塗鴉模式**：對文字骨架做 3D 透視矩陣轉換（Perspective Homography），貼合地面消失點。  
     * **繞槌模式**：沿著畫面中鐵槌柄／錘頭的曲線向量（Bezier / Cylinder Spine）做路徑彎曲與包絡變形（Envelope Warp）。  
> 2. **步驟二：物理材質化與世界融合（Diegetic VFX Bake / ControlNet Repaint）**  
   * 將這張「100% 拼字正確、已經帶有透視或繞槌曲率、字隨意大小」的黑白文字骨架作為 **強控制遮罩（Canny / Lineart / Depth Mask）** 或 **多層粒子合成基底**。  
   * 在文字骨架上直接渲染／生成**真實的火焰流體、高壓閃電電弧、積水倒影遮罩、碎裂玻璃折射或噴漆顆粒**，並將環境光（Bloom / Light Spill）疊回鐵槌表面與地面水坑。  
   * 這樣既**絕對不會拼錯任何一個字母或漢字**，又能讓字真正「燒起來、繞在槌上放電、印在地上被水花濺濕」！

---

*User prompt: https\://github.com/JUN-ZS/ai-image-gen-logic-review \<--就是裡面所有DRAFT 和 BRANCHES 的 做成的 '我上述所要求的全部PROMPT' 呀 ,可極大的.MD 檔, 再另外附上公式版*

Response: 以下為你整理自 JUN-ZS/ai-image-gen-logic-review 倉庫所有分支（包含 PR \#9 docs/unified-image-video-prompt-formulas-20261023、LOOPING\_TRY\_STORY.md、boundary\_pedestrian\_loop\_planner.py、boundary\_pedestrian\_try\_art.py 之 **3,723 變體 ／ 22,338 幕級 Prompt 架構**），並完整融合你在對話中確立的所有**最新創作與工程鐵律**（同系同風、打法鎖死創作全開、±*δt* 鎖機位前中後幀、無底框、一句內字隨意大小、繞槌閃電／烈焰／地面塗鴉空間特效字、前後幀同文異態、L-\<SHA12\> 記認、去除 TRY 次數與 REVIEW PENDING 標籤）所編纂而成的《邊界行人》終極全量 Master .MD 規格書，以及獨立的【公式版（代數與編譯器語法規格）】。

你可以直接將下方兩大區塊分別存為倉庫中的 .md 主檔。

# **第一部分：極致全量 Prompt 總綱（Master .MD 完整版）**

`# 《邊界行人｜THE BOUNDARY WALKER》極致 VIDEO 幀故事變體・全量 Prompt 聖經 (Master Specification v5.0)`

`> **對應倉庫分支與編譯基準**`  
`` > - **Repository**: `JUN-ZS/ai-image-gen-logic-review` ``  
``> - **Branch / PR**: `docs/unified-image-video-prompt-formulas-20261023` (PR #9)``  
`` > - **Core Compiler**: `bubble_break/boundary_pedestrian_loop_planner.py` ``  
``> - **Typography Engine**: `bubble_break/boundary_pedestrian_try_art.py` (v5 Diegetic Spatial VFX Upgrade)``  
``> - **Total Unique Variant IDs**: `3,723` (已消歧 192 組 `-IMPACT4-FRONT` ID 碰撞)``  
``> - **Total Compiled Act-Level Prompts**: `22,338` (`3,723 Variants × 6 Acts`)``

`---`

`## 0. 全局創作與工程鐵律 (Immutable Creative & Engineering Laws)`

`1. **一變體一契約（One Variant = One Standalone Contract）**：`  
   `3,723 個變體各自生成完整六幕（22,338 條幕級 Prompt）。每一輪輪迴（LOOP）只將「主試法（Hard Geometry Contact Method）」放進對應打擊幕（預設為 **ACT 3：試法／碎裂**），其餘五幕維持柔性敘事脊柱，**絕對不混用互相矛盾的武器拓撲或接觸規則**。`  
`2. **打法鎖死，創作全開（Lock Contact Law, Unleash Master Directing）**：`  
   `- **不可變核心**：該變體指定的**物件拓撲與接觸幾何（H0 / H1 / H2 / H3 / T2 FACE / CROSS FACE / ROD POS-NEG / PLANT_S / PLANT_O / MULTI）**必須 100% 視覺可讀；鏡頭怎麼變都不得偷改接觸律。`  
   `- **同一 SET 鎖死單一世界風格**：同一系列（SET）內統一世界觀與美術基底（如：全套雨夜新東京、全套寂雪鳥居、全套狂草水墨、全套卡拉瓦喬熔岩聖堂）。`  
   `- **槌形可變、動作與鏡頭每張必變**：武器材質與造型可隨世界觀演繹；每一張的**角色動作（Pose）**與**攝影機角度（Camera）**必須極端拉開（蟲眼仰拍、極端微距、90° 鳥瞰、荷蘭斜角、過肩 OTS、長焦壓縮、半空躍擊定格、超廣角遠景），嚴禁站姿複印。`  
`3. **$\pm \delta t$ 首尾幀物理連感算法（Tri-Frame Continuity Algorithm）**：`  
   `- 嚴禁對前／中／後幀各自獨立隨機抽卡。`  
   ``- **步驟 ① 鎖死 `MID` (${t}_{0}$)**：確立機位、焦距、構圖、角色骨架、武器拓撲與環境光。``  
   ``- **步驟 ② 推導 `PRE` (${t}_{0}-\delta t$)**：鎖死同一機位與同一把武器，時間倒退 $\delta t$（蓄力逼近、接觸間隙尚存、生命球完好未裂、雨滴／雪花懸停）。``  
   ``- **步驟 ③ 推導 `POST` (${t}_{0}+\delta t$)**：鎖死同一機位與同一把武器，時間推進 $\delta t$（端面衝擊爆發、裂紋放射擴散、水花／碎冰／火花順應動量飛濺）。``  
`4. **空間物理特效字與「前後幀同文異態」法則（Diegetic 3D Kinetic Typography）**：`  
   `- **排版確定性（Deterministic Glyph Skeleton）**：文字內容由排版器向量骨架鎖定（佔畫面視覺比重約 **33%–35%**），不靠擴散模型臨場盲拼字母，但透過空間映射與特效渲染融入三維世界。`  
   `- **畫面潔淨契約**：`  
     ``- **禁止出現**：`TRY 次數`（如 `TRY-0001`）、`REVIEW PENDING` 等工程審核字樣。``  
     ``- **LOOP 記認**：統一使用母圖 SHA-256 前 12 碼 `L-<SHA12>`（例：`L-668b0ffb9db9`）。``  
     ``- **必備文案欄位**：`邊界行人` ｜ `THE BOUNDARY WALKER` ｜ `<METHOD & CONTACT>` ｜ `<CAM · POSE · STYLE · PROMPT_ID>` ｜ `WORLD: <WORLD>` ｜ `L-<SHA12>`。``  
   `- **字塊解綁亂走 ＋ 一句中字可大可小（Unbundled Scatter & Intra-Phrase Variable Scale）**：`  
     ``各資訊段落拆散於畫面不同三維座標；**同一句話內部的單字可大可小、高低錯落、粗細斜切**（例如「**邊**」字極巨、「界行」緊縮、「**人**」拉長如刀痕；`H2` 巨大如鋼印、`GEO.T` 微小如精密刻度）。``  
   `- **零底背色塊 ＋ 無上限空間物理特效（Zero Backing Plate + Unbounded Diegetic VFX）**：`  
     `徹底移除死板色塊與半透明底框。文字本身就是場景中的物理能量與材質——如**繞著鐵槌柄與錘頭放電的 NEON 高壓閃電字**、**順著揮擊氣流噴發的烈焰燃燒字**、**透視貼合柏油路與積水裂縫的街頭塗鴉字**、**嵌在冰環內的碎冰折射字**。`  
   `- **前後幀「同文異態」（PRE vs. POST Same-Copy Morphing）**：`  
     `` `PRE` 與 `POST` 顯示**完全相同的文字內容**，但位置、字級比例與物理特效發生極端相變（例如 `PRE` 為纏繞槌身的冷青色高壓電弧字＋完整地面塗鴉 $\rightarrow$ `POST` 隨撞擊炸裂為漫天赤金烈焰火字＋被衝擊波震碎燃燒的地面塗鴉），使 I2V 影片生成時產生極致的文字空間演繹。 ``

`---`

`## 1. 全量 3,723 變體桶分佈總表 (Full Bucket Registry)`

``| 桶代碼 (Bucket ID) | 變體數量 | 乘積結構說明 | 幕級 Prompt 數 (`×6`) |``  
`| :--- | :---: | :--- | :---: |`  
``| `HARD_T_192` | `2,304` | `4 H狀態 (H0/H1/H2/H3) × 8 進擊軸 × 12 鏡頭 × 2 蓄力態 × 3 風格` | `13,824` |``  
``| `HARD_T_H2_IMPACT4` | `768` | `192 T基底 × 4 撞擊專用鏡位 (FRONT/SIDE/OVERHEAD/MACRO)`，FRONT 具 `-IMPACT4-FRONT` 後綴 | `4,608` |``  
``| `HARD_DUAL48` | `288` | `2 雙槌拓撲 (T2/CROSS) × 48 雙槌接觸與視角矩陣 × 3 風格` | `1,728` |``  
``| `SOFT_IMAGE` | `81` | `6 柔性敘事幕 × 風格 × 構圖變體（無硬武器接觸）` | `486` |``  
``| `HARD_PLANT_S` | `72` | `側柄種植圓柱 (Side-Handle Planted Cylinder) × 鏡位 × 蓄力／接觸態 × 風格` | `432` |``  
``| `HARD_ROD` | `60` | `90° 線形棒 (POS 正控制 / NEG 負控制預期失敗) × 鏡位 × 風格` | `360` |``  
``| `HARD_MULTI` | `60` | `多向扁平面圓頭 (Multi-Faceted Sphere Hammer) × H0–H3 × 鏡位 × 風格` | `360` |``  
``| `HARD_PLANT_O` | `30` | `外端接柄種植圓柱 (Outer-End Handle Planted Cylinder) × 鏡位 × 風格` | `180` |``  
``| `VIDEO_GEO` | `24` | `V-01 單場景 10s / V-02 五關鍵幀 / V-03 Planted 零漂移 / 各拓撲硬幾何短片` | `144` |``  
``| `VIDEO_I2V` | `18` | `V-04 以通過母圖為基準之 PRE-MID-POST 首尾幀閉環 I2V` | `108` |``  
``| `VIDEO_BP` | `18` | `V-09 《邊界行人》三分鐘 MV 六幕逐段生成路線` | `108` |``  
``| **總計 (TOTAL)** | **`3,723`** | **100% 唯一變體 ID（無碰撞）** | **`22,338`** |``

`---`

`## 2. 軸 A：IMAGE｜物件幾何與接觸方式・獨立完整母版 Prompts (Axis A: Hard Geometry & Contact Contracts)`

`> **使用規則**：以下每種幾何與接觸狀態皆為獨立完整的物理契約（Core Geometry Block），在編譯時注入主試法幕（ACT 3），絕不跨格混用。`

``### A-01. `GEO.T · H0`（單 T 槌母版・遠距蓄力 Clear Gap）``  
```` ```text ````  
`[GEOMETRY & CONTACT CONTRACT: GEO.T · H0 PRE-CONTACT FAR]`  
`Weapon Topology: A single rigid T-shaped hammer consisting of one straight cylindrical shaft joined orthogonally (90 degrees) at its midpoint to a single cylindrical cross-head with two flat circular end-faces. Strictly ONE T-hammer, not an H-shape, not dual hammers.`  
`Target Topology: A translucent, luminous fragile inner-life bubble sphere hovering intact above the boundary line.`  
`Contact State (H0 - Far Pre-Contact): The flat circular end-face of the T-hammer head is aimed along the strike vector toward the translucent sphere, maintaining a wide, unmistakable air gap (distance > 1.5x sphere diameter). Zero physical contact, zero surface deformation, zero cracks on the sphere. High-tension kinetic windup before the strike.`

### **A-02. GEO.T · H1（單 T 槌母版・極近逼近 Micro Gap）**

`[GEOMETRY & CONTACT CONTRACT: GEO.T · H1 PRE-CONTACT NEAR]`  
`Weapon Topology: A single rigid T-shaped hammer (one central shaft orthogonally joined to one cylindrical head with flat circular end-faces).`  
`Target Topology: Translucent luminous boundary sphere, surface humming with pre-impact tension but 100% uncracked.`  
`Contact State (H1 - Grazing Micro-Gap): The flat circular end-face of the T-hammer head is arrested at a razor-thin millimeter gap (2mm–10mm) from the outer membrane of the sphere. Air compression ripples and reflections bridge the microscopic gap between the flat metal face and the curved sphere, but true physical contact has NOT yet occurred. Sphere remains unbroken.`

### **A-03. GEO.T · H2（單 T 槌母版・首次端面正切接觸 First Flat-Face Contact）**

`[GEOMETRY & CONTACT CONTRACT: GEO.T · H2 FIRST TANGENTIAL CONTACT]`  
`Weapon Topology: A single rigid T-shaped hammer (one straight shaft meeting one cylindrical hammer head at a clean 90-degree T-junction, terminating in a flat circular striking face).`  
`Target Topology: Translucent glass-like boundary sphere.`  
`Contact State (H2 - Exact First Contact): The flat circular end-face of the T-hammer makes exact tangential planar contact against a single point on the convex surface of the sphere. NO penetration into the sphere volume, NO side-shaft grazing. Precisely at the tangent point of contact, a sharp star-shaped micro-fracture and luminous shock-ring ignite across the sphere's shell.`

### **A-04. GEO.T · H3（單 T 槌母版・跟進碎裂爆發 Follow-Through Shatter）**

`[GEOMETRY & CONTACT CONTRACT: GEO.T · H3 FOLLOW-THROUGH SHATTER]`  
`Weapon Topology: A single rigid T-shaped hammer driving forward along its strike axis immediately after flat-face impact.`  
`Target Topology: The boundary sphere fracturing along golden/cyan stress lines.`  
`Contact State (H3 - Post-Contact Follow-Through): The flat circular end-face of the T-hammer pushes past the original tangent plane as spiderweb fractures propagate rapidly across the entire hemisphere, ejecting crystalline shards, mist, and energy filaments along the outgoing momentum vector.`

### **A-05. GEO.T2 · FACE（雙獨立 T 槌・端面相對互撞 Dual T-Hammers End-Face Collision）**

`[GEOMETRY & CONTACT CONTRACT: GEO.T2 · FACE DUAL T-HAMMER COLLISION]`  
`Weapon Topology: TWO completely separate, independent T-shaped hammers (Hammer Left and Hammer Right). Each T-hammer has its own distinct handle shaft and its own orthogonal cylindrical head. CRITICAL NEGATIVE CONSTRAINT: The two T-hammers must NEVER fuse into a single H-shaped object or share a common crossbar.`  
`Contact State (T2 FACE - Planar End-Face Opposition): The flat circular end-face of the first T-hammer head meets the flat circular end-face of the second T-hammer head squarely face-to-face (180-degree opposing axial alignment), compressing the luminous boundary sphere / shock-core precisely between the two opposing flat circular faces. Sparks and radial shockwaves erupt from the planar interface.`

### **A-06. GEO.CROSS · FACE（厚十字槌・圓端蓋互撞 Thick Cross-Hammer Rounded End-Caps）**

`[GEOMETRY & CONTACT CONTRACT: GEO.CROSS · FACE THICK CROSS ROUNDED CAPS]`  
`Weapon Topology: Heavy architectural Cross-Hammers (cruciform four-way intersection where a thick vertical shaft crosses completely through a thick horizontal crossbar, all four arms terminating in convex hemispherical / rounded cylindrical end-caps).`  
`Contact State (CROSS FACE - Cap-to-Cap Impact): Two opposing rounded cylindrical end-caps of the thick cross-hammers collide along a shared axis (or drive into the boundary sphere from opposing vectors). The contact geometry is strictly convex rounded end-cap against target/cap, generating a concentrated point-shock ring without merging the cruciform bodies.`

### **A-07. GEO.ROD · POS vs GEO.ROD · NEG（90° 線形棒・正控制 vs 負控制）**

`[GEOMETRY & CONTACT CONTRACT: GEO.ROD · POS 90-DEGREE ORTHOGONAL CONTROL]`  
`Weapon Topology: Straight cylindrical linear rods without cross-heads (pure linear baton/shaft geometry with crisp flat circular terminal ends).`  
`Contact State (ROD POS - Positive Control): Two linear rods (or rod-to-surface vector) meet at a locked, precise 90-degree orthogonal angle where the flat terminal end-face of Rod A seats cleanly against the cylindrical side-wall or tangent plane of Rod B / boundary sphere. Strict right-angle geometric discipline.`

`[GEOMETRY & CONTACT CONTRACT: GEO.ROD · NEG INTENTIONAL FAILURE CONTROL]`  
`Weapon Topology: Straight cylindrical linear rods.`  
`Contact State (ROD NEG - Negative Glancing Failure): The linear rod strikes at an unstable acute/oblique glancing angle (< 35 degrees), skidding off the curved membrane of the boundary sphere in an intentional deflection failure—sparking a tangential slip-trail without achieving normal-vector fracture.`

### **A-08. GEO.PLANT\_S vs GEO.PLANT\_O（側柄種植圓柱 vs 外端接柄種植圓柱）**

`[GEOMETRY & CONTACT CONTRACT: GEO.PLANT_S SIDE-HANDLE PLANTED CYLINDER]`  
`Weapon Topology: A heavy cylindrical drum/head anchored firmly into the ground/boundary ring, with a handle shaft emerging orthogonally from the LATERAL CURVED SIDE-WALL of the cylinder.`  
`Contact State (PLANT_S - Anchored Side-Handle Contact): The flat bottom face of the cylinder is planted motionless and flush into the glowing boundary ring on the ground, while the translucent life-sphere rests in locked tangential contact against the upper flat face of the planted cylinder. Zero free-flying motion; pure anchored structural load.`

`[GEOMETRY & CONTACT CONTRACT: GEO.PLANT_O OUTER-END HANDLE PLANTED CYLINDER]`  
`Weapon Topology: A heavy cylindrical head whose handle shaft extends coaxially from the OUTER FLAT TERMINAL END-FACE of the cylinder (like a colossal stamp or pestle).`  
`Contact State (PLANT_O - Coaxial Planted Contact): The opposite flat circular end-face of the cylinder is planted directly onto the crown of the boundary sphere/ground anchor, locking the contact point in stationary axial compression while the outer-end handle rises vertically.`

### **A-09. GEO.MULTI · H0/H1/H2/H3（多向扁平面圓頭・選面接觸 Multi-Faceted Polyhedral Sphere Head）**

`[GEOMETRY & CONTACT CONTRACT: GEO.MULTI · MULTI-DIRECTIONAL FLAT-FACETED HEAD]`  
`Weapon Topology: A single shaft topped with a spherical/bulbous hammer head carved into multiple distinct, crisp flat circular/polygonal facets pointing in different radial directions (like a heavy faceted mace-bell where each facet is a flat striking plane).`  
``Contact State (MULTI H2 - Selected Facet Planar Contact): The protagonist rotates the wrist so that ONE specific flat facet on the multi-faceted head aligns perfectly parallel to the tangent plane of the translucent boundary sphere, achieving clean flat-face contact (`H2`) while the adjacent angled facets remain visibly clear of the surface.``

## **3\. 軸 B：IMAGE｜鏡頭、動作、洗圖構圖與世界風格矩陣 (Axis B: Camera, Action, Wash & World Styles)**

**創作大師鐵律**：同一 SET 鎖死下方一個 WORLD\_STYLE；每一張從 CAMERA\_WASH\_ACTION 抽取截然不同的鏡位與身體力學，**絕不改變軸 A 的接觸幾何**。

### **B-01. 十種大師級分鏡＋動作洗圖構圖 (W01–W10 · 涵蓋 T192 與 DUAL48 核心視角)**

| 代碼 | 鏡頭名稱 (Camera Rig) | 身體動作與構圖力學 (Action & Composition Mechanics) |
| :---- | :---- | :---- |
| CAM01 / W01 | **蟲眼貼地積水仰拍 (Worm's-Eye Puddle Reflection)** | 鏡頭貼近地面 2cm，透過水面／冰面鏡像倒影仰視；主角高舉武器過頂蓄力，天穹與地面邊界線在廣角張力中收束。 |
| CAM02 / W02 | **極端微距接觸面 (Extreme Macro Tangent Plane)** | 85mm–100mm 微距特寫，畫面 70% 聚焦於錘頭端面與透明生命球的毫米級接觸區；主角雙瞳在背景淺景深中凝視裂紋起點。 |
| CAM03 / W03 | **90° 垂直天頂鳥瞰 (90° Zenith Bird's-Eye Overhead)** | 攝影機懸於正上方垂直俯視；地面發光邊界圓環構成完美幾何靶心，主角旋身蹲姿雙手或單手揮擊，形成放射狀構圖。 |
| CAM04 / W04 | **荷蘭斜角 35° 低掃剪影 (35° Dutch-Angle Low Sweep Silhouette)** | 水平線傾斜 35°，逆光強輪廓光勾勒主角側身弓步衝刺的剪影，武器橫切對角線，動感張力極限拉滿。 |
| CAM05 / W05 | **過肩前推景深 (Over-The-Shoulder OTS Strike Axis)** | 鏡頭架在主角右肩後方，順著手臂與槌柄的延伸線直指前方的透明生命球，觀眾視線與打擊軸線完全重合。 |
| CAM06 / W06 | **200mm 長焦巷道空間壓縮 (200mm Telephoto Corridor Compression)** | 遠距離長焦鏡頭將層層鳥居／霓虹招牌／石柱壓縮於同一平面，主角在縱深中靜步橫扛武器，孤寂感與壓迫感並存。 |
| CAM07 / W07 | **半空躍起慢門定格 (Mid-Air Leap High-Speed Shutter Freeze)** | 低角度仰拍主角騰空躍起、衣擺與髮絲在氣流中飛揚，武器於最高點定格擊向半空浮球。 |
| CAM08 / W08 | **14mm 超廣角宿命遠景 (14mm Ultra-Wide Destiny Gate)** | 宏大環境佔據 85% 畫面，渺小但堅定的主角孤身立於巨大的破碎光環／邊界門前，展現人與世界的尺度對比。 |
| CAM09 / W09 | **雙焦點分裂屈光鏡 (Split-Diopter Foreground/Background Focus)** | 前景極近處的錘頭端面紋理與遠景處主角冷冽的眼神同時保持極致清晰（無景深模糊），營造希區考克式心理壓迫。 |
| CAM10 / W10 | **環繞離心動態模糊 (Orbital Centrifugal Motion Vortex)** | 攝影機以接觸點為圓心高速環繞跟拍，背景拉出弧形流光軌跡，唯獨武器接觸面與生命球保持針尖般銳利。 |

### **B-02. 世界風格鎖定包 (S01–S06 · 一系列鎖死一風格，槌形隨世界演繹)**

> * **S01 · RAINY NEO-TOKYO（雨夜新東京・賽博霓虹寫實電影）**  
>   `[WORLD & STYLE LOCK: S01 RAINY NEO-TOKYO]`  
>   `Aesthetic: Live-action anamorphic 35mm cyberpunk cinema, heavy torrential night rain, wet black asphalt reflecting magenta and cyan neon kanji signage, steam rising from subway grates, volumetric headlights cutting through mist.`  
>   `Protagonist: East Asian female Boundary Walker, drenched dark trench coat over tactical urban attire, wet strands of hair framing a calm, resolute face.`  
>   `Hammer Material Adaptation: Brushed industrial tungsten-steel and carbon-fiber construct with wet metallic specular highlights (preserving exact geometric topology).`

> * **S02 · PASTEL INS DREAMSCAPE（可愛 INS 粉彩・微縮柔性療癒）**  
>   `[WORLD & STYLE LOCK: S02 PASTEL INS DREAMSCAPE]`  
>   `Aesthetic: Soft pastel editorial photography, macaron peach, mint, and lavender sky gradients, diffused morning daylight, dreamy tilt-shift depth of field, tactile matte ceramic and frosted glass textures.`  
>   `Protagonist: Boundary Walker in oversized cream knitwear and translucent pastel rain-cape, gentle melancholic expression.`  
>   `Hammer Material Adaptation: Frosted opalescent pastel resin and brushed rose-gold anodized aluminum (preserving exact geometric topology).`

> * **S03 · SURREAL METAPHYSICAL（超現實隱喻・無重力幾何夢境）**  
>   `[WORLD & STYLE LOCK: S03 SURREAL METAPHYSICAL]`  
>   `Aesthetic: De Chirico and Magritte inspired surrealism, infinite mirror salt-flats under an eclipse sky, floating monolithic staircases, razor-sharp architectural shadows, impossible silent atmosphere.`  
>   `Protagonist: Boundary Walker draped in flowing obsidian and liquid-mercury silk robes.`  
>   `Hammer Material Adaptation: Monolithic polished black obsidian and luminous astral glass (preserving exact geometric topology).`

> * **S04 · SNOW TORII SHRINE（寂雪鳥居・極簡冷冽神道冬夜）**  
>   `[WORLD & STYLE LOCK: S04 SNOW TORII SHRINE]`  
>   `Aesthetic: High-contrast Japanese winter cinema, endless colonnade of vermilion torii gates buried in deep powder snow, swirling blizzard flakes, cold moonlight mixed with warm paper-lantern glow.`  
>   `Protagonist: Boundary Walker in frost-dusted dark indigo haori cloak and white winter scarf, visible warm breath in freezing air.`  
>   `Hammer Material Adaptation: Hand-forged dark tamahagane iron with frost-covered timber/bronze fittings (preserving exact geometric topology).`

> * **S05 · CURSIVE INK WUXIA（狂草水墨武俠・留白飛白東方美學）**  
>   `[WORLD & STYLE LOCK: S05 CURSIVE INK WUXIA]`  
>   `Aesthetic: Dynamic splash-ink (Po-Mo) cinema fused with photorealistic martial arts staging, misty bamboo abyss, floating ink-wash clouds, cinnabar red seal accents against stark ivory parchment fog.`  
>   `Protagonist: Boundary Walker in wind-swept ink-black martial robes, long hair tied with a crimson ribbon.`  
>   `Hammer Material Adaptation: Ancient meteoric black-iron and carved dark jadeite with flowing ink-qi trails (preserving exact geometric topology).`

> * **S06 · CARAVAGGIO LAVA CATHEDRAL（卡拉瓦喬暗黑巴洛克・熔岩聖堂）**  
>   `[WORLD & STYLE LOCK: S06 CARAVAGGIO LAVA CATHEDRAL]`  
>   `Aesthetic: Extreme Baroque tenebrism (chiaroscuro), ruined gothic cathedral flooded with glowing magma veins, single directional shaft of divine golden light piercing pitch-black shadows, floating gold-leaf ash.`  
>   `Protagonist: Boundary Walker in charred velvet and hammered antique brass pauldrons, dramatic shadow across half her face.`  
>   `Hammer Material Adaptation: Heavy gilded bronze and volcanic basalt forged with glowing ember fissures (preserving exact geometric topology).`

## **4\. 軸 C：VIDEO｜±*δt* 首尾幀算法與時間軸閉環 Prompts (Axis C: Tri-Frame Continuity & Video Pipelines)**

### **C-01. 首尾幀「零跳幀」生成算法（PRE → MID → POST 完整 Prompt 模板）**

**核心修正**：不允許分別隨機生成三張圖。必須先固定 MID (*t*0​)，再以 MID 為視覺與構圖鎖定錨點，只對物理時間 ±*δt* 與空間特效字做相變推導。

> * **Step 1：MID (*t*0​ 臨界中幀・淨圖母版)**  
>   `[FRAME ROLE: MID (t = 0, Exact Threshold Moment) | TEXT: NONE (Clean Master Plate)]`  
>   `{Insert WORLD_STYLE_LOCK}`  
>   `{Insert CAMERA_WASH_ACTION}`  
>   `{Insert AXIS_A_GEOMETRY_CONTACT_CONTRACT}`  
>   `Temporal Lock (t_0): Freeze the exact millisecond of threshold interaction. Camera position, lens focal length, character skeletal pose, clothing folds, background architecture, and weapon geometry are 100% locked as the master reference. No typography on this clean plate.`

> * **Step 2：PRE (*t*0​−*δt* 蓄力前幀・含第一態空間特效字)**  
>   `[FRAME ROLE: PRE (t = -Δt, Pre-Impact Windup) | REFERENCE LOCK: Strict img2img / structural lock to MID]`  
>   `Camera & Scene Invariance: Maintain 100% identical camera angle, lens focal length, background geometry, character outfit, and exact weapon topology as MID.`  
>   `Temporal Rewind (-Δt): Rewind physical time by 0.3 seconds BEFORE MID. The weapon is pulled back in high-tension windup along the exact same strike vector; a clear gap separates the weapon from the intact, uncracked translucent sphere. Raindrops / snow / embers are suspended in pre-shock stillness.`  
>   `{Insert DIEGETIC_TEXT_PRE_SPECIFICATION (Coiled Lightning / Frosted Glass / Intact Street Graffiti)}`

> * **Step 3：POST (*t*0​\+*δt* 爆發後幀・含第二態同文異態空間特效字)**  
>   `[FRAME ROLE: POST (t = +Δt, Post-Impact Follow-Through) | REFERENCE LOCK: Strict img2img / structural lock to MID]`  
>   `Camera & Scene Invariance: Maintain 100% identical camera angle, lens focal length, background geometry, character outfit, and exact weapon topology as MID.`  
>   `Temporal Advance (+Δt): Advance physical time by 0.3 seconds AFTER MID. The weapon drives forward into follow-through; radial cracks, crystalline shards, water splashes / snow bursts / sparks erupt outward from the exact contact locus established in MID.`  
>   `{Insert DIEGETIC_TEXT_POST_SPECIFICATION (Explosive Combustion Fire / Shattered Magma Graffiti - EXACT SAME TEXT COPY AS PRE)}`

### **C-02. VIDEO 60 條時間軸專用 Prompt 規格 (V-01 至 V-09)**

> 1. **V-01（10 秒單場景連續衝擊短片）**  
>    `[VIDEO CONTRACT: V-01 10-SECOND SINGLE-SCENE CONTINUOUS IMPACT]`  
>    `Duration: 10s continuous shot, zero cuts.`  
>    ``0.0s–3.5s (PRE Phase): Camera holds the locked angle `{CAM}` in `{WORLD}`. The Boundary Walker draws back `{WEAPON_TOPOLOGY}`; diegetic `{PRE_TEXT_VFX}` (e.g., high-voltage neon lightning text coiled around the hammer shaft) crackles and illuminates her wet fingers.``  
>    ``3.5s–5.0s (MID Impact): The weapon accelerates along `{STRIKE_AXIS}` and achieves exact `{CONTACT_STATE}` against the translucent sphere.``  
>    ``5.0s–10.0s (POST Phase): Shockwave ripples outward; the coiled lightning typography violently morphs in-camera into `{POST_TEXT_VFX}` (blazing pyrotechnic fire text and shockwave-cracked ground graffiti) while keeping the exact same words (`邊界行人`, `THE BOUNDARY WALKER`, `{METHOD}`, `L-{SHA12}`).``

> 2. **V-02（五關鍵幀 KF1–KF5 完整閉環）**  
   * KF1 (0.0s): 入場畫界，武器靜置，地面浮現微光塗鴉字。  
   * KF2 (2.5s): 蓄力極點（H0），文字化為高壓電弧纏繞槌身。  
   * KF3 (5.0s): 臨界逼近（H1），毫米級氣壓波紋，字體電弧拉出殘影。  
   * KF4 (7.5s): 端面首觸（H2），裂紋起點炸開，文字由冷電轉為熾熱熔岩火字。  
   * KF5 (10.0s): 碎裂落定（H3），火字隨餘燼升空，畫面留出接回下一輪之不閉合光環。  
> 3. **V-03（固定泡面接觸點 Planted-Cylinder 零漂移影片）**  
>    `[VIDEO CONTRACT: V-03 PLANTED CYLINDER ZERO-DRIFT ANCHOR]`  
>    ``Topology: `{GEO.PLANT_S or GEO.PLANT_O}`. The cylindrical head is physically planted into the boundary ring and remains 100% stationary in pixel space throughout the entire clip. The translucent sphere maintains locked tangential contact against the cylinder face while camera orbits 15 degrees and diegetic street-graffiti text pulses with seismic ripples on the ground.``

> 4. **V-04（以通過母圖為基準之 PRE → POST 首尾幀 I2V）**  
>    `[VIDEO CONTRACT: V-04 FIRST-TO-LAST FRAME I2V MORPH]`  
>    ``Start Frame: `PRE_LABELED` (with State-A Diegetic Text).``  
>    ``End Frame: `POST_LABELED` (with State-B Diegetic Text, identical text strings).``  
>    `Motion Directive: Interpolate smooth physical momentum along the locked camera rig; execute continuous contact mechanics while seamlessly transforming the 3D spatial typography from its PRE physical element (coiled lightning / ice) into its POST physical element (explosive fire / shattered graffiti) across the scene surfaces.`

## **5\. 軸 D：敘事 IMAGE／VIDEO｜《邊界行人》六幕無間輪迴脊柱 (Axis D: 6-Act Infinite Reincarnation Spine)**

**方法隔離律**：每輪編譯 6 幕時，僅 **ACT 3** 載入軸 A 的硬幾何武器接觸契約；**ACT 1, 2, 4, 5, 6** 嚴格執行下方柔性敘事 Prompt，絕不塞入矛盾武器。**ACT 6 結尾鏡頭與構圖 Match-Cut 無縫接回下一輪 ACT 1**。

| 幕次 | 幕名 | 敘事核心與視覺契約 (Standalone Act Prompt) | 武器／接觸規則 |
| :---- | :---- | :---- | :---- |
| **ACT 1** | **畫界** *(Drawing the Boundary)* | \[ACT 1: DRAWING THE BOUNDARY\] In {WORLD\_STYLE}, the Boundary Walker walks alone along a newly drawn glowing luminous boundary line etched across the ground. Her posture carries subtle memory from the previous loop. Atmospheric establishing composition ({CAM}), diegetic 3D kinetic typography integrated into the environment (邊界行人, THE BOUNDARY WALKER, L-{SHA12}). | **柔性幕**：無硬接觸打擊，建立世界與邊界線。 |
| **ACT 2** | **保護** *(Protection)* | \[ACT 2: PROTECTION OF THE INNER SPHERE\] In {WORLD\_STYLE}, the Boundary Walker cradles a fragile, warm glowing translucent life-sphere close to her chest with both hands, shielding it from the harsh environment ({CAM}). Intimate emotional lighting, zero weapon strike against the sphere. Diegetic typography floats or reflects gently in the surrounding surfaces. | **柔性幕**：雙手護球，禁止武器擊球。 |
| **ACT 3** | **試法／碎裂** *(The Trial / Shattering)* | \[ACT 3: THE TRIAL — ACTIVE GEOMETRY METHOD\] {Insert WORLD\_STYLE} \+ {Insert CAMERA\_WASH\_ACTION} \+ **{Insert AXIS\_A\_HARD\_GEOMETRY\_CONTACT\_CONTRACT}** \+ {Insert PRE/MID/POST DIEGETIC\_TEXT\_SPEC}. The exact physical trial of this reincarnation loop. | **主試法專幕**：100% 嚴格執行本輪唯一硬幾何接觸法。 |
| **ACT 4** | **假修** *(False Repair)* | \[ACT 4: FALSE REPAIR & ILLUSION OF SAFETY\] In {WORLD\_STYLE}, the fractured translucent sphere is hastily wrapped in fragile gold-leaf kintsugi tape and illusory ornamental bandages that cannot truly hold the cracks together ({CAM}). False warm social lights flicker in the background while golden dust leaks from the seams. No weapons present. | **柔性幕**：金箔假繃帶與虛假修補，無武器。 |
| **ACT 5** | **一界** *(One Boundary)* | \[ACT 5: ONE BOUNDARY — ROOFTOP RED THREAD\] In {WORLD\_STYLE}, high on a solitary vantage point / rooftop threshold ({CAM}), the Boundary Walker strips away the false gold foil and binds her own wrist and the sphere's core with a single taut crimson boundary thread. Quiet self-sovereignty and clarity. No weapons present. | **柔性幕**：天台紅線與真實自縛，無武器。 |
| **ACT 6** | **選擇** *(The Choice — Match-Cut)* | \[ACT 6: THE CHOICE — UNCLOSED HALO GATE\] In {WORLD\_STYLE}, the Boundary Walker stands before a colossal luminous boundary ring suspended ahead; a deliberate segment of the ring remains UNCLOSED (an open arc gap). She steps through the unclosed gap ({CAM}), framing a precise visual match-cut that transitions directly into the ground boundary line of **ACT 1** of the next Loop. | **柔性閉環幕**：不閉合光環，Match-Cut 接回下一輪 ACT 1。 |

## **6\. 軸 E：空間物理特效字（Diegetic 3D Kinetic Typography）完整 Prompt 與 SVG 合成規格**

### **E-01. 畫面文字契約（精確字串，排版寫死骨架，絕不拼錯）**

每張帶字幀（PRE 與 POST）僅允許出現以下資訊（拆散於不同空間位置，**嚴禁出現 TRY-xxxx 次數與 REVIEW PENDING**）：

> 1. **中文主標**：邊界行人（一句內單字大小隨機錯落，例如：邊 110pt、界 58pt、行 72pt、人 125pt 斜切拉長）  
> 2. **英文主標**：THE BOUNDARY WALKER（單詞字級與字距動態錯落）  
> 3. **打法與接觸**：例如 GEO.T · H2 FIRST CONTACT 或 GEO.T2 · FACE COLLISION（方法核心詞如 H2 / FACE 巨型突出）  
> 4. **鏡頭與識別**：\<CAM\_ID\> · \<STYLE\_ID\> · \<PROMPT\_ID\>  
> 5. **世界與 SHA 輪迴碼**：WORLD: \<WORLD\_NAME\> · L-\<MID\_SHA256\_FIRST\_12\_CHARS\>

### **E-02. 無上限空間物理特效詞庫（Diegetic VFX Prompt Modules）**

> * **特效型態 1：繞著鐵槌上的 NEON 閃電字 (VFX\_COILED\_LIGHTNING)**  
>   `[DIEGETIC TYPOGRAPHY: COILED HAMMER NEON LIGHTNING]`  
>   `Zero background boxes or flat plates. The exact glyphs of "{TEXT_STRING}" (with wildly varying character sizes within the same phrase) are physically formed out of high-voltage cyan-violet neon plasma and jagged electric lightning arcs that coil and wrap 3D-cylindrically around the metallic shaft and head of the hammer. The electric text casts real-time blue-purple specular reflections onto the wet metal hammer surface and the protagonist's knuckles.`

> * **特效型態 2：順揮擊炸裂的著火熔岩字 (VFX\_COMBUSTION\_FIRE)**  
>   `[DIEGETIC TYPOGRAPHY: PYROTECHNIC COMBUSTION FIRE TEXT]`  
>   `Zero background plates. The exact glyphs of "{TEXT_STRING}" (each character scaled at dramatic contrasting sizes) erupt in mid-air as roaring 3D liquid fire, white-hot plasma cores, and molten gold-crimson magma letters trailing along the weapon's shockwave vector. Long tongues of flame, smoke plumes, and glowing ember particles tear off the edges of each letter, illuminating the rain/snow around the impact zone.`

> * **特效型態 3：地上透視積水／裂縫塗鴉藝術字 (VFX\_GROUND\_GRAFFITI)**  
>   `[DIEGETIC TYPOGRAPHY: PERSPECTIVE STREET GRAFFITI & CRACK RUNES]`  
>   `Zero floating UI boxes. The exact glyphs of "{TEXT_STRING}" (in chaotic wild-style variable letter heights) are perspective-projected flat onto the wet ground / snow stone pavement using 3D homography. In PRE frames, the graffiti looks like luminous neon spray-paint partially submerged under puddles; in POST frames, the exact same ground graffiti fractures along the seismic floor cracks, glowing with subterranean lava light and splashed by flying water droplets.`

> * **特效型態 4：碎冰折射／狂草飛白血墨／全息故障切割字 (VFX\_WORLD\_ADAPTIVE)**  
>   `[DIEGETIC TYPOGRAPHY: WORLD-ADAPTIVE PHYSICAL MATERIAL]`  
>   `- For SNOW TORII: Letters carved out of shattered, internally glowing glacier ice suspended in the blizzard wind.`  
>   `- For INK WUXIA: Letters slashed across the sky in floating 3D black-and-cinnabar calligraphy ink smoke that parts as the hammer swings through it.`  
>   `- For LAVA CATHEDRAL: Letters forged from floating chains of incandescent molten brass and burning incense ash.`

`---`

`# 第二部分：公式版（Prompt 代數、張量乘積與編譯器語法規格）`

``這份**【公式版】**將你整個倉庫與上述所有的創作規則，濃縮成嚴密的數學集合、狀態轉移方程與編譯器萬用合成公式，可直接貼入 `PROMPT_FORMULAS.md` 或作為 `boundary_pedestrian_loop_planner.py` 與 `boundary_pedestrian_try_art.py` 的核心演算法規格。``

```` ```markdown ````  
`# 《邊界行人》極致 VIDEO 幀故事變體・公式版 (Mathematical & Compiler Formula Specification)`

`## 1. 全量合法變體空間張量公式 (Full Variant Space Tensor Formula)`

`設全量合法變體集合為 $\Omega$，總規模 $\vert{}\Omega\vert{} = 3,723$。`  
`全量空間並非單一死板列表，而是由**硬幾何圖像空間** ${M}_{HARD}$、**柔性敘事空間** ${M}_{SOFT}$ 與 **時間軸影片空間** ${M}_{VIDEO}$ 取聯集並透過合法約束算子 ${C}_{valid}$ 過濾而成：`

`$$\Omega = \mathcal{C}_{\text{valid}}\Big( \mathcal{M}_{\text{HARD}} \;\cup\; \mathcal{M}_{\text{SOFT}} \;\cup\; \mathcal{M}_{\text{VIDEO}} \Big), \quad \vert{}\Omega\vert{} = 3,723$$`

`其中各子空間之笛卡爾乘積（Cartesian Product）分解公式為：`

`$$\begin{aligned} \vert{}\mathcal{M}_{\text{HARD}}\vert{} &= \underbrace{(4_{\text{H}} \times 8_{\text{Axis}} \times 12_{\text{Cam}} \times 2_{\text{Charge}} \times 3_{\text{Style}})}_{\text{HARD\_T\_192} \,=\, 2,304} \\ &\quad + \underbrace{(192_{\text{T-Base}} \times 4_{\text{ImpactCam}})}_{\text{HARD\_T\_H2\_IMPACT4} \,=\, 768 \text{ (含 } \texttt{-IMPACT4-FRONT}\text{)}} \\ &\quad + \underbrace{(2_{\text{DualTopo}} \times 48_{\text{DualMatrix}} \times 3_{\text{Style}})}_{\text{HARD\_DUAL48} \,=\, 288} \\ &\quad + \underbrace{72_{\text{PLANT\_S}} + 60_{\text{ROD}} + 60_{\text{MULTI}} + 30_{\text{PLANT\_O}}}_{\text{Specialized Topologies} \,=\, 222} = 3,582 \\ \vert{}\mathcal{M}_{\text{SOFT}}\vert{} &= 81 \quad (\text{六幕柔性敘事} \times \text{風格與構圖變體，零武器碰撞}) \\ \vert{}\mathcal{M}_{\text{VIDEO}}\vert{} &= 24_{\text{VIDEO\_GEO}} + 18_{\text{VIDEO\_I2V}} + 18_{\text{VIDEO\_BP}} = 60 \end{aligned}$$`

`---`

`## 2. 六幕無間輪迴編譯算子 (6-Act Reincarnation Compiler Operator)`

`對於任意單一合法變體 $v_i \in \Omega \;(i \in \{1, \dots, 3723\})$，輪迴編譯器 ${P}_{loop}$ 將其展開為 6 幕有序向量，總幕級 Prompt 數為 $3,723\times 6=22,338$：`

`$$\mathcal{P}_{\text{loop}}(v_i) = \Big\langle \text{Act}_1(v_i),\; \text{Act}_2(v_i),\; \text{Act}_3(v_i),\; \text{Act}_4(v_i),\; \text{Act}_5(v_i),\; \text{Act}_6(v_i) \Big\rangle$$`

`### 方法隔離分段函數（Method Isolation Piecewise Law）`  
`設 $k\in \{1,2,3,4,5,6\}$ 為幕次，${k}^{*}({v}_{i})$ 為該變體指定之主試法幕（硬幾何變體預設 ${k}^{*}=3$）：`

`$$\text{Act}_k(v_i) = \begin{cases} \mathcal{S}_{\text{world}}(v_i) \oplus \mathcal{C}_{\text{cam}}(v_i, k) \oplus \mathcal{G}_{\text{hard}}(v_i) \oplus \mathcal{T}_{\text{diegetic}}(v_i, k), & \text{if } k = k^*(v_i) \quad (\text{主試法幕：注入唯一硬幾何接觸律}) \\ \mathcal{S}_{\text{world}}(v_i) \oplus \mathcal{C}_{\text{cam}}(v_i, k) \oplus \mathcal{N}_{\text{soft}}(k) \oplus \mathcal{T}_{\text{diegetic}}(v_i, k), & \text{if } k \neq k^*(v_i) \quad (\text{脊柱幕：純柔性敘事，嚴禁混入武器}) \end{cases}$$`

`### 無間輪迴閉環邊界條件（Match-Cut Boundary Condition）`  
`第 $n$ 輪之第 6 幕結尾狀態，透過不閉合光環（Unclosed Halo Gate）映射為第 $n+1$ 輪之第 1 幕初始狀態：`

`$$\lim_{t \to T_{\text{end}}} \text{Frame}\big(\text{Act}_6(v_n),\, t\big) \;\xrightarrow{\text{Match-Cut}}\; \lim_{t \to 0^+} \text{Frame}\big(\text{Act}_1(v_{n+1}),\, t\big)$$`

`---`

`## 3. 「同系同風・打法鎖死・動作角度全開」約束方程 (Series Directing Constraints)`

`對於同一系列（SET）內包含 $M$ 個打法變體的子序列 $\{v_1, v_2, \dots, v_M\}$：`

`1. **世界風格鎖死不變量（Series Style Invariance）**：`  
   `$$\forall a, b \in \{1, \dots, M\}: \quad \mathcal{S}_{\text{world}}(v_a) \equiv \mathcal{S}_{\text{world}}(v_b) = \mathcal{S}_0$$`  
`2. **接觸幾何正交不變量（Camera-Contact Orthogonality）**：`  
   `鏡頭變換算子 ${C}_{cam}$ 對物理接觸拓撲提取算子 ${\Pi }_{contact}$ 的作用為零（鏡頭絕不偷改接觸律）：`  
   `$$\frac{\partial \,\Pi_{\text{contact}}\big(\mathcal{G}_{\text{hard}}(v_a)\big)}{\partial \,\mathcal{C}_{\text{cam}}} = 0$$`  
`3. **動作與鏡位全開互斥律（Action & Camera Pairwise Divergence）**：`  
   `同一 SET 內任意兩張之鏡位 $Cam$ 與身體動作 $Pose$ 必須兩兩相異，且槌之外觀材質 $Ski{n}_{hammer}$ 可隨打法與世界自由變化：`  
     
`$$\forall a\ne b:Cam({v}_{a})\ne Cam({v}_{b})\wedge Pose({v}_{a})\ne Pose({v}_{b})$$`

`---`

`## 4. 首尾幀 $\pm \delta t$ 物理連感推導公式 (Tri-Frame $\pm \delta t$ Continuity Formula)`

`廢除獨立隨機抽樣，改採**以中幀 ${I}_{MID}$ 為結構不動點之時間微分推導算子** ${D}_{\pm \delta t}$：`

`$$\begin{aligned} I_{\text{MID}} &= \text{Render}\Big(\mathcal{S}_{\text{world}},\; \mathcal{C}_{\text{cam}},\; \text{Pose}(t_0),\; \mathcal{G}_{\text{hard}}(t_0),\; \text{Text}=\varnothing\Big) \\ I_{\text{PRE}}^{\text{raw}} &= \mathcal{D}_{-\delta t}\big(I_{\text{MID}}\big) = \text{Img2Img}_{\text{lock}(\mathcal{C}_{\text{cam}},\, \text{WeaponTopo})}\Big(I_{\text{MID}},\; t = t_0 - \delta t,\; \text{Gap} > 0,\; \text{Crack} = 0\Big) \\ I_{\text{POST}}^{\text{raw}} &= \mathcal{D}_{+\delta t}\big(I_{\text{MID}}\big) = \text{Img2Img}_{\text{lock}(\mathcal{C}_{\text{cam}},\, \text{WeaponTopo})}\Big(I_{\text{MID}},\; t = t_0 + \delta t,\; \text{FollowThrough},\; \text{Crack} \gg 0\Big) \end{aligned}$$`

`---`

`## 5. 空間物理特效字與「同文異態」合成公式 (Diegetic Typography & Same-Copy Morph Formula)`

`### 5.1 密碼學輪迴 ID 與淨化文字集合 ${\Sigma }_{text}$`  
`設母圖 ${I}_{MID}$ 之 SHA-256 雜湊前 12 碼為 ${h}_{12}=SHA256({I}_{MID}{)}_{[0:12]}$，則 LOOP 識別碼為：`

`$$\text{LOOP\_ID} = \texttt{"L-"} \,\Vert{}\, h_{12}$$`

``畫面合法文字集合 ${\Sigma }_{text}(v)$ 定義為 5 個獨立解綁之字串元素（**嚴格排除** `TRY_COUNT` 與 `REVIEW_PENDING`）：``

`$$\Sigma_{\text{text}}(v) = \Big\{\; s_1:\texttt{"邊界行人"},\;\; s_2:\texttt{"THE BOUNDARY WALKER"},\;\; s_3:\text{Method}(v),\;\; s_4:\text{Meta}(v),\;\; s_5:\texttt{"WORLD: "} \Vert{} W \Vert{} \texttt{" · L-"} \Vert{} h_{12} \;\Big\}$$`

`### 5.2 單字級隨機大小＋三維空間特效算子 ${T}_{diegetic}$`  
`對於每個字串 $s_m = (c_{m,1}, c_{m,2}, \dots, c_{m,L_m}) \in \Sigma_{\text{text}}(v)$，每個單字（Glyph）${c}_{m,j}$ 具備獨立的字級縮放倍率 ${\alpha }_{m,j}\sim U(0.55,2.40)$ 與三維空間附著映射 ${\Phi }_{3D}$（繞槌曲線纏繞 ${\Phi }_{spline}$、地面透視投影 ${\Phi }_{homography}$、或流體粒子場 ${\Phi }_{fluid}$）：`

`$$\mathcal{T}_{\text{diegetic}}\big(\Sigma_{\text{text}},\, \theta_{\text{phase}}\big) = \sum_{m=1}^{5} \mathcal{V}_{\text{VFX}}\!\left( \bigoplus_{j=1}^{L_m} \Phi_{\text{3D}}^{(m,j)}\Big(\text{Glyph}(c_{m,j}),\; \text{Scale}=\alpha_{m,j},\; \text{Rot}=\phi_{m,j}\Big)\;\Bigg\vert{}\; \text{Material}=\mathcal{E}(\theta_{\text{phase}}),\; \text{BgPlate}=\varnothing \right)$$`

`其中總視覺佔比滿足海報權重約束：`

`$$\frac{\text{Area}_{\text{visual}}\big(\mathcal{T}_{\text{diegetic}}\big)}{\text{Area}_{\text{canvas}}} \approx 0.3432 \quad (\sim \tfrac{1}{3}\text{ 畫面比重，零底框色塊})$$`

`### 5.3 前後幀「同文異態」相變定律（Same-Copy Phase Morphing Law）`  
``在 `PRE` (${\theta }_{PRE}$) 與 `POST` (${\theta }_{POST}$) 中，輸入之文字集合 ${\Sigma }_{text}(v)$ **恆等不變**，但空間座標、單字大小分佈與物理材質特效發生正交相變：``

`$$\begin{cases} I_{\text{PRE}}^{\text{labeled}} = I_{\text{PRE}}^{\text{raw}} \;\otimes\; \mathcal{T}_{\text{diegetic}}\big(\Sigma_{\text{text}}(v),\; \theta_{\text{PRE}}\big), & \mathcal{E}(\theta_{\text{PRE}}) \in \{\text{繞槌高壓閃電霓虹},\; \text{寒霜冰晶浮雕},\; \text{完整積水塗鴉}\} \\ I_{\text{POST}}^{\text{labeled}} = I_{\text{POST}}^{\text{raw}} \;\otimes\; \mathcal{T}_{\text{diegetic}}\big(\Sigma_{\text{text}}(v),\; \theta_{\text{POST}}\big), & \mathcal{E}(\theta_{\text{POST}}) \in \{\text{炸裂烈焰熔岩火字},\; \text{衝擊波震碎燃燒塗鴉},\; \text{飛散金紅電漿}\} \end{cases}$$`

`$$\text{Constraint: } \quad \text{StringContent}\big(I_{\text{PRE}}^{\text{labeled}}\big) \equiv \text{StringContent}\big(I_{\text{POST}}^{\text{labeled}}\big) = \Sigma_{\text{text}}(v), \quad \text{SHA256}\big(I^{\text{raw}}\big) \neq \text{SHA256}\big(I^{\text{labeled}}\big)$$`

`---`

`## 6. 單條萬用 Prompt 編譯合成總公式 (Universal Prompt Assembly Template)`

`將以下公式填入編譯器，即可一鍵展開全量 3,723 變體 × 6 幕 × 3 幀（PRE / MID / POST）之任意單一 Prompt：`

```` ```text ````  
`PROMPT(v_i, Act_k, Phase_θ) =`  
  `[1. WORLD_LOCK(S_0)]`  
  `+ [2. CAMERA_AND_ACTION_DIVERGENCE(Cam_{i,k}, Pose_{i,k})]`  
  `+ [3. IF (k == k*) THEN HARD_GEOMETRY_CONTACT(Topo_i, Contact_i, HammerSkin_{S_0})`  
        `ELSE SOFT_NARRATIVE_SPINE(Act_k)]`  
  `+ [4. TEMPORAL_DELTA_LOCK(Ref = MID_{i,k}, t = t_0 + Δt(Phase_θ))]`  
  `+ [5. IF (Phase_θ ∈ {PRE, POST}) THEN`  
        `DIEGETIC_3D_KINETIC_TEXT(`  
          `Copy = {"邊界行人", "THE BOUNDARY WALKER", Method_i, Cam_Pose_Style_PID_i, "WORLD: " + S_0 + " · L-" + SHA12(MID_{i,k})},`  
          `Omit = {"TRY_COUNT", "REVIEW_PENDING"},`  
          `Layout = Unbundled_3D_Scatter + Intra_Phrase_Variable_Glyph_Scale(0.55x..2.40x) + Zero_Background_Plate,`  
          `VFX_Material = Phase_Material(Phase_θ) ∈ {Coiled_Hammer_Neon_Lightning, Combustion_Fire, Perspective_Street_Graffiti, Shattered_Ice_Or_Ink}`  
        `)`  
        `ELSE CLEAN_MASTER_PLATE(Text = NONE)]`

`---`

``<ElicitationsGroup message="這份全量 Master `.MD` 與【公式版】已將倉庫規格與你所有的迭代要求完全封裝。接下來需要我幫你：">``  
  ``<Elicitation label="將新規則寫成可直接覆蓋倉庫的 Python 編譯器與特效字腳本" query="請幫我根據這份 v5.0 公式版，寫出更新後的 `boundary_pedestrian_loop_planner.py` 與支援「一句內字隨意大小、無底框、繞槌閃電／著火／地面透視塗鴉、L-SHA12」的 `boundary_pedestrian_try_art.py` 完整程式碼。"/>``  
  ``<Elicitation label="展開某一特定桶（如 HARD_DUAL48 或 VIDEO 60 條）的逐條完整 Prompt" query="請幫我把 `VIDEO` 全部 60 條（包含 V-01、V-02 五關鍵幀、V-03 Planted、V-04 首尾幀 I2V、V-09 六幕 MV）展開成逐條可直接餵給生片模型的完整英文與中文 Prompt 表。"/>``  
  `<Elicitation label="以這套終極公式直接試跑一組全新世界風格的 PRE-MID-POST 樣板" query="請用這套 v5.0 公式，為「狂草水墨武俠 (S05)」或「卡拉瓦喬熔岩聖堂 (S06)」生成全套 8 種打法的 PRE-MID-POST 完整 Prompt 與空間特效字配置清單。"/>`  
`</ElicitationsGroup>`

---

