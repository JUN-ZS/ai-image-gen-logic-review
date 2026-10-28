# §0.12.34 首幀追尾技能棧（HTFC_STACK · OTL0+RML+雙錨 · **LOCK**）

> asof 2026-10-28T21:10:00+08:00  
> **用戶：**「把 OTL0+RML+雙錨 這上試錯到連動到技能『首幀追尾』的過程入憲」  
> **正名：首幀追尾技能棧** · **HTFC_STACK**  
> **LOCK：** 是  
> 連動：§0.12.31 OTL0 · §0.12.33 RML · §0.12.32 HTFC · §0.12.29 DAMD

---

## 0.12.34.A 定義

**首幀追尾（技能）** 不是「只出 t% 序列」· 是：

```
HTFC_STACK := OTL0 ∧ RML ∧ DualAnchor(F0, FT_PASS) ∧ ForwardChase(t)
```

缺 **任一** → 可叫實驗／對照 · **不得** 標 `MODE=HTFC` 完成（**E-HTFC-04/05**）。

---

## 0.12.34.B 層級（執行序）

```
① 格物 F0 → OTL0 CONST（含 shaft.mat）
② RML 錨點圖 + JSON（根因／准動分帶）
③ FT 候選 → OTL0+RML Verify → FT_PASS
④ 雙錨 [F0, FT_PASS]  = 圖級弱提醒
⑤ 正推 t：Soft 只准 S_pose / Ω / S_fx
⑥ 每幀 Verify + mono · Kill 段
⑦ 交付格／膠片／輪播／META
```

**文案短指紋** 防 OIDV；**真** 在 OTL0 欄 + RML 錨 + 雙錨像素。

---

## 0.12.34.C 試錯 → 憲（過程入憲）

### C1 柄金辮（治標 vs 治本）

| | |
|--|--|
| 現象 | t12 `92d45c` 深色纏→金辮 |
| 治標 | Kill 重做該幀 |
| 治本 | `shaft.mat` 入 OTL0 + **S_shaft 因鎖（RML）** + Soft 禁寫柄 |
| 入憲 | §0.12.33.D · §0.12.31 柄欄 |

### C2 提醒鎖命題

| | |
|--|--|
| 用戶 | 模型會換角想像 · 找提醒鎖／座標噪點 |
| 入憲 | RML = 錨×R_ij×根因 N 鎖 |
| 示範 | d5f9／ab1139 錨點全圖 |

### C3 有鎖 vs 無鎖對照（ab1139）

| 模式 | 結果 | 憲義 |
|------|------|------|
| HTFC_STACK | 環+盤全序穩 | 生產態 |
| 無文案+雙錨 | 拓大致仍在 | 雙錨=弱提醒 · 非無鎖 |
| 單圖 free climax | 多環結、失盤 | 真無提醒 → E-01 |
| redesign OK | 整把變斧 | 先驗換槍 |

**入憲結論：** 關 OTL0/RML **文案** ≠ 關提醒；關提醒 = 不喂物真。

### C4 合格尾錨

| | |
|--|--|
| 偽尾例 | 環弱／針柄（X1 類）→ Kill |
| 流程 | Xn 候選 → Verify → 用戶選 → 再追 |

---

## 0.12.34.D 樣板索引（2026-10-28）

| 棧跑 | F0 | FT_PASS | META/產物 |
|------|-----|---------|-----------|
| 環槌 | `d5f9fe0e` | `3822d80f` | HTFC_d5f9_* |
| 環盤衝擊 | `ab1139d4` | `4ad1e2c0` | HTFC_ab1139_* · LOCK_vs_FREE |
| RML 錨 | 同上 | — | RML_*_ANCHOR_MAP |

---

## 0.12.34.E 與舊 HTFC 條

§0.12.32 仍為 **招法**（正推鐵序）。  
**本節 = 技能完整棧 + 試錯連動**；執行 HTFC 時 **本節優先於「只跑 t%」**。

---

## 0.12.34.F 黑名單

| 碼 | 禁 |
|----|-----|
| **E-HTFC-05** | 無 RML／無 shaft.mat 稱完整棧 |
| **E-HTFC-06** | 對照實驗的無鎖產物混入生產時間序 |
| **E-HTFC-07** | 單圖 freestyle 當追尾幀 |
| **E-HTFC-08** | 以「雙錨已夠」永久省略 OTL0 Verify |

## 0.12.34.G 參數卡

```
MODE=HTFC_STACK
F0=  FT=  RML_ANCHORS=
CONST_F0_SHORT=  # topo + shaft.mat + Ω
DUAL=[F0,FT]
N=11..24  PUSH=forward_t
SOFT_FORBID=root_classes  SOFT_FREE=pose,fx
VERIFY=topo,shaft_mat,mono
```

*END §0.12.34 · HTFC_STACK · LOCK*
