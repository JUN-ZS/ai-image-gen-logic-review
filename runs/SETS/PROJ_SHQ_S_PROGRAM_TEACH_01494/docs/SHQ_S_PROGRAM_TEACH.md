# S 程序教學 · 聯動生圖課綱（01494）

**formal:** `SHQ_S_PROGRAM_TEACH_V1`  
**結合：** 是 · 母源 01492 重整 ⊕ 01487 強心針 ⊕ 01489 反推 ⊕ 01493 教學板  
**範圍：** 只先做頭（大咬）Layer A→B  
**ACCEPT_FULL_HD:** false

---

## 根方程

```text
[(生,除,洞,扣)×(反)] ← 外力GROK ⊕ 強心針[認∩放大∩升質×物]
```

## 咬物契約

咬 → 洞座位 → 升清塊 → 回洞；同構必對上。

| 字 | 角色 |
|----|------|
| 洞 | 形＝抓走前座位 MARK |
| 除 | 態＝離開（外力GROK） |
| 扣 | 證＝驗票（不重寫洞） |
| 生 | 填＝洞座升級 |
| 反 | 鏡＝每步對板 |

## 偽組合（必背）

```text
獨立 PASS ≠ 可組合
可組合 ⇔ Bus ∧ 不變量 ∧ 同宣稱 ∧ 外力除生 ∧ BOOST AND ∧ 鏈頭 RESET
```

## 課綱 S0–S11

| S | 名 | 層 | 強心針 | 教什麼 |
|---|----|----|--------|--------|
| S0 | L0 凍 | A | — | 同機位原圖寫死；下游禁止重算場景 |
| S1 | 正除 | A | — | 外力GROK EDIT 去頭/件 → L1；不是 Ope |
| S2 | 正扣 | A | — | 扣只作證：差分或除背→CLIP；不重寫洞 |
| S3 | 正洞 MARK | A | — | 洞=抓走前座位；先 MARK 再咬；真洞=像素真去 |
| S4 | 部件'認' | B | REN | 強心針第1關：整件身份+閉合邊；非 band 切 |
| S5 | peep 取域 | B | — | 抽圖 ⊂ 此步；只是取域，不是升清 |
| S6 | 放大 | B | SCALE | 強心針第2關；★抽圖放大=S5+S6 only |
| S7 | 升質×物 | B | ELEV_x | 強心針第3關；外力 densify 該物；elev≠正生 |
| S8 | BOOST AND | B | — | 認∩放大∩升質 缺一禁 BOOST 正標 |
| S9 | 正生 | B | — | 洞座 seat-born 外力填；base=L_empt |
| S10 | 正回 | B | — | hardpaste @ MARK；outside=0；a |
| S11 | 反板 | B | — | 八格齊 · 牙 stamp · 宣稱分級 |

### 逐步

#### S0 · L0 凍

- **教：** 同機位原圖寫死；下游禁止重算場景
- **做：** freeze SRC, RESET_DONOR 僅鏈頭
- **Bus 寫：** SRC
- **反：** 反除的對照基
- **敗若：** 中途換底圖 / 無 freeze

#### S1 · 正除

- **教：** 外力GROK EDIT 去頭/件 → L1；不是 OpenCV 擦
- **做：** imagine_image_to_image 除
- **Bus 寫：** L1
- **反：** 反除 = L0 有 vs L1 無
- **敗若：** E-FA-12 本地假除

#### S2 · 正扣

- **教：** 扣只作證：差分或除背→CLIP；不重寫洞
- **做：** |L0-L1|, 可選 除背→M_subj
- **Bus 寫：** kou_map, CLIP?
- **反：** 反扣 = 緣反查 · 禁 self_peep
- **敗若：** E-FA-09 扣改洞主權 · E-CLIP-01 自 peep 冒 CLIP

#### S3 · 正洞 MARK

- **教：** 洞=抓走前座位；先 MARK 再咬；真洞=像素真去
- **做：** MARK 凍 M · corners_4, 真洞板 checker/void
- **Bus 寫：** MARK, corners_4
- **反：** 反洞 = 洞外 bitexact 義務
- **敗若：** E-FA-08 先除後猜 · E-FA-10 紫疊冒洞

#### S4 · 部件'認'

- **教：** 強心針第1關：整件身份+閉合邊；非 band 切
- **做：** part_role 寫 Bus, 認失敗禁放大/生
- **Bus 寫：** part_role
- **反：** 認錯 → 下游全假
- **敗若：** E-KY-BOOST-01 · E-DNA-CANCER-SELF_PEEP

#### S5 · peep 取域

- **教：** 抽圖 ⊂ 此步；只是取域，不是升清
- **做：** peep = SRC∩MARK
- **Bus 寫：** peep
- **反：** peep 必須與洞同構
- **敗若：** 整圖 freeframe 當 peep

#### S6 · 放大

- **教：** 強心針第2關；★抽圖放大=S5+S6 only
- **做：** scale-lock densify, grow_max
- **Bus 寫：** grow_max, scale_meta
- **反：** 反生尺度鎖
- **敗若：** E-FA-03 freeframe 主權 · E-KY-BOOST-02

#### S7 · 升質×物

- **教：** 強心針第3關；外力 densify 該物；elev≠正生
- **做：** 外力 elev densify on object
- **Bus 寫：** elev_candidate
- **反：** elev 只候選
- **敗若：** E-KY-ATX elev 當正生 · E-KY-BOOST-03

#### S8 · BOOST AND

- **教：** 認∩放大∩升質 缺一禁 BOOST 正標
- **做：** 三關 AND 閘
- **Bus 寫：** boost_all_three
- **反：** 弱針 = 無針
- **敗若：** E-KY-BOOST-04

#### S9 · 正生

- **教：** 洞座 seat-born 外力填；base=L_empty/洞座
- **做：** Imagine 洞座生
- **Bus 寫：** I_sheng
- **反：** 反生 = 鎖尺 · 禁 freeframe 完成
- **敗若：** E-WLG-06 本地冒生 · E-WLF3-01 無洞生回

#### S10 · 正回

- **教：** hardpaste @ MARK；outside=0；alone 不足
- **做：** R[M]=I_sheng[M], outside vs base
- **Bus 寫：** RETURN
- **反：** 反回 = 洞外≡base · 洞內≠空
- **敗若：** outside alone 當 PASS · freeframe hardpaste

#### S11 · 反板

- **教：** 八格齊 · 牙 stamp · 宣稱分級
- **做：** F8 board, claim C0/C1/C2
- **Bus 寫：** ANTI_boards, claim_level
- **反：** 跳過反 = E-FA-06
- **敗若：** E-FA-01 獨立冒全鏈 · E-FA-04 宣稱偷換

## 金句

1. 洞=座位；除=離開；扣=驗票；生=升級；回=入座；反=鏡子。  
2. 獨立 PASS ≠ 可組合。  
3. 抽圖放大只是 S5+S6；升清是 S0→S11。  
4. elev≠正生；CLIP=身份，洞=座位。  
5. 除/生=外力GROK；OpenCV 只扣、貼、反查。  
