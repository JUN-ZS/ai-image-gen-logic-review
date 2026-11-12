# 外力如何回到正洞（01495）

**formal:** `SHQ_WAI_LI_RETURN_TO_ZHENG_DONG_V1`  
**掛：** S 程序 01494 · S4–S6–S9–S10  
**ACCEPT_FULL_HD:** false

---

## 你問的兩段

1. **外力認出** S4：咬出的將在 S5 成為「整體中的一個獨立部件」，再 S6 放大。  
2. **最重要：** 如何用**外力**幫助**回到正洞**。

---

## S4 → S5 → S6（外力認件）

| 步 | 外力角色 | 結果 |
|----|----------|------|
| **S4 認** | 外力理解整件身份 | 咬出塊 = 整中之**獨立部件** |
| **S5 peep** | 取域 SRC∩MARK | 該部件像素樣本（身份） |
| **S6 放大** | scale-lock 該件 | 升密度；**尚未回洞** |

> 抽圖放大只到這裡；**回洞是另一段外力座生。**

---

## 最重要：外力回正洞（R0–R4）

```text
正洞 MARK = 座位（形·機位·座標）
peep/部件  = 身份（是誰/哪一塊）
外力座生   = 在「有洞的同機位圖」上，只往座位填身份
hardpaste  = 證：洞外不動、洞內入座
```

### 合法鏈

1. **R0** 正洞在座：MARK 凍 · L1 真空位  
2. **R1** 外力認件完成：獨立部件 peep（+可選 elev 候選）  
3. **R2 關鍵** **外力 seat-born**：  
   - `base = L1`（或真洞圖）同機位  
   - Imagine：只在洞座填回該部件  
   - ref = peep / CLIP / elev* 只當身份  
   - → `I_sheng`  
4. **R3** `RETURN[MARK] = I_sheng[MARK]` · outside=0  
5. **R4** 反洞/反回板  

### 公式

```text
I_sheng = 外力GROK( base = 有正洞的同機位圖,
                     ref  = 獨立部件 peep )
RETURN  = hardpaste(base, MARK, I_sheng)
s.t.    out[¬MARK] = base[¬MARK]
```

### 角色分離（禁混）

| 角色 | 是 | 不是 |
|------|----|------|
| peep | 身份 | 完成圖 |
| elev_candidate | 升質候選 | 正生 / RETURN |
| I_sheng | 洞座外力生 | freeframe 特写 |
| MARK | 正洞座位 | 可事後重算 |
| RETURN | 入座證 | 無洞創作 |

---

## 為什麼必須外力回洞

- 本地 densify 再 warp → 易對不回座位（elev_remap）  
- 外力在**洞座上**生 → 同機位填空，對的是 MARK  
- **身份與座位分離**：peep 是誰，MARK 坐哪，外力在座上結合  

## 禁

- elev 當 RETURN · 無洞 freeframe 回 · 重算洞 · OpenCV 冒生 · 不認就放大回  

## 金句

> peep 管身份，MARK 管座位；外力在座上把身份填回正洞。  
> S6 放大還在件上；回正洞是 S9 外力座生 + S10 入座。  

asof 2026-11-10T01:39:47.835607+00:00
