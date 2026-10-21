# Dual-actor correct vs inverse-face strike formula

Branch: `feat/dual-actor-correct-vs-inverse-strike` (from `main`).

## Invariant (geometry — camera cannot change this)

Let `n` be the unit outward normal of the target at the contact point, and `f` the unit normal of the hammer's intended flat striking face. A valid face-on strike requires:

\[
\mathrm{PASS} \iff \mathbf{f}\cdot(-\mathbf{n}) \ge \cos(\theta_{\mathrm{tol}})
\]

Default tolerance: 8 degrees.

| Role | Face | Expectation |
|------|------|-------------|
| CORRECT | `f = -n` | alignment ≈ +1 → **PASS** |
| INVERSE_NEGATIVE_CONTROL | `f = n` | alignment ≈ −1 → **must FAIL**, never mixed into correct samples |

Camera azimuth/elevation/orbit may change freely. Camera must **not** reclassify an inverse face as correct.

## Impact event lock (pixels — without this, formula cannot be audited)

Formula checks *orientation*. Realization must still produce a **weapon-on-weapon contact event**.

Mandatory prompt lines for every realization:

1. **THE IMPACT:** the two hammer heads meet mid-air with sparks; weapon-on-weapon only.
2. **Forbidden:** missing contact, hovering gap, hitting bodies, hitting floor.
3. **Correct tip face vs inverse cheek face still TOUCH** each other (inverse is wrong *orientation*, not a miss).

If hammers do not meet, the frame is `IMPACT_EVENT_FAIL` even when poses look dynamic.

## Paired scene variables

| Variable | Actor A | Actor B |
|----------|---------|---------|
| Height | airborne | ground low / crouch |
| Swing path | dive, overhead, spin… | rising pick, ground sweep… |
| Face | CORRECT *or* inverse (alternate who is correct) | the other role |
| Camera | free view transform | free view transform |
| Scale (optional pack) | mega T-hammer ~ human body size, sci-fi | same |

Actors must not mirror-copy poses. Full head, long handle, and contact seam must remain inspectable. Sparks must not hide the seam.

## Acceptance gates

| Gate | Meaning |
|------|---------|
| formula unit tests | `f·(-n)` CORRECT pass / INVERSE fail |
| image_realization | raster produced or `NOT_RUN` |
| impact_event | hammer-face clash present or fail |
| pixel_audit | human review of face types + poses |
| contact_PASS_claimed | **false** for paired scene (contains intentional FAIL control) |
| formula_PASS_claimed | only after formula tests; never from a single pretty image |

Until reviewed: `IMAGE_REALIZATION=NOT_RUN` (or CANDIDATE) and `PIXEL_AUDIT=NOT_RUN`.

## Minimal executable core

```python
import math

def unit(v):
    length = math.sqrt(sum(x * x for x in v))
    if length == 0:
        raise ValueError("法線不可為零向量")
    return tuple(x / length for x in v)

def check_contact(target_normal, face_normal, tolerance_deg=8):
    n = unit(target_normal)
    f = unit(face_normal)
    alignment = sum(f[i] * (-n[i]) for i in range(3))
    threshold = math.cos(math.radians(tolerance_deg))
    return {
        "alignment": round(alignment, 6),
        "threshold": round(threshold, 6),
        "pass": alignment >= threshold,
    }

n = (1, 0, 0)
correct = check_contact(n, (-1, 0, 0))
inverse = check_contact(n, (1, 0, 0))
assert correct["pass"] is True
assert inverse["pass"] is False
```

Expected: CORRECT alignment=1.0 pass; INVERSE_NEGATIVE_CONTROL alignment=-1.0 fail.
