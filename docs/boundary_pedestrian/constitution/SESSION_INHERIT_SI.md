# 下一 AI 繼承包 · SESSION_INHERIT / 場慣性

> **asof 2026-11-01T13:06:55Z** · **正名：場繼承 / Session Inherit** · 短碼 **SI**  
> **用途：** 下一任 Grok／AI **一開場先讀本檔**，即可接上與用戶的長線「技能憲 + 圖工 + 試錯」慣性，而不是從零聊天。  
> **母倉：** `JUN-ZS/ai-image-gen-logic-review`  
> **完整技能樹分支（2026-11-01）：** `docs/constitution-skills-ssbtz-20261101` @ `2a8a31eebe43`  
> **`main` 現況：** 只有 ~31 份舊憲 · **不含** SSBT-Z／GNP／NCPG／PBI 等新招 → **下一 AI 必須 checkout 上述分支或工位 artifacts，不可只拉 main。**

---

## 0. 開場 30 秒清單（必做）

1. 讀本檔全文  
2. 讀 `docs/boundary_pedestrian/constitution/MSR_GOU_SKILL_INVENTORY_01238.md`（技能總表）  
3. 讀最新 headline 招：  
   - `SHENGSHENG_BUTIE_ZHEN_SSBTZ_01258.md`（**生生補貼真 SSBT-Z**）  
   - `PREVENT_BLUE_INJECTION_PBI_01255.md`  
   - `NESTED_CONTEXT_PEEP_GENERATION_01253.md` + R4  
   - `ONE_BY_ONE_ACCUMULATE_OBA_01244.md`（一人累貼）  
4. 掃 `*_DO_NOT_REPEAT.md` / `trial_notes/` —— **失敗先於發明**  
5. 確認當前專案：`SETS/PROJ_R5_SILVER_ARMOR_2394/`（銀甲／網紋女人）  
6. **問用戶下一刀**前，用一句覆述「現在場在哪、開／未開」

**工位檔（若在 Grok sandbox）：** `/workspace/artifacts/` 同名 md 往往比 main 新。

---

## 1. 用戶是誰 · 說話慣性

| 項 | 實際 |
|----|------|
| 語言 | **粵語／書面夾雜** · 短指令 · 常「GO」「下一刀」「入憲」「貼」「試」 |
| 目標 | **可重跑、可入憲、可驗收**的圖工技能，不是一次性美圖 |
| 價值 | **誠實閘** > 漂亮數字 · 假 PASS 會被拆 |
| 命名 | 用戶給正名（中文）→ 你補短碼／§號 · 例：`生生補貼真` = **SSBT-Z** |
| 入憲格式 | **NAME + 正文(§) + DO_NOT_REPEAT + PROCESS** · 錯成入 FAIL 表 |
| 禁 | 只改 JSON 宣告 PASS · 毒板當母 · 縮掉 HF 當「完成」· batch 無 STEP |

**用戶常說的元指令：**

| 句 | 意思 |
|----|------|
| `入憲` | 寫死技能名／鐵律／黑名單，push 可追 |
| `GO` / `下一刀` | 立刻執行，少廢話 |
| `貼` / `出LOG` | 交付路徑 + 數字 + 圖 |
| `有毒` / `解毒` | 重跑前先對照 DO_NOT_REPEAT |
| `格人脫鉤` | 黃 GRID 格號=座標 ≠ 人 ID |
| `不用補位,就生成` | 轉 **SSBT-Z**（整身 GEN · 禁 peep 填） |
| `MERGE DOCS` 等 | 明確才合 main · 預設 **merge main: NO** |

---

## 2. 核心世界觀（不要推翻）

### 2.1 憲在先 · 圖在後

- 技能是 **可命名、可閘、可禁** 的操作單元  
- 每次長線試錯 → **FAIL 備註 → 入憲**，不是散落 chat  
- 樣板路徑常在 `SETS/...` · 合法樣才 LOCK

### 2.2 解析度階層（血教訓）

```
原圖 FULL（例 1792）
  → PEEP1 / board ×2
  → PEEP2 child ×4 級
  → 更高子板 ×8 …
```

- **Virtual Master（VM）**：全局座標底板 + **原生子板註冊**（不縮回舊 Master 殺 HF）  
- **禁止：** 1024 細節縮回 512 當「高清完成」  
- **OOM：** 全圖×多角度×float 堆 → STREAM tile · 一 peep 一 job · child PNG 當慢速 RAM

### 2.3 生成 vs 貼 vs 洗

