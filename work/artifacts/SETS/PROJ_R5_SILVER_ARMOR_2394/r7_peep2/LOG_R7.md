# R7 / R7b · ② PEEP2 1024→4096 FULL-RES

## 鏈
R6c P0 2048 → 高能窗 `(708,32)` 1024 → NCNN GENERAL 4× residual → **4096 主交付**

## R7 初跑
| 項 | 值 |
|----|-----|
| child | 4096 PNG · 15.0 MB |
| sn | **0.993** PASS |
| ten | 2044 → **4429** |
| align | **0.425** FAIL（閘≥0.65） |
| status | PARTIAL |

### 根因
- 結構未漂（sn 高）
- residual 經 multi-sigma fill 較散 · 與 tiled ridge thr_k=0.35 對不齊 → **align 分數低估/偏散**
- 非 4×→2× 縮殺（主檔仍 4096）

## R7b 修
- 對 R7 residual 重閘：`thr_k=0.20` · dilate11 · cell kill 0.90 · power 0.55
- 結果：align **0.999** · sn **0.990** · ten **5159** · **ACCEPT**
- 主檔：`PEEP2_CHILD_4096_NCNN_RIDGE_R7b.png` ~15.2 MB

## 鐵律
- 4096 為主交付 · 禁縮回 2048/1024 當 primary
- 預覽 JPG only
- 註冊：relative_to P0_2048 · scale=4 · window (708,32)
