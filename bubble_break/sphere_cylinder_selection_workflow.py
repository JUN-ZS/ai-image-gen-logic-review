#!/usr/bin/env python3
"""Compile a staged sphere-surface cylinder selection workflow.

Outputs prompt packets, a deterministic candidate manifest, and an SVG atlas
proxy. This is not an image-generation API and makes no raster-acceptance claims.
"""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence
from xml.sax.saxutils import escape

V3 = tuple[float, float, float]


def add(a: V3, b: V3) -> V3:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def mul(a: V3, scalar: float) -> V3:
    return (a[0] * scalar, a[1] * scalar, a[2] * scalar)


def dot(a: V3, b: V3) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a: V3, b: V3) -> V3:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def length(v: V3) -> float:
    return math.sqrt(dot(v, v))


def unit(v: V3) -> V3:
    magnitude = length(v)
    if magnitude < 1e-10:
        raise ValueError("方向向量不可為零向量")
    return mul(v, 1.0 / magnitude)


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


@dataclass(frozen=True)
class Candidate:
    candidate_id: str
    ring: int
    ring_index: int
    polar_deg: float
    azimuth_deg: float
    tilt_deg: float
    roll_deg: float
    anchor: V3
    outward_normal: V3
    cylinder_axis: V3
    contact_patch: str = "emissive circular/elliptical base interface"
    unselected_policy: str = "remove entirely after selection"


# Camera from sphere center towards viewer. Candidate ring basis is stable.
CAMERA_DIRECTION: V3 = unit((3.0, -5.0, 2.8))
WORLD_UP: V3 = (0.0, 0.0, 1.0)
CAMERA_RIGHT: V3 = unit(cross(CAMERA_DIRECTION, WORLD_UP))
CAMERA_UP: V3 = unit(cross(CAMERA_RIGHT, CAMERA_DIRECTION))
SPHERE_RADIUS = 100.0
STUB_LENGTH = 15.0

# 1 + 6 + 8 + 10 = 25 candidates. Ring azimuth offsets differ to reduce overlap.
RINGS: tuple[tuple[int, float, float], ...] = (
    (1, 0.0, 0.0),
    (6, 24.0, 0.0),
    (8, 46.0, 11.25),
    (10, 68.0, 0.0),
)


def make_candidates() -> list[Candidate]:
    candidates: list[Candidate] = []
    next_number = 1
    for ring_no, (count, polar_deg, azimuth_offset) in enumerate(RINGS, start=0):
        for index in range(count):
            azimuth_deg = azimuth_offset + (360.0 * index / count if count > 1 else 0.0)
            polar = math.radians(polar_deg)
            azimuth = math.radians(azimuth_deg)
            tangent = add(
                mul(CAMERA_RIGHT, math.cos(azimuth)),
                mul(CAMERA_UP, math.sin(azimuth)),
            )
            radial = unit(
                add(mul(CAMERA_DIRECTION, math.cos(polar)), mul(tangent, math.sin(polar)))
            )
            # Deliberate but modest tilts make candidate orientations distinguishable.
            tilt_deg = (0.0, 8.0, 14.0, 18.0)[ring_no]
            roll_deg = (azimuth_deg * 0.7 + ring_no * 13.0) % 360.0
            # Build a true tangent basis at this anchor so tilt_deg is exact.
            reference = WORLD_UP if abs(dot(radial, WORLD_UP)) < 0.92 else CAMERA_RIGHT
            tangent_u = unit(cross(reference, radial))
            tangent_v = unit(cross(radial, tangent_u))
            roll = math.radians(roll_deg)
            local_tangent = unit(
                add(mul(tangent_u, math.cos(roll)), mul(tangent_v, math.sin(roll)))
            )
            axis = unit(
                add(
                    mul(radial, math.cos(math.radians(tilt_deg))),
                    mul(local_tangent, math.sin(math.radians(tilt_deg))),
                )
            )
            candidates.append(
                Candidate(
                    candidate_id=f"C{next_number:02d}",
                    ring=ring_no,
                    ring_index=index,
                    polar_deg=polar_deg,
                    azimuth_deg=round(azimuth_deg % 360.0, 3),
                    tilt_deg=tilt_deg,
                    roll_deg=round(roll_deg, 3),
                    anchor=tuple(round(x, 6) for x in mul(radial, SPHERE_RADIUS)),
                    outward_normal=tuple(round(x, 8) for x in radial),
                    cylinder_axis=tuple(round(x, 8) for x in axis),
                )
            )
            next_number += 1
    return candidates


