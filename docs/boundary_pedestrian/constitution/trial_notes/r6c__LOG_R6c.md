# R6c · NCNN 加速 GENERAL（選項 ③）

## 環境限制
- `realesrgan-ncnn-vulkan` 需 `libvulkan.so.1` · 本機無
- workspace **noexec** · 官方 binary 無法直接 exec
- 改用：**pnnx 轉 ncnn** + **pyncnn CPU**

## Bench 64×64→256
見 `bench/BENCH_NCNN.json`

## Fullres
- P0/P1 2048 · NCNN GENERAL · 4× residual 保留
- ridge align 閘

## 誠實
NCNN CPU 未必大幅快過已很輕的 GENERAL PyTorch；若 speedup≈1 則收益在 **portable/部署** 而非本機 wall-time。
