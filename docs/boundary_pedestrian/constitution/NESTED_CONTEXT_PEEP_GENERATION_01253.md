# §0.12.53 NESTED_CONTEXT_PEEP_GENERATION（LOCK · 2026-10-31）

> 用戶正名：**嵌套脈絡 PEEP 生成** · 短碼 **NCPG**  
> 架構跳躍：主引擎 = **框選→脈絡→放大→生成新像素→原座標混回→再 Zoom**  
> **非** 單靠 skeleton 18k 短 path 主導全部微細節

## 一句
**每一層 PEEP 同時保留：全局脈絡 · 父層高清 · 局部 Generation Mask · 原始母圖座標；只納新高清進主畫布，禁止縮回低解析度後宣稱保留高清。**

## 四層

| 層 | 名 | 義 |
|----|-----|-----|
| P0 | GLOBAL | 完整人物場景 · 姿／臉／光／衣位 鎖定 |
| P1 | GARMENT | 衣區框 + **Context Ring**（腰腿光影可見）· ×2 生成新衣料像素 |
| P2 | SUBREGION | 裙／胸／袖 未清區再裁 · 帶 P1 結果+母+donor |
| P3 | MICRO | 金絲／開網／纖維 · Zoom 再生成 · L2/L3G 只 **約束** |
| ZOOM OUT | Virtual Master | 4K/8K 主畫布 · 讀低層預覽 **≠ 刪高清像素** |

## 兩 Mask 必須分離
| Mask | 義 |
|------|-----|
| **Generation Mask** | 模型可創造新像素的範圍 |
| **Context Ring** | 模型可見／理解 · **禁止任意重畫** 的周邊 |

## 每子 PEEP 三參考（禁只跟生成父層）
| 參考 | 功能 |
|------|------|
| Original Parent | 位置／形／光影 |
| Generated Parent | 上一層高清 |
| Material Reference | L2／L3G 材質方向 |

**禁：** 只把上一層生成圖放大再畫 → 逐層偏差放大。

## L3T／L3G 新地位（降權為約束）
| 技 | 角色 |
|----|------|
| L3T Skeleton UV | 紋理方向／donor 映射 **參考** |
| L3G A+B | 微纖形態／材料 **限制** |
| **NCPG Contextual PEEP** | **主生成引擎** |
| Crop&Stitch / Tile Refine / Dazzle | 裁切脈絡／大圖連續（可嵌） |

## 主交付
- **Virtual PEEP Master**（高清子板 + 4K/8K Base）
- 禁：唯一交付 = 縮回 1792 FULL 並宣稱 HF 保留（E-NCPG-01）

## 勿再犯
| 碼 | 禁 |
|----|-----|
| E-NCPG-01 | 縮回低 res 殺 HF 後稱成功 |
| E-NCPG-02 | Generation Mask = Context（無脈絡）|
| E-NCPG-03 | 只跟 Generated Parent · 丟 Original+Material |
| E-NCPG-04 | skeleton 短 path 主導全部細節 · 取代模型理解衣 |
| E-NCPG-05 | 覆蓋 L2／原 FULL 無備份 |

## 程式對照（研究 · 非已驗收）
- ComfyUI Crop and Stitch · Context-Anchored Tile Refine · DazzleNodes · TiledUpscale sequential context

---
## 0.12.53.R2 Native peep + 母拓撲不漂（2026-10-31 LOCK）

### 鐵序
1. **Native board** = peep crop ×2 固定像素（禁模型改畫幅當主座標）
2. 切 **固定 tile**（如 768）· 每格 = Original Parent 像素
3. Imagine densify 後：**ECC 對齊** → 量 topo NCC
4. **HF residual only** · LP = Original Parent
5. **Parent-wire ridge gate**：HF × 母 wire 脊 · 禁自由重網
6. Gen Mask 內注入 · Context Ring 強制母像素
7. 閘：`topo_out ≥ 0.90` 才 ACCEPT；全板 `topo_ncc ≥ 0.90`
8. 主交付 = **Native plate + Master 4K** · 1792 只 preview

### 禁
| 碼 | |
|----|--|
| E-NCPG-06 | 以 Imagine 輸出分辨率當 peep 主座標 |
| E-NCPG-07 | gen 重網後不對齊、不 ridge gate 直接貼 |
| E-NCPG-08 | 堆 skeleton path 當本刀主引擎 |

### 樣板
`SETS/PROJ_A8B_MID_DHY_V1/ARCH_V2_NESTED_CONTEXT_PEEP/R2_NATIVE_TOPO/`  
ACCEPT：board topo **0.973** · 400% Tenen 29k→44k

---
## 0.12.53.R3 審計修正（2026-10-31 LOCK）

### 驗收狀態定義
| 狀態 | 義 |
|------|-----|
| `PEEP2_INPUTS_PREPARED` | 只有 tile/parent/mask/manifest · **≠完成** |
| `PEEP2_GENERATED_AND_STITCHED` | gen→ECC→雙閘→residual fuse→register 全鏈有輸出 |

### 鐵律修
1. **ECC 必須** `findTransformECC` + warp 日誌；禁裸 resize 當對齊
2. **letterbox 保比例** · 禁 stretch-to-square 作主座標
3. **硬 ridge gate**：ridge 外 HF=0；**禁 beta=0.12 偷渡 REJECT**
4. **雙閘**：全局 topo≥0.90 否則 REJECT；像素 ridge 清越界 HF
5. **融合** \(I = I_{parent} + \sum w\Delta / \sum w\) · 順序無關
6. **Master 主檔 lossless PNG**；JPG 只 preview
7. LOG key 必須對齊 ACCEPT 欄位名

### R3 樣板結果（誠實）
- 4 格 gen 硬閘後 **n_accept=0 n_reject=4**（topo 0.69–0.85 < 0.90）
- board ≡ R2 parent · topo_vs_parent **0.973** · spill **0**
- **不宣稱 PEEP2 densify 成功**；宣稱：硬閘可追蹤 · R2 安全保留

---
## 0.12.53.R4 Coordinate-Preserved High-Resolution Stitch（LOCK 2026-10-31）

### 核心診斷（寫死）
1. **尺度不一致**：PEEP2 已是 4×，Master 仍 2× → 貼回縮採樣殺 HF
2. **ECC 不足**：裙子非剛性 → 需 Dense Warp（Farneback 等）
3. **融合錯誤**：禁整張 RGB 貼紙 → \(M_{HR}=P_{HR}+\alpha G_{mask} R_{HF}\)

### Virtual Master
- FULL 1792×1008 → **VM 7168×4032（4×）**
- PEEP2 child **原生 1024** 寫入 VM 座標 · **禁** 1024→512 再當主交付
- Transform Manifest 記 crop / pad / g / letterbox / vm_rect

### 閘拆分
| 閘 | 用途 |
|----|------|
| structural_ncc（LP 下採樣） | 硬拒 <0.90 · 結構不漂 |
| hf_ncc | 診斷 only · 新細節可降 |
| hard ridge + garment mask | 禁 spill |

### R4b 樣板
- n_accept **4/4** · struct garment **0.9998**
- ten_400 **16530 → 24634** · PASS_densify
- 主檔：`VIRTUAL_MASTER_4X_R4b_LOSSLESS.png` · garment plate 4× PNG
