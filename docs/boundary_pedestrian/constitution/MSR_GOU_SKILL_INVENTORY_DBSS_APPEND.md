# MSR 技能庫追加 · 單白殺升 (DBSS 01261)

| 代碼 | 中名 | 英名 | 編號 | 一句 |
|------|------|------|------|------|
| DBSS | 單白殺升 | Single White-Kill Light Upscale | 01261 | 非高清殺白→PATH1E ECC 貼母圖→Lanczos+Imagine light 回扣升清 |

## 調用提示

```
技：單白殺升 / DBSS
輸入：A 母圖 + 全臉 ROI
順序：NONHD_WNK → PATH1E → ECC paste → Lanczos 與/或 Imagine light
禁止：HD 殺白預設；降 PIXEL；半臉；把輕量升清當 quality PASS
```

## 關聯

- 上游可選：WNK 全圖、MCP（非必須）
- 下游可選：NCNN 全幅 + strip PBI（另技 NFP-M，不併入 DBSS 必做）
- 對立分支：HD 正方殺白再貼（收據分開）
