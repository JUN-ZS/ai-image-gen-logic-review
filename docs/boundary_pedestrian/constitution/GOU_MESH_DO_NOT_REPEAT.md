# GOU_MESH_DO_NOT_REPEAT.md
# 病毒 → 錯走 → 勾勾：永久黑名單（不要重蹈）

> asof 2026-10-27T14:38:15Z · 對齊 §0.12.23 / .24 / .25  
> **用戶：**「把我試出這方法的重重錯走病毒到現在這勾勾圖的方法入憲和流程」

---

## 0. 一句話

**錯走了 N 刀才到勾勾。下列每條都曾真發生過；再犯 = 結構 FAIL。**

---

## 1. 病毒族（母底）

| ID | 錯 | 症狀 | 殺法 |
|----|-----|------|------|
| **V-01 VIRUS_LOCAL_BASE** | 用單一局部 crop（胸甲／無頭 torso）當「全圖」母底再升 | 姿勢光邊鎖死 PART；失敗區放大成全圖病毒 | BASE 只准全幅 native |
| **V-02 UP_LOCAL_PRETEND_FULL** | 先升局部 → 再當全圖 | 上半有網下半無；「有／無」分界 | 從全幅裁 crop，不倒過來 |
| **V-03 TOXIC_PLATE_AS_BASE** | 把已拼假底／舊 GEN 當新母 | 層層模糊、岔邊 | 回正典全幅（如 f5／947／aee 系） |
| **V-04 CHEAT_OLD_FORMULA** | 拼貼公式偷用 OLD 底結構 | 上半服裝沒併到全圖 | 母底 SHA 寫 META 可核 |

## 2. 拼貼錯走

| ID | 錯 | 症狀 | 殺法 |
|----|-----|------|------|
| **P-01 BOX_PASTE** | 整 ROI 方框 α 蓋回 | fill≈1 · 方塊感 · 背景火一起糊 | 拼 = 不規則形狀 α |
| **P-02 PATCH_UPPER_ONLY** | 「無」區只補上半 | 整體不均 · 假進步 | WHOLE 全板 uniform |
| **P-03 REV_AS_CONTENT** | 反推像素當 full-RGB 貼 | lap 崩 · 假紋 | 反推 **只定 RANGE** |
| **P-04 SOFT_RGB_COVER** | soft GEN 全色蓋硬母 | 清晰崩（CHEAT_B） | V5：MF Δ + base HF 保留 |
| **P-05 OLD_EDGE_LOCK** | 借 OLD／CONST 邊「省算力」 | 岔邊 · 錯鎖輪廓 | 衣板 **自認** 新邊界 |
| **P-06 FILL_FAKE_SHAPE** | mask 填滿 box 冒充形 | fill>0.90 | fill 閘 [0.30, 0.75] |
| **P-07 NO_AFFINE** | 不比對就硬貼 | 錯位鬼影 | template + AFFINE ECC |
| **P-08 LOW_NCC_ACCEPT** | ncc<0.55 仍稱完成 | 衣漂 | 目標 affine ncc≥0.75 |

## 3. 對位／分支錯認

| ID | 錯 | 症狀 | 殺法 |
|----|-----|------|------|
| **A-01 LEFT_BRANCH** | 錯認左母／節外錯枝 | 左右岔邊 | 鎖定正確 INTO／右母 |
| **A-02 WRONG_DONOR_LOCK** | GEN 鎖錯圖（非 7f5 密網） | 網不密／形不對 | mesh donor 寫死 asset |
| **A-03 HARD_SCALE_NO_TEMPLATE** | 硬縮放填 box 無 template | ncc≈0.36（F5 v1） | multi-scale match 先 |
| **A-04 FEATHER_BLAME** | 錯位當 feather 問題 | 治標不治本 | 先對位再羽化 |

## 4. 材質／升清假法

| ID | 錯 | 症狀 | 殺法 |
|----|-----|------|------|
| **M-01 EDGE_ONLY_SHARP** | 只硬提邊不 GEN 紋 | 假清 · 無網孔 | 局部 GEN 重組密網 |
| **M-02 WEAPON_TOUCHED** | 升甲連武器柄一起改 | 拓撲漂 | weapon soft/hardlock Δ≈0 |
| **M-03 PIXEL_STEAL_DOWN** | 偷壓像素灌 MB | 比原更糊 | 全幅混放大再拼 · 超 MB 真細節 |
| **M-04 SIAX_FULL_OIL** | 全副 Siax 無 GRID | 油面假紋 | GRID 地圖 + 好區寫 |

## 5. 態度錯

| ID | 錯 | 殺法 |
|----|-----|------|
| **T-01 DENY_PROGRESS** | fill≪1 且 lap 升仍喊全敗 | 進展寫憲 · 繼續下一刀 |
| **T-02 SAVE_COMPUTE_LIE** | 借 OLD 底自稱省算力 | 禁止 |

---

## 6. 實證錯刀 → 正解（時間線摘要）

```
局部 PART 當母 (virus)
  → 上半有網下半無 / 全圖更差
  → 用戶診斷：病毒
  → §0.12.23 KILL VIRUS_LOCAL_BASE

只補「無」上半 / 反推當內容 / 貼錯位
  → §0.12.24 WHOLE · 反推=RANGE · V5 · affine

方框拼 / 借 OLD 邊 / fill≈1
  → 用戶：拼一定不是方框 · DETECT 改動邊界
  → §0.12.25 GOU_DETECT_SHAPE

f5 衣放大密網試：v1 ncc0.36 fill0.89 FAIL
  → v2 template+affine+勾 fill0.575 ncc0.82 OK
  → L-8ed30b6e8fe0 樣板
```

*END DO_NOT_REPEAT · 2026-10-27T14:38:15Z*
