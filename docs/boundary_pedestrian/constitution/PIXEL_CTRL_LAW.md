# PIXEL 每點記認與控制法（正典附件 · §0.12.16 · §0.12.17）

> ASOF 2026-10-26T15:55:00Z  
> 總憲：**§0.12.16** · **§0.12.17** · **§0.12.18** · **§0.12.19 DETAIL6** · 黑名單 E-GS-08…18  
> 樣板 PIXEL_CTRL `L-69e63d57a466` · PATH1E `L-fc0a2fa7b8a9`

---

## 一句話

```
記認 mask[x,y] → 只允許改這些像素
眼白/ runaway → 寫回結構 ST（L0 Lanczos）
其餘像素 → 完全不動 base
臉 residual → plate=Ref(face_crop,a8b) → ECC → 硬貼（§0.12.17）
棚拍 a8b 直 ECC = 禁止（E-GS-12）
```

## 記認

| 標記 | 條件 |
|------|------|
| eye_white / sclera | 眼高斯區 ∧ **local** 高亮（≥p75）∧ 互斥 iris |
| iris | **每眼** mid band p20–p75 · **瞳孔 annulus** · 互斥 ew |
| pupil | ≤ local p40 |
| runaway | 眼區 ∧ (base 離 ST 大 / 假高頻 / 假高亮低彩) ∧ ¬iris |
| mask | soft(eye_white ∪ runaway) |
| HARD | mask > 0.35 ∧ ¬iris |

## 控制

| 像素 | 寫入 |
|------|------|
| mask / HARD | out → ST（soft / exact） |
| 非 mask | out = base（零改動） |
| PATH1E core | plate warped · α·conf · **仍** ew HARD→ST |

## 眼白鐵律

- **禁止** Siax／plate HF 寫入眼白像素
- 唯一合法源 = L0 結構升採樣 ST
- feature USM / color_pull / face gain **不得**作用於 eye_white

## PATH1E（§0.12.17 摘要）

```
P2 plate = Ref(face_crop, a8b)
P3 ECC(plate → base)  cc ≥ 0.85 才可強貼
P6 ew HARD 不破
閘  PATH1E_OK | PARTIAL | WEAK
```

樣板：ECC **0.980** · conf **0.782** · core→plate **5.13** · ew→ST **0.18** · `L-fc0a2fa7b8a9`

## PROOF（只在 mask 內 · PIXEL_CTRL 樣板）

| 對比 | mean\|Δ\| |
|------|----------|
| ST→ctrl | **0.383**（應接近 0） |
| base→ctrl | 2.209（有清 runaway） |
| Siax→ctrl | 12.646（遠離亂跑） |

## 與 Hybrid 關係

§0.12.15 Hybrid 先 →（可選）§0.12.18 GRID_CLEAN／BEAT → §0.12.16 PIXEL_CTRL →（可選）§0.12.17 PATH1E →（可選）§0.12.19 DETAIL6 體積／細節。
勝過 pure Siax 定義見 §0.12.18.D；≥6MB 交付見 §0.12.19。  
皮膚雙帶合法於 skin/feature；**不得**借雙帶重寫整臉（E-GS-09）。

*END PIXEL_CTRL_LAW · 2026-10-26T15:55:00Z*


## E-GS-25…28 · FACE_GENMIX（§0.12.21 · asof 2026-10-26T18:50Z）

| ID | 禁止 |
|----|------|
| E-GS-25 | 用 P3/P4 像素 Lab/HF 混冒充「混參」 |
| E-GS-26 | 直接圖拿 P3/P4 paste 當臉完成 |
| E-GS-27 | GEN 無結構錨 |
| E-GS-28 | GENMIX 不 ECC／不結構鎖硬貼 |

正典：`Ref(結構錨, P4白, P3自然)` 重生 → ECC 拼回。樣板 `L-90961cfbcd33`。
