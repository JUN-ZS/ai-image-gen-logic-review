# NCPG SPM-A 8X · 勿再犯（§0.12.55）

| 碼 | 禁 |
|----|-----|
| E-NCPG-40 | 算了 512 Hybrid 卻只把 256/512 寫入 4× VM 當主交付 |
| E-NCPG-41 | 1024→512 降採樣貼 4× 槽並稱保留 8× HF |
| E-NCPG-42 | `HF=child−Blur(child)` 冒充 SPM residual_new |
| E-NCPG-43 | residual_ridge_alignment < 0.65 仍 ACCEPT 定版 |
| E-NCPG-44 | TILE_N=48 但 unique_probe_count 未記／全是 overlap 卻稱 48 獨立 |
| E-NCPG-45 | 單 tile feather 被 sum_w 正規化抵消 |
| E-NCPG-46 | S1HL 定版後再跑第二次全幅／全板 SIAX（E-GS-47 連動） |
| E-NCPG-47 | 無 Transform Register 的「感覺對位」貼子板 |

asof 2026-10-31
