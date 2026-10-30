# §0.12.50 四技對紋絕招 · TEX4 / FOUR_SKILL_TEX_ALIGN（**LOCK**）
# asof 2026-10-30T21:15:44Z

> **用戶正名路徑：** 虛形互搏 × 影分身合 × 殘相轉生 × P_G紋 → **入憲絕招**  
> **用戶鐵句：**「虛形互搏 和 影分身合 都要用到，因為改不到新的對紋」  
> **用戶鐵句：**「那這4技可用什麼幫改這圖？」→ 對準黑裙金線三綠圈 · 試錯寫入  
> **連動：** §0.12.46 RRT · §0.12.47 影分身合 · §0.12.48 虛形互搏 · §0.12.49 P_G紋 · 可嵌 §0.12.43 SWP（**之後**）· §0.12.39 SPM（residual 輔）

---

## 0.12.50.A 一句

**四技唔係「再美顏一次」**，係：

```
IP 給新順紋 → 虛形讓 peep 只鎖衣 → RRT 殺殘／螺旋 → P_G 用 peep×姿座標貼返母
```

**絕招定位：** 衣／甲 **錯順紋 · 錯拓撲 · 新紋對不準** 時的總招。  
**非** 單靠 SWP 升清 · **非** 單靠 SPM 咬 residual。

---

## 0.12.50.B 為何是絕招（發現）

| 缺 | 結果 |
|----|------|
| 無 **影分身合** | 無獨立衣 IP · 新紋無身份 donor · 只能在殘相上糊修 |
| 無 **虛形互搏** | 手／杖實搶 peep · 衣紋被互動體帶跑 · **對不準** |
| 僅 RRT+P_G | 結構可補 · **新紋貼位仍漂** |
| 僅 SWP/SPM | densify ncc 過 · **螺旋拓撲遺傳**（保 PIXEL = 保錯線） |

→ **四技全上** 才稱對紋完成（E-TEX-03）。

---

## 0.12.50.C 試錯鏈（黑裙金線 · LOCK 備註）

### 失敗鏈（已殺 · 勿重）

| # | 錯 | 現象 | 根因 | 碼 |
|---|-----|------|------|-----|
| F1 | 單 RRT 或單 P_G | 改不到新的對紋 | 無 IP 身份 · 無虛形 peep | E-TEX-01/02 |
| F2 | 只 SWP 金字塔 | 閘過 · 胯螺旋 C 仍在 | 升清≠換拓 · IPSD 遺傳錯線 | E-TEX-08/09 |
| F3 | 只 SPM 定位改 | ECC 弱／α 淡 · 半改 | 無清 donor 拓 · 弱 α | E-TEX-04/07 |
| F4 | 半修圖當母再修 | 疊毒 · 越修越 spiral | 毒 donor 疊層 | E-TEX-04/05 |
| F5 | 無鎖 peep · 全幅改 | 臉／杖／灰底 spill | 無鎖面 · 無 peep 閘 | E-TEX-06/10 |
| F6 | 格號當尺／人 | scale 毒 | 格人脫鉤 · 見 E-OBA-02 | 連 OBA |

### 成功鏈（LOCK · 黑裙樣板）

```
母 22cf97df（姿鎖）+ 問題圈 ad220951（肩帶亂線 · 胯螺旋C · 下胯飄線）
  ① 影分身合 → 衣-only IP 全形 + 胸胯 detail sheet（無手杖頭）
  ② 虛形互搏 → 實=衣 · 虛=手/杖 青 dash ghost 條件板
  ③ 殘相轉生 → 綠圈 ROI 當殘 → 全形知識 → 1A 回母姿（只貼1A）
  ④ P_G紋 → peep 衣平面 × 姿鎖座標 · IP 材質貼合 · 禁 spill
  （可選）SWP 嵌 1A 後升清 · SPM residual 輔咬 peep 內
```

**樣板落盤：** `SETS/OBA_DRESS_FULLCHAIN/`  
IP · GHOST · RRT · ROI · COMPLETE/FINAL_1A_FOUR_SKILL

---

## 0.12.50.D 四技分工（幫改這圖）

