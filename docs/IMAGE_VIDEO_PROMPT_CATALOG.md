# IMAGE／VIDEO 半公式＋完整 PROMPT 總庫

## 怎樣用這份總庫

這份文件把 repo 中互不相同的生成方法整理成**可直接複製的自然語言 Prompt**。每個方法都有簡短「半公式」供人理解，再附完整英文 Prompt 給 IMAGE 或 VIDEO 模型。半公式是人類編排提示的摘要，不要求模型解讀機器欄位、向量方程或 JSON。

**重要：不同拓撲分開使用。** 一次只選以下一種物件方法：側柄種植圓柱、外端接柄圓柱、T 槌、雙 T 槌、厚十字圓端蓋雙槌、線形棒、或多向扁平面圓頭。不要把它們合併成同一把武器。

建議每次完整 Prompt 依序包括：
- **畫面目標：**要生成一張乾淨的圖、一條影片，或一個單獨關鍵幀。
- **主體與場景：**女主、泡泡、真實場景、畫面構圖。
- **武器結構：**只描述當前方法的幾何。
- **動作與接觸：**接觸前、第一次接觸、後續破裂的差異。
- **鏡頭與美術：**選一種相機角度和一種風格，不讓美術覆蓋幾何。
- **負面約束：**明確禁止最常見的錯誤。

若需要保持同一主角，請附上已核准的人物參考圖；若要連續影片，請附上通過審查的母圖／關鍵幀。文字無法替代參考圖。所有幾何用語仍需由生成後的實際畫面驗證。

---

# PART I — IMAGE PROMPTS

## I-00｜通用電影圖像底稿

**用途：**建立場景和人物基本畫面。這不是武器接觸驗收圖；先確認構圖，再選用下方其中一個武器專用 Prompt。

**半公式：** 16:9 單張圖 + 固定女主 + 一個透明球體 + 一種武器 + 指定接觸區 + 可讀構圖 + 克制特效。

~~~text
Create one single full-resolution photorealistic cinematic 16:9 image, not a collage or storyboard sheet.

Show the same adult East Asian female warrior from the supplied character reference, with long straight dark-brown hair, natural makeup, expressive eyes, and a fitted matte-black combat outfit with restrained metallic details. Preserve her facial identity, body proportions and outfit design from the reference.

Place the heroine on the left third of a vast abandoned industrial hall with believable scale, dark basalt and steel structures, a few readable distant landmarks, and a motivated cinematic key light. Place one large translucent crystal-glass sphere on the right side. Keep the heroine, her hands, the entire weapon, the weapon-to-target region, and the sphere boundary all visible in the same frame.

Use one physically coherent action and one clearly readable camera position. Use controlled volumetric light, realistic glass refraction, restrained bloom, subtle film grain and an emotionally rich cinematic grade. The contact area must remain visible and must not be hidden by sparks, haze, flares or debris.

Do not invent a second weapon, extra hands, extra fingers, extra limbs, a new handle, a different character face, text, logos, watermarks, interface overlays or panel borders. Keep the image free of labels and typography; any teaching labels will be added separately after generation.
~~~

## I-01｜T 槌形狀母版：只驗武器，不打泡

**用途：**先鎖定一把標準 T 槌，避免模型在場景裡把它畫成斧、長矛或普通大槌。

**半公式：** 單把 T 槌 + 一條直柄 + 橫頭中央接柄 + 中性背景 + 完整輪廓。

~~~text
Create one single photorealistic 16:9 product-reference image of exactly one complete T-headed hammer on a neutral studio background. Show the entire weapon from end to end, with clear negative space around it.

The hammer has one straight rigid rectangular crossbar with equal left and right ends. One long straight handle is attached at the defined midpoint joint on the underside of the crossbar. The crossbar and handle form one rigid connected T-shaped object. Both terminal end faces and both long sidewalls of the crossbar are clearly distinguishable. The handle is perpendicular to the crossbar's long axis.

Use a three-quarter product view that reveals the crossbar thickness, both ends, the central handle joint and the full handle length. Realistic dark steel, small bevels and restrained material detail; no fantasy spikes or decorative structures that change the silhouette.

No person, no hands, no sphere, no second hammer, no axe blade, no cross-shaped plus-sign head, no radial multi-face head, no additional shaft, no detached pieces, no bend, no text or labels. This image is only a clean weapon-topology reference.
~~~

## I-02｜T 槌打泡泡 H0：有明確空隙

**用途：**第一張接觸前母圖。不能先裂、不能先發光，亦不可讓柄像長矛指向球心。

**半公式：** 女主＋單把剛性 T 槌 + 指定端面已對準 + 球面前正空隙 + 完整泡泡。

~~~text
Create one full-frame photorealistic cinematic 16:9 still using the supplied approved heroine reference and the approved T-hammer weapon reference.

The heroine stands on the left side, gripping the same T-hammer with both hands. The hammer has one rigid straight rectangular crossbar and one straight handle fixed at its midpoint. The handle remains perpendicular to the head axis; the head and handle never bend or rotate independently.

One large translucent crystal sphere occupies the right side. The hammer's designated flat terminal striking face is already oriented toward the sphere and is clearly separated from the sphere surface by a wide visible air gap. The face-to-sphere approach direction is readable, but the weapon is not touching the sphere. Keep the handle visibly angled relative to the line from the heroine's torso through the sphere centre; do not make the weapon look like a spear aimed through the centre.

The sphere is pristine and intact. No cracks, contact glow, sparks, dents, debris or impact shadow. Show the complete hammer, head-handle joint, both hands, the air gap and the sphere surface. Cinematic live-action photography, believable anatomy, motivated light, realistic metal and glass, restrained bloom, 16:9 widescreen.

No axe, no cross hammer, no radial hammer, no cheek-first contact, no corner-first contact, no handle-first contact, no missing weapon, no extra shaft, no bent head, no sphere damage before contact, no text or watermark.
~~~

## I-03｜T 槌打泡泡 H1：接近但仍未碰到

**用途：**以通過的 H0 圖做 image-to-image／局部編輯，只把槌整體沿原接近路徑推近。這不是重畫整個場景。

**半公式：** H0 母圖 + 剛體槌沿原路徑前移 + 空隙縮小但仍大於零 + 其他元素凍結。

~~~text
Use the supplied accepted H0 image as the strict visual parent. Create one new full-frame 16:9 image of the same instant in the same scene, preserving the heroine's identity, facial features, outfit, hands, body proportions, hammer design, head-handle joint, sphere centre and radius, background landmarks, lighting direction and camera framing.

Change only the rigid hammer's position along its already established final approach path so its designated terminal striking face is closer to the sphere than in H0, while a clearly visible positive air gap still remains. Move the complete hammer as one rigid object. Do not rotate the head independently, change the handle axis, rescale the weapon or move the sphere.

The sphere remains pristine and intact. There is no contact yet, so there must be no contact glow, crack, spark, debris, dent or impact shadow. Keep the gap visibly measurable in the picture and keep the active face and sphere surface separately readable.

Do not redesign the scene, switch the weapon to an axe or spear, invent an axial handle, bend the hammer, hide the gap with bloom, move the heroine to a new position, or create any cracks before the H2 contact state. No text, labels, panel borders or watermark.
~~~

## I-04｜T 槌打泡泡 H2：指定端面第一次接觸

**用途：**核心接觸驗收圖。目標是接觸面正確，不是爆炸得漂亮。

**半公式：** H1 母圖 + 指定端平面碰 P + 零空隙但不穿模 + 第一條裂只從 P 開始。

~~~text
Use the supplied accepted H1 image as the strict visual parent. Create one single photorealistic cinematic 16:9 first-contact frame. Preserve the same heroine, face, outfit, body pose, rigid T-hammer topology, straight handle, head-handle joint, sphere geometry, camera, scene landmarks and light direction.

The designated flat terminal end striking face of the hammer is now the first and only weapon surface touching the sphere, at one clearly visible point P on the shell. The face-to-sphere gap is exactly closed with no visible air gap and no interpenetration. The striking-face normal and the sphere's outward surface normal oppose one another at P.

The broad crossbar cheek, long upper and lower sidewalls, corners, central handle joint and handle must remain clear of the sphere. Do not use a camera trick to make a sidewall look like an end-face hit. The hammer remains a rigid object; the crossbar and handle do not bend.

Show only a restrained first-contact glow at P and the first fine micro-cracks beginning at that exact point. Do not jump directly to a full explosion. Keep the contact seam, face perimeter, handle joint and sphere curvature inspectable. The inner sanctuary and any inhabitants inside the sphere remain untouched and safe.

No gap at contact, no penetration, no cheek-first collision, no corner-first collision, no handle-first collision, no detached head, no newly invented shaft, no random crack origin, no pre-existing cracks, no effect bloom hiding P, no text or watermark.
~~~

