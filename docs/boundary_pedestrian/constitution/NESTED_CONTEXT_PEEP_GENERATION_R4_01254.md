# NCPG R4 · Coordinate-Preserved High-Resolution Stitch
> asof 2026-10-31 · §0.12.54 · LOCK from user audit

## 一句
**生成解析度 ≠ 人物原圖解析度 ≠ 主畫布解析度** 必須分階；PEEP2 原生像素禁止縮回 2× Master 當主交付。

## 致命舊毒
| 碼 | 毒 |
|----|-----|
| E-NCPG-30 | PEEP2 已 4× 級 · Master 仍 2× → 縮回殺 Nyquist 新 HF |
| E-NCPG-31 | 單用 ECC 仿射當衣服曲面對位 |
| E-NCPG-32 | 整張 RGB Alpha 貼紙 · 蓋掉身形/光影/開網 |
| E-NCPG-33 | 單一 HF-Sobel NCC 同時判結構+新細節 → 真細節被當漂移拒 |
| E-NCPG-34 | 把 R3 全拒當 densify 成功（R3=安全拒收測試 only） |

## 解析度階梯（寫死）
| 層 | 尺度 | 角色 |
|----|------|------|
| FULL | 1× (e.g. 1792×1008) | 原圖座標根 |
| PEEP1 / R2 board | 2× peep | 衣區工作板 |
| PEEP2 child | 局部 4× | **原生 HF 子板 · 不縮** |
| Virtual Master | 全局 4× | 座標底板；Zoom In 讀子板 |
| Preview | 2× JPG | 僅預覽 · 非主檔 |

## 座標公式
裁切 parent 上 \((x_0,y_0)\)，context pad \((p_x,p_y)\)，生成倍率 \(g\)：
\[
X_0=g(x_0-p_x)+X_{\mathrm{garment}},\quad
Y_0=g(y_0-p_y)+Y_{\mathrm{garment}}
\]
子板原生像素 **直接** 放入 VM；letterbox offset 記入 Transform Manifest。

## 分頻融合
\[
M_{HR}=P_{HR}+\alpha\,G_{mask}\,R_{HF}
\]
- LP/MP ← Parent（身形·摺痕·拓撲）
- HF ← Generated Child（對位後）
- Chroma 限漂
- 融合發生在 **4× VM / 子板** · 非 1792

## 對位
1. 座標映射主（Transform Manifest）
2. ECC 粗對齊
3. **Dense Warp** 非剛性（裙褶/胸甲）— ECC 不足

## 閘（拆開）
| 閘 | 測什麼 |
|----|--------|
| Structural NCC | LP+下採樣 · 輪廓/開網 · ≥0.90 |
| HF Alignment | 新絲是否沿母方向 |
| Mask Spill | 禁臉/髮/背景 |

## R3 定性
**成功的安全拒收測試** · n_accept=0 · 非高清貼回成功。

## R4 狀態機
`COORD_READY` → `GEN_STRUCTURE_LOCKED` → `WARP_OK` → `HF_FUSE_NATIVE` → `VM_REGISTERED`
禁：`GEN` 後直接 `resize→2× master` 稱 primary。

## 研究旁系（不宣稱可 clone 即跑）
- FabricTryOn (SIGGRAPH 2026 方向): material-normalize → fabric swatch → context tile；借兩階段設計 · 非現成推論全家桶
- Pix2Surf / SPATT: dense clothing correspondence / UV prior
- ComfyUI Crop&Stitch: context crop/mask stitch · **不**自動保高於畫布的像素 → 仍要 VM 座標層


## 連動 §0.12.55
SPM-A **8× 子板註冊**（NCPG_SPM_A_8X_REGISTER）：見 `NCPG_SPM_A_8X_REGISTER_01255.md`。PEEP3 512→1024 child · ridge≥0.65 · 禁縮回 4×。
