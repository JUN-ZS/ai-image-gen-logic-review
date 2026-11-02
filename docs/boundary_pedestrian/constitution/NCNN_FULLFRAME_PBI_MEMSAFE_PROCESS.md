# NFP-M · PROCESS

1. 備 `*.ncnn.param` + `*.ncnn.bin`（GENERAL_x4v3 · pnnx）  
2. `run_ncnn_fullframe_pbi.py --input --out-dir --param --bin`  
3. 確認 out 有 `*_RAW.png` **早於** `*_PBI.png` 時間戳／流水線 step  
4. 讀 `*_RESULT.json`：`default_pipeline=write_raw_then_strip_pbi`  
5. 需要 G7/G8/S1S2 時 **另掛** peep 閘工具 · 不混稱本節已品質合格  
6. 與 Siax 對照時 **另目錄** · 勿覆寫 Siax 交付檔名
