# 人物 SCAN-CROP / 描邊裁切 → 貼回完成圖（消 img2img 疊影）

> 問題：人物在 **反覆 img2img / multi-REF** 後出現**疊影、重影、ghost**。  
> 解法：用**首次 clean 生成**的人物做 extract（scan crop），再 **alpha 貼**到完成圖（HUD／字層）上。

---

## 1. 管線

```text
1. PRE clean   = 首次定稿人物（女主鎖 + 世界）
2. MID/POST    = 只以上一 clean 推進時間（幀連）
3. 完成層      = only-add HUD / 字（可令人物微漂、疊影）
4. SCAN CROP   = imagine_extract_subject( clean_frame ) → RGBA cutout
5. PASTE       = alpha_composite( 完成層, soft_edge(cutout) )
6. 輸出        = 完成圖場景 + 首次人物清晰輪廓
```

### 為何有效

| 層 | 來源 | 保留 |
|----|------|------|
| 場景／VFX／HUD／字 | 完成圖 | 箭咀、HOT、3D 字、碎裂 |
| 人物（+當幀槌姿） | **clean 首幀 extract** | 無疊影臉／衣 |

Cutout 與完成圖 **同分辨率、同構圖對齊**（extract 全幅透明底）→ 貼 (0,0) 即可。

---

## 2. 技術細節

- 工具：`imagine_extract_subject`（subject 指「the woman with the hammer」）  
- 邊緣：`MinFilter` 收邊 + `GaussianBlur(1–3)` 羽化，減少白邊  
- 同幀對貼：PRE cut→PRE HUD，MID cut→MID HUD（**唔好**用 PRE 人貼 POST 姿）  
- 槌／球：若 extract 連武器一齊出，貼上會蓋住部分接觸 HUD——可接受；要保留接觸標可改「只裁身體」或分兩層

---

## 3. 與既有層關係

```text
L0 clean 鏈
L1 HUD / DEPTH type（完成層）
L2 SCAN-CROP paste（人物救回）  ← 本檔
（可選）L3 SVG 準字 sidecar
```

**禁止**：paste 之後再整圖 img2img（會再次疊影）。

---

## 4. SET-J 示範

- cutouts：`boundary_pedestrian_setJ_porcelain/cutouts/`  
- pasted：`…/pasted/J01_*_PASTE.jpg`  
- 對照：上 HUD 原圖 / 下 paste 救回

---

## 5. 一鍵口令（給下一 AI）

```text
若完成圖人物有 ghost：
1) extract subject from matching CLEAN frame
2) soft-edge alpha paste onto finished frame
3) do not re-img2img after paste
```

> 字層同理：見 **TYPE_SCAN_CROP_PASTE.md**（字從首字圖描出，貼在人上）。
