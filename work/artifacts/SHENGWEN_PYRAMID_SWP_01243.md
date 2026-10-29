# 升紋金字塔 · 正確流程（SWP / §0.12.43）

> asof 2026-10-29T21:51:45Z · 憲：§0.12.43 · 連動 IPSD · GOU · FUB · OTL0 · LP2  
> **樣板：** 母 `700b99f1` · 落盤 `SETS/FUBZ_700b/RUSB_PY3/` · 洗後 `*WASHED*`

---

## ★ 試錯 → 成功（入憲備註 · 必讀）

### 失敗鏈（已殺 · 勿重）

| # | 錯 | 現象 | 根因 |
|---|-----|------|------|
| F1 | 當「單階 RUSB」或 **L2 直貼 700b 本母** | 對位漂／NCC 低／無支母座標 | **不是** 金字塔；缺 L1 支母緩衝 |
| F2 | L2 densify 用 **HEX 蜂窩換拓** 混入 donor | 第三層「看起來更清」但語法另一套 | **毒 DONOR** · OTL0 換物 |
| F3 | 毒底 + **α 過淡** 層層 HF 咬 | L3 到 · 貼回 **斷連** · L0 HF 幾乎不升 | 洗未做 · 強 α 未開 |
| F4 | 產品板／近鏡 E1 當同幅 densify | 「高清沒對位」 | 須 **ROI 同比例 IPSD** 非另板 |
| F5 | 一次全幅 4× 當金字塔 | 爆紋／OOM | 用 SWP 層層 ×2 + 閘 |

### 成功鏈（LOCK）

```
放大 3 層：
  L0 本母 = 全幅胸 ROI（母座標 box）
    → ×2 densify（同幅 IPSD · HYB/MOLD 僅約束）→ L1 支母 HF 咬
      → 裁甲面 ZOOM IN ×2 densify → L2 深層 HF 咬

貼回 3 層（倒序 · 不可跳）：
  L2 ──同拓洗後──▶ L1 支母（sub-box 座標）
  L1' ──────────▶ L0 本母
  L0' ──────────▶ 全幅母圖

閘每層：NCC≥0.75 · 同拓 orient/NCC 優於換拓候選 · HF 應層層可傳
```

### 掃毒表（L3 到 ≠ 可貼）

| 檢查 | 過 | 殺 |
|------|-----|-----|
| densify vs L2_base **NCC** | ≥0.90 級（樣板同拓 A≈0.93） | HEX 樣板≈0.78 → **毒** |
| **orient hist corr** | 同拓高 | 換拓低 → 禁混咬 |
| 貼後 HF(L0) | 明顯 > HF(母 ROI)（樣板 8.5→13.1） | 只 +1 內 → 斷連／α 淡 |
| 貼路徑 | L2→L1→L0 | L2→全幅 一次 |

### 治本三刀

1. **洗 donor**：只用 **同拓 densify**（樣板 L2_DENSIFY_A）；**BAN HEX／異拓**
2. **強 α 甲面**：支母／本母 **MF 拓鎖** + **高 k_hf** 注入洗後 residual
3. **鐵序貼回**：必經支母；每層 NCC 閘；FAIL 停、不硬貼

---

## 鐵序（不可顛倒）

```
0  定 L0 本母 ROI box（與母圖同比例）
1  L1 = densify(L0×2) + HF 咬 → 存為 支母
2  在 L1 上裁甲 ROI → L2_base = crop×2（ZOOM IN）
3  L2 = densify(L2_base)  · 閘同拓 · 洗毒
4  L2 HF 咬（MF= L2_base）
5  paste L2 → L1@sub-box（強 α）
6  paste L1' → L0（強 α）
7  paste L0' → 全幅 · PROOF
```

## 與其它招

| 招 | 關係 |
|----|------|
| **IPSD** | 每層 densify 核＝同幅升紋；SWP 管 **支母／貼序** |
| **GOU T3 / FL** | densify 紋語；仍受 **同拓閘** |
| **FUB / FUB+Z** | 升前掃線／深度；可嵌 L2 |
| **LP2** | 單 PART 尺度爬；**非** 支母金字塔貼回 |
| **OTL0** | 換拓 densify = 物格死 · 必洗 |
| **OIDV** | 禁灌長 3D 文當 densify 主路 |

## 一刀參數卡

```
MODE=SHENGWEN_PYRAMID
LAYERS=3 SCALE=2
PASTE=L2→L1→L0→FULL
DONOR_WASH=true BAN_TOPO_SWAP=true
NCC_GATE=0.75 ALPHA=strong_armor
SAMPLE=SETS/FUBZ_700b/RUSB_PY3/
```

## 樣板路徑

| 角色 | 路徑／id |
|------|----------|
| 母 | `700b99f1-83fd-4581-ab48-04c1e1e8939c` |
| 毒 peep | `SETS/FUBZ_700b/RUSB_PY3/POISON_PEEP.jpg` |
| 洗後全鏈 | `STRIP_WASHED.jpg` · `FULL_700b_WASHED.jpg` |
| 同拓 donor | `L2_DONOR_WASHED.jpg` |
| 毒 donor 反例 | `L2_DENSIFY_B_hex.jpg` |
