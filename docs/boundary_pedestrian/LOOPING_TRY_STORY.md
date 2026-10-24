# 《邊界行人》無限輪迴：全部方法進入同一故事

**狀態：故事與出圖規格；不是「已把所有變體全部生成」的宣稱。**  
入口： [IMAGE／VIDEO Prompt 總庫](../IMAGE_VIDEO_PROMPT_CATALOG.md) · [合法變體乘積表](VARIANT_CROSSWALK.md) · [全量 ID 入口](variants/README.md) · [26 鏡分鏡](mv26/README.md)

## 核心概念

《邊界行人》不再只是六張固定分鏡，而是一部**不斷重返同一個邊界、每次採用不同試法的輪迴故事**。

每一輪仍然是同一位女主、同一個世界問題、同一條因果主線；改變的是本輪嘗試的方法：物件拓撲、接觸狀態、相機軸／鏡頭、蓄力方式、構圖洗圖、畫風、單段影片／五關鍵幀／母圖轉影片，以及故事隱喻。方法以每一張圖／每一段影片自己的 TRY 標籤顯示在作品裡。觀眾看見的不只是「她再試一次」，而是「她這次到底用了哪一種方法」。

故事可以無限續寫；方法清單不假稱無限。第一輪按現有合法變體 ID 清單逐一走完，之後才開新輪次，用新 seed／新敘事揭示／尚未測過的合法組合重新編排。每個實際 TRY 都留下可追溯 ID、來源 Prompt、輸出檔與狀態。

## 固定的故事 DNA

- **人物不變：**同一成年東亞女主，以已核准的角色參考圖鎖定身份。臉、長深棕髮、體型和服裝不因 TRY ID 改變。
- **世界不變：**邊界是一個可見的圓環／裂縫／光線；邊界內的微型城邦、住民和內在生命是故事的道德中心。
- **問題不變：**她試圖弄清楚，邊界是在保護生命，還是在把生命隔開？
- **試法可變：**每次只在當前鏡頭使用一種互斥拓撲；鏡頭／美術可改外觀，不可以偷改物件物理。
- **因果不變：**接觸前、首次接觸、接觸後、假修復、重新理解、選擇的時間順序不能倒置。
- **結局可循環：**ACT 6 的邊界線／步伐／光點要能 match-cut 回下一輪 ACT 1。每輪世界有新變化，但不把上一輪的失敗偽裝成成功。

## 每一輪的六幕

| 幕 | 故事事件 | 試法如何入戲 | 預設規則 |
|---|---|---|---|
| ACT 1 — 畫界 | 行人沿著世界邊界行走，看見一道不合常理的光線 | 本輪 TRY 印記第一次出現，像電影章節題字／收藏版印章 | SOFT；可變鏡頭、畫風、場景、隱喻；不必放武器 |
| ACT 2 — 保護 | 她把手放在透明世界外，確認裡面的生命仍安全 | 方法印記像一枚置於留白處的設計標記 | SOFT；不做武器接觸 |
| ACT 3 — 試法／碎裂 | 她選一個本輪方法接近、檢驗或觸碰邊界 | **本輪主試驗在這一幕發生**；標籤寫明幾何家族、接觸態、鏡頭與 Prompt ID | 硬接觸只選一種 GEO 家族；H0/H1/H2/H3 狀態不可混 |
| ACT 4 — 假修 | 世界用漂亮但不可靠的補丁掩蓋裂痕 | 失敗不是剪掉的廢片；標示 REJECTED 或 REVIEW PENDING，裂痕成為劇情線索 | SOFT 為主；不可混入另一種接觸方法 |
| ACT 5 — 一界 | 她看見邊界兩側互相牽連，裡面的生命沒有因外殼破裂而被抹去 | 方法以反射、影子、窗格、紅線、花／門／見證者等隱喻回響 | SOFT；不把特效當幾何證據 |
| ACT 6 — 選擇 | 她不宣稱終於完美成功；她帶著新理解再走一次 | 結尾印記顯示本輪結果與下一輪的差異軸 | SOFT；最後一幀為下一輪 match-cut 留接口 |

### 反覆不是單純複製

每一輪至少有一個「主試法差異」：geometry family、contact state、camera axis、camera ID、windup、wash ID、style ID、video method 或 narrative motif 之一要不同。除非刻意做對照實驗，否則不允許連續兩輪的完整方法指紋相同。人物身份、世界因果和上一輪已發生的故事事實仍然保留。

## 讓總庫方法真正進入劇情

