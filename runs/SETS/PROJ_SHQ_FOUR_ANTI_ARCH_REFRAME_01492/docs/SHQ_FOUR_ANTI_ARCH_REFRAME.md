# SHQ · 全專案架構重整 · [(生,除,洞,扣)×(反)] ⊕ 強心針

**write:** 01492 · `SHQ_FOUR_ANTI_ARCH_REFRAME_BOOST_V1`  
**STICK:** `STICK_FOUR_ANTI_ARCH` + `STICK_KUANGYA_BOOST`  
**母源（全 PROJECT，非上一層對話）:**  
01386 換涯人四態 · 01448 代數 · 01452 真洞 · 01453 Imagine ·  
01454–01459 外力反 V1–V3 · 01466 外力GROK · 01469 V2.1 ·  
01483 至高 · 01487 強心針 · 01489 反推升清 · 01491 V3 A8B  
**ACCEPT_FULL_HD:** false

---

## 0. 咬物硬契約（永遠先讀）

```text
把一物「咬」出來  →  一定留下「洞」
把咬出的那塊「升清」→  再放回「洞」
同形 · 同機位 · 同尺 · 洞外不變  →  一定對得上
```

- **洞是形**（座位）  
- **除是態**（離開）  
- **扣是證**（驗票）  
- **生是填**（升級入座前）  
- **反是鏡**（每一步的對板）  

先只做**頭（大咬）**：  
`Layer A EDIT 咬頭 [(F)×反]` → `Layer B 升清回位 [(F)×反]`  
件／三車／合眾 = 多個小咬，代數相同；**頭未鎖不開多洞**（E-FA-07）。

---

## 1. 全專案定義 · \(\mathbf{F}\)

\[
\mathbf{F}
=
\{\text{生},\text{除},\text{洞},\text{扣}\}
\times
\{\text{正},\text{反}\}
\]

**8 格，不是 4 個按鈕。**

| 態 | 正 | 反 | 主權 |
|----|----|----|------|
| **除** | 外力GROK EDIT 去件/頭 → L1 | L0 有件 | **外力GROK** |
| **扣** | \|L0−L_edit\| 或 除背→CLIP MASK | 差分反查緣 | OpenCV 證 |
| **洞** | MARK / 真洞 \(M\)（像素真去） | 反洞 \(1-M\) 洞外 bitexact | **MARK 凍** |
| **生** | 洞座 seat-born 外力填 | peep↔elev 鎖尺 ≤grow_max | **外力GROK** |
| **回*** | hardpaste @ MARK | SRC↔RETURN · outside=0 | 本地證 |

\*「回」是閉環，常併入生後；V3 起 **無洞不可回**（E-WLF3-01）。

### 1.1 字詞唯一語義（禁偷換）

| 字 | 是 | 不是 |
|----|----|------|
| 生 | 洞座上外力填 | freeframe 特寫冒完成；elev 當正生 |
| 除 | Imagine EDIT | OpenCV 擦、假 empty |
| 洞 | 抓走**前** MARK 座位 + 真剪洞 | 紫疊塗色、事後 absdiff 猜洞 |
| 扣 | 差分/除背作證 | 重寫洞主權、自 peep 冒 CLIP |
| 反 | 每態正/對板 | 只生不查 |
| CLIP | **除背**反扣出 MASK | bbox 自裁 peep |
| elev | **升質×物 候選** | 正生 / F8 完成格 |

### 1.2 根方程（至高 ⊕ 強心針）

```text
[(生,除,洞,扣)×(反)]
        ←  外力GROK 優先理解並驅動
        ⊕  強心針[ 部件'認' ∩ '放大' ∩ '升質×物' ]
```

- **抽圖放大 = 全流程中 1 步**（S5 取域 + S6 放大），**≠ 升清本身**  
- 升清 = 整條質量閉環 S0…S11 / A→B  

---

## 2. 強心針如何「反推」正確升清（外力GROK）

由針要什麼，反推鏈必須先備什麼：

