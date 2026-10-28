# GRID×SIAX · 不要重犯（Obs 黑名單）

> ASOF 2026-10-26T15:00:00Z  
> 地位：**錯誤只記一次 → 之後禁止再走**  
> 正典條文：總憲 **§0.12.15 · §0.12.16 · §0.12.17**  
> 正確進程：`GRID_SIAX_CORRECT_PROCESS.md` · `PIXEL_CTRL_LAW.md`

---

## 0. 一句話

```
調 gain ≠ 像素有變
無 PROOF 禁止說「臉更高」
真 Siax pth ≠ Imagine Enhance
全圖 Siax 當 FINAL = 油面風險
眼白 ≠ 再加 face gain
修眼白 ≠ 整臉重構
PROOF 必須 mask 內量
棚拍 a8b 直 ECC ≠ PATH1E 完成
iris 無 annulus / 無 local p = 錯 class
```

---

## 1. 錯誤黑名單（E-GS）

| ID | 錯誤 | 後果 | 校正 |
|----|------|------|------|
| **E-GS-01** | 把 i2i Enhance／GRID「微改」叫 SIA MKD／Siax | 名實不符 | 僅 `4x_NMKD-Siax_200k.pth` |
| **E-GS-02** | 只加 \(g_{FACE}\)，κ_skin 高 + conf 嚴 | **參數↑畫面≈不變**（v1→v2 meanΔ1.56） | 同步降 κ、FACE conf/det 地板、Δ_ROI |
| **E-GS-03** | 無口頭稱有變、無 face crop 量測 | 用戶質疑成立 | 強制 PROOF 閘 |
| **E-GS-04** | 全圖 float64 4× 常駐 | OOM 137 | tile-to-disk + strip · float32 |
| **E-GS-05** | 無 LP conf | 假細節／鬼邊 | conf 壓 M |
| **E-GS-06** | 全圖 Siax = FINAL | 油面／假紋 | Hybrid M |
| **E-GS-07** | 無 FACE/TEXT ROI 推升 | 格增益被吃掉 | Δ_ROI 入公式 |
| **E-GS-08** | **眼白仍吃 Siax HF**；只加 face gain 治爆點 | 眼白假紋／怪 PIXEL | **M_hf=0 · HARD=ST** · EYE_HF_KILL |
| **E-GS-09** | **整臉 ROI 重合成**「修」眼／皮 | 非 mask 像素大漂 | **外科**只寫 mask（§0.12.16） |
| **E-GS-10** | 整眼 crop PROOF 含虹膜當「眼白鎖死」 | 誤判 | 只在 **mask 內**量 ST→ctrl |
| **E-GS-11** | 臉只認三元參數 | 調無效／副作用 | 參數地圖 + EYE_* 入 META |
| **E-GS-12** | **棚拍 a8b 直接 ECC 海報臉** 當 PATH1E 完成 | 不收斂／conf≈0.2／鬼貼 | **plate=Ref(face_crop,a8b)** 再 ECC（§0.12.17） |
| **E-GS-13** | iris 僅全球 mid／chroma；無 annulus | n=0 或臉頰當 iris · HARD 誤傷 | local p + 瞳孔環 + 互斥 ew |

---

## 2. 實證（SET-R 海報 L0 `90807317…`）

| 對比 | mean\|Δ\| | pct>8 | 判定 |
|------|---------|-------|------|
| v1→v2 face | **1.56** | **2.4%** | 幾乎沒變 · **E-GS-02/03** |
| v2→v3 face | **4.81** | **15.2%** | 有可量測變 |
| v3→SiaxFULL face | 3.72 | 9.4% | 貼近但未全開 |
| **PIXEL_CTRL mask 內 ST→ctrl** | **0.38** | **0.4%** | **鎖死** · v1.1 外科 |
| mask 內 Siax→ctrl | **12.65** | 50% | 遠離亂跑源 |
| mask 內 base→ctrl | 2.21 | 4% | 有清 runaway |
| **棚拍 a8b 直 ECC conf** | — | — | **≈0.20 · FAIL** · E-GS-12 |
| **plate→ECC PATH1E** | core→plate **5.13** | 16% | **PATH1E_OK** · `L-fc0a2fa7b8a9` |
| plate ECC cc | **0.980** | — | 收斂 |
| ew→ST after 1E | **0.18** | 0.6% | 眼白仍鎖 |

---

## 3. 閘 · 任一即 FAIL 稱「有變／已鎖」

```
[ ] 未跑 face crop mean|Δ| / pct>8
[ ] mean|Δ|<2 且 pct>8<5% 仍對用戶說已變
[ ] 權重非真 pth
[ ] L0 為疊上疊鏈（E-FLOW-06）
[ ] 眼白未 HARD→ST 仍稱已修
[ ] 整臉重構後無 mask 內 ST≈ctrl
[ ] 棚拍 a8b 直 ECC 仍稱 PATH1E_OK
[ ] iris 無 local p／annulus 仍 HARD 全眼
```

*END GRID_SIAX_DO_NOT_REPEAT · 2026-10-26T15:00:00Z*
