# 技名 · 一升混鎖

| 語 | 名 |
|----|-----|
| **正名** | **一升混鎖** |
| **粵／短** | **混鎖** |
| **英／碼** | **Single-Siax Hybrid FaceLock** · **S1HL** |
| **一句** | **一次**真 SIAX4× → Hybrid（LP+HF×M）→ Ref(hybrid,a8b) 臉鎖女主；**禁二升** |
| **母招** | §0.12.15 GRID×SIAX · 支招 **.L** |
| **地位** | **LOCK** |
| **禁稱** | 再 TRUE SIAX4× · 全開 Siax 當混鎖 · 棚拍 a8b 直 ECC 冒充 Ref 臉鎖 |

## 正典流程（無二升）

```
母圖 L0
  → TRUE SIAX4×（唯一一次 · 真 4x_NMKD-Siax_200k.pth）
  → Hybrid：out = LP(Lanczos) + HF(Siax)×M
       g_face≈0.88 · g_body≈0.72 · g_bg≈0.40 · 眼白 M≈0
  → Ref(hybrid, a8b) 臉鎖女主（姿／裝／械鎖死）
  → 停（不再 SIAX）
```

## 增益起點（可調 · 必 META）

| 區 | g |
|----|---|
| face | ≈0.88（可 0.82–0.95 · PROOF） |
| body／metal | ≈0.72 |
| bg／flat | ≈0.40 |
| 眼白 | M≈0 · HARD |

## 樣板（68ff 鏈）

| 角色 | 值 |
|------|-----|
| 母 | `68ffbcb3-d315-4c78-a96a-3be84cf206c9` |
| 臉鎖中 | `e002eca0-a025-4657-9ac9-f816e0730e99` |
| a8b | `a8b78fe5-2654-4f6f-84e3-c1dfbee61004` |
| 終態 FULL | **L-9441d3d22539** · 4608×6912 · ≈23MB |
| 註 | 實作曾多跑「再 SIAX」；**正典招不要求二升** · 正名鎖定一升 |

## 口令

「上一升混鎖」「跑混鎖」「S1HL」＝同一招。

asof 2026-10-28T07:06:25Z · 用戶：「入憲」· 技法不用「再 TRUE SIAX4×」
