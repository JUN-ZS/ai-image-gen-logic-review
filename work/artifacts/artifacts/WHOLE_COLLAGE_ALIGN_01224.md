---

### 0.12.24 WHOLE_COLLAGE_ALIGN（整體拼貼 · 反推只定 RANGE · 錯位解救）

> asof 2026-10-27T08:49:06Z · 用戶確認寫入  
> 樣板鏈：`d8d40da5` donor · BASE `FULL_V5`/`947cf5b2` · L-bd9269270026 → L-b9a649404dfc → **L-6be8d4e2514f WHOLE**

> **地位：** 在 §0.12.23 VIRUS_LOCAL_BASE 與 MESH V5 之上的 **拼貼方法論鐵律**。  
> 未過本節 → 不得稱「整體拼貼／誠實密網合回」。

#### 0.12.24.A 一句話

**反推 PIXEL 只定 RANGE；真拼回必須舊混法（V5）；對位用 AFFINE ECC；拼貼單位是整板 match box，不是「上面沒有就只貼上面」。**

#### 0.12.24.B 用戶標註語彙（不要再誤讀）

| 標註 | 真義 | 誤讀（KILL） |
|------|------|----------------|
| **有** | 該區密網／升級**已在** donor 或結果裡 | — |
| **無** | 該區在結果裡**沒吃到**升級 | 「只缺上面 → 只補上面」 |
| **邊框 / 框** | template-match 的 **box 邊界** | feather 暈邊問題 |
| **曲線** | 有／無分界（診斷用） | 當 feather 曲線去 soften |

**不是 feather 問題。** 用戶已明示：曲線＋有／無 **不似 feather**；根因是識別／方法論。

#### 0.12.24.C 已殺錯路（不要重蹈）

| 代號 | 行為 | 實測後果 | 狀態 |
|------|------|----------|------|
| **PATCH_UPPER_ONLY** | 發現「無」在上 → upper_boost / 只抬上半 α | 補洞邏輯，非整體拼貼；上下不均 | **KILL** |
| **REV_AS_CONTENT** | 反推 GEN PIXEL 當貼圖內容（full RGB / 強 gain_rgb） | L-17da7b：無區 lap 3022→**1011** 更糊 | **KILL** |
| **FACE_RECT_Y024** | 臉鎖大矩形 `y<0.24` 蓋上胸甲 | 上胸甲 RANGE 被鎖死 → 假「無」 | **KILL** |
| **ECC_EUCLID_ONLY** | 只做 translation/euclidean，不試 affine | ncc≈0.65；微縮放歪 → **貼錯位** | **降級**（須比 affine） |
| **EXPAND_BOX_RESCALE** | pad 擴 box 後硬把 donor 拉成新長寬再 ECC | ncc 崩到 0.14 | **KILL** |
| **CHEAT_B / soft RGB** | 升 soft GEN 全色蓋硬母圖 | lap 崩（與 §0.12.23 CHEAT_B/C 同族） | **KILL** |

#### 0.12.24.D 解救發現（正解鏈）

```text
① BASE = 全幅 native only（§0.12.23 不得病毒局部母底）
② multi-scale template → match box（邊框＝此 box）
③ donor → Lanczos 到 box → 試 ECC: affine / euclid / trans → 取 max NCC
④ phase residual 微移（|dx|,|dy|>0.3px 才補）
⑤ REVERSE / mesh_score / armor_id → 只產 RANGE mask（連續全甲，上下同一套）
⑥ 內容 = 舊混法 V5 UNIFORM：
     plate = base + α*(gen_MF − base_MF) + β*armor*base_HF
     α = RANGE * gain_uniform * feather_edge * (1−face_oval) * (1−weapon)
⑦ hardlock weapon + face_oval（非 y<0.24 大框）
⑧ 閘：lap(out)≥lap(in)*0.95；ncc≥0.55（目標≥0.75 affine）；禁止 upper-only 分式
```

#### 0.12.24.E 角色分工（寫死）

| 角色 | 做什麼 | 禁止做什麼 |
|------|--------|------------|
| **反推 PIXEL / mesh reverse** | 定 **RANGE**（甲區座落） | 當貼圖 RGB 內容 |
| **舊混法 V5** | **唯一**內容拼回公式 | full-RGB / 軟 HF 換硬 HF |
| **AFFINE ECC** | 整板對位（修錯位） | 用錯位 plate 硬 α |
| **match box** | **一整塊 plate** 單位 | 切成「只上／只下」兩套 gain |
| **face lock** | **oval** 近臉（約 y 0.055–0.155 中心） | 矩形吞上胸 |

