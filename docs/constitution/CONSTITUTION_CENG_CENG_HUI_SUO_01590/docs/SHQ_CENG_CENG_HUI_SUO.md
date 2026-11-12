# 憲技 · 層層回鎖（CENG_CENG_HUI_SUO）

**write** 01590 · **formal** `SHQ_CENG_CENG_HUI_SUO_V1`  
**stick** `STICK_CENG_CENG_HUI_SUO`  
**× 勤力DNA** · 反推自 01589 / 先读错线 / E-QL-WRONG_ELEV / E-QL-SKIP_CRUSH

---

## 0. 金句

1. **每一層 densify / 升清，只能虛回自己那一層的凍座 S_k；禁止跨線冒稱。**
2. **先讀成果 → 只鎖回先讀 S11；遠景 densify → 只鎖回遠景 S11。**
3. **高像素 DENSE 保留到一槍回座；禁 peep 小圖壓碎當主 elev。**
4. **層層 = 子 S11* → 父 MARK 座 → 再外層；每步 outside=0 才開下一層。**

---

## 1. 定義

**層層回鎖** = 把「升清 / densify / 先讀 / 嵌套」的成果，**按血緣線**逐層硬鎖回對應座位，形成可繼承的 State Bus，而不是另開一條回位計劃。

```
層 k 的 elev_k / I*_k
    → 虛回 / hardpaste
    → 凍 M_k @ 本層 S_k（或父 S_{k-1} 的座）
    → ‖RETURN − S_k‖_outside = 0
    → 才允許開層 k+1 或外層虛回
```

---

## 2. 血緣線（反推 01589）

| 線 | S0 例 | S11 例 | densify 可回 |
|----|-------|--------|--------------|
| **先讀線** | be09e993 | 73c1068a（01581 RETURN_BATCH） | 01581 leaf elev · b4a0 nest · 846f |
| **遠景三物線** | 01559 L0 | 01559 FINAL | 同物 peep densify @ M_obj_* |
| **頭嵌套線** | HEAD peep | b4a0 nest RETURN | 頭內 清鎖·件 elev |

**禁**：遠景 freeframe densify 冒「先讀虛回」；先讀 elev 硬塞遠景 mecha 座仍叫先讀。

**E-code**

| 碼 | 義 |
|----|-----|
| E-CC-01 | elev 血緣 ≠ 回鎖底 S11（選錯先讀成果） |
| E-CC-02 | 跨線虛回仍掛本線 claim |
| E-CC-03 | 高像素 densify 過早壓 peep 小圖（跳步） |
| E-CC-04 | 子層未 outside=0 就開外層 |
| E-CC-05 | 無凍 MARK 座硬貼（無洞回） |

---

## 3. 與 虛回 / 先讀 / SS驗.清 的關係

```
先讀      = 結構定義 → 批量 清鎖·件（產 elev 與 S11）
SS驗.清   = 洞座硬鎖 · 升清不移位
虛回      = 已抽出升清未回 · 虛擬跟鎖回（不重開洞）
層層回鎖  = 元規則：上述每一步的「回」必須對上本層血緣 S_k
```

方程：

\[
\text{RETURN}_k = S_k \odot (1-M_k) + \mathrm{resize}(I^*_k) \odot M_k
\quad \|\,\text{RETURN}_k - S_k\,\|_{\mathrm{out}}=0
\]

嵌套：

\[
S_{k-1}^* = S_{k-1} \odot (1-M_{\mathrm{child}}) + \mathrm{resize}(S_k^*) \odot M_{\mathrm{child}}
\]

---

## 4. 勤力DNA 合閘（層層回鎖必經）

| 閘 | 層層回鎖落點 |
|----|----------------|
| **I-ID-BAN** | elev 必須可溯本線 peep0 / 先讀 leaf；禁跨身份 freeframe 冒同物 |
| **I-PROCESS** | 真 densify 在高像素完成；禁「未升清 peep 自貼」當 C2 |
| **I-SEAT** | 每層必有凍 MARK + frame；回位只經座；無洞 = E-CC-05 |
| **outside=0** | 每層回鎖閘；子 PASS 才開父/外層 |
| **claim 分級** | C2_層內 ≠ C2_跨線；先讀 claim 不可寫在遠景 FINAL 上 |

**勤力合閘** = I-ID-BAN ∧ I-PROCESS ∧ I-SEAT ∧ outside0 ∧ 血緣匹配

---

## 5. 層級表（模板）

| 層 | 輸入 | 處理 | 回鎖底 | 閘 |
|----|------|------|--------|-----|
| L0 | SRC | 凍 | S0 | SHA |
| L1 | 除/扣/洞 | MARK | — | 不重開洞 |
| 先讀/PART | peep | densify | 本 L0 或 peep 父 | out=0 |
| 嵌套 | 子 peep | 再 清鎖 | 子 S11 | out=0 |
| 虛回外 | 子 S11* | hard | 父 S11 | out=0 |
| 終極 | 支線* | 僅同物 | 該線終極 S11 | 禁偽先讀 |

---

## 6. 糾錯教材（入 ERROR_TEXTBOOK）

| 錯例 | 錯 | 對 |
|------|----|----|
| 01587 | 遠景 densify 冒先讀→01559 | 先讀 elev→73c |
| 01587 elev crush | 4f6d 壓 227 當主 | 高像素 densify→一槍回座 |
| 跨線 01585 | 雪原 elev 進遠景座 | 同物 peep densify 或分線 claim |

---

## 7. 落盤

| 檔 | 職 |
|----|-----|
| `SHQ_CENG_CENG_HUI_SUO.md` | 本正文 |
| `DNA_CENG_CENG_HUI_SUO.json` | 機讀 |
| `CONSTITUTION_LOCK_01590.json` | 鎖 |
| 勤力指針 | `CONSTITUTION_FOLDER_QINLI_DNA` 掛本技 |

**ACCEPT_FULL_HD** = false  
**claim 範例** `C2_CENG_CENG_HUI_SUO` 僅當血緣∧勤力合閘∧各層 out=0


## 补 01594

| E-CC-06 | elev 后跳过先读2 直接层回锁 |
| 金 | 先读1→Imagine elev→先读2→层回锁 |

## 补 01595 · 先读1≤50 + 先读2 discovery

| 闸 | 值 |
|----|----|
| N_MAX_XIAN1 | 50（grid+local CC；全图一团时禁只 largest） |
| M_MAX_XIAN2 | 6（true multi-CC discovery，非死4带） |
| fanout | Σ kids ≤ N×M_max（本跑 298/300） |
| elev@50 | 默认可 local densify；Imagine top-k 另批 |
| E-CC-06 | elev 后必先读2 |


## 补 01596 先讀MAX
| E-CC-08 | 先读1 后无 densify₁ 就先读2 |
| densify | ₁@先读1 · ₂@先读2 |