## I-05｜T 槌打泡泡 H3：同一軸跟進

**用途：**以通過的 H2 為母圖，做接觸後跟進，不重新設計整把槌。

**半公式：** H2 母圖 + 同一剛體沿同一軸小幅前進 + 裂紋從 P 擴散 + 外殼碎片向外。

~~~text
Use the supplied accepted H2 contact image as the strict parent. Create one single photorealistic cinematic 16:9 immediate follow-through frame. Preserve the heroine's identity, the weapon topology, head-handle connection, grip, sphere centre and radius, contact anchor P, background landmarks, camera and lighting.

The same rigid hammer has advanced a small, clearly motivated distance along the same collision path after the terminal end face first contacted the sphere at P. Do not rotate the hammer head independently or change the angle between head and handle. The active face remains aligned with the established contact direction.

Fine cracks propagate outward from the same P across the outer glass shell. The first controlled shock ripple and a small number of shell fragments move outward from the fracture region. The cracks must not originate at the handle, a random sphere location or the opposite side. The protected inner sanctuary and its inhabitants remain intact.

Keep the active face, contact point, hands, handle joint and fracture direction readable. Do not allow bloom or debris to obscure the actual contact geometry. No new weapon, no bend, no extra shaft, no random crack pattern, no early full-scene explosion, no resident injury, no text or watermark.
~~~

## I-06｜雙 T 槌端面對端面：幾何證明圖

**用途：**兩把獨立 T 槌真正互撞。不可把兩把武器合併成一個 H 形武器，也不可用槌腰互撞。

**半公式：** 兩把完整剛性 T 槌 + 指定端面平面重合 + 法線相反 + 同一接觸點 P + 兩柄均清楚可見。

~~~text
Create one full-frame photorealistic 16:9 geometry-proof image of exactly two separate, complete T-headed hammers facing one another.

Each hammer has its own straight rigid rectangular crossbar, its own central perpendicular handle joint, and one long straight handle. The two tools remain separate rigid objects; never merge them into a single H-shaped weapon. The two crossbars remain straight and each handle stays attached at its own defined midpoint joint.

At the instant of contact, only the selected terminal end striking face of hammer A touches the selected terminal end striking face of hammer B. The two flat end-face planes meet at one shared point P, and their outward normals point in opposite directions along the declared collision axis. The broad sidewalls, upper and lower cheeks, corners, center joints and handles remain clear of one another.

Show both end-face boundaries, both complete head profiles and both handles so the contact identity can be reviewed. Use a slightly grazing three-quarter camera rather than a perfectly head-on view that hides the seam. Tiny sparks may accent the contact but must not cover it. Realistic heavy steel and cinematic light; no montage, no panels, no labels.

No cheek-to-cheek contact, no sidewall-first hit, no corner-first hit, no handle-first hit, no hovering gap, no interpenetration, no bent crossbars, no independently rotating heads, no fused H-shaped tool, no extra hammer, no text or watermark.
~~~

## I-07｜雙 T 槌 H0：兩個端面尚有空隙

**用途：**與 I-06 配對，先證明兩端面在同一軸上對正，再生成真正 H2 接觸圖。

~~~text
Create one photorealistic full-frame 16:9 image of two separate complete T-hammers aligned for terminal-face-to-terminal-face contact. Each has one straight rigid rectangular crossbar and one straight handle attached at its own midpoint joint at a right angle.

The selected flat terminal end face of hammer A directly faces the selected flat terminal end face of hammer B along one shared collision axis. Leave a clearly visible positive air gap between the two circularly or rectangularly bounded flat contact planes, depending on the approved hammer reference. Both faces are aligned as if they will meet next, but there is no contact yet.

Both weapons must remain full, separate T-hammers. Show both crossbar cheeks, both selected end-face outlines and both handles. Place the camera slightly off the collision normal so the gap is easy to inspect. No sparks, dents, cracks, overlap or contact shadow.

No sidewall-first alignment, no crossed broad cheeks, no center-joint collision, no handle collision, no fused H-shaped object, no changed weapon topology, no text or watermark.
~~~

## I-08｜厚十字／CYLINDER_CROSS 雙槌：圓端蓋面對面

**用途：**與 T 槌不同的拓撲。每一把頭部是厚實的 plus-sign 十字，末端有圓柱端蓋；不是兩把 T 槌。

~~~text
Create one full-frame photorealistic 16:9 geometry-proof image showing exactly two independent, complete, thick plus-sign cross hammers.

Each hammer has a massive clean orthogonal plus-shaped head made from one thick vertical rectangular arm and one thick horizontal rectangular arm crossing at the centre. Each arm terminates in a solid cylindrical end piece with a flat circular outer end cap. Each complete hammer has one long straight rigid handle attached at its own centre joint. Preserve both the horizontal and vertical arms; neither head may become a T, X, axe or single-bar hammer.

At the first-contact instant, the selected flat circular outer end cap of hammer A meets the selected flat circular outer end cap of hammer B. The two circular cap planes coincide at a single contact centre P and their outward normals oppose one another along the collision axis. The curved cylinder barrels, broad crossbar sides, vertical arms, corners, centre joints and handles must not touch first.

Keep both handles and both complete heads visible. Use a slight grazing camera angle that reveals the circular cap rims and actual seam. Realistic heavy steel, controlled sparks, no effect that hides the seam.

No curved barrel-to-barrel contact, no broad-side contact, no corner-first collision, no handle-first collision, no missing cross arm, no thin plus-sign, no fused H-shaped object, no extra weapons, no collage, no text or watermark.
~~~

## I-09｜厚十字雙槌稠密候選 Atlas

**用途：**在單張圖中找幾何候選；這是候選地圖，不可當成每組獨立接觸已通過。正式接觸證據必須把選中的候選逐張重生成。

~~~text
Create one clean full-resolution 16:9 candidate-atlas image showing multiple clearly separated pairs of thick plus-sign cross hammers in distinct small test areas spread across one neutral dark studio space. Each pair is an independent geometry candidate, not a single giant weapon. Keep enough negative space between pairs so each candidate can be selected individually.

Every hammer must have a thick orthogonal plus-sign head with four solid arms, cylindrical end pieces with flat circular outer caps, one rigid centre joint and one straight handle. In each pair, nominate one outer cap on each hammer as the intended active face; arrange the pair toward face-to-face contact with opposing cap directions. Vary candidate collision axes and rigid-body roll so the handles have visibly different projected orientations. Do not simply mirror-copy the same pair.

Use a wide view with every candidate pair fully inside frame and no overlap between candidate areas. Do not add any heroine or sphere. Keep the image a candidate atlas, not a decorative poster. Avoid labels that overlap the tools; if the model cannot keep every pair separately readable, show fewer candidates rather than merging them.

No T-hammer head, no X-head, no fused H-shaped weapon, no curved barrel-first contact, no handle-first contact, no hidden joints, no repeated identical poses, no panel borders, no fake pass/fail text, no watermark.
~~~

## I-10｜線形擊打棒：正控制 90° 交叉、平面互撞

**用途：**另一條不是槌的幾何路線。棒軸為 90°；撞擊小平面彼此平行且相對，這兩個條件不能混為一談。

~~~text
Create one photorealistic cinematic 16:9 image showing two adult fighters, one airborne and one grounded in a low stable stance, meeting with thin rigid line-shaped striking rods.

Do not render hammers. Each fighter holds one long, straight, very thin rigid rod with a small, visible planar impact facet integrated into the rod tip. The facet is only slightly wider than the rod, never a bulky hammer head. Keep each rod straight, with the full length and each grip visible.

At the impact instant, the two rod centre lines cross at a right angle. Their small planar impact facets are parallel and face one another, with opposing face normals, making real face-to-face contact at the shared crossing point. Keep the rod-axis right angle and the opposing contact faces visually legible. The airborne fighter uses a diving or overhead action; the grounded fighter has a distinct crouching or kneeling action, not a mirrored copy.

Use a three-quarter audit camera, keep the contact seam unobstructed, and use small restrained sparks only. Realistic cinematic photography and believable anatomy.

No T-head, no plus-sign hammer, no bulky hammer head, no coaxial end-to-end rods, no fake crossing caused only by perspective, no gap between contact facets, no bent rods, no contact with either fighter's body, no text or watermark.
~~~

## I-11｜線形擊打棒：反向面負控制

**用途：**刻意生成指定幾何錯誤，供比較及教學；結果必須視為預期失敗，絕不可併入正控制通過數量。

~~~text
Create one photorealistic cinematic 16:9 negative-control image using the same two fighters, same scene, same straight thin rods, same camera and same action family as the supplied positive-control reference.

