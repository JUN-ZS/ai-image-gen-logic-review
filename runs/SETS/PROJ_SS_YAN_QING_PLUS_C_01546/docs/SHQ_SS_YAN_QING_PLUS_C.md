# SS驗.清+C

**call**: `SS驗.清+C`  
**formal**: `SHQ_SS_YAN_QING_PLUS_C_DETECT_MARK_V1`  
**write**: 01546

## 一句
检测外力给 whole 框（开放词）→ bbox 建 MARK → peep → 清/清锁；无 API 时 boxes_json/manual 契约，禁静默冒 whole_subject

## 方程
```
SS验.清+C ≡ Detect(L0, labels)→{bbox_i,score_i} → MARK_i=fill(bbox)[+refine] → anti(area) → peep → [清锁] F2
```

## Providers
| provider | 说明 |
|----------|------|
| http_open_vocab | `DETECTION_API_URL` POST labels+image |
| boxes_json / manual_bbox | 上游已给 boxes |
| unavailable | E-QC-00 禁冒 whole_subject |

## vs +A
| +A | +C |
|----|----|
| 除主 L1 差分洞 | 检测框 whole |
| 要空景 | 不依赖 L1 |

ACCEPT_FULL_HD=false
