# 升清回位 · 子技能總表 v1.1
> asof 2026-11-03T06:45+08 · 父技 **SHQ / 升清回位 §0.13.01 · write 01263**

| 子碼 | 正名 | 一句 | 何時用 | 禁 |
|------|------|------|--------|-----|
| **SHQ-BEST** | 優先金牌鏈 | 公式+DEL+1.0 硬貼 | 默認主路徑 | 跳過 COREFIT |
| **SHQ-ANTHRO** | 人體公學標點 | 臉手腳軀幹作標 · 分組 residual | 估 a,R,t 前 | 腳點吃岩；單點定 scale |
| **SHQ-COREFIT** | 核心擬合 | 只 Face+Torso 估 a | **任何 scale 判決（重點）** | Legs 進擬合 |
| **SHQ-GROUND** | 地平鎖 | sole 水平=原圖 | HD plate 與貼回 | 斜腳不修就貼 |
| **SHQ-DDXXAR** | 大大小小-AR | Scene 放大、人 scale=1.0 | 人大於格位 | 人縮放；回縮 VM |
| **SHQ-VM** | Virtual Master | 擴畫布容納 1:1 人 | 交付主圖 | 與固定小母三條件同時硬鎖 |
| **SHQ-LOCKXY** | 鎖位硬貼 | 記 donor_xy 整數貼 · core bit-exact | 一切最終貼 | 軟α當完成 |
| **SHQ-PATH1E-F** | 臉 PATH1E | ROI peep→ECC≥0.85→硬貼 | 同構臉 peep | 異構 peep 直 ECC |
| **SHQ-PATH1E-P** | 身 PATH1E | 多 ROI 或標點板→硬貼 | 全身換 | 單 ECC 套全身 |
| **SHQ-POSEPLATE** | 姿態板 | 中/遠姿+高清身份合併 | 異構 peep | 無板硬 ECC |
| **SHQ-IMDEL** | Imagine 精刪 | region_edit 只人+披風 | 原景有人要空槽 | OpenCV 連岩大剷 |
| **SHQ-EMPTY** | 空景主權 | 無女主原景作 warp 底 | 重貼/換 donor | 半修毒底再貼 |
| **SHQ-LS** | 局部支撐 | 只 sole 下補岩/影 | 黑縫/接觸 | 為補腳重估 a |
| **SHQ-PLAT** | 峰頂 underfill | sole 以下深腔補岩 | 大黑腔 | 塗到瀑布/遠山 |
| **SHQ-ACORE** | ACCEPT_CORE | 臉甲 exact+Core lm | 身份通過閘 | 用 Legs 否決 CORE |
| **SHQ-AFULL** | ACCEPT_FULL | CORE+接觸+披風+觀感 | 最終 | 未過仍稱完成 |
| **SHQ-CAPE** | 披風覆蓋閘 | Body/Cape mask 分驗 | 有披風 peep | ROI 切尾仍稱全 |
| **SHQ-ANCHOR** | 錨點審計 | 同源定位·落區有效 | 任何 REJECT_POSE 前 | 背景點進 E |
| **SHQ-SHA** | 像素主權證 | donor core SHA = out core | 交付 | 無 SHA 稱 exact |
| **SHQ-FARFACE** | 遠臉管線 | 遠臉 detect→升清→回 | 只臉任務 | 遠臉公式硬套全身無升級 |
| **SHQ-REPASTE** | 記位重貼 | 空景 + 舊 donor_xy 再貼 | 換空景後 | 無故重估 a |
| **SHQ-PEEP** | 窺窗 | 完整頭身腳披風 | 抽姿 | peep 過遠過小 |

## 子技依賴（SHQ-BEST 最小可跑）

```text
SHQ-PEEP + SHQ-POSEPLATE
  + SHQ-ANTHRO + SHQ-COREFIT + SHQ-GROUND
  + SHQ-IMDEL + SHQ-DDXXAR + SHQ-VM
  + SHQ-LOCKXY + SHQ-SHA
  → SHQ-ACORE → IMAGINE_DEL_LOCKED_PASTE_OK
  → (可選) SHQ-LS / SHQ-PLAT → SHQ-AFULL
```

## 命名速查

| 口語 | 子碼 |
|------|------|
| 這方法優先 / 公式對位 | **SHQ-BEST** + **SHQ-COREFIT** |
| 大大小小 | SHQ-DDXXAR |
| 不降 PIXEL 拼回 | SHQ-LOCKXY + SHQ-SHA |
| 清鬼重貼 | SHQ-IMDEL 或 SHQ-EMPTY + SHQ-REPASTE |
| 人體公學對位 | SHQ-ANTHRO + SHQ-COREFIT |
| 地平一致 | SHQ-GROUND |
| 終於對到了 | IMAGINE_DEL_LOCKED_PASTE_OK |
