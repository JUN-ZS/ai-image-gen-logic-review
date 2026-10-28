# §0.12.29 雙錨中密（DAMD · Dual-Anchor Mid-Densify）

> asof 2026-10-28 · 用戶：「給這插幀憲法一個技名再入憲」  
> 源鏈：RPF 尾先補 → CONST_F0 → HTM 頭尾中 → 本段加中 → 貼≠REF · OIDV/GFV 除毒  
> 樣板：ZOOM20（純 zoom 穩）· RAISE30（舉械示 E-02 繞路）

> **地位：LOCK** · 未過本節 → 不得稱「插幀憲完成／DAMD 鎖死」

---

## 0.12.29.A 招名

| 語 | 名 |
|----|-----|
| **正名** | **雙錨中密** |
| **粵／短** | **錨密** · **中密** |
| **英／碼** | **Dual-Anchor Mid-Densify** · **DAMD** |
| **一句** | 先 FT 雙錨 · 頭尾中遞歸加密 · 本段加中 · SoftRef 姿 ⊕ Hard 貼 ⊕ Verify · 禁 OIDV |
| **禁稱** | soft Ref＝貼 · 全圖重跑治標 · 長文代 Verify |

詳：`DAMD_DUAL_ANCHOR_MID_DENSIFY_NAME.md`

---

## 0.12.29.B 正推 · CONST_F0 短指紋

```
CONST_F0.短 =
  物拓: 部件圖（例：開月環—轂—桿）· 剛體 · 禁 retopo
  握: 握位（例：握桿非握環）
  臉: F0 身份 → 貼算子（非 soft 第三張）
  景: S（例：灰棚）
  Ω允許: 關節角 · 整械剛體 SE(3) · dolly/zoom · 微 pitch · 本動作 δ
  Ω禁止: delete_part · 拼版 · 過頂繞路（若本軌禁）· 全圖重身份
  δ: 單調約束（例 zoom↑ · h_ring↑ 趨終態）
```

**鐵：指紋短 · 非長小說。** 長文化 → 觸發 **OIDV**（§0.12.29.G）。

---

## 0.12.29.C 反推 · 合法幀合約

```
FT 合約 = 終態姿／構圖／鏡  ∧  拓=CONST_F0  ∧  臉可貼

F_t 合法 ⇔ SoftRef_姿(Head,Tail,t)
         ⊕ Paste_臉(F0)  ⊕  (Paste_S?)
         ∧ Topo(F0) ∧ Mono(δ) ∧ ¬拼版 ∧ ¬OIDV長文
```

Verify 失敗 → **拒收／Kill**，不得入列。

---

## 0.12.29.D 正典流程（鐵序）

```
D0  格物 F0 → 寫 CONST_F0 短指紋
D1  先出 FT · Verify 拓／終態合約
D2  雙錨 = {F0, FT}
D3  進度鍵 t=k/N 或 HTM 二分：mid = halfway(Head,Tail)
D4  每幀：
      gen = SoftRef_姿(Head, Tail, t)   # 只姿／鏡／zoom
      → Verify(拓, 單幀, δ)
      → Paste_臉(F0)   # HARD · 非 soft
      → 可選 Paste_S / 械剛貼
      → 入列
D5  失敗：Kill · 定合法 A,B · 只重 (A,B) mid
D6  中途加插：只動本段頭尾 · 禁動全樹
D7  交付：時間序格 + 膠片 + 輪播 + META
```

**錯序禁：** 先密中間再補尾 · 全 30 重跑當除毒 · 中途加插重跑全圖。

---

## 0.12.29.E HTM 加密（頭尾中）

```
L0: F0 ──── FT
L1: F0 ── M ── FT          # M 兼作子段頭/尾
L2: … 遞歸 mid …
```

| 規則 | 內容 |
|------|------|
| 中幀雙役 | mid 對左段是尾 · 對右段是頭 |
| 本段原則 | 加中 **只** 用本段頭尾 · 非全圖邏輯 |
| 視覺重排 | 進度鍵若 t 語漂 → 按實際構圖遠近／角 **重排** 再密 |

