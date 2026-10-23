# 影片 Prompt 公式教學｜打泡動作、關鍵幀連續性與 MV 整合

> Repo: JUN-ZS/ai-image-gen-logic-review  
> 基準：main @ 03934ba4f147e5f85937068e1113f2f62198f8e6；參照 V5／V5.1、Gemini、Shannon continuity 分支與槌1.txt／槌2.txt。  
> 本文件是可複用的影片 Prompt／驗收規格，不宣稱 repo 已連接任何外部影片生成器。

## 0. 先選影片模式

| 模式 | 輸出目標 | 應用 |
|---|---|---|
| A. 10 秒單場景打泡短片 | 蓄力、接近、第一次接觸、裂紋、破殼；同場景且因果連續 | T 槌 H0/H1/H2/H3 或明確指定的 C13 時間軸版本 |
| B. 多關鍵幀 closed loop | 每一幀獨立生成、審查、綁定母圖與允許變更區域 | V5.1 continuity；優先證據與可靠性 |
| C. 三分鐘敘事 MV | 6 幕；約 24 張關鍵卡或 50–54 鏡頭；可換棚、換隱喻、發展角色弧 | 《邊界行人》／Original Sin／EFV 主題擴展 |

不可同時拿十秒物理動作和三分鐘高頻換棚當同一個時間規格。先選模式，再組 Prompt。

## 1. 影片總公式

~~~text
VIDEO_PROMPT =
  MASTER_SCENE_STATE
+ STORY_CAUSAL_CHAIN
+ TIMECODED_BEATS
+ KEYFRAME_STATE_CONTRACT
+ MOTION_PATH
+ CAMERA_PATH
+ AUTHORIZED_DELTA_FIELDS
+ CAUSAL_FX
+ CONTINUITY_GATES
+ NEGATIVE_CONSTRAINTS
+ OUTPUT_CONTRACT
~~~

圖片 Prompt 定義某幀「是什麼」；影片 Prompt 還必須寫明「上一狀態如何，沿哪條路徑，因什麼事件轉換為下一狀態」。

每個時間段指定四件事：

- 不變量：身份、服裝、武器拓撲、球心／半徑、錨點 P、場景地標、相機 rig、光源方向。
- 唯一合法變化：距離、姿勢、運動方向、裂紋、碎片或相機運動。
- 物理因果：接觸前完整；接觸瞬間才出現第一道裂紋；裂紋從 P 傳播；最後只破泡殼。
- 證據：真實 raster、父圖 SHA、master anchor SHA、edit/freeze mask、逐幀審查收據。

## 2. 可直接使用的 10 秒單場景影片 Prompt

以下版本屬於「打擊物由空隙接近泡面」的時間軸。若選用底座已貼住泡面的 planted-cylinder 母版，不可同時宣稱 0 秒仍有空隙；第 4 節另有 planted-cylinder 專用版本。

~~~text
Create one continuous 10-second photorealistic cinematic 16:9 shot, not a montage and not unrelated scenes stitched together.

MASTER STATE:
Use the same approved female warrior, same identity and outfit, same approved rigid weapon topology, same single translucent sphere, same sphere center and radius, same contact anchor P, same scene landmarks, same camera rig and motivated light direction throughout.
The inner sanctuary and its inhabitants are protected. They are never struck.

PHYSICAL ACTION:
The heroine transfers force through her hands, the handle, the rigid hammer head, the designated active striking face, and then the sphere at P.
The weapon head does not bend, detach, rotate independently, or change into an axe, spear, spiked mace, or different hammer.

TIMELINE:
0.0–2.0 s — PRE_FAR: the designated active face is clearly separated from the pristine sphere by a wide positive air gap. The heroine is winding up. No contact light, cracks, or debris.
2.0–4.5 s — PRE_NEAR: the same rigid weapon advances along the declared impact path. The air gap narrows but stays positive until contact. The head-to-handle angle remains locked.
At 4.5 s — CONTACT: the designated flat active face meets the sphere exactly at P. The gap becomes zero with no interpenetration. The first restrained contact glow and first micro-cracks begin at P only.
4.5–7.0 s — E_MID: radial cracks and concentric shock ripples propagate outward from P across the shell. Camera and scene landmarks remain stable; any follow-through follows the declared path.
7.0–10.0 s — E_END: the outer shell breaks outward from P into coherent fragments. The inner sanctuary stays intact and unharmed. End on a readable composition, not an all-white explosion.

CAMERA:
Use one continuous motivated camera move. Preserve the contact point and weapon geometry. No teleporting camera, hidden geometry reset, fake impact through zoom, or background replacement.

