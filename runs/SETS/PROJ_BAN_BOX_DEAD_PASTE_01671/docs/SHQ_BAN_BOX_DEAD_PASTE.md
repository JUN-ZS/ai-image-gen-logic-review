# 禁框死贴 · DNA 01671

## E-BOX-01 DEAD_RECT_PEEP_PASTE

用户指出（crop 死框）：壶被**方框式**整块贴回，直角切景，像印章，不是镂空座贴。

### BAN
- peep / elev 按 **bbox 矩形** 整框 hardpaste
- 任何可见 **直角死边**
- 无剪影 mask 的框贴

### MUST
```
R = hardpaste(base, donor, M_silhouette)   # 不是 bbox
R[M_aperture] = base                       # 内腔透光
```
禁止：`R[y0:y1,x0:x1] = peep_resized`

### 教材
error_textbook/E_BOX_01_* 

PASS=False asof 2026-11-12T04:39:11.621624+00:00
