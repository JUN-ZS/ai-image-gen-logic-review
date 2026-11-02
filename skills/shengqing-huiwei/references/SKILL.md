---
name: shengqing-huiwei
description: 升清回位（SHQ / SC-H）— 高清人物原生像素硬貼回風景槽。**優先法 = 公式對位 COREFIT（Face+Torso a,R,t）+ Imagine-DEL + person_scale=1.0 鎖位硬貼 + VM 不回縮 + 地面水平鎖**。用在遠/中人換高清人、峰頂換女主、DDXX-AR、PATH1E、A8B、不降 PIXEL。
metadata:
  type: workflow
  version: "1.1"
  code: SHQ
  alias: SC-H
  zh: 升清回位
  section: "0.13.01"
  asof: "2026-11-03T06:40+08"
  priority_method: "IMAGINE_DEL_LOCKED_PASTE + SHQ-COREFIT"
  gold_sample: "PROJ_SHQ_MID_LEVEL_RETURN_V1"
  gold_status: "IMAGINE_DEL_LOCKED_PASTE_OK"
---

# 升清回位（SHQ）v1.1

## ★ 優先法（本輪進化 · 必須先走）

> 用戶：「記得這方法是優先啊，這最後的研究出來的**公式對位**是重點」

**正名：** `SHQ-BEST` = **公式對位優先的升清回位**

```text
① 原景：中距人為佳（人高約 25–35% 畫高；太遠 peep 資訊不足）
② peep 抽姿（可 ×3 參考）→ PLATE-POSE 出高清同姿 donor
   · 高清 donor 雙腳必須同一水平地線（= 原景 sole 水平）
③ Pose / ANTHRO JSON：Face+Torso(+肩髖) 估 a,R,t
   · 公式 q = a · (p @ R) + t
   · a 只由 Face+Torso；Hands/Legs 只報告，不進 a
   · 腳標點只鎖平移 / 地面水平，不反過來縮人
④ IMAGINE-DEL：region_edit 只圈人+披風；峰台水平岩面必須保留
⑤ Scene × S（S≈1/a 或 cap）→ Virtual Master 畫布
⑥ HARDPASTE person_scale=1.0 · 整數 donor_xy
   · core α≥0.5 bit-exact · 禁對人 resize / 軟融
⑦ 地面鎖：sole_y 對齊峰台水平線（GROUND_HORIZONTAL_LOCK）
⑧ 閘：IMAGINE_DEL_LOCKED_PASTE_OK · core_exact=1.0 · face_exact=1.0
```

**一句正典：** 不是把人縮到風景，而是用**公式**把風景座標系擴到能容納原生的人；刪原人用 Imagine 局部，貼新人用鎖位硬貼。

### 為何公式對位是重點

| 錯法 | 問題 |
|------|------|
| 只 peep 視覺貼 / 軟 α | 降像素、非 exact |
| 單 ECC 當全身完成 | 異構 peep 崩（E-GS-12 類） |
| 人 resize 遷就槽 | 違 person_scale=1.0 |
| 錨錯仍 REJECT_POSE | 應先 ANCHOR-AUDIT |
| 遠 peep 硬全 inverse S | OOM；應中距 + 可 S_cap |

| 對法 | 作用 |
|------|------|
| **COREFIT Face+Torso → a,R,t** | 尺度/位姿分佈恆定變量 |
| **sole 只鎖 t / 水平** | 地平一致、不污染 a |
| **Imagine-DEL + 硬貼 1.0** | 峰台保留 + core exact |
| **VM formal 不回縮** | 像素主權 |

## 金牌樣板（進化後）

### A · 中距水平地 · 本輪 BEST

| key | value |
|-----|-------|
| SET | **PROJ_SHQ_MID_LEVEL_RETURN_V1** |
| status | **IMAGINE_DEL_LOCKED_PASTE_OK** |
| a | ≈0.39358 |
| S | ≈2.511 |
| donor_xy | (623, 821) |
| person_scale | **1.0** |
| sole_y_vm | 2268（水平鎖） |
| VM | **2552×4520** |
| core_exact | **1.0** |
| face_exact | **1.0** |
| asof | 2026-11-03T06:40+08 |

### B · 峰頂首樣（仍有效）

| key | value |
|-----|-------|
| SET | DDXX_IMAGINE_DEL_PASTE（A8B 峰） |
| a | ≈0.28985 |
| donor_xy | (1654, 1429) |
| VM | 3623×6263 |
| core_exact | 1.0 |

## Hard rails（永不放鬆）

1. **person_scale = 1.0 always** — Scene 可 scale；人不可。
2. **公式對位優先** — 先 COREFIT 再貼；禁「感覺縮放」。
3. **Imagine region_edit 只刪人** — 禁 OpenCV 大 mask 連岩。
4. **a 主用 Face+Torso** — Legs residual 不進 a、不縮人。
5. **integer locked donor_xy** — core bit-exact。
6. **Virtual Master formal 不回縮**。
7. **ACCEPT_CORE ≠ ACCEPT_FULL**。
8. **錨錯 → INCONCLUSIVE**，不可直接 REJECT_POSE_MISMATCH。
9. **GROUND_HORIZONTAL_LOCK** — HD 雙腳同一水平；貼回 sole 對峰台。
10. **中距優先於極遠** — 人 ≥25% 畫高較穩；極遠可 S_cap 但須標 BOUNDARY。

**矛盾集：** 鎖死小母圖尺寸 ∧ 大原生人物 ∧ person 1.0 同框 → 必開 VM。

## 子技能

| 碼 | 正名 | 職 | 優先 |
|----|------|-----|------|
| **SHQ / SHQ-BEST** | 升清回位 | 主技全鏈 | ★ |
| **SHQ-COREFIT / ANTHRO-FIT** | 人體公學對位 | landmark a,R,t | ★ 重點 |
| **SHQ-DEL / IMAGINE-DEL** | 想像去人 | region_edit 只人 | ★ |
| **SHQ-LOCKXY / HARDPASTE** | 鎖位硬貼 | core 原像素 | ★ |
| **SHQ-VM / VM-LOCK** | 虛擬母圖 | formal 不回縮 | ★ |
| **SHQ-GROUND** | 地面水平鎖 | sole 對峰台 | ★ 本輪升格 |
| **DDXX / DDXX-AR** | 大大小小 / 錨定保像素 | 概念前身 | |
| **PATH1E-F / PATH1E-P** | 臉核 / 姿板 | 局部或 plate | |
| **SHQ-ANCHOR** | 錨點審計 | 禁落空 | |
| **SHQ-LS** | 腳底岩補 | 可選 | |
| **SHQ-PEEP / SHQ-PLATE** | 窺窗 / 姿板 | 抽姿→HD | |

詳：`SHQ_SUBSKILLS.md` · `references/SUBSKILLS.md`

## 勿再犯

`DO_NOT_REPEAT.md` · E-SHQ-01…23  
口訣：**公式先；人永遠 1.0；山可放大；刪人只圈人；貼回要 exact；腳鎖水平。**

## 證據

- BEST：`SETS/PROJ_SHQ_MID_LEVEL_RETURN_V1/SHQ_RUN/`
- 首樣：`…/DDXX_IMAGINE_DEL_PASTE/`
- 登記：`references/REGISTRY.json`

## Done / stop

formal = VM 原尺寸 + REPORT（a, donor_xy, core_exact, face_exact, sole_y, method=`IMAGINE_DEL_LOCKED_PASTE`）。  
禁：half 冒充 formal；GEN 軟融當回位；縮人交差。