def candidate_by_id(candidates: Sequence[Candidate], candidate_id: str) -> Candidate:
    normalized = candidate_id.strip().upper()
    for candidate in candidates:
        if candidate.candidate_id == normalized:
            return candidate
    valid = ", ".join(candidate.candidate_id for candidate in candidates)
    raise ValueError(f"未知候選編號 {candidate_id!r}；可用編號：{valid}")


def fmt_vec(v: Sequence[float]) -> str:
    return "(" + ", ".join(f"{x:.4f}" for x in v) + ")"


def make_stage1_prompt(candidates: Sequence[Candidate]) -> str:
    ids = ", ".join(c.candidate_id for c in candidates)
    return f"""# STAGE 1 — SPHERE-SURFACE CYLINDER CANDIDATE ATLAS

Create one clean cinematic-technical image, 16:9 landscape, of a single intact,
large translucent spherical bubble/shell against a restrained dark neutral
background. The shell is centered and completely visible.

Place exactly {len(candidates)} short, stubby cylindrical projections directly
mounted on the visible hemisphere. Their base patches conform to the spherical
surface; each cylinder points generally outward, with controlled, individually
varied small tilts. Vary their surface positions and tilts so each candidate can
be selected independently. Cylinders must be separated enough that their base
interfaces are individually inspectable.

MOST IMPORTANT: the circular or slightly elliptical BASE INTERFACE where each
cylinder meets the bubble shell emits a distinct bright rim glow (white-hot core
with a restrained cyan/amber edge). This is the intended contact surface. It is
NOT the cylinder's free outer cap. Keep the base interface boundary crisp and
visible against the shell.

Candidate IDs in the geometric manifest: {ids}. Put small clean callout labels
near corresponding candidates when possible; do not allow text or lines to cover
the glowing interfaces. Use the accompanying candidate SVG/JSON as the positional
selection reference, not as proof of final raster accuracy.

STRICT EXCLUSIONS: no people, no hands, no handles, no long rods, no hammer or
T-shaped heads, no second sphere, no impact, no cracks, no shards, no explosion,
no smoke covering the sphere. All cylinders remain short placeholders. Do not
merge cylinders or let any be hidden behind another. This is a selection atlas,
not the final action shot.

Readability: true 3D form, clear silhouette separation, camera angle showing
depth, every base glow readable, balanced distribution over the visible sphere.
The image must make it easy for a human to choose ONE cylinder by ID and position.
"""


def selected_geometry_block(candidate: Candidate) -> str:
    return f"""Selected immutable candidate: {candidate.candidate_id}
- sphere anchor in candidate-local world frame: {fmt_vec(candidate.anchor)}
- local outward surface normal: {fmt_vec(candidate.outward_normal)}
- selected cylinder axis: {fmt_vec(candidate.cylinder_axis)}
- design tilt relative to local outward normal: {candidate.tilt_deg:.1f} degrees
- base contact patch: emissive circular/elliptical interface directly touching bubble
- contact point / axis / camera selection: LOCKED; do not drift, reselect, or invent a new one
"""


def make_stage2_prompt(candidate: Candidate) -> str:
    return f"""# STAGE 2 — ATTACH ONE HANDLE AND ONE PERSON

Use the accepted Stage-1 atlas as the identity and geometry reference. Do not
recompose the sphere or select another cylinder.

{selected_geometry_block(candidate)}
Keep exactly the selected short cylinder at the selected anchor. It is the head
of the striking tool. Attach one long, straight, rigid handle concentrically to
the cylinder's OUTER/FREE END CAP (the end away from the bubble), extending
outward away from the sphere. The joint is continuous, centered, and physically
connected; no gap, hinge, bend, or sideways handle. Preserve the selected base
contact patch touching the bubble and preserve its glow.

Add exactly ONE full human figure positioned on the outside end of the handle.
Both hands must visibly grip the handle at plausible locations, fingers wrapping
around it, wrists aligned, arms connected naturally to shoulders. Place the body
so the person could plausibly push/swing the tool toward the selected bubble
contact point. Keep the tool, contact patch, hands, and full figure in frame.

REMOVE every unselected candidate cylinder completely. The final Stage-2 frame
contains one bubble, one selected short cylindrical head, one attached long
handle, and one person. There must be no extra stubs, duplicate heads, ghost
cylinders, spare handles, disembodied hands, or additional people.

Keep the bubble intact. The selected base interface glow may be bright but must
not bloom so strongly that its exact boundary disappears. Do not add large
fractures, shards, shockwaves, or explosion effects yet. This is the structural
attachment proof frame, not the final spectacle.
"""


