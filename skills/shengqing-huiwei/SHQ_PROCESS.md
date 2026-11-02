# 升清回位 · 正程 v1.1（公式對位優先）
> asof 2026-11-03T06:40+08 · **優先法 SHQ-BEST** · 金牌 PROJ_SHQ_MID_LEVEL_RETURN_V1

## ★ 優先成功鏈（必須）

```text
1) 中距原景有人（人高 ~25–35% 畫高）
2) peep 抽姿（可 ×3）
3) PLATE-POSE：高清同姿 · 雙腳同一水平地線
4) Pose JSON：Face+Torso(+肩髖) → a,R,t
   公式:  q = a * (p @ R) + t
   a 只 Core；腳只鎖 t / ground
5) Imagine-DEL 只人 · 峰台水平岩保留
6) Scene × S（≈1/a）→ Virtual Master
7) HARDPASTE person_scale=1.0 @ integer (tx,ty)
8) GROUND_HORIZONTAL_LOCK · sole 對峰台
9) core_exact=1.0 · face_exact=1.0
10) 終態 IMAGINE_DEL_LOCKED_PASTE_OK
```

## 公式（重點 · 不可跳過）

### donor → scene

```
q = a * (p @ R) + t
```

- **a,R**：Face+Torso(+肩髖) weighted / Huber robust
- **t**：優先用 sole/feet 鎖地面水平：`t = feet_t - a*(R@feet_d)`
- Hands/Legs residual **報告不進 a**
- |rot| 過大（>8°）→ 先審錨/姿；可 clamp R=I 保水平（記錄）

### scene → VM（人 1:1）

```
S ≈ 1/a   (可 S_cap 防 OOM，須標 S_capped)
v = S * q
person_scale = 1.0 永遠
paste: integer donor_xy，core α≥0.5 直接複製
```

## 金牌鎖定量

### MID_LEVEL BEST

| key | value |
|-----|-------|
| a | 0.39358124917249104 |
| S | 2.5111607142857144 |
| rot_deg | ≈−2.18 |
| donor_xy | (623, 821) |
| sole_y_vm | 2268 |
| VM | 2552×4520 |
| core_exact | 1.0 |
| face_exact | 1.0 |
| status | IMAGINE_DEL_LOCKED_PASTE_OK |

### A8B 峰首樣

| key | value |
|-----|-------|
| a | ≈0.28985 |
| donor_xy | (1654, 1429) |
| VM | 3623×6263 |

## 交付最小集

| 檔 | 義 |
|----|-----|
| 00_BOARD | 鏈條可視化 |
| 02_EMPTY | Imagine 空峰 |
| 03_HD_RGBA | 高清 donor |
| 04_VIRTUAL_MASTER.png | formal 全像素 |
| 06_FACE_EXACT | 臉 bit 證據 |
| 07_GROUND_AUDIT | 水平 sole 線 |
| REPORT.json | a,S,donor_xy,exact,sole |

## 狀態機

```text
COREFIT_OK
  → IMAGINE_DEL_OK
  → HARDPASTE_1.0_OK
  → GROUND_LOCK_OK
  → IMAGINE_DEL_LOCKED_PASTE_OK   ← 優先終態
  → ACCEPT_FULL_COMPOSITION       ← 未默認
```
