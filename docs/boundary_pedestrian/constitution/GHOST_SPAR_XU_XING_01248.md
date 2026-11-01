# 虛形互搏 · 母圖 ControlNet + 他機透明虛線
# §0.12.48 · asof 2026-10-30T19:39:31Z

> **用戶鐵句（refs a49e62f6 / d7427ac2 / f3757a08 動作錯）：**  
> 試用 **ControlNet 去描母圖** · AND 把**其他非自己的物件做成透明虛線** 去幫助出形互動 ← **技：虛形互搏**

---

## 0. 一句

每人／每機做 **「實己 + 他虛」** 母圖條件板：  
**自己** = 實像素／綠描；**其他機** = **半透虛線 silhouette**（禁實填）。  
此板當 **ControlNet 姿條件** + 自己 **IP 展開** 身份 → 出個別 COMPLETE · 懂互搏咬合。

---

## 1. 鐵序

```
母 + peep masks
  for L in A..：
    board_L =
      自己 L   → 實 peep（或綠描實邊）
      其他 ≠L  → alpha 半透 + 虛線描邊 silhouette（ghost）
      底        → 可 VOID 或母淡化
    CN_L = ControlNet/等價(
      condition = board_L（描母姿 + 虛形互動）
      identity  = L 的 IP 展開
    )
    → 個別 COMPLETE（自己 · 姿鎖母 · 知他機虛形）
  遠→近 peep s 貼 GRID-locked VOID
```

---

## 2. 虛形規則

| | 自己 | 他機 |
|--|------|------|
| 填充 | 實 peep 像素 | **半透 15–30%** 或 **空心** |
| 邊 | 可綠實描 | **虛線 dash**（青／灰／白） |
| 角色 | 主體身份+姿 | **互動參考 only** · 禁入 cut |

**禁：** 他機實填進 CN 主體 · 無虛形只 solo peep（易丟互搏）

---

## 3. 與影分身合

| 影分身合 | + 虛形互搏 |
|---------|-----------|
| IP 展開 + peep CN | peep 升級為 **實己+他虛** 母描板 |
| 個別自己 | 仍個別 · 但 CN **看得見** 對手虛形 |

---

## 4. 毒碼

| 碼 | 禁 |
|----|-----|
| **E-GHOST-01** | 他機實像素當主 · 身份串色 |
| **E-GHOST-02** | 無虛形 · 只 solo 丟咬合 |
| **E-GHOST-03** | 虛線板未對母對齊（未聯動 GRID） |
| **E-GHOST-04** | CN 出多機實身（應只一機） |

---

## 5. 一刀卡

```
技=虛形互搏 §0.12.48
cond=母描 · 實己 · 他機透明虛線
CN=cond + IP身份 → 個別 COMPLETE
合=peep s · GRID-locked VOID
BAN=ghost_solid, no_ghost_solo_only, multi_real_out
```

*END*

## 四技聯動（對紋）
影分身合+虛形互搏+殘相轉生+P_G紋 · 缺影分身/虛形則改不到新對紋 · 樣 OBA_DRESS_FULLCHAIN · 2026-10-30T20:20:40Z
