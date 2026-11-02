# §0.12.60 掩抽拼 · MASK_CLIP_PASTE / MCP

> asof 2026-11-02 · 正名入憲  
> 樣板：A=`OUT_WNK` 3584×2016 SHA `0d1dd797…` · B=FAIR_e283／目標 10d59 · OUT SHA `2d37472a…`

## 0.12.60.A 一句

> A 母留下的 **MASK** 放到 **B 另母** 上 **CLIP 像素**，再 **硬寫回 A** 的 MASK 區。

## 0.12.60.B 步驟

| 步 | 名 | 產 |
|----|-----|-----|
| 1 | 備 A 與 MASK | 通常 A_WNK + WNK_KILL_MASK |
| 2 | 備 B 另母 | 同構圖乾淨／高質像素源 |
| 3 | MASK→B | `NEAREST` 縮放 |
| 4 | CLIP | BGRA 或 RGB×mask |
| 5 | 拼回 A | 只寫 `MASK_A>T` 像素 |
| 6 | RESULT JSON | SHA／wh／kill_frac · pixel_drop=false |

## 0.12.60.C 尺寸

- **定版母圖不降 PIXEL**（貼回後若要 7k，先升清再 MCP，或全程 7k）
- MASK 縮放 **NEAREST**；像素插值可用 LANCZOS（只動中間體）

## 0.12.60.D 工具

- `pipe_mask_clip_paste.py`（artifacts／可鏡像 UP-engine tools）
- 上游：`tools/wnk_white_noise_kill.py` → MASK

## 0.12.60.E 證據樣板

| 檔 | 值 |
|----|-----|
| A_WNK | SHA `0d1dd797f54ec00f1ffd10fa5fa955ce0bb0d9273d26e39239d993f1831a3d0a` |
| A_paste | SHA `2d37472a9415b88def371286a58dced9fd3244e88934714378b009fccba85442` |
| kill_frac | ≈0.21 |
