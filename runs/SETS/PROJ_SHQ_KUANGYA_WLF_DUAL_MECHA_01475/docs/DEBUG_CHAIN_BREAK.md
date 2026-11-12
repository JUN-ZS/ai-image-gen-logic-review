# DEBUG · 鏈斷 · 回不了原圖 · 外力GROK

## 記錄
用戶：鏈斷了，回不了原圖，要重走 DEBUG，外力GROK 介入。

## 斷點
- 除 freeframe：L1 洞外 ≠ L0（max=227）
- 生 freeframe：I 洞外 ≠ L0/L1
- 把整張 freeframe 當 RETURN → **回不了原圖**

## 修
```text
RETURN = L0.copy()
RETURN[M] = 外力GROK_I[M]   # 只填洞
assert maxdiff(RETURN, L0, ~M) == 0
```
本跑 primary outside_vs_L0 = 0
