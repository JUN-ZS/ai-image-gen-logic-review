# 一升混鎖 S1HL 正確流程 · §0.12.15.L

asof: 2026-10-28T07:06:25Z

## 定位
GRID×SIAX（§0.12.15）之 **成套支招**：升清 + 混 + 女主臉鎖 **一條過**；**SIAX 只一次**。

## T0 母底
- 正典 L0／IP 原生（§0.12.23 禁病毒局部母）
- 標準面 a8b 就位（§0.10）

## T1 真 SIAX4×（唯一）
- 權重：`4x_NMKD-Siax_200k.pth`
- **預覽／一升未指定 → §0.12.39 SPM-A（48×64²）**；定版 → 全幅 tile／band 防 OOM；存 `SIAX4x_*_FULL`
- **禁止** i2i Enhance 冒充


<!-- SPM_DEFAULT_SIAX §0.12.39 -->
## 預設 SIAX／一升混圖（§0.12.39 SPM-A）

> **一升／預覽／探針升清預設 = SPM-A：48 × 64² · 殘粗糙**  
> 全文：`SIAX_PROBE_MATCH_SPM_01239.md`  
> 定版全幅仍走 **S1HL-P0** strip（OOM 見 `SIAX_HYBRID_FACELOCK_S1HL_OOM_NOTES.md`）。

| 項 | 預設 |
|----|------|
| TILE | **48 × 64×64** · grid 8×6 邊優先 |
| residual_gain | 1.15 |
| rough_boost | 0.85 |
| fill_sigmas | [4, 8, 16] |
| M | 0.45–1.0 邊權 |
| 等價旋鈕 | GUIDANCE≈gain+M · NOISE≈rough+amp · STEP≈fill_sigmas（**非**擴散原生） |

```
out = LP(Lanczos) + residual_field(SPM-A)×M
```
禁：默認全幅 4× 當預覽；稱 SIAX 有 CFG/steps。
<!-- END_SPM_DEFAULT -->


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

---

## 預設 SIAX · 掛 SPM-A（2026-10-29T19:00:00+08:00）

> 詳：`SIAX_PROBE_MATCH_SPM_01237.md` · §0.12.37

**一升未指定 PATH 時：**

| 用途 | 預設 |
|------|------|
| 預覽／指紋／衣板 ZYF | **SPM-A：48 × 64² · 殘粗糙** |
| 定版交付 | 仍 **S1HL P0** strip 全幅 4× Hybrid |
| 臉鎖後 | T3 a8b 僅定版路；SPM 預覽可無臉 |

```
S1HL 預覽 = SPM-A（探針 HF + LP×M）
S1HL 定版 = P0 SIAX 全幅 strip + Hybrid + a8b
```

等價旋鈕（GUIDE/NOISE/STEP）只改 residual 後處理，**不**表示 Siax 有 CFG。
