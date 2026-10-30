# 升紋金字塔 · 正確流程（SWP / §0.12.43）

> asof 2026-10-30T18:20+08 · 憲：§0.12.43 · 連動 **ROI** · **IPSD** · GOU · FUB · OTL0 · LP2 · **ETZ**  
> **樣板：** 母 `700b99f1` · 落盤 `SETS/FUBZ_700b/RUSB_PY3/` · 洗後 `*WASHED*`  
> **本批補：** 層層保 PIXEL 回母 · L2 IPSD residual 洗毒 · ETZ E1 嵌 SWP

---

## 0. 設計本意（ROI · IPSD · SWP）

| 招 | 管 | 不負責 |
|----|-----|--------|
| **ROI** | 點名只搞呢塊（胸／肩／甲…） | 升幾倍、怎貼 |
| **IPSD** | **同幅** densify：姿／拓鎖死 · 只升 HF · bite=LP(母)+HF×M | 多層支母金字塔 |
| **SWP** | **多層支母** L0→L1→L2 放大 · **L2→L1→L0→FULL** 貼回 | densify 核仍靠 IPSD／GOU |

```
全幅母
  └─ ROI_L0 本母（同比例 box）
        │  IPSD 同幅 densify + HF 咬   ← 保 PIXEL 語法
        ▼
     L1 支母（≈×2 工作幅）
        │  再裁 ROI_ZOOM · 禁 reframe
        │  IPSD 再 densify + HF 咬
        ▼
     L2 深層 donor
        │
        ▼ 貼回鐵序（不可跳）
     L2 ──ncc閘──▶ L1 支母
     L1' ────────▶ L0 本母
     L0' ────────▶ 全幅潔淨母
```

**一句：** 層層放大升清 → 每層保住對該層母的 PIXEL → 倒序貼回層層母。

---

## ★ 除毒過程（試錯 → 成功 · 入技能備註 · 必讀）

### 失敗鏈（已殺 · 勿重）

| # | 錯 | 現象 | 根因 |
|---|-----|------|------|
| F1 | 當「單階 RUSB」或 **L2 直貼本母／全幅** | 對位漂／NCC 低／無支母座標 | 缺 L1 支母緩衝 |
| F2 | L2 densify **HEX／換拓** 當 donor | 「更清」但語法另一套 | **毒 DONOR** · OTL0 |
| F3 | 毒底 + **α 過淡** 層層 HF 咬 | L3 到 · 貼回 **斷連** · L0 HF 幾乎不升 | 未洗 · 弱 α |
| F4 | 產品板／近鏡／異比例 densify | 高清沒對位 | 須 **ROI 同比例 IPSD** |
| F5 | 一次全幅 4× 當金字塔 | 爆紋／OOM | 層層 ×2 + 閘 |
| **F6** | L2 **1:1 reframe／另構** 當 donor | residual 熱圖全亮 · ncc≈**0.43** | 未保 PIXEL 對 L2_base |
| **F7** | 知「升了」就貼 · 不查回母 ncc | 毒灌全幅 · 潔淨母斷 | 缺層層閘 |
| **F8** | ETZ **E1 未嵌 SWP** 就 E2 | 正衣紋弱／毒板入合 | E1 先 SWP 先衣 |

### 成功鏈（LOCK）

```
放大 3 層：
  L0 本母 = 全幅 ROI（母座標 box · 同比例）
    → IPSD densify + HF 咬 → L1 支母
      → 裁甲 ZOOM · 同比例 L2_base → IPSD densify + HF 咬 → L2

貼回 3 層（倒序 · 不可跳）：
  L2 ──同拓洗後──▶ L1 支母（sub-box）
  L1' ──────────▶ L0 本母
  L0' ──────────▶ 全幅母

閘：每層 densify ncc≥0.90 · paste ncc≥0.75 · orient 同拓 · HF 可傳
```

### 掃毒表（L3 到 ≠ 可貼）

| 檢查 | 過 | 殺 |
|------|-----|-----|
| densify vs **該層 base** ncc | ≥0.90（樣板 IPSD residual **0.982**） | reframe≈0.43 · HEX≈0.78 |
| **orient hist corr** | 同拓高 | 換拓低 → 禁混咬 |
| 貼後 ncc vs 支母／本母 | ≥0.75（優 0.90+） | 跳支母 · 硬貼 |
| 貼後 HF(L0) | 可測 > 母 ROI（樣板 8.5→13.1） | 只 +1 內 → 斷連／α 淡 |
| 貼路徑 | L2→L1→L0→FULL | L2→全幅 一次 |
| residual 熱圖 | 邊緣可控 · 非全域亮 | 全域亮 = 毒 donor |

