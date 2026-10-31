# R6c · ③ NCNN 加速 GENERAL

## 環境
- 官方 `realesrgan-ncnn-vulkan`：缺 `libvulkan` + workspace noexec
- 實際：**pnnx 轉 ncnn** + **pyncnn CPU**

## 毒與修
| 碼 | 現象 | 修 |
|----|------|-----|
| E-R6C-01 | `PIXEL_BGR2RGB` 輸出偏 · fullres sn~0.43 | `cv2.BGR2RGB` + `PIXEL_RGB` |

## Bench 64→256
- mae NCNN↔PT ≈ **1.53e-05**
- PT **56.2 ms** · NCNN **31.5 ms** · speedup **1.78×**

## Fullres
見 ACCEPT_R6c.json · 應對齊 R6b GENERAL 結構閘