The rods still cross at a right angle, but intentionally rotate one small planar impact facet away from the required face-to-face orientation. The two designated facets visibly fail to oppose one another, so the intended correct planar-face collision is not achieved. Make this a clear deliberate inverse-face example, not an ambiguous camera-hidden miss. Preserve both straight rods and the small facets; do not make a hammer head appear.

Keep all unrelated visual elements comparable to the positive-control reference so the wrong facet orientation is the main visible difference. Do not add decorative sparks that could falsely imply a valid collision.

This is an expected-fail negative control for teaching geometry. It must not be presented as a correct technique or a passing sample. No T-hammer, no plus-sign head, no coaxial rod contact, no unrelated scene redesign, no labels, no text or watermark.
~~~

## I-12｜T 槌正確接觸 vs 刻意錯面：雙人對照畫面

**用途：**一張圖同時展示正控制與預期失敗的負控制，但必須清楚分區、不是將兩種規則混在同一把槌上。

~~~text
Create one photorealistic cinematic 16:9 teaching-comparison image in one coherent sphere scene with two clearly separated impact demonstrations at two different sphere locations.

On the left, an airborne adult fighter performs the correct positive-control strike with a rigid T-hammer. Its designated terminal end face meets the sphere first at point P; the face normal opposes the local sphere normal, and no cheek, corner or handle touches.

On the right, a different grounded adult fighter performs a deliberate negative-control strike at a separate point Q. The T-hammer broad cheek/sidewall is intentionally the first-contact surface, while its terminal end face is visibly not the contacting surface. This right-side example is intentionally wrong and must read as a negative control, not an alternative valid technique.

Keep the two T-hammers separate, straight and complete. The two contact locations P and Q must be spatially distinct and individually visible. Use different body actions—airborne diagonal dive on the left, deep low stance on the right—rather than mirrored copies. Keep the scene and camera coherent, with enough space to compare both impact surfaces.

Do not blend the rules, do not label the negative control as a pass, do not let sparks hide either contact patch, and do not fuse the weapons. No extra weapons, text, watermark or fake interface graphics.
~~~

## I-13｜雙頭短圓柱種植在泡面：側柄中段版 Atlas

**用途：**此方法的底座一開始就貼著球面，柄從短圓柱側面中段橫向伸出。這不是 T 槌，也不是外端接柄版。

~~~text
Create one full-resolution photorealistic 16:9 image of one large intact translucent spherical bubble, seen in a clean three-quarter view.

Distribute up to 24 separately readable short double-ended cylindrical round-hammer heads across the visible hemisphere, like small rigid trunks planted on the sphere. Every cylinder's long axis follows the local outward sphere normal. The bubble-facing circular base uses a sphere-conforming contact seat so the base footprint fits the local curvature; a narrow bright rim glow belongs only to the base-to-shell interface.

Each cylinder has a visible outer circular end cap and exactly one thin straight handle attached sideways at the middle of the cylinder's sidewall. The handle extends in the local tangent direction and is approximately perpendicular to the cylinder's radial axis. The handle does not attach to the bubble-facing base and does not extend axially from the outer cap. Keep each head, side-middle joint and full handle independently traceable. Vary tangent handle directions around the sphere; do not make all handles parallel.

No people, no hands, no swinging, no hammer-to-hammer collision, no cracks, no debris and no regular tiled grid. Keep the sphere pristine. If 24 heads cannot remain visually distinct, show fewer instead of fusing or simplifying them.

No T-head, no plus-sign cross head, no outer-end axial handle, no missing side handle, no floating base, no glow at the outer cap or handle joint, no random damage, no text or watermark.
~~~

## I-14｜球面短圓柱候選 Atlas：先無柄、無人物

**用途：**與 I-13 不同：這條先只選球面位置與圓柱方向，刻意不加柄，適合「選候選再加柄／人物」分階段流程。

~~~text
Create one photorealistic full-resolution 16:9 candidate-atlas image containing one large intact translucent spherical bubble and 25 short cylindrical stubs positioned at distinct, well-spaced points across its visible hemisphere.

Each stub is short and clearly cylindrical, with a flat circular base patch mounted directly against the spherical surface. Its centreline points generally outward from the local sphere surface with modest intentional variations in tilt. The base-to-bubble interface is the selected contact surface and emits a narrow bright circular or elliptical rim glow. The opposite free end cap remains visible.

Do not add handles, people, hands, T-heads, crossbars, swinging motion, impact cracks or destruction effects. Keep all candidate stubs separated and individually selectable; no two stubs overlap. This image is for selecting one candidate position and axis before later stages, not a final action scene.

Use realistic glass refraction, controlled lighting and a neutral dark studio environment. Preserve the complete spherical silhouette and every base contact patch.

No long shafts, no outer-end handles, no side handles at this stage, no axes, no hammers, no labels covering the candidates, no repeated ghost stubs, no text, no watermark.
~~~

## I-15｜從候選選一枝：外端接柄＋人物握柄版

**用途：**只適用 I-14 這條外端接柄拓撲。選中的短圓柱保留原位置；長柄同軸接在遠離泡泡的外端面。不可套用側柄中段方案。

~~~text
Use the supplied accepted single-candidate bubble raster as the exact visual parent. Preserve the selected short cylindrical stub's sphere anchor, cylinder axis, base contact patch and camera. Remove every unselected cylinder, glow ring and ghost candidate completely.

Keep exactly one selected short cylinder as the striking head. Attach one long straight handle concentrically to its outer free circular end cap, extending away from the sphere. This is an axial outer-end handle, not a lateral side handle. The cylinder and handle form one rigid continuous assembly with no gap or bend at the joint.

Add exactly one adult female warrior beside the selected assembly. Her two hands visibly and anatomically plausibly grip the existing long handle. Her grip aligns with the locked handle axis. Keep the large translucent sphere intact and preserve the selected base-to-sphere contact ring; do not add a large burst yet.

Show the complete sphere, the selected cylinder, the outer-end handle joint, the full handle, both gripping hands and the contact patch. Realistic cinematic materials and clear scale.

No side-middle handle, no second shaft, no extra cylinder, no other person, no leftover candidate, no moved sphere anchor, no missing grip, no bent handle, no cracks before the contact-effect stage, no text or watermark.
~~~

## I-16｜一柄一頭、多向扁平面圓槌

**用途：**後期武器結構：頭部看起來圓，是因為很多厚實平面沿不同方向排列；不是刺球、鏈錘或一圈獨立小槌。

~~~text
Create one photorealistic cinematic 16:9 image of the approved adult female warrior holding exactly one massive war hammer with both hands.

The weapon has one long straight rigid handle and one integrated rounded hammer head. The head appears broadly rounded because many thick, wide, flat metal striking faces point outward in different directions. Each face is a broad sledgehammer-like flat facet, not a spike, stud, blade or ball-shaped ornament. All facets belong to one integrated head; they are not separate miniature hammers arranged in a ring.

The outward flat facet aimed at the translucent glass sphere is the only active striking face. It reaches the target at one clear point P. Keep the active flat facet, its boundary, the rigid head, the single handle, the grip and the contact seam visible. The weapon remains recognizably one hammer: one handle, one head.

Use realistic heavy metal, controlled cinematic light, a readable three-quarter camera, and a large clear sphere. Keep contact glow restrained until the actual contact point is unambiguous.

No spikes, no studs, no chain, no flail, no morning-star, no halo of separate hammers, no ring-shaped scene prop, no second handle, no axe blade, no random contact, no hidden active face, no text or watermark.
~~~

## I-17｜多向扁平面圓槌 H0 / H2 配對規則

**用途：**這一條沿用 I-16 的同一把武器，只分開出兩張圖。

**H0 完整 Prompt：**

~~~text
Create one photorealistic cinematic 16:9 still using the approved heroine and the approved single-handle, single-rounded-head multi-facet hammer reference.

The hammer head is one integrated rounded mass made from many thick broad flat outward-facing metal facets. The heroine holds one long straight handle with both hands. One nominated outward flat facet is oriented toward the large translucent sphere and is visibly separated from the intact sphere by a clear positive air gap.

The head and handle remain one rigid tool. Keep the nominated facet boundary, sphere surface, full handle and both hands visible. Use a three-quarter camera that reveals which flat facet is intended to meet the sphere. No contact glow, cracks, dents or debris.

No spikes, no studs, no chain, no flail, no separate mini hammers, no extra handle, no axe, no sidewall-first contact, no text or watermark.
~~~

**H2 完整 Prompt：**

~~~text
Use the approved H0 image as the strict parent and keep the exact same multi-facet rounded-head hammer, handle, heroine, sphere, camera and scene.

Move the same rigid hammer along its established path until only the nominated broad flat outward-facing facet first contacts the sphere at P. Close the air gap to zero without interpenetration. The other head facets remain away from the sphere; no spike, edge or curved head region reaches the target first.

