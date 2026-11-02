# NFP-M · 全圖 NCNN＋PBI 省記憶體（§0.12.59）

方法入憲：`docs/boundary_pedestrian/constitution/NCNN_FULLFRAME_PBI_MEMSAFE_*`

鐵序：**先 RAW 落盤 → 再 strip PBI** · `--unsafe-all-in-ram` 拒絕。

```bash
python work/scripts/r6c_pbi/run_ncnn_fullframe_pbi.py \
  --input BASE.jpg --out-dir out \
  --param general_x4v3_ts.ncnn.param --bin general_x4v3_ts.ncnn.bin
```

merge main: **NO** · quality 預設 false · not_siax。
