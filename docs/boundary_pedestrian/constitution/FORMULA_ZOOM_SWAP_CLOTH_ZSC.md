# ZSC 放大換衣 · 落地咬合以 **解毒化衣 DHY** 為準（§0.12.51）
# 舊 soft LP 廢 · 弱 residual 不得單獨稱成功
# 放大中換衣 · 保 PIXEL 回大圖
# ZSC / ZOOM_SWAP_CLOTH · **BITE = HARD RESIDUAL（LOCK）**
# asof 2026-10-30T22:50Z

> **用戶鐵句：** 找公式是**放大中去換衣**，不失去 PIXEL 細節的**套入去大圖**

## 一句
**先放大 peep 衣區 → densify HF=IP衣 → HARD residual 咬合 → α 貼回大圖。**  
禁 soft `LP + M·HF`（E-ZSC-04 洗死換衣）· 禁全幅 GEN densify（E-TEX-05）。

## 公式（生效）

```
L0   = FULL 母大圖
ROI  = peep 衣／甲區（綠描形 · 非框）
L1   = ROI ×2 Lanczos              ← 支母工作幅（放大中）
dens = IPSD_same_frame(L1, HF=IP衣)  ← sole donor = IP衣（影分身合）
α    = peep(金線 ∪ 甲面) · radial · ≤0.98
k    = 1.25 .. 1.35

out  = L1 + k · (dens − L1) · α    ← **HARD RESIDUAL 換衣**
ROI' = resize(out → ROI.size)
FULL'= paste(FULL, ROI', feather·α, at=ROI.xy)
```

### 廢式（E-ZSC-04 · 不得當主公式）
```
L1' = LP(L1) + M·HF(dens)     ← 把 IP衣 densify 洗回 L1 · 衣唔入大圖
```

## 閘
| 閘 | 值 |
|----|-----|
| L1↔dens meanΔ | ≥15（有換衣） |
| L1↔out meanΔ | ≥10（hard 落地） |
| ROI paste meanΔ | ≥12 |
| densify vs L1 ncc | 宜 0.75–0.92（太高=無 rewrite） |
| spill | peep 外 0 |

## BAN
| 碼 | 禁 |
|----|-----|
| E-ZSC-04 | soft LP+M·HF 當 bite |
| E-ZSC-01 | FULL Δ 近零仍稱成功 |
| E-ZSC-05 | densify≈L1 無 IP衣 rewrite |
| E-TEX-05 | 全幅 GEN densify 當換衣 |
| — | 甲碎片 scrap 當 sole HF（必須 IP衣） |

## 與 TEX4 絕招（附屬掛接）
```
① 影分身合 → IP衣 sole HF
② 虛形互搏 → peep 只鎖衣
③ FTSA 枚舉 T_* → 每區跑 ZSC
④ P_G 姿鎖
**嵌 ZSC：** ROI×2 → densify(IP衣) → HARD residual → α FULL
```

連動：§0.12.50 TEX4 · §0.12.50.I FTSA · §0.12.43 SWP · IPSD
樣板：SETS/OBA_BW_POSTER_TEX4/TEX4_ZSC/HARD_RESIDUAL/


---
## 附屬 · 解毒化衣 DHY（§0.12.51 · asof 2026-10-31T07:45+08）

**失敗→成功：** ECC/residual 對準後 FULL Δ≈1.45「沒改」→ dens **可見 rewrite** + peep **硬換 α≈0.9** → ROI Δ≥12 才 LOCK。

```
化衣落地 = DHY
  dens 肉眼有差 → peep 硬貼 → PROOF Δ
  禁：只 MATCH／只 ncc／弱 residual 稱成功（E-DHY-01..03）
```

正檔：`DETOX_HUA_YI_01251.md` · `DETOX_HUA_YI_DO_NOT_REPEAT.md`  
樣板：`SETS/OBA_BW_POSTER_TEX4/DETOX_VISIBLE/` · `FINAL_DETOX_VISIBLE.jpg`