### 治本四刀

1. **洗 donor**：只用 **同拓 · 同比例 IPSD** densify；**BAN HEX／reframe／異拓**
2. **保 PIXEL 咬**：`out = LP(該層母) + HF(densify)×M`（k 高 · 甲面強 α）；MF 鎖支母／本母
3. **鐵序貼回**：必經支母；每層 ncc 閘；FAIL 停、不硬貼
4. **ETZ E1 嵌 SWP**：就正板先走金字塔升清洗毒，再 E2 合新

### L2 毒 → IPSD 重跑（F6 樣板）

```
毒：L2 donor 1:1 reframe     ncc≈0.43 vs L2_BASE
正：IPSD same-frame residual bite
    LP = L2_BASE · HF = densify · k≈0.95
    → ncc≈0.982 · HF↑ · residual 熱圖收斂
再：L2→L1→L0 paste（樣板 paste ncc 0.998 / 0.984 級）
```

---

## 鐵序（不可顛倒）

```
0  定 L0 本母 ROI box（與母圖同比例）
1  L1 = IPSD densify(L0×2) + HF 咬 → 存為 支母
2  在 L1 上裁甲 ROI → L2_base = crop 同比例（ZOOM · 禁 reframe）
3  L2 densify = IPSD(L2_base) · 閘同拓 · 洗毒
4  L2 bite = LP(L2_base) + HF×M
5  paste L2 → L1@sub-box（強 α）
6  paste L1' → L0（強 α）
7  paste L0' → 全幅 · PROOF
```

## 與其它招

| 招 | 關係 |
|----|------|
| **ROI** | 裁哪裡；SWP／IPSD 都在 ROI 內做 |
| **IPSD** | 每層 densify 核＝同幅升紋；SWP 管支母／貼序 |
| **GOU T3 / FL** | densify 紋語；仍受同拓閘 |
| **FUB / FUB+Z** | 升前掃線／深度；可嵌 L2 |
| **LP2** | 單 PART 尺度爬；**非** 支母金字塔貼回 |
| **OTL0** | 換拓 densify = 物格死 · 必洗 |
| **ETZ** | **E1 內嵌 SWP 先衣** → E2 合 |
| **OIDV** | 禁灌長 3D 文當 densify 主路 |

## 一刀參數卡

```
MODE=SHENGWEN_PYRAMID
ROI=chest|armor|…
LAYERS=3
SCALE=2
DENSIFY=IPSD_same_frame
BITE=LP(mother)+HF(donor)×M
L0=mother_ROI_box
L1=支母 full_ROI×2 densify+HF
L2=ZOOM_IN crop_on_L1 同比例 densify+HF
PASTE=L2→L1→L0→FULL
DONOR_WASH=true
BAN_TOPO_SWAP=true
BAN_REFRAME=true
NCC_LAYER=0.90
NCC_PASTE=0.75
ORIENT_CORR_prefer_high
ALPHA=strong_armor
MF_LOCK=支母/本母
HF_INJECT=high
ETZ_E1_EMBED_SWP=true
FAIL_if=hex_or_topo_swap | reframe_donor | paste_skip_branch | ncc<gate
SAMPLE=SETS/FUBZ_700b/RUSB_PY3/
```

## 樣板路徑

| 角色 | 路徑／id |
|------|----------|
| 母 | `700b99f1-83fd-4581-ab48-04c1e1e8939c` |
| 毒 peep | `SETS/FUBZ_700b/RUSB_PY3/POISON_PEEP.jpg` |
| 洗後全鏈 | `STRIP_WASHED.jpg` · `FULL_700b_WASHED.jpg` |
| 同拓 donor | `L2_DONOR_WASHED.jpg`（densify A） |
| 毒 donor 反例 | `L2_DENSIFY_B_hex.jpg` · reframe ncc0.43 |
| IPSD 洗樣 | L2 residual bite ncc **0.982** |
| 報告 | `POISON_DIAG.json` · `WASH_REPORT.json` |
