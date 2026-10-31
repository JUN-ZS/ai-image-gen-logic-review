# R10.1 CLEAN CHECKOUT VERIFY

- source: `gh release download r10-1-atomic-closed-loop`
- host: sandbox clean dir (CI-equivalent: empty dir + release assets only)
- asof: 2026-10-31T20:36:19Z

## Chain
```
gh release download r10-1-atomic-closed-loop
→ tar -xzf INPUTS_R10_1.tar.gz -C inputs/
→ python3 run_r10_1.py
→ python3 verify_r10_1.py .
```

## VERIFY (exit 0)
```
VERIFY PASS
runner 80bcb8f76273c7f9322f82dc64f2d777da593a9fbce2ceae49d49f5a19a2cad7
accept 5143fe3b44a5ac2c7cf64b7ce8671fc98ce834480e2b8e8e62a8ac72b55edf54
jobs 12 formal 6 skip 2
```

## Determinism
| check | result |
|-------|--------|
| runner_sha256 match release ACCEPT | **True** (`80bcb8f76273c7f9…`) |
| PNG sha vs release ACCEPT | **10/10 match** (all OK jobs) |
| ACCEPT json byte-identical | **False** (expected: `asof`/`elapsed_s` timestamps) |
| status / n_jobs / formal / skip | `PARTIAL` / 12 / 6 / 2 |

## Note
ACCEPT content hash changes each run only due to wall-clock fields; **pixels + runner are bit-stable**.

## merge_main
**NO** (formal PARTIAL · dual-ROI 6/10 · 2 SKIPPED_OOM)

## RUN TAIL
```
  "n_jobs": 12,
  "n_ok": 10,
  "n_skip": 2,
  "n_pass_formal": 6,
  "nested": {
    "lab_champion": "N2_REBASE",
    "blue_champion": "N1_DIRECT",
    "note": "blue detox primary = FIXED_MESH blue_opp; Lab secondary",
    "detail": {
      "N1_DIRECT": {
        "lab_ab_improve_pct": 85.73,
        "blue_opp_improve_pct": 44.31,
        "blue_opp_detox": 4.993406295776367,
        "ten_keep_pct": 98.07,
        "PASS_FORMAL": false
      },
      "N2_REBASE": {
        "lab_ab_improve_pct": 87.76,
        "blue_opp_improve_pct": 35.63,
        "blue_opp_detox": 5.7718119621276855,
        "ten_keep_pct": 97.57,
        "PASS_FORMAL": false
      }
    }
  },
  "runner_sha256": "80bcb8f76273c7f9322f82dc64f2d777da593a9fbce2ceae49d49f5a19a2cad7",
  "accept_sha256": "5143fe3b44a5ac2c7cf64b7ce8671fc98ce834480e2b8e8e62a8ac72b55edf54",
  "elapsed_s": 31.52
}
DONE R10.1 /workspace/artifacts/SETS/PROJ_R5_SILVER_ARMOR_2394/r10_1_CLEAN/work/complete
```
