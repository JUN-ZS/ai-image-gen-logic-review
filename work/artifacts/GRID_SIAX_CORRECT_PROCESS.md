# GRID×SIAX · 正確進程（T0–T16）

> ASOF 2026-10-26T15:55:00Z  
> 正典：總憲 **§0.12.15–§0.12.19**  
> 不要重犯：`GRID_SIAX_DO_NOT_REPEAT.md`  
> 像素控制：`PIXEL_CTRL_LAW.md`

---

## 進程

| 步 | 名 | 必做 | 禁止 |
|----|----|------|------|
| **T0** | L0 LOCK | 正典母圖／鎖幀；寫 SHA | 疊上疊生成鏈當 L0 |
| **T1** | TRUE SIAX | `4x_NMKD-Siax_200k.pth` 4×（可 tile）存 FULL | i2i Enhance 冒充 |
| **T2** | GRID+MAP | 6×4 分類 + detail/skin/gain/ROI maps | 整圖同一 g |
| **T3** | HYBRID | out=LP(Lanczos)+HF(Siax)×M | 全圖 Siax 當 FINAL |
| **T4** | PROOF | face/text crop 量測；不過回調 κ/Δ_ROI | 只改 g 就宣稱有變 |
| **T5** | META | 寫 g、κ、mix_face/text、L- | 無 META 標 HYBRID_OK |
| **T6** | PIXEL_CLASS | 每點 class／mem · eye_white 最高優先 | 無 class 就調 gain |
| **T7** | PIXEL_CTRL | **外科** mask 寫 ST；HARD exact | 整臉 dual-band 重構 |
| **T8** | PROOF_MASK | mask 內 ST→ctrl≈0 | 整眼 crop 冒充 |
| **T9** | LAW/META | PIXEL_CTRL_META + 更新 LAW | 無 mask PROOF 稱已鎖眼白 |
| **T10** | **PATH1E plate** | `Ref(face_crop,a8b)` → ECC → 硬貼（§0.12.17 P0–P7） | 棚拍 a8b 直 ECC 當完成 |
| **T11** | PATH1E_PROOF | cc/conf/core→plate/ew→ST + gate | 無量測標 OK |
| **T12** | **CLASS_MAP** | TEXT/METAL/FIRE/FACE/SKIN/EW/FLAT 地圖（§0.12.18） | 把 GRID 當生成工廠 |
| **T13** | **GRID_CLEAN／BEAT** | 只寫好 donor · 禁區 M=0 · 字邊 polish · strip | 全開 Siax 當 FINAL；追 HF 總量 |
| **T14** | **WIN_PROOF** | 分區 clarΔ/HFΔ vs pure Siax · 言清閘 | 無口頭勝過 |

## 正典增益起點（可調 · 必 PROOF）

- FACE **0.82** + ROI push · κ_skin **0.25**（三元核心）
- 擴展見 §0.12.16.G（M_CAP / det / conf / color_pull）
- **eye_white：M=0 · lock=1 · 不可被 face gain 覆蓋**
- TEXT **0.98** + ROI +0.35
- METAL 0.80 · FIRE 0.72 · FLAT 0.45
- 皮膚可選雙帶：MID_SKIN_M≈0.45 · FEATURE_USM 僅 feature mask

## 樣板

- L0 `90807317-4e7d-4646-9f98-ac6c59208d08`
- Siax FULL `L-ec355935c17f`
- Hybrid v3 `L-8bca4ceb59b5`
- PIXEL_CTRL v1.1 `L-69e63d57a466`
- PATH1E plate→ECC `L-fc0a2fa7b8a9`（cc 0.980 · conf 0.782）
- plate asset `44d18362-906a-4659-b162-f162cc5a51df`
- BEAT_v7 `L-5c738bdfdcdf`（清晰 5/5 ≥ pure Siax）
- GRID_CLEAN_v1 `L-6fb3f0816139`（字 clarΔ +11.2）
- pure Siax 對手 `SIAX4x_9080_FULL` ≈ `4c99ea4b…`（禁 FINAL）

*END CORRECT_PROCESS · 2026-10-26T15:35:00Z*

## §0.12.20 SKIN_MAT 進程（2026-10-26T17:40:00Z）

1. A0 face_same_comp 全構圖裁（禁只臉心）  
2. A1–A2 毛孔板 · face_ncc≥0.90 → **P3** `2befbe5e-751c-434a-a39f-ad4bf8ed4374`  
3. B 銳化混法（可大 MB）· 板預覽 **P2**  
4. C 板主導拼回（對齊 **P1** 銳拼邏輯 · 禁 canvas-LP）→ **P4**  
5. D PROOF：BEAT facezone + 可見Δ；META 寫 P1–P4

---

## 支招 · 一升混鎖 S1HL（§0.12.15.L · 2026-10-28T07:06:55Z）

```
T0 L0 → T1 SIAX×1 → T3 Hybrid → Ref(hybrid,a8b) 臉鎖 → 停
```

- **禁** 再 TRUE SIAX4×（E-GS-47）
- g_face≈0.88 · g_body≈0.72 · g_bg≈0.40 · 眼白 M≈0
- 樣板 **L-9441d3d22539**
- 詳 `SIAX_HYBRID_FACELOCK_S1HL.md`