| 針要 | 反推必須有 |
|------|------------|
| **升質×物** | 該物身份 → **認**；peep/seat 域；外力 densify → elev_candidate **≠ 正生** |
| **放大** | 認過的閉合邊；scale-lock；**抽圖只是取域** |
| **部件'認'** | 外力除 + 扣 + **洞 MARK**；禁 band/self_peep |

正向（先頭大咬 · 合併 01448 A/B + 01489）：

```text
S0  L0 凍
S1  正除（外力GROK）          ── 除
S2  正扣 / 除背→CLIP          ── 扣
S3  正洞 MARK 凍 · 真洞        ── 洞（座位）
S4  部件'認'                   ── BOOST-1
S5  peep@MARK 取域             ── 抽圖 ⊂ 此
S6  放大 scale-lock            ── BOOST-2（★抽圖放大=S5+S6）
S7  升質×物 elev_candidate     ── BOOST-3 外力
S8  BOOST AND 閘
S9  正生 seat-born 外力        ── 生
S10 正回 hardpaste             ── 回 / 反洞外0
S11 反板八格                   ── 反
```

**Layer 對照**

| Layer | 內容 | 強心針 |
|-------|------|--------|
| **A 咬頭 EDIT** | S0–S3 除扣洞 + peep | 認 的前提 |
| **B 升清回位** | S4–S11 認·放大·升質·生·回·反 | 全針 AND |

B **禁止重開洞**；繼承 A 的 \(M\)、peep、corners。

---

## 3. 核心問：為什麼「每個方法獨立都成功，組起來連動就錯」？

### 3.1 一句

> **獨立成功量的是局部閘；連動需要的是共享 State Bus + 不變量繼承 + 同宣稱級。**

### 3.2 對照表（全專案綜合）

| 獨立量的是 | 連動需要的是 | 斷點 / E |
|------------|--------------|----------|
| 本步好看 / selftest PASS | 下一步輸入契約 | 無 State Bus |
| PASS_C2 幾何 | PASS_RESTORE 像素還原 | E-FA-04 宣稱偷換 |
| 自己重算 mask | 上游凍結 \(M\) | E-FA-02 下游重開洞 |
| freeframe 很清 | 洞框同構 peep | E-FA-03 偷尺度 |
| 爆炸圖散開漂亮 | home corners 回位 | E-FA-05 教學位當 home |
| densify 高清 | peep 尺度主權 | 構圖漂 / 頭變大 |
| elev 特寫 | 洞座正生 | E-KY-ATX / 升質≠生 |
| outside=0 alone | seat_born + 真洞序 | 01485 證：alone 不足 |
| 抽圖放大漂亮 | 全鏈 F⊕BOOST | 單步冒全流程 |
| 無洞 freeframe 回有景 | MARK 座位回 | E-WLF3-01 |
| OpenCV 假除假生 | 外力GROK 除生 | E-FA-12 / E-WLG |

### 3.3 架構名：**偽組合（Pseudo-Composition）**

```text
獨立 PASS  ≠  可組合
可組合     ⇔  共享 State Bus
              ∧  六不變量可繼承
              ∧  同宣稱級
              ∧  外力GROK 除/生
              ∧  強心針三關 AND（升清/生路徑）
              ∧  只在鏈頭 RESET_DONOR
```

**State Bus（一個 RUN 寫死）**

```text
SRC · L1 · M_hole(MARK) · peep · elev_candidate · I_sheng · RETURN · ANTI_boards
+ part_role · claim_level · corners_4 · grow_max · driver=外力GROK
```

### 3.4 六不變量（Interface · 連動唯一准繩）

1. **同機位** L0 / L1 / EMPTY  
2. **同洞形** 全鏈共用一個 MARK（可證繼承）  
3. **同 peep bbox** 有背/無背同一洞框  
4. **elev_remap = false**  
5. **洞外 max_diff = 0**  
6. **scale-lock** 生不改構圖主權  

