# Dual-actor right-angle line-strike formula

Branch: `feat/dual-actor-correct-vs-inverse-strike` (branched from `main`).

## Object redesign: hammer → rigid line-shaped striker

**Do not render hammers.** Each fighter holds a single straight, rigid, thin line-shaped striker/rod. No T-head, crossbar, hammer head, extra arms, or bulky head. Keep the full length visible and keep both strikers straight; no bending, twisting, or perspective-induced false joins.

A mathematically zero-thickness line has no physical face. For a renderable face collision, represent each line as a very thin rigid bar with a small, clearly visible planar impact facet. The facet is part of the line-like object; it must not become a hammer head.

## The key geometry: crossed at 90°, faces meet

The **striker centerlines must not be collinear or coaxial**. At the impact instant their undirected axes cross at 90° (within tolerance). At the same instant, the two tiny planar impact facets are parallel and oppose one another, so they genuinely meet face-to-face. Keep these two constraints separate: the **rod axes are 90°**; the **contact-face outward normals are 180° opposed**. Do not incorrectly force the rods coaxial just to make the faces meet.

Let `a` and `b` be unit centerline directions and `f1`, `f2` the unit outward normals of the two contact facets. Since a line axis is undirected, use the absolute axis dot product:

\[
\alpha=\arccos(|\mathbf a\cdot\mathbf b|)
\]

\[
E_{90}=|\alpha-90^\circ|
\]

The two facets must oppose:

\[
E_{face}=\arccos(\operatorname{clamp}(-\mathbf f_1\cdot\mathbf f_2,-1,1))
\]

Default tolerances: `axis_tolerance_deg = 5`, `face_tolerance_deg = 8`.

\[
\mathrm{GEOMETRY\_PASS}\iff E_{90}\leq5^\circ\quad\land\quad E_{face}\leq8^\circ
\]

## Correct versus inverse-face negative control

| Role | Rod-axis relation | Contact facets | Expected result |
|------|-------------------|----------------|-----------------|
| `CORRECT_CROSSED_FACE` | 90° | face-to-face, opposing normals | **PASS** if real contact is visible |
| `INVERSE_FACE_NEGATIVE_CONTROL` | still 90° | facet rolled/flipped out of opposition | **FAIL**; must not be counted as a correct sample |
| `COAXIAL_NEGATIVE_CONTROL` | 0° | even if facets appear to meet | **FAIL**; wrong collision geometry |

The inverse control must be a deliberate orientation failure, not merely a miss hidden by camera angle. Label it as a negative control. Camera changes may alter the view but must never change the geometry classification.

## Paired action scene

- Fighter A: airborne, executing a diving/overhead/spinning attack.
- Fighter B: grounded and low (crouch, kneel, or rising attack).
- Their attack paths differ; do not mirror-copy the same pose.
- The thin line-like strikers meet each other at a visible 90° crossing event. The two small planar facets make actual face contact at the crossing point.
- Keep both full strikers, both hands/grips, the crossing point, and the contact seam visible. Sparks may accent the event but must not cover the seam.
- Do not substitute parallel/coaxial end-to-end contact, side-swipe with no facet contact, object-to-body contact, hovering gaps, or a camera-only illusion of collision.
- Vary camera azimuth, elevation, lens perspective, swing direction, airborne height, and grounded stance independently across samples; the world-space constraints above must remain true.

## Impact event lock

The formula checks geometry, not whether an image actually depicts a collision. Audit both separately:

1. `AXIS_90_PASS`: line-like centerlines intersect in projection **and** are 90° in world space.
2. `FACET_FACE_CONTACT_PASS`: the two designated planar facets visibly touch; no gap.
3. `NO_COAXIAL_CONTACT_PASS`: the strike is not end-to-end along a shared axis.
4. `PIXEL_AUDIT`: human review confirms the visible result matches the intended geometry.

If any item fails, record the image as failed; do not claim success from dynamic poses or sparks alone.

## Minimal executable formula core

```python
import math

def unit(v):
    length = math.sqrt(sum(x * x for x in v))
    if length == 0:
        raise ValueError("方向向量不可為零向量")
    return tuple(x / length for x in v)

def dot(a, b):
    return sum(a[i] * b[i] for i in range(3))

def angle_deg(cosine):
    cosine = max(-1.0, min(1.0, cosine))
    return math.degrees(math.acos(cosine))

def check_crossed_face_contact(axis_a, axis_b, face_n_a, face_n_b,
                                axis_tolerance_deg=5,
                                face_tolerance_deg=8):
    a, b = unit(axis_a), unit(axis_b)
    f1, f2 = unit(face_n_a), unit(face_n_b)

    # Undirected rod axes: parallel and anti-parallel both mean 0° apart.
    axis_angle = angle_deg(abs(dot(a, b)))
    axis_error = abs(axis_angle - 90.0)

    # Opposed outward normals means the two facets face one another.
    face_error = angle_deg(-dot(f1, f2))

    return {
        "axis_angle_deg": round(axis_angle, 6),
        "axis_error_from_90_deg": round(axis_error, 6),
        "face_opposition_error_deg": round(face_error, 6),
        "axis_90_pass": axis_error <= axis_tolerance_deg,
        "face_opposition_pass": face_error <= face_tolerance_deg,
        "geometry_pass": (
            axis_error <= axis_tolerance_deg
            and face_error <= face_tolerance_deg
        ),
    }

# Rod axes X/Y cross at 90°. Contact facets have opposite outward normals.
correct = check_crossed_face_contact(
    axis_a=(1, 0, 0), axis_b=(0, 1, 0),
    face_n_a=(0, 0, 1), face_n_b=(0, 0, -1),
)
assert correct["geometry_pass"] is True

# Negative control 1: axes remain 90°, but facets face the same way.
inverse = check_crossed_face_contact(
    axis_a=(1, 0, 0), axis_b=(0, 1, 0),
    face_n_a=(0, 0, 1), face_n_b=(0, 0, 1),
)
assert inverse["axis_90_pass"] is True
assert inverse["face_opposition_pass"] is False
assert inverse["geometry_pass"] is False

# Negative control 2: coaxial rods are never accepted as a 90° strike.
coaxial = check_crossed_face_contact(
    axis_a=(1, 0, 0), axis_b=(-1, 0, 0),
    face_n_a=(0, 0, 1), face_n_b=(0, 0, -1),
)
assert coaxial["axis_90_pass"] is False
assert coaxial["geometry_pass"] is False
```

Expected outcome: `correct.geometry_pass = True`; both negative controls are `False`.

## Acceptance status

- Formula: the code above defines deterministic geometric checks; it must be run by the repository test workflow before reporting tests as passed.
- Image realization: `NOT_RUN` until actual images are produced.
- Pixel audit: `NOT_RUN` until produced images are reviewed.
- Do not claim image success from prompt/build tests alone.