VISUAL PRIORITY:
The active face, contact seam, handle joint, both hands, crack origin, and intact inner sanctuary remain inspectable. Control the bloom so it does not hide the contact geometry.

FORBIDDEN:
No early cracks, false contact, gap at the impact instant, mesh interpenetration, cheek-first or handle-first impact, newly invented shaft, extra weapon, scene re-layout, character identity or scale changes, vertical splice seam, random crack source, resident injury, text, or watermark.

DELIVERABLE:
One continuous 10-second 16:9 clip with five internally coherent timeline states. If continuous motion cannot be guaranteed, generate and audit five separate keyframes instead of claiming continuity.
~~~

## 3. 五個關鍵幀：每一幀只有一組授權變化

### KF1 — 0.0 秒 PRE_FAR
泡泡完整；active face 和球面有清楚正距離；人物在準備動作。沒有接觸 glow、裂紋或碎片。保存場景地標、鏡頭、武器拓撲與 P 的主錨點。

### KF2 — 2.0 秒 PRE_NEAR
只允許空隙縮短、身體重心與手腳進一步前移；空隙仍大於零。背景不能重排，武器不能變形，不能有撞擊特效。

### KF3 — 4.5 秒 CONTACT
指定端面觸及 P，gap=0，不穿模；法線關係正確。只出現受控接觸光與第一道微裂，不能直接跳成全爆炸。

### KF4 — 7.0 秒 E_MID_SHOCK
只准裂紋從同一 P 向外擴散、外殼局部裂開與衝擊波傳播。主角與武器保持連接；背景和內部場景不重排。

### KF5 — 10.0 秒 E_END_BLAST
泡殼碎片沿合理裂面向外擴散；內部居民與聖所仍完整。最後畫面保留人物、武器與破殼輪廓，不能由特效淹沒主體。

### 關鍵根因與修法

V5 診斷指出，從遠距 PRE_FAR 無遮罩一路串行重繪，模型可能失去泡面幾何錨點，把側柄圓柱重畫成同軸大錘或躺倒鐵管。可靠做法是先鎖定已通過的接觸母版，再用明確的剛體位移和授權區域推導前後幀。不可把每一幀當成完全自由的新圖。

## 4. planted-cylinder 專用時間軸（不能和飛行槌版混用）

若 A 線的雙頭圓柱底座從第一幀起就貼住球殼，這是「接觸錨點已固定、人物透過側柄施力／扭矩」的版本，不是從空中飛過來的 T 槌。使用以下狀態：

~~~text
PLANTED-CYLINDER CLIP:
Keep point P, conformal base seat, cylinder axis, the side-middle lateral handle, and the opposite clear outer end cap locked to the accepted master.
The base-to-shell interface remains the only contact anchor. The heroine's grip, shoulders, hips, stance, and applied torque evolve across frames.
At the defined force-transfer beat, energy and cracks begin at the same base interface P, then propagate outward over the shell.
Do not create a pre-impact air gap unless a separate, verified PRE_FAR parent was explicitly created for this version.
Do not invent or move a handle. Preserve the same lateral handle pixels or return to the last accepted parent.
~~~

B 線有正空隙的 H0/H1；A 線可採「錨點已接觸」母版。任何一次 run 必須在 manifest 明確聲明是哪一種，不能同時說底座始終貼住，又說 PRE_FAR 距離球面 50 units。

## 5. SceneState、授權差異與真實閉環

每個 stage/keyframe 應綁定：scene ID、parent PASS raster SHA-256、master anchor SHA-256、frame time、authorized_delta_fields、frozen_fields、P 的識別與位置、freeze mask、edit mask、最終 raster SHA、review receipt。

結構示例（佔位 SHA 不可當成實際收據）：

~~~json
{
  "scene_id": "one_stable_scene",
  "frame_time_s": 4.5,
  "parent_pass_sha256": "REPLACE_WITH_REAL_PARENT_SHA",
  "master_anchor_sha256": "REPLACE_WITH_REAL_MASTER_SHA",
  "authorized_delta_fields": ["contact_gap", "contact_glow", "first_micro_cracks"],
  "frozen_fields": ["character_identity", "weapon_topology", "camera_rig", "background_landmarks", "sphere_geometry"],
  "contact_point_id": "P",
  "image_realization": "MUST_BE_REAL",
  "pixel_audit": "PENDING"
}
~~~

每次 FAIL 後，不是只輸出 repair_prompt.txt 就算重試；必須真的重新呼叫 generation backend，使用最後一張 PASS 母圖、受限遮罩與拒絕理由。該輪仍失敗就 BLOCK，不可把最高分 FAIL 圖偷渡至下一幀。synthetic test raster 要標記 SYNTHETIC_TEST_ONLY，不能冒充實際生產圖。

