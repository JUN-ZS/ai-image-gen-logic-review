# §0.12.52 生成新像素 · GEN_NEW_PIXEL / GNP（**LOCK** · asof 2026-10-31）

> 用戶正名：**生成新像素** · **補像素** · 短碼 **GNP**  
> 觸發：開網／衣紋「不夠清」· 僅 USM／LANCZOS 放大仍糊 · 要 **真有新 HF 像素** 再合回 peep  
> **連動：** SWP §0.12.43 · DHY · HPT · MESH_CONSIST · MESH_SHARP · 解毒化衣 · ZSC  
> **樣板證據：**  
> - 母開網 `0d6aa9b2` / NATIVE_400_MOTHER  
> - 只對網軟 `d6734fe9`（topo 過 · **tenen 不夠**）  
> - wire-USM `d165723f`（tenen↑ · **仍非 dens 新像素**）  
> - 刺絲反例 `ceffce07`（假清 · 拓撲崩）

---

## 0.12.52.A 一句

**LANCZOS×N + USM ≠ 生成新像素。**  
真清 = **另路 densify／Imagine 生出 HF 新樣** → 再以 **母 wire 拓撲** 作 mask 合回 peep；USM 只可作 wire 微咬，**不得**當 sole 升清並宣稱 MATERIAL／L2。

---

## 0.12.52.B 三層像素法（鐵序）

| 層 | 名 | 做什麼 | 禁 |
|----|-----|--------|-----|
| **P0** | 母拓撲鎖 | 抽 wire／cell／node map · peep edge | 金色閾當衣 · bbox |
| **P1** | 工作板 | peep ×S（≥3）LANCZOS · **只放大框** | 全幅 GEN 重畫姿 |
| **P2** | **生成新像素** | SWP densify **或** Imagine macro／quilting HF 板 · 產出 **母圖沒有的 HF 樣** | 把 USM 殘差當 dens |
| **P3** | 拓撲合 | HF_new 只進 wire∪(β_cell 低) · **母 wire = master** | 全 α 蓋刺絲 |
| **P4** | 微咬 | wire-only USM ≤ 一次 · 可選 | 全幅 USM · 多次叠銳 |
| **P5** | 貼回 | pyramid HF reinject · multi-band · α peep | 單次 AREA 殺 HF |

**驗收必須同時：**
1. **topo NCC**（wire map vs 母）≥ 0.85（400%）  
2. **tenen** ≥ 母 crop ×1.05（400%）**且** ≥ 上輪 soft  
3. 目視：**開網孔洞仍在** · 非刺絲糊滿  
4. 若缺 P2 dens／Imagine → **不得**寫「生成新像素成功」· 只可寫「wire 加利」

---

## 0.12.52.C 公式（拓撲主 + 新 HF）

\[
I = LP_{mother} + MP_{mother}
+ M_{peep}\Big[
  W\cdot\big((1-\beta_w)HF_{mother}+\beta_w HF_{new}\big)
  + C\cdot\big((1-\beta_c)HF_{mother}+\beta_c HF_{new}\big)
\Big]
\]

- \(W\) = 母 wire mask · \(C\) = cell  
- 建議：**β_w ∈ [0.35, 0.55]**（wire 上要有真新絲粒）· **β_c ∈ [0.05, 0.15]**（孔洞少灌）  
- \(HF_{new}\) **必須**來自 densify／Imagine／quilting **獨立生成**，不是 \(USM(I)\)  
- 之後可選：\(I \leftarrow I + \lambda\cdot USM_{wire}(I)\) · \(\lambda\le 0.5\) · **只 wire**

---

## 0.12.52.D 與舊招關係

