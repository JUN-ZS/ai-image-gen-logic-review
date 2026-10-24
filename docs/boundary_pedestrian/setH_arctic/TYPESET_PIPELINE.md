# SET-H 入場修正 · 字軌 + 女主鎖

## 問題（用戶誠實反饋）
1. 模型自行拼字 → 入場感差、字形漂移
2. 女主未鎖 → 每幀換人

## 解法（已落地 artifacts，設定上 branch）

### A. 女主 root
- ID: `BW_HEROINE_SET_H_V1`
- `HEROINE_BODY` + `HEROINE_FACE` 雙參考
- 之後每幀：`reference = [WORLD, BODY, FACE]`，prompt 寫「exact same woman」
- 見 `heroine_lock/HEROINE_LOCK.json`

### B. 字 = 真 SVG 排版（非模型）
- 流程：先出**無字** clean PRE/MID/POST → `setH_try_art_typeset_v1` 疊 SVG → PNG
- 字元由 `WenQuanYi Zen Hei` 寫死
- PRE=`before` 冷青｜MID=`middle`｜POST=`after` 熱橙
- **無** TRY 次數、**無** REVIEW PENDING
- LOOP = `L-` + clean MID SHA12
- 浮雕 3D poster 板約 38%×72% 區，可 left/right

### C. 產物路徑
```
boundary_pedestrian_setH_arctic/
  heroine_lock/
  frames_v2/{pre,mid,post}/*_clean.jpg
  typeset/out/H02_H2_*_TYPESET.jpg
```

### D. 下一 AI 硬規則
1. 禁止用 imagine 生成方法名漢字
2. 必須帶 heroine lock 參考
3. 字只走 typeset 軌

## v2 · 世界融入 + 物理綁定（2026-10-25）

用戶：字一定要美麗地融入世界；前後幀字要表達跟圖的 INFO 和物理關係。

### 改動
- **無底板** solid panel 取消
- 字 = 冰霜 glow 浮雕層，位置流動、可旋轉，貼場景氣流／打擊軸／碎裂場
- **PRE**：`PRE_NEAR` · `signed_gap ≫ 0` · `F_n→0` · `Crack=0` · STRIKE pending · RECV far
- **MID**：`FIRST_CONTACT` · `GAP=0` · `n·v=1` · `F_n` · shock-ring · REJECT CHEEK…
- **POST**：`REACTION` · `Crack≫0 +δt` · impulse 力鏈 END→HEAD→HANDLE→GROUND · follow-through

字形仍 **WenQuanYi 寫死**，非模型拼。女主鎖不變。
產物：`typeset_world/out/H02_H2_{pre,mid,post}_WORLD.jpg`
