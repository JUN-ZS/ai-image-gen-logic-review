# HUB 真正值得壓上圖（優先清單 · 2026-10-25）

> 來源：Master A-01–A-09／公式 §4–5／軸 E；`DUAL_T_HAMMER_COLLISION_CONTRACT`；`DUAL_ACTOR_CORRECT_VS_INVERSE_FORMULA`；`槌1.txt`。  
> **唔係全部 HUB 都壓**——只壓下面呢批。其餘留在 docs，唔做畫面噪音。

---

## 1. 缺行／狀態碼（表未成完整分析行 · 優先補）

| 碼 | 意思 | 壓圖時寫法示例 |
|----|------|----------------|
| `GEO.ROD · POS` | 棒軸 **90° 正交正控** | `GEO.ROD · POS · AXIS_90` |
| `GEO.ROD · NEG · θ<35°` | **斜滑失敗**負控 | `GEO.ROD · NEG · θ<35° · SLIP` |
| `GEO.PLANT_O` | **外端同軸**接柄種植 | `GEO.PLANT_O · OUTER-END · F_axial` |
| 五段相（雙 T 細過 H0–H3） | `PRE_FAR → PRE_NEAR → FIRST_CONTACT → REACTION → RECOIL` | 逐幀只標**當前相** |
| 合法打擊 | `END_FACE_TO_END_FACE` | `STRIKE: END_FACE∥END_FACE` |
| 拒斥面 | `CHEEK` \| `HANDLE` \| `SHAFT` | `REJECT: CHEEK｜HANDLE｜SHAFT`（錯接觸時標） |
| 負控角色碼 | `CORRECT_CROSSED_FACE` \| `INVERSE_FACE` \| `COAXIAL` | 雙槌／交叉場景標角色 |
| `ZERO-DRIFT ANCHOR` | planted 影片錨點 | `ZERO-DRIFT · P∈盤` |
| `P` | 接觸點須落**兩打擊面盤內** | `P ∈ DISK₁ ∩ DISK₂` |

---

## 2. 公式晶片（分析行旁硬編碼 · 可縮寫）

```text
n·v · signed_gap · F_n · F_axial
n1·n2 ≈ −1 · E_face · F↔180°
α = arccos(|a·b|) · E_90 = |α−90°|
GEOMETRY_PASS ⇔ E_90≤5° ∧ E_face≤8°
Crack=0 | Crack≫0 · ±δt · Gap>0 | FollowThrough
AXIS_90_PASS · FACET_FACE_CONTACT_PASS · NO_COAXIAL_CONTACT_PASS
```

壓圖規則：

- 當幀只顯示**當前相關** 2–4 個晶片，唔好整頁公式牆。  
- PASS 碼只在該法真嘅約束上出現（例如 ROD POS 才出 `AXIS_90_PASS`／`E_90`）。

---

## 3. 物理標籤（HUB 原生 · 唔係人名）

**Reaction impulse 力鏈**（坐 H2／H3／`REACTION` 相）：

```text
END FACE → HEAD → HANDLE → … → GROUND
```

**視覺相**（可寫短標，亦可只做 VFX 唔寫字）：

| 相 | 視覺 |
|----|------|
| H1 | `air compression ripples` |
| H2 | `star-shaped micro-fracture` · `luminous shock-ring` |
| H3 | `spiderweb fractures` |

---

## 4. 軸 E 必備疊字（每張有字嘅成品）

```text
邊界行人｜THE BOUNDARY WALKER
METHOD: GEO.* · <H/狀態>
WORLD: <本 SET 世界碼>
L-<SHA12>
VFX: <模組碼 可選>
```

**嚴禁畫面出現：**

- TRY 次數  
- `REVIEW PENDING`

---

## 5. 下一輪優先壓旁分析行（12）

出圖時旁行／流動藝術字**優先這 12 類**（可組合，唔使一次全上）：

1. `GEO.ROD · POS`  
2. `GEO.ROD · NEG · θ<35°`  
3. `GEO.PLANT_O`  
4. 五段相：`PRE_FAR` / `PRE_NEAR` / `FIRST_CONTACT` / `REACTION` / `RECOIL`  
5. `E_90`（及 `AXIS_90_PASS`）  
6. `E_face`（及 `n1·n2≈−1`）  
7. `signed_gap`  
8. `Crack=0|≫0` · `±δt`  
9. `reaction impulse` 力鏈短標  
10. `END_FACE ≠ CHEEK`（合法 vs 拒斥）  
11. `ZERO-DRIFT` · `P∈盤`  
12. 軸 E 條：`邊界行人` / `METHOD` / `L-SHA` / `WORLD`

---

## 6. 與既有 11 法 Axis A 的關係

- A01–A11 映射仍見 `setG_gold/axis_a_full/AXIS_A_FULL_MAP.csv`。  
- 本檔 = **壓字優先級**；未列嘅 HUB 細節留 docs，唔強制上圖。  
- 雙 T 五段相 **細過** H0–H3：同一 H2 內都可拆 PRE_FAR…RECOIL 五幀／五標。

---

## 7. 字怎麼壓（上 HUB · 見 TYPO_DOCTRINE_HUB.md）

- 壓邊啲行：本檔 §1–5。  
- **點樣寫成藝術字**：`TYPO_DOCTRINE_HUB.md`（雙軌 A/B、世界材料、幀綁定）。  
- 提醒：**用法跟 SET-F 憲法；外觀跟本 SET 世界**——唔好每輪硬套 F 霓虹塗鴉皮。
