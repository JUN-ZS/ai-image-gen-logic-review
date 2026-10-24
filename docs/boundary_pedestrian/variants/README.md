# 變體全量 ID 展開 + 已出圖 × 總庫方法對照

## 本步做了什麼

1. **expand-full-csv**：機器展開合法乘積 ID（**只清單、不出圖**）
2. **GENERATED_ASSETS_CATALOG_MAP.csv**：每張已落地圖對應總庫四線哪些方法
3. **GENERATED_VS_CATALOG_COVERAGE.json**：總庫條目覆蓋 YES/NO/SAMPLE

## 全量 ID 計數

見 `VARIANT_IDS_FULL_SUMMARY.json`（合計約 **3723** 列，含 VIDEO 與 IMPACT4 層）。

主桶：

| bucket | 約數 | 對應總庫 |
| --- | --- | --- |
| HARD_T_192 | 2304 | I-01…I-05 × I-18 × H0–3 × S-01…3 |
| HARD_T_H2_IMPACT4 | 768 | H2 × 192 × PACK_IMPACT_4 四鏡（S01） |
| HARD_DUAL48 | 288 | I-19 × (T2\|CROSS) × 3 style |
| HARD_ROD | 60 | I-10/11 × I-22 × style |
| HARD_MULTI | 60 | I-16/17 × I-22 × style |
| HARD_PLANT_* | 102 | I-13…15 |
| SOFT_IMAGE | 81 | 邊界行人柔性 × style × shot |
| VIDEO_* | 60 | V-01…V-10 展開 |

## 已出圖用了什麼方法（摘要）

| 產物 | 幾何 | 鏡頭/美術 | 敘事 | VIDEO |
| --- | --- | --- | --- | --- |
| `i20/` ×6 | 柔性 NONE（ACT3 敘事錘可入） | S-01；I-20 | 六幕完整 | — |
| `i21/` ×6 | 柔性／隱喻 | **S-02**；I-21 | 六幕完整 | — |
| `mv26/` ×26 | ACT3 硬鏡偏 **I-16 MULTI**；其餘 SOFT/道具錘 | 槌2 MV 鏡頭包；S-01 | 六幕×多鏡 | — |
| `hard_samples/p3_multi/` ×3 | **I-16/I-17 MULTI H2** | **I-22** W01/W04/W07；S-01 | ACT3 碎裂 | — |
| `hard_samples/p4_t_h2/` ×8 | **I-01 + I-04 H2 + I-18 軸抽樣 8/192** | CAM02-like；S-01 | ACT3 碎裂 | — |
| 會話 36s MV | 敘事 | S-01 | 六幕 | **V-04 I2V + V-09 路線 + ffmpeg** |

### 尚未用圖像落地的總庫方法（重要）

- H0 / H1 / H3 系統抽樣  
- 雙 T（I-06/07）、厚十字（I-08/09）、線形棒（I-10/11）  
- 種植側柄／外端（I-13…15）  
- I-18 全 192、I-19 全 48  
- I-22 其餘 7 種洗圖  
- S-03 超現實、S-04 幾何驗收  
- V-01/02/03/05/06/07/08/10  

完整逐檔對照：`GENERATED_ASSETS_CATALOG_MAP.csv`。