方法不是在故事外面另開技術表。它們各自成為 ACT 3 的一次邊界試法；而 ACT 1／2／4／5／6 的鏡頭與隱喻，讓同一輪有情緒、後果，以及下次重來的理由。

### IMAGE：互斥幾何試法

| 方法 ID | 放進故事的方式 | 禁止混用 |
|---|---|---|
| GEO.T／I-01…05 | 單把 T 槌：H0 空隙、H1 近距、H2 指定端面首次接觸、H3 同軸跟進 | 不可把槌腰、角或手柄當第一接觸 |
| GEO.T2／I-06…07、I-19 | 兩把獨立 T 槌指定端面互相校準，測試「對稱是否等於理解」 | 不可融合成一把 H 形武器 |
| GEO.CROSS／I-08…09 | 厚十字雙槌圓柱端蓋面對面；每輪改變合法末端／軸 | 只允許指定平端蓋先接觸，不可槌腰互撞 |
| GEO.ROD／I-10…11、I-22 | 線形棒 90° 正控制與反向面負控制，成為「看似相交，不代表真的接上」的隱喻 | 正控制與預期失敗的負控制分開標示 |
| GEO.PLANT_SIDE／I-13 | 雙端圓柱先種植在球殼；柄由柱身側面中段切向伸出 | 不可暗中變成軸向外端柄 |
| GEO.PLANT_OUTER／I-14…15 | 球面候選柱中選一枝，柄接在圓柱外端；測試另一種施力入口 | 不可暗中變成側柄中段接柄 |
| GEO.MULTI／I-16…17 | 一柄一頭、多向扁平圓頭，選一塊平面作 H0／H2 | 不可變成 T 槌、厚十字或多柄武器 |
| GEO.NONE | 柔性敘事：手、步伐、絲線、花、門、玻璃、舞蹈，不發生武器接觸 | 柔性幕不可為展示方法而硬塞武器 |

### IMAGE：鏡頭與美術試法

- CAM.T192：I-18 的 **8 軸 × 12 鏡 × 2 蓄力**；只對 GEO.T。每張是獨立全幅，不是 192 格拼貼。
- CAM.DUAL48：I-19 的 **4 軸 × 12 鏡**；只對雙 T 或厚十字候選。
- WASH10：I-22 的十種獨立構圖試法；每次選一種。
- STYLE：S-01 寫實、S-02 粉彩、S-03 超現實、S-04 幾何審核。美術改變情緒和材質，不改物理契約。
- BP_SHOT：六幕／MV 多鏡包；26 鏡和 24 卡是不同剪輯方案，要在 manifest 記明。
- NARRATIVE_MOTIF：原罪／花／門／見證者／內在脈搏等語義核用作不同輪次的寓言。它們是故事層，不是接觸幾何證據。

### VIDEO：每種方法是不同的時間行為

| 方法 ID | 在故事中的表現 | 必須保留的差異 |
|---|---|---|
| V.T10 | 單一 10 秒場景，由遠到近、接觸、衝擊、結尾 | 一段連續動作，不冒充多機位剪輯 |
| V.KF5 | 五狀態：PRE_FAR → PRE_NEAR → CONTACT → MID_SHOCK → END_BLAST | 每個狀態有合法母幀；不可跳過接觸 |
| V.PLANT | 種植圓柱固定原位，人物和鏡頭動，錨點 P 不漂 | 不可變成飛來的 T 槌 |
| V.I2V | 從通過的母圖起步，只允許一個核准變量改動 | 保留母圖身份、場景、接觸錨點 |
| V.T2／V.CROSS／V.ROD／V.MULTI | 每種拓撲有自己的接觸方式和時間軸 | 一條影片只描述一個拓撲家族 |
| V.BP | 六幕短片按鏡頭剪輯成 MV，而非一次幻想出完整三分鐘 | 各段獨立生成，再以母圖與連續性審查銜接 |
| V.TEACH | 乾淨作品、藝術字版、教學板各自輸出 | 字牌不代替影片／像素驗收 |

## 畫中要有藝術字，但不能把準確性交給生成模型

每個成品分兩層：

1. **底圖層：**IMAGE／VIDEO 模型只負責故事影像；底圖 Prompt 明確要求不要任何文字、Logo、水印、UI 或假數據。
2. **藝術字層：**用 SVG／排版器把標題、TRY 方法牌、章節、Prompt ID 與狀態疊在成品上。文字來自 manifest 的確定字串，而不是請生成模型在畫面上拼寫。

