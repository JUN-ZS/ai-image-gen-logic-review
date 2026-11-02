# 單白殺升 · DO_NOT_REPEAT · DBSS_01261

## 禁止再犯

1. **先高清再殺白當本技預設**  
   在 NCNN／Imagine dens 完成後才 WNK，再貼回 —— 那是另一條實驗，**不是** 單白殺升。  
   本技：**NON-HD peep 上殺白** → 再 PATH1E。

2. **半臉 peep 硬貼**  
   只含五官、裁掉額／下巴／髮際 → ECC 易 FAIL、貼回露縫。全臉額→下巴齊。

3. **降 PIXEL 貼回**  
   為對位縮小母圖或輸出小於輸入母圖 WH。

4. **把 Lanczos／Imagine light 標成品質 PASS**  
   輕量回扣 ≠ NCNN PBI 驗收 ≠ Siax final_acceptance。

5. **Imagine light 重構構圖**  
   換臉、重擺錘、改鏡頭 —— 違輕量鎖構圖。

6. **與「正方高清殺白再貼」混收據**  
   正方 HD WNK 是分支實驗；DBSS 收據必須 `hd_face_wnk: false`。

7. **gate 與 paste_fail 混用**  
   raw ECC＜0.85 仍可 soft 貼，但不得寫成 strict quality PASS。

## 應做

- 固定順序 S1→S6  
- 全臉 ROI  
- 母圖 WH 鎖  
- 收據分欄：wnk_nonhd / path1e / lanczos / imagine_light  
