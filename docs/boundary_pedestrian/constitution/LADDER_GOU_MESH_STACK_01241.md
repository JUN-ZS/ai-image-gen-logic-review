# LADDER + GOU 密網棧 · LPV2-GOU · §0.12.41

> asof 2026-10-29T16:40:58Z · **LOCK**  
> 用戶：v2 入憲後再 **v2+GOU 密網**

## 一句

**先 GOU 近距 GEN 真密網 donor → 再 LADDER_PRESS_V2 階梯升尺寸。**  
純 residual 階梯保拓撲節奏弱時，用 GEN 密網補「有序蜂窩」。

## 鐵序

```
G0  BASE crop / 正衣板（OTL0 拓鎖）
G1  GOU T3：Ref(crop, mesh_lock) 密網重組 · 真生成網孔
G2  閘：目視有序蜂窩／金線 · 禁爆亂 · 禁換物
G3  LADDER_PRESS_V2 on GEN 板（§0.12.40 參數）
G4  可選 GOU 勾形貼回全幅（T5–T10）· 或 donor 出新
```

## 為何要棧

| 只 LPV2 | 只 GOU | **LPV2+GOU** |
|---------|--------|--------------|
| 尺寸階梯穩 | 密網語義真 | 語義真 **且** 尺寸階梯穩 |
| 密網節奏弱 | 尺寸仍小／一次放大易爆 | 先真網再階梯 |

## 禁

- 先一次×4 再 GOU（已爆）  
- GOU 後再一次 Hybrid×4  
- 跳 G1 直接 ladder 當「密網完成」

## 參數卡

```
MODE=LPV2_GOU_STACK
CROP=
MESH_LOCK=
GOU_PROMPT=rebuild dense ordered honeycomb + gold filigree; keep topo
THEN=LADDER_PRESS_V2 (HF_KEEP=0.62 ...)
```

*END §0.12.41*
