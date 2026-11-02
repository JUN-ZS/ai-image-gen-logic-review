# 真女主轉皮 · 過程規格 · ZHEN_NV_ZHU_ZHUAN_PI_ZNZZP_01262C

## 0. 地位

**face俱圓 FJY_01262 子招** · **S3.6**  
補全漏步：此前 HPP／JLP 可無女主；本招**強制**用女主真臉當 **皮材 + 身分 donor**。

證據目錄：`tmp/fjy_true_skin_f670/` · `RESULT_TRUE_SKIN.json`  
主推 plate 例：`5c714e21`（ECC≈0.982 · pose@6f05 + f670）

## 0.1 為何獨立成招

| 舊做法 | 問題 |
|--------|------|
| HPP i2i「少塑料」 | 無特定女主皮 |
| soft identity blend | 皮不像 donor |
| dens@97 跨母圖硬貼 | 姿錯 · ECC 崩 |

**真女主轉皮** = pose 鎖 plate + **女主清臉真皮** 強轉。

## 1. 輸入

| 輸入 | 要求 |
|------|------|
| **pose_plate** | 本場 dens／JLP／HPP 全臉 · ar 跟 dens · 同姿 |
| **heroine_face** | TRUE_A8B `identity_ref`（默認 f670 級清臉特寫） |
| **母圖 FACE_BOX** | 全臉俱圓 |

## 2. 生成契約（Imagine ref）

```
asset_ids = [pose_plate, heroine_face]   # 順序：幾何先，女主後
aspect    = auto 或 omit（跟 dens，禁 2:3 硬鎖）

prompt 必須包含：
- 第一張：crop / ar / 頭角 / 濕髮 / 甲 鎖死，不 reframe
- 第二張：女主真臉 → 身分 + 真皮材質（pores / 頰光 / 次表面）
- 雨水泥點可留在「她的真皮」上
- full face in frame
```

## 3. 驗收

```
ar_match: |ar - dens_ar| 合理（無海報比硬扭）
ECC ≥ 0.85 vs 母圖 ROI
gate FAIL → 不貼，或降 soft hybrid 並標 not_znzzp
```

## 4. face俱圓 全鏈（更新）

```
S1   全臉 ROI
S2   dens 本場同姿（TRUE_A8B 作配方，不跨姿硬 dens）
S3   plate auto 跟 dens
S3.4 近臉皮真 JLP     （近圖 A 程序 · 可選）
S3.5 畫皮皮 HPP       （生成級皮 · 可選）
S3.6 真女主轉皮 ZNZZP  ← 本技（女主 donor 真皮 · 近臉建議開）
S3.7 原臉光鎖 YLGS     （原臉 IC／陰影）
S4   SHOW 自由長邊
S5   ECC ≥ 0.85
S6   feather 貼母圖
S7   收據
```

## 5. 收據

```json
{
  "znzzp": {
    "enabled": true,
    "heroine_skin_donor": "<asset_id>",
    "pose_plate": "<asset_id>",
    "true_skin_plate": "<asset_id>",
    "ar": 0.806,
    "ecc_after": 0.982,
    "gate_raw_085": true,
    "not_soft_id_only": true
  }
}
```

## 6. 與 TRUE_A8B

沿用 `RESULT_TRUE_A8B.json`：

- `identity_ref` → 本招 **heroine_skin_donor**
- `dens_donor` 角色 = **本場** dens，不是跨母圖硬貼
- `setS_hard_swap: false`
