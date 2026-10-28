# S1HL 一升 · OOM 失敗備註 · 下次先走別路

> asof 2026-10-29T04:10:00+08:00  
> 憲位：§0.12.15.L 一升混鎖 · 擴 E-GS-04 族  
> 樣板失敗鏈：SET-S ST1 · L0 `abe76dab…` · 2026-10-28/29 實跑  
> 正典成功：`S1HL_v3_strip` · VIEW/HD · T3 `be436496…`

## 一句（下次一升先讀）

> **一升前先選路：預設不開「全幅 4× float 三陣」；OOM 過就改 strip／降階／ROI，不要重試同死法。**

---

## 失敗實錄（必須備註）

| 版 | 做法 | 結果 | 根因 |
|----|------|------|------|
| **v1** | 全幅 SIAX 回傳 FULL ndarray + Hybrid 再持 LP/HF/Siax 三幅 float | **exit 137 OOM** | E-GS-04：全幅 float 常駐 RAM（非「格數」） |
| **v2** | siax memmap 成功 → 再開 **hyb.mm 第二個 6912×4608** 全幅寫 | **OSError I/O / 不穩** | 雙 memmap 全幅 + flush 峰值；仍近 OOM 族 |
| **v3 ★** | siax **僅** memmap；Hybrid **條帶**直出 VIEW(1/4) + HD(1/2)；**不**建 hyb.mm FULL | **PASS** | 從不駐 3×FULL float |

### 數字印象（本機 CPU spandrel）

- L0 1152×1728 → SIAX 4608×6912  
- tile **128** · band **96** · float32 · overlap 12  
- 單圖 SIAX ≈ **9–10 min** CPU  
- 成功產物：`ABE76_HYBRID_VIEW` · `ABE76_HYBRID_HD` · strip · T3 a8b

---

## 黑名單擴（E-GS-04 族 · 一升專用）

| ID | 禁 | 後果 | 校正 |
|----|-----|------|------|
| **E-GS-04** | 全圖 float64／多幅 4× 常駐 RAM | OOM 137 | tile-to-disk + strip · float32 band |
| **E-GS-04b** | Hybrid 再開全幅 float LP+HF+Siax | OOM／I/O | Hybrid **只** strip 混，直寫 VIEW/HD |
| **E-GS-04c** | 同時常駐 siax.mm + hyb.mm 雙 FULL 寫 | 峰值 RAM／I/O fail | **只** siax.mm；hyb 不落地 FULL mm |
| **E-GS-04d** | OOM 後 **原樣重跑** 更大 band／更大 tile | 再 137 | 見「一升選路表」降階 |
| **E-GS-04e** | OOM 後改 **二升** 或 pure Siax 當 FINAL 救 | 違 S1HL／E-GS-06/47 | 改路不改招義 |

---

## 一升選路表（下次先走 · 防 OOM）

**決策：開跑 S1HL 前選 PATH；OOM 只允許「換 PATH」，禁止「同 PATH 加碼」。**

| 優先 | PATH | 何時用 | 做什麼 | 禁 |
|------|------|--------|--------|-----|
| **P0 預設** | **STRIP_S1HL** | 全幅 IP／1152×1728 級 | tile SIAX→memmap；Hybrid strip→VIEW+HD；T3 Ref(a8b) | 三幅 float FULL；hyb.mm |
| **P1** | **ROI_S1HL** | 只要臉／甲／械清 | crop ROI → SIAX×1 → Hybrid → 拼回（勾形 α） | 全幅 4× 先開 |
| **P2** | **S2_BAND** | 內存緊／要快預覽 | **S=2** 非 4× 先出可審；再決定是否真 4× | 直接 S=4 全幅 |
| **P3** | **GRID_CELL** | 已有 GRID 好區 | 只升好格 + GRID_CLEAN 寫 donor | 全開 pure Siax FINAL |
| **P4** | **XHL 外折** | 本機一升不穩／待解 | 外 donor 包 → 內 Hybrid×M → a8b（§XHL 待解） | 本機假冒 SUPIR 當 SIAX |
| **P5 禁** | FULL_F64_×3 | — | — | **永禁** · E-GS-04 |

### 口令建議

```text
「一升」／「S1HL」        → 預設 PATH P0 STRIP_S1HL
「一升 ROI」               → P1
「一升先 2×」              → P2
「OOM 了換路」             → 禁止重試 v1/v2；跳 P1 或 P2
```

---

## 與總憲對齊

| 條 | 關係 |
|----|------|
| §0.12.15 E-GS-04 | 本備註 = 一升實戰擴寫 |
| §0.12.15.L S1HL | T1 必 tile；T2 必 Hybrid strip；T4 禁二升 |
| §0.12.5 每格 HD | P1／P3 可接 |
| XHL 外折混鎖 | P4 待解並列，非取代 TRUE SIAX 名 |

## 成功閘（v3）

- [ ] 無 exit 137  
- [ ] 有 Hybrid VIEW（非 pure Siax 當交付）  
- [ ] M 含 face/body/bg/ew  
- [ ] T3 a8b 後 **停**（無二升）  
- [ ] META 寫 PATH=P0|P1|…

*END S1HL_OOM_NOTES · 2026-10-29T04:10:00+08:00*
