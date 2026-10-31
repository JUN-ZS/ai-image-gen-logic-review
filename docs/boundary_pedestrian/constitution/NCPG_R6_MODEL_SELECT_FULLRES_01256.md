# §0.12.56 NCPG R6 · MODEL-SELECT + FULL-RES REGISTER（LOCK 鐵律）

> 用戶審計 2026-10-31：R5b = 能工作的 SIAX 注入鏈 · **非** 全模型選冠；SIAX 4× 被縮 2× 抽 residual = 主浪費

## 0.12.56.A 一句

**4× MODEL OUTPUT → 4× RESIDUAL / CHILD REGISTRATION**  
不准再用 4× 模型花完整推論成本，最後只保留 2× 細節。

## 0.12.56.B R5b 已用 vs 未用

| 技術 | R5 鏈角色 | 曾否同條件選優 |
|------|-----------|----------------|
| NMKD-Siax | 48 探針 HF residual | 否 · 指定使用 |
| SPM-A | residual 填補 | 否 |
| Ridge hard / S1HL / NCPG | 閘／架構 | 流程約束 · 非模型選優 |
| Dense Warp / PG-VTON / SeedVR2 / Superscale / RealESRGAN / LSDIR | — | **未** 公平比較 |

## 0.12.56.C 性能與解析度毒（R5b 根因）

1. **DEVICE=cpu** · PyTorch 逐 probe 64²  
2. **48× peep**（P0+P1 → 96 次）獨立 forward  
3. **E-R6-01**：`siax 64→256` 再 `INTER_AREA →128` 才 vs 2× LP → **最高頻 Nyquist 殺**  
4. **E-R6-02**：hyb512 算過卻 child=hyb256 寫 VM  

## 0.12.56.D 鐵序 R6

```
P0 母 peep 固定
→ MODEL-SELECT 同 tile 競賽（結構NCC · Tenen · wire align · 時間 · 原生尺寸）
→ 勝出引擎 **full-res 4×** residual（禁 4×→2×）
→ ridge hard gate @ native 4×
→ CHILD 原生 PNG 註冊（peep×4 · 例 512→2048）
→ Virtual Master 座標 scale=4 · 禁縮回 peep 當主檔
→ JPG 只預覽
```

## 0.12.56.E 競賽候選（未冠 · 實驗設計）

| 區 | 第一候選 | 第二 | 目標 |
|----|----------|------|------|
| 金網裙 | Siax | LSDIRCompact | 細絲開網 |
| 金絲高光 | Siax | Superscale-SP | 邊／反光 |
| 胸甲 | Real-ESRGAN | Siax | 拓撲 |
| 臉／皮 | 保守 | SeedVR2 對照 | 身份 |
| 背景 | Real-ESRGAN | SeedVR2 | 星點 |

**引擎優先測：** NCNN Siax 速度 vs PyTorch；batch 4–8 probes；OpenVINO；有 GPU 再 Vulkan/CUDA。

## 0.12.56.F 交付

| 檔 | 格式 |
|----|------|
| FULL 4× Master | Lossless PNG／TIFF |
| P0/P1 8×＝peep×4 子板 | Lossless PNG 主交付 |
| 預覽 | JPG only |
| 禁 | 為湊 30MB 加噪／膨脹 |

## 0.12.56.G 閘

- residual_ridge_alignment ≥ 0.65  
- struct_ncc ≥ 0.97  
- child_hw == peep_hw × model_scale（SIAX=4）  
- 主交付 ≠ soft board ≠ chat 600px  