這不是把技術板硬貼進作品，而是把方法牌設計成電影海報式章節字：細金屬框、光軌、印章、細字字幕與低調的角落定位線。保持 16:9；標題在上方或留白區，TRY 方法牌在另一角。主角臉、接觸點、武器輪廓和裂紋起點不得被遮住。可用書法／襯線題字配無襯線技術小字；方法碼固定拼寫、保持可讀。

### 每張圖的標記格式

    邊界行人  /  THE BOUNDARY WALKER
    LOOP 001  ·  TRY 0001
    METHOD  GEO.T  /  H2  /  CAM-AX03-CAM07  /  WINDUP-1
    PROMPT  I-04  ·  STYLE S-01
    本輪試法：T 槌指定端面第一次接觸
    狀態：待審  /  REVIEW PENDING

這是版式示例；實際值必須從本次 manifest 取得。若本輪是 GEO.PLANT_SIDE，標籤必須寫側柄種植圓柱；若是 GEO.PLANT_OUTER，標籤必須寫外端接柄圓柱；若是負控制，必須顯示 NEGATIVE CONTROL／預期失敗。不能拿同一張標籤套在不同幾何之上。

### 可執行的藝術字疊加

使用 bubble_break/boundary_pedestrian_try_art.py，把一張實際生成的 PNG/JPEG 作底圖，輸出含內嵌原圖及藝術字層的 SVG。工具同時輸出 JSON sidecar，記錄來源 SHA、藝術版 SHA、Loop／TRY／Act／Method ID；它不會呼叫圖像模型，也不會自行判定像素 PASS。

    python bubble_break/boundary_pedestrian_try_art.py \
      --image path/to/actual_generated_frame.png \
      --out out/boundary_pedestrian/loop001_try0001.svg \
      --loop-id 001 --try-id 0001 --act-id 3 \
      --method-id GEO.T --method-label "T-hammer end-face contact" \
      --prompt-id I-04 --style-id S-01 \
      --note "本輪試法：T 槌指定端面第一次接觸" \
      --status REVIEW_PENDING

若要為影片同一方法加精確字牌，使用相同 ID 生成 ASS 字幕層：

    python bubble_break/boundary_pedestrian_try_art.py \
      --image path/to/actual_generated_keyframe.png \
      --out out/boundary_pedestrian/loop001_try0001.svg \
      --loop-id 001 --try-id 0001 --act-id 3 \
      --method-id GEO.T --method-label "T-hammer end-face contact" \
      --prompt-id V-02 --style-id S-01 \
      --ass-out out/boundary_pedestrian/loop001_try0001.ass \
      --duration-seconds 6

SVG 是帶有藝術字的作品版，JSON sidecar 是追溯記錄；ASS 是後期影片字牌。這些輸出只證明字牌已排版，不證明幾何、人物連續性或影片物理通過。工具預設 REVIEW_PENDING，禁止使用含糊的裸字 PASS；未有真實像素審查，請保留 NOT_RUN／NOT_VERIFIED 狀態。

### 狀態字不得造假

- PROMPT READY：Prompt 已編寫，未必出圖。
- IMAGE GENERATED／VIDEO GENERATED：只表示有輸出媒體。
- REVIEW PENDING：未由人檢查。
- HUMAN ACCEPTED：只有指定圖／幀經人審並記錄該檔 SHA 後才能標示。
- REJECTED／NEGATIVE CONTROL：失敗或預期失敗，仍然保留在故事裡，不能偷偷刪掉或計成 PASS。

所有 TRY 標籤都綁定變體 ID 和原始媒體 SHA。換了底圖就必須重做標籤和 SHA 記錄，舊圖的審核不能沿用。

## 每輪可直接套用的故事 IMAGE Prompt

    Create one single 16:9 cinematic story frame for the ongoing looping film THE BOUNDARY WALKER. This frame belongs to LOOP {LOOP_ID}, TRY {TRY_ID}, ACT {ACT_ID}: {ACT_TITLE}.

    Keep the same adult East Asian heroine from the supplied approved identity reference, with unchanged face, long dark-brown hair, body proportions and canonical outfit. Keep the same world: an immense threshold between an outer ruined city and a small living sanctuary protected inside a translucent boundary sphere. The visual story remains emotionally continuous with the prior accepted frame, but this loop uses the declared new method and must not simply duplicate the previous composition.

    Current method is exactly: {METHOD_ID}. Method description: {METHOD_DESCRIPTION}. Geometry family: {GEOMETRY_FAMILY}. Contact state: {CONTACT_STATE}. Camera: {CAMERA_METHOD}. Style: {STYLE_ID}. Narrative motif: {MOTIF_ID}. Follow only the declared method for this frame. Do not add a second weapon topology or contradictory contact rule.

    Use this act-specific event: {ACT_EVENT}. The emotional subtext is that the heroine has returned to the same boundary because the previous attempt revealed a new question. Keep the inner residents safe and visible whenever the scene calls for them. Use strong composition, motivated lighting, beautiful material contrast, meaningful negative space, and a recurring circular line that can visually connect this frame to the next loop.

    IMPORTANT: create the artwork with no readable letters, numbers, captions, labels, UI, logo or watermark. Accurate title and TRY/method typography will be applied as a separate deterministic art-design layer after generation. Keep planned corner areas calm enough for an editorial title and method stamp without covering the heroine's face, active contact surface, handles, boundary or fracture origin. One full-frame image only; no collage or contact sheet.

    Never claim that geometry or continuity passed merely because this prompt is followed. Render the declared visual event and leave acceptance to actual media inspection.

