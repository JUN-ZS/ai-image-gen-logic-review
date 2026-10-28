# 招名：**啞面貼光 · 分溫鎖相**（啞貼分溫 / MATTE_LIGHT_CTEMP）

# STONE_FIRE_LIGHT_CTEMP 正確流程 · §0.12.26

asof: 2026-10-27T16:28:38Z

## T0 母底
- 全幅 native only（§0.12.23）
- 石啞面母優先：STONE_V2 級（樣板 8978bc25）

## T1 抽裁 + DETECT
- 自 ORIG/BASE 抽 stone_mid / fire_title
- GrabCut／殘差勾形（§0.12.25）· fill 閘

## T2 GEN 拓樸（甲鏈）
- 大裁 → image_to_image 真拓樸
- 可 2× → 二次拓樸（prompt 禁白噪線、禁糊）

## T3 白分層
- NOISE_WHITE 殺
- SPEC_LIGHT 留／正推創
- 反推 light_field（falloff 近火，禁 mean≈1 鋪滿）

## T4 啞面 + 光源貼層
- albedo/HF = 啞面鎖
- LIGHT_COMPUTE 上代有用 → 只貼照明
- out = lit_lp + matte_hf

## T5 色溫 Lab 正反推
- 冷岩 a,b ← 啞面
- 近火 a,b ← hybrid ref 插值 + maxΔ 閘
- 火 ← ref
- PROOF \|Δb_cold\| ≤ 2

## T6 SIAX mask 溫拋
- gain ≤ ~0.4 · 護 spec · 殺白向 HF

## T7 形拼 FULL
- 高α · 人／器鎖 · 2× band FULL ≥6MB
- META + L hash

## 停
色溫／反光／拓樸過閘即停；不為「再銳一點」破啞面母。
