# 圖像 Prompt 公式教學｜Bubble／Hammer 全嘗試統整

> Repo: JUN-ZS/ai-image-gen-logic-review  
> 基準：main @ 03934ba4f147e5f85937068e1113f2f62198f8e6（2026-10-23 核對）。  
> 文件狀態：跨分支規格手冊，不是單次生成成功的證明。

## 輸出規則：乾淨打擊圖 + 精確教學／驗收板

完整板式與命令參考：[Prompt Evidence Board 使用指南](PROMPT_EVIDENCE_BOARD.md)。

每次 attempt 預期交付兩個視圖，而不是讓圖像模型把數據字硬畫進成圖：

1. **SOURCE RASTER**：純打擊畫面。Prompt 要求 no text / no labels / no panel grid，保留原始輸出供像素驗收。
2. **PROMPT EVIDENCE BOARD**：將該張 raster 原樣嵌入 SVG，再由程式以真實 manifest 加上 attempt ID、branch／commit、topology、改動變量、數字參數、EXPECTED vs OBSERVED、接觸點 ROI、失敗原因、下一輪變量及審查狀態。標籤與數據是確定性渲染，避免模型把數字或中文字拼錯。

編譯工具：`bubble_break/prompt_evidence_board.py`；矩陣 Prompt 封包編譯器：`bubble_break/prompt_attempt_packet.py`；資料契約：`schemas/prompt_attempt_manifest.schema.json`；樣本：`examples/prompt_attempt_manifest.example.json`。例子中的 placeholder 不是實際實驗數據。

~~~bash
python bubble_break/prompt_evidence_board.py --manifest examples/prompt_attempt_manifest.example.json --out out/prompt_evidence/TRY-0001.svg
# 真實圖片到手後，將 --image 指向該次原始 raster，再生成同一 attempt 的註記板
python bubble_break/prompt_evidence_board.py --manifest out/attempt.json --image out/attempt.png --out out/prompt_evidence/TRY-0001.svg
~~~

若沒有附上原始 raster，板上會明確顯示 NO SOURCE RASTER ATTACHED；程式不會把 Prompt PASS 或 SVG proxy PASS 改寫成 image PASS。Pixel Audit 的 PASS 只有在 review receipt 的 SHA-256 與實際 raster 一致、且 verdict=PASS 時才會顯示。這仍依賴可信的實際審查者；工具本身不會自動看懂碰撞。

## 0. 核心原則：所有分支都在打泡，但不是同一種槌

不可把所有分支揉成一條 mega-prompt。現有嘗試有互斥的武器拓撲：

| 代號 | 物件拓撲 | 真正接觸規則 | 角色 |
|---|---|---|---|
| A 側柄雙頭圓柱 | 短雙頭圓柱沿泡面局部法線放置；單柄接圓柱側面中段，沿切線伸出 | 圓柱底端的順球面貼合座接觸泡殼；光與裂源於同一錨點 P | Planted-bubble 主線 |
| B T 字槌 | 一把剛性 T 槌；柄接槌頭中段並與槌頭軸垂直 | 指定終端打擊面先接觸球面，法線相反 | T-Hammer 打泡 H0/H1/H2/H3 |
| C 厚十字／CYLINDER_CROSS 雙槌 | 兩把獨立十字槌，各自完整槌頭與柄 | 兩個指定外側平端蓋面對面；槌腰、角、柄與中心接點不准先碰 | 幾何碰撞與候選抽樣 |
| D 線形擊打棒 | 兩支細直剛性棒，各有小型平面撞擊面 | 棒軸成 90°，兩平面法線相反；另設刻意錯面的負控制 | 正確／反例辨別實驗 |
| E 多向扁平槌面圓頭 | 一柄一頭；多個向外平坦槌面形成整合式圓頭 | 面向泡泡的外向平面是 active face，裂由此處開始 | 槌2.txt 的武器進化選項 |

每次 run 先選一種拓撲。A 不能偷偷長出 T 槌的外端長柄；B 不能變成斧；C 的雙槌不能融合成一把 H 型武器；E 不能變成刺球或鏈錘。錯了就是拓撲 FAIL，不是美術風格差異。

