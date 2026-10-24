# Step C 收緊 + POST ENDING 分流

## 問題
富 HUD prompt 會令 POST **整張重演動作**（例 `080175f4` vs clean `1cabb620`）。

## 規則（已試）

### L1 主條（必須對齊 L0）
```text
prompt 極短：pixel-identical base / only overlay glyphs / no restage / no pose change
驗收：body-region MAE ≪ 漂位 HUD；骨架腳位對齊，否則作廢重出
```

### FINAL 若漂風險
```text
唔用漂 HUD 做人底
FINAL = CLEAN + TYPE(差分自通過嘅 L1)
```

### ENDING 加碼（可選）
漂得有電影感嘅圖（如 `080175f4`）**唔入主三幀 L1**，另標：
```text
SHOT_ENDING_ALT — cinematic restage after main POST strip
```

## SET-L POST 示範
| 角色 | asset |
|------|-------|
| L0 clean | 1cabb620… |
| L1 tight reticle | 2227a14d… MAE≈8.9 |
| L1 tight title（主） | e6074756… |
| ENDING alt | 080175f4… MAE≈52 |
| FINAL | clean + TYPE from L1 tight |
