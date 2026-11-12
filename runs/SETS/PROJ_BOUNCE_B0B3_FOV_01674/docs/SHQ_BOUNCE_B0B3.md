# 追·B0B3 01674

```
B0: ENV0 = mix(↓FF_scene, reflect_pix)
B1: SUPPLY_glass = sample(ENV0)⊙M_NEAR 独; ENV1 = ENV0⊕inject(B1)
B2: SUPPLY_metal = sample(ENV1)⊙M_FAR 独
B3: SUPPLY_diff  = sample(ENV1)⊙M_MID 独
S11: FOV-hardpaste(B2→B3→B1), outside=0
```
FOV: FAR soft · MID · NEAR sharp. 镂空 aperture=L1. 禁框.
outside_vs_L1=0 PASS=True