## 1. 共用 Prompt 編譯公式

~~~text
IMAGE_PROMPT =
  OUTPUT_CONTRACT
+ HERO_IDENTITY
+ SCENE_STATE
+ ONE_WEAPON_TOPOLOGY
+ CONTACT_CONTRACT
+ ACTION_STATE
+ TARGET_STATE
+ CAMERA
+ LIGHT_AND_GRADE
+ AUTHORIZED_DETAILS
+ NEGATIVE_CONSTRAINTS
~~~

正確流程：

~~~text
PHYSICS / GEOMETRY TRUTH
        ↓
VISUAL PRIMITIVE（能畫出清晰輪廓）
        ↓
PROMPT COMPILER
        ↓
REAL IMAGE GENERATION / EDIT
        ↓
PIXEL AUDIT ON THE EXACT RASTER
        ↓
PASS → 才能成為下一步 parent
FAIL → 診斷錯誤槽，只改該槽，從最後 PASS 重新生成
~~~

程式測試通過，代表資料模型／提示詞編譯符合規格；SVG 通過代表幾何代理生成成功；兩者都不能證明外部模型真的畫對。

## 2. 永久槽、可變槽與升級規則

### 必須鎖住的永久槽

- 單張 16:9；不以拼貼格代替一張可檢驗的畫面。
- 同一系列的角色身份、服裝、場景 ID、背景地標、相機 rig、光源方向。
- 一個主要透明泡泡；接觸前保持完整。
- 武器拓撲、頭柄連接、剛性、錨點 P 與 active face。
- 接觸前後狀態：H0/H1 有正空隙；H2 gap=0 且不穿模；H3 沿指定軸推進；裂由 P 擴展。
- 內部居民／聖所是保護對象，不是被打擊的目標。

### 可變槽

撞擊軸、蓄力姿勢、重心與腳步、鏡頭方位／仰俯／焦距、景別、服裝、場景棚、色彩、光影、粒子與碎片。每輪只改 1–2 個變量，並寫明預期差異。

### k 層：由可畫到好看

- k=0：人物、指定武器、泡泡、接觸點；先過拓撲。
- k=1：加服裝與材質，凍結接觸區。
- k=2：加實景與背景地標。
- k=3：加電影光、色調、景深。
- k=4：加接觸光、裂紋與碎片。

若高階畫面變形，回到最後一張通過的低階母圖；不要用 more powerful、epic、ultra-detailed 去掩蓋錯面接觸。

### 最小 CORE Prompt

~~~text
One single photorealistic 16:9 frame.
A consistent female warrior stands left of frame, holding the specified approved weapon in both hands.
One large intact transparent crystal sphere occupies the right side.
The explicitly designated active striking surface makes the only first contact at point P.
The sphere is intact before contact; cracks begin only at P after contact.
Keep the complete weapon, handle joint, both hands, contact seam, and sphere surface readable.
No extra weapon, no missing weapon, no text, no watermark, no panel grid.
~~~

電影質感只在 CORE 通過後加入：high-budget cinematic music-video photography、motivated volumetric light、controlled bloom、fine film grain、emotional grade、off-center composition；禁止它改變已驗收的拓撲或接觸點。

## 3. A 線：雙頭圓柱側柄／泡面錨定公式

來源：main 的 DENSE_HAMMER_BUBBLE_SELECTION_WORKFLOW.md、STAGE_FAILURE_SUCCESS_REWRITE_LOG.md，以及 Gemini／Shannon planted-bubble 文件。

比例設計目標：

~~~text
D_h = 0.08 × D_b
H_h = 1.5 × D_h
L_g = 3 × H_h
D_g = D_h / 10
~~~

D_b 是泡泡直徑；D_h 是圓柱直徑；H_h 是圓柱軸向高度；L_g 是側柄長；D_g 是柄徑。比例只是設計目標；真實產圖需另量像素。底座使用順球面曲率的 conformal seat，不能要求平圓片無過渡地完美貼合曲面。

