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

---

## 姿漂備註（F-POSE · 與 SCD 同）

> 試錯：`9486` ZPS 後變全身立 · 姿主 `60a` 是舉杖半身側望 → **動作不一樣＝姿漂** 非正衣問題。

| 要 | 不要 |
|----|------|
| `Keep EXACT same pose crop head turn staff height grip` | 只寫 keep face |
| 半身姿主 → 半身出 | 半身姿主 → 無聲變全身大裙構（除非接受構變）|
| 走／舉／坐 **分開** 樣板 | 跨 GOU-B 新構 與 ZPS 掃衣 混比 |

**殺樣板：** 姿主 `60a` + donor `4b74` → 姿鎖 ★ `91e9`（舉杖同動作）  
**走姿另軌：** `bf2e` → `1e1b`（本來另一動作，不算 9486 失敗）

### 一句
> **ZPS 成功＝衣對 + 姿仍是姿主；衣對姿漂＝F-POSE-01 未過閘。**