Show one restrained contact glow and the first micro-crack beginning at P. Do not produce a full burst yet. Keep the active facet boundary visible.

The weapon remains one integrated rounded head and one straight handle. No spikes, no studs, no flail, no chain, no ring of separate hammers, no axe blade, no random crack origin, no text or watermark.
~~~

## I-18｜T 槌多角度／多動作矩陣：完整母 Prompt＋選項

**用途：**repo 中的 192 組路線是 8 個碰撞軸 × 12 個鏡頭 × 2 種蓄力。每張是一個獨立全幅圖；不能生成一張拼圖冒充 192 張證據。

先貼以下母 Prompt，再**每次只選一個碰撞方向、一個鏡頭、一種蓄力動作**。

~~~text
Create one single full-frame photorealistic 16:9 image of the approved heroine and one approved rigid T-hammer in the approved sphere scene. Generate only one test variant, one camera view and one action version in this image.

The selected terminal end striking face must be the only allowed first-contact surface. Keep the head as one straight rigid rectangular crossbar, the single handle straight and attached at the midpoint joint, and the handle perpendicular to the crossbar's long axis. The terminal face must meet the sphere at P when the selected state is H2. The cheek, upper and lower long sides, corners, centre joint and handle remain clear of the target.

The heroine's body pose and wind-up may differ between variants, but the final approach segment must follow the chosen collision direction. Camera movement changes only the view, never the world-space impact geometry. Show the full weapon and contact area; use a slight off-axis angle where necessary so the contact seam is visible.

No axe, no plus-sign cross head, no radial multi-face head, no cheek-first contact, no corner-first contact, no handle-first contact, no bending, no detached head, no extra shaft, no false gap at H2, no penetration, no random cracks, no montage, no labels, no watermark.
~~~

**8 個碰撞方向，每次只選一個：**

1. X_RIGHT — 從畫面左往右的水平橫掃。
2. X_LEFT — 從右往左的反向橫掃。
3. Z_UP — 由下而上的垂直上勾。
4. Z_DOWN — 由上而下的高位下劈。
5. XZ_RISE — 左下向右上的斜向上擊。
6. XZ_FALL — 左上向右下的斜向下擊。
7. Y_DEPTH — 由場景前後景深方向接近；相機須偏離法線以顯示接縫。
8. OBLIQUE_3D — 三維斜方向的全身旋轉重擊。

**12 個鏡頭，每次只選一個：**

1. 端面掠射審計：約偏離碰撞法線 18°，可見接縫與端面邊界。
2. 前側三分之四：同時顯示端面及側壁厚度。
3. 側面輪廓：看清槌頭、柄接點與碰撞軸。
4. 低仰角英雄鏡：從低位仰拍，但接觸切口仍可見。
5. 高位鶴臂俯視：從碰撞軸另一側高位看向接觸面。
6. 荷蘭斜角：相機約 25° 滾轉，武器本體不跟著變形。
7. 反向三分之四：從目標另一側反看，兩柄與接縫仍可見。
8. 微距接縫：近拍端面周界，火花不可蓋住接觸。
9. 越肩追擊：從攻擊者手柄後方看向碰撞區。
10. 高空環繞：上方環繞視角，但世界碰撞方向保持不變。
11. 低位掠射：顯示端面厚度及零間隙狀態。
12. 縱深透視斜視：凸顯前後景深，仍看見兩端面與握柄。

**2 種蓄力動作，每次只選一個：**

- 寬幅旋轉蓄力：肩與髖先帶動大弧線；接觸前最後一段直線沿指定碰撞方向進入。
- 緊湊加速蓄力：收縮蓄力後快速加速，使用不同於寬幅版本的身體姿勢；接觸前最後一段仍直線沿指定方向進入。

若要 H0、H2、H3，請為每個 variant 各自使用 I-02、I-04、I-05 的對應狀態 Prompt。192 組規劃不代表 192 張真實圖片已經生成或通過驗收。

## I-19｜雙槌端面矩陣：48 個獨立測試的變體法

**用途：**這條是 4 種碰撞軸 × 12 種鏡頭，共 48 個變體。它與 I-18 的 192 組及 I-09 稠密候選圖不是同一種計數。

使用 I-06 的雙 T 槌 Prompt，或 I-08 的厚十字 Prompt，然後每張只選一個碰撞方向及一個鏡頭。

**4 個方向：**水平左至右；垂直由下至上；左下至右上的斜向上；前後景深方向。

**12 個鏡頭：**端面掠射、側面、前側三分之四、反側三分之四、低角度、高角度、俯視、15° 荷蘭斜角、微距接縫、越肩、長焦壓縮、廣角全景。

**4 種柄向輪轉方法：**兩柄投影分處接縫兩側、兩柄朝同一側、A 柄朝相機而 B 柄背向相機、兩柄在畫面投影成不同對角線。每次柄向只能作為選定變體的一個固定設定，不能改變指定端面互撞。

~~~text
Create one single full-frame 16:9 geometry-test image of the selected pair of complete approved hammers. Apply only the selected collision axis, camera view and handle-roll arrangement. Both designated terminal faces must meet face-to-face at P with opposing normals. Keep the two weapons separate and rigid. The handles may project in different directions because each complete rigid weapon is rolled about the collision axis, but neither handle may bend and neither head may rotate independently from its handle. The camera view must reveal the face boundaries. No panel grid, no contact sheet, no fake geometry labels and no text.
~~~

## I-20｜《邊界行人》六幕 IMAGE 分鏡：寫實電影版

**用途：**故事敘事路線，而非武器幾何驗收。每張圖只講一個可拍事件；角色身份要用同一參考圖鎖定。需要實際打擊時才從 I-02 至 I-05 選用對應拓撲。


**預覽（會話生成 · 非正式驗收）**

| 幕 | 預覽 |
| --- | --- |
| ACT 1 畫界 | ![I20-1](boundary_pedestrian/i20/act1_draw_boundary.jpg) |
| ACT 2 保護 | ![I20-2](boundary_pedestrian/i20/act2_protect_sphere.jpg) |
| ACT 3 碎裂 | ![I20-3](boundary_pedestrian/i20/act3_shatter_fall.jpg) |
| ACT 4 假修 | ![I20-4](boundary_pedestrian/i20/act4_false_repair.jpg) |
| ACT 5 一界 | ![I20-5](boundary_pedestrian/i20/act5_one_boundary.jpg) |
| ACT 6 選擇 | ![I20-6](boundary_pedestrian/i20/act6_choose_dance.jpg) |

完整圖庫與 SHA：[`boundary_pedestrian/README.md`](boundary_pedestrian/README.md)

### ACT 1 — 畫界：混亂中建立邊界

~~~text
Create one photorealistic cinematic 16:9 music-video still featuring the same adult East Asian heroine from the reference. She stands in a chaotic neon graffiti workshop at night, surrounded by tangled cables, torn paper, blurred silhouettes and conflicting coloured light. She draws one bright clean line across the floor with a small handheld light marker, separating the chaotic space into two visually distinct worlds. Her expression is focused and compassionate, not villainous. The scene should look like a real high-budget music-video set with motivated light, deep spatial layers, off-centre composition and realistic materials. The line is a visual metaphor for an attempt to impose order; it is not a literal weapon. No hammer, no bubble impact, no text or logo.
~~~

### ACT 2 — 保護：完美泡泡逐漸窒息

~~~text
Create one photorealistic cinematic 16:9 still in a vast gilded retro capsule-toy hall. The same heroine gently cups one large perfectly transparent glass sphere containing a few small warm human silhouettes representing loved ones. Outside the sphere, wind-driven rain and dark thorn-like shadows strike the glass but do not enter. Inside, the warm light is beautiful yet slightly too sterile; a delicate flower begins to wilt near the trapped figures. The heroine's body language is protective and loving, but the composition makes the sphere feel like a beautiful closed cage. Preserve a realistic human face, believable scale and tactile glass refraction. No weapon, no impact, no explosion, no readable text or watermark.
~~~

### ACT 3 — 碎裂：垂直保護關係崩塌

~~~text
Create one photorealistic cinematic 16:9 slow-motion music-video still at the instant a large transparent glass sphere breaks open. Crystal fragments travel outward from one clearly motivated fracture region and reflect multiple human faces, while the same heroine and the previously protected people fall together toward the same ground plane. No one is elevated like a saviour; everyone shares the same physical level. Use a wide camera with a distinct foreground, middle ground and background, sharp readable glass fragments and controlled highlights. The metaphor is the collapse of a one-way protection system into shared responsibility. No random extra spheres, no decorative text, no gore, no watermark.
~~~

### ACT 4 — 假修：止痛與假安全

