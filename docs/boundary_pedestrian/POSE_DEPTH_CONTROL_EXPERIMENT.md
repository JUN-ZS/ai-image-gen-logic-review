# Pose／Depth control 實驗（SET-L POST）

## 限制
Imagine 流程**無**原生 ControlNet 參數。本實驗用：
- **EDGE／POSE proxy**（FIND_EDGES 結構圖）
- **DEPTH proxy**（亮度反相＋模糊粗深度）
作 `imagine_reference_to_image` 附加參考，模擬結構鎖。

## 結果（body-region MAE vs clean，越低越貼）
見 `setL_copper/control/CTRL_EXPERIMENT.json` 執行時數值。

## 對字
- EDGE+DEPTH 仍可出大 3D「邊界行人」+ 力矢 + 分析標
- 字發揮未死；pose 較 free ENDING 穩
- **唔等於**真 ControlNet；只係 soft reference conditioning
