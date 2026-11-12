# DNA · 無毒 DONOR（入憲）

**write:** 01482 · `DNA_DONOR_TOXIN_FREE_V1`  
**試錨:** 01481 · **關係:** 01480 freeframe↔外力GROK · 01478 污染洞回  
**用戶:** 記錄入DNA

---

## 一句

> **無毒 DONOR0 = L0 peep@MARK 原像素；無毒 DONOR1 = 外力GROK 只升 peep 再 scale-lock。**  
> **freeframe 全圖 = 有毒 donor，禁當 RETURN / 主 donor。**

---

## 三類

| 類 | 源 | 無毒 | 角色 |
|----|-----|------|------|
| DONOR0_PEEP_L0 | L0 peep@MARK same bbox | ✓ | 金錨 bitexact |
| DONOR1_ELEV_PEEP_ONLY | 外力 elev 只 peep · scale-lock | ✓ | 升清 donor |
| DONOR_TOXIC_FREEFRAME | 全圖 freeframe 裁 M | ✗ | 僅錯教材 |

---

## 七律 D0–D7

1. 主錨 DONOR0（可無外力）  
2. 升清 donor 必須 peep-domain 外力，禁全圖 freeframe  
3. scale-lock · grow≤max · elev_remap=false  
4. hardpaste 只填 M；outside=0 不證 donor 無毒  
5. freeframe 只可 ERROR_TEXTBOOK  
6. RESET_DONOR 每試  
7. 框牙 primary donor 必須 toxin_free  

---

## E 碼

| 碼 | |
|----|--|
| E-DONOR-TOXIC-FREEFRAME | freeframe 當 donor |
| E-DONOR-NO-MARK | 無 MARK peep |
| E-DONOR-ELEV-REMAP | elev 破座 |
| E-DONOR-LOCAL-HF-AS-PRIMARY | 本地 HF 冒充主 donor |

---

## 金句

> freeframe 全圖不是 donor，是毒。  
> outside=0 不洗 donor 毒源。  
> 無毒 = peep 原像素 ± 外力只升 peep。

---

## 試錨 01481

- project: 01475 dual mecha  
- B elev→L0 outside=0 · status PASS  
- assets: DONOR0 `86a5df0b…` · DONOR1 elev `327a8469…`
