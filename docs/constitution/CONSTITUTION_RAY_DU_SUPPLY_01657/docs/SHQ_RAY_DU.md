# 光追递式 独补给 01657
{
  "write_id": "01657",
  "call": "光追递式·独补给",
  "formal": "SHQ_RAY_DU_ENV_SUPPLY_REC_V1",
  "vs_true_path_trace": {
    "true": "mesh+BRDF+ray PDF multi-bounce",
    "ours": "image-space ENV map + gradient normal guess + recursive ENV inject",
    "can_produce_独补给": true,
    "limit": "无真遮挡/焦散几何；透光玻璃为猜式 fresnel"
  },
  "递式": [
    "B0 ENV0 = mix(scene↓, reflect_pixels(glass))",
    "B1 SUPPLY_glass = sample(ENV0) on S0.NEAR  独",
    "ENV1 = ENV0 ⊕ inject(B1 peep)",
    "B2 SUPPLY_metal = sample(ENV1) on S0.FAR  独",
    "B3 SUPPLY_diff  = sample(ENV1) on S0.MID  独",
    "S11 = FOV hardpaste back→front outside=0"
  ],
  "parents": [
    "回正镜01656",
    "独·环境反射",
    "轴.反射.生",
    "叠斜折",
    "移轴FOV"
  ],
  "asof": "2026-11-12T02:32:03.399944+00:00"
}