| 模式 | 何時 |
|------|------|
| **貼／peep 補**（舊 SSBT / NCPG） | 要鎖母姿、局部升清、可拒收 tile |
| **整身 GEN**（**SSBT-Z**） | 用戶說「不用補位就生成」· 拓撲與紋一齊重生 |
| **PBI luma-only residual** | 銀／金屬網 **防藍噪注入** · 非事後洗藍冒充 PASS |
| **GNP 層層新像素** | 新細節要過母拓撲閘 · 禁 DoG/USM 假清當 GNP |

### 2.4 驗收哲學

- **結構閘**（SN / topology / ECC）與 **HF 閘**（tenen / ridge / align）**拆開**  
- **G7 藍** 與 **G8 黑** 拆開 · 藍過≠可收  
- **THIS_RUN 圖** 必須與 runner／ACCEPT／SHA **同 commit**  
- 數字漂亮但圖爛 → **FAIL** · 用戶會追「不出圖怎知改到」

---

## 3. 技能地圖（按「討論延續」優先序）

### A. 2026-10 底～11 頭 · Headline 線

| 正名 | 碼 | § | 一句 | 下一 AI 何時用 |
|------|-----|---|------|----------------|
| **生生補貼真** | **SSBT-Z** | 0.12.58 | 母姿 LP→整身 GEN→可選紋鎖·**禁 peep 填貼** | 用戶要「新邏輯只生成」全身 |
| 生生補貼 | SSBT | 0.12.56 | 生₁GEN→生₂補紋→貼 PBI+S1S2 | 仍要 peep 補時（父招） |
| 防藍注入 | **PBI** | 0.12.55 | 升清只許 Y residual · C(LP)×Y | 銀網／金屬 4× 必開 |
| Nested Context PEEP | NCPG | 0.12.53–54 | 層層 peep+脈絡+VM 座標 | 局部再清、要保母姿 |
| SPM-A 8× 註冊 | NCPG-R5 | 0.12.55 | 1024 子板 scale=2 註 8× · 禁縮回 4× 冒充 | 子板交付 |
| 新生像素 | **GNP** | 0.12.52 | 可信新 HF · 非銳化 | 要「真新絲」時 |
| 絲／孔保護 | **S1S2** | 0.12.57 | wire/cell 不同 max_drop | 黑點 G8 歸因後 |
| 解毒化衣 | DETOX | 0.12.51 | 失敗鏈→成功換衣公式 | 衣 donor 中毒 |
| 四技絕招 | TEX4 | 0.12.50 | 影分身合×虛形×殘相×P_G | 錯順紋／金線衣 |
| 一人累貼 | **OBA** | 0.12.44 | 一次一件·REF 同姿·線對看 | 多機／重疊大戰母圖 |
| 殘相轉生 | RRT | 0.12.46 | 1→2→3→**只貼 1A** | 被擋肢體 |
| 升紋金字塔 | SWP | 0.12.43 | 層層升·倒序貼回 | densify 保 PIXEL |

### B. 較早但仍有效

MSR 宏圖總程 · GOU 密網 · S1HL 一升混鎖 · ZYF 正衣 · ETZ · FUB+Z · IPSD · 黃 GRID 格人脫鉤 · 格號≠人（E-OBA-02/14）

### C. 讀檔順序（探討新技能時）

```
NAME.md → 正文 § → DO_NOT_REPEAT → PROCESS → trial_notes/LOG
→ 對照 MSI 總表是否已掛索引
→ 若新招：正名+短碼+§+黑名單+樣板路徑 再入憲
```

---

## 4. 當前主場 · PROJ_R5_SILVER_ARMOR_2394

| 項 | 值 |
|----|-----|
| 題材 | 金／銀網紋盔甲女人 · 高清衣紋 |
| 根 | `SETS/PROJ_R5_SILVER_ARMOR_2394/` |
| 升清鏈 | r6c NCNN PBI · r7 PEEP2 · R9/R10 藍解毒實驗 |
| 最新方向 | **SSBT-Z 整身 GEN**（`r6c/ssbt_fullgen/`）· 放棄弱 peep 拼 |
| 未收 | R7 align · G8 黑點 · peep 全拼 coverage · main 未合憲 |

### 已知毒／半毒（勿重犯）

| 碼／現象 | 記 |
|----------|-----|
| 全 RGB residual → 藍噪 | 改 **PBI** Y-only |
| soft LP bite 洗掉 donor | hard residual / 禁 soft |
| peep 用「金色」≠ 衣形 | semantic garment peep |
| 4× 模型輸出縮 2× 抽 residual | **4× residual 原生子板** |
| DoG/USM 當 L3 GNP | 假清 · 撤銷 |
| 格號當人 scale | E-OBA-02 |
| 母只供 VOID+box · HD 異姿 | 有位無形 E-OBA-24 |
| runner 與 ACCEPT 兩套 | 閉環 FAIL |
| G8 非銀網專屬 mask | 黑點閘失真 |