### Layer 1：硬閘門
- 真實單張 raster；非拼貼／非測試合成圖。
- 角色身份、武器拓撲、柄軸、球體、P 正確。
- H0/H1 有空隙，H2 無空隙但不穿模，H3 沿已定軸跟進（依選定模式）。
- 背景地標與相機符合鎖定；freeze mask 外的像素不應變更。
- pose signature 按指定動作改變；不能一整串只是相同姿勢複製。
- 真實 reviewer／semantic-vision 收據綁定最終無損 raster 的 SHA。

### Layer 2：創意排序
只有 Layer 1 全部 PASS 才比較姿勢演化、鏡頭美感、內部聖所可見度、色調與碎片戲劇性。創意分數不能救回物理 FAIL。

V5／Shannon 文件出現過 NCC ≥ 0.78、亮度差 ≤ 16、人物高度小於泡泡直徑 60%、相鄰幀人物比例變化不超過 18% 等門檻。它們是可調工程啟發值，不是普遍視覺定律；需和 ROI、相機政策與實際 reviewer receipt 一起核對。

## 6. 鏡頭矩陣：改變視角，不改變幾何

main 的 T-Hammer multiview spec 規劃 8 個三維撞擊軸 × 12 個鏡頭 × 2 種不同蓄力方式 = 192 個試驗。另一條 T 端面矩陣是 4 個軸 × 12 個鏡頭 = 48 個變體；CYLINDER_CROSS atlas 則是一張稠密取樣圖。三者不能混用一份計數或同一條驗收聲明。

可獨立變動的鏡頭槽：
- 全身側三分之四：主角、槌、球和距離都可見。
- 接觸微距：審核端面、接觸 seam、裂源，不作唯一證據。
- 低角度英雄鏡：增加力量感，同時保留 active face 可讀性。
- 高機位／俯視：檢查接觸軸與球面位置。
- 景深方向鏡頭：可變投影，但不能改世界法線。
- 過肩／跟拍：突出人物動作，背景身份仍穩定。

密集 atlas 可以用來找候選；正式影片關鍵幀必須是獨立全幅圖、有母圖與狀態契約，不能用一張 20 格拼圖假裝有連續動作。

## 7. 三分鐘《邊界行人》／Original Sin MV 公式

來源：槌1.txt／槌2.txt 與 Original Sin story engine。

~~~text
ACT 1 畫界：混亂 → 建立 A／B 邊界
ACT 2 保護：所愛被放進完美泡泡 → 保護逐漸成為窒息
ACT 3 碎裂：泡殼破裂 → 保護者與被保護者共同承擔
ACT 4 假修：濾鏡、止痛劑、替罪羊 → 假安全
ACT 5 一界：回到破碎真實 → 停止以邊界控制彼此
ACT 6 選擇：重建泡泡，或在碎片上自由起舞
~~~

三分鐘歌曲可用約 50–54 鏡；精簡法是每幕 4 張 key cards，共 24 張。這是編排設計，不是已生成的產出數量。

每鏡公式：

~~~text
SHOT =
  LYRIC_OR_BEAT_MEANING
+ PHYSICAL_METAPHOR
+ HERO_STATE
+ A_OR_B_WORLD_STATE
+ ONE_CAMERA_SETUP
+ ONE_MOTIVATED_ACTION
+ LIGHT_AND_PALETTE
+ CONTINUITY_LINK
~~~

六棚可依敘事依序選擇：霓虹塗鴉工作室／廢工廠、復古扭蛋遊樂場／金廳、粉彩超市、糖果藥房餐廳、乾涸泳池、破片天台黎明。角色身份要鎖定；柔抱泡泡的畫面不要硬塞武器；打擊畫面必須清楚保留武器與接觸契約。

55/30/15 是故事注意力啟發式，不是可量測像素比例或模型 attention 的保證。

## 8. 影片交付清單

- [ ] 已選影片模式 A／B／C，沒有混淆時間尺度。
- [ ] 已選物件拓撲 A 側柄圓柱或 B T 槌等互斥路徑。
- [ ] 每個時間點只改狀態表授權的欄位。
- [ ] 每幀是實際生成的 raster，並有 parent/master SHA、mask 與審查收據。
- [ ] 接觸前後的幾何、破裂因果及居民安全通過。
- [ ] FAIL 會從最後 PASS 回滾並真正重新調用生成器。
- [ ] 已逐幀檢查影片輸出；VIDEO_RENDERED 不等於 VIDEO_AUDIT_PASS。

**不放棄的不是同一個 Prompt，而是同一個可驗證目標。失敗時可以換方法，不可以改寫事實。**
