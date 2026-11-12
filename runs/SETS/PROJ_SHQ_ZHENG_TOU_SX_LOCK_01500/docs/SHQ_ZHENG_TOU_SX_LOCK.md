# 正頭 · 強心針 · (S)×(S) 遞迴鎖（01500）

## 技名：正頭

**正頭** = Imagine 原生 EDIT 多層（有頭×無頭 · 有背×無背）認洞 + **洞框內 INPAINT** 生頭 → **對位正確**。

- 解：洞錯位 / 剪影 hardpaste 偷步  
- **不解 alone**：強心針全鏈、S 層回鎖  

## 問題

正頭對位對了，但 **框牙強心針** 會因 **升清鏈沒有回到各 (S) 層** 而失敗。

升清（S4–S7）若只往前漂、不把結果 **回鎖 Bus[S_i]**，則 S8 AND / S9 座生 / S10 回 讀到斷層。

## (S)×(S) 遞迴鎖（可能）

```text
∀ S_i: out_i → Bus[S_i] 寫死
∀ S_j (j>i): 消費前 reload Bus[S_i]
升清邊: S6×S5 · S7×S5  （子代指回 peep0，不覆蓋）
正頭邊: S9×S3 · S10×(S3×S9)
強心針: S8×(S4∩S6∩S7) 且三關已 SX 回鎖
```

| 鎖 | 對 | 寫 |
|----|----|----|
| SX-S3 | S3×S3 | MARK 凍 · 正頭洞回寫 |
| SX-S5 | S5×S5 | peep0 只讀 · 永不覆寫 |
| SX-S6 | S6×S5 | peep_s · parent=peep0 |
| SX-S7 | S7×S5 | elev* 子代 · 不占 peep0 |
| SX-S8 | S8×(S4∩S6∩S7) | BOOST AND + SX |
| SX-S9 | S9×S3 | 正頭 INPAINT 綁洞座 |
| SX-S10 | S10×S3×S9 | 回綁洞+生 |

### 五種落實可能

1. **Bus 槽分離** peep0 | peep_s | elev* | I_sheng  
2. **parent_sha 邊** 子代必須可溯 peep0  
3. **正頭後 REBIND S3** 只允許正頭完成時更新 MARK  
4. **S×S 閘門表** 進 S_j 前 checklist  
5. **升清回灌 peep_child** 不占 peep0  

## E 碼

E-SX-01 升清未回鎖 S 層 · E-SX-02 elev 覆寫 peep0 · E-SX-03 放大孤兒 · E-SX-04 MARK 未回綁 · E-SX-05 強心針無 SX  

## 金句

> 正頭解對位；**(S)×(S) 解強心針與升清連動**。  
> 升清每刀完，立刻回鎖；下一刀只讀鎖。  

asof 2026-11-10T02:19:14.140703+00:00
