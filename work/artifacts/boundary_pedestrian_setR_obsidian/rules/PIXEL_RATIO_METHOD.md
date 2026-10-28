# PIXEL_RATIO 臉回原圖 · 座標校正 + 真臉鎖

> ASOF 2026-10-26T18:14:00Z · 對位法審核後 · TRUE_FACE_LOCK 入憲

## 空間

| 符號 | 含義 |
|------|------|
| D | dst 全圖 |
| S | src 原生 |
| C / C↑ | cell 窗 / ×U 放大 |
| F_d / F_s | 臉框（**必須真臉**） |

## 公式（校正）

```
s_face = sqrt( (w_d/w_s) * (h_d/h_s) )
nw, nh = size_after_Lanczos(S, s_face)
s_eff  = 0.5 * (nw/W_s + nh/H_s)          # ★ 縮放後必重算
place_tl = c_d - c_s * s_eff               # FULL_SRC_PLACE
p_D = p_S * s_eff + place_tl
p_S = (p_D - place_tl) / s_eff

# FACE_CROP_DIRECT（軟身份首選 · 真臉）
crop_S = expand(F_s, pad≤0.10)
place_crop = c_d - (c_s - crop_S.tl) * s_face
paste only ellipse on expand(F_d, pad≤0.10) + hammer_kill + kill_wall

# FAT
face_C  = face_D - cell_tl
face_C↑ = face_C * U
reinsert: Lanczos(C↑ → cell_size) @ cell_tl
center check: face_C↑.c / U + cell_tl == c_d
```

## 真臉鎖（§0.12.14.F · SET-R aerial 2455522d）

| 項 | 值 |
|----|-----|
| F_d LOCK | **[648, 118, 92, 108]** |
| kill_wall_x | **620** |
| 錯框禁 | (528,102) 頸/C-ring；(492,154)；(535,108)；(615,118) 偏左 |
| 閘 | center_err=0 · δ_cring=0 · δ_hairL=0 · 熱圖只亮 x∈[650,738] |
| 用戶 | bb5fb0fa「你對後, 要是改對臉的」 |

```
C-ring strip clean ≠ 臉完成
改對臉的 = 朝相機臉，不是銅盤／頸／左髮誤認
```

## 禁

- expand sx=0.35/syt=0.55（鬼臉）
- float s 算 place、int resize 出圖（中心漂）
- 銅盤當臉 · 錯框當 F_d
- letterbox 512 當 S
- face_D * U 不做 cell 原點減除
- 無 kill_wall 左溢

## 閘

|c_s→c_d| < 0.5px · δ_cring=0 · outside_chg≈0 · GHOST_PERSON=OK · 熱圖∈真臉

詳見總憲 **§0.12.14 / §0.12.14.F** · `PIXEL_RATIO_COORD_CORRECTED.json`
