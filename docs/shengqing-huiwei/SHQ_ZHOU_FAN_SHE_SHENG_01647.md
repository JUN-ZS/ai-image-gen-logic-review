# 宪技 · 轴.反射.生（01647）

## 全名
**轴向生（同形态轴向）· HD 反射重建** = **`轴.反射.生`**

## 至高
```
[(生,除,洞,扣)×(反)] ← 外力GROK
```
本技落在 **生（正）**：洞座已冻后，用同形态轴向外力重建 HD 反射／材质，再入座。

## 方程
```
轴.反射.生 =
  绿语义座（同机位·同姿·同尺·同座）
  ⊕  VDIR全相 BACKUP（只作反射/材质身份）
  →  每件 HD 高光 / 折射 / caustic / 台面反射 重建
  →  supply ⊙ MARK  hardpaste
  →  outside = 0
```

## 与旧名对照
| 口语 | 宪 call |
|------|---------|
| 轴向生（同形态轴向）· HD 反射重建 | **轴.反射.生** |
| 01645 轴向生主路 | 同族 · 材质场景 |
| 01646 埋叠杯反射重建 | 同族 · **本技证明跑** |

## 必用 / 禁用
**LIVE**
- 外力 neon 绿语义座 + chroma 洞
- `imagine_reference_to_image(绿座, 全相BACKUP)`
- 全相 = BACKUP only
- 步步為一 后→前（叠反射）

**DEAD**
- 差分 \|L0−L_rm\| + CC 造洞
- 全相当主贴（白晕）
- freeframe 换原冒正生

## 闸
- 非框 · green_residual<0.05 · outside=0
- claim: `C2_ZHOU_FAN_SHE_SHENG`

## 证明
- 01645 柠檬碗肉桂
- 01646 埋叠玻璃杯 `C2_GLASS_STACK_REFLECT_01646`

ACCEPT_FULL_HD = false


```json
{
  "write_id": "01647",
  "call": "轴.反射.生",
  "zh": "轴.反射.生",
  "full_name": "轴向生（同形态轴向）· HD 反射重建",
  "formal": "SHQ_ZHOU_FAN_SHE_SHENG_V1",
  "stick": "STICK_ZHOU_FAN_SHE_SHENG",
  "asof": "2026-11-12T00:52:35.177381+00:00",
  "至高无上": "[(生,除,洞,扣)×(反)] ← 外力GROK",
  "algebra_cell": "生（正）· 外力驱动 · 座锁",
  "equation": "轴.反射.生 = 绿语义座同形态轴向 ⊕ VDIR全相BACKUP(反射/材质身份) → 每件 HD 高光/折射/水纹 重建 → 只在 MARK 洞座 hardpaste",
  "derived_from": [
    "01645 轴向生·全相BACKUP",
    "01646 埋叠杯·反射重建",
    "01644 外力neon绿语义座+chroma"
  ],
  "inputs": {
    "座": "外力 neon 绿语义座（同机位）",
    "洞": "chroma(绿) → MARK；禁差分CC",
    "BACKUP": "VIRTUAL_DIR 全相 = 反射/材质身份 only，不主贴",
    "工具": "imagine_reference_to_image [绿座, 全相BACKUP]"
  },
  "outputs": {
    "主生": "VIRTUAL_DIR/轴向生_反射/{物}_AXIAL_HD.jpg 或 elev 洞内 supply",
    "锁回": "RETURN = base⊙(1−M) + supply⊙M；outside=0"
  },
  "gates": {
    "ok_非框": "MARK 非矩形毒",
    "ok_green_residual": "<0.05",
    "ok_axial_not_white": "white_frac 主路低（全相不主贴）",
    "outside": 0,
    "claim": "C2_ZHOU_FAN_SHE_SHENG"
  },
  "DEAD": [
    "E-SCAN-DIFF-CC-01",
    "全相作主补给",
    "freeframe换原冒正生",
    "全相主贴白晕路径"
  ],
  "LIVE": [
    "轴.反射.生",
    "轴向生≡绿座形态",
    "全相BACKUP only",
    "绿座洞+chroma",
    "步步為一 后→前 叠反射"
  ],
  "proof_runs": {
    "01645": "柠檬碗肉桂 · 轴向主 / 全相备 · PASS",
    "01646": "埋叠玻璃杯 4件 · 反射重建 · PASS C2_GLASS_STACK_REFLECT_01646"
  },
  "ACCEPT_FULL_HD": false,
  "note_residual": "透光物姿态锁仍可能微漂；下一刀可加姿态IoU闸"
}
```
