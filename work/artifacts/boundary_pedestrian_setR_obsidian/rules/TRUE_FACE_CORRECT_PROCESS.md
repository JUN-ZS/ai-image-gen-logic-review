# 真臉改臉 · 正確進程（唯一準繩）

> ASOF 2026-10-26T18:23:00Z  
> 地位：**改臉只准走本卡**  
> 不要重犯：`TRUE_FACE_DO_NOT_REPEAT.md`  
> 總憲：**§0.12.14 + §0.12.14.F**

---

## 正典輸入

| 端 | 值 |
|----|-----|
| **dst** | `2455522d-06e7-44c5-b925-cd9a3c5f05df`（aerial 原構） |
| **donor** | `a8b78fe5-2654-4f6f-84e3-c1dfbee61004`（§0.10 標準面） |
| **MODE** | `FACE_CROP_DIRECT` |
| **F_d LOCK** | **`[648, 118, 92, 108]`** |
| **F_s** | `[175, 70, 200, 250]`（可微調，心對心） |
| **kill_wall_x** | **620** |
| **pad** | ≤ 0.10 |

---

## 進程 T0→T4（不可跳）

```
T0  VERIFY_CRING
    clean vs 9d8fGHOST vs CORRECTED
    閘：δ_cring 必須 = 0（只證明環乾淨，≠臉完成）

T1  LOCK 真臉框
    GRID100 + DENSE 頭區掃
    人眼：雙眼+鼻+嘴 同框；**本鏡表情=望球**（見表情鎖；非望相機）
    拒：銅盤、頸、胸、錯框黑名單
    寫：TRUEFACE_META.json（F_d / F_s / 備註）

T2  PIXEL_RATIO V4（身份硬鎖）
    s_face = sqrt((wd/ws)*(hd/hs))
    resize → 重算 s_eff → place_tl 心對心
    橢圓 + hammer_kill + kill_wall_x=620
    alpha_center ≈ 0.88–0.92 · color_match 中
    閘：
      center_err = 0
      δ_face / δ_feat > 0（有改）
      δ_cring = 0 · δ_wrong_left = 0 · δ_hairL = 0
      熱圖 diff 只亮真臉框（實測 x∈[650,738] y∈[120,223]）

T3  V5 可選（清原圖左髮 face-like / 降貼紙感）
    image_to_image：只清左髮誤認、協調光與髮際
    禁止：重抽真臉骨相、禁止動 C-ring、禁止換機位
    閘：仍單臉 · C-ring 可指認 · 身份仍 a8b

T4  交付
    FINAL · STRIP · BEFORE_AFTER_FACE · HEAT · VERIFY_CRING_FACE
    TRUEFACE_META + PIXEL_RATIO_META
    SHA / L- 可選
```

---

## 公式卡（V4 鎖值 · SET-R aerial）

```
F_d      = [648, 118, 92, 108]
F_s      = [175, 70, 200, 250]
s_face   ≈ 0.4458
s_eff    ≈ 0.4444
place_tl ≈ (646, 112)
kill_wall_x = 620
V4 實測：δ_face≈23 · δ_cring=0 · center_err=0
Final 樣板 asset：314f3660-eb42-49a0-b091-c2287632d8a4（V5）
```

---

## 與 Ref 全圖的關係

| 用途 | 准否 |
|------|------|
| 座標／δ_cring／熱圖審計 | **只認 PIXEL V4** |
| 姿態協調、清左髮 | V5 i2i 可 |
| 單獨 `Ref([2455,a8b])` 當「已改對臉」 | **否**（可輔助，不可取代 T1–T2 閘） |

---

## 每跑一次必勾

```
[ ] 讀過 DO_NOT_REPEAT（錯框＋E-PR＋E-FLOW）
[ ] F_d = [648,118,92,108] 或同等人眼鎖（不在黑名單）
[ ] s_eff 已重算 · center_err < 0.5
[ ] kill_wall 生效 · δ_cring=0
[ ] 熱圖質心 ∈ 真臉
[ ] before/after 真臉 feature 可見 a8b
[ ] META 已寫
```


---

## 母圖法則（防層層模糊 · 2026-10-26 用戶 Obs）

> **用戶：**「用這的母圖去改, 因為你用了疊上疊的圖, 層層模糊了」  
> **不要重犯：** `E-FLOW-06` · `E-FLOW-07`

| 准 | 禁 |
|----|----|
| **dst 正典母圖** = `2455522d`（aerial 原構）或 ST2 已鎖 **MID 淨母版** | 以「上一輪 Ref／i2i 產物」當下一輪 dst 再堆 |
| **單次** 全幅鎖臉／望球／身份：`Ref(a8b, 母圖)` **一次** 或 PIXEL V4 **一次** | ce→510f→d33→7c→dbea… 鏈式疊上疊 |
| V5 i2i **最多一刀**（清左髮／柔邊），且仍溯母圖 | V5 上再 V5、Ref 上再 Ref |
| 堆疊圖只作 **對照／教學**（望球對照等） | 把堆疊圖標 FINAL 母版或繼續改 |

```
改臉／改表情／望球 公式：
  I_out = Edit( I_MOTHER=2455522d | locked_MID , a8b , instruction )
  禁止：I_out = Edit( Edit( Edit(I_m, …), …), …)
```

表情鎖仍成立：**望球**（禁望相機）— 但必須在 **母圖單次** 上做，不在糊鏈上修。

*END CORRECT_PROCESS · 2026-10-26T18:44:00Z*



## 表情鎖（SET-R aerial 本鏡）
- **望球**：目光與頭朝右側水晶球／錘擊方向，**禁止望相機**
- 錯誤例：ce2961b6 級「朝相機柔靜」
- 正確例：dbea357d 望球 + a8b 原女主級