### A0：候選圖譜

~~~text
Create one seamless 16:9 raster image of a single large intact translucent sphere.
Place up to 24 separately readable double-ended short cylindrical hammer heads at irregular points on the visible hemisphere.
Each cylinder axis follows the local radial direction. Its bubble-facing base uses a sphere-conforming seat with a narrow luminous base-to-shell contact seam.
One thin straight handle attaches at the cylinder side-middle and extends sideways in the local tangent plane, approximately perpendicular to the radial axis.
Keep each cylinder, side joint, and complete handle independently traceable, with negative space between neighboring tools.
No people, no hands, no swinging, no cracks, no debris, no hammer-to-hammer collision, and no regular tile grid.
Return the original full-resolution raster. If 24 tools cannot stay legible, use fewer rather than fake the topology.
~~~

### A1：選一個真實 raster 並隔離

以實際 A0 原圖選 Cxx，再以該圖做 reference edit。保留其泡面錨點、圓柱兩端、底座 glow、側柄接點與柄向；其餘候選的頭、柄、ID、光暈與殘影全部移除。SVG／JSON 位置只是導航提示，不是像素真值。原圖根本沒柄就判 FAIL，不能靠 Prompt 宣稱它存在。

### A2：加入迷你人物，先不握柄

~~~text
Use the accepted isolated single-cylinder raster as the exact image reference.
Add exactly one miniature female warrior beside it; her full-body visual area is approximately the hammer assembly's visual area.
Do not change the cylinder, base contact, side-middle handle, handle axis, sphere, camera, or background.
Her hands are near the existing handle but do not grip it yet.
Do not create, extend, duplicate, or move any rod or handle. Keep the outer circular end cap clear.
~~~

### A3：只握原本已存在的側柄

~~~text
Use the immediately preceding accepted raster as parent. Change only wrist and hand placement so both hands grip the same already-visible side-middle lateral handle.
Pixel-lock the handle shaft, side-middle joint, cylinder body, outer end cap, bubble anchor P, camera, and all background landmarks.
No new handle, no axial shaft, no second rod, no tool redesign, and no person rescaling.
If the existing handle cannot be gripped without changing its pixels or axis, reject this candidate and return to the last accepted parent.
~~~

### A4：動作與受力

只改肩胯旋轉、重心、腳步、手臂張力、視線；凍結工具拓撲、既有握柄、泡泡錨點和相機。明列 authorized_delta_fields，不接受「整體優化」這種無邊界修改。

### A5：接觸光與破殼

~~~text
Use the accepted parent raster and preserve its exact tool topology, contact anchor P, character identity, camera, and scene landmarks.
Increase the light only at the selected cylinder-base / sphere interface P.
The first fine radial cracks begin at P and propagate over the outer shell.
For the end state, fracture the shell outward from P with coherent outward-moving fragments and a visible shock ring.
The inner sanctuary and inhabitants remain intact and unharmed. Keep one clean frame where the contact seam is not hidden by bloom or debris.
Do not create a new contact point, move the tool, or crack the sphere before the defined contact stage.
~~~

A 線是側柄圓柱方案；不要把 T 槌的接觸句直接混進來，除非明確重定義圓柱的 active face 與運動方向。

## 4. B 線：T 槌對泡泡的 H0／H1／H2／H3

來源：T_HAMMER_MULTIVIEW_SWING_ENGINE_SPEC.md、槌2.txt、REAL_SCENE_BUBBLE_BREAK_WORKFLOW.md、Original Sin engine。

幾何條件：一把剛性 T 槌；指定終端打擊面法線為 n；球面外法線為 −n；槌頭長軸與 active end-face 法線共線；柄接槌頭中段並與槌頭軸垂直。第一接觸面只可為指定終端平面，禁止 cheek、長側壁、角、柄或中心接點先碰。

### H0 — 接觸前