~~~text
Create one photorealistic cinematic 16:9 still in a pastel neon dessert pharmacy and retro diner. The same heroine and a small group of people smile for phones under exaggerated beauty-filter lights while holding bright milkshakes and capsules that symbolize temporary relief. Behind them, a huge transparent balloon is stretched almost to bursting, and a tiny pin approaches it unnoticed. A cheap smiley bandage covers a deep crack in the wall. The image should feel superficially cute and comfortable, but the framing leaves the unstable balloon ominously visible above the group. Realistic people, tactile props, deliberate art direction and a visual contradiction between cheerful foreground and threatening background. No weapons, no readable signage, no watermark.
~~~

### ACT 5 — 一界：濾鏡消退、回到真實

~~~text
Create one photorealistic cinematic 16:9 still in a drained abandoned swimming pool at blue hour. The pastel filter world has faded, revealing bare concrete, broken glass reflections and honest unpolished textures. The same heroine kneels at the same physical level as her friends and carefully wraps a simple bandage around one person's hand. Their clothes are plain and practical; their expressions are tired but genuine. A subtle red thread connects their hands, not as magic spectacle but as a quiet symbol of mutual responsibility. Use natural overcast light, wide negative space and restrained colour. No weapon, no glamour filter, no heroic pedestal, no text or watermark.
~~~

### ACT 6 — 選擇：重建泡泡，或在碎片上起舞

~~~text
Create one photorealistic cinematic 16:9 final music-video still on a rooftop covered in harmless reflective glass-like fragments at dawn. The same heroine stands with her friends at equal height, holding a simple bubble wand in one hand while choosing whether to blow a new bubble. The group begins a liberated dance together across the reflective rooftop; their body language is joyful, imperfect and mutually connected. The sky transitions from cool blue to a restrained warm sunrise, giving the image a feeling of earned freedom instead of a perfect happy-ending filter. Preserve the heroine's identity and outfit continuity from the supplied references. No giant weapon, no new bubble impact, no split-screen, no text or watermark.
~~~

## I-21｜《邊界行人》六幕：可愛 INS／粉彩藝術版

**用途：**使用相同六幕因果，但以可愛、粉彩、社交媒體美學處理。只換風格與道具隱喻，不應把物理接觸規則混入柔性敘事鏡。


**預覽（粉彩會話生成 · 非正式驗收）**

| 幕 | 預覽 |
| --- | --- |
| ACT 1 | ![I21-1](boundary_pedestrian/i21/act1_pastel_yarn_line.jpg) |
| ACT 2 | ![I21-2](boundary_pedestrian/i21/act2_candy_jar_protect.jpg) |
| ACT 3 | ![I21-3](boundary_pedestrian/i21/act3_diamond_rain_shatter.jpg) |
| ACT 4 | ![I21-4](boundary_pedestrian/i21/act4_claw_machine_fake_safety.jpg) |
| ACT 5 | ![I21-5](boundary_pedestrian/i21/act5_pool_bandage.jpg) |
| ACT 6 | ![I21-6](boundary_pedestrian/i21/act6_rooftop_rollers.jpg) |

完整圖庫：[`boundary_pedestrian/README.md`](boundary_pedestrian/README.md)

**將以下風格段落加在 I-20 的其中一幕 Prompt 結尾：**

~~~text
Use a playful Instagram-inspired pastel art direction: soft candy pink, lilac, mint and butter yellow; glossy bubblegum reflections; charming oversized props; playful retro-capsule, dessert-shop and roller-skating references; crisp editorial composition with cinematic depth rather than a flat cartoon. Keep the people visually human and emotionally nuanced, not chibi or anime. The metaphor should remain readable beneath the cute surface. No fake social-media interface, no readable text or logos.
~~~

**6 個可替換道具場景：**

1. 粉彩亂房間：打結的粉色毛線、毛絨玩具、少女用螢光筆畫出發光界線。
2. 甜點玻璃罩：草莓蛋糕與小人被巨大的透明糖果罐罩住，外面紫色酸雨，裡面暖黃卻封閉。
3. 鑽石雨碎裂：玻璃糖罐裂開，晶片像彩色鑽石雨，大家一同向後傾倒。
4. 抓娃娃機咖啡廳：粉紅金屬爪抓起舊泰迪熊作替罪羊，朋友們喝珍珠奶茶假裝放心。
5. 濾鏡消退：霓虹裝潢剝落，普通混凝土顯露，少女替朋友包紮。
6. 復古溜冰天台：大家穿雙排溜冰鞋牽手起舞，將裂痕重新變成共同的節奏。

每一張仍須是單張完整圖像。不要讓模型把這六幕畫在一張六格拼貼裡。

## I-22｜十種接觸畫面的洗圖方法：各自獨立出圖

**用途：**用不同動作與攝影方向找真正能看清接觸的構圖。每次只取一種，不要一次要求十格同時出現在畫面。

**共同母 Prompt：**

~~~text
Create one single full-frame photorealistic 16:9 image of the approved rigid hammer and translucent sphere. The nominated active surface must be visible, and the contact state must match the requested stage. Keep the same character identity, weapon topology, contact location and world-space geometry. Make the chosen camera and action visibly different from the prior candidate, not a mirrored duplicate. The contact seam must remain inspectable. This is one full image, not a ten-panel grid, contact sheet or collage.
~~~

**十種獨立方法（每次選一項加在共同母 Prompt 後）：**

1. 赤金／青銀雙色的正面端面撞擊：色光描出兩個端面邊界，但不能遮住接縫。
2. 垂直高位跳劈：人物從高位落下，最終端面接觸方向保持鎖定。
3. 45° 對角上擊：整把剛體槌沿斜向路徑進入，柄與頭不相對轉動。
4. 貼地低角橫掃：低機位看見全身重心與端面接觸；不能以側壁假裝端面。
5. 360° 蓄力後定格：只呈現一個真正接觸瞬間，避免重影槌頭。
6. 復古競技場戰鼓材質：槌頭可採鼓面質感，但所選平端仍須是唯一接觸面。
7. 越肩接觸微距：同時看見主角手部、頭柄接點、端面周界和球面。
8. 熔岩深淵低仰角：使用環境光營造力量感，幾何與接觸點不變。
9. 側逆光拉扯姿勢：光源勾出端面厚度，不讓剪影完全遮掉接觸 seam。
10. 超廣角斷橋場景：環境規模很大，但人物、武器、球面接觸位置仍可審查。

這十種不是十個已證實成功的方式；它們是十個可獨立生成、獨立審核的候選構圖。

---

# PART II — VIDEO PROMPTS

## V-00｜影片共用寫法：半公式，不用程式語法

**半公式：** 固定世界與角色 + 本段開始狀態 + 唯一動作路徑 + 明確時間節點 + 因果效果 + 不可變項 + 輸出要求。

影片不是把多張漂亮 IMAGE 的描述連起來就算完成。每段都要講清楚：開始時是什麼狀態，物件如何運動，哪一刻發生接觸，效果從哪裡開始，以及結束時哪些東西仍然不變。

## V-01｜10 秒單場景 T 槌打泡泡 VIDEO

**用途：**由正空隙開始，進入端面接觸，裂紋擴散，再破殼。整段使用一把剛性 T 槌，不換場、不換武器。

~~~text
Create one continuous 10-second photorealistic cinematic 16:9 live-action shot, not a montage and not unrelated scenes stitched together.

Use the supplied approved adult East Asian heroine reference, the approved single rigid T-hammer reference, and one large translucent crystal-glass sphere in a vast abandoned industrial hall. Keep the heroine's face, long dark-brown hair, black combat outfit, body scale, weapon silhouette, head-handle joint, sphere centre and radius, contact anchor P, camera rig, background landmarks and motivated key-light direction consistent throughout.

The heroine holds the T-hammer with both hands. The crossbar is one straight rigid rectangular head and the handle is attached at its midpoint at a right angle. The hammer head and handle move as one rigid tool. The designated terminal end striking face is the only surface allowed to contact the sphere first. The broad cheek, corners, head-handle joint and handle never touch first.

TIMELINE:
0.0–2.0 seconds — PRE_FAR: the nominated terminal face is clearly separated from the pristine sphere by a wide visible air gap. The heroine is winding up. No contact glow, cracks, sparks or debris.
2.0–4.5 seconds — PRE_NEAR: the same rigid hammer advances along the established approach path. The gap narrows but remains positive. The sphere remains intact.
At 4.5 seconds — CONTACT: the terminal face meets the sphere at P. The gap becomes zero without interpenetration. A restrained first contact glow and the first fine micro-cracks begin at P only.
4.5–7.0 seconds — E_MID: cracks and a subtle shock ripple propagate outward from P across the outer glass shell. The heroine and weapon follow through naturally without changing the head-to-handle angle. Background landmarks remain stable.
7.0–10.0 seconds — E_END: the outer shell breaks outward into coherent fragments from the established fracture region. The inner sanctuary and its inhabitants remain intact and unharmed. End on a readable composition in which the heroine, hammer and shell fragments can still be distinguished.

