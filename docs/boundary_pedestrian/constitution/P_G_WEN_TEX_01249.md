# P_G紋 · peep×GRID 對位升高清貼紋
# §0.12.49 · asof 2026-10-30T20:07:01Z

> **命名（用戶）：P_G紋**  
> **P** = peep 綠描量尺／ROI　**G** = 黃 GRID 座標鎖　**紋** = 高清材質／decal 貼合  
> 樣板：`22cf97df` 杖女 · `SETS/OBA_UPSCALE_STAFF_GIRL/`

---

## 0. 一句

用 **一人累貼 OBA 的對位骨架**（綠 peep + 黃 GRID）鎖定姿／位／尺，  
再以 **HD 材質 sheet（紋 donor）** 對 peep ROI 做高清貼紋升圖——  
**格號＝座標 ≠ 人／≠ 紋 ID**；**s 跟 peep · 永不跟格邊長**。

---

## 1. 符號

| 符 | 義 |
|----|-----|
| **P** | peep：綠描邊 · 主體／局部 ROI · 量尺 s 來源 |
| **G** | GRID：黃線格 · 母↔目標同線聯動 · 格號 coords only |
| **紋** | HD 材質 catalog／decal sheet · 緞、金嵌、鉻、石、布… |

**全名：** peep×GRID 紋升  
**短碼：** `P_G紋` · `PG-TEX` · `OBA-TEX-LIFT`

---

## 2. 鐵序

```
① 母圖
② P：綠 peep（全形 or 分段 ROI：臉／胸甲／杖／靴…）
③ G：黃 GRID 聯動（母＝目標同 v/h 線 · 格號只座標）
④ 紋：NORMAL 法出 HD 材質 sheet（與 peep 材質對應）
⑤ 合：姿鎖主圖（第一 ref）+ 紋 sheet（第二 ref）
     或 peep-mask 內 composite decal
⑥ s = peep 尺 ≤1 · 錨＝心／腳／ROI 中心（禁 grid scale）
⑦ 自審：peep+GRID 板 · ROI 原｜升 zoom · 全圖對照條
```

---

## 3. 與姐妹技

| 技 | 關係 |
|----|------|
| **一人累貼 OBA** §0.12.44 | **對位主幹**（P+G 同源） |
| **影分身合** | 可先 IP 再 P_G紋 升 |
| **虛形互搏** §0.12.48 | 多體時只實己 peep 貼紋 · 他機虛線不搶 mask |
| **殘相轉生** | 被擋區先補全 · 再 P_G紋 |

```
OBA 累貼整機／多人
  └─ P_G紋 = 同一對位 · 貼的是「高清紋」不是「整機 cut」
```

---

## 4. 適用

| 場景 | 適 |
|------|----|
| 甲面金線／網紋／迷彩 decal | ✓ |
| 布料緞面、皮革 grain | ✓ |
| 金屬／鉻靴／法杖石 macro | ✓ |
| 臉膚細節升（peep 臉 ROI） | ✓ |
| 全身無縫 UV wrap | △（需分段 P） |
| 純 2×/4× 超分檔 | ✗（本技＝姿鎖材質升 · 非 ESRGAN 檔） |

---

## 5. 毒碼

| 碼 | 禁 |
|----|-----|
| **E-PG-01** | 格號當紋 ID／當 peep scale（E-OBA-02 同源） |
| **E-PG-02** | s 跟格邊長 · 紋被格放大 |
| **E-PG-03** | 無 peep mask · 紋 spill 出主體 |
| **E-PG-04** | 母／目標 GRID 不聯動 · 紋漂 |
| **E-PG-05** | 無姿鎖只自由 GEN · 人／姿跑掉 |
| **E-PG-06** | 把 P_G紋 說成物理超分檔（命名詐） |

---

## 6. 參數卡

```
技=P_G紋 §0.12.49
P=綠peep ROI · s≤1 · 錨心/腳
G=黃GRID coords_only · 母↔目標同線
紋=HD material sheet · peep對應材
合=姿鎖 ref0 + 紋 ref1 · mask內
BAN=grid_scale, no_peep_spill, free_pose_gen, fake_supersample
樣=OBA_UPSCALE_STAFF_GIRL · 22cf97df
```

---

## 7. 樣板證據

| 件 | 位 |
|----|-----|
| 源 | `22cf97df-68ba-4e4b-983c-b4559b7d2f11` |
| peep+G | `peep/01_PEEP_GRID.jpg` |
| 紋 sheet | `COMPLETE/HD_MAT_SHEET.jpg` |
| 升圖 | `COMPLETE/PASS2_OBA_TEX_LIFT.jpg` |
| 對照 | `COMPLETE/COMPARE_STRIP.jpg` · `ROI_ZOOM_COMPARE.jpg` |

*END P_G紋*

## 聯動：殘相轉生 × P_G紋
不順／斷紋 ROI → RRT 2全形 → 1A 回姿 → P_G紋 貼。樣：OBA_FIX_PG_RRT_DRESS · 2026-10-30T20:13:31Z

## 四技聯動（對紋）
影分身合+虛形互搏+殘相轉生+P_G紋 · 缺影分身/虛形則改不到新對紋 · 樣 OBA_DRESS_FULLCHAIN · 2026-10-30T20:20:40Z