---

## 5. 與用戶一起「繼續探討技能」的標準節奏

```
1) 用戶一句需求 / 一張 ref
2) 你：對表（哪個既有招）· 一句「用 X 招 / 或要新招」
3) 若新：先命名草稿 → 用戶確認正名 → 入憲骨架
4) 小樣 1 刀（可 FAIL）→ LOG + 圖
5) 對 DO_NOT_REPEAT 更新
6) 過閘才 LOCK 樣板；不過就歸因（像 G8 歸因）再刀
7) 長線結束：索引 MSI + push docs 分支
```

**探討時你要主動：**

- 拆「工程閉環」vs「圖像驗收」（用戶已反覆打這點）  
- 拆「轉移紋理」vs「真生成微纖維」  
- 問清：要 **貼回母姿** 還是 **整身重生**（SSBT vs SSBT-Z）  
- 不準用「Tenen 升了」代替「紋對了／藍沒了／絲沒斷」

---

## 6. Git / 繼承實操

| 目標 | 命令／位置 |
|------|------------|
| 拉全技能 | `git fetch && git checkout docs/constitution-skills-ssbtz-20261101` |
| 憲根 | `docs/boundary_pedestrian/constitution/` |
| 試錯 | `.../constitution/trial_notes/` |
| 樣卡 | `work/artifacts/SETS/PROJ_R5_SILVER_ARMOR_2394/r6c/ssbt_*` |
| main | **不完整** · 合 PR 前勿宣稱 main 可繼承 |
| PBI 產物另支 | `feat/r6c-ncnn-pbi-luma`（圖+runner · 與 docs 分支分開） |

**下一 AI 自檢：**

```bash
test -f docs/boundary_pedestrian/constitution/SHENGSHENG_BUTIE_ZHEN_SSBTZ_01258.md && echo SI_OK
```

若 404 → 你在錯分支。

---

## 7. 開場回覆模板（給下一 AI）

> 已讀 **SESSION_INHERIT**。場在 **PROJ_R5 銀網甲**；headline 招 **SSBT-Z**（整身 GEN）與 **PBI**（防藍）；`main` 未合全憲，技能在 **`docs/constitution-skills-ssbtz-20261101`**。  
> 未收：G8 黑、R7 align、peep 弱拼。  
> 請下：**繼續哪條（SSBT-Z／PBI／NCPG／OBA／新招）？**

---

## 8. 禁（繼承級）

| ID | 禁 |
|----|-----|
| E-SI-01 | 只讀 main 就說「技能已齊」 |
| E-SI-02 | 無 DO_NOT_REPEAT 就重跑已毒路徑 |
| E-SI-03 | 用報告 PASS 代替 THIS_RUN 圖 |
| E-SI-04 | 把 peep 補與 SSBT-Z 混成同一招 |
| E-SI-05 | 為過閘調低 G7/G8 門檻 |
| E-SI-06 | 長文灌用戶（OIDV）· 跳層 MSR |

---

## 9. 檔案角色

| 檔 | 角色 |
|----|------|
| **本檔 SESSION_INHERIT** | **對話+慣性+如何繼續** |
| MSI §0.12.38 | 技能總索引 |
| 各 NAME/§/DO_NOT | 單招真理 |
| trial_notes | 本專案數字與毒史 |
| BOUNDARY_WALKER_UNIFIED_RULES | 操作總憲 |

**一句：**  
下一 AI 要完美繼承 → **SI 開場 + MSI 索引 + 分支全憲 + DO_NOT 先於發明 + 問清貼或整身 GEN**。

---

## 10. meta

| | |
|--|--|
| LOCK | 繼承包 · 隨 headline 招更新 asof |
| merge_main | 隨 docs PR · 預設 NO 直至用戶 MERGE DOCS |
| 相關 | SSBT-Z 01258 · PBI · NCPG · OBA · MSI |


---

## 11. 圖檔 primary 薄索引（B）

| 檔 | 用途 |
|----|------|
| `PROJ_R5_PRIMARY_MANIFEST.md` | 本專案 primary path + bytes + sha256 + role（無大圖） |
| `PROJ_R5_PRIMARY_MANIFEST.json` | 機器可讀同內容 |
| 工位副本 | `SETS/PROJ_R5_SILVER_ARMOR_2394/PROJ_R5_PRIMARY_MANIFEST.md` |

> 全量 742 張不做索引。新 Canvas：SI → 本 manifest → 按 path 回 artifacts 讀像素。