Use one motivated continuous camera move. The camera may travel slightly to reveal the contact seam, but it must not fake the hit with a zoom, hide a geometry reset, replace the background or teleport the object. Controlled bloom and small sparks only; never cover the first-contact point.

No early cracks, no gap at the impact instant, no penetration, no cheek-first or handle-first contact, no extra shaft, no weapon redesign, no vertical splice seam, no random fracture source, no resident injury, no text, no logo and no watermark.

Deliver one real continuous 10-second clip. If the generation system cannot preserve continuous motion, do not claim the clip passed: produce five separate audited keyframes using V-02 instead.
~~~

## V-02｜五關鍵幀閉環：KF1 至 KF5

**用途：**如果影片模型容易跳場或把柄變形，就改成五張各自生成的全幅圖，再用真正影片工具剪輯／插值。每幀都應以最後一張已通過的母圖作參考，不能每次從零自由重畫。

### KF1 — 0.0 秒 PRE_FAR

~~~text
Create one full-frame photorealistic 16:9 keyframe at 0.0 seconds. Use the approved heroine reference, approved rigid T-hammer reference and master scene reference. The heroine stands on the left in a believable wind-up pose; the large translucent sphere is on the right. The nominated terminal striking face is aligned for the intended future approach but remains visibly separated from the pristine sphere by a wide positive air gap. Preserve the exact character identity, outfit, weapon topology, handle joint, sphere geometry, background landmarks, camera and light direction. No cracks, glow, sparks, debris or contact shadow. This is the PRE_FAR state, not an impact scene. No text or watermark.
~~~

### KF2 — 2.0 秒 PRE_NEAR

~~~text
Create one full-frame photorealistic 16:9 keyframe at 2.0 seconds, using the accepted KF1 raster as the strict visual parent. Keep the same heroine, face, outfit, rigid T-hammer, sphere, camera and background landmarks. The only intended change is that the complete hammer advances along the established approach path and the positive air gap becomes smaller. The designated terminal face is still not touching the sphere. Keep the head and handle as one rigid object; preserve their angle and the existing grip. The sphere remains pristine with no glow, cracks or debris. Do not move the sphere, relayout the scene or invent a new handle. No text or watermark.
~~~

### KF3 — 4.5 秒 CONTACT

~~~text
Create one full-frame photorealistic 16:9 keyframe at 4.5 seconds, using the accepted KF2 raster as the strict visual parent. Preserve the same heroine, identity, outfit, rigid T-hammer, sphere, camera, lighting and background landmarks. The hammer's designated flat terminal end face now makes its first contact with the sphere at the same established point P. The gap is zero without penetration; the broad cheek, corner, central joint and handle remain clear of the sphere. Only a restrained contact glow and the first fine micro-cracks begin at P. Do not jump to a full explosion. Make the contact seam easy to inspect. No text or watermark.
~~~

### KF4 — 7.0 秒 E_MID_SHOCK

~~~text
Create one full-frame photorealistic 16:9 keyframe at 7.0 seconds, using the accepted KF3 raster as the strict visual parent. Keep the heroine, weapon topology, grip, sphere location, camera rig and background landmarks stable. Change only the authorized post-impact action and the shell fracture state. Fine cracks and a restrained shock ripple propagate outward from the same point P across the outer shell. A few shell fragments may begin to separate outward, but the full scene must remain readable. The hammer remains a rigid connected object and the inner sanctuary remains untouched. No new crack source, no character drift, no background replacement, no text or watermark.
~~~

### KF5 — 10.0 秒 E_END_BLAST

~~~text
Create one full-frame photorealistic cinematic 16:9 final keyframe at 10.0 seconds, using the accepted KF4 raster as the strict parent. Preserve the heroine's identity, outfit, body scale, weapon topology, camera and scene landmarks. The outer sphere shell breaks outward from the fracture region already established at P. The glass fragments have coherent outward trajectories; the inner sanctuary and its inhabitants remain intact and safe. Keep enough negative space to read the heroine, the hammer silhouette and the broken shell rather than drowning everything in white light. Do not move the original impact point, invent a second sphere, redesign the weapon or replace the location. No text or watermark.
~~~

**注意：**五張關鍵幀逐張通過，不自動等於影片連續性通過。完成後還要檢查中間運動、場景跳變、垂直接縫、速度突變及未授權的身份／幾何漂移。

## V-03｜Planted-cylinder 專用影片：錨點固定、人物施力

**用途：**給底座一開始已經貼住泡面的側柄圓柱。這一條沒有 H0 遠距空隙；不能將 V-01 的飛行 T 槌時間軸套進來。

~~~text
Create one continuous 8–10 second photorealistic cinematic 16:9 shot using the supplied accepted planted-cylinder master image.

The scene contains one large translucent sphere and the same approved double-ended short cylindrical hammer head planted against the sphere. Its bubble-facing base is fitted to the local sphere curvature with a narrow luminous contact seat. The single thin straight handle attaches sideways at the cylinder's side-middle and extends in the local tangent plane. The handle is not attached to the base and does not extend axially from the outer cap. Preserve the cylinder axis, base seat, side-middle joint, outer circular cap and contact anchor P.

The same adult heroine grips the existing lateral handle with both hands and gradually transfers force through her wrists, shoulders, hips, stance and body rotation. The cylinder base remains planted against the sphere at P throughout; the contact point does not travel across the shell. The head and handle remain one rigid assembly. The heroine's pose, balance and applied torque evolve naturally, but the handle must never be invented, moved to the outer cap or bent to accommodate her grip.

At the defined force-transfer beat, a tight glow appears at the existing base-to-shell interface P. Fine cracks begin at that same interface and propagate outward over the sphere shell. The outer shell eventually breaks outward from the established fracture region. The protected inner sanctuary and its inhabitants remain intact and unharmed.

Use one continuous motivated camera move and realistic glass refraction. Preserve the same background landmarks and camera identity. Include at least one clear moment where the base contact ring, side-middle handle joint, both hands and contact anchor are visible before the brightest bloom and debris.

Do not create a pre-impact air gap unless the supplied parent reference explicitly has one. No T-hammer head, no plus-sign cross head, no outer-end axial handle, no additional rod, no moving contact anchor, no head-handle deformation, no early cracks, no random crack origin, no resident injury, no text or watermark.
~~~

## V-04｜真正的 Image-to-Video／母圖閉環 Prompt

**用途：**任何 VIDEO 拿通過的 IMAGE 續動，都可使用這個規則；每段只允許一個明確狀態改變。

~~~text
Animate the supplied accepted parent frame into one short photorealistic 16:9 shot. Treat the supplied image as the visual source of truth, not a loose style reference.

Preserve the same character identity, face, outfit, body scale, approved object topology, object dimensions, contact anchor P, target geometry, background landmarks, camera rig and motivated light direction. The object must remain the same object, with the same joints and relative proportions. Do not redesign it to make the next action easier.

For this segment, the only authorized change is: [DESCRIBE ONE VISIBLE ACTION OR STATE CHANGE IN PLAIN NATURAL LANGUAGE]. Every other named scene element remains fixed. Let the motion travel through a physically coherent path from the parent state into the next state. Do not teleport, splice, dissolve into a different composition, silently reset the camera or use a dramatic zoom to fake contact.

If contact is not yet due, preserve a visible positive gap and an intact target. If this is the first-contact segment, the designated active surface alone reaches P with no gap and no penetration. If this is a post-contact segment, effects continue from the same P rather than starting elsewhere.

Keep the critical object boundary, joint, grip, contact seam and target surface unobstructed long enough to review. Use restrained effects and motivated camera motion. No unapproved character or background changes, no new weapon or handle, no bending rigid parts, no early fracture, no unrelated edit, no text or watermark.

Output a real clip derived from this parent frame. If the requested change cannot be made while preserving the frozen scene, stop and report the segment as blocked rather than inventing a different image.
~~~

每個片段中的方括號只替換成一個自然語言動作，例如「move the complete hammer 10 units closer while preserving a positive gap」；不要同時改相機、武器、角色、光效和背景。

## V-05｜雙 T 槌端面互撞 VIDEO

**用途：**兩個分開的 T 槌先有空隙、再端面對端面接觸，之後輕微回彈。這不是打泡影片。

~~~text
Create one continuous 6-second photorealistic cinematic 16:9 shot showing two adult fighters controlling two separate complete T-hammers.

