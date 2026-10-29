# 宏圖層律 MSR · 大圖三維律動 → 世界 READ → 訊號 → 層層收放

> asof 2026-10-28  
> 用戶宏圖：「先從大圖理解整體會有對稱三維律動的噪對位/景/物，再一次過生成重生定義理解它本來在真實世界再 READ 完再 PROMPT 生成下的模樣參考，再要有能力/訊號使這格物可重回邏輯正確的合理性分辨解/噪生成，層層收細又放大中律動」  
> **正名：宏圖層律** · **短碼 MSR** · Multi-Scale Rhythm  
> **地位：** 格物／密網／解噪的 **總程**（駕馭 OTL0·RML·GOU·N2R·V5·GCS·SDS-3D MAP）  
> **禁：** 跳過 L_MACRO 直接局部 Soft 當真（= 舊失敗）

---

## 1. 一句

```
先大圖懂 景·物·三維律動噪場
→ 世界定義 READ
→ 一次過造「模樣參考板」（donor／lock · 非 BASE）
→ 多尺度訊號 KEEP/FREE 分辨解噪
→ 層層收細（ROI·GEN·V5）又放大拼回
→ 全程同一 BASE 座標 · 律動連續
```

---

## 2. 六層（不可跳層）

| 層 | 名 | 做什麼 | 產物 | 憲位 |
|----|-----|--------|------|------|
| **L0** | **MACRO 景物場** | 全幅讀：景深節奏、主物對稱軸、金屬/網/膚分帶、粗中細 HF | SCENE / KEEP_MACRO / FREE_MACRO 圖 | 新增總程 · 喂 RANGE |
| **L1** | **WORLD READ** | 每主物真實世界層（如 305d2：L0 hex·L1 鑄星·L2 有序絲） | CONST_WORLD 短卡 | OTL0 物真之上的「材質讀」 |
| **L2** | **一次過模樣參考** | 用短 READ+短 RML **一次** Ref/i2i 出 plate | **REF_PLATE** = mesh_lock / density donor | **非 BASE** §0.12.23 |
| **L3** | **訊號能力** | 多尺度 KEEP3D/FREE3D + N2R cand + RML 錨 | MAPS · 可稽 | SDS 只 MAP；N2R/WNK 噪職 |
| **L4** | **收細** | 同 BASE 裁 ROI → GOU T3 GEN( crop, REF_PLATE ) → ECC | plate_w | GOU T2–T6 |
| **L5** | **放大拼回** | RANGE∩MAP → V5；歪則 GCS；點則 PIXEL | FULL_out | V5·WHOLE·GCS·PIXEL |

**層層收細又放大中律動** = L0 場在 L4/L5 **繼承**（α/gain 跟 SCENE/KEEP），禁止收細後換一套無關噪先驗。

---


<!-- SPM_DEFAULT_SIAX §0.12.39 -->
## 預設 SIAX 升清（§0.12.39 SPM）

| 層 | SIAX 預設 |
|----|-----------|
| L3 訊號 | 可用 SPM-A 探針 residual 作 HF／N2R 指紋 |
| L4 收細 | ROI 真 SIAX 或 GOU；**全幅預覽默認 SPM-A 48×64** |
| L5 拼回 | 定版才 S1HL-P0 全幅 |

**宏圖一升未指定 → SPM-A**，禁止默認全幅 4×。
<!-- END_SPM_DEFAULT -->


## 3. 流程圖

```
[全幅 BASE native]
        │
        ▼
 L0  MACRO：SCENE · KEEP_MACRO · FREE_MACRO · 物框粗定位
        │
        ▼
 L1  WORLD READ 短卡（禁 OIDV 長文）
        │
        ▼
 L2  一次 PROMPT → REF_PLATE（模樣參考 · lock only）
        │
        ├──────────────────────┐
        ▼                      ▼
 L3  訊號 MAPS            L4  收細 ROI 鏈
 KEEP/FREE/N2R/RML          crop→GEN(lock)→ECC
        │                      │
        └──────────┬───────────┘
                   ▼
 L5  RANGE = reverse∪gou∪f(KEEP)∧¬FREE_kill
     out = V5(base, plate) · 可選 GCS · PROOF
                   │
                   ▼
         可再一層更細 ROI（仍同一 BASE）· 律動不重抽世界
```

---

## 4. 與舊失敗的差

