# 全圖 NCNN＋PBI 省記憶體 · NCNN_FULLFRAME_PBI_MEMSAFE / NFP-M

| 項 | 值 |
|----|-----|
| **正名** | **全圖 NCNN＋PBI 省記憶體** |
| **短碼** | **NFP-M** · NCNN Fullframe PBI Memsafe |
| **憲節** | **§0.12.59**（連動 PBI §0.12.55 · NCPG R6 §0.12.56 · R6c NCNN 鏈） |
| **一句** | **全圖 4×：先寫 RAW 落盤，再 strip 做 PBI** · 禁 all-in-RAM 整幅 residual |
| **樣板圖** | warrior mud-hammer 1792×1008 → 7168×4032 · engine `NCNN_GENERAL_x4v3` |
| **工具** | `work/scripts/r6c_pbi/run_ncnn_fullframe_pbi.py`（UP-engine 鏡像 `tools/ncnn_fullframe_pbi.py`） |
| **merge main** | **NO** 直至工具 LOCK 且權重路徑可重跑 |
| **asof** | 2026-11-02 |

## 與既有招

| 招 | 關係 |
|----|------|
| **PBI** §0.12.55 | 本節強制 **luma_only** 全圖預設；禁 RGB residual 當正式鏈 |
| **R6c NCNN peep** | peep／24 probe 仍用 `run_r6c_ncnn.py`；**全圖**改走本節 |
| **Siax / NMKD** | **不是** 本節引擎 · `not_siax=true` |
| **GENERAL_x4v3** | RealESRGAN general → pnnx → `*.ncnn.param/bin` |

## 別名

全圖 NCNN 省 RAM · RAW-first PBI · memsafe fullframe SR
