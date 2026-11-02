# §0.12.60.S 母修全鏈 · AMRS

> asof 2026-11-02  
> 編排棧 · 不取代各組件專章

## 資料流

```
A母
  │ WNK
  ├─► A_WNK
  └─► MASK ──► MCP(B另母) ──► CLIP ──► A_paste
                                           │
                              ROI peep ────┤
                              PATH1E plate ┤
                              ECC 硬貼 ────┤
                              DHY（可）────┤
                                           ▼
                              A_refined ──► NFP-M（可）──► 7k 定版
```

## 模組檔

| 步 | 工具／附件 |
|----|------------|
| WNK | `WHITE_NOISE_KILL_NAME.md` · `tools/wnk_white_noise_kill.py` |
| MCP | `MASK_CLIP_PASTE_MCP_*` · `pipe_mask_clip_paste.py` |
| PATH1E | `PATH1E_PLATE_ECC_LAW.md` · `pipe_e357_ecc_hardpaste.py` |
| NFP-M | `NCNN_FULLFRAME_PBI_MEMSAFE_*` · `ncnn_fullframe_pbi.py` |
| 編排 | `pipe_A_master_orchestrator.py` |

## 驗收欄位（每步 JSON）

`step` · `*_sha` · `out_wh` · `pixel_drop=false` · `quality_qualified=false` · `e3_speed_claim=false`

## 樣板 SHA（本輪）

| 步 | SHA 前綴 |
|----|----------|
| A_WNK | `0d1dd797…` |
| A_paste | `2d37472a…` |
| NFP-M 例 | `0703915d…` / `c743e3dc…` |
| ECC 定版 | `72e7e87f…`（7168） |
