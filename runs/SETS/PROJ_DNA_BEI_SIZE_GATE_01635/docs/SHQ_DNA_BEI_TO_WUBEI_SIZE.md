# DNA 有背→無背 尺闸 · write 01635

## 问题
trio 左 **有背** peep（桌+特写）与中 **無背** 除背：APPLE **大小不一样**，旧链仍 PASS。

## 为何假 PASS？
1. **outside=0** 不比较两图主体尺度  
2. 除背 canvas 被 resize 成 peep 高宽后，**主体在画布内占比** 仍可完全不同（freeframe）  
3. 无 **E-BEI-SIZE** 闸 → 尺度毒漏网

## 量
- 有背：peep 主体 bbox \(w_b,h_b\)、面积  
- 無背：除背 alpha 主体 bbox \(w_w,h_w\)、面积  
- \(s_x=w_b/w_w,\; s_y=h_b/h_w,\; s=\sqrt{s_x s_y},\; s_{area}=\sqrt{A_b/A_w}\)

## 闸
`sx,sy,s_bbox,s_area ∈ [1/1.15, 1.15]` 且 AR 锁 → 否则 **F8 FAIL**（不 rewrite）

## APPLE 本测
- 有背 bbox: **265×227** area=28600
- 無背 bbox: **201×209** area=32510
- s_bbox=1.197 s_area=0.938 sx=1.318 sy=1.086
- **F8_PASS=False** codes=['E-BEI-SIZE-01', 'E-BEI-AR-01', 'E-OUTSIDE-ALONE-01']

## 金句
有背与無背，同一物，尺度必须同锁；大小不一不得 PASS。
