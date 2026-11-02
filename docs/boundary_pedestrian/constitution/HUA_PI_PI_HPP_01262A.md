# 畫皮皮 · 過程規格 · HUA_PI_PI_HPP_01262A

## 0. 地位

**face俱圓（FJY_01262）子招** · **S3.5**（**S3.4 近臉皮真 JLP** 之後）。

近臉何時開 A／B：見 `JIN_LIAN_PI_ZHEN_JLP_01262B`；本技是 **B 生成級主路**。

| 做 | 不做 |
|----|------|
| dens 正確 ar 上生成級皮膚 | 錯 2:3 皮硬貼 |
| i2i 鎖 crop／姿／甲 | 換臉身分為目的（那是身分 ref 另步） |
| 近臉毛孔／次表面／去塑料 | 網紅磨皮、降 PIXEL |
| 畫完重跑 ECC | 不測 gate 直接貼 |

## 1. 輸入

- **geom plate**：dens 或 FJY auto plate（ar ≈ dens_ar，全臉）
- **可選 skin_ref**：如舊 2:3 好皮（`@4713` 類）——**只借皮質，不借框**
- **禁止**：以 skin_ref 的 2:3 尺寸／構圖為 primary

## 2. 主路 · Imagine i2i（生成級）

```
prompt 必須鎖：exact same crop, aspect, pose, wet hair, armor, rain
只改：photoreal skin, pores, subsurface, less plastic, natural oil/rain on skin
out = Imagine_image_to_image(geom)   # 省略 aspect 以保持輸入 ar
assert out.wh 近 geom 且 |out.ar - dens.ar| 小
```

實測例（2026-11-03）：

| 板 | ar | ECC | 皮 |
|----|-----|-----|-----|
| 舊 2:3 好皮 | 0.67 | 0.67 FAIL | 生成級但框錯 |
| dens i2i 畫皮皮 | **0.913** | **0.978 PASS** | 生成級 + 框對 |
| dens+ref auto | 0.913 | 0.73 | 皮好姿微漂 |

**主交付模式**：`i2i(dens)`，不是 `硬貼(2:3皮)`。

## 3. 輔路 · 程序皮真實

```
bilateral de-plastic → HF residual → midtone grain → mild mid desat → Y light unsharp
WH/ar 不變；可控、可複現；標 backend=procedural
```

近臉優先；遠景小臉可 skip。

## 4. 可選 · ref 只借皮

```
Imagine_reference(primary=dens, skin_ref=good_skin_plate, aspect=auto)
# 若 ECC < 0.85 → 棄，改回純 i2i(dens)
```

## 5. 接回 face俱圓

```
S1 全臉 ROI
S2 dens 幾何
S3 FJY plate (auto 跟 dens，可選身分)
S3.4 近臉皮真 JLP   （近圖 A）
S3.5 畫皮皮 HPP     ← 本技（B）
S3.6 真女主轉皮 ZNZZP （女主 donor 真皮）
S4 SHOW 自由長邊
S5 ECC ≥ 0.85
S6 feather 貼母圖 WH 鎖
S7 收據
```

## 6. 收據欄

```json
{
  "hpp": {
    "enabled": true,
    "backend": "imagine_i2i",
    "geom_ar": 0.914,
    "skin_ar": 0.913,
    "aspect_forced_wrong": false,
    "skin_ref_used": false,
    "ecc_after_hpp": 0.978,
    "gate_raw_085": true
  }
}
```

## 7. 證據

- i2i 主板：`b55a53be-06d7-4851-ae92-4aea5c54ef6e`
- 舊錯比皮：`47134783-6ee8-4182-9db1-ce2526ecabfe`
- dens：`97cfa7e1-2ddd-497b-9ae4-981b848188a3`
- 貼母：`tmp/fjy_ratio_skin_gen/`
