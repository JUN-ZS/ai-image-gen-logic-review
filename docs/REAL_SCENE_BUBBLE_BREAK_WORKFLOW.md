# 由 Repo 現有 Prompt 到「真人女主在真實場景擊破泡泡」的逐關流程

> 目的：沿用 `槌2.txt` 的角色鎖定、可畫核心、武器端面和像素審核規則；先驗證 T 字槌接觸幾何，再做寫實場景，最後交付 H0（未碰）、H2（首次碰撞）、H3（泡殼爆裂）三張相互連貫的完成圖。
>
> **重要界線：** `bubble_break/` 會生成 Prompt、JSON、SVG 幾何參考和局部編輯規格；它不會呼叫圖片模型。只有實際出圖並檢查像素，才能宣稱真人完成圖驗收通過。

## 0. 先取對的 Prompt 與程式

主要 Prompt 源檔在 repo 的 `main` 分支：
- [槌2.txt（現用公式與完整 Prompt 記錄）](https://github.com/JUN-ZS/ai-image-gen-logic-review/blob/main/%E6%A7%8C2.txt)
- [槌1.txt（較早的隱喻分鏡存檔）](https://github.com/JUN-ZS/ai-image-gen-logic-review/blob/main/%E6%A7%8C1.txt)

程式則在 `feat/original-sin-bubble-break-engine` 分支的 `bubble_break/`。截至目前，兩個分支未完全同步；只 checkout 功能分支時，唔好假設根目錄一定有 `槌2.txt`。

建議先讀 `槌2.txt` 的這幾部分，而不是把整份歷史檔一次過餵給圖片模型：
- 影像契約、角色及場景層疊：1.4、1.5、S10。
- 可複製公式：3.1；武器結構先用可辨認的 T 頭版本，之後才比較多向圓頭版本。
- 六幕與完整 Prompt 組裝：後段的 `HERO + GEAR + WEAPON + ACTION + TARGET + SET + CAM + LIGHT + GRADE`。
- 像素審核：第 4 節。
- 原則：`k=0` 可畫核心先過，再逐層加服裝、實景、電影光；每次只改一個槽。

## 1. 鎖定「同一個主角」與第一個測試場景

先選定一張真正要保留的女主參考圖作唯一身份來源。文字只能描述外觀，不能代替實際臉部參考。按現有 Prompt：真實系亞洲女戰士、長直深棕髮、柔和五官、大眼、自然妝；第一輪先用一套簡潔深色戰鬥服，唔好同時換十幾種服裝。

第一個真實場景建議用**寬闊的廢棄工業大廳／舊發電廠**：地面和背景有真實比例、光線有方向、可看清人物全身與泡泡；暫時不要用大量小冰球、密集粒子或過度繁複的室內裝飾。第一輪只有**一個主要透明泡泡**。

固定以下內容直到通過驗收：
- 畫幅 16:9；同一女主參考圖、同一服裝、同一鏡頭及背景。
- 女主位於畫面左下方，巨大泡泡位於右側；女主雙手握住一柄錘。
- 第一版用清楚、厚實、單一手柄的 T 字槌作低複雜度基準；不要在同一條 Prompt 混入十字槌和多向圓頭槌的句子。
- 泡泡保持完整直到 H2；裂紋只在接觸後出現。

## 2. A：先做 T 槌對 T 槌的幾何錨點

在簡單中性背景，先生成一張**只有兩把大型 T 頭槌**的結構參考，不要人物、不要泡泡、不要電影特效。兩把槌只用指定的厚實平端面相對；手柄、槌頭側壁不可搶先接觸。這一步只驗證「哪個端面會碰哪裡」，不追求成片美感。

### 幾何錨點 Prompt

> A clean photorealistic industrial-design reference, 16:9 side-three-quarter view. Two enormous solid-steel T-headed war hammers face each other. Each is one hammer with one handle and one robust T-shaped head. Align only the two designated broad, flat terminal striking faces on one exact contact plane; no cheek, side wall, shaft or handle touches first. Keep both T silhouettes readable, head scale and face thickness consistent, no extra weapons, no people, no bubble, no debris, no text, neutral studio lighting. This is a geometry reference, not poster art.

**先決定接觸點規則再生圖：**目前專案原有契約把目標點鎖在泡泡的六點鐘底極點 (P)。所以兩個 T 頭必須沿著最終那個端面法線對正，接觸位置要代表未來的 (P)。如果把兩把槌簡單地左右水平互撞，之後接觸點自然會落在泡泡的側面，而不是底極點；那會違反舊契約。不要把這兩種擊球方向混成一種。除非你明確決定改規格，第一版先保留六點鐘 (P)。

**A 關通過條件：**T 頭形狀可辨、兩把槌各一柄一頭、只有指定端面接觸，且接觸法線和預定的 (P) 方向一致。失敗就只改槌的朝向／相機，不加人物或場景。

## 3. B：把「目標方 T 頭」局部替換成泡泡

將 A 的已通過圖存成不可覆寫的 `A_anchor.png`。用具遮罩的局部編輯，把**目標方** T 頭替換成一個巨大、完整、透明的肥皂泡／晶玻璃泡；只遮罩目標方，攻擊方 T 槌、手柄、相機及背景盡量原樣保留。把目標 T 頭原先指定的接觸端面對應成泡泡的六點鐘接觸點 (P)。

### B 局部編輯 Prompt

> Edit only the masked target-hammer region. Replace the target T-head with one huge intact transparent iridescent soap-glass sphere. Preserve the attacking T hammer, its selected striking face, handle, perspective, lighting and camera composition. The sphere must remain whole: no cracks, no chips, no shatter, no extra spheres. Register the sphere so the preselected terminal-face contact location becomes its exact six-o'clock bottom pole P. Do not move or redesign anything outside the mask.

**B 關通過條件：**泡泡完整；只有一個泡泡；攻擊方槌及指定端面沒有漂移；接觸位置仍對到泡泡底極點。模型有可能改動未遮罩區域，故不能單憑 Prompt 自稱對準，必須看輸出像素。

## 4. C：產生真實場景的 H0 主畫面

幾何錨點通過後，**不要將中性背景直接當作最終成片**。另外以「女主身份參考圖 + A/B 幾何參考」生成真實場景 H0。使用同一角色參考與場景描述；只讓場景恢復真實材質與光線，不要讓模型重新發明錘型或接觸點。

### H0 可複製 Prompt（未接觸）

> Photorealistic cinematic 16:9 live-action music-video still in a vast abandoned industrial power hall, practical concrete floor, rusted steel structures, believable atmospheric depth and motivated shafts of light. Use the supplied original heroine reference for the same Asian female warrior: long straight dark-brown hair, soft large eyes, natural makeup, focused determined expression. Keep her full body visible in the lower-left area, wearing the established dark combat outfit. She grips ONE enormous solid-steel T-headed hammer with BOTH hands; one handle, one clearly readable T-shaped head, no extra weapon. The hammer's designated broad flat terminal striking face is aimed at the exact six-o'clock bottom pole P of ONE giant intact transparent iridescent bubble on the right. Her body and handle form a dynamic diagonal, not a straight spear through the bubble's center. Leave a visible gap: no contact yet. The bubble has NO cracks. Grounded live-action cinematography, believable scale, real materials, strong but motivated light, film grain, off-center composition. No text, no labels, no extra limbs, no axe, no spikes, no extra bubbles.

H0 的工作只是建立**可用的主場景母版**。第一輪先求人物、槌、泡泡三者都存在且位置正確，再逐步加光暈、碎屑或強烈動作。若加場景後槌消失、變斧或人物變成跟泡泡共舞，退回可畫核心，不要繼續堆形容詞。

## 5. 從同一個 H0 分別產生 H2 和 H3

H0 通過後，另外複製成兩條編輯分支。不要不斷把失敗的上一張全幅 Img2Img 當新底圖疊下去；每張都保留母版與遮罩，並把身份／幾何參考一併提供。

### H2 — 唯一第一次接觸

> Using H0 as the master composition and the approved geometry anchor as a reference, edit only the hammer-face/bubble contact region and the minimum pose area required. The single broad flat terminal striking face makes its first contact at the exact six-o'clock bottom pole P of the bubble. The striking face—not the cheek, shaft or handle—is the only first contact. The bubble was intact immediately before impact; cracks begin only at this contact patch and radiate outward from it. Preserve the heroine's identity, both hands on the handle, the T-head silhouette, camera, set and lighting. No unrelated cracks, no second impact point, no text.

### H3 — 泡殼破裂、人物無傷

> Create the post-impact endpoint from the approved H0 master, using the approved H2 contact location as a reference. The same transparent bubble has now fractured outward from the exact same six-o'clock contact point P; large believable shell fragments fly away from the contact region with physically readable direction and depth. The heroine remains the same person, still holding the same single T-headed hammer; do not redesign her face, weapon, outfit or camera. Any people who were inside the bubble survive, remain visibly uninjured and regain freedom to move and choose. The containment shell breaks; the people are not targets. No blood, no injured residents, no unexplained second fracture origin, no text.

**關鍵：**H2 和 H3 可以參照同一個 H0 母版，但各自獨立編輯；H3 另參照已核准的 H2，只用來鎖定接觸位置與裂源。不要讓生成器重新構圖整張照片。

## 6. 每一關的像素驗收清單

一項不合格就退回對應關，不要用「整體很有氣勢」取代幾何驗收。

- **身份：**與原女主參考圖一致，髮型、臉型及五官沒有漂移。
- **武器：**一柄一頭、T 頭清楚、雙手握柄；沒有變斧、刺球、多柄或多把槌。
- **端面：**指定的厚實平端面先碰；長側壁、槌頭面頰、槌柄都不能先碰。
- **方向：**保留六點鐘 (P) 契約；柄呈動態斜線，不是刺穿泡泡球心的矛。
- **H0：**泡泡完整，槌與泡泡仍有可見空隙，沒有預先裂紋。
- **H2：**只有一個接觸點，位置在泡泡底極點；裂紋由該點起始。
- **H3：**裂源與 H2 相同；泡殼確實碎裂，人物活著、無傷，背景與主角仍連貫。
- **寫實性：**有可信地面接觸、透視比例、光向與碎片深度；不是平面插畫、不是教學示意圖。

只有以上像素檢查都過，才標記 `IMAGE_REALIZATION=PASS` 和 `PIXEL_AUDIT=PASS`。程式上的 `PROMPT_CONTRACT_PASS` 或 SVG 的 `GEOMETRY_PROXY_VALID` 不能代替這兩項。

## 7. 程式只負責把 Prompt 和幾何包整理好

在已 checkout 正確功能分支的工作區，單張試跑可以用：

```bash
mkdir -p out
python3 bubble_break/generate.py --count 1 --seed 20261020 --mode heroine --weapon-topology T --format jsonl --out out/one_story_T.jsonl
python3 bubble_break/frame_pipeline.py --input out/one_story_T.jsonl --outdir out/frame_packet --limit 1
python3 -m unittest discover -s bubble_break -p 'test_*.py'
```

如需產生 A/B/C 幾何代理包，找到 frame packet 裡的 `layout.json`，再執行：

```bash
LAYOUT="$(find out/frame_packet -name layout.json -print -quit)"
test -n "$LAYOUT" || { echo "layout.json not found"; exit 1; }
python3 bubble_break/proxy_edit_pipeline.py --input-layout "$LAYOUT" --outdir out/proxy_T --final-weapon T
```

如果工作區還沒有 `bubble_break/`，先 clone `feat/original-sin-bubble-break-engine` 分支；不要在空目錄直接跑上述腳本。這幾條命令不會生成真實圖片，也不會替你呼叫任何圖片服務。

## 最終交付物

首個可驗收版本不是 1,000 張混合圖，而是同一場景、同一主角的三張圖片：
1. `H0_intact.png`：真實場景、泡泡完整、尚未接觸。
2. `H2_contact.png`：指定端面剛好打中六點鐘 (P)，裂紋從接觸點開始。
3. `H3_shattered.png`：同一泡泡由同一點碎裂，人物無傷。

這三張通過後，才沿用同一個角色參考和幾何契約換六棚、動作、服裝或攝影角度；每輪只改一個變量。
