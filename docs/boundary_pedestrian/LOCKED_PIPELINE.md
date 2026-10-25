# 《邊界行人》成圖 LOCKED PIPELINE（已鎖 · 2026-10-25）

> **狀態：LOCKED**  
> 本檔係之後 AI／人工出圖嘅**唯一主流程**。  
> 分支：`feature/boundary-pedestrian-setg-axis-a-settings`

---

## 0. 一句

```text
clean 鏈定人景 →【立刻 CROP 三人切層】→ 首張有字 HUD → 人用 clean 切層 PASTE → 字從首字圖叠最上
```

**禁止** paste 後再整圖 img2img。  
**禁止** 等鬼影先救——**L0 完即描人**。  
**禁止** 將 pose／depth proxy control 當主流程（實驗效果差，已否決）。

**層層遞法**（已鎖）：見 `LAYERED_CHAIN_LOCK.md` —— clean→CROP→有字→PASTE；切層 REF 下一幀；**身份必夾 PRE 根人 cut／face**（不可只靠上一幀）。

---

## 1. 層級（由底到面）

| 層 | 名 | 內容 | 來源 |
|----|----|------|------|
| L0 | **CLEAN 鏈** | 人＋場景＋幾何；**無字** | PRE→MID→POST 幀連 |
| L0b | **CUTOUTS** | 人+槌 RGBA | **extract(L0) 立刻** + alpha refine |
| L1 | **HUD_GEN** | 箭／HOT／3D 字（可鬼影） | only-add on L0；每幀一次 |
| L2 | **人 PASTE** | 清晰人物 | **只用 L0b cutouts** 貼上 L1 |
| L3 | **TYPE_LAYER** | 字／力矢／標 | 差分自 L1 vs L0，贴 **L2 最上** |

**定稿 = L2 + L3**。

---

## 2. 逐步工序（不可調序）

### Step A · 世界與女主鎖
- WORLD_PLATE；女主 body+face **同一 root**；本 SET 一種風格。

### Step B · CLEAN 鏈
```text
PRE_clean  = world + heroine + method PRE（無字）
MID_clean  = img2img(PRE_clean only)  只推進接觸
POST_clean = img2img(MID_clean only)  只推進 REACTION
LOOP = L- + SHA12(MID_clean)
```
禁止三幀各自重抽；禁止跳過上一 clean。

### Step B2 · **立刻 CROP／描人**（新增 · 鎖死）
```text
對 PRE／MID／POST 各：
  raw = imagine_extract_subject(clean, woman+hammer…)
  cut = refine_alpha(raw)   # 無疊影、無噪邊
存 cutouts_clean/{PRE,MID,POST}_CUT.png
```
詳見 `CHARACTER_SCAN_CROP_PASTE.md`。  
**此步係強制**，唔係可選救火。

### Step C · 首張有字（只一次／每幀）
```text
HUD_GEN = img2img(clean, ANALYSIS_HUD_PACK + DEPTH_TYPE_PACK)
```
- 見 `ANNOTATION_HUD_AND_3D_TYPE.md`  
- 無 TRY 次數、無 REVIEW PENDING  
- 若 pose 大漂：可重抽 C 或另標 ENDING alt；**主條 L2 仍用 B2 cutout 對 clean 姿**（漂極大時 FINAL 可改 CLEAN+TYPE，須標明）

### Step D · 人 PASTE
```text
PASTE = alpha_composite(HUD_GEN, cutouts_clean[same_frame])
```
- 只用 B2；禁止從 HUD 再 extract 人

### Step E · 字層置頂
```text
TYPE_LAYER = isolate(HUD_GEN vs CLEAN)
FINAL = alpha_composite(PASTE, TYPE_LAYER)
```

### Step F · 收工
- SHA-256：clean／cut／HUD／PASTE／TYPE／FINAL  
- **FINAL 後禁止 img2img**  
- 可選 SVG sidecar（唔替代 L3）

---

## 3. 決策表（鎖死）

| 情況 | 做法 |
|------|------|
| 幀不連 | 重做 B，唔在 L1 救 |
| 人鬼影 | 確認用咗 B2 cutout PASTE；唔好再 img2img 臉 |
| 噪邊／白邊 | 重跑 B2 refine；棋盤 QA |
| 字被蓋 | E 字置頂 |
| 字無趣／無箭 | 重做 C 條件包，再 D→E |
| pose／depth control | **唔做主流程**（已否決） |
| 準契約字 | SVG sidecar |
| 新 SET | 換世界+方法；**流程不變** |

---

## 4. 與舊檔

| 檔 | 角色 |
|----|------|
| **LOCKED_PIPELINE.md** | **主鎖** |
| CHARACTER_SCAN_CROP_PASTE.md | B2 + D |
| TYPE_SCAN_CROP_PASTE.md | E |
| ANNOTATION_HUD_AND_3D_TYPE.md | C |
| STEP_C_TIGHT_AND_ENDING.md | C 漂位分流（可選） |
| POSE_DEPTH_CONTROL_EXPERIMENT.md | **實驗／否決**，非主流程 |
| TYPO_DOCTRINE_HUB.md | 字用法 |

---

## 5. 下一 AI 最短口令

```text
LOCKED_PIPELINE + LAYERED_CHAIN_LOCK:
A world+heroine → B ROOT=PRE_clean → CUT_PRE+FACE_PRE →
  MID/POST clean = ref(prev_scene + CUT_PRE + FACE_PRE [+ prev CUT pose]) →
  each frame: extract CUT → HUD → PASTE same CUT → TYPE top → stop.
Face must match PRE or abort. No img2img after FINAL. No TRY count.
LOOP=L-SHA12(mid_clean).
```

---

## 6. 變更

| 日 | 內容 |
|----|------|
| 2026-10-25 | 初鎖 L0–L3；定稿=人清晰 PASTE+字置頂 |
| 2026-10-25 | **B2 強制：L0 起即 CROP；refine 無疊影噪邊；否決 pose/depth 主流程** |
| 2026-10-25 | **層層遞法鎖**：CROP→有字貼回；切層 REF 下一幀；身份必帶 PRE face（`LAYERED_CHAIN_LOCK.md`） |
