# Cross Hammer 10-Panel Wash · 2026-10-23

Contract: `CROSS_HAMMER_INTO_CAMERA_BUBBLE_L1_L5`  
Refs: still `34eede64` · face `6ee74baf`  
`visual_acceptance_status`: **NOT_VERIFIED_BY_CODE** (human soft gate below)

| Panel | Skill | Camera intent | Asset | Soft L1 cross | Soft L3 barrage | Note |
|-------|-------|---------------|-------|---------------|-----------------|------|
| 01 | SK_SIDE_SWEEP | CAM_INTO_LENS_EYE | 559ad519 | PASS | PASS | strong + head |
| 02 | SK_OVERHEAD_SMASH | CAM_INTO_LENS_LOW | fc0dfa93 | PASS | PASS | low angle |
| 03 | SK_SPIN_SLASH | CAM_ORBIT_LEFT | e46aee4f | PASS | PASS | leap spin |
| 04a | SK_THRUST_INTO_LENS | CAM_INTO_LENS_EYE | 5523456b | **FAIL** | PASS | PLAIN_CYLINDER |
| 04b rewash | SK_THRUST_INTO_LENS | CAM_INTO_LENS_EYE | 9eb494a4 | PASS | PASS | cross restored |
| 05 | SK_WHIRLWIND | CAM_INTO_LENS_DUTCH | de79a141 | PASS | PASS | tunnel |
| 06 | SK_COUNTER_PUNCH | CAM_ORBIT_RIGHT | 1f51e1bc | PASS | PASS | counter |
| 07 | SK_COMBO_3HIT | CAM_INTO_LENS_LOW | b138cb5a | PASS | PASS | mid combo |
| 08 | SK_SIDE_SWEEP (W) | into lens | 04d5c60e | PASS | PASS | other side |
| 09 | SK_OVERHEAD_SMASH | zenith | e97b3c45 | PASS | PASS | top-down cross |
| 10 | SK_WHIRLWIND | boss key | fa144da7 | PASS | PASS | ring shockwave |

**Locked board for advance (use 04b not 04a):**  
01,02,03,04b,05,06,07,08,09,10

L4 intent: distinct skills/cameras across board; layout variance subjective.  
L5: no code reaudit with annotated geometry yet — geometry labels still PENDING_HUMAN_AXES.
