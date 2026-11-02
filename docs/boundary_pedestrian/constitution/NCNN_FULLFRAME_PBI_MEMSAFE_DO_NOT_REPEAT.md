# NFP-M · DO_NOT_REPEAT（全圖 NCNN＋PBI）

> 生成／升清前必掃 · 來自 warrior OOM 與 R6c 血教訓

| 碼 | 禁 | 改為 |
|----|----|------|
| **E-NFP-01** | SR 全圖 float canvas + 整幅 LP + 整幅 PBI **同時在 RAM** | **先寫 RAW 落盤** · 再 strip PBI |
| **E-NFP-02** | 把 `--unsafe-all-in-ram` 當預設或繞過 refuse | 腳本 **必須 refuse** |
| **E-NFP-03** | 全圖走 peep 腳本 `run_r6c_ncnn.py` 當完成 | peep≠全圖 · 全圖用 **NFP-M 工具** |
| **E-NFP-04** | 宣稱 NCNN 輸出 = Siax／NMKD 等價 | `not_siax=true` · 分開 A/B |
| **E-NFP-05** | 無 param/bin 仍宣告「可重跑 PASS」 | limits 寫清 · clean-checkout 不能假重跑 |
| **E-NFP-06** | 4× 模型輸出再 **砍成 2× residual 當主交付** | 遵守 §0.12.56 **4×→4× CHILD** |
| **E-NFP-07** | 事後洗藍冒充 PBI PASS | 升清時 **luma_only residual**（§0.12.55） |
| **E-NFP-08** | wall_s 當 E3 speed claim | `e3_speed_claim=false` |
| **E-NFP-09** | 只改 JSON 把 quality 改 PASS | 圖＋SHA＋閘 同 commit |
| **E-NFP-10** | merge main 未 LOCK 工具／權重契約 | **merge main: NO** 直至可重跑 |

## 記憶體經驗值（備註 · 非硬閘）

- 7168×4032×3×float32 ≈ 數百 MB **級** 單畫布；雙畫布 + 中間量易觸 OOM  
- strip 預設 256 BASE px 可調小以再省峰
