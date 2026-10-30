# OBA · DO_NOT_REPEAT
# asof 2026-10-30T18:30:45Z · §0.12.44

| 碼 | 禁 |
|----|-----|
| E-OBA-01 | 一次過全人 batch |
| **E-OBA-02** | **黃 GRID 格號當人 ID／定 scale**（毒大小規格） |
| E-OBA-03 | 母圖當貼底 |
| E-OBA-04 | HD cut upscale s>1 |
| E-OBA-05 | 無綠描邊／無邊對邊／只 box |
| E-OBA-06 | 綠線大包圍 fill（非 2px stroke） |
| E-OBA-07 | 重用紅線／OLD MASK |
| E-OBA-08 | VOID 比例未對母 |
| E-OBA-09 | 前後排唔跟 peep |
| E-OBA-10 | 有 HD 無掃瞄鏈 → ILLEGAL_OBA_DEMO |
| E-OBA-11 | peep 鄰人污染 |
| E-OBA-12 | 姿差大硬貼不重 GEN／無 shape-cond |
| E-OBA-13 | clean 層層降智（要裸 peep 解毒） |
| **E-OBA-14** | **格佔用入 scale** |
| E-OBA-15 | 只鎖腳無邊對邊 RATIO |
| E-OBA-16 | 線稿+OLD 混座標 |
| E-OBA-17 | MARK.h 當遠近（反透視） |
| E-OBA-18 | 軟 crop 帶地／背 |
| E-OBA-19 | 無 DETAIL 重 PROMPT |
| E-OBA-20 | VOID 隨便空板 |
| E-OBA-21 | peep RGB 用 diff／地紋 · 非母圖 |
| E-OBA-22 | rembg 小件崩 · 唔補 mother−VOID+Voronoi |
| E-OBA-23 | 混淆 peep-LOCK 與 ASC |
| **E-OBA-24** | **有位無形：最新母只 VOID+框 · HD 棚拍無同姿**（「最新圖沒用到」） |
| **E-OBA-25** | **無 REF 或 HD 非由 REF 生 · 自由棚拍**（脫離母原本動作） |
| **E-OBA-26** | **batch 生 HD 再一齊貼 · 非一次一件** |
| **E-OBA-27** | **無 STEP 線對看自審 · 只交 final／圖冊** |
| E-ASC-01..07 | 見 `OCCLU_COMPLETE_ASC_DO_NOT_REPEAT.md` · **E-ASC-07** 無 REF 同姿 ASC |

**黃線格號法：** `OBA_YELLOW_GRID_CELL_LAW.md` · §0.12.44.K  
**母形咬回：** `OBA_MOTHER_BITE_POSITION_WITHOUT_SHAPE.md` · §0.12.44.L  
**REF 原本動作／線對看：** `OBA_REF_ORIGINAL_POSE_LINE_ALIGN.md` · §0.12.44.**M**  
**LOCK 樣：** `OBA_SCAN_B132` · BATTLE6 · 母 b1326837 · **MIX** `OBA_MIX_ROBOT_SHIP/ONE_BY_ONE`  
**非法示範：** box+棚拍 HD · robots OBA_v1 · 舊 BATTLE6 粗貼 · batch HD 無 STEP
