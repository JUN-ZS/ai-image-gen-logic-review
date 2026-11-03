---
name: shengqing-huiwei
description: 升清回位（SHQ / SC-H）— 高清人物原生像素硬貼回風景槽。person_scale 永遠 1.0；公式對位 COREFIT 優先；放大場景；Imagine region_edit 只刪原人；Virtual Master 不回縮。用在遠/中人換高清人、峰頂換女主、DDXX-AR、PATH1E 全身、A8B 銀甲、不降 PIXEL 拼回、locked donor_xy paste。
metadata:
  type: workflow
  version: "1.2"
  code: SHQ
  alias: SC-H
  zh: 升清回位
  section: "0.13.01"
  write_id: "01263"
  priority_method: SHQ-BEST
  asof: "2026-11-03T06:45+08"
  gold: "PROJ_SHQ_MID_LEVEL_RETURN_V1"
  sample_legacy: "PROJ_R5_SILVER_ARMOR_2394 / DDXX_IMAGINE_DEL_PASTE"
---

# 升清回位（SHQ）v1.2

**一句正典：** 不是把人縮到風景，而是把風景擴到能容納原生的人；**公式對位是主幹**；刪原人用 Imagine 局部；貼新人用鎖位硬貼。

**優先法（SHQ-BEST · 用戶確認「這方法是優先」）：**

```text
中距原景有人（勿極遠）
  → peep 抽姿 + HD 同姿同水平地 plate
  → COREFIT：q = a · (R @ p) + t   （Face+Torso 估 a；腳只鎖 t / 水平）
  → IMAGINE-DEL 只人（峰台保留）
  → Scene × S=1/a · person_scale=1.0
  → HARDPASTE 整數 donor_xy · core bit-exact
  → Virtual Master formal（不回縮）
```

**金牌 ACCEPT：** `PROJ_SHQ_MID_LEVEL_RETURN_V1` · `IMAGINE_DEL_LOCKED_PASTE_OK`

| a | S | donor_xy | VM | core/face |
|---|---|----------|-----|-----------|
| ≈0.39358 | ≈2.511 | (623, 821) | 2552×4520 | **1.0 / 1.0** |

**首成樣板（legacy）：** `DDXX_IMAGINE_DEL_PASTE` · a≈0.28985 · VM 3623×6263 · 用戶「終於對到了」。

Read this before any far/mid-person / high-res donor / landscape re-paste that claims **不降 PIXEL**.


## v1.2 — 強制方法選擇與防失憶執行鎖（新增，優先於舊式自由敘述）

**先選 method_id；不得把兩種公式混成一條，也不得靜默 fallback。**

| method_id | 適用 | 尺度估算 | 其他部位 |
|---|---|---|---|
| `SHQ_BEST_CORE_V1_1` | 單一人物；臉／軀幹清晰，手腳可能姿態不同 | Face+Torso 求 a,R；sole/ground 鎖 t | hands/legs/cape 只作獨立驗證 |
| `DDXX_WHOLEBODY_SIMILARITY_V1` | 全身配對標點可信、遮擋少 | 全部可信語意點做 weighted Umeyama + Huber：q=a(p@R)+t | 逐點殘差與低置信點審核 |
| `DDXX_MECHA_CORE_SIMILARITY_V1` | 一台機甲 SOLO | head/chest/pelvis/左右肩關節作 core fit | 肘腕膝踝、武器軸、盾、翼端及 silhouette 作 pose validation；禁止用岩石連接的 contour 點冒充關節 |
| `SHQ_MULTI_RETURN_V1` | N 個獨立物件回拼 | N 次 SOLO 各自算；最後才共景 | 每個 slot_ratio 必須報告 |

**注意：**
- DDXX 手動 11 點範例 `DDXX_MANUAL_PANEL_GOLD_01` 來自縮圖拼板、人工初標、DONOR 披風亦被裁切。它只用來測 solver 數學實作有否改壞，不是 production pose 閘值。
- V16 U0 的 DDXX solver 確實有跑；問題在自動 silhouette 點把左腳／膝混入碎石，導致 RMSE≈21px、單點可達 123px。這是 ANCHOR SEMANTICS FAIL，不是 solver 未執行。
- `ACCEPT_CORE=true` 若只依據 feet lock≈0.50px，必須作廢；feet lock 只代表 PLACEMENT，不代表 COREFIT／POSE。
- AI detail 若只對 soft GENFIT 作比較，只能通過 `BASE_TO_DETAIL`；仍要另有 `TARGET_TO_BASE` 對原始 TARGET 的姿態驗收。
- V14 的 H-only、W/AR 漂移及 soft-extract 循環認證不得重犯；V15 雖補 H+W 並誠實標 `ACCEPT_FULL_HD=false`，仍不能把 soft-base 對 detail 的相似度當成原景姿態完整通過。

