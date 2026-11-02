# face俱圓 · DO_NOT_REPEAT · FJY_01262

## 禁止再犯

1. **硬鎖錯誤 aspect ratio**  
   dens 約 1280×1400 (ar≈0.91) 時，強制 `2:3` → 1152×1728 (ar≈0.67)  
   → 構圖被拉長、ECC 掉到 ~0.65、gate FAIL。  
   **應**：`aspect_ratio=auto` 或近 dens／1:1；**用戶未限 ratio 時不得自限錯比**。

2. **把 1920×1080 contain 當成 plate 幾何**  
   1920×1080 黑邊 contain 只可作 SHOW 展示；ECC／貼回必須用 dens 框或 free long plate，不可把 letterbox 當 peep。

3. **半臉／五官裁**  
   缺額、缺下巴、只眼睛嘴 → 不算 face俱圓；貼回易露縫、ECC 假高或假低。

4. **setS／庫存異姿硬換本場**  
   舉錘板硬貼揮錘母圖、身分庫存板硬蓋本場 peep —— 違同姿；只可作身分參考，幾何必須 dens／本場 peep。

5. **ratio 錯仍標 quality PASS**  
   old 2:3 plate ECC＜0.85 不得寫成 strict paste PASS。

6. **降 PIXEL 貼回**  
   母圖 WH 必須鎖死；預覽半解像度（如 896×504）不得當「母圖變低 pixel」證據。

7. **dens 細節期望留在 1792 臉槽**  
   dens 1280 貼回 320 槽＝×4 下採樣；高 PIXEL 產物是 dens／plate 本身，不是 1792 母圖臉槽。

## 應做

- 全臉 ROI（額→下巴齊）  
- plate 比例跟 dens（auto）  
- dens 幾何 + 可選身分 ref  
- ECC ≥ 0.85 才 raw paste  
- 收據分：aspect、ecc、gate_raw、pixel_drop  
