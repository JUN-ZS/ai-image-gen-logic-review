# L0 全抽首圖部署

**規則：** 應先在沒有字的圖時，就做全抽的首圖部署。

## 順序
1. `L0_CLEAN` — 無字、無 HUD、無標題
2. **立刻** every-object 全抽 → 物件庫
3. 各 cutout 獨立放大修正（同像素源）
4. pure collage → `L0_DEPLOY_NOTEXT`
5. 之後才 TYPE／HUD／藝術字

## 為什麼
- 有字圖再抽會把字/HUD 綁進 cutout，污染物件庫
- 跨源貼臉才會雙影；L0 整層 cutout 拼貼無 PIXEL 衝突
- 字永遠是最後一層，可換、可審、可 SHA

## 驗收
- [ ] 存在 `L0_CLEAN` 且畫面無字
- [ ] `cutouts/` 含 woman／sphere／bg 至少三層
- [ ] `L0_DEPLOY_COLLAGE_NOTEXT` 無字可還原主體
- [ ] 有字圖只允許在 L0 部署完成之後生成
