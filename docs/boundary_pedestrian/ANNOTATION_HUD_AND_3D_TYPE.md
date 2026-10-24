# 分析 HUD／方向指示／受擊高亮／3D 前後融入字 —— 條件還原

> 用戶 REF（2026-10-25）：  
> `a51850bc` · `91cee726` · `30d7e781` · `d969c622`  
> 問題：這些有**指示方向 / 物件 HIGHLIGHT / 3D 字前後融入**，是怎麼條件出來的？之後為什麼沒有了？

---

## 1. 四張各自「有咩」

| asset | 模式 | 關鍵視覺語言 |
|-------|------|--------------|
| **a51850bc** | **物件特寫 + HOT 標註** | 大紅箭咀指向受擊頂；頂面 **emissive HOT 高亮**；左右 HUD 標 `打擊面`/`受面`/`STRIKE`/`RECV`；無角色搶戲 |
| **91cee726** | **俯視力線圖** | 青色 **力矢／對向弧 F↔180°**；接觸 **準星 reticle**；`FACE` 寫在槌面；四角 scan-frame；`n·v` 沿線 |
| **30d7e781** | **全息線框 HIGHLIGHT** | 雙槌 **wireframe / mesh 高亮**；軸線貫球；`打擊面`/`FACE` 貼在 3D 表面；`F↔180° OPPOSE` 豎矢 |
| **d969c622** | **景深 3D 融入字** | 火字 **站在景深裏**（人與字前後關係）；方法刻進 **橫梁幾何**；地面 **FAR→AFTERMATH** 路徑箭；LOOP 像燒在原木 |

三類能力（用戶講嘅）：

1. **指示方向** = 箭咀／力矢／對向弧／地面路徑  
2. **物件 HIGHLIGHT** = HOT 面發光、wireframe、reticle、貼面標籤  
3. **3D 字前後融入** = 字係場景物件（火／木／全息），有遮擋與景深，唔係螢幕貼圖

---

## 2. 當時點樣「條件出來」（可複現配方）

### 2.1 共同前提（有，先有圖）

- **分析／圖解意圖**寫進 prompt（唔只「美圖 + 標題」）  
- 模型軌 **B**：允許把箭咀、線框、HOT 當 VFX 生成  
- 標註字串對齊 HUB：`打擊面` `受面` `STRIKE` `RECV` `n·v` `F↔180°` `GEO.*`

### 2.2 方向指示 · 條件句（要明示）

```text
draw cyan/red force arrows and dimension leaders IN the 3D scene
label F↔180°, n·v along the arrow shafts
ground path arrow FAR → AFTERMATH as diegetic marks
arrowheads point at the actual contact point / face
NOT flat UI icons floating random; vectors locked to geometry axes
```

### 2.3 物件 HIGHLIGHT · 條件句

```text
emissive HOT glow only on the receiving face / crown / end-face
wireframe or holographic mesh overlay ON the hammer volumes
HUD reticle / crosshair exactly at contact point
edge-highlight strike faces; leave non-strike faces dark
side callouts 打擊面=… 受面=… with leader lines to the surface
```

### 2.4 3D 字前後融入 · 條件句

```text
typography as physical objects in world space (fire glyphs, carved beam, holo panels)
parallax: some strokes BEHIND character, some IN FRONT, some ON architecture
method string burned into wood beam / basalt / ice — not a screen sticker
large title has thickness, light wraps, can be occluded by hammer/body
NO solid rectangular subtitle plate; no pure 2D HUD-only title for the hero type
```

### 2.5 構圖條件（四張共通）

| 條件 | 作用 |
|------|------|
| 物件／接觸點居中或可讀 | 箭咀有地方指 |
| 角色可縮小／背影／缺席（圖解格） | 唔同電影主鏡頭搶字 |
| 一種主標註色（紅 HOT / 青全息） | 圖表可讀 |
| 一次只講一個契約（PLANT_O / T2 FACE / H0 PRE-FAR） | 唔塞爆 |

---

## 3. 之後為什麼沒有了（誠實時間線）

| 階段 | 優化目標 | 犧牲 |
|------|----------|------|
| 早期 SET-G 圖解格 | **契約可讀**、力線、HOT、wireframe | 敘事電影感 |
| 轉「RICH 藝術字／入場」 | 火字、海報感、1/3 字場 | 箭咀／線框／貼面標變少 |
| **女主鎖 + 幀連 clean 鏈** | 身份連續 PRE→MID→POST | 唔敢大改成圖解 HUD |
| **SVG 疊字** | 字形準、底像素 100% 不變 | **純螢幕空間 2D** → 無真 3D 遮擋、無力矢、無 wireframe |
| 「只加字」模型 | 標題書法 | prompt **沒要求** arrows / HOT face / mesh / beam-carved type |

**一句**：**唔係能力消失，係管線目標換咗**——由「圖解契約」轉「連貫敘事 + 準字／火字」，配方裏刪咗方向／高亮／景深字條件。

---

## 4. 兼顧：三層成品（建議鎖入 HUB）

```text
L0  clean 鏈        幀連 + 幾何 + 女主
L1  敘事字 B/A      境界行人 火字／準字（入場）
L2  分析圖解層      箭咀 + HOT + wireframe + 貼面 STRIKE/RECV
```

- **故事三幀**：L0 + L1（可少 L2）  
- **契約驗收格**：L0（可無女主）+ **L2 為主** + 軸 E 小字  
- **英雄關鍵幀**：L0 + L1 景深 3D 字 + **精簡 L2**（1 箭 + 1 HOT 面 + 2 標）

### 4.1 禁止再犯

- 只寫「加藝術字」→ 唔會出箭咀／HIGHLIGHT  
- 只用 SVG 螢幕疊字 → **出唔到**真 3D 前後遮擋同 wireframe（除非另外畫矢線 SVG，仍缺體積 mesh）  
- 連貫鏈上整圖重抽圖解 → 易斷幀；圖解格應 **獨立槽** 或 **同一 clean 上只加 L2**

---

## 5. 一鍵條件包（之後 prompt 可直接貼）

**ANALYSIS_HUD_PACK**

```text
Diegetic analysis overlay in-world (not a flat app UI):
- HOT emissive highlight on the exact strike/receive face
- one primary direction arrow (or F↔180° pair) locked to contact axis
- optional holographic wireframe on weapon volumes
- reticle at contact point
- callouts 打擊面 / 受面 / STRIKE / RECV / n·v with leaders to real surfaces
- hero title 邊界行人 as 3D world-space type with depth occlusion
- no TRY count, no REVIEW PENDING
```

**DEPTH_TYPE_PACK**（景深字）

```text
Title and method exist as scene objects: fire/basalt/wood/holo with thickness;
character can occlude letters; letters can sit on beams, ground paths, sphere skin.
```

---

## 6. 關聯

- `TYPO_DOCTRINE_HUB.md` — 字用法  
- `HUB_PRESS_ON_IMAGE_PRIORITY.md` — 壓邊啲行  
- 本檔 — **點樣視覺化成箭／高亮／3D 融入**（曾有、後失、可復）
