# 影分身合 · IP展開 → ControlNet回母姿 → 個別合VOID
# §0.12.47 · asof 2026-10-30T19:24:59Z

> **用戶鐵句（母 4fe0469b）：**  
> 錯 · 要用**正常法出 IP 展開圖** · 再用 **ControlNet 回到這動作** · 但是是**個別的自己** ← **影分身合（技）**

---

## 0. 一句

**每人／每機先出自己的 IP 展開（身份全形）** → **用 peep／母姿當 ControlNet 條件** 把該 IP **拉回母圖同姿**（仍是個別自己）→ 再遠→近貼回 **GRID-locked VOID**。  
**不是** 只做殘相 amodal 補洞；**是** 影分身（各出 IP）+ 合（ControlNet 回姿後累貼）。

---

## 1. 正確次序（鐵）

```
母 ── peep 綠描（每人）
 │
 ├─【影】正常法 IP 展開圖（該機身份 · 可多視／全身 catalog · 非棚拍亂姿當終）
 │        = VER.IP / 展開 sheet
 │
 ├─【分身】ControlNet（或 shape-cond 等價）：
 │        REF0 = peep／母姿（動作條件）
 │        REF1 = IP 展開（身份／材質）
 │        → 個別 COMPLETE = 該 IP 的自己 · 鎖母姿
 │
 └─【合】遠→近 peep s≤1 貼 GRID-locked VOID
```

| 步 | 名 | 產出 |
|----|-----|------|
| S0 | 母 + VOID GRID 聯動 | 同線 |
| S1 | peep 綠描 | VER.1 動作條件 |
| S2 | **正常法 IP 展開** | VER.IP sheet（身份） |
| S3 | **ControlNet 回母姿** | 個別 COMPLETE（自己+母動作） |
| S4 | peep 量尺貼 VOID | FINAL 合 |

---

## 2. 與殘相轉生的分界

| | 殘相轉生 RRT | **影分身合** |
|--|-------------|-------------|
| 主線 | 1殘→2全→3反→1A | **IP展開 → CN回姿 → 合** |
| 身份源 | 從 peep 補 | **獨立 IP 展開（正常法）** |
| 動作鎖 | VER.3 反補 | **ControlNet / peep pose cond** |
| 合 | 1A 貼 VOID | 個別 COMPLETE 貼 VOID |

可聯動：IP 展開 可當 RRT 的 VER.2 身份源；但**本技名**以影分身合為準。

---

## 3. ControlNet 等價（本場）

無原生 CN 時：
```
imagine_reference_to_image
  asset_ids[0] = peep 綠 / 母姿 crop   # ControlNet 條件（位+姿）
  asset_ids[1] = IP 展開 sheet         # 身份
  prompt = 用第二圖的 IP 身份 · 強制第一圖 peep 的姿與傾角 · 單一機 · 黑底
```

**禁：** 只 RRT 不展開 IP · 棚拍自由姿當最終 · 兩機一次生

---

## 4. 毒碼

| 碼 | 禁 |
|----|-----|
| **E-SHADOW-01** | 跳過 IP 展開 · 直接 amodal 當終 |
| **E-SHADOW-02** | ControlNet 回姿時混兩機 |
| **E-SHADOW-03** | 回姿後不貼 VOID · 貼母 |
| **E-SHADOW-04** | IP 展開當最終姿（未 CN 回母） |

---

## 5. 一刀卡

```
技=影分身合
S2=正常法 IP展開（個別自己）
S3=ControlNet/peep-cond 回母動作
S4=合→GRID-locked VOID
BAN=skip_IP, free_pose_final, dual_in_one_CN
```

*END §0.12.47*
