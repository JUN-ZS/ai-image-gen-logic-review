# §0.12.59 全圖 NCNN＋PBI 省記憶體（NFP-M · LOCK 方法備註）

> **用戶：** 下次預設改為「先寫 RAW，再分段 PBI」· 並入憲技 NCNN 方法參考  
> **觸發事故：** warrior 全圖 SR 完成後整幅 PBI 仍在 RAM → **OOM kill exit 137**（7168×4032 雙 float 畫布）  
> **地位：** 方法備註 + 鐵序 · 不取代 peep 版 `run_r6c_ncnn.py`

---

## 0.12.59.A 一句

> **NCNN tile 升清 → 立刻 `*_RAW.png` 落盤 → 從磁碟讀 RAW → BASE 水平 strip 做 PBI → `*_PBI.png`**  
> 預設 **禁止** all-in-RAM 整幅 PBI。

---

## 0.12.59.B 鐵序（預設 · 不可反序當預設）

```
INPUT (BASE)
  → ① NCNN GENERAL_x4v3 · tile（預設 64）+ pad · feather 拼
  → ② 合成 uint8 後 **立刻寫 RAW** · del float canvas / gc
  → ③ 自磁碟 imread RAW
  → ④ 按 BASE 高 strip（預設 256px）:
        LP = Lanczos4×4(strip)
        dY = ridge(Y_SR − Y_LP)
        hyb = C(LP) × (Y_LP + gain·dY)     # PBI luma_only
  → ⑤ 寫 PBI · 可選 preview/half JPEG
  → ⑥ RESULT.json · quality_qualified=false · not_siax=true
```

### CLI（定版入口）

```bash
python work/scripts/r6c_pbi/run_ncnn_fullframe_pbi.py \
  --input  <BASE.jpg> \
  --out-dir <out> \
  --param  general_x4v3_ts.ncnn.param \
  --bin    general_x4v3_ts.ncnn.bin
# 預設 --pbi-mode luma_only
# --unsafe-all-in-ram → 必須拒絕（腳本已 refuse）
```

---

## 0.12.59.C 引擎與權重

| 項 | 值 |
|----|-----|
| 引擎標籤 | `NCNN_GENERAL_x4v3` |
| 權重來源 | `realesr-general-x4v3.pth`（官方 Real-ESRGAN） |
| 轉換 | pnnx · Input `in0` · Output `out0` · trace 例 1×3×64×64 |
| 執行 | pyncnn · **預設 Vulkan=false**（缺 lib 時 CPU） |
| 非本節 | NMKD-Siax Torch · Comfy UNET · Grok Imagine 當 SR |

**clean-checkout 無 `param/bin` 不能重跑** · 須自備權重；此為 limits 必寫。

---

## 0.12.59.D 樣板 · warrior 全圖（2026-11-02）

| 項 | 值 |
|----|-----|
| 輸入 | 1792×1008 mud-hammer（Imagine asset 參考） |
| 輸出 | **7168×4032** |
| tiles | 777 · tile 64 / pad 8 |
| infer | ~32 s CPU pyncnn（環境相依 · 非 E3 claim） |
| wall | ~46 s 含 strip PBI |
| 政策 stamp | `default_pipeline=write_raw_then_strip_pbi` · `memsafe_default=true` |

**不是** 品質 PASS · **不是** 與 Siax cell 等價驗收。

---

## 0.12.59.E 與 peep 鏈分界

| | R6c peep `run_r6c_ncnn.py` | 本節全圖 NFP-M |
|--|---------------------------|----------------|
| 輸入 | peep 子板／probe | **整幅 BASE** |
| 記憶 | peep 級 | **必須 RAW-first** |
| 閘 | G7/G8/S1S2 可選 | 本節最小交付不強制 G7；可後掛 |
| 交付 | `*_NCNN_PBI_R6c.png` child | `*_RAW.png` + `*_PBI.png` |

---

## 0.12.59.F 驗收欄位（JSON）

必含：

- `default_pipeline: write_raw_then_strip_pbi`
- `memsafe_default: true`
- `not_siax: true`
- `pbi_mode: luma_only | raw_only`
- `quality_qualified: false`（除非另開品質閘且 THIS_RUN 圖同 commit）
- `limits[]` 含 OOM 禁令與權重路徑

---

## 0.12.59.G 入庫位置

- 憲：`docs/boundary_pedestrian/constitution/NCNN_FULLFRAME_PBI_MEMSAFE_*.md`
- 腳本：`work/scripts/r6c_pbi/run_ncnn_fullframe_pbi.py`
- UP-engine 鏡像（若並存）：`tools/ncnn_fullframe_pbi.py` · `docs/NCNN_FULLFRAME_PBI_DEFAULT_MEMSAFE.md`
