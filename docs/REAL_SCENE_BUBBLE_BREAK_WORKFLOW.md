# 由 Repo 現有 Prompt 到「真人女主在真實場景擊破泡泡」的逐關流程

> 目的：沿用 `槌2.txt` 的角色鎖定、可畫核心、武器端面和像素審核規則；先驗證單一 T 字槌形狀母版，再驗證 T 槌對 T 槌的終端打擊面互撞矩陣，最後才做各故事的多視角寫實場景，先交付 48 組端面互撞矩陣的獨立 H2 接觸證據，再為每個故事輸出 12 個攝影機角度各自的 H0／H2／H3 三張連貫成圖；每組都要另外做人眼像素審核。
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
- 第一版以清楚、厚實、單一手柄的 T 字槌作形狀基準。槌頭的 T 橫杠在物件自身座標中保持平直；為讓指定終端面命中 P，允許整把剛體槌在 3D／鏡頭畫面中側轉，絕不允許槌頭相對柄彎折。不要混入十字槌和多向圓頭槌的描述。
- 泡泡保持完整直到 H2；裂紋只在接觸後出現。

## 2. A：先建立唯一一把 T 槌形狀母版

第一關仍然只驗證武器自身拓撲：一條剛直矩形橫杠、一條接在規定中點的長柄、完整可見的單一 T 槌。這張參考只鎖武器結構，不能當成電影構圖，也不能代替接觸面驗證。

### T 槌母版 Prompt

> Create ONE photorealistic 16:9 product-reference image of exactly ONE T-headed hammer on a neutral studio background. Show the complete weapon. Its crossbar is one straight rigid rectangular head with equal left/right ends, and one long handle attaches at the defined central underside joint. The hammer is one connected rigid object. No second hammer, no bubble, no heroine, no city, no debris, no text or extra post. This is a weapon-topology reference only, not a scene composition.

把真正產出的圖片存成 `A_T_weapon_master.png`，由人類確認橫杠、柄的接點和完整結構後建立 `A_T_weapon_master_review.json`。Prompt／SVG 只證明資料包內容正確，不能證明外部模型畫對。

## 3. B：真正驗證 T 槌對 T 槌的打擊面互撞

這一關是先前漏掉的關鍵。不是把兩把槌的上下寬面疊住，也不是只把兩個 T 外形放到同一畫面，更不是讓一把槌頭的 cheek（長側壁）、角或柄先碰到另一把。**必須是 T 槌 A 的指定終端打擊面，正面撞上 T 槌 B 的指定終端打擊面。**

定義固定如下：

- **Active face A / B：**兩把槌的橫杠端部各自選中的平坦 `TERMINAL END STRIKING FACE`。
- **H2 接觸：**兩個端面平面重合、接觸中心都是同一個 P，兩個面法線沿碰撞軸反向；不可留縫，也不可穿模。
- **失敗接觸：**cheek／長側壁先碰、橫杠上／下寬面先碰、角先碰、柄先碰、兩個槌頭只是靠近卻沒有實際端面互撞。
- **形狀：**兩把槌必須仍是兩把分開的 T 槌，各自有一個頭與一條柄。在某些側視角，整體接合輪廓可能像 H 對 H；那只是兩把槌的投影，不可把兩把槌合併成一件 H 形武器。

### 不是只做一張：48 組碰撞矩陣

`bubble_break/t_contact_matrix.py` 將測試組合成 **12 個鏡頭角度 × 4 個碰撞軸向 = 48 個變體**。四種柄向關係在這 48 組內以確定性輪轉均衡分配（每種 12 組）；這是可追溯的分層矩陣，不是把鏡頭、碰撞軸、柄向全部做成 12 × 4 × 4 的 192 組全交叉。每個變體各自輸出 H0、H2、H3 三張獨立圖片提示，總共 **144 個單圖 Prompt**：

- 鏡頭：正看接觸面、側面、正／反三分之四、低角度、高斜角、Dutch roll、接觸微距、過肩、長焦、全景等。
- 碰撞軸：水平、垂直、左下至右上的對角、前後景深方向。
- H0：兩個端面在同一碰撞軸上對正，保留清楚空隙。
- H2：兩個 `TERMINAL END STRIKING FACE` 真正面對面接觸，接觸中心和反向法線清晰可辨。
- H3：同一對端面沿相同碰撞軸輕微回彈，兩把槌仍然是剛體。