~~~text
Single 16:9 cinematic frame using the locked heroine, approved rigid T-hammer, same sphere, camera rig, and background.
The selected terminal striking face is visibly separated from the intact sphere by a clear positive air gap along collision normal n.
The hammer head is already oriented for face-first contact; its handle remains perpendicular to the head axis and fully visible.
No cracks, contact glow, sparks, debris, or contact shadows implying a collision.
~~~

### H1 — 接近但仍有正空隙

~~~text
Use the accepted H0 raster as reference. Reduce only the face-to-sphere air gap while keeping it strictly positive.
Translate the same rigid hammer along n; do not rotate the head independently, bend the handle, change the character, or re-layout the background.
The sphere remains whole. No contact glow, cracks, or debris before H2.
~~~

### H2 — 第一次端面接觸

~~~text
Use the accepted H1 raster as parent. The designated flat terminal end-face reaches exactly point P on the sphere; the air gap becomes zero without interpenetration.
The striking-face normal and sphere outward normal oppose one another. The cheek, corner, handle, and center joint remain clear.
Show a restrained initial contact glow and first fine cracks starting at P only. No full explosion yet.
~~~

### H3 — 沿同一軸跟進

~~~text
Use the accepted H2 raster as strict reference. Advance the same rigid hammer a small declared distance along the same collision normal n; preserve the head-to-handle geometry and camera.
Cracks grow outward from the same P, and shell fragments move outward from the shell, not from the weapon or random background points.
The inner sanctuary remains intact. Keep the hammer, grip, contact zone, and fragment trajectory readable.
~~~

若使用 main 的 T-Hammer multiview 尺寸契約：雙槌 H0 總 gap=50 units（每端距 P 25）；H2 gap=0；H3 沿 +n 前進 15 units。單槌打泡的 H0 是距球面 50 units。不要把雙槌總 gap 誤當成每一把各 50。

B 線負面詞：no cheek-first impact, no long-sidewall contact, no corner-first contact, no handle-first impact, no spear-like handle through the sphere center, no bent/telescoping weapon, no detached head, no extra shaft, no early cracks, no hovering gap at H2, no interpenetration, no random crack origin, no effect bloom hiding the contact seam.

## 5. C 線：厚十字／CYLINDER_CROSS 雙槌

來源：feat/cylinder-cross-dense-atlas 與 SPEC_H_vs_H_TERMINAL_FACE_MATRIX.md。

兩種採樣不可混為一談：

- **48 張獨立接觸矩陣：**4 個撞擊軸 × 12 個鏡頭，每張獨立生成、獨立審核，H0/H2/H3 分開。
- **一張稠密 atlas：**畫面內嘗試多組碰撞候選，目標可為 24 對／48 柄。用途是找候選，不是替代 48 張獨立 H2 證據。

單張雙槌 Prompt：

~~~text
Create one full-frame 16:9 geometry-proof image of exactly two independent complete plus-shaped cross hammers.
Each hammer has one rigid horizontal crossbar, one rigid vertical arm, and one long straight handle fixed to its own center joint.
Never merge the weapons into a single H-shaped object.
Only the selected outer circular end caps may make first contact, flat face to flat face, with coincident planes and opposing normals at P.
Crossbar barrels, broad sides, vertical arms, corners, center joints, and handles remain clear.
Both complete handles and both cap boundaries must be visible. Tiny sparks must not cover the seam.
No labels, panel borders, or collage.
~~~

main 的 T-Hammer multiview 是另一矩陣：8 個三維撞擊軸 × 12 個鏡頭 × 2 種蓄力 = 192 個試驗。它不等於上述 48 矩陣，也不等於一張 atlas。每個 run 必須照自己的 manifest 編譯。

## 6. D 線：線形棒正控制／負控制

來源：feat/dual-actor-correct-vs-inverse-strike。正控制使用兩支細直剛性棒，棒軸以 90° 相交，兩個小型平面撞擊面互相平行並面對面接觸。負控制刻意將撞擊面翻離接觸方向，或設定錯誤同軸碰撞；標記 EXPECTED_FAIL_NEGATIVE_CONTROL，不得混入 PASS 計數。這條線不是主角持槌 Prompt。

