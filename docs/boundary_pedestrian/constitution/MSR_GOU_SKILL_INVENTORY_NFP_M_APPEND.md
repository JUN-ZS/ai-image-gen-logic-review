# MSI 附錄 · NFP-M（§0.12.59）· 2026-11-02

> 掛到 `MSR_GOU_SKILL_INVENTORY_01238`／NAME 的連動列 · **不整表覆寫**

| 正名 | 碼 | § | 生成時角色 |
|------|-----|---|------------|
| **全圖 NCNN＋PBI 省記憶體** | **NFP-M** | **0.12.59** | 全圖 4× NCNN GENERAL · **RAW-first** · strip PBI · 禁 all-in-RAM |
| （連動）防藍注入 | PBI | 0.12.55 | 全圖預設 luma_only |
| （連動）NCPG R6 full-res | — | 0.12.56 | 4× MODEL→4× residual／CHILD · 禁砍 2× |
| （對照）R6c peep NCNN | — | R6c | peep 鏈 · 非全圖預設入口 |

**FAIL→備：** 見 `NCNN_FULLFRAME_PBI_MEMSAFE_DO_NOT_REPEAT.md` · E-NFP-01..10