每列 JSONL 是**一張獨立圖片**，不可要求模型把 3 張做成拼貼或 contact sheet。輸出中的 `image_realization=NOT_RUN` 只代表 Prompt 已建立；必須生成 48 張真正的 H2 接觸圖，逐張人工審核其端面平面與接觸位置後，矩陣才可標記 PASS。48 組的測試圖不可用 SVG 示意圖、T 輪廓表或文字聲稱替代。

## 4. C：產生真實場景的 H0 主畫面

幾何錨點通過後，**不要將中性背景直接當作最終成片**。另外以「女主身份參考圖 + A/B 幾何參考」生成真實場景 H0。使用同一角色參考與場景描述；只讓場景恢復真實材質與光線，不要讓模型重新發明錘型或接觸點。

### H0 可複製 Prompt（未接觸）

> Photorealistic cinematic 16:9 live-action music-video still in a vast abandoned industrial power hall, practical concrete floor, rusted steel structures, believable atmospheric depth and motivated shafts of light. Use the supplied original heroine reference for the same Asian female warrior: long straight dark-brown hair, soft large eyes, natural makeup, focused determined expression. Keep her full body visible in the lower-left area, wearing the established dark combat outfit. She grips ONE enormous solid-steel T-headed hammer with BOTH hands; one handle, one clearly readable T-shaped head, no extra weapon. The hammer's designated broad flat terminal striking face is aimed at the exact six-o'clock bottom pole P of ONE giant intact transparent iridescent bubble on the right. For the canonical bottom-pole view, the terminal-face normal points upward on screen, so the complete T rotates as one rigid body: the crossbar projects vertically and the centered handle projects laterally through the crossbar midpoint. Position her hands and body to follow that handle axis; do not keep the crossbar vertical while drawing the handle diagonally down-left. An oblique camera may make both axes oblique only through one coherent 3D transform, never by bending or independently rotating the head and handle. Leave a visible gap: no contact yet. The bubble has NO cracks. Grounded live-action cinematography, believable scale, real materials, strong but motivated light, film grain, off-center composition. No text, no labels, no extra limbs, no axe, no spikes, no extra bubbles.

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
- **方向：**保留六點鐘 (P) 契約；柄的投影方向由整把剛體槌的姿態與攝影機決定，不固定為左下斜線。底點法線在畫面向上時，標準正投影下柄應橫向伸出；斜角必須來自一致的 3D 姿態，不可將柄單獨扭斜。
- **H0：**泡泡完整，槌與泡泡仍有可見空隙，沒有預先裂紋。
- **H2：**只有一個接觸點，位置在泡泡底極點；裂紋由該點起始。
- **H3：**裂源與 H2 相同；泡殼確實碎裂，人物活著、無傷，背景與主角仍連貫。
- **寫實性：**有可信地面接觸、透視比例、光向與碎片深度；不是平面插畫、不是教學示意圖。

只有實際圖片逐張通過像素檢查，才標記 `IMAGE_REALIZATION=PASS` 和 `PIXEL_AUDIT=PASS`。48 組 T-to-T 接觸矩陣須先通過，再做 12 視角電影場景 sweep。程式上的 `PROMPT_CONTRACT_PASS` 或 SVG 的 `GEOMETRY_PROXY_VALID` 不能代替這兩項。

## 6.5 防止 T 字槌被扭成球頭、十字或歪頭

這個 repo 的既有故事板主參考圖顯示的是 `WEAPON_C_RADIAL_SPHERE` 多向扁平面球頭，**不是 T 字槌**。如果把那些圖當成 T 版本的 image reference，視覺參考會和文字互相打架；模型通常更容易照著圖中的球頭複製。所以測 T 形時，不要把原球頭故事板當成武器形狀參考。人物臉參考仍可單獨使用。

T 的結構只定義為以下三件事：