| 技 | 憲位 | 幫黑裙／同類圖做什麼 | 輸出 |
|----|------|----------------------|------|
| **① 影分身合** | §0.12.47 | 出 **只有衣** 清 IP（無手／杖／頭）→ 新順金線 **身份 donor** | 全衣 IP + 胸胯 detail |
| **② 虛形互搏** | §0.12.48 | **實=衣 peep** · **虛=手／杖** 青虛線 → 杖唔搶 peep · 衣紋先對得準 | Ghost 條件板 |
| **③ 殘相轉生 RRT** | §0.12.46 | 綠圈當「殘相」→ 生全形 → **1A 回母姿**（動作不變 · 只貼 1A） | ROI + 全幅 1A |
| **④ P_G紋** | §0.12.49 | **P=peep 量尺 · G=姿鎖座標** · IP 材質貼合 · 禁 spill | 合回母姿鎖定 |

### 三綠圈 · 誰主殺

| 圈 | 主殺 | 輔 |
|----|------|-----|
| 上：肩帶亂線 | ① IP 順弧 + region | ④ P_G peep 只貼衣面 |
| 中：螺旋 C 結 | ③ RRT 1A **殺拓** + ① IP detail 胯板 | ② 虛形：杖唔搶 peep |
| 下：飄線 | ④ P_G peep∩shape 貼連續線 | ③ RRT 保同姿 |

---

## 0.12.50.E 鐵序（不可顛倒）

```
① 影分身合 → 衣／甲 IP（NORMAL 展開 · 個別自己 · 禁手杖頭入 IP）
② 虛形互搏 → cond 板：實=衣 peep · 虛=手/杖/頭 dash
③ 殘相轉生 → 不順 ROI：1殘→2全→3反補→**1A**（只貼1A）
④ P_G紋 → peep×GRID/姿鎖 + HD 材質 sheet 貼合
⑤ 合 → 姿鎖母（手杖臉死鎖）+ 衣 IP 紋 + 1A 結構 + 材質
⑥ 可嵌 → SWP 升清 after 1A/P_G · SPM residual peep 內
```

---

## 0.12.50.F 三律

1. **換拓先於升清** — 螺旋／錯順必須 ①+③ 換拓；SWP/SPM 不得冒充對紋完成（E-TEX-08）  
2. **peep 只鎖衣面** — 互動體必虛（②）；實搶 peep = 漂（E-TEX-02）  
3. **四技全過閘** — 缺一不得 LOCK 稱成功（E-TEX-03）

---

## 0.12.50.G 一刀參數卡

```
MODE=TEX4_FOUR_SKILL_ALIGN
聯動=影分身合+虛形互搏+殘相轉生+P_G紋
實=衣/甲 peep
虛=手·杖·頭（助位不入 cut）
IP=衣展開 sheet（NORMAL · 無人物）
RRT=1→2→3→1A only
PG=P_G紋 peep×姿鎖/GRID
可嵌=SWP after 1A · SPM residual peep
BAN=no_IP_free_tex, solid_hands_steal_peep, PG_only_on_residual, SWP_only_as_align, toxic_half_fix_master, four_skill_missing
SAMPLE=SETS/OBA_DRESS_FULLCHAIN/
MOTHER=22cf97df
PROBLEM_CIRCLES=ad220951
FAIL→ redo from missing skill · 不疊毒半修
```

---

## 0.12.50.H 附件

- `FOUR_SKILL_TEX_ALIGN_NAME.md`
- `FOUR_SKILL_TEX_ALIGN_01250.md`（本文）
- `FOUR_SKILL_TEX_ALIGN_DO_NOT_REPEAT.md`
- `FOUR_SKILL_TEX_ALIGN.md`（短卡）
- 子技：`SHADOW_CLONE_MERGE_01247` · `GHOST_SPAR_XU_XING_01248` · `RESIDUAL_REBIRTH_RRT_01246` · `P_G_WEN_TEX_01249`
- 樣板：`SETS/OBA_DRESS_FULLCHAIN/`

*END §0.12.50 · TEX4 四技對紋絕招 · LOCK · asof 2026-10-30T21:15:44Z*


---

## 0.12.50.I 全紋自對順（FTSA · LOCK 補 · asof 2026-10-30T22:11:49Z）

見 `FULL_TEX_SELF_ALIGN_01250I.md`。

**用戶鐵句：** 要懂自己對應**該所有紋**去順的修復效果。

**一句：** 本母 peep 全部紋區自對應 · 逐區順修到同一效果標準 · 1f795=標準非 donor · 禁跨母 PIXEL。
