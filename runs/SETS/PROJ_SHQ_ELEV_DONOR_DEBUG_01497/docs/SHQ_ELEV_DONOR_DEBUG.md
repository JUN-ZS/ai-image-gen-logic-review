# 放大繼承對的原 · ELEV/DONOR 錯用 DEBUG（01497）

**formal:** `SHQ_SCALE_INHERIT_ORIGIN_ELEV_DONOR_DEBUG_V1`  
**框牙更新 · 強心針 S6/S7 + donor**

---

## 更新一句

> **放大的物件要繼承對的原。**  
> **DEBUG 根因：ELEV 和 DONOR 的錯用。**

---

## 對的原是什麼

```text
peep₀ = SRC ⊙ MARK     ← 唯一「對的原」
```

| 角色 | 是 | 不是 |
|------|----|------|
| **peep₀** | 對的原 · 放大起點 | elev 特写 |
| **peep_s** | scale_lock(peep₀) | 任意 freeframe scale |
| **elev*** | densify(peep 域) 候選 | 原 / 正生 / RETURN |
| **donor** | peep₀ 或 elev*(peep) 可溯原 | 全景 freeframe elev |
| **I_sheng** | 外力洞座生 ref=donor | elev 直出 |
| **RETURN** | hardpaste MARK | elev 貼圖 |

---

## 正確繼承鏈

```text
SRC → MARK → peep₀（對的原）
         → scale_lock(peep₀)     # 放大繼承原
         → elev* = densify(peep) # 只升 peep 域
         → donor ∈ {peep₀, elev*}  # 同源
         → I_sheng = WLG(base=洞座, ref=donor)
         → RETURN = hardpaste
```

## DEBUG 錯用表（E-ED）

| 碼 | 錯 |
|----|-----|
| **E-ED-01** | elev 當「對的原」再放大/回 |
| **E-ED-02** | donor = 整圖 freeframe elev |
| **E-ED-03** | elev 當正生 / RETURN |
| **E-ED-04** | donor 來自錯 SRC / 錯洞 |
| **E-ED-05** | 放大未綁 peep₀ |
| **E-ED-06** | freeframe donor 毒（01481） |

---

## 金句

1. 放大繼承 **peep@MARK**，不繼承 freeframe elev。  
2. elev 是 peep 的升質子代，不是原。  
3. donor 必須可溯 peep₀。  
4. 回洞仍靠外力座生 + MARK，不是 elev 貼回。  

asof 2026-11-10T01:57:10.276069+00:00
