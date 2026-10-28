# 正衣×人主 試換成功樣板 · ZPS（LOCK 附 SCD/ETZ）

> asof 2026-10-29 · 用戶：「試換, 如果成功就入憲」  
> **donor 正衣** `090a9ce3` · **人主** `355eca85` · **★直換** `d026c44b`

## 成功條件（本樣板全過）

| 閘 | 結果 |
|----|------|
| 中心 motif | 葉紋跟 090a · 非另抽星 |
| 人槽 | 臉／髮／姿／杖在 |
| 衣槽 | 蜂窩銅線語＝正衣 |
| 手套 | **直換保留甲手套**；SCD 睡衣會清掉手套（衣槽連手套） |

## 配方（入憲）

### 路徑 A · 直換（donor 已強正衣時優先）
```
Ref([PERSON_355e, ZHENGYI_090a],
  "Change only the clothes to the exact armor dress in the second image.
   Keep same face hair pose hands crescent staff.")
→ ★ d026
```

### 路徑 B · SCD 清槽（舊網鎖死時）
```
i2i(PERSON, pajamas CLEAR)
Ref([CLEAR, ZHENGYI_090a], change clothes only)
→ 89fe  · 注意：手套若屬甲，會被清槽清掉
```

## 與半齊毒
正衣 090a 已鎖葉紋 → 合身只轉移 → **中心 motif 不重生** → 破 MSR-HALF。

## 連動
SCD §0.12.37 · ETZ E2 · ZYF · S1 同姿換衣