| 招 | 角色 |
|----|------|
| **SWP 升紋金字塔** | **P2 主源** · 層層 dens 生新 HF |
| **HPT / macro tile** | P2 材料庫 · quilting 後再 warp |
| **MESH_CONSIST** | P0+P3 · 母開網 master · 防刺絲 |
| **MESH_SHARP** | **僅 P4** · 不夠清時的微咬 · **不替代 P2** |
| **DHY peep** | P5 貼回 · 身形／衣 peep |
| **解毒化衣** | dens 後 hard residual · 防 soft bite 洗回 |

**本輪試錯定論（入憲）：**  
`MESH_CONSIST` 過 topo 但用戶判「不夠清」→ 因 **缺 P2 生成新像素**，只吃母 HF+輕 grain。  
`MESH_SHARP` tenen 1.42× 母 · 仍標 **wire-USM** · **未**達 GNP 完整義。  
下一完整 GNP = **P2 dens／Imagine 沿 wire 生新絲** + P3 拓撲合 + P4 可選微咬。

---

## 0.12.52.E 參數卡（可抄）

```
GNP=LOCK
P0=wire|cell|node from mother · peep edge
P1=work ×3..4 peep only
P2=HF_new = SWP densify | Imagine macro | quilt(L2)   # 必有一
P3=β_w=0.35..0.55 · β_c=0.05..0.15 · mother wire master
P4=wire USM optional λ≤0.5
P5=pyramid HF reinject · ban AREA-kill
GATE=topo≥0.85 · tenen≥1.05×母 · 開網目視 · 禁刺絲
BAN=USM-as-sole-clear · full-frame GEN · gold-peep · 1408 tile spam
TAG=GEN_NEW_PIXEL | GNP
```

---

## 0.12.52.F 錯碼

| 碼 | 毒 | 治 |
|----|-----|-----|
| **E-GNP-01** | 只 LANCZOS+USM 稱「生成新像素／高清 MATERIAL」 | 必須有獨立 HF_new 源 · 否則只標 wire-USM |
| **E-GNP-02** | dens／L2 全蓋 → 刺絲 · topo 崩 | wire master · β_c 低 · MESH_CONSIST 合 |
| **E-GNP-03** | 全幅 GEN 生清 · 姿／臉毀 | 只 peep 工作板 dens |
| **E-GNP-04** | HF↑ tenen↓ 仍過閘 | 閘必 Tenen+topo+目視開網 |
| **E-GNP-05** | 貼回 AREA 殺 HF_new | pyramid reinject |
| **E-GNP-06** | 把 soft mesh 當最終交付 | 用戶判不夠清 → 補 P2 再交 |

---

## 0.12.52.G 交付命名

| 檔 | 義 |
|----|-----|
| `PLATE_GNP.jpg/png` | 含 P2 新像素之工作板 |
| `NATIVE_400_GNP.jpg` | 400% 驗收 |
| `FINAL_GNP.jpg` | peep 貼回 FULL |
| `ACCEPT_GNP.json` | topo · tenen · HF_new 源標註 |
| 若無 P2 | 檔名用 `MESH_SHARP` **禁止**寫 GNP |

---
asof 2026-10-31 · §0.12.52 LOCK draft · 用戶：「加點生成新像素去補的憲法」

---
## 0.12.52.H L3 微細節殘差（2026-10-31）
全文：`GEN_NEW_PIXEL_GNP_L3_MICRODETAIL.md`  
**禁** L2 整板再 dens；只殘差微紋；失敗不蓋 L2。

---
## 0.12.52.I 真 L3 獨立 donor（2026-10-31）
`GEN_NEW_PIXEL_GNP_L3_TRUE_DONOR.md`  
L3 DoG/USM 撤銷 · L2 主板 · 真 L3 = 獨立 micro-fiber donor + wire 映射。

---
## 0.12.52.J L3T≠L3G（2026-10-31）
全文 `GEN_NEW_PIXEL_GNP_L3T_vs_L3G.md` · 轉移 ≠ 生成。

## → 主架構升級 NCPG §0.12.53
見 NESTED_CONTEXT_PEEP_GENERATION_01253.md
