# SET-I 連續修復

## 失敗
半途對各幀獨立 world 重抽 + img2img 加字 → 女主／槌／鏡頭漂移。

## 修復管線
1. PRE clean 定稿  
2. MID = img2img(**PRE**) 只推進 FIRST_CONTACT  
3. POST = img2img(**MID**) 只推進 REACTION  
4. 字 = **SVG 疊層**（底像素不變）

LOOP = `L-` + SHA12(MID clean)

workspace: `boundary_pedestrian_setI_obsidian/cont/`
