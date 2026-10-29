# 技名：SIAX 探針匹配 · SPM

> short: **SPM** · SIAX Probe Match  
> 憲位：**§0.12.39**  
> asof: 2026-10-29  
> 用戶口令：「稀疏 SIAX 探針 + 模底互構」「等價旋鈕入憲」「方案 A 48×64 為一升／N2R／S1HL／GOU／MSR 預設 SIAX」

## 正名
**SIAX 探針匹配**（SIAX Probe Match）

## 一句
用 **極少真 SIAX tile（預設 48×64² 殘粗糙）** 抽 HF／residual 指紋，與 **Lanczos 模底** 做 MAP 互構；  
**不是** 截擴散半步（SIAX 無 STEP／NOISE／CFG 原生）。

## 預設
**SPM-A**：TILE 48 × 64² · residual_gain 1.15 · rough_boost 0.85 · fill_sigmas [4,8,16]

## 與連動
N2R · S1HL Hybrid · GOU · MSR · ZYF 衣板  
全文：`SIAX_PROBE_MATCH_SPM_01239.md`
