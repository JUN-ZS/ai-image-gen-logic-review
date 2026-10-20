# 由 Repo 現有 Prompt 到「真人女主在真實場景擊破泡泡」的逐關流程

> 目的：沿用 `槌2.txt` 的角色鎖定、可畫核心、武器端面和像素審核規則；先驗證單一 T 字槌的形狀母版，再做各故事的寫實場景，最後交付 H0（未碰）、H2（首次碰撞）、H3（泡殼爆裂）三張相互連貫的完成圖。
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
- 畫幅 16:9；同一故事的 H0/H2/H3 共用女主、服裝、鏡頭及背景；不同故事保留各自的環境、規模、泡殼、色彩與因果隱喻變化。
- 女主位於畫面左下方，巨大泡泡位於右側；女主雙手握住一柄錘。
- 第一版用清楚、厚實、單一手柄的 T 字槌作低複雜度基準；不要在同一條 Prompt 混入十字槌和多向圓頭槌的句子。
- 泡泡保持完整直到 H2；裂紋只在接觸後出現。

## 2. A：先建立唯一一把 T 槌形狀母版

第一關只驗證**武器拓撲**，不是兩把槌互撞，也不是最終電影構圖。只生成一把完整 T 字槌：一條直的水平矩形橫杠；一條長柄直接接在橫杠底面正中央。長柄本身就是 T 的主幹，不能多一截短柱。整把武器必須在畫面內完整可見。

### T 槌母版 Prompt

> Create ONE photorealistic 16:9 product-reference image of exactly ONE T-headed hammer on a neutral studio background. Show the complete weapon. Its head is one straight rigid horizontal rectangular crossbar with equal left/right ends. Exactly one long handle attaches directly to the exact underside midpoint of that crossbar; the handle itself forms the only stem of the capital T. Use a level near-front view so the crossbar stays straight and horizontal. No second hammer, no inverted T, no bubble, no heroine, no city, no debris, no text, no extra shaft or short post. This is a weapon-shape reference only, not the composition for later cinematic scenes.

**A 關通過條件：**只有一把槌；橫杠平直、水平、左右端對稱；長柄與橫杠底面中點直接相連；全柄完整可見。把真正產出的圖片存成 A_T_weapon_master.png，再由人類檢查並建立 A_T_weapon_master_review.json。Prompt 和 SVG 只能驗證程式契約，不能代替實際圖片審核。

## 3. B：共用同一把 T 槌，生成有變化的故事場景

整個批次只需一張通過審核的武器母版，放在 _shared_T_weapon_master/，不要每個 story 都重新產一張一模一樣的母版。每個故事繼續使用自己那組 H0/H2/H3 Prompt：母版只控制槌子的形狀，**不控制場景、人物姿勢、背景、光線或構圖**。

- H0：同一把 T 槌尚未碰到泡泡，槌面與泡膜之間保留明顯空隙。
- H2：同一把 T 槌的指定上平面首次接觸泡泡底部 P，裂紋只從該處開始。
- H3：同一泡泡從同一個 P 破裂，槌仍然是同一把 T 槌，人物與泡內居民無傷。

每一張圖分開生成；不要把 H0/H2/H3 做成拼貼。不同 story ID 要保留各自的場景、泡泡規模、泡殼、色彩、象徵和故事因果；同一 story 的三幀才鎖定連貫性。**絕不能再畫上方倒置 T 來充當泡泡，也不能做「先兩把 T 對接，再把其中一把換成泡泡」這個錯誤步驟。**

Stage B 使用 generate_scene_with_T_master.txt，並同時提供該故事的 H0/H2/H3 prompt 檔。場景生成完成後，才逐張進行真實像素審核。

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

## 6.5 防止 T 字槌被扭成球頭、十字或歪頭

這個 repo 的既有故事板主參考圖顯示的是 `WEAPON_C_RADIAL_SPHERE` 多向扁平面球頭，**不是 T 字槌**。如果把那些圖當成 T 版本的 image reference，視覺參考會和文字互相打架；模型通常更容易照著圖中的球頭複製。所以測 T 形時，不要把原球頭故事板當成武器形狀參考。人物臉參考仍可單獨使用。

T 的結構只定義為以下三件事：

1. **一條直的水平矩形橫杠**，左右兩端對稱、等長等厚；橫杠寬度約為厚度的 3.8 倍。
2. **唯一一條長柄直接接在橫杠底面正中央**；這條長柄本身就是 T 的主幹。不得再加一截短柱、第二柄、球頭、X 臂或多餘橫杠。
3. **打擊面另行定義**：本 T 方案使用橫杠的寬扁平上平面接觸泡泡底點 P；不要同時把它叫成「槌頭末端面」再要求模型用側端面。對 T 版，幾何用語固定為 `broad upper plane of the horizontal crossbar`。

最重要的不是再堆負面詞，而是用形狀參考 + 局部遮罩控制結構：
- `proxy_edit_pipeline.py --final-weapon T` 會在輸出包中另外產生 `05_T_silhouette_reference.svg`。這是無文字、無球泡、無角色的純 T 輪廓參考。若圖片編輯器不收 SVG，先將它轉成 PNG，再把它當作**武器形狀參考**；不要用它替代場景母版。
- `04_final_weapon_preview.svg` 用來看武器放回指定場景位置後的幾何；`03_attacker_edit_mask.svg` 是從原十字代理改形時用的遮罩。
- 生成／編輯時，場景母版控制人物與相機；`05_T_silhouette_reference` 控制 T 橫杠和柄的拓撲；只遮罩武器區域做局部編輯。不要每次全圖重畫。
- 任一關只要橫杠彎曲／斜轉、柄離開橫杠中點、出現額外短柱、頭部變圓球或加號，就標記形狀失敗，回到武器遮罩重編；不要靠「more powerful」等風格詞補救。

## 6.6 為什麼「T 對 T」不是正確的首關

上一版把「T 字槌不能走形」誤解成「必須先畫兩把 T 槌上下合軸」。程式因而將上方倒置 T 當成泡泡的替身，並用舊的兩把槌閘門將整批停在同一種上下合軸構圖。這不但多造出一把錯誤目標物，也令批次無法展示各故事的實際場景變化。正確流程應是「單一武器母版 → 故事場景變化」。

新 T 路徑會產生：
- 00_T_weapon_master_geometry.svg：只有一把 T 字槌的向量形狀參考。
- 00_generate_T_weapon_master.txt：生成唯一 T 槌母版的 Prompt。
- _shared_T_weapon_master/：批次共用一份母版 Prompt、形狀參考與審核閘門；不再讓每個故事各產一張重複的 T 母版。
- generate_scene_with_T_master.txt：告訴模型將母版只用作槌形參考，並依各故事 prompt 生成 H0/H2/H3。
- stage_gate.json：在實際母版經人工審核前維持 BLOCKED_UNTIL_T_WEAPON_MASTER_APPROVED。

人工審核後建立 _shared_T_weapon_master/A_T_weapon_master_review.json。這是人工記錄，不是自動認證。CI 綠燈只代表 Prompt／資料包規格一致；沒有真正的 A_T_weapon_master.png、人工審核紀錄和 H0/H2/H3 真實圖片時，不能宣稱圖片生成或像素審核 PASS。

對 H2 的接觸位置，仍須在實際出圖中檢查泡泡六點鐘底極點與槌頭接觸區。向量座標 P=(1090,610) 只定義 1920×1080 代理畫布，不是外部生成圖片已符合的證據。

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
