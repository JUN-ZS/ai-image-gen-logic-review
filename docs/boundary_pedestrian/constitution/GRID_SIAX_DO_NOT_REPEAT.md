# GRID×SIAX · 不要重犯（Obs 黑名單）

> ASOF 2026-10-26T15:55:00Z  
> 地位：**錯誤只記一次 → 之後禁止再走**  
> 正典條文：總憲 **§0.12.15 · §0.12.16 · §0.12.17 · §0.12.18 · §0.12.19**  
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
HF 總量最大 ≠ 勝過 hybrid／言清
GRID 當工廠長像素 = 錯（GRID 只是地圖）
假升採樣／空大檔灌 6MB = 錯
整圖 USM 冒充加細節 = 錯
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
| **E-GS-14** | 以 **HF energy 總量** 論勝過／逼 hybrid 追全開 Siax HF | 回油面、假「清晰」 | **§0.12.18.D** 清晰／字可讀為主 |
| **E-GS-15** | 把 GRID 當 uplift 工廠或混合後再全開 Siax 循環 | 疊糊／假好 | GRID=地圖；T12–T14 一次 |
| **E-GS-16** | 為衝 ≥6MB **小圖再 upscale** 或空高 q 大檔 | 假細節／廢帶寬 | **§0.12.19** 原生 4× + residual + q≥95 |
| **E-GS-17** | 整圖 USM／Clarity 當「加細節」 | 油／光暈 | 分區 D4 · PROOF |
| **E-GS-18** | 標 DETAIL6_OK 但 W×H 非全幅或無分區↑ | 名實不符 | SIZE_GATE + PROOF |

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
| **BEAT_v7 vs Siax 清晰** | 5/5 區 ≥ | — | `L-5c738bdfdcdf` · §0.12.18 |
| **GRID_CLEAN 字 clarΔ** | **+11.2** | — | `L-6fb3f0816139` 言清 |
| **METAL_BITE 甲 clarΔ vs Siax** | **+37** | HF+1.1 | `L-f99f139b55a6` |
| **DETAIL6 主檔** | q98 **21MB** / q100 **35MB** | — | `L-7fcd14aab71a` · §0.12.19 |
| DETAIL6 甲 vs v8 | HF+5.2 clar+73 | — | residual 合法 |

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
[ ] 僅 HF 總量稱勝過 pure Siax（E-GS-14）
[ ] 無 CLASS/M 地圖稱 GRID_CLEAN
[ ] 假升／空大檔稱 ≥6MB（E-GS-16）
[ ] 無分區 PROOF 稱 DETAIL6
```

*END GRID_SIAX_DO_NOT_REPEAT · 2026-10-26T15:55:00Z*

## E-GS-21…24 · SKIN_MAT（§0.12.20 · 2026-10-26T17:40:00Z）

| ID | 禁止 | 對照 |
|----|------|------|
| E-GS-21 | 緊特寫毛孔板硬拼全構圖 | ncc 崩；必用 P3 同構圖 |
| E-GS-22 | canvas-LP 主導拼臉 | P1 反例：Lap 崩 |
| E-GS-23 | 差分全黑稱真實 MATERIAL | c27b+0c70 自檢 FAIL |
| E-GS-24 | 無 G-BEAT-ZONE 稱比上圖好 | 必對 baseline zone |

**正典四參數：**  
P1 `9e1cd1e9-f229-4b21-bf4c-91b2d045e08b` · P2 `3f769105-e85e-43d2-854f-f454f8171e34` · P3 `2befbe5e-751c-434a-a39f-ad4bf8ed4374` · P4 `d4d2d76d-c467-46e9-96f2-eb6ba58ec5f6`

*（E-GS-17 已用於 DETAIL6 整圖 USM，皮膚黑名單從 21 起，勿覆寫）*



## E-GS-25…28 · FACE_GENMIX（§0.12.21 · asof 2026-10-26T18:50Z）

| ID | 禁止 |
|----|------|
| E-GS-25 | 用 P3/P4 像素 Lab/HF 混冒充「混參」 |
| E-GS-26 | 直接圖拿 P3/P4 paste 當臉完成 |
| E-GS-27 | GEN 無結構錨 |
| E-GS-28 | GENMIX 不 ECC／不結構鎖硬貼 |

正典：`Ref(結構錨, P4白, P3自然)` 重生 → ECC 拼回。樣板 `L-90961cfbcd33`。

## 一升混鎖 S1HL（§0.12.15.L · 2026-10-28T07:06:55Z）

| 代號 | 禁止 |
|------|------|
| **E-GS-47** | 本招再跑第二次全幅 SIAX（「再 TRUE SIAX4×」） |
| **E-GS-48** | 無 Hybrid 只 Siax 稱「混鎖」 |
| **E-GS-49** | 先臉鎖再 SIAX 當一升混鎖正典順序 |
| **E-GS-50** | 無 a8b Ref 只喊臉鎖 |

**正：** SIAX×1 → Hybrid → Ref(hybrid,a8b) → **停**。

---

## E-GS-04 族擴 · S1HL 一升 OOM（2026-10-29T04:10:00+08:00）

| ID | 禁 | 後果 | 下次先走 |
|----|-----|------|----------|
| **E-GS-04** | 全圖 float64 4× 常駐 | OOM 137 | tile-to-disk · float32 band |
| **E-GS-04b** | Hybrid 持 LP+HF+Siax 三幅 FULL float | OOM | strip Hybrid 直出 VIEW/HD |
| **E-GS-04c** | siax.mm + hyb.mm 雙全幅 | I/O／峰值 | 只 siax.mm |
| **E-GS-04d** | OOM 後原樣加大 tile/band 重跑 | 再 137 | 換 PATH：ROI / S=2 / GRID |
| **E-GS-04e** | OOM 後二升或 pure Siax 當 FINAL | 違 S1HL | 見 `SIAX_HYBRID_FACELOCK_S1HL_OOM_NOTES.md` 選路表 |

**正典成功 PATH：** STRIP_S1HL v3 · 樣板 SET-S `abe76` → T3 `be436496…`
