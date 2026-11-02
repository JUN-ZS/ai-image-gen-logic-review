# 掩抽拼 · DO_NOT_REPEAT

| 碼 | 錯 | 改 |
|----|-----|-----|
| E-MCP-01 | 從 **B** 抽白當 MASK | MASK **只從 A**（WNK 等） |
| E-MCP-02 | 全圖 soft α 當「拼回」 | **硬寫 MASK 區**；邊可極輕 feather 但核 α≈1 |
| E-MCP-03 | MASK 用 bilinear 糊成半標籤 | **NEAREST** |
| E-MCP-04 | 把定版母圖整圖縮成 1792 當完成 | preview 另檔；master shape 鎖 |
| E-MCP-05 | B 與 A 不同構／未對位仍 CLIP | 先對位或 fail-closed |
| E-MCP-06 | 10d59 未 staged 卻默認成功 | 顯式 fallback 或 FAIL |
| E-MCP-07 | 把 MCP 叫成 PATH1E／ECC | MCP≠plate；ECC 是後段 peep 對位 |
| E-MCP-08 | 把 MCP 叫成 NCNN／PBI | 升清是 NFP-M，不是抽貼 |

asof 2026-11-02
