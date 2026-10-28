# §0.12.32 首幀追尾（HEAD_TAIL_FORWARD_CHASE / HTFC · **LOCK**）

> asof 2026-10-28T12:15:00Z HKT  
> **用戶：**「那連動它的這首幀追尾技法,也入憲技法」  
> **正名：首幀追尾** · **HTFC** · Head-to-Tail Forward Chase  
> **LOCK：** 是  
> **連動硬依賴：** §0.12.31 **物格 L0（OTL0）** · §0.12.29 **雙錨中密（DAMD）**  
> 名卡：`HEAD_TAIL_FORWARD_CHASE_NAME.md`

---

## 0.12.32.A 招名

| 語 | 名 |
|----|-----|
| **正名** | **首幀追尾** |
| 粵／短 | **頭追尾** · **首追** |
| 英／碼 | **Head-to-Tail Forward Chase** · **HTFC** |
| 一句 | 先合格雙錨 → **由 F0 極細正推** 追至 FT → 每步 OTL0 Verify |
| 禁稱 | 無尾先追 · 僝尾當終點 · soft 全圖當已鎖物 · 長憲灌每幀 |

---

## 0.12.32.B 地位（在插幀族內）

```
DAMD（雙錨中密）= 插幀總殼
  ├─ HTM 頭尾中加密      （二分 mid）
  ├─ 本段加中            （只動局部頭尾）
  └─ HTFC 首幀追尾       （正推細 t：F0→FT）  ← 本節
OTL0 物格 L0             = 全程 L0 根閘（連動強制）
```

**HTFC 不是另開山頭，是 DAMD 的正推密模 + OTL0 硬綁。**

---

## 0.12.32.C 鐵序（不可颠倒）

```
H0  格物 F0 → CONST_F0.物（OTL0 短指紋）
H1  先出 FT 候選（終態：正面／ZOOM／動作…）
H2  Verify_Topo(FT, F0)     # OTL0 · 不過 → Kill · 禁入錨
H3  雙錨 = {F0, FT_PASS}    # 可記 FT_ALT（P1）但物真仍 F0
H4  正推序列：t = ε, 2ε, … → 1
      每幀：
        SoftRef_姿(F0, FT, t)   # 只姿／鏡／Ω
        ⊕ 短指紋（非長文）
        → Verify_Topo + Mono(δ)
        → 可選 Paste_臉(F0) HARD
        → 入列 or Kill
H5  視覺重排（t% 語≠視覺時）+ 段殺重 mid（DAMD）
H6  交付：時間序格 · 膠片 · 輪播 · META
```

**錯序禁：**
- 無合格 FT 就「追」
- 僝尾（未過 OTL0）當終點
- 先密中間再補尾
- 每幀灌滿憲文（OIDV）

---

## 0.12.32.D 與「反推補前幀」分流

| | 尾先反補（RPF 系） | **首幀追尾 HTFC** |
|--|-------------------|-------------------|
| 起點 | FT 倒推回 F0 | **F0 正推到 FT** |
| 體感 | 由終態貼回 | 由首態細步追終態 |
| 共用 | 雙錨 · OTL0 · Verify · 短指紋 · 禁僝尾 | 同 |
| 選用 | 終態姿極難、宜先釘尾 | **終態已合格 · 要從首看出漸變** |

用戶 2026-10-28 改序：「出頭尾後，**再由頭幀**依憲極細膧推到尾」→ 本招。

---

## 0.12.32.E Ω／δ（正推約束）

```
Ω ⊆ DAMD.Ω ∧ OTL0.Ω_物
δ 必須單調趨 FT（例：yaw→front↑ · zoom↑ · 禁先過頂再落若本軌禁）
物：只 SE(3) 投影 · 不重生（OTL0）
```

短指紋例：

```
物=開月C+單輷+桿 · 握桿 · Ω=yaw→正+zoom · mono
```

---

## 0.12.32.F 連動 OTL0（強制）

| 步 | OTL0 要求 |
|----|-----------|
| H1–H2 | FT 必須 **Topo PASS**；P0 Kill；P1 可 FT_ALT 記帳 |
| H4 每幀 | Verify 物格；E-01／E-OTL0-04 近景重雕 → Kill |
| 僝尾 | **E-DAMD-08** · 全鏈中段作廢 |
| 創造 | **不得** 以美觀放水武器不一致（E-OTL0-01） |

---

## 0.12.32.G 失敗與除毒

```
不: 加長 prompt · 全 20 幀重跑當唯一手段
要: Kill 毒幀/僝尾 → 重 FT（多步小 yaw）→ 只重壞段 (A,B) mid 或 重跑壞 t 帶
```

| 碼 | 禁（HTFC 加） |
|----|----------------|
| **E-HTFC-01** | 無 FT_PASS 即正推 |
| **E-HTFC-02** | 以 t% 數值代替視覺單調（不重排、不 Kill） |
| **E-HTFC-03** | 把 P1 備錨當可改物依據 |
| **E-HTFC-04** | 跳過 OTL0 稱「已追尾完成」 |

---

## 0.12.32.H 樣板（2026-10-28）

| 項 | 值 |
|----|-----|
| F0 | `0b9d87d8-4219-4ee0-8d49-a1713aadc16f`（3/4 背 · 晶月杖） |
| KILL 僝尾 | `74d9ae53`（E-01／未 Verify） |
| FT_PASS | `41f91ded`（正面 ZOOM · 拓 PASS） |
| FT_ALT | `740b95a6`（拓 PASS · P1 · 矛尖同向） |
| 跑 | `DAMD20_FWD` · 先雙錨後極細正推 · 教訓：僝尾先 Kill 再追 |

---

## 0.12.32.I 一刀參數卡

```
MODE=HTFC
F0=
FT=                 # 必須 OTL0 PASS
CONST_F0_SHORT=     # 物拓/握/Ω/δ
N=16..24            # 極細：ε≈1/N
PUSH=forward_t      # F0→FT
PASTE_FACE=true
VERIFY=topo,mono_delta,single
OTL0=required
FAIL=kill_segment_or_retarget_FT
PROMPT=short_fingerprint_only
```

*END §0.12.32 · 首幀追尾 / HTFC · LOCK · asof 2026-10-28*