---

## 0.12.29.F 貼 ≠ REF

| | REF soft | 貼 HARD |
|--|----------|---------|
| 本質 | 條件重生 | 像素合成 |
| 姿／zoom | **用** | — |
| 臉 | 易 GFV | **必須貼** |
| 物拓 | 易 E-01 | L2 閘 ± 械剛貼 |
| S | 常漂 | 可貼 |

```
Error ≈ SoftRef(全圖) − Paste(臉,S,械?) − Verify
```

---

## 0.12.29.G 病毒憲（插幀域）

| 碼 | 名 | 症 | 除 |
|----|-----|-----|-----|
| **OIDV** | 過干預降智毒 | 長憲灌 prompt → 模型簡化／改物 | 刪長文 · 回指紋 · 硬閘在 L2/L3 |
| **GFV** | 重影臉毒 | soft 當貼 | HARD 臉貼 F0／a8b |
| **E-01** | 改物 | 拓≠F0 | Kill · 段重 mid · 拓閘 |
| **E-02** | 跳級／繞路 | δ 非單調（過頂再落） | 段殺 · 線性 t mid |
| **E-03** | 拼版毒 | 雙聯圖 | Kill |
| **E-05** | 糊幀 | motion blur 當靜幀 | Kill |

**不降智鎖：** 約束在 **Paste + Verify**，不在散文密度。

```
L1 指紋  2～4 短句
L2 Verify 拓／單幀／δ
L3 貼    臉 HARD · 可選 S／械
```

---

## 0.12.29.H 除毒（段殺重 mid）

```
不: 全序列重跑 + 更長 prompt
要: 定合法錨 A,B → 刪毒段 → 只 HTM(A,B) → 每幀 L2+L3
```

---

## 0.12.29.I Ω／δ 樣例

| 動作 | Ω | δ 單調 |
|------|-----|--------|
| 純 ZOOM20 | dolly only | zoom↑ |
| 舉械到臉 | 臂角 + 械剛 + zoom + 微俯 | h_ring↑趨臉 · zoom↑ · 禁先過頂 |

---

## 0.12.29.J 樣板

| 跑 | 要點 |
|----|------|
| **ZOOM20** | F0 `40edb55a` · FT `ce06e08c` · 20 幀 · 姿鎖純 zoom · 連貫佳 |
| **RAISE30** | 舉+zoom+微俯 · #09–12 E-02 · 診斷 `RAISE30_DIAG_CONST.md` |
| 產物 | `*_TIMEORDER_GRID` · `*_FILMSTRIP` · `*_SEQUENCE.mp4` · `*_META.json` |

---

## 0.12.29.K 黑名單

| 代號 | 禁 |
|------|-----|
| **E-DAMD-01** | soft Ref 稱臉已貼 |
| **E-DAMD-02** | 無 Verify 入列 |
| **E-DAMD-03** | 全樹重跑當除毒 |
| **E-DAMD-04** | 中途加插動全圖 |
| **E-DAMD-05** | OIDV 長文代 L2/L3 |
| **E-DAMD-06** | 拼版／改物幀入列 |
| **E-DAMD-07** | δ 非單調仍稱軌完成 |

---

## 0.12.29.L 與他節

| 節 | 關係 |
|----|------|
| §0.12.15 S1HL | 單幀升清／臉鎖；DAMD 管 **序列** |
| §0.12.14 PATH1E | 硬貼對位可作 L3 貼實作 |
| §0.12.27 GCS | 單圖細格解毒；DAMD 是 **時間軸** 加密 |
| XHL | 外折混鎖升清 · 與 DAMD 正交 |

---

## 0.12.29.M 一刀參數卡

```
F0=
FT=                    # 先出
CONST_F0_SHORT=        # 物拓/握/Ω/δ
N_TARGET=20|30
MODE=zoom|pose|orbit
PASTE_FACE=true        # HARD
VERIFY=topo,single,mono_delta
FAIL=kill_segment_redo
PROMPT=short_fingerprint_only
```

*END §0.12.29 · 雙錨中密 / DAMD · asof 2026-10-28*
