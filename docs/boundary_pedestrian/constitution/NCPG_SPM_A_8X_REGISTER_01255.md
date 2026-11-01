# §0.12.55 NCPG · SPM-A 八倍子板註冊（NCPG_SPM_A_8X_REGISTER）

> asof 2026-10-31 · LOCK · 用戶審計 R5：256 誤寫 4×VM／整張 HF 當 residual／feather 抵消 → 修正並定版

## 0.12.55.A 一句
**512 PEEP → 48 unique SIAX 探針 → 1024 新像素 Hybrid → ridge 硬閘 → 8× 子板註冊 → Zoom In 讀原生 · Zoom Out 讀 4× VM**

## 0.12.55.B 解析度階梯（接 R4 §0.12.54）
| 層 | 尺度 | 角色 |
|----|------|------|
| FULL | 1× | 座標根 |
| 4× Virtual Master | 全局 4× | 位置底板 · **不**被 8× 降採樣覆蓋 |
| PEEP3 L0 | 512 | 探針輸入 |
| SPM-A Hybrid child | **1024** | **主交付原生 HF 子板** |
| 相對 FULL | **8×** | Zoom In 層 |

座標（peep3 樣板）：
\[
X_0=1828,\ Y_0=2288\ (\text{4× VM 槽 512×512})
\]
\[
\mathrm{child}[u,v]\ \leftrightarrow\ \mathrm{VM4}\!\left[Y_0+v/2,\ X_0+u/2\right]
\]

## 0.12.55.C residual 定義（寫死）
\[
\mathrm{Hybrid}=\mathrm{LP}(\mathrm{Lanczos}\,2\times)+\underbrace{(\mathrm{filled}\cdot M\cdot G_{\mathrm{ridge}})}_{\mathrm{residual\_new}}
\]
| 項 | 規定 |
|----|------|
| filled | SPM-A 探針 residual 多尺度填洞 |
| M | 探針權重 / rough_boost |
| G_ridge | 母 wire ridge 硬閘 · **residual_ridge_alignment ≥ 0.65** |
| 禁 | `HF = child − GaussianBlur(child)` 當「新增 residual」 |
| 禁 | 整張 Hybrid 高頻當 GNP 新像素 |

## 0.12.55.D 探針
| 項 | 值 |
|----|-----|
| 模型 | `4x_NMKD-Siax_200k.pth` · OldESRGAN `model.*` **strict** |
| TILE | 64² · 目標 48 |
| 必記 | **unique_probe_count** · **probe_coverage** · 禁止只報 TILE_N |
| 不足 48 unique | 可 overlap_pad · **TAG 分開** · 不可謊稱 48 獨立 |

## 0.12.55.E 融合 / feather
單板／多板：
\[
\Delta_{\mathrm{acc}}=\sum_i w_i\Delta_i,\quad
I_{\mathrm{out}}=I_{\mathrm{base}}+\frac{\Delta_{\mathrm{acc}}}{\max(1,\sum_i w_i)}
\]
| 禁 | 單 tile 時 `sum_wD/sum_w` 令 feather≡1 抵消邊緣 |
| soft preview | 可降採樣 residual 入 4× 槽 · **JPG only · 非 primary** |

## 0.12.55.F 閘
| 閘 | 閾 |
|----|-----|
| residual_ridge_alignment | **≥ 0.65** |
| struct_ncc LP↔Hybrid | ≥ 0.97 |
| spill outside ridge | 記錄 · 宜 < 0.40 |
| native_roundtrip | 證明 1024→512→1024 會殺 Tenen · **故禁縮回主交付** |

## 0.12.55.G 與 S1HL
- **預覽／探針** = SPM-A（本節）
- **裙 8× 定版 strip** = L0｜LP｜res_ridge｜Hybrid｜parent（**不再二次 SIAX**）
- 臉鎖 a8b 仍走 S1HL T3（全身定版時）· 本 peep 衣板可無臉

## 0.12.55.H 樣板
| 檔 | 角色 |
|----|------|
| `CHILD_SPM_A_1024_NATIVE_8X.png` | R5 soft residual 子板 |
| `CHILD_SPM_A_1024_RIDGE_8X.png` | R5b ridge 硬閘 **定版** |
| `S1HL_STRIP_SKIRT_8X.jpg` | 定版 strip |
| `ACCEPT_NCPG_SPM_A_R5B.json` | 閘 |

## 0.12.55.I 狀態機
`PEEP3_512` → `SPM_A_48` → `HYB_1024` → `RIDGE_GATE` → `REGISTER_8X` → `S1HL_STRIP`
禁：`HYB_1024` → `resize 512` → `paste VM4` 稱 primary。