## 每輪可直接套用的故事 VIDEO Prompt

    Create one standalone 5–8 second cinematic clip for THE BOUNDARY WALKER, LOOP {LOOP_ID}, TRY {TRY_ID}, ACT {ACT_ID}. Use the supplied accepted parent frame and identity reference. Current method: {VIDEO_METHOD}. Underlying geometry family: {GEOMETRY_FAMILY}. Camera/action method: {CAMERA_METHOD}. Style: {STYLE_ID}.

    Keep the same heroine, world landmarks, light direction, boundary shape and declared object topology. Animate only the action described for this shot. Preserve the causal state: {START_STATE} → {ACTION} → {END_STATE}. If this is an impact clip, preserve the selected active face, contact point P, opposing contact normals, and correct PRE/CONTACT/AFTER ordering. If it is a planted-cylinder clip, the planted anchor stays fixed. If it is a soft narrative clip, do not introduce a weapon impact.

    Do not add extra weapons, extra limbs, new handles, topology changes, teleporting objects, unexplained camera cuts, random cracks or changes to the sanctuary residents. Keep the focal action readable and do not let particles or bloom hide the event.

    Do not generate text, subtitles, logos, fake interface labels or watermarks inside the video. The exact loop number and TRY method will be composited as an editorial lower-third / chapter stamp after rendering, using the same manifest as the still images. The clip must end on a frame that can cut cleanly into the next act or loop; do not pretend separate shots are one continuous take.

## 連續輪迴的排程規則

1. 以全量 ID 清單作第一輪隊列；清單是排程來源，不代表所有 ID 都已生成。
2. 每次生成前先選下一個尚未執行的合法 ID，回填 LOOP_ID、TRY_ID、ACT_ID、METHOD_ID、Prompt 版本、風格、鏡頭、來源母圖 SHA。
3. 按合法乘積表的 lane／拓撲限制過濾；柔性幕不得硬塞碰撞，側柄種植和外端接柄不得混句，T 槌和厚十字不能互換。
4. 同一輪的 ACT 1–6 使用同一主 TRY ID；各鏡的 SHOT_ID 可不同。若一輪有多個獨立方法比較，另加 SUBTRY_ID，不能用一個標籤掩蓋多個不同方法。
5. 每張作品輸出底圖和藝術字版兩份；底圖保留原始媒體，藝術字版另記輸出 SHA。影片的字牌亦用後期向量字幕／lower-third，不要讓模型每幀重寫文字。
6. 不論成功或失敗都保留。失敗會推動 ACT 4 假修與 ACT 5 新理解；下一輪改方法，不是偷偷放寬接觸規則。
7. 第一輪所有合法 ID 走完才標記 SWEEP 1 COMPLETE。下一輪採用新 seed 或新敘事 motif，並區分新組合／重試，不把「重新出圖」冒充新方法。

## 從一輪接到下一輪

ACT 6 的最後鏡頭以女主再次踏上發光邊界作結。她的腳印形成不閉合的圓；下一輪 ACT 1 從同一圓弧、同一方向的腳步開始，但邊界另一側的世界、光色、鏡頭／試法牌已有變化。方法字牌在剪接點切換成新的 TRY_ID，讓觀眾一眼知道故事回來了，這次試法不一樣。

## 驗收邊界

本文件把故事結構、方法選擇、Prompt、標記規格和排程串起來；它不會自動產生所有變體的媒體。只有執行過生成、保存真實 raster／影片、記錄 manifest 與 SHA，並按指定幾何及相鄰幀規則完成實際檢查後，才能逐項更新媒體狀態。PROMPT_READY、IMAGE_GENERATED、PIXEL_AUDIT_PASS、CONTINUITY_PASS 和 VIDEO_AUDIT_PASS 是不同狀態，不得互相替代。
