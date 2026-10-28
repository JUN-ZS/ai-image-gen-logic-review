# MESH STITCH — 騙公式已殺 / V5 正解

## 騙的母底公式（必須永久禁用）

### CHEAT_A · V1 結構鎖假進度
```
plate = base*(1-0.55*α) + gen*(0.55*α) + HF*1.1   # 窄 mask
```
結果 ≈ base（mad 小但細節沒上）→ 騙「有拼」

### CHEAT_B · V2/V3 全色 GEN 主導（失敗區放大元兇）
```
plate = base*(1-α) + gen*α     # α≈0.9, full RGB
```
GEN 低頻（姿勢/光/金比例）整塊灌入全圖 → 放大圖好看、全圖更差

### CHEAT_C · V4 錯 HF 替換
```
plate = base + α*(gen_HF - base_HF)
```
GEN 是 ~1400 升到 4608，HF 比母圖軟 → 用軟 HF 換掉硬 HF → lap 下降變糊

## V5 正解（band-pass 網紋 + 保留母圖銳度）
```
gen_w  = ECC_warp(gen → base)
gen_m  = Lab_match(gen_w → base)          # 去色漂
gen_MF = blur(gen_m,1.2) - blur(gen_m,4.5)  # 中頻網格帶
base_MF= blur(base,1.2) - blur(base,4.5)
base_HF= base - blur(base,0.9)              # 母圖自身銳度
plate  = base + α*gain*(gen_MF-base_MF) + β*armor*base_HF
hardlock weapon + face
SKIP plate 80aecc41 (金改版有毒)
```

## 門檻
- gold_frac(out) ≈ gold_frac(src) ±0.02
- lap(out) >= lap(src) * 0.95
- MAD(full) << V3
- 禁止 full-RGB gen paste
