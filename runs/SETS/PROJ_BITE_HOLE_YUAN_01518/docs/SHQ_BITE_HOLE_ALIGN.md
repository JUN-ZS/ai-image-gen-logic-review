# 咬合硬契約 · 01518

```
咬出一塊 → 必有洞 MARK
升清那塊 → 同 peep 大細（合適大細）
放回洞   → 置中對位 hardpaste
洞外     → bitexact
```

| 字 | 落點 |
|----|------|
| 除 | 咬走 → L1 空座 |
| 洞 | MARK = 咬的形 |
| 扣 | peep = L0⊙MARK 證咬塊 |
| 生 | 升清 peep 同尺（外力GROK） |
| 反 | outside=0 · size_lock |

**合適大細** = `I_sheng.shape == peep.shape`  
**置中對位** = 回写原 `bbox_xyxy` 座位  
**禁** freeframe 全幀當布局／無洞回
