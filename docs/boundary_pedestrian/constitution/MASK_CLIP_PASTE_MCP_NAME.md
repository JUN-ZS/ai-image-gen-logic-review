# 技名 · 掩抽拼

| 語 | 名 |
|----|-----|
| **正名** | **掩抽拼** |
| **粵／短** | **掩抽拼** · **用掩抽像素** |
| **英／碼** | **MASK_CLIP_PASTE** · **MCP** |
| **一句** | **MASK 從 A 母來；PIXEL 從 B 另母來；只改 MASK 區拼回 A** |
| **母招** | §0.12.60 · 連動 WNK §0.12.26.D · PIXEL §0.12.16 |
| **地位** | **LOCK（命名）** · 工具可迭代 |
| **禁稱** | 從 B 抽白當 MASK · 全圖 soft α 當拼回 · 縮定版母圖當完成 |

## 公式

```
MASK_A  = from A  (e.g. WNK kill map)
MASK_B  = resize(MASK_A → B.size, NEAREST)
CLIP    = B_pixels  where MASK_B
A_paste = A  with CLIP written only under MASK_A
```

## 口令

「上 **掩抽拼**」「跑 **MCP**」「A 掩 B 抽 拼回 A」＝ §0.12.60

asof 2026-11-02T23:00:00+08
