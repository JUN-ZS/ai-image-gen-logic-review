# 技法技能 · OCCLU-COMPLETE / ASC
**憲位** §0.12.45 · 全文 `OCCLU_COMPLETE_ASC_01245.md`  
**asof** 2026-10-30T17:13:34Z

## 正名
| | |
|--|--|
| 短碼 | **OCCLU-COMPLETE** / **ASC** |
| 中 | 補擋全機 · 無遮擋 solo 補全 |
| 英 | Amodal Solo Complete |
| 一句 | peep 殘形 → amodal 先驗補肢 → hard α → peep s≤1 腳錨 → 遠→近一人一刀 |

## 技能四層（說明入憲）
1. **Amodal prior** — 完整機體訓練先驗  
2. **shape-cond** — peep／shape_pad 殘形外推  
3. **explicit complete prompt** — full unoccluded · reconstruct blocked · no other mechs · black bg  
4. **solo isolation** — 隔離棚拍逼全身商品圖  

## 鐵序短卡
`T_asc0 peep → T_asc1 pad → T_asc2 i2i complete → T_asc3 hard α → T_asc4 s≤1 foot recall → T_asc5 far→near paste`

## 閘
recall peep≥0.4 · spill=0 · s≤1 · 遠→近 · TAG=COMPLETE_IMAGINED

## 樣
BATTLE6 COMPLETE · C=`ccdec01e` · 變體=`7344994c`

## 禁
E-ASC-01..06 · E-OBA-23 · 見 `OCCLU_COMPLETE_ASC_DO_NOT_REPEAT.md`

*技能卡 · 憲正文以 §0.12.45 為準*

---

## ASC × OBA .M 嵌接（asof 2026-10-30T18:26:00Z · 入憲）

ASC 補擋 **仍受** §0.12.44.**M** 約束：

```
每件：母 peep 綠描 REF（原本動作）
  → OCCLU-COMPLETE i2i from REF（同姿 · 禁自由棚拍）
  → peep s≤1 腳／心錨
  → **一次一件** 遠→近累貼
  → STEP 線對看自審（REF｜HD complete｜accum）
```

| TAG | 用法 |
|-----|------|
| `COMPLETE_IMAGINED` | 自由補全（舊） |
| `OCCLU_COMPLETE_SHAPECOND` | **f168／.M 正路** · REF shape-cond 同姿 |

禁：E-OBA-25/26/27 對 ASC 同樣生效 · 禁 batch ASC 無 STEP。