## 7. E 線：一柄一頭、多向扁平面圓槌

來源：槌2.txt 的後期武器公式，作獨立選項。

~~~text
She holds ONE war hammer: a single long handle ending in ONE rounded hammer head.
The head looks spherical because many thick wide flat metal striking faces point radially outward.
The striking surfaces are broad flat facets, not spikes or studs. They belong to one integrated head, not separate miniature hammers.
The outward facet aimed at the sphere is the only active face and visibly meets the glass at P.
No morning-star chain, no flail, no halo of hammers, no extra handle, no axe.
~~~

若模型畫成刺球、鏈錘、槌環，或將各面拆成多把武器，判 FAIL。不要同一 Prompt 同時要求乾淨 plus-sign 和多向圓頭。

## 8. 敘事公式：Original Sin／《邊界行人》

來源：槌1.txt、槌2.txt、Original Sin story engine 與 EFV story expansion。

~~~text
STORY = SYSTEM_PROMISE
      + HIDDEN_CONTAINMENT_MECHANISM
      + VISIBLE_SYMPTOM
      + HUMAN_COST
      + CLUE_AT_P
      + HERO_DISCOVERY
      + PHYSICAL_ACTION
      + SHELL_ONLY_BREACH
      + RESTORED_AGENCY
~~~

六幕：1 畫界；2 保護；3 碎裂；4 假修；5 一界；6 選擇。三分鐘 MV 可採約 50–54 鏡，或每幕 4 張關鍵卡共 24 張。六棚選項包含霓虹塗鴉工作室／廢工廠、復古扭蛋遊樂場／金廳、粉彩超市、糖果藥房餐廳、乾涸泳池、破片天台黎明。

55/30/15 是故事注意力的啟發式（主體／舊動機變形／下一故事伏筆），不是實際像素比例、經校準的模型注意力或物理法則。

每鏡公式：

~~~text
SHOT = CONTRACT + HERO + GEAR + ACTION
     + ONE_WEAPON_TOPOLOGY + TARGET + SET
     + CAMERA + LIGHT + GRADE + NEGATIVE
~~~

同一張只選一個武器槽；六幕只換允許改動的故事槽，武器句盡量不動。柔抱鏡不要硬塞錘；打擊鏡必須明確保留武器與接觸契約。

## 9. 負面詞按拓撲選擇

- 共用：blurry, low quality, deformed hands, extra fingers, watermark, text, extra limbs, extra weapons.
- A 側柄圓柱：no outer-end new shaft, no axial rod, no missing lateral handle, no floating base, no base glow on outer cap or grip joint.
- B T 槌：no axe, no cheek-first, no corner-first, no handle-first, no bent head/handle, no spear-line through sphere center.
- C 十字槌：no T-head, no X-head, no missing vertical/horizontal arm, no short handle, no center-joint collision, no fused hammers.
- D 線形棒：no coaxial end contact, no gap between intended facets, no unlabelled negative control.
- E 圓頭：no spikes, no flail, no chain, no halo of separate hammers, no extra handles.
- 全部：effects must not obscure the contact seam; camera angle must not conceal a geometry failure.

## 10. 共用像素審查表

- [ ] 武器拓撲、柄頭連接與指定 active face 正確。
- [ ] 第一接觸面正確；P 位置可辨認，無穿模與漂浮。
- [ ] H0/H1 gap>0，H2 gap=0，H3 沿指定軸推進（若適用）。
- [ ] 泡泡接觸前完整，裂紋由 P 開始。
- [ ] 相機沒有把側面碰撞偽裝成端面碰撞。
- [ ] 內部聖所與居民保持安全。
- [ ] 角色、場景、parent raster、mask 與審查收據都可追溯。
- [ ] 像素審查收據綁定最終無損 raster SHA-256。
- [ ] 負控制明確標記 EXPECTED_FAIL，不計入正樣本。

**原則：幾何契約負責不變，Prompt 公式負責可畫，真實像素審查負責判真偽。**