Each hammer has one straight rigid rectangular crossbar and one straight handle attached at its own midpoint joint at a right angle. Both weapons remain separate complete objects. The selected terminal end striking face of hammer A is aligned with the selected terminal end striking face of hammer B on one shared collision axis. Their selected face normals oppose one another. The broad cheeks, corners, centre joints and handles must remain clear.

TIMELINE:
0.0–2.0 seconds: both selected terminal faces approach along the same collision axis with a clear positive gap. The heads do not rotate independently and the handles remain straight.
2.0–3.0 seconds: the gap narrows; both fighters' bodies absorb the swing and their grips remain secure. There is still no contact effect before the actual hit.
At 3.0 seconds: the two designated flat terminal end faces meet at P, face-to-face, with no gap and no interpenetration. Show a small brief contact flash at the seam only.
3.0–4.5 seconds: the same two rigid hammers recoil slightly along the same collision axis, with the face boundary and handle geometry preserved.
4.5–6.0 seconds: both fighters stabilize, and the camera holds a readable side three-quarter view of the separate weapons and the final separation.

Use one continuous motivated camera move. The camera may orbit slightly to expose the seam but must not change the world collision axis or fuse the two tools in projection. Controlled sparks only.

No cheek-first contact, no sidewall hit, no corner-first hit, no handle-first collision, no one giant H-shaped weapon, no bent heads, no detached handles, no fake contact by zoom, no scene cut at impact, no text or watermark.
~~~

## V-06｜厚十字圓端蓋 VIDEO

**用途：**與 V-05 不同：兩把厚 plus-sign 十字槌，指定圓柱外端蓋對撞。

~~~text
Create one continuous 6-second photorealistic cinematic 16:9 geometry-action shot of two independent thick plus-sign cross hammers.

Each hammer head has one thick horizontal rectangular arm and one thick vertical rectangular arm crossing at the centre, with solid cylindrical end pieces and flat circular outer end caps. Each complete hammer has its own straight rigid handle attached to its centre joint. Keep both plus-shaped heads and both handles fully separate.

0.0–2.0 seconds: the selected flat circular outer end caps align on one collision axis with a clearly visible gap. The curved cylinder barrels remain apart.
2.0–3.0 seconds: both hammers translate along the established axis while the camera reveals their cap rims and the intended contact.
At 3.0 seconds: only the two nominated flat circular end caps meet cap-to-cap at P. Their planes coincide and their normals oppose. No curved barrel, cross arm, corner, centre joint or handle touches first.
3.0–4.5 seconds: both rigid hammers recoil a small distance along the same axis, without independently rotating the heads.
4.5–6.0 seconds: the camera settles on both complete weapons with the contact rims still identifiable.

No T-hammer head, no X-head, no missing vertical arm, no fused H-shaped tool, no sidewall-first contact, no corner-first contact, no handle-first contact, no false camera-only collision, no bending or detached parts, no text or watermark.
~~~

## V-07｜線形棒正控制／負控制 VIDEO

**用途：**製作兩條分開的短片：正控制與負控制。不可在同一條生成中途把正確的接觸面悄悄翻錯。

### 正控制完整 Prompt

~~~text
Create one continuous 5-second photorealistic 16:9 shot of two adult fighters using very thin, straight, rigid rods with small planar impact facets integrated at their tips. Do not render hammers or crossbars.

The airborne fighter uses a diving overhead attack; the grounded fighter uses a distinct low crouching response. Their full rods and gripping hands remain visible. The two rod centre lines approach and cross at a right angle. At the impact instant, the small planar facets are parallel and face-to-face with opposing normals at the crossing point.

0.0–2.0 seconds: the rods approach with visible separation.
2.0–3.0 seconds: the final paths align so the rod axes cross at 90 degrees while their tiny planar facets are prepared for face-to-face contact.
At 3.0 seconds: the facets make actual contact; no gap and no interpenetration. Small sparks may appear exactly at the facet seam.
3.0–5.0 seconds: the rods rebound slightly while retaining their straight shape and readable crossing geometry.

Keep the axis crossing and face orientation separately legible. Camera motion must not create a false crossing. No T-head, no plus-sign hammer, no bulky rod tips, no coaxial end-to-end hit, no bent rods, no body contact, no text or watermark.
~~~

### 負控制完整 Prompt

~~~text
Create one continuous 5-second photorealistic 16:9 negative-control clip using the same scene, fighters, rods, camera, lighting and action scale as the supplied positive-control clip.

Both thin rigid rods approach and cross at a right angle, but intentionally rotate one small planar impact facet away from the required face-to-face orientation. At the collision beat the two facets do not oppose one another, and the intended correct planar-face contact fails. Keep the failure visible and unambiguous; do not hide it with a flash, motion blur or camera cut.

The rods remain straight and separate, with their tiny facets visible. The fighters complete the failed attempt without changing into a different weapon system. This is an expected-fail negative control for comparison, not a passing example. Keep all other scene conditions as comparable to the positive-control clip as possible.

No hammer heads, no plus-sign weapons, no false claim of correct face contact, no unrelated action or costume change, no text or watermark.
~~~

## V-08｜多向扁平面圓槌 VIDEO

**用途：**單柄單頭的多面圓頭；接觸面在頭部周圍切換選擇，但一個片段只讓一個指定面負責接觸。

~~~text
Create one continuous 8-second photorealistic cinematic 16:9 shot of the approved heroine using one integrated rounded-head war hammer. The weapon has one straight handle and one rounded head built from many thick broad flat metal striking facets pointing outward. It is one hammer, not a collection of separate small hammers, and it has no spikes or chain.

0.0–2.0 seconds: the heroine prepares a compact rotating swing while the nominated flat facet is visible. The sphere is intact and a positive gap remains.
2.0–4.0 seconds: the same rigid hammer advances toward the sphere. The nominated facet becomes the leading active face; the head and handle do not bend or separate.
At 4.0 seconds: the designated broad flat facet contacts the sphere at P, with zero gap and no interpenetration. Only restrained contact glow and the first fine cracks at P appear.
4.0–6.5 seconds: cracks propagate outward from P. The hammer follows through while preserving its integrated rounded-head silhouette.
6.5–8.0 seconds: the outer shell breaks outward from the established fracture region while the inner sanctuary remains intact.

Keep the nominated facet, its boundary, handle, grip and contact point readable. No new active contact point, no spikes, no studs, no chain, no flail, no halo of separate hammers, no second handle, no axe blade, no random crack source, no text or watermark.
~~~

## V-09｜3 分鐘《邊界行人》／Original Sin 敘事 MV 的製作 Prompt

> 靜幀母圖見 [`boundary_pedestrian/`](boundary_pedestrian/)。寫實六幕可作 V-09 image-to-video 起點。

**用途：**這是敘事剪輯方法，不是要模型一次生成完整 3 分鐘並幻想所有連續性。先生成 24 張關鍵卡或 50–54 個獨立鏡頭，再剪輯成影片。柔性敘事鏡不放武器；真正打擊鏡回到合適的專用武器 Prompt。

### MV 統一製作 Prompt

~~~text
Create a 3-minute cinematic music-video sequence titled conceptually as a journey from protection to shared freedom. Use the same adult East Asian female protagonist from the supplied character reference throughout. Preserve her facial identity and core character design, while allowing costumes and sets to change with each act.

The story has six distinct acts:
Act 1, drawing a boundary in chaos.
Act 2, protecting loved ones inside a flawless transparent sphere until protection becomes confinement.
Act 3, the sphere breaks and the protected people fall to the same level as the protector, revealing shared responsibility.
Act 4, a society covers deep cracks with cute filters, quick relief and a scapegoat.
Act 5, the filter fades and people face the damaged real world together.
Act 6, the protagonist chooses between rebuilding another false boundary and dancing freely with others on the fractured ground.

Use six visually distinct sets in order: a neon graffiti workshop or abandoned factory; a retro capsule-toy golden hall; a pastel supermarket of broken glass reflections; a candy-pharmacy diner with beauty-filter lights; a drained abandoned swimming pool; and a glass-fragment rooftop at dawn.

Build the video from approximately 24 key cards, four per act, or 50–54 short cuts. Give each shot one motivated action and one clear camera setup. Use wide establishing shots, close-up inserts, overhead views, low angles, Dutch angles, over-the-shoulder views, slow motion and tracking shots with purposeful variety. Maintain the protagonist identity and make the A-world/B-world visual change readable: A is warm, polished, protective and enclosed; B is cooler, fractured, tactile and shared.

Generate each shot as a separate asset, then edit to music. Do not force all six acts into one continuous scene. Keep physical object topology consistent within any shot that includes a weapon or impact; use dedicated contact prompts for such shots. No fake on-screen text, watermarks or generated UI.
~~~

### ACT 1 — 影片片段 Prompt：建立界線