def make_stage3_prompt(candidate: Candidate) -> str:
    return f"""# STAGE 3 — DYNAMIC ACTION REFINEMENT (GEOMETRY LOCKED)

Animate/refine the accepted Stage-2 composition into a strong, readable action
pose: full-body weight transfer, foot plant or airborne drive as suitable,
shoulder/hip rotation, believable wrist and grip, controlled wind-up and
follow-through. Make the movement visibly different from a static upright pose.

{selected_geometry_block(candidate)}
LOCK the selected contact anchor, cylinder axis, handle-to-head joint, and
person-to-handle grip. Change body pose around this invariant assembly only as
the chosen action permits. The short cylindrical head and long handle remain
straight and rigid. No independent head rotation, curved handle, broken joint,
or handle detached from either the head or hands.

Only one cylinder/head, one handle, one person, and one bubble remain. All
unselected candidate stubs must stay removed. Preserve a clean contact proof
frame with the base interface still readable. Do not yet let debris or massive
bloom obscure the actual contact surface.
"""


def make_stage4_prompt(candidate: Candidate) -> str:
    return f"""# STAGE 4 — CONTACT BLOOM + LARGE BUBBLE-SHELL BREAK

Start from the accepted Stage-3 pose; do not rebuild or relocate the scene.

{selected_geometry_block(candidate)}
First preserve a readable contact moment: the selected cylindrical base interface
is exactly where the tool meets the bubble shell. Intensify emission at that
interface only: a white-hot contact core, tightly layered cyan/amber plasma rim,
concentric energy ripples across the spherical surface, and sharp radial cracks
that originate at the selected anchor. The glowing interface must be causally
connected to the shell fracture; do not put the main light source at the free end
of the cylinder or at an unrelated point.

Then show a spectacular shell rupture: a large section of translucent bubble
surface breaks outward from the selected anchor, with coherent curved shell
fragments, refracted highlights, luminous shock rings, and fine particles. The
sphere surface should visibly fail; do not merely add sparks around an intact
sphere. Give the effects scale and depth, but preserve the tool silhouette,
handle/head joint, gripping hands, and body action. Produce at least one clean
contact frame before the maximum bloom/debris frame.

FINAL CLEANUP: all unselected candidate cylinders are absent. No ghost stubs,
duplicate weapons, spare handles, extra people, or unrelated impact points.
Do not let sparks completely cover the contact boundary in every frame.
"""


def project(candidate: Candidate, center_x: float, center_y: float, radius: float) -> tuple[float, float, float, float]:
    anchor = unit(candidate.anchor)
    x = center_x + radius * dot(anchor, CAMERA_RIGHT)
    y = center_y - radius * dot(anchor, CAMERA_UP)
    # Axis proxy only: approximate projected direction for visibility.
    ax = dot(candidate.cylinder_axis, CAMERA_RIGHT)
    ay = -dot(candidate.cylinder_axis, CAMERA_UP)
    norm = math.hypot(ax, ay)
    if norm < 1e-5:
        ax, ay, norm = dot(CAMERA_DIRECTION, CAMERA_RIGHT), -dot(CAMERA_DIRECTION, CAMERA_UP), 1.0
    ax, ay = ax / norm, ay / norm
    end_x, end_y = x + ax * 27.0, y + ay * 27.0
    return x, y, end_x, end_y