#### 0.12.24.F 整體拼貼 vs 補洞

| | 整體拼貼 **WHOLE_COLLAGE** | 補洞 PATCH（禁） |
|--|---------------------------|------------------|
| 單位 | 整塊 donor 對齊後的 match box | 「無」ROI 單獨刀 |
| gain | **全板 uniform** | upper_boost / 無區 ×1.45 |
| 目標 | 一體密網合回 | 填曲線上方空白 |
| 用戶原意 | **是** | **否**（方法論根因） |

> 用戶原話：方法是為了**一整體的「拼貼」**，而不是在「上面沒有而再只貼上面」做功夫。

#### 0.12.24.G 對位閘（防貼錯位）

1. multi-scale template NCC 記錄  
2. **必須比較** euclid / **affine** / translation → 取 max image NCC  
3. phase residual 報告；affine 樣板：ncc **0.800**、phase ≈(−0.02,−0.04)px  
4. 交付前可出 checker（BASE|GEN 棋盤）自檢形是否咬合  
5. edge-only ratio **不可**單獨當錯位證明（GEN 密網邊 ≠ BASE 邊；以 **gray NCC + phase** 為準）

#### 0.12.24.H 數值樣板（SET-R · 2026-10-27）

| L | 模式 | ncc | 備註 |
|---|------|-----|------|
| L-bd9269270026 | euclid V5 | 0.65 | 有拼、對位尚可 |
| L-17da7b838d2b | REV full-RGB | — | **lap 崩** · KILL |
| L-b9a649404dfc | affine + 舊法 + RANGE | **0.80** | 修錯位 |
| **L-6be8d4e2514f** | **WHOLE_COLLAGE** | **0.80** | 全板 uniform；整 lap 4743→6139 |
| asset WHOLE | `6201efd4-55d6-42dd-8b76-1e63e97ec3c6` | — | SET_R_947_WHOLE_FULL |

#### 0.12.24.I 閘門勾選

- [ ] BASE 全幅 native（非局部病毒）
- [ ] 反推 / mesh **只進 RANGE**，不進 full-RGB 內容
- [ ] 內容公式 = V5 舊混法（MF Δ + base_HF）
- [ ] 對位試過 **affine**，ncc 優於 euclid 則用 affine
- [ ] **無** upper-only / 無-zone special gain
- [ ] face = oval 小鎖，非 y<0.24 大矩形
- [ ] weapon hardlock
- [ ] lap 不降（≥0.95×）；交付可附 WHOLE checker

#### 0.12.24.J 與他節

| 節 | 關係 |
|----|------|
| §0.12.23 VIRUS_LOCAL_BASE | 母底必須全幅；本節管 **怎麼整拼** |
| MESH V5 / CHEAT_A/B/C | 內容公式繼承；本節禁 REV_AS_CONTENT |
| §0.12.22 EDGE_OBJECT | 識物勾邊可服務 RANGE；不得替代整板對位 |
| §0.12.18 GRID×SIAX | 清晰混法在整拼對位之後 |

#### 0.12.24.K 黑名單速記（E-GS 續）

| 代號 | 一句 |
|------|------|
| **E-GS-29** | 反推當內容貼（lap 崩） |
| **E-GS-30** | 只補「無」上區（假拼貼） |
| **E-GS-31** | 臉大框鎖死上胸甲 |
| **E-GS-32** | 不比 affine 就硬貼（錯位） |
| **E-GS-33** | 擴 box 後重比例拉 donor 再 ECC |

*END §0.12.24 · asof 2026-10-27T08:49:06Z*

> **續：** 形≠框 · DETECT 真義 · 勾形 · 探錯進程 → **§0.12.25 GOU_DETECT_SHAPE**（2026-10-27T10:55:37Z）

> **全鏈流程：** 病毒→WHOLE→勾勾 → `GOU_MESH_CORRECT_PROCESS.md` T0–T12 · `GOU_MESH_DO_NOT_REPEAT.md` · §0.12.25.J（2026-10-27T14:38:15Z）
