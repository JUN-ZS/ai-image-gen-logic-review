# §0.12.25 GOU_DETECT_SHAPE — 勾形 DETECT · 非方框拼 · 探錯進程

> 附件專章 · 與 BOUNDARY_WALKER_UNIFIED_RULES §0.12.25 同步  
> asof 2026-10-27T10:55:37Z · 用戶：「這不是有進展嗎, 探錯過程寫入憲」

 GOU_DETECT_SHAPE（勾形 DETECT · 非方框拼 · 探錯進程入憲）

> asof 2026-10-27T10:54:00Z · 用戶確認：「這不是有進展嗎, 探錯過程寫入憲」  
> 鏈：§0.12.23 VIRUS · §0.12.24 WHOLE · **本節 = 反推真義 + 勾形拼 + 探錯年表**  
> 樣板：`L-767fc2634e8f`（形狀 fill=0.568）· `L-05683b2c4e72`（勾→無框母）· contour `360ef2a0…` · FULL `f5c6a555…`

> **地位：** 升清／密網／材質拼回時，**拼的單位是「DETECT 出的改動形狀」**，不是 search box。  
> 未過本節 → 不得稱「勾形拼回／誠實密網合回」。

#### 0.12.25.A 一句話

**反推 = DETECT 圖中改了什麼（含 SIAX／混生／放大衣）的真邊界；拼 = 沿該不規則形狀 α 貼 FULL；search box 只定位；母底必須全幅非病毒。**

#### 0.12.25.B 用戶原話（不可再誤讀）

| 原話 | 真義 | 誤讀（KILL） |
|------|------|----------------|
| 「反推…DETECT 圖中改了什麼的邊界(包括SIAX和混生)」 | residual∩mesh∩metal∩自邊界 → 形狀 mask | 反推 RGB 當貼圖內容 |
| 「定義回去的『拚』,一定不會是一個方框拼回」 | 拼貼單位 = 不規則 RANGE | magick 方框 cover 當完成 |
| 「不用借鑒 OLD 底自以為 SAVE 了算力」 | 不借 CONST／舊結構邊鎖輪廓 | 為省算力鎖 OLD 邊 |
| 「把這勾勾概念貼到這本來無邊框出錯的圖」 | 綠勾內域形狀 → 無邊框出錯母 | 只畫綠線裝飾 |
| 「抑或你不用底病毒? TRY」 | 全幅母底 + 勾形 同時成立 | 局部 crop 當 BASE |
| 「這不是有進展嗎」 | fill≪1 · lap 升 · 綠形≠紅框 = 有效進展 | 無視數值只喊 FAIL |

#### 0.12.25.C 探錯進程（年表 · 不要重蹈）

| 序 | 錯法 | 症狀 | 解救 |
|----|------|------|------|
| 1 | **BOX_PASTE** | 整 ROI 方框 α 蓋回；形狀填滿≈1 | 拼 = RGBA 形狀 α；fill_ratio 閘 |
| 2 | **REV_AS_CONTENT** | 反推像素當 full-RGB 內容 → lap 崩 | 反推 **只定 RANGE**（§0.12.24） |
| 3 | **OLD_EDGE_LOCK** | 借 OLD/CONST 結構邊「省算力」→ 岔邊／錯鎖 | 衣板 **自認新邊界** |
| 4 | **VIRUS_LOCAL_BASE** | 局部 PART 當母底再升全圖 | **§0.12.23** 全幅 native only |
| 5 | **FILL≈1 假形** | body/metal 過寬 → mask 填滿 box | GrabCut 自邊界 ∩ gou 內域 ∩ changed |
| 6 | **PATCH_UPPER_ONLY** | 「無」區只補上半 | WHOLE 全板 uniform |
| 7 | **LEFT_BRANCH_ALIGN** | 錯認左母／節外錯枝 | 右母／正確 INTO 鎖定 |
| 8 | **REMBG_WEAK_ARMOR** | 黑甲+火底 rembg frac≈0.06 失敗 | 半幅 GrabCut 自邊界 |
| 9 | **a0beb 未落盤** | asset 28.9MB 無 path → 誤母 | 標明替代全幅 + 允許用戶重丟原檔 |

#### 0.12.25.D 正解鏈（GOU_DETECT_SHAPE）

```text
① BASE = 全幅 native only（§0.12.23 · virus_local_base=false）
② donor = 放大改過的衣服／SIAX·混生板（從 BASE 裁出 i2i 亦可）
③ multi-scale template → search box（**只定位**）
④ AFFINE ECC 整板對位（比 euclid；ncc 目標 ≥0.75）
⑤ 形狀來源（可疊）：
     a) 勾概念：綠輪廓內域 flood（e61ab 類）
     b) 自邊界：GrabCut / rembg 衣板 silhouette
     c) DETECT：residual ∩ mesh ∩ metal ∩ hf_delta（改了什麼）
⑥ RANGE = shape ∩ DETECT · 壓 skin · face oval · weapon softlock
⑦ 內容 = V5：base + α*(gen_MF−base_MF) + β*armor*base_HF
⑧ 拼回 = plate_SHAPE.png（RGBA · α=RANGE）→ composite FULL
⑨ 閘：fill_ratio ∈ [0.30, 0.75] · lap(out)≥0.95×lap(in) · 綠形≠紅框圖
```

#### 0.12.25.E 角色分工（寫死）