1. **一條直的水平矩形橫杠**，左右兩端對稱、等長等厚；橫杠寬度約為厚度的 3.8 倍。
2. **唯一一條長柄直接接在橫杠底面正中央**；這條長柄本身就是 T 的主幹。不得再加一截短柱、第二柄、球頭、X 臂或多餘橫杠。
3. **打擊面固定為橫杠端部的終端平面**：T-to-T 碰撞關卡必須由槌 A 的 `TERMINAL END STRIKING FACE` 正面接觸槌 B 的 `TERMINAL END STRIKING FACE`；兩個面平面重合、法線相反。禁止把橫杠上／下寬面、長側壁（cheek）、角或柄誤認為打擊面。後續泡泡場景沿用同一個指定端面去接觸 P，不可又改回寬上平面。

最重要的不是再堆負面詞，而是用形狀參考 + 局部遮罩控制結構：
- `proxy_edit_pipeline.py --final-weapon T` 會在輸出包中另外產生 `05_T_silhouette_reference.svg`。這是無文字、無球泡、無角色的純 T 輪廓參考。若圖片編輯器不收 SVG，先將它轉成 PNG，再把它當作**武器形狀參考**；不要用它替代場景母版。
- `04_final_weapon_preview.svg` 用來看武器放回指定場景位置後的幾何；`03_attacker_edit_mask.svg` 是從原十字代理改形時用的遮罩。
- 生成／編輯時，場景母版控制人物與相機；`05_T_silhouette_reference` 控制 T 橫杠和柄的拓撲；只遮罩武器區域做局部編輯。不要每次全圖重畫。
- 任一關只要橫杠彎曲／斜轉、柄離開橫杠中點、出現額外短柱、頭部變圓球或加號，就標記形狀失敗，回到武器遮罩重編；不要靠「more powerful」等風格詞補救。

## 6.6 為什麼舊版的固定 T 對 T 圖仍然不合格

問題不是「不應做 T 對 T」；恰好相反，T 對 T 的端面互撞是必需的。舊版把這項必要驗證收窄成一張上下合軸的固定示意圖，而且未證明實際生成像素中兩個指定端面真的相碰。它沒有測不同角度、不同碰撞軸，也沒有排除 cheek／角／柄先碰，所以不能證明模型懂得「哪個平面先接觸」。

正確順序是：

1. 一張真實的單一 T 槌母版，鎖定槌的結構。
2. 48 組 T 槌對 T 槌的 END-FACE-to-END-FACE 碰撞變體；每組 H0/H2/H3，共 144 個單圖 Prompt。人工審核 48 張實際 H2 圖。
3. 只有接觸面矩陣通過後，才做泡泡場景；最終場景每個故事再以 12 個攝影機角度分別產生 H0/H2/H3，每個故事是 36 個單圖 Prompt。

新版程式輸出：
- `00_T_weapon_master_geometry.svg`／`00_generate_T_weapon_master.txt`：單一武器結構參考。
- `t_contact_matrix.jsonl`／`contact_matrix_manifest.json`：12 角度 × 4 碰撞軸的 48 組端面互撞矩陣。
- `_shared_T_weapon_master/`：跨故事共用的武器母版和接觸矩陣；不重複產相同的槌形測試。
- 每個故事的 `frames/`：12 個 camera-view 子目錄，各自包含一組 H0/H2/H3。
- `generate_scene_with_T_master.txt`：規定母版只控制槌形；接觸面由通過審核的矩陣定義；每個故事的場景和鏡頭按自己的 Prompt 變化。

**CI 只能驗證這些 Prompt、JSONL、閘門和資料包的結構。** 沒有實際產生並人工審核的 48 張 H2 碰撞圖，以及後續的場景圖，就不能聲稱模型已理解端面接觸或場景畫面已通過像素驗收。

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
1. 48 組 T 槌對 T 槌端面互撞矩陣的真實 H2 接觸圖先逐張通過人工審核；每組同時保留 H0/H2/H3 三個單圖 Prompt。
2. 每個故事再輸出 12 個視角 × H0/H2/H3，共 36 張獨立場景圖 Prompt；每一個視角內人物、泡泡與接觸軸保持連貫。
3. 泡泡 H2 的真實像素需證明指定 END FACE 命中六點鐘底極點 P，裂紋從該接觸中心開始；H3 沿同一接觸軸破裂，女主和居民無傷。

這三張通過後，才沿用同一個角色參考和幾何契約換六棚、動作、服裝或攝影角度；每輪只改一個變量。
