# 一升混鎖 S1HL 正確流程 · §0.12.15.L

asof: 2026-10-28T07:06:25Z

## 定位
GRID×SIAX（§0.12.15）之 **成套支招**：升清 + 混 + 女主臉鎖 **一條過**；**SIAX 只一次**。

## T0 母底
- 正典 L0／IP 原生（§0.12.23 禁病毒局部母）
- 標準面 a8b 就位（§0.10）

## T1 真 SIAX4×（唯一）
- 權重：`4x_NMKD-Siax_200k.pth`
- tile／band 防 OOM；存 `SIAX4x_*_FULL`
- **禁止** i2i Enhance 冒充

## T2 Hybrid 混
```
out = LP(Lanczos(L0→4×)) + HF(Siax)×M + mid×κ
M：face≈0.88 · body≈0.72 · bg≈0.40
眼白：M≈0
```
- PROOF face/text（E-GS-02/03）
- 禁全圖 Siax = FINAL（E-GS-06）

## T3 臉鎖女主
```
I_lock = Ref(hybrid, a8b)
# 姿／裝／械／構圖鎖 hybrid；身份鎖 a8b
```
- 禁棚拍 a8b 直 ECC 當完成（E-GS-12）
- 姿漂 → 重 Ref，**不**靠二升 SIAX 救

## T4 停
- **不再 TRUE SIAX4×**（本招定義）
- 交付 FULL ≥6MB 可選走 §0.12.19 存檔層（非再 Siax）
- META + L-

## 黑名單（本支）
| 代號 | 禁 |
|------|-----|
| **E-GS-47** | 本招流程再跑第二次全幅 SIAX |
| **E-GS-48** | 無 Hybrid 只 Siax 稱混鎖 |
| **E-GS-49** | 先臉鎖再 SIAX 當「一升混鎖」正典（順序反） |
| **E-GS-50** | 無 a8b Ref 只喊臉鎖 |

## 樣板
L-9441d3d22539 · 母 68ff · a8b 標準面