~~~text
Create one 5–8 second photorealistic cinematic 16:9 music-video clip in a chaotic neon graffiti workshop at night. The same adult heroine moves through tangled cables, torn paper and blurred silhouettes. She notices the disorder, pauses, then draws one luminous line across the floor with a small light marker. The camera begins high and wide to show the disorder, then descends into a medium tracking shot of the line and her focused expression. Keep the action readable and motivated; the light line is a metaphor, not a weapon. Dark neon reflections, tactile surfaces, realistic movement and an editorial music-video rhythm. No glass sphere impact, no hammer, no text or watermark.
~~~

### ACT 2 — 影片片段 Prompt：保護逐漸成為封閉

~~~text
Create one 5–8 second photorealistic cinematic 16:9 clip in a grand retro golden capsule hall. The same heroine gently lifts a large transparent sphere containing small warm human silhouettes and cradles it with both hands. Outside, dark rain and thorn-like shadows press against the surface; inside, the warm light remains beautiful but unnaturally still. The camera tracks slowly around the sphere and briefly looks from inside the glass toward the heroine's concerned face. Let the figures inside make small restrained movements that suggest discomfort, not exaggerated cartoon distress. No weapon, no impact, no random cracks, no readable text or watermark.
~~~

### ACT 3 — 影片片段 Prompt：泡殼破裂、共同墜落

~~~text
Create one 5–8 second cinematic slow-motion 16:9 clip of a large transparent sphere fracturing and breaking open. The first visible fracture begins at one motivated shell region, then propagates outward before the outer shell fragments move away. The same heroine and the formerly protected figures fall together to the same ground level; no one remains elevated as a saviour. The camera tracks through the glass fragments without losing the main bodies or changing their identities. Use realistic glass refraction and controlled highlights. Keep the sequence causal—cracks first, shell separation next, falling fragments afterward. No unrelated explosion, no duplicate people, no text or watermark.
~~~

### ACT 4 — 影片片段 Prompt：虛假舒適與止痛

~~~text
Create one 5–8 second photorealistic cinematic 16:9 clip in a pastel neon dessert diner. The same heroine and a small group of people smile for their phones and raise bright milkshakes under flattering filter-like lights. The camera glides past a cheap smiley bandage covering a large crack in the wall, then tilts up to reveal a huge transparent balloon stretched dangerously tight above them. Their smiles continue while the balloon subtly trembles. Use deliberate contrast between cute surface design and underlying instability. No weapons, no sudden destructive impact, no readable signage, no text or watermark.
~~~

### ACT 5 — 影片片段 Prompt：回到破碎真實

~~~text
Create one 5–8 second photorealistic cinematic 16:9 clip in a drained abandoned swimming pool at blue hour. The neon look fades into natural cold light and real concrete texture. The same heroine kneels beside a friend and carefully wraps a bandage around the friend's hand. Other people sit nearby at the same level rather than looking up to a leader. The camera moves from a close-up of the hands to a restrained medium shot of the group. Their expressions are tired and honest, but there is the first quiet sign of mutual trust. No magic shield, no weapon, no glamour filter, no text or watermark.
~~~

### ACT 6 — 影片片段 Prompt：選擇自由

~~~text
Create one 5–8 second photorealistic cinematic 16:9 final clip on a rooftop at dawn. The same heroine holds a simple bubble wand while standing with friends on a ground scattered with harmless reflective glass-like fragments. She looks at the wand, then lowers it and takes a friend's hand. The group begins to dance together in a loose, imperfect circle as the sunrise warms the rooftop. Use a moving wide camera that reveals every person sharing the same ground, then settle on a readable final composition. The feeling is earned freedom rather than flawless fantasy. No weapon impact, no dangerous glass injury, no new bubble attack, no text or watermark.
~~~

## V-10｜將影片畫面做成「IMAGE＋教學」雙輸出

**用途：**每一幀原圖保持乾淨；教學板是額外資產，不要叫模型在影片內精確生成中文字、角度、SHA 或 PASS 勾號。

~~~text
For every generated keyframe, preserve an untouched full-resolution source image with no labels or overlaid diagnostics. Also prepare a separate teaching version using external layout tools, placing the exact source image beside the human-readable prompt formula, intended geometry, observed contact result, frame time and review status.

Never paint machine-readable IDs, hashes, numeric geometry values, Chinese labels or pass/fail icons into the source frame. Those belong in the separately rendered teaching board. The source image remains the evidence asset; the board is an explanatory copy and must not replace the source. If a real source frame or review receipt is missing, mark the corresponding field unverified instead of guessing.
~~~

---

# PART III — STYLE BLOCKS（一次只選一種）

以下只改美術，不改武器結構、接觸點或時間因果。將其中一段加到 IMAGE 或 VIDEO Prompt 最後即可。

## S-01｜寫實電影感

~~~text
Use high-budget live-action music-video photography, naturalistic skin and materials, motivated volumetric light, realistic glass refraction, restrained cinematic bloom, fine film grain, a dramatic but readable colour grade, off-centre composition and believable spatial depth. Preserve all specified object geometry and keep the contact area inspectable.
~~~

## S-02｜可愛 INS／粉彩

~~~text
Use a playful Instagram-inspired pastel art direction with candy pink, lilac, mint and butter yellow, glossy bubblegum reflections, charming oversized retro props and crisp editorial composition. Keep people visually human and emotionally nuanced rather than chibi or anime. The metaphor should remain readable beneath the cute surface. Preserve all specified geometry and event order. No fake social-media UI, no readable text or logos.
~~~

## S-03｜超現實隱喻

~~~text
Use restrained surrealist symbolism: impossible scale contrast, reflective glass fragments, boundary lines, suspended droplets and carefully composed negative space. Keep the core action physically legible even when the environment is dreamlike. Do not let surreal effects change the designated weapon surface, contact point, object count or cause-and-effect order. No random extra weapons or unexplained contact points.
~~~

## S-04｜低調幾何驗收／產品參考

~~~text
Use neutral studio lighting, a simple dark or grey background, clear silhouette separation and restrained reflections. Prioritize the complete object outline, joints, flat face boundaries and contact seam over atmosphere. No cinematic flare or dramatic particles that obscure geometry. No text, watermark or panel borders.
~~~

---

# PART IV — PROMPT 選擇索引

| 你的目的 | IMAGE 用法 | VIDEO 用法 |
|---|---|---|
| 先驗證 T 槌造型 | I-01 | 不需要先做影片 |
| T 槌打泡泡，從空隙到破殼 | I-02 → I-03 → I-04 → I-05 | V-01 或 V-02 |
| 兩把 T 槌真正端面互撞 | I-07 → I-06 | V-05 |
| 厚十字雙槌圓端蓋互撞 | I-08；候選搜尋用 I-09 | V-06 |
| 線形棒 90° 正反控制 | I-10 與 I-11；對照展示用 I-12 | V-07 |
| 側柄圓柱種植在泡面 | I-13 | V-03 |
| 球面候選、外端接柄、再加人物 | I-14 → I-15 | 依這條拓撲另用 V-04，不能照搬飛行槌版 |
| 多向扁平面圓頭 | I-16、I-17 | V-08 |
| 192 個 T 槌多視角變體 | I-18 | 用 V-02 保持時間狀態清晰 |
| 48 個雙槌接觸變體 | I-19 | V-05 或 V-06，取決於選定武器 |
| 六幕故事圖像 | I-20 或 I-21 | V-09 六幕逐段生成 |
| 單幀圖與精確教學並行 | 任意 IMAGE + V-10 的教學規則 | 每個 keyframe 都另外輸出教學板 |

## 從 branch 盤點而來的方法範圍

本總庫整理了 repo 中可明確區分的武器／敘事路線：planted-cylinder 側柄；sphere-cylinder 候選後由外端接柄；T-Hammer H0/H1/H2/H3；雙 T-Hammer 端面互撞；CYLINDER_CROSS 圓端蓋互撞及稠密候選；線形棒 90° 正控制與反向負控制；T-Hammer 正／反接觸對照；多向扁平面圓頭；單圖多視角／蓄力矩陣；十種獨立洗圖構圖；真實電影六幕與可愛 INS 六幕；10 秒單場景物理短片；五關鍵幀 closed loop；固定錨點 planted-cylinder 片段；以及三分鐘 MV 的分鏡剪輯路線。

歷史 branch 的每一個 ZIP／二進位輸出並未全部解壓逐張重建。這份文件的「完整」意指上述明確分辨的方法都各有可複製 Prompt，不代表每個歷史圖像已成功生成或通過像素審核。

**最重要的用法：一個 Prompt 只描述一種拓撲與一種主要事件。IMAGE 說清楚畫面要長什麼樣；VIDEO 說清楚狀態怎樣隨時間改變。實際生成結果仍要看圖、看幀、看接觸，不可只因 Prompt 寫對就判成功。**
