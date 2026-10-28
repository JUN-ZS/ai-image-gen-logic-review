# GRID60 PATH1E LOCK RULES

> **LOCKED** · PATH1E is the only approved face/head HD reassembly method for SET-N grid60 proportional finals.
> Do not silently fall back to PATH1B soft multiband, PATH1C multi-blend wash, PATH1D ORB full-RGB (ghost), or PATH1F unless the user explicitly unlocks.

**ASOF:** 2026-10-25T09:42:23Z  
**SET:** SET-N · GOLDEN_RICE_TERRACE · grid60  
**CANONICAL DELIVERABLE:** `FINAL_PATH1E_CLEAN_HD_FACE.jpg`  
**SHA256:** `355bfec974e3b2b7f7e03548e133050c6b6807559a4395dc84c8b9c1d0116faf`  
**L-code:** `L-355bfec974e3`  
**Size:** 5376×3024  
**Imagine asset (CLEAN 1E):** `a2141161-5a72-4a64-b51f-53912f5b8519`

---

## 0. Why 1E is locked

| Path | Verdict | Reason |
|------|---------|--------|
| **PATH1E** | **LOCKED · DEFAULT** | Clean model-face hard paste; ECC≈0.997; edge-only feather; no ghost sky; face micro sharp ~7–10× PATH1B |
| PATH1B | FORBIDDEN as final | Soft multiband + conf mask washed HF → face Laplacian ~99 vs HD ~300–500 |
| PATH1C | FORBIDDEN | Multi-step soft blend collapsed sharp 98→31 |
| PATH1D | FORBIDDEN | ORB full-RGB warp → double-face / mirror ghosts |
| PATH1F | VARIANT only | Narrower feather / fuller face; only if user asks; not lock default |
| pure residual paste | FORBIDDEN alone | HD close-ups (94b6/3707) reframe → conf kill or ghost |

User signal that forced this lock: *下載完成圖放大後沒有 HD 格質素；併回不致於完全不似。*

---

## 1. Immutable pipeline (PATH1E)

### 1.1 Canvas
- L0 structure base: proportional **S=3** → **5376×3024** from L0 1792×1008
- Body/scene: keep **detail-transfer 60-cell** assembly (L0 LP lock + HD HF residual, confidence gate)
- Face/head: **PATH1E only** (overrides body face region)

### 1.2 Face / head ROI (L0 coords → ×S)

```
FACE_ROI_L0    = [700, 40, 1120, 430]   # x0,y0,x1,y1
HEAD_ROI_L0    = [640, 0, 1180, 500]
FACE_ROI_FINAL = [2100, 120, 3360, 1290]
HEAD_ROI_FINAL = [1920, 0, 3540, 1500]
```

Do not drift these without a new LOCK revision + user ack.

### 1.3 Model face composite (structure carrier)
1. Source composites must be **pose-matched** to full scene (not pure close-up only):
   - face: model refs made with `b3166` / face HDs via reference_to_image (e.g. `575ef483`, `bf193e7c`)
   - head: `0bf1472e`-class head composite
2. **ECC affine only** (MOTION_AFFINE or EUCLIDEAN). Target = face ROI on structure canvas.
3. Accept only if **ECC score ≥ 0.85** and **SSIM vs target ≥ 0.55** (prefer ECC ≥ 0.99, SSIM ≥ 0.98).
4. Reject ORB/homography full-RGB as primary paste (PATH1D failure mode).

### 1.4 Hard paste (the 1E core — non-negotiable)
- Mask = **edge feather only** (≈32–40 px) × **person matte** (left-center; kill sky-right)
- **Interior person mix ≈ 0.92–1.0** of model composite RGB
- **NOT** multiband pyramid with soft base (PATH1B wash)
- **NOT** successive soft blends that re-average with L0 (PATH1C)
- Color match mild only (strength ≤ 0.4)

### 1.5 Optional HF inject (secondary, gated)
From `94b67111` / `3707b092` / `b3166b07` close-ups:
- Inject **high-frequency residual only** (not full RGB geometry)
- Mask = edge × person × **conf map** (LP abs-diff); **no conf floor on sky**
- Require conf > ~0.35 before inject
- After inject: **force sky restore** from structure base
- If LP-SSIM vs base face < 0.85 → discard inject, keep hard model paste

