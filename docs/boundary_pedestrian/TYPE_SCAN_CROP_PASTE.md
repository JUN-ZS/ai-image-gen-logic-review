# 字／HUD SCAN-CROP → 貼回（字唔再被人物蓋住）

> 人物 paste 會蓋住完成圖上嘅字。  
> 解法：從**首張有字圖**（first HUD／type gen）**描出字層**，再貼上 **clean 底**（或 paste 人後再貼字）。

---

## 1. 正確疊序

```text
① CLEAN 首幀（人＋場景清晰，無字）
② 首張有字圖 HUD_GEN（人可能鬼影，但字／箭／HOT 好）
③ TYPE_LAYER = isolate(HUD_GEN vs CLEAN)   ← 字從首字圖「描」出
④ FINAL = CLEAN + TYPE_LAYER（字在最上）
```

可選：若仍要用 character cutout  
`FINAL = (HUD 底 + person cutout) + TYPE_LAYER`  
但首選 **CLEAN + TYPE_LAYER**（人永遠用 clean，鬼影唔入成品）。

---

## 2. 點樣「描」字層（非再靠模型拼字）

| 方法 | 做法 |
|------|------|
| **主用 · 差分** | `mask = |HUD − CLEAN|` 大嘅像素 + 高 chroma 霓虹 | 
| 抑制 | 低 chroma 中等差分（多為皮膚鬼影）權重壓低 |
| 形態 | MaxFilter 補筆畫 → MinFilter 去雜點 → Gaussian 羽化 |
| 輸出 | RGBA：RGB 取自 **首張 HUD**，A = mask |

結果：箭咀、HOT、標題、標註來自 **first text image**；人物來自 **clean**。

---

## 3. 與人物 paste 關係

| 層 | 來源 |
|----|------|
| 場景 + 人 + 槌姿 | CLEAN（或 person cutout） |
| 字 / 力矢 / HUD | **首張有字圖** TYPE_LAYER |
| 禁止 | paste 字後再整圖 img2img |

---

## 4. SET-J 產物

- `text_paste/layers/J01_*_TYPE_LAYER.png`  
- `text_paste/final/J01_*_CLEAN_PLUS_TYPE.jpg`  
- manifest 含各 SHA-256  

---

## 5. 一鍵口令

```text
字被疊／被蓋：
1) 用首張有字圖 vs clean 做 TYPE_LAYER
2) FINAL = clean + TYPE_LAYER（字最上）
3) 唔好再 img2img 成品
```

---

## LOCK 對齊（2026-10-25）

**主定稿**以 [`LOCKED_PIPELINE.md`](./LOCKED_PIPELINE.md) 為準：

```text
FINAL = 人清晰 PASTE（例 f9925b2a 類） + TYPE_LAYER（來自首張 HUD）置頂
```

`CLEAN + TYPE_LAYER` 僅作對照／備用，**唔再做主定稿**（除非用戶改鎖）。

