
# §0.12.23 VIRUS_LOCAL_BASE — 局部母底病毒（永久禁用）

> asof 2026-10-27T08:01:29Z · 用戶診斷確認 · L-9168908bc3b9 後寫入

## 根因（不是「拼貼 α  alone」）

曾用**單一局部圖**當放大母底（例：`b47031a9` 胸甲 crop 1440×1376、無頭無全構圖；
以及 `28abef` 路徑把局部升成「全圖」），導致：

1. **底圖邏輯被限死在 PART 座標系**（只有上半身裁切的光、比例、邊緣）
2. 之後所有 ECC / mask / α / GEN 都以這 PART 為「真」→ 拼回全圖時
   - 姿勢／光／邊緣對不齊全幅
   - 失敗區被放大成全圖級病毒
3. 局部 GEN 板（`80aecc41` 等）再 full-RGB 貼上 → **CHEAT_B** 與病毒疊加

**病毒定義**：任何「以非全幅 native 海報為 BASE」的混放大／拼回流程。

## 永久禁用

| 代號 | 行為 | 狀態 |
|------|------|------|
| **VIRUS_LOCAL_BASE** | 用單一局部 crop 當母底再升／再拼全圖 | **KILL** |
| CHEAT_A | V1 結構鎖假進度 | KILL |
| CHEAT_B | full-RGB GEN paste α≈0.9 | KILL |
| CHEAT_C | 軟 HF 替換母圖硬 HF | KILL |
| TOXIC_PLATE | 金改版肩板 `80aecc41` 當全色源 | KILL |

## 合法角色（只允許）

| 角色 | 必須是什麼 | 不可是什麼 |
|------|------------|------------|
| **BASE（母底）** | 全幅 native 海報（如 `947cf5b2` 4608×6912） | 局部 crop、已拼假底、1152 縮圖 |
| **GEN donor** | 從 **BASE 裁出** 的 crop → i2i 密網 | 無關單圖、他圖局部、病毒底再裁 |
| **plate** | 只提供中頻網紋（V5 MF Δ） | 不提供 LF 色／姿勢／全 RGB |

## 強制流程

```
BASE = full native poster only          # 唯一母底
crop_i = BASE[box_i]                    # 從母底裁，不是外來單圖
gen_i  = i2i(crop_i)                    # donor only
plate  = V5(BASE, gen_i)                # base + α*(gen_MF-base_MF) + β*base_HF
never:  BASE ← local_only_image
never:  upscale(local) → pretend_full
```

## 自檢

- [ ] BASE.asset 是全幅且含頭／石／字／球
- [ ] 所有 GEN crop 的 box 來自該 BASE 座標
- [ ] 無「先升局部再當全圖」中間檔進母鏈
- [ ] gold_frac / lap / MAD 門檻過 V5

## 毒株示例（勿再當 BASE）

- `b47031a9-99ed-4b91-b94a-c730e9e8b555` — 胸甲局部 1440×1376
- 任何 headless torso-only / 單臂 / 單甲 crop 當「全圖升」起點

> **全鏈流程：** 病毒→WHOLE→勾勾 → `GOU_MESH_CORRECT_PROCESS.md` T0–T12 · `GOU_MESH_DO_NOT_REPEAT.md` · §0.12.25.J（2026-10-27T14:38:15Z）
