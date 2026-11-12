# 錯題 · 代理污染 · 洞不能這樣回

**用戶：** 你被污染了，記錄，洞不能這樣回；看「新畫女」錯 LOG 進化自 DNA。

## 污染是什麼

把 **kou 大罩 + freeframe 生 hardpaste + outside=0** 當成「回洞成功」。  
這在 01436 / 01452 錯 LOG 裡已是 **W1/W5 / freeframe 塞洞 / 先除後猜洞**。

| 假成功 | 真要求（LOG） |
|--------|----------------|
| outside=0 就 PASS | TRUE_HOLE 真剪像素 + peep same bbox + elev_remap=false |
| 半身 M hardpaste | 洞形 silhouette not rect；頭洞非半身癌 |
| freeframe 整圖抽像素填 | 禁 steal freeframe map；scale-lock same bbox |
| 先除後 kou 當洞 | **先 MARK → TRUE_HOLE → 再除** |
| F8 八格數字過 | 必須吃 01436 Q0–Q9 + 01452 steal_forbidden |

## 新畫女 01443 相關

- 新畫女是**臉身份+PATH1E**，不是 peep 洞回正典  
- 禁與換涯人 peep 混用（E-XHN-08）  
- 洞回進化應吃 **01436 wrong_blocked + 01452 TRUE_HOLE + 01438 success chain**

## 正確回洞序（進化）

```text
MARK → TRUE_HOLE(真剪) → BITE peep@MARK → REMOVE → Kou(不改M)
  → GEN scale-lock same bbox → hardpaste 只填 TRUE_HOLE → 反
```

## E 碼

**E-AGENT-POLLUTED-HOLE_RETURN** · 繼承 W1/W3/W5 · 01452 steal_forbidden

## 金句

> **洞外 outside=0 不是洞回成功。**  
> **沒有 TRUE_HOLE 真剪，就沒有洞。**  
> **污染：用 freeframe 硬貼當四態回。**