### 每次新 Run 的強制前置

1. 讀本 SKILL、`SHQ_METHOD_REGISTRY.json`、`SHQ_EXECUTION_CONTRACT_V1_2.md`、`SHQ_DO_NOT_REPEAT.md`。
2. 凍結唯一 `run_id` 與 `method_id`。
3. 執行 `python skills/shengqing-huiwei/tools/test_ddxx_golden_regression.py`，產生 regression JSON。
4. 建立 `RUN_STATE.json`，填入 canonical 文件 SHA-256、golden regression report 路徑及單位數。
5. 執行 `python skills/shengqing-huiwei/tools/shq_preflight_guard.py RUN_STATE.json`。Exit code 非 0 即 BLOCK；不准以文字自填 PASS。
6. 每次換 session 讀取同一 RUN_STATE 與 SHA；從最後有檔案證據的 phase 繼續，不憑對話記憶重建結果。

完整狀態機、報告欄位及硬性 BLOCK 條件見 `SHQ_EXECUTION_CONTRACT_V1_2.md`。

## First acts

1. 掃 **E-SHQ / E-SCH** 勿再犯 — 曾犯必拒。
2. **優先走 SHQ-BEST 公式鏈**，不要先 soft fusion / 縮人 / 全圖 Imagine。
3. DONOR = 清身份原生 RGBA；禁毒疊母圖當 sole donor。
4. TARGET 錨點必須落在真實臉/肩/腳（ANCHOR-AUDIT）。
5. 主線 **SHQ**：IMAGINE-DEL → **COREFIT a,R,t** → scene 放大 → HARDPASTE 1.0 → VM formal。
6. 局部臉/甲可走 **PATH1E-F**（同構 peep · ECC≥0.85 · 硬貼）— 不可把單 ECC 直接當全身完成。

## Hard rails（永不放鬆）

1. **person_scale = 1.0 always** for formal identity donor. Scene may scale; person does not.
2. **公式優先**：先 `q = a (R @ p) + t` 鎖 a 與 donor_xy，再貼；禁跳過 COREFIT 糊貼。
3. **Imagine region_edit** 只刪人 — 禁 OpenCV 大 mask 連岩剷。
4. Fit **a,R,t** 主用 **Face+Torso**；禁用 Legs residual 反過來縮人。
5. **HD plate 地平** 與原圖 sole **同水平**（雙腳同線 · GROUND_LOCK）。
6. Paste **integer locked donor_xy**；core α≥0.5 **bit-exact**。
7. Deliver **Virtual Master** full size；formal 不回縮小母圖。
8. **ACCEPT_CORE** ≠ **ACCEPT_FULL**；腳/披風未過不可縮人交差。
9. 錨錯 → `INCONCLUSIVE_ANCHOR_GEOMETRY_INVALID`，不可直接 `REJECT_POSE_MISMATCH`。
10. **中距優先**（人 ≥25–35% 畫高）；極遠 peep 資訊不足時先升 peep 或 PLATE-POSE，勿硬縮人。

**矛盾集：** 鎖死小母圖尺寸 ∧ 大原生人物 ∧ person 1.0 同框 → 必開 VM。

## Canonical pipeline（SHQ-BEST 成功鏈）

```text
① 中距原景有人（sole 水平可讀）
② SHQ-PEEP：完整頭身腳披風 peep
③ SHQ-PLATE：同姿 HD · 雙腳同水平地
④ SHQ-COREFIT / ANTHRO-FIT：Pose JSON → a,R,t（Face+Torso；腳鎖 t）
⑤ SHQ-DEL / IMAGINE-DEL：region_edit 只圈女主+披風 → 空峰台保留
⑥ SHQ-SCENE：warp scene by S=1/a → Virtual Master
⑦ SHQ-LOCKXY / HARDPASTE：donor @ (tx,ty) scale=1.0 · core exact
⑧ SHQ-GROUND：sole_y 鎖岩台水平線
⑨ SHQ-SHA：core_exact / face_exact / SHA
⑩ （可選）SHQ-LS / SOLE-SUPPORT：只補鞋底下岩
⑪ 閘：IMAGINE_DEL_LOCKED_PASTE_OK · ACCEPT_CORE · ACCEPT_FULL 僅當賺到
```

### 金牌鎖（MID_LEVEL_RETURN_V1 · 2026-11-03）

| key | value |
|-----|-------|
| a | ≈0.393581 |
| S / 1/a | ≈2.511 / ≈2.541 |
| rot | ≈−2.18°（可 clamp≈0 保水平） |
| donor_xy | (623, 821) |
| ground_y_scene | ≈903.32 |
| sole_y_vm | 2268 |
| person_scale | 1.0 |
| VM | 2552×4520 |
| core_exact | 1.0 |
| face_exact | 1.0 |
| status | IMAGINE_DEL_LOCKED_PASTE_OK |

