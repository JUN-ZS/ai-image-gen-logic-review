# 升清回位 · 試錯→成功時間線
> asof 2026-11-03T05:50+08

## 1. 起：遠臉 A8B → DETECT 放大 LOCK
- 意圖：遠臉生成 → 偵測 → 升清 → 回位
- 錯：升清後用生成器對照仍可能「非原 PIXEL」；讀圖能力未自動擋錯臉

## 2. 抽人全修回貼
- 意圖：整人抽出修完再貼
- 錯：融合常=降像素；對位 peep 邊對不上

## 3. 技「大大小小」DDXX 記錄
- 對：風景 peep 可放大；人應保像素
- 錯：實作仍常把人縮進小槽（E-SCH-01）

## 4. DDXX-AR 理論修正
- 對：person_scale=1.0 · scene 遷就人 · Virtual Master
- 錯 v1：TARGET/DONOR face 錨落空 → 假 REJECT_POSE（E-SCH-04）
- v1.1b：核幾何初步過 · 腳仍待驗

## 5. 臉 PATH1E 成功 vs 人失敗
- 臉：ROI→ECC cc≥0.85→硬貼 · 母圖鎖 · 不降 PIXEL
- 人：同邏輯但單 ECC 全身不夠 · 需姿板/分區/人體標點（E-SCH-03）

## 6. ANTHRO 人體公學
- 對：分佈公式 p+t≈s·q · 可逆 scene scale
- 對：臨時升清原景人取座標後銷毀
- 錯：腳易吃岩 · panel≠native 尺度（E-SCH-11/12）

## 7. 公式硬貼試 / NATIVE_CORE_VM
- 對：a≈0.29 · donor 1.0 · VM · core_exact=1
- 待：腳底接觸 · Local Support / platform underfill

## 8. DEL 原人（失敗→成功）
- 敗：OpenCV 大 mask 連岩剷 → 浮空（E-SCH-07）
- **成：Imagine region_edit 只刪人** → 峰頂完整（IMAGINE-DEL）

## 9. CLEAN-REPASTE / 鎖位貼
- 空景或 Imagine 空峰 + 鎖 (1654,1429) 硬貼
- **STATUS: IMAGINE_DEL_LOCKED_PASTE_OK** · 用戶確認「終於對到了」

## 成功判據（本輪）

| 項 | 值 |
|----|-----|
| DEL | Imagine region 只人 |
| Paste | locked · scale 1.0 · HARDPASTE |
| core_exact | 1.0 |
| 峰頂 | 岩台在 · 人站峰 |
| formal | 3623×6263 VM |


## 2026-11-03T06:40+08 · 公式對位升格為 BEST

- 用戶確認：「記得這方法是優先啊」「公式對位是重點」「入憲 PUSH GIT」
- 新金牌：`PROJ_SHQ_MID_LEVEL_RETURN_V1`
  - 中距人 · HD 水平地 · COREFIT a≈0.3936 · S≈2.51 · donor_xy(623,821)
  - core/face exact=1.0 · `IMAGINE_DEL_LOCKED_PASTE_OK`
- 憲版升 **v1.1** · 優先法 **SHQ-BEST**
