# 《邊界行人》成圖 LOCKED PIPELINE（已鎖 · 2026-10-25）

> **狀態：LOCKED**  
> 本檔係之後 AI／人工出圖嘅**唯一主流程**。  
> 示範定稿底：SET-J POST 人清晰 PASTE `f9925b2a-b626-4974-b8fe-d9f89a74a22c` 類產物。  
> 分支：`feature/boundary-pedestrian-setg-axis-a-settings`

---

## 0. 一句话

```text
clean 鏈定人景 → 首張有字 HUD → 人從 clean 描貼 → 字從首字圖描貼到「人清晰 PASTE」最上
```

**禁止** paste 後再整圖 img2img。

---

## 1. 層級（由底到面）

| 層 | 名 | 內容 | 來源 |
|----|----|------|------|
| L0 | **CLEAN 鏈** | 人＋場景＋幾何接觸；**無字** | PRE 定稿 → MID←PRE → POST←MID |
| L1 | **首張有字 HUD_GEN** | 箭／HOT／wire／3D 景深字（可鬼影） | only-add on L0；**只做一次** |
| L2 | **人 PASTE** | 清晰人物（+當幀槌） | `extract(L0)` 羽化貼上 L1（或僅作中間） |
| L3 | **字 TYPE_LAYER** | 字／力矢／標註 | **差分描自 L1 vs L0**，貼上 **L2 人清晰底** 最上 |

**定稿畫面 = L2 + L3**（人用清晰 PASTE，字用首字圖層置頂）。

> 用戶已否決「只叠在純 clean」作為主定稿；主定稿底 = **人清晰 PASTE**（例 POST：`f9925b2a…`）。

---

## 2. 逐步工序（不可調序）

### Step A · 世界與女主鎖

1. 新 SET：先出 **WORLD_PLATE**（空場、無字、無武器可）  
2. 女主：**同一 root**（body + face lock，例 `BW_HEROINE_SET_H_V1`）  
3. 本 SET **一種風格／世界材料**（字效跟世界，唔抄死 SET-F 外觀）

### Step B · CLEAN 鏈（幀連）

```text
PRE_clean  = world + heroine + method PRE（無字）
MID_clean  = img2img(**只以 PRE_clean 為底**)，只推進接觸
POST_clean = img2img(**只以 MID_clean 為底**)，只推進碎裂／REACTION
```

- 禁止：三幀各自從 world 重抽  
- 禁止：MID/POST 用 face+world 跳過上一 clean  
- LOOP id：`L-` + SHA12(**MID_clean**)

### Step C · 首張有字（只一次）

對每幀 clean：

```text
HUD_GEN = img2img(clean, only-add ANALYSIS_HUD_PACK + DEPTH_TYPE_PACK)
```

必寫條件包（見 `ANNOTATION_HUD_AND_3D_TYPE.md`）：

- 方向箭／力矢／reticle  
- HOT 受擊面  
- 可選 wireframe  
- 3D 景深字（可遮擋）  
- HUB 行：打擊面／受面／GAP／n·v／Crack／METHOD／WORLD（**無 TRY 次數、無 REVIEW PENDING**）

**此圖 = 字嘅唯一「首字圖」來源。**

### Step D · 人 SCAN-CROP → PASTE

```text
cut_person = extract_subject(CLEAN, "woman + hammer；接觸幀唔包球")
PASTE      = soft_alpha_paste(HUD_GEN 或 完成底, cut_person)
```

- 同幀對貼（PRE→PRE）  
- 羽化 1–3px  
- 產物例：POST 人清晰 = 用戶認可之 `f9925b2a…` 類

### Step E · 字 SCAN-CROP → 叠在人清晰 PASTE 最上

```text
TYPE_LAYER = isolate(HUD_GEN vs CLEAN)   # diff + chroma；抑皮膚鬼影
FINAL      = alpha_composite(PASTE, TYPE_LAYER)   # 字最上
```

- 字**必須**來自 **Step C 首字圖**，唔好重新模型拼字做定稿  
- 底**必須**係 **Step D 人清晰 PASTE**，唔好改用純 clean 做主定稿（除非用戶另令）

### Step F · 收工

- 記 SHA-256：clean／HUD_GEN／PASTE／TYPE_LAYER／FINAL  
- 可選 A 軌 SVG sidecar 寫死公式（唔替代 L3 主畫面字）  
- **FINAL 之後：禁止再 img2img**

---

## 3. 決策表（鎖死）

| 情況 | 做法 |
|------|------|
| 幀不連 | 重做 Step B，唔好在 L1 救 |
| 人鬼影 | Step D；唔好再 img2img 臉 |
| 字被人物蓋 | Step E 字置頂 |
| 字無趣／無箭 | 重做 Step C 條件包，再 D→E |
| 要準契約字 | A 軌 SVG sidecar，唔取代 L3 |
| 新 SET | 換世界+方法；**流程不變** |

---

## 4. 與舊檔關係

| 檔 | 角色 |
|----|------|
| **本檔 LOCKED_PIPELINE** | **主鎖** |
| `ANNOTATION_HUD_AND_3D_TYPE.md` | Step C 條件 |
| `CHARACTER_SCAN_CROP_PASTE.md` | Step D |
| `TYPE_SCAN_CROP_PASTE.md` | Step E（底改為 PASTE） |
| `TYPO_DOCTRINE_HUB.md` | 字用法／F=用法非外觀 |
| `CONTINUITY.md` / setI | Step B 教訓 |

`TYPE_SCAN_CROP_PASTE.md` 主定稿句以本檔為準：**FINAL = PASTE + TYPE_LAYER**。

---

## 5. 下一 AI 最短口令

```text
跟 LOCKED_PIPELINE.md：
A world+heroine → B clean PRE→MID→POST → C one HUD_GEN →
D person extract→PASTE → E type isolate from HUD→on PASTE top → stop.
No img2img after FINAL. No TRY count. LOOP=L-SHA12(mid_clean).
```

---

## 6. 變更

| 日 | 內容 |
|----|------|
| 2026-10-25 | 初鎖：L0–L3、定稿底=人清晰 PASTE、字=首字圖置頂 |
