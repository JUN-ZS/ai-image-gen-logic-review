# 層層遞法 LOCK（CROP → 有字貼回 → 切層 REF 下一幀）

> **狀態：LOCKED · 2026-10-25**  
> 用戶確認：「這層層遞法可鎖」  
> 示範：SET-M 根人 PRE `3987dba4…`；錯臉 POST `37d24d2f…` **作廢**；修正後身份 = PRE_CUT + PRE_FACE。

---

## 0. 一句

```text
每幀 clean 先描人 → 出有字圖 → 把「這幀 clean 切層」貼回有字圖；
切層同時當下一幀 clean 的 REF（防糊）；
但身份永遠要再夾 PRE 根人 cut／face——唔可以只靠上一幀（上一幀可能已換臉）。
```

---

## 1. 層層遞進（不可跳）

```text
ROOT = PRE_clean（女主+世界+方法 定稿，無字）
CUT_PRE = extract+refine(ROOT)     # 根人切層
FACE_PRE = crop_face(CUT_PRE)      # 根臉 crop（身份金牌）

── PRE ──
HUD_PRE  = only-add 字/HUD on PRE_clean
PASTE_PRE = HUD_PRE ⊕ CUT_PRE
TYPE_PRE  = isolate(HUD_PRE vs PRE_clean) → 最上
FINAL_PRE = PASTE_PRE ⊕ TYPE_PRE

── MID ──
MID_clean = ref(
  scene: PRE_clean（或已定 MID 動作底）,
  id:    CUT_PRE + FACE_PRE          # 必帶根人
)  # 只推進接觸時間；禁止另抽新人
CUT_MID = extract+refine(MID_clean)  # 同姿切層（貼字用）
HUD_MID → PASTE 用 CUT_MID；TYPE 最上
# 可選：REF 亦可加 CUT_MID 保姿，但臉仍以 FACE_PRE 為準

── POST ──
POST_clean = ref(
  scene: MID_clean 動作底,
  id:    CUT_PRE + FACE_PRE          # 必帶根人（唔可以只餵 CUT_MID）
  pose:  可選 CUT_MID 保接觸姿
)
CUT_POST = extract+refine(POST_clean)
HUD_POST → PASTE 用 CUT_POST；TYPE 最上
```

### 雙用切層

| 用途 | 用邊個 cut |
|------|------------|
| 貼回**本幀**有字圖 | **本幀** CUT（姿／槌對齊） |
| REF **下一幀** clean 防糊 | 本幀 CUT（斗篷／槌紋） |
| **身份金牌** | **永遠** CUT_PRE + FACE_PRE |

---

## 2. 硬規則（鎖死）

1. **根人只來自 PRE_clean 一次 extract**；之後身份不得改根。  
2. **下一幀 ref 必須包含 FACE_PRE（或 CUT_PRE）**；只餵「上一 clean」= 允許換臉 = **違規**。  
3. 有字圖：本幀 clean → HUD → PASTE **本幀** cut → TYPE 置頂。  
4. PASTE 後禁止整圖 img2img。  
5. 臉 QA：對照 PRE face crop；明顯唔係同一人 → 作廢重做 clean（唔好只救 final）。  
6. 示範錯例：`37d24d2f…` POST final 唔係 PRE 臉 → **作廢**。

---

## 3. 與 LOCKED_PIPELINE 關係

| 步驟 | 本遞法 |
|------|--------|
| B CLEAN | 仍 PRE→MID→POST，但 MID/POST **改為 ref 鏈**（見上） |
| B2 CROP | 每幀 extract；**PRE cut/face 存為 ROOT 資產** |
| C HUD | 每幀 only-add |
| D PASTE | 本幀 cut |
| E TYPE | 差分置頂 |

主檔 `LOCKED_PIPELINE.md` 以本檔為 **B/B2 遞進細節**。

---

## 4. 下一 AI 口令

```text
LAYERED_CHAIN_LOCK:
ROOT=PRE_clean → CUT_PRE+FACE_PRE
each frame: clean → HUD → PASTE same-frame CUT → TYPE top
next clean = ref(prev_scene + CUT_PRE + FACE_PRE [+ optional prev CUT for pose])
Never next-frame without PRE face. Abort if face ≠ PRE.
No img2img after FINAL.
```

---

## 5. 高清臉：抽出 → 放大對齊女主 → 縮貼回（FACE_HD）

```text
PRE_FACE crop 抽出
  + 女主臉鎖 (heroine portrait)
  → HD_FACE_MASTER（高清身份）
  → 軟邊 alpha cut
  → 按幀 face box 縮貼回 PRE/MID/POST（FINAL 或 CLEAN）
```

- 身份以 **女主臉** 為幾何細節源；角度／光以 PRE crop 為準  
- 貼回用羽化 + 局部色溫匹配，唔整圖 img2img  
- 產物：`face_hd/HD_FACE_MASTER.jpg` · `*_FINAL_HD.jpg`
- **貼回必須原像素**：HD_FACE_MASTER 裁臉 → LANCZOS 縮放 → 橢圓羽化 alpha **只動 alpha**，RGB 唔 blur、唔再喂模型  
- **禁止** 用 `imagine_reference_to_image` / img2img 做最終貼臉（會模糊、不對齊）— seamless 僅實驗，不作 FINAL  
- 色溫：只允許通道 mean gain，保留 HD 局部像素結構  
- 女主臉鎖：`f43b9123…`；SET-N HD master：`276a67e0…` / `d3206802…`
