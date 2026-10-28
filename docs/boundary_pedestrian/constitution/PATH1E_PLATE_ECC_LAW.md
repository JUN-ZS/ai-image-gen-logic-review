# PATH1E plate→ECC 法（正典附件 · §0.12.17）

> ASOF 2026-10-26T15:00:00Z  
> 用戶：試 D7-B 後「寫」  
> 樣板 `L-fc0a2fa7b8a9` · plate `44d18362…` · gate PATH1E_OK

## 正典

```
plate = Ref(face_crop, a8b)
ECC(plate → base) ≥ 0.85
hard_paste + eye_white HARD→ST
```

## 禁止（E-GS-12）

棚拍／裸 a8b 直接 ECC 到海報臉並標 PATH1E_OK。

## 閘

| 級 | ECC cc | conf | core→plate |
|----|--------|------|------------|
| OK | ≥0.85 | ≥0.55 | \<12 |
| PARTIAL | 0.55–0.85 | 0.35–0.55 | 12–25 |
| WEAK | \<0.55 或不收斂 | \<0.35 | \>25 |

## 樣板實測

- ECC cc **0.980**
- conf **0.782**
- core→plate **5.13**
- ew→ST **0.18**
- iris ∩ ew **0**

*END PATH1E_PLATE_ECC_LAW · 2026-10-26T15:00:00Z*