| 舊 | MSR |
|----|-----|
| 先 crop 再悟 3D | **先全幅場** 再 crop |
| 多輪 Soft 愈修愈 logo | **L2 一次** 參考板 |
| SDS 當主重生 | SDS/**MAP** 只分辨解噪 |
| 局部當 BASE | REF_PLATE = lock · BASE 永全幅 |
| 收細後噪先驗斷裂 | L0 場貫穿 L5 gain |

---

## 5. 訊號定義（合理性分辨解／噪）

```
SCENE_λ     = 粗+中 HF（景/體塊節奏）
KEEP_λ      = 結構帶 ∪ 金屬/網（應保留／升）
FREE_λ      = 細 HF ∧ ¬粗結構（應解／N2R／WNK）
λ ∈ {macro, mid, fine}   # 層層

升清／GEN 寫入：偏 KEEP_λ
解噪：偏 FREE_λ（N2R 轉 or WNK 殺）
拼回 α：α *= SCENE continuity（邊勿突變）
```

**三維律動噪對位** = 唔係 flip 對稱分數，而係：  
同物在 **透視＋曲面** 下，KEEP 帶連續、FREE 帶唔污染結構棱。

---

## 6. PROOF 閘

| 閘 | 要求 |
|----|------|
| BASE | 全幅 native · virus=false |
| L0 場 | SCENE/KEEP/FREE 可稽圖 |
| L2 | REF_PLATE 標 `role=lock_or_donor` 非 base |
| L4 ECC | ncc≥0.75（GOU） |
| L5 V5 | 禁 CHEAT_B · lap 結構區↑或持平 |
| 律動連續 | 收細前後 KEEP 重疊合理 · 無整區 FREE 變結構 |
| OTL0 | 物拓 Verify |

---

## 7. 一刀參數卡

```
BASE_ASSET=
L0_maps= SCENE,KEEP_MACRO,FREE_MACRO
WORLD_READ_CARD=   # 短 · 分物
REF_PLATE=         # 一次生成 · lock
ROI_chain=         # 大→中→細 box on BASE
V5=true  GCS=on_fail  N2R|WNK=on FREE
OIDV_long_prompt=false
```

---

## 8. 鄰條

| 條 | 關係 |
|----|------|
| OTL0 | 物真 L0 · MSR 不改拓 |
| RML | L3 錨 · 短提醒 |
| GOU T0–T12 | L4–L5 主執行 |
| N2R/WNK | FREE 帶處置 |
| COMPLEMENT_MESH3D | 互構職分；MSR 為 **總程包裝** |
| OIDV | 禁跳 L0/L1 灌長文硬重生 |

*END 宏圖層律 MSR*


---

## 9. 正衣先行（2026-10-28 用戶鎖）

> 用戶：「既然你另生圖就能對稱，…一開始就出一件正確的衣，再合新就行了」  
> 樣板對稱板：`8f09b935`（世界 READ 後一次重生 · 雙側對稱 OK）

```
L2' 正衣（ZHENGYI）
  = 獨立一次生成「正確的一件衣／甲」
  = 世界 READ + 短 PROMPT + 對稱真源（可 8f09 類）
  ≠ 在全圖 Soft 修對稱
  ≠ 病毒局部母

然後：
  合新 = Ref(全幅姿／BASE 骨架, 正衣) 或 V5/GOU 把正衣合入
  訊號 = KEEP/FREE 只管合入時解噪 · 不正衣本身再亂改拓
```

| 舊錯 | 正衣先行 |
|------|----------|
| 全圖裡硬修對稱 | 另板一次生對稱正確 |
| crop Soft 愈改愈歪 | 正衣 OK 才合 |
| 合時重雕衣 | 合只對位／V5 · 衣拓已鎖 |

*END §正衣先行*

---

## 預設 SIAX · SPM-A（2026-10-29T19:00:00+08:00）

> 掛：§0.12.37 SPM · 嵌入 L3–L4

| 層 | SIAX |
|----|------|
| L0–L2 | 不強制 SIAX |
| **L3 訊號** | 可用 **SPM-A residual／edge** 作 KEEP/FREE 輔 |
| **L4 收細** | 預設升清 = **SPM-A**；定版格 = ROI 真 SIAX 或 P0 |
| L5 拼回 | 同前 V5；SPM 產物 ≠ BASE |

大圖場先立（MSR）→ 探針落在 KEEP 密網／金屬帶（48 格邊優先）。
