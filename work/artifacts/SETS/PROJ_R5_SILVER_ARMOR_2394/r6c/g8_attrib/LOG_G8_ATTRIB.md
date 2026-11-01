# G8 四源歸因 · ATTRIB

- asof: 2026-11-01T10:30:06.792514+00:00
- global_winner_mode: **S1_strong_neg_residual**
- G8 仍 FAIL · 不降閘 · merge main NO

## 源定義
- **S1** 孔內負向 Y residual 過強
- **S2** 新黑落在 LP ridge/wire（絲被咬黑）
- **S3** Lanczos LP 本身已近黑（脆弱帶）
- **S4** C(LP)×Y 色度鎖導致亮度合成偏差

## P0 · winner **S1_strong_neg_residual**
```
{
  "S1_strong_neg_residual": 21910,
  "S2_ridge_wire_hit": 6920,
  "S3_LP_already_dark": 6511,
  "S4_chroma_compose": 0,
  "S5_other": 0,
  "new_black_B_total": 35341,
  "new_black_A_full": 39133
}
fracs: {"S1_strong_neg_residual": 0.62, "S2_ridge_wire_hit": 0.1958, "S3_LP_already_dark": 0.1842, "S4_chroma_compose": 0.0, "S5_other": 0.0, "denom_new_black_B": 35341}
```
- S1 dominant: multi_sigma/ridge allows large negative dY in holes → clip to black

## P1 · winner **S1_strong_neg_residual**
```
{
  "S1_strong_neg_residual": 23291,
  "S2_ridge_wire_hit": 21744,
  "S3_LP_already_dark": 18841,
  "S4_chroma_compose": 0,
  "S5_other": 0,
  "new_black_B_total": 63876,
  "new_black_A_full": 85485
}
fracs: {"S1_strong_neg_residual": 0.3646, "S2_ridge_wire_hit": 0.3404, "S3_LP_already_dark": 0.295, "S4_chroma_compose": 0.0, "S5_other": 0.0, "denom_new_black_B": 63876}
```
- S1 dominant: multi_sigma/ridge allows large negative dY in holes → clip to black
- S2 strong: new black lands on LP wire ridge → ridge gate not protecting silks
- S3: many G8 pixels sit on fragile LP (Y near 18–30) Lanczos peep

## 下一步修（按源，不調 G8 門檻）
- **S1**: cap negative residual in holes: res_y = max(res_y, -k) or hole-aware soft floor only inside cell not wire; keep ridge protect wire
- **S2**: harden ridge gate on wire: forbid new black on high-mag LP; dilate wire protect mask before fuse
- **S3**: don't SR-darken fragile LP band Y∈[18,30]; skip probe or reduce GAIN there
- **S4**: compose in linear Y with chrom separate; avoid chrom floor blow; verify to_y(C*Y)≈Y
