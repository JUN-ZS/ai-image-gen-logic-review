# REF 原本動作法 · 線對看 · 真一人累貼
# OBA §0.12.44.**M** · asof 2026-10-30T18:30:45Z

## verbatim（用戶 · 重要）
> 而且他是一次一次加物件入圖啊，每次都對位自審，並會在每物件都出一 REF 出來的圖去用那物件「原本」的動作 — **重要**。

## 法
| 項 | 法 |
|----|-----|
| 一次一件 | VOID 起 · 每輪只 paste 一件 · accum/NN_AFTER_L |
| 每物件出 REF | 綠 peep 板 = 母原本動作 · REF/L_REF_ORIGINAL_POSE.jpg |
| 用 REF 蛹／生 | HD 必須 i2i from REF · 同姿 · 禁自由棚拍 |
| 每次對位自審 | STEP 三格 mandatory：REF｜HD｜accum |
| 線對看 | 半透綠 peep vs 紅 paste · GRID+字母 · 全 STEP 蒙太奇 |

## 鐵序
```
for L in far→near:
  1. emit REF(L)           # 綠 peep = 母原本動作
  2. HD = i2i_from_REF(L)  # 蛹同姿
  3. cut · peep s≤1 · paste ONE onto accum
  4. STEP 線對看自審
  5. pass → next L
```

## 毒碼
| 碼 | 禁 |
|----|-----|
| **E-OBA-25** | 無 REF 或 HD 非由 REF 生 · 自由棚拍 |
| **E-OBA-26** | batch 生 HD 再一齊貼 · 非一次一件 |
| **E-OBA-27** | 無 STEP 線對看 · 只交 final／圖冊 |
| **E-ASC-07** | ASC 無綠 peep REF 同姿 |

## 樣
`SETS/OBA_MIX_ROBOT_SHIP/ONE_BY_ONE/`

見主憲 `ONE_BY_ONE_ACCUMULATE_OBA_01244.md` · **.M**


---
## 升格 · 殘相轉生（asof 2026-10-30T18:35:44Z）

「用 REF 生 HD」**不是** 一步 complete 完事。  
完整鏈見 §0.12.46：

```
1 REF 原 → 2 生全形 → 3 反補(動作=1) → 1A 落地 cut
```

**最終貼 1A** · 唔貼 2。
