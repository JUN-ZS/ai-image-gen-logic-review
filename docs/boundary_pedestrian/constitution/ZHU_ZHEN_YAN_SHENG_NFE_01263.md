# §0.12.63 · 逐幀延生（NFE）

> LOCK 架構 · 母倉執行面：`JUN-ZS/UP-engine` · `src/ige/nfe/*` · `tools/nfe_*.py`

## A · 公式

\[
F_{t+1}=G(F_t,F_{t-1},K,\Delta S_t,C_t)
\]

| 符 | 義 |
|----|-----|
| G | **I2I next-still only**（一呼叫一靜圖） |
| K | 身份／母幀鎖 · 定期 re-anchor |
| ΔS | Motion Compiler 允許的本步動作 |
| C | Temporal State 歷史上下文 |

## B · 槽位（栓死）

| 槽 | 名 | 實作 |
|----|-----|------|
| C0 | Temporal State | `ige.nfe.state` |
| C0.1 | Motion Compiler | `ige.nfe.motion` |
| C0.2 | G | 外部 I2I · STICK prompt |
| C0.3 | Validator | `ige.nfe.validate` + 可選 `siax_next_frame_f2f_verify` / DDXX |
| C0.4 | Accept/Reject | `ige.nfe.loop` · 失敗不推進 t |
| STICK | 進化附卡 | `ige.nfe.stick` |
| C1–C5 | 組片 | `still_sequence_f2f_kit` · **只吃 accepted** |

## C · 錨點分裂

- **Static**：相機／地面／固定物 → DDXX 可鎖  
- **Dynamic**：頭肩肘腕／錘／披風／泥 → **追蹤**，禁止整身強對齊消運動  

## D · Provenance

每幀必標 `frame_origin`。  
`not_image_to_video_this_encode=true` **不足以** 宣稱血統無 I2V。

## E · 一鍵

```text
python tools/nfe_one_click.py --master F0.png --job-id JOB --out-dir runs/nfe/JOB
# 或 PowerShell: .\tools\nfe_one_click.ps1 -Master F0.png -JobId JOB -OutDir runs\nfe\JOB
```

產物：`state.json` · `STICK_EVOLVE.json` · `FRAMEWORK_MANIFEST.json` · `BOLT_CHECK.json`

## F · 里程碑

- **NFE-P0**：F0→F1→F2→F3 真 I2I + accept  
- **非目標**：5 關鍵幀 + 光流 = 360 next-frame；I2V 6s 當 F2F PASS  

## G · 品質

`quality_qualified=false` · `final_acceptance=false` · `cinematic_product=false` 直至正式閘。
