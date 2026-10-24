# 《邊界行人》字軌憲法 · HUB（TYPO DOCTRINE）

> 狀態：**LOCKED 用法** · 2026-10-25  
> 來源：用戶累積糾正（SET-E/F/G/H/I）+ `USER_REQUIREMENTS_LOCKED.md` §1 + `HUB_PRESS_ON_IMAGE_PRIORITY.md`  
> **本檔上 HUB**：之後所有 AI／人出字先對呢度，再出圖。

---

## 0. 一句話

> **字是世界的物理與契約的可見層**——位置流動、材料跟 SET、內容跟幀、方法名可準可氛圍雙軌；  
> **唔係**角落水印，**唔係**死底板海報，**唔係**抄死某一個舊 SET 的外觀。

---

## 1. 雙軌（必須分清）

| 軌 | 名稱 | 用途 | 字形來源 | 審核 |
|----|------|------|----------|------|
| **A · 準字** | SVG／ASS／manifest typeset | 公式、方法 ID、LOOP、審核、sidecar | **寫死**（文泉驛等）· 模型**不准**拼 | 可當 PASS 依據 |
| **B · 生動** | RICH model 軌 | 入場感、MV、主畫面氛圍 | 模型拼 · **允許漂移** | 氛圍用；方法名以 A 或 manifest 為準 |

- 主畫面可選 B；契約／公式以 A 或 sidecar 為準。  
- **禁止**把 B 軌漂亮錯字當成幾何驗收成功。

---

## 2. 「舊 SET-F 字效 REF」正解（重要）

| ✅ 係 | ❌ 唔係 |
|------|--------|
| SET-F 時期確立的**用法原則** | 硬抄 F 的雨夜霓虹／濕地塗鴉**外觀** |
| 字融入世界、自由位、無底板、一句可大可小 | 每 SET 都長得像 Tokyo rain poster |
| 特效不限（火／霓虹／塗鴉／冰／熔岩…） | 把 F 的圖當 image REF 死套字皮 |
| PRE／POST 同字串、不同風格 | 字場與本 SET 世界無關 |

**創作大師義務**：每個 SET 先發明**本世界材料字效**，再出字。

### 2.1 世界材料字效（示例 · 可擴）

| SET | 世界 | 原生字材料（發明） |
|-----|------|-------------------|
| F | 雨夜都市 | 濕霓虹、地面水漬透視、閃電環（**歷史樣例**，非母版） |
| G | 金箔廢寺 | 箔金浮雕、焦痕、銅綠蝕字 |
| H | 極光冰原 | 冰霜蝕刻、極光描邊、冷青 vapor |
| I | 黑曜火山 | 玄武熔岩浮雕、灰煙字、裂縫熔漿、碎片成字 |

下一個 SET：**禁止**默認「再 REF 一張 F」；要寫 `WORLD_TYPE_MATERIALS` 再生成。

---

## 3. 必守用法（由 SET-F 對話鎖落）

1. 圖裡**必須有字**；藝術感可佔約 **1/3** 畫面。  
2. **無底背色／無 UI 實心底板**（准半透明 glow，不准鎖死色塊牌）。  
3. **位置可流動**：故事名、LOOP、方法、晶片**不 SET 死座標**；每幀可亂走、大小不一。  
4. **一句中字可大可小**。  
5. 特效**不限**：火字、槌身 NEON、地面透視字、冰面字、熔岩字、煙字…  
6. **融入世界** > 貼圖感。  
7. **PRE 一種風格 · POST 極大不同**；字串內容可同，外觀必須跟幀物理。  
8. **嚴禁畫面**：`TRY 次數`、`REVIEW PENDING`。  
9. LOOP = `L-` + **MID 原圖** SHA-256 前 12 hex。  
10. 原圖與有字版**分開存** + SHA-256 manifest。

---

## 4. 字 ↔ 幀物理綁定（HUB 對齊）

字要講**圖入面正在發生的 INFO**，唔係裝飾 slogans。

| 幀 | 時間 | 字氣溫 | 必帶物理晶片（選 2–4） |
|----|------|--------|------------------------|
| **PRE** | t−δt | **冷** | `PRE_NEAR`/`PRE_FAR` · `signed_gap≫0` · `Crack=0` · `F_n→0` · STRIKE pending |
| **MID** | t0 | 臨界 | `FIRST_CONTACT` · `GAP=0` · `n·v=1` · 合法 `END_FACE` · 相關 PASS |
| **POST** | t+δt | **熱** | `REACTION`/`RECOIL` · `Crack≫0 ±δt` · impulse 力鏈 · follow-through |

### 4.1 軸 E 必備（有字成品）

```text
邊界行人｜THE BOUNDARY WALKER
METHOD: GEO.* · <態>
WORLD: <本 SET 世界碼>
L-<SHA12>
```

### 4.2 壓圖優先 12 類（詳見 HUB_PRESS）

ROD± · PLANT_O · 五段相 · E_90/E_face · signed_gap · Crack±δt · reaction impulse · END_FACE≠CHEEK · ZERO-DRIFT · 軸 E 條。

**當幀只出相關晶片**，唔做公式牆。

---

## 5. 生成流程（下一 AI 照做）

```text
1. 讀本檔 + USER_REQUIREMENTS_LOCKED + HUB_PRESS_ON_IMAGE_PRIORITY
2. 定 SET 世界 → 寫 WORLD_TYPE_MATERIALS（本 SET 字用咩物質）
3. 鎖女主 root（有則用）+ 幾何契約（唔偷改接觸）
4. 出 clean PRE|MID|POST（無字）
5. B 軌：按本世界材料發明字場（唔硬 REF 舊 SET 圖外觀）
6. （可選）A 軌：SVG 寫死方法名 / 公式 sidecar
7. LOOP = L-{sha12(MID clean)}；manifest 記 SHA
8. 三圖並排驗：女主連續 · 幀連感 · 字跟物理
```

### 5.1 禁止

- 用舊 SET 標字圖當**外觀母版**硬套  
- 鏡頭／字場偷改接觸幾何  
- 只出單幀無 PRE/MID/POST  
- 模型拼字當幾何驗收  
- 顯示 TRY 次數 / REVIEW PENDING  

---

## 6. SET-I 示範（2026-10-25）

- **世界**：`OBSIDIAN_VOLCANO_NIGHT`  
- **字材料**：玄武熔岩浮雕、裂縫熔漿、灰煙、碎片成字（**非 F 霓虹**）  
- **法**：`GEO.T · H3`  
- **LOOP**：`L-bdc34d8cb667`  
- **女主**：`BW_HEROINE_SET_H_V1`  
- **路徑**：workspace `boundary_pedestrian_setI_obsidian/`  

---

## 7. 關聯檔

| 檔 | 角色 |
|----|------|
| `USER_REQUIREMENTS_LOCKED.md` | 用戶硬規則總表 |
| `HUB_PRESS_ON_IMAGE_PRIORITY.md` | 邊啲 HUB 行值得壓圖 |
| `setH_arctic/TYPESET_PIPELINE.md` | A 軌 SVG 技術筆記 |
| `MASTER_PROMPT_…v5…md` | 公式母版 |
| `bubble_break/boundary_pedestrian_try_art.py` | 早期 SVG／ASS 工具 |

---

## 8. 變更日誌

| 日 | 變更 |
|----|------|
| 2026-10-25 | 初版上 HUB：雙軌、F=用法非外觀、世界材料表、幀物理綁定、SET-I 示範 |