### 首成鎖（A8B 峰 · legacy）

| key | value |
|-----|-------|
| a | ≈0.28985 |
| scene_scale | ≈3.450 |
| donor_xy | (1654, 1429) |
| VM | 3623×6263 |
| core_exact | 1.0 |

## 公式（研究終態 · 重點）

### 相似變換（donor → target scene）

    q = a * (R @ p) + t

- **a 只由 Face+Torso（+可肩髖）Robust/Huber 或 Pose face–hip 擬合**
- Hands/Legs **報告殘差但不進 a**
- 腳：`t = feet_t − a · (R @ feet_d)` → **GROUND_LOCK**

### 逆變換（scene → Virtual Master，人 1:1）

    S = 1/a
    v = S · q
    donor 整圖以整數 (tx,ty) 硬貼 · **禁止**對人 resize / 非等向 affine

### 分組殘差

| 組 | 用途 |
|----|------|
| Face | 進 a · ACCEPT_CORE |
| Torso | 進 a · ACCEPT_CORE |
| Hands | 觀察 · 不進 a |
| Legs | 可高 · Local Support / 換同姿 · 不重估 a |

## 子技能

| 碼 | 正名 | 職 |
|----|------|-----|
| **SHQ** | 升清回位 | 主技全鏈 |
| **SHQ-BEST** | 優先法 | 公式+DEL+1.0 硬貼金牌鏈 |
| **DDXX** | 大大小小 | 場景放大·人1:1 概念前身 |
| **DDXX-AR** | 錨定保像素 | person=1.0 · scene 搜 s,t |
| **SHQ-COREFIT** / **ANTHRO-FIT** | 人體公學對位 | landmark a,R,t · 分組殘差 |
| **PATH1E-F** | 臉核硬貼 | ROI→ECC≥0.85→硬貼 |
| **PATH1E-P** | 姿板全身 | plate 後再配準/硬貼 |
| **SHQ-DEL** / **IMAGINE-DEL** | 想像去人 | region_edit 只人 |
| **SHQ-LOCKXY** / **HARDPASTE** | 鎖位硬貼 | core 原像素寫回 |
| **SHQ-VM** / **VM-LOCK** | 虛擬母圖 | formal 不回縮 |
| **SHQ-GROUND** | 地平鎖 | sole 水平對原圖 |
| **SHQ-CLEAN** / **CLEAN-REPASTE** | 空景回貼 | 空山+鎖座標 |
| **SHQ-ANCHOR** / **ANCHOR-AUDIT** | 錨點審計 | 雙邊同法·禁落空 |
| **SHQ-LS** / **SOLE-SUPPORT** | 腳底岩補 | 只補接觸·不動人 |
| **SHQ-PEEP** / **PEEP-ROI** | 窺窗 | 完整頭身腳披風 |
| **SHQ-PLATE** / **PLATE-POSE** | 姿板 | 遠/中姿+HD身份 |

詳表：`references/SUBSKILLS.md` · `SHQ_SUBSKILLS.md`

## 勿再犯

全文：`references/DO_NOT_REPEAT.md` · **E-SHQ-01…35**

口訣：**公式先；人永遠 1.0；山可放大；刪人只圈人；地平要齊；貼回要 exact；錨錯先修錨。**

## 試錯時間線

`references/TRIAL_TIMELINE.md` · 敗→成：OpenCV 大剷 → Imagine-DEL；縮人 → VM；單 ECC 全身 → ANTHRO+鎖位硬貼；極遠 peep → 中距+GROUND_LOCK。

## 證據

- gold formal：`SETS/PROJ_SHQ_MID_LEVEL_RETURN_V1/SHQ_RUN/04_VIRTUAL_MASTER.png`
- gold REPORT：同目錄 `REPORT.json`
- legacy formal：`…/DDXX_IMAGINE_DEL_PASTE/02_VIRTUAL_MASTER.png`
- 登記：`references/REGISTRY.json` · write **01263**

## Do not confuse

| 名稱 | 是升清回位拼回？ |
|------|------------------|
| PBI | 否 · 升清後混頻 |
| Imagine 全圖軟融 | 否 |
| 異構全身只 ECC | 否 · 要 plate/landmarks |
| person resize to slot | **禁** |
| half 預覽 | 非 formal 原 SIZE |
| 跳過公式 peep 糊貼 | **禁** · 非 SHQ-BEST |

## Done / stop

formal = VM 原尺寸 + REPORT（a, donor_xy, core_exact, DEL 方法名, ground lock）。  
禁：half 冒充原 SIZE；GEN 全身當已回位；大剷連岩自稱 IMAGINE-DEL；無 COREFIT 稱完成。
