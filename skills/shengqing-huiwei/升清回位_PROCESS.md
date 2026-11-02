# 升清回位 · 正程（SHQ-BEST 成功鏈）
> asof 2026-11-03T06:45+08 · write 01263 · 金牌：PROJ_SHQ_MID_LEVEL_RETURN_V1

## 優先法（用戶：這方法優先 · 公式對位是重點）

```text
1) 中距原景有人（~25–35% 畫高 · sole 水平可讀）
2) peep 抽姿 + HD 同姿 plate（雙腳同水平地）
3) Pose JSON · Face+Torso → a,R  · 腳 → t / GROUND_LOCK
4) Imagine region_edit 只刪人 · 峰台保留
5) Scene × S=1/a → Virtual Master
6) HARDPASTE donor scale=1.0 @ integer (tx,ty)
7) core_exact=1 · face_exact=1 · REPORT 入檔
```

**STATUS 終態：** `IMAGINE_DEL_LOCKED_PASTE_OK`  
**CORE：** `ACCEPT_CORE`（face/core exact）  
**FULL：** 未默認通過（Legs/披風/接觸可選開）— **不**為 FULL 動 person_scale

## 公式

### 相似變換（donor → target scene）

    q = a * (R @ p) + t

- p：donor 標點  
- q：原景標點  
- **a 只由 Face+Torso**  
- Hands/Legs **報告但不進 a**  
- 腳：`t = feet_t − a (R @ feet_d)` · **sole 水平鎖**

### 逆變換（scene → VM，人 1:1）

    S = 1/a
    feet_vm = S * feet_t
    (tx,ty) = round(feet_vm − feet_d_local)
    person_scale = 1.0 always

### 金牌鎖定量（MID_LEVEL · 2026-11-03）

| key | value |
|-----|-------|
| a | 0.39358124917249104 |
| S | 2.5111607142857144 |
| rot | −2.182° |
| donor_xy | (623, 821) |
| sole_y_vm | 2268 |
| VM | 2552×4520 |
| core_exact | 1.0 |
| face_exact | 1.0 |
| sha16 | 3b286bb099f0ac43 |

### 首成鎖（A8B legacy）

| key | value |
|-----|-------|
| a | ≈0.28985 |
| 1/a | ≈3.450 |
| donor_xy | (1654, 1429) |
| VM | 3623×6263 |

## 交付物最小集

| 檔 | 義 |
|----|-----|
| 00_BOARD | 中距|peep|HD|空|貼 |
| 02_EMPTY | Imagine 空峰 |
| 03_HD_RGBA | donor 原生 |
| 04_VIRTUAL_MASTER.png | 全像素 formal |
| 07_GROUND_AUDIT | sole 黃線 |
| REPORT.json | a,S,donor_xy,exact,sha |

## 狀態機

```text
PEEP_OK → PLATE_LEVEL_OK → COREFIT_OK
  → IMAGINE_DEL_OK → HARDPASTE_1.0
  → IMAGINE_DEL_LOCKED_PASTE_OK   ← SHQ-BEST 終態
  → ACCEPT_FULL_COMPOSITION       ← 未默認
```