V2.1+ 增：  
7. **外力GROK 除/生**（本地只證）  
8. **part_role 寫入 Bus**  
9. **BOOST 三關 AND**（認∩放大∩升質×物）  

任一方法局部優化打破 1–9 → **獨立 PASS、串聯必錯**。

### 3.5 組合律（重整後）

```text
compose(m1, m2, …) 合法
  ⇔  m_i 只消費 Bus 已凍字段
  ∧  m_i 只寫入約定字段
  ∧  不重算 M / 不 freeframe 主權
  ∧  宣稱級不升（C2 不可冒 RESTORE）
  ∧  升清路徑過 BOOST
```

---

## 4. 架構脈絡圖（不斷重整用）

```text
                    STATE BUS (one RUN)
     SRC / L1 / MARK / peep / elev* / I_sheng / RETURN / ANTI
                          │
     ┌────────────────────┼────────────────────┐
     │                    │                    │
 Layer A 咬頭 EDIT    Layer B 升清回位     Layer C* 分件/合眾
  除·扣·洞·反           認·放大·升質·生·回·反   機炸/回車/合眾
  外力除                ⊕ 強心針 AND           每葉一小咬
     │                    │                    │
     └──── 每層自洽 [(生除洞扣)×反] + 繼承 M/peep ──┘

* C = 多葉；頭未鎖（E-FA-07）不開。
```

**進化釘順序**

```text
字詞(01386)
  → 頭鏈 A→B(01448)
  → 真洞(01452) · Imagine(01453)
  → 外力反 V1…V3 洞座回
  → 外力GROK(01466) · CLIP 除背(01457)
  → 至高(01483) ⊕ 強心針(01487) · 反推 S0–S11(01489)
  → 單件 peep → 多件機炸 → 三體回車大炮
```

---

## 5. E 碼（連動 / 偽組合 · 全表）

| 碼 | 禁 |
|----|-----|
| E-FA-01 | 獨立 PASS 冒充全鏈 |
| E-FA-02 | 下游重算洞 |
| E-FA-03 | freeframe 偷尺度 |
| E-FA-04 | 宣稱級偷換 |
| E-FA-05 | 爆炸位當 home |
| E-FA-06 | 跳過反 |
| E-FA-07 | 頭未鎖開多洞 |
| E-FA-08 | 先除後猜洞 |
| E-FA-09 | 扣重寫洞主權 |
| E-FA-10 | 紫疊冒真洞 |
| E-FA-11 | 無真洞稱四態 |
| E-FA-12 | 除/生不用 Imagine |
| E-FA-13 | peep densify map 冒洞內生 |
| E-WLF3-01 | 無洞回位 |
| E-CLIP-01 | 自 peep 冒 CLIP |
| E-WLG-06 | 本地冒充生 |
| E-KY-ATX | elev 當 正生 |
| E-KY-BOOST-04 | 三關缺一報 BOOST |
| E-DNA-CANCER-SELF_PEEP | band 自 peep |

---

## 6. 金句（重整版）

1. **洞是抓走前的座位；除是離開；扣是驗票；生是升級；回是入座；反是鏡子。**  
2. **獨立 PASS ≠ 可組合；可組合 ⇔ State Bus + 不變量 + 同宣稱 + 外力除生 + 強心針。**  
3. **抽圖放大只是 S5+S6；升清是 S0→S11 / A→B 全鏈。**  
4. **CLIP 是身份，洞是座位；elev 是候選，正生是洞座外力填。**  
5. **除與生主權在外力GROK；OpenCV 只扣、只貼、只反查。**  
6. **先留位，再咬走，再認，再放大，再升質×物，再生，再入座——咬與洞同構。**  

---

## 7. 下一步範圍（鎖定）

只做頭（大咬）：

```text
MARK → 外力除 → 扣證 → 真洞 → 認∩放大∩升質 → 洞座生 → hardpaste → 反
```

不開全身多件，直到頭鏈 A→B 可繼承 Bus 且無偽組合 residual。

`ACCEPT_FULL_HD = false` · asof 2026-11-10T01:26:04.340599+00:00