def make_svg(candidates: Sequence[Candidate], selected_id: str | None = None) -> str:
    width, height = 1100, 850
    cx, cy, radius = 540.0, 410.0, 295.0
    elems = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#101722"/>',
        '<text x="40" y="45" fill="#ffffff" font-size="25" font-family="sans-serif">Sphere contact candidates — geometry proxy only</text>',
        f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="#84c9ec" fill-opacity="0.12" stroke="#a5e9ff" stroke-width="3"/>',
        f'<circle cx="{cx}" cy="{cy}" r="{radius - 8}" fill="none" stroke="#a5e9ff" stroke-opacity="0.2" stroke-width="1"/>',
    ]
    for candidate in candidates:
        x, y, ex, ey = project(candidate, cx, cy, radius)
        active = candidate.candidate_id == selected_id
        glow_color = "#ffffff" if active else "#49e8ff"
        stroke_width = "4" if active else "2.2"
        label_color = "#ffe48a" if active else "#e7f5ff"
        elems.extend([
            f'<line x1="{x:.2f}" y1="{y:.2f}" x2="{ex:.2f}" y2="{ey:.2f}" stroke="#b5d9ee" stroke-width="6" stroke-linecap="round" opacity="0.88"/>',
            f'<circle cx="{x:.2f}" cy="{y:.2f}" r="10" fill="{glow_color}" fill-opacity="0.30"/>',
            f'<circle cx="{x:.2f}" cy="{y:.2f}" r="5.4" fill="{glow_color}" stroke="#ffffff" stroke-width="{stroke_width}"/>',
            f'<text x="{x + 11:.2f}" y="{y - 8:.2f}" fill="{label_color}" font-size="16" font-weight="bold" font-family="sans-serif">{escape(candidate.candidate_id)}</text>',
        ])
    if selected_id:
        elems.append(f'<text x="40" y="800" fill="#ffe48a" font-size="21" font-family="sans-serif">Selected: {escape(selected_id)} (locked anchor and axis)</text>')
    else:
        elems.append('<text x="40" y="800" fill="#ffffff" font-size="18" font-family="sans-serif">Choose one candidate ID; stubs are schematic and not a rendered image.</text>')
    elems.append("</svg>")
    return "\n".join(elems) + "\n"


def build_packet(outdir: Path, selected_id: str | None = None) -> dict[str, object]:
    candidates = make_candidates()
    chosen = candidate_by_id(candidates, selected_id) if selected_id else None
    outdir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "schema_version": 1,
        "workflow": "sphere-cylinder-pick-and-attach",
        "image_realization": "NOT_RUN",
        "pixel_audit": "NOT_RUN",
        "sphere_radius_units": SPHERE_RADIUS,
        "stub_length_units": STUB_LENGTH,
        "camera_direction": CAMERA_DIRECTION,
        "candidate_count": len(candidates),
        "selected_candidate_id": chosen.candidate_id if chosen else None,
        "selection_lock": bool(chosen),
        "candidates": [asdict(c) for c in candidates],
    }
    (outdir / "candidate_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (outdir / "candidate_atlas_proxy.svg").write_text(
        make_svg(candidates, chosen.candidate_id if chosen else None), encoding="utf-8"
    )
    (outdir / "stage1_candidate_atlas.md").write_text(
        make_stage1_prompt(candidates), encoding="utf-8"
    )
    outputs = [
        "candidate_manifest.json",
        "candidate_atlas_proxy.svg",
        "stage1_candidate_atlas.md",
    ]
    if chosen:
        for filename, prompt in (
            ("stage2_attach_handle_person.md", make_stage2_prompt(chosen)),
            ("stage3_action_refine.md", make_stage3_prompt(chosen)),
            ("stage4_contact_bloom_break.md", make_stage4_prompt(chosen)),
        ):
            (outdir / filename).write_text(prompt, encoding="utf-8")
            outputs.append(filename)
    return {
        "outdir": str(outdir),
        "candidate_count": len(candidates),
        "selected_candidate_id": chosen.candidate_id if chosen else None,
        "outputs": outputs,
        "image_realization": "NOT_RUN",
        "pixel_audit": "NOT_RUN",
    }


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=Path("out/sphere_cylinder_workflow"))
    parser.add_argument("--select", type=str, default=None, help="Lock one ID, e.g. C07, and compile stages 2–4")
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        summary = build_packet(args.outdir, args.select)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