| 角色 | 做 | 禁止 |
|------|----|------|
| **search box** | 對齊搜尋範圍 | 當拼貼形狀 |
| **勾／自邊界** | 不規則 silhouette | 方框 feather 冒充形 |
| **DETECT residual** | 標「改了什麼」強度 | full-RGB 內容 |
| **V5 混法** | 唯一內容公式 | soft RGB 蓋硬母 |
| **BASE** | 全幅 | 局部病毒 |
| **fill_ratio** | 形狀面積／bbox · 證非方框 | 忽略填滿率 |

#### 0.12.25.F 進展樣板（PROOF · 有進展）

| L / asset | 模式 | fill | ncc | lap armor | 備註 |
|-----------|------|------|-----|-----------|------|
| **L-767fc2634e8f** | SHAPE DETECT | **0.568** | 0.977 | 1592→**2086** | 綠形≠紅框 · contour `e61ab50c` 邏輯 |
| **L-05683b2c4e72** | 勾→無框母 TRY | **0.581** | 0.930 | 1529→**1825** | gou e61 ∩ GrabCut · FULL `f5c6a555` · contour `360ef2a0` |
| L-5d776bf61a20 | WHOLE 自邊界（前） | — | 0.977 | 999→1204 | 仍偏 ROI 拼；後改形狀 |
| L-a6ca442ac78f | 假形 fill≈0.96 | **0.964** | — | — | **KILL 樣** · 形未收緊 |

**進展判定（寫死）：** fill≪1 **且** lap 升 **且** 目視綠勾跟衣緣 **= 有進展**。不得因中間錯刀否定已驗證鏈。

#### 0.12.25.G 閘門勾選

- [ ] BASE 全幅 · `virus_local_base=false`
- [ ] search box **未**當拼貼單位
- [ ] RANGE 來自 DETECT±勾±自邊界 · 非矩形
- [ ] `shape_fill_ratio` 記錄且 ∈ [0.30, 0.75]（過寬重跑）
- [ ] 內容 = V5 · 反推不進 RGB
- [ ] AFFINE 試過 · ncc 報告
- [ ] face oval · weapon soft/hardlock
- [ ] 交付可附：綠形 vs 紅框圖 · DETECT mask · META
- [ ] lap_gate_ok

#### 0.12.25.H 黑名單速記（E-GS 續）

| 代號 | 一句 |
|------|------|
| **E-GS-34** | 方框拼回當完成（fill≈1） |
| **E-GS-35** | 借 OLD/CONST 邊省算力 |
| **E-GS-36** | DETECT 假形（mask 填滿 ROI） |
| **E-GS-37** | 無視 fill/lap 進展只喊全敗 |
| **E-GS-38** | a0beb 類未落盤卻硬稱「已用原像素」不標替代母 |

#### 0.12.25.I 與他節

| 節 | 關係 |
|----|------|
| §0.12.23 VIRUS_LOCAL_BASE | 母底鐵律；本節管 **勾形怎麼拼** |
| §0.12.24 WHOLE_COLLAGE | 反推=RANGE · V5 · affine；本節補 **形≠框 + DETECT 真義 + 勾** |
| §0.12.22 EDGE_OBJECT | 識物勾邊可服務自邊界；不得替代 DETECT 改動 |
| MESH V5 | 內容公式繼承 |

*END §0.12.25 · asof 2026-10-27T10:54:00Z*

#### 0.12.25.J 病毒→勾勾 全鏈入憲（用戶試出 · 流程鎖）

> asof 2026-10-27T14:38:15Z · **用戶：**「把我試出這方法的重重錯走病毒到現在這勾勾圖的方法入憲和流程」

**終態一句：**

```
全幅 BASE（禁病毒）
  → 從 BASE 裁衣 → GEN 密網重組（真生成）
  → 可選 2× 放大加紋
  → template 定位 + AFFINE
  → 勾形 DETECT（形≠框）
  → V5 形狀 α 拼回 FULL
  → PROOF fill/ncc/lap
```

**重重錯走（已殺 · 詳 GOU_MESH_DO_NOT_REPEAT）：**

病毒局部母 → 上半有網下半無 → 只補上／反推當內容／貼錯位  
→ 方框拼／借 OLD 邊／fill≈1 → 硬縮放 ncc 崩  
→ **勾勾正解**。

**流程附件（強制隨本節）：**

| 檔 | 角色 |
|----|------|
| `GOU_MESH_CORRECT_PROCESS.md` | **T0→T12 正確流程** |
| `GOU_MESH_DO_NOT_REPEAT.md` | 病毒／拼貼／對位／材質黑名單 |
| `VIRUS_LOCAL_BASE_01223.md` | 母底 |
| `WHOLE_COLLAGE_ALIGN_01224.md` | 反推 RANGE · WHOLE |
| `MESH_STITCH_FORMULA_V5.md` | V5 內容 |

**終態樣板（試錯 v2 過閘）：**

| 欄 | 值 |
|----|-----|
| L | **L-8ed30b6e8fe0** |
| BASE | `f5c6a555…` GOU_ON_A0 FULL |
| GEN | `96992a7f…` Ref(crop,7f5)+2× |
| fill | **0.575** |
| affine ncc | **0.824** |
| lap armor | 1178→**1609** |
| out | 4608×6912 · ~31MB |
| FULL asset | `8875ed8a…` |

**v1 錯刀（保留當反例）：** 硬縮放無 template · ncc **0.36** · fill **0.89** → FAIL · 已殺。

#### 0.12.25.K 下次生圖必提參數（憲提醒）

升清／密網刀開跑前，助手應提或寫 META：

`BASE_ASSET · MESH_LOCK · ALPHA_GAIN · WEAPON_LOCK · FACE_OVAL · FILL_TARGET · NCC_MIN · UPSCALE`

*END §0.12.25 補 · 2026-10-27T14:38:15Z*