### 1.6 Quality gates (must pass before calling result FINAL)

| Gate | Threshold |
|------|-----------|
| Face Laplacian var | **≥ 400** (PATH1B ~99; fail if < 250) |
| LP-SSIM vs structure face | **≥ 0.90** |
| Right-sky mean\|Δ\| vs structure | **≤ 5** (ghost check) |
| ECC of model paste | **≥ 0.85** |
| No double-face / mirror | visual + structure SSIM |

### 1.7 Export
- Full final: JPEG quality **≥ 97**, `subsampling=0`
- Face crop proof: **PNG lossless** (`FACE_PATH1E.png`)
- Record SHA256 + L-<12> in MANIFEST

---

## 2. Forbidden operations (explicit)

1. Soft multiband as the **only** face path (PATH1B)
2. ORB/homography **full RGB** paste of close-up HD into face ROI (PATH1D ghosts)
3. Mask mean ≪ 0.5 on person interior while claiming "used HD"
4. Claiming FINAL matches 94b6/3707 without micro sharp proof
5. Replacing PATH1E with PATH1F/1C/1D without user unlock
6. Text-to-image from memory for heroine face (must reference HD assets)

---

## 3. Asset map (locked)

| Role | Asset / file |
|------|----------------|
| PATH1E CLEAN final (LOCK DEFAULT) | `a2141161-5a72-4a64-b51f-53912f5b8519` · `SETN60_PATH1E_CLEAN_HD_FACE.jpg` |
| PATH1E HF variant (optional) | `4c4c9ca6-c9f5-4da6-81b9-23f5b6b191bd` · `SETN60_PATH1E_HD_HF_FACE.jpg` |
| PATH1F MAX (not default) | `79ad1c9e-9553-49db-bc8d-1b1929f7421a` |
| PATH1F CLEAN (not default) | `ad0befda-48bf-4f12-a270-6fbb9f2d6773` |
| HD face refs | `b3166b07…`, `94b67111…`, `3707b092…` |
| L0 | `d87e75cd…` / `0_l0/L0.jpg` |

---

## 4. Procedure checklist (every future face reassembly turn)

```
[ ] Load structure canvas = detail-xfer 60 @ 5376×3024
[ ] Crop FACE_ROI_FINAL / HEAD_ROI_FINAL
[ ] ECC-warp pose-matched model face; score≥0.85
[ ] Hard paste edge-only + person matte; interior ≥0.92
[ ] Optional: conf-gated HF from 94b6/3707/b3166; sky restore
[ ] Gates: sharp≥400, LP-SSIM≥0.90, skyΔ≤5
[ ] Write FINAL + FACE PNG + SHA + update MANIFEST face_lock=PATH1E
[ ] Do NOT ship PATH1B/1C/1D as final
```

---

## 5. Unlock

Only the user saying **「解鎖 1E」** or **「改用 1F/其他」** may change `face_lock`.  
Until then every SET-N grid60 face reassembly **must** run PATH1E.

---

## 6. Relation to body grid

- 60-cell proportional detail-transfer remains for **non-face** body/scene.
- Face/head channel is a **dedicated override** (1E), not another soft residual cell paste.
- Structure lock still wins on geometry; 1E only upgrades person HF/RGB inside ROI.

---

## 5. FAR-FIELD parameter scaling (see UNIFIED §0.11)

When face height \(h_f\) is small (elevated / bird / graffiti full-scene):

- `feather_px = clamp(round(0.12*h_f), 2, min(40, 0.22*h_f))`  — do NOT keep 32–40 on tiny faces
- `s < 0.35` → use HEAD_ROI, larger relative margin
- `mix_interior` 0.65–0.78; `color_match` up to 0.45; HF conf ≥0.55 or skip HF
- World-edge blur only on matte exterior 0–3px; never Gaussian the face core
- Example FAR (`b0b6e9bb`): {"face_h_px": 120, "scale_vs_near": 0.316, "feather_px": 14, "roi_margin_frac": 0.387, "mix_interior": 0.78, "color_match_strength": 0.45, "conf_hf_min": 0.55, "use_HEAD_ROI": true, "ecc_min": 0.85, "edge_world_blur_px": 2, "gate_face_lap_min": 224}

