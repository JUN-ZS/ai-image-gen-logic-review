# 人物 SCAN-CROP / 描邊裁切 → 貼回（消疊影）· **LOCKED**

> **狀態：LOCKED · 2026-10-25**  
> 問題：人物在 **反覆 img2img / multi-REF** 後出現**疊影、重影、ghost、噪邊**。  
> 解法：**L0 clean 一出就 CROP／描人**，之後全程只用呢批 cutout 做 L2 PASTE。

---

## 0. 硬規則（鎖死）

```text
1. 必須在 CLEAN 鏈完成後、進 Step C 之前（或 C 之後立刻），對 PRE／MID／POST
   各做一次 extract——「一開始就描」，唔好等鬼影先救。
2. cutout 只來自對應 clean 幀（同幀對貼），禁止用 PRE 人貼 POST。
3. 邊緣必須 refine：去白底、去毛刺、輕羽化、去白邊污染——目標「無疊影、無噪邊」。
4. L2 PASTE 只用這批 cutouts_clean，禁止從 HUD_GEN 再描人。
5. PASTE 後禁止整圖 img2img。
```

---

## 1. 管線（更新）

```text
L0 CLEAN  PRE → MID → POST（無字）
    ↓ 立刻
CUT_PRE  = extract(PRE_clean,  woman+hammer；唔包球)
CUT_MID  = extract(MID_clean,  woman+hammer；唔包球)
CUT_POST = extract(POST_clean, woman+hammer；碎裂幀可保附着 VFX，但要修 alpha）
    ↓ refine_alpha（見 §2）
cutouts_clean/*.png
    ↓ 之後
L1 HUD_GEN（可鬼影）
L2 PASTE = alpha_composite(HUD_GEN, soft_edge(CUT_same_frame))
L3 TYPE  叠最上
```

### 為何一開始就描

| 舊做法 | 新鎖 |
|--------|------|
| 等 HUD 鬼影先 extract | **L0 定稿即 extract 存檔** |
| 每次救火重描 | **一 SET 三幀 cutout 固定資產** |
| 從 HUD 描人 | **只從 clean 描** |

---

## 2. 邊緣 refine（鎖死參數意圖）

```text
1. 白底 → alpha 0（含近白 fringe）
2. MinFilter(3) → MaxFilter(3~5) → MinFilter(3)  去毛刺、閉合小缺口
3. GaussianBlur(0.5~0.8) 輕羽化——禁止大 blur（會疊影暈邊）
4. 半透明邊緣去白污染：高亮度 fringe 壓暗 RGB
5. alpha < 閾 → RGB 清 0
6. 禁止過狠 erode（會穿面／穿斗篷）
7. POST：可保附着碎裂光；遠飄純噪可清；穿洞要 fill 回
```

QA：棋盤格預覽（checker）睇邊；有雙邊／毛刺 → 重 refine，唔好帶病 PASTE。

---

## 3. extract subject 用語

| 幀 | subject 建議 |
|----|----------------|
| PRE | woman and T-hammer only, not the floating sphere |
| MID | woman and T-hammer only, not the sphere |
| POST | woman holding the metal hammer（附着碎裂可接受；再 refine） |

---

## 4. 與 LOCKED_PIPELINE

- 本檔 = **Step D 專則** + **L0 末強制 cutout 資產化**  
- 主序見 `LOCKED_PIPELINE.md`  
- SET-L 示範：`setL_copper/cutouts_clean/`

---

## 5. 下一 AI 口令

```text
After CLEAN PRE/MID/POST: immediately extract_subject each frame →
refine alpha (no ghost, no noisy rim) → save cutouts_clean.
L2 PASTE only from those cutouts onto HUD_GEN. Never re-extract from HUD.
```

---

## 6. 切層兼下一幀 REF（防糊 · 2026-10-25 補鎖）

```text
PRE_clean → extract CUT_PRE
PRE: HUD(PRE) → PASTE CUT_PRE
MID_clean = ref(PRE_clean + CUT_PRE as sharp identity)   # 唔單靠 img2img 上一幀
MID → extract CUT_MID → HUD → PASTE CUT_MID
POST_clean = ref(MID_clean + CUT_MID)
POST → extract CUT_POST → HUD → PASTE CUT_POST
```

- 切層用途雙重：**貼回有字圖** + **REF 下一 clean**（臉／斗篷／槌清晰，減少糊化）
- 根人示範：PRE clean `3987dba4…`
