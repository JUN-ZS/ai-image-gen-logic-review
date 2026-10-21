#!/usr/bin/env python3
"""Compile formula prompts for double-ended cylindrical hammers planted on a bubble.

The handle sprouts sideways from each radial cylindrical head. The glowing,
sphere-conforming contact interface is at the planted base. This compiler emits
prompts/metadata/SVG only; it does not generate images or claim pixel acceptance.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence
from xml.sax.saxutils import escape

V3 = tuple[float, float, float]
CANDIDATE_COUNT = 24
BUBBLE_DIAMETER = 1000.0
BUBBLE_RADIUS = BUBBLE_DIAMETER / 2.0
HEAD_DIAMETER_RATIO = 0.08
HEAD_LENGTH_TO_DIAMETER = 1.5
HANDLE_LENGTH_TO_HEAD_LENGTH = 3.0
HANDLE_DIAMETER_TO_HEAD_DIAMETER = 0.10
# Stage C hard locks (user 2026-10-21):
# - NO_NEW_HANDLE: B-master handle only; never grow a new shaft
# - person:hammer = 1:1 means MINI person: full-body visual area ≈ hammer assembly
#   visual area in frame (person is small, not life-size vs bubble). NOT person >> hammer.
PERSON_TO_HAMMER_SCALE_DEFAULT = 1.0
NO_NEW_HANDLE = True
SEED = 20261021
WORLD_UP: V3 = (0.0, 0.0, 1.0)
VIEW_DIRECTION: V3 = (0.381, -0.762, 0.524)


def add(a: V3, b: V3) -> V3:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def sub(a: V3, b: V3) -> V3:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


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


CAMERA_DIRECTION: V3 = unit(VIEW_DIRECTION)
CAMERA_RIGHT: V3 = unit(cross(WORLD_UP, CAMERA_DIRECTION))
CAMERA_UP: V3 = unit(cross(CAMERA_DIRECTION, CAMERA_RIGHT))

HEAD_DIAMETER = BUBBLE_DIAMETER * HEAD_DIAMETER_RATIO
HEAD_LENGTH = HEAD_DIAMETER * HEAD_LENGTH_TO_DIAMETER
HANDLE_LENGTH = HEAD_LENGTH * HANDLE_LENGTH_TO_HEAD_LENGTH
HANDLE_DIAMETER = HEAD_DIAMETER * HANDLE_DIAMETER_TO_HEAD_DIAMETER


@dataclass(frozen=True)
class HammerCandidate:
    candidate_id: str
    index: int
    radial_head_axis: V3
    bubble_contact_anchor: V3
    head_outer_cap_center: V3
    handle_tangent_direction: V3
    handle_root: V3
    handle_end: V3
    polar_deg_to_camera: float
    azimuth_deg: float
    handle_roll_deg: float
    projected_contact_x: float
    projected_contact_y: float
    projected_handle_x: float
    projected_handle_y: float
    head_diameter: float = HEAD_DIAMETER
    head_axial_length: float = HEAD_LENGTH
    handle_length: float = HANDLE_LENGTH
    handle_diameter: float = HANDLE_DIAMETER


def tangent_basis(normal: V3) -> tuple[V3, V3]:
    reference = WORLD_UP if abs(dot(normal, WORLD_UP)) < 0.92 else CAMERA_RIGHT
    tangent_u = unit(cross(reference, normal))
    tangent_v = unit(cross(normal, tangent_u))
    return tangent_u, tangent_v


def make_candidates(count: int = CANDIDATE_COUNT, seed: int = SEED) -> list[HammerCandidate]:
    """Make stable irregular sphere anchors; handle directions stay tangent to the sphere."""
    if count < 1:
        raise ValueError("候選數量必須至少為 1")
    rng = random.Random(seed)
    camera = CAMERA_DIRECTION
    right = CAMERA_RIGHT
    up = CAMERA_UP
    golden_angle = math.pi * (3.0 - math.sqrt(5.0))
    min_polar = math.radians(27.0)
    max_polar = math.radians(77.0)
    cos_min = math.cos(min_polar)
    cos_max = math.cos(max_polar)
    candidates: list[HammerCandidate] = []

    for i in range(count):
        fraction = (i + 0.5) / count
        cos_polar = clamp(
            cos_min + fraction * (cos_max - cos_min) + rng.uniform(-0.014, 0.014),
            cos_max,
            cos_min,
        )
        polar = math.acos(cos_polar)
        azimuth = i * golden_angle + rng.uniform(-0.20, 0.20)
        tangent = add(mul(right, math.cos(azimuth)), mul(up, math.sin(azimuth)))
        radial = unit(add(mul(camera, math.cos(polar)), mul(tangent, math.sin(polar))))
        contact = mul(radial, BUBBLE_RADIUS)
        outer_cap = mul(radial, BUBBLE_RADIUS + HEAD_LENGTH)
        head_center = mul(radial, BUBBLE_RADIUS + HEAD_LENGTH / 2.0)

        tangent_u, tangent_v = tangent_basis(radial)
        roll_deg = rng.uniform(0.0, 360.0)
        roll = math.radians(roll_deg)
        handle_axis = unit(add(mul(tangent_u, math.cos(roll)), mul(tangent_v, math.sin(roll))))
        handle_root = head_center
        handle_end = add(handle_root, mul(handle_axis, HANDLE_LENGTH))

        proxy_scale = 275.0 / BUBBLE_RADIUS
        projected_contact_x = 700.0 + proxy_scale * dot(contact, right)
        projected_contact_y = 600.0 - proxy_scale * dot(contact, up)
        projected_handle_x = 700.0 + proxy_scale * dot(handle_end, right)
        projected_handle_y = 600.0 - proxy_scale * dot(handle_end, up)

        candidates.append(HammerCandidate(
            candidate_id=f"C{i + 1:02d}",
            index=i,
            radial_head_axis=tuple(round(x, 8) for x in radial),
            bubble_contact_anchor=tuple(round(x, 8) for x in contact),
            head_outer_cap_center=tuple(round(x, 8) for x in outer_cap),
            handle_tangent_direction=tuple(round(x, 8) for x in handle_axis),
            handle_root=tuple(round(x, 8) for x in handle_root),
            handle_end=tuple(round(x, 8) for x in handle_end),
            polar_deg_to_camera=round(math.degrees(polar), 4),
            azimuth_deg=round(math.degrees(azimuth) % 360.0, 4),
            handle_roll_deg=round(roll_deg, 4),
            projected_contact_x=round(projected_contact_x, 3),
            projected_contact_y=round(projected_contact_y, 3),
            projected_handle_x=round(projected_handle_x, 3),
            projected_handle_y=round(projected_handle_y, 3),
        ))
    return candidates


def candidate_by_id(candidates: Sequence[HammerCandidate], candidate_id: str) -> HammerCandidate:
    requested = candidate_id.strip().upper()
    for candidate in candidates:
        if candidate.candidate_id == requested:
            return candidate
    raise ValueError(f"未知候選編號 {candidate_id!r}；可用範圍為 C01–C{len(candidates):02d}")


def fmt_vec(vector: Sequence[float]) -> str:
    return "(" + ", ".join(f"{value:.4f}" for value in vector) + ")"


def make_stage_a_prompt(candidates: Sequence[HammerCandidate]) -> str:
    ids = ", ".join(candidate.candidate_id for candidate in candidates)
    return f"""# STAGE A — DENSE DOUBLE-ENDED ROUND HAMMERS PLANTED ON ONE BUBBLE

Create one cinematic 16:9 image with exactly ONE large, intact, translucent
spherical bubble. Densely plant exactly {len(candidates)} complete double-ended
round cylindrical hammers across irregular positions on its visible surface,
like many trees planted on a sphere. This is one continuous spatial scene, not a
grid, tile sheet, row/column layout, or repeated isometric product stamps.

CORRECT HAMMER TOPOLOGY — DO NOT REINTERPRET:
- Each hammer head is a short, solid, straight circular cylinder with TWO axial
  circular end caps: one bubble-facing base cap and one outer cap. It is not a
  ball, spike, T-crossbar, single disk, or projectile aimed at the bubble.
- The head's cylindrical axis follows the local outward normal of the sphere,
  like a planted trunk. The bubble-facing base cap is seated flush against the
  bubble with a small sphere-conforming contact seat/pad. The full circular
  contact footprint touches the shell with NO hovering gap.
- The contact footprint/base seam at the sphere is bright and legible: white-hot
  or cyan-white core, restrained amber/cyan rim. This glow is at the PLANTED BASE
  INTERFACE, not on the outer cap and not at the handle joint.
- One long thin straight handle attaches to the SIDE-MIDDLE of the cylinder
  head and sprouts SIDEWAYS in the local tangent plane, approximately 90 degrees
  to the radial head axis. It is a lateral branch from the planted head, not an
  axial extension, not rooted directly into the bubble, and not pointing through
  the sphere.
- Preserve the visible side attachment joint. One rigid cylindrical head, one
  single continuous lateral handle per candidate; no duplicate handle.

COMMON PROPORTION FORMULA FOR ALL {len(candidates)} CANDIDATES:
D_head = 0.08 * D_bubble
H_head = 1.5 * D_head
L_handle = 3 * H_head
D_handle = D_head / 10 (approximately one fifth of the head radius).
Use identical object proportions across all candidates. Candidate variety comes
from different surface anchors, radial axes, tangent handle directions,
perspective depth and projected slopes—not arbitrary size changes.

DENSE BUT AUDITABLE:
- Distribute all hammers irregularly around the visible curved surface in depth;
  vary both the surface anchor and sideways handle direction. Make the handle
  directions clearly diverse in the image. Do not align every handle the same way.
- Every cylindrical head must read as double-ended, with the planted base
  interface boundary, outer circular cap, side-middle handle joint, and whole
  handle separately inspectable. Do not let tools fuse together.
- Put labels {ids} next to OUTER HANDLE TIPS, never on the glowing base/contact
  patch. One ID belongs to one visible hammer only; avoid duplicated labels.
- Keep the whole sphere visible, filled with dense candidates but no tiny stamps.
  Object readability is more important than squeezing the maximum count.

STRICT EXCLUSIONS: no people, no hands, no bodies, no swing/action motion, no
hammer-to-hammer collisions, no extra bubbles, no cracks, no shards, no explosion,
no smoke, no giant sparks covering the contact patch, no T-heads shaped as one
flat bar across the top. The bubble remains intact; every hammer is planted on
the bubble surface by its base, as a tree is planted in soil.

Candidate IDs guide user selection only. Do not claim model-world coordinates or
proxy projection are exact raster truth. The actual generated Stage-A raster is
the authority for choosing the hammer and its visible contact location.
"""


def selected_geometry_note(candidate: HammerCandidate, bubble_scale: float, hammer_scale: float) -> str:
    return f"""SELECTED CANDIDATE: {candidate.candidate_id}
PROXY METADATA ONLY — NOT PIXEL-EXACT EVIDENCE:
- radial head axis: {fmt_vec(candidate.radial_head_axis)}
- bubble contact anchor: {fmt_vec(candidate.bubble_contact_anchor)}
- lateral handle tangent axis: {fmt_vec(candidate.handle_tangent_direction)}
- approximate outer head cap center: {fmt_vec(candidate.head_outer_cap_center)}
- approximate side-handle root: {fmt_vec(candidate.handle_root)}
Use the actual Stage-A raster-visible selected hammer as the geometry source.
If raster and proxy differ, preserve the raster and do not move it to match JSON.
Authorized scale factors:
- bubble scale relative to Stage A: {bubble_scale:.3f}x
- selected hammer scale relative to Stage A: {hammer_scale:.3f}x
"""


def make_stage_b_prompt(
    candidate: HammerCandidate,
    bubble_scale: float = 1.0,
    hammer_scale: float = 1.0,
    raster_sha256: str | None = None,
    roi: tuple[int, int, int, int] | None = None,
) -> str:
    raster_info = ""
    if raster_sha256:
        raster_info += f"Source Stage-A raster SHA-256: {raster_sha256}.\n"
    if roi:
        raster_info += f"User-confirmed selected raster ROI (x,y,width,height): {roi}.\n"
    raster_info += "If the real source raster is not supplied to the edit model, BLOCK; never reconstruct from text alone.\n"
    return f"""# STAGE B — ISOLATE ONE PLANTED ROUND HAMMER, NO PERSON

Use the exact accepted Stage-A raster as the image-reference/inpainting source.
Do not compose a new bubble from text and do not use proxy coordinates as proof.

{raster_info}
{selected_geometry_note(candidate, bubble_scale, hammer_scale)}
Select the actual visible {candidate.candidate_id} hammer in the raster. Preserve
its bubble anchor, glowing full-base contact interface, two-ended round cylinder,
outer cap, side-middle handle joint, sideways/tangent handle direction and
perspective as actually shown.

Remove every other 23 hammer assemblies completely: no spare heads, handles,
glows, labels, reflections, or ghost fragments. Keep one bubble and exactly one
selected hammer. No human, hands, swing action, cracks, shards or explosion.

The hammer head stays planted radially on the sphere. Its bubble-facing base
remains fully seated with no gap; its base contact seam glows. Its one thin,
straight handle must remain attached at the SIDE-MIDDLE of the head and extend
sideways in the local tangent plane, roughly perpendicular to the head axis.
Never put the handle on the contact base, never extend it axially from the outer
cap, never aim it through the bubble, never break the side joint.

Unless overridden by the recorded scale factors, preserve H_head = 1.5 D_head,
L_handle = 3 H_head, and D_handle = D_head / 10. A scale change must be deliberate
and reported; it must not silently change topology or move the selected anchor.
"""


def make_stage_c_prompt(
    candidate: HammerCandidate,
    person_to_hammer_scale: float = PERSON_TO_HAMMER_SCALE_DEFAULT,
) -> str:
    """Stage C hard locks: NO_NEW_HANDLE; person:hammer scale (default 1:1)."""
    if person_to_hammer_scale <= 0:
        raise ValueError("person_to_hammer_scale 必須是正數")
    return f"""# STAGE C — ADD ONE PERSON (NO NEW HANDLE · PERSON:HAMMER = {person_to_hammer_scale:.3f}:1)

Use the approved Stage-B raster only. Preserve the actual selected {candidate.candidate_id}
hammer and its bubble contact point. Do not reconstruct the tool.

## HARD LOCK A — NO_NEW_HANDLE (non-negotiable)
- Do NOT add, grow, extrude, or invent any new handle, shaft, rod, or grip bar.
- Do NOT convert the tool into (head + coaxial long shaft).
- Do NOT attach any rod to the outer end cap or through the glowing base.
- The ONLY handle is the existing single thin lateral rod already on the Stage-B
  raster: attached at the SIDE-MIDDLE of the cylinder, ~90° to the radial axis.
- Hands must grip that SAME existing lateral handle only. If grip is hard, move
  the person — never grow a new shaft for convenience.
- Outer circular end cap must stay free and empty. Base contact glow stays free.

## HARD LOCK B — PERSON : HAMMER = {person_to_hammer_scale:.3f} : 1 (MINI PERSON)
- person:hammer = 1:1 means the person's FULL BODY and the locked hammer assembly
  occupy roughly the SAME visual area in the frame — the person is MINI next to the
  large bubble (人變迷你：全身面積 ≈ 槌面積).
- Default locked target: person_to_hammer_scale = 1.0.
- REJECT if the person is life-size / much larger than the hammer (person >> hammer).
- REJECT if the person is ant-sized speck much smaller than the hammer (person << hammer).
- Do not enlarge or reshape the hammer; scale the MINI person to match the hammer area.
- Still NOT person height = k × bubble diameter.

Add exactly one complete person beside/outside the bubble where the existing
sideways handle can be gripped. One or both hands visibly grip the SAME existing
lateral handle; fingers, wrists, elbows and shoulders connect naturally. The
person must not block the luminous base interface or overwrite the side joint.

Keep the planted double-ended cylinder, both circular ends, tangent side handle,
full-base contact and contact glow. All 23 other candidate hammers remain absent.
Bubble intact; no large break effect yet. Record bubble/hammer/person ratios.
If a generation grows a new handle or changes handle axis, it is REJECT (same
error class as outer-end quasi-axial shaft).
"""


def make_stage_d_prompt(candidate: HammerCandidate) -> str:
    return f"""# STAGE D — ACTION REFINEMENT WITH PLANTED-CONTACT LOCK

Start from the accepted Stage-C raster. Refine stance, weight transfer, torso and
shoulder rotation, grip, and a readable wind-up/follow-through around the selected
{candidate.candidate_id} hammer. Avoid a static mannequin pose.

Keep the double-ended cylindrical head rigid, with its planted base and glowing
interface at the accepted anchor. Keep the handle attached to the head's side-middle
joint and preserve its tangent direction/length. Do not detach or bend the handle,
flip the two caps, silently shift the anchor, restore any other hammers, or
grow any new handle / outer-end coaxial shaft (NO_NEW_HANDLE remains locked). If the
action intentionally lifts the tool from the bubble, it is a separate state and
must not be mislabeled as the still-planted contact state.
"""



def make_stage_d_step_prompt(
    candidate: HammerCandidate,
    step: str,
    prev_raster_sha256: str | None = None,
    from_step: str | None = None,
) -> str:
    """Emit one Stage-D micro-step prompt. Outer-end new handle is always REJECT.

    Formula lock: no skipping D1/D2; first grip (D2) must hard-lock previous frame
    side-handle pixels via prev_raster_sha256. Use stage_d_gates to enforce.
    """
    from bubble_break.stage_d_gates import (
        grip_pixel_lock_clause,
        normalize_step,
        previous_step,
        validate_step_transition,
    )

    step = normalize_step(step)
    if from_step is None and step != "D0":
        from_step = previous_step(step)
    validate_step_transition(from_step, step)
    if step != "D0" and not prev_raster_sha256:
        # still emit prompt text but mark REQUIRED so full-RUN gate fails closed
        prev_raster_sha256 = prev_raster_sha256  # may be None → clause shows REQUIRED
    pixel_lock = grip_pixel_lock_clause(step, prev_raster_sha256)
    common = f"""SOURCE: locked Stage-B master for {candidate.candidate_id} only.
FROZEN TOPOLOGY (must match source pixels): double-ended cylindrical head planted on bubble;
cyan-white glow only at base contact; outer circular end cap EMPTY; ONE thin handle only at
SIDE-MIDDLE of cylinder (~90° to radial axis). NO_NEW_HANDLE: any outer-end shaft / second
rod / handle-axis rewrite is REJECT — roll back.
PERSON SCALE when person exists: mini, full-body visual area ≈ hammer area (1:1).
STEP CHAIN LOCK: never skip D1/D2; order D0→D1→D2→D3→D4 only.
{pixel_lock}
"""
    steps = {
        "D0": common + """
# STEP D0 — TOPOLOGY FREEZE (no person)
Re-output the locked hammer only. Zero people. Zero new geometry. Outer cap empty.
""",
        "D1": common + """
# STEP D1 — MINI PERSON PLACE (no grip)
Add exactly one mini person (full-body area ≈ hammer area) beside the bubble near the
existing side handle. Hands must NOT grip the tool yet (open or at sides). Do not move
or rewrite any hammer part. Outer end cap stays empty. No new handle.
""",
        "D2": common + """
# STEP D2 — GRIP EXISTING HANDLE ONLY (FIRST GRIP — PIXEL HARD LOCK)
From accepted D1 raster only (prev_raster_sha256 above). Move hands onto the SAME
existing side-middle lateral rod pixels already in that D1 frame.
Do not invent a new handle. Do not grow outer-end shaft. Outer cap empty.
Keep mini 1:1 scale. Still-planted base.
After IMG→IMG: run stage_d_gates (outer_end_empty + side_handle_present). FAIL → roll back to D1.
PROVEN 2026-10-21 HARD LOCK: 跳過「握既有左柄」會長新柄；鎖左柄像素後可壓住。
Grip the SAME left-pointing side-middle rod already in D1; outer end EMPTY; never a new outer-end stub.
""",
        "D3": common + """
# STEP D3 — 找／持槌氣勢＋動作
From accepted D2: refine stance, weight transfer, eyes, intent (seek→hold). Keep grip on
existing side-middle handle only. Still planted. No break FX. NO_NEW_HANDLE.
""",
        "D4": common + """
# STEP D4 — POLISH ONLY
Lighting/clothing polish only. No topology change. NO_NEW_HANDLE.
""",
    }
    if step not in steps:
        raise ValueError(f"未知 Stage D step {step!r}；可用 D0–D4")
    return steps[step].strip() + "\n"


def make_stage_e_prompt(candidate: HammerCandidate) -> str:
    return f"""# STAGE E — GLOWING PLANTED BASE → BUBBLE BREAK SPECTACLE

Use the accepted Stage-D raster. Do not recreate the person, bubble or {candidate.candidate_id}
hammer. Lock their approved relative ratios, selected surface anchor, radial head
axis, circular planted base contact, and side-mounted lateral handle.

The first bright energy source is the selected HAMMER BASE / BUBBLE INTERFACE.
Intensify its rim and contact core, then send coherent luminous ripples along the
translucent spherical shell. Radial cracks must originate at this selected planted
anchor—not at the outer cap or side-handle joint. The peak frame shows the bubble
shell bursting outward from that same point, with curved translucent shards,
large luminous shock rings and dramatic depth.

Provide a clean contact frame before the biggest bloom. At least one frame must
keep the whole glowing base boundary, both cylindrical-head cap identity, side
handle joint and the person's grip readable. Do not let sparks/bloom obscure the
contact seam in every frame. All other 23 hammer assemblies remain absent.
"""


def parse_roi(value: str) -> tuple[int, int, int, int]:
    try:
        parts = tuple(int(item.strip()) for item in value.split(","))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("ROI 格式必須是 x,y,width,height") from exc
    if len(parts) != 4 or parts[0] < 0 or parts[1] < 0 or parts[2] <= 0 or parts[3] <= 0:
        raise argparse.ArgumentTypeError("ROI 必須是非負 x/y 及正數 width/height")
    return parts  # type: ignore[return-value]


def project_point(point: V3, cx: float, cy: float, radius_px: float) -> tuple[float, float]:
    scale = radius_px / BUBBLE_RADIUS
    return (
        cx + scale * dot(point, CAMERA_RIGHT),
        cy - scale * dot(point, CAMERA_UP),
    )


def make_svg(candidates: Sequence[HammerCandidate], selected_id: str | None = None) -> str:
    width, height = 1400, 1200
    cx, cy, sphere_px = 700.0, 600.0, 275.0
    scale = sphere_px / BUBBLE_RADIUS
    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#101720"/>',
        '<text x="36" y="42" fill="#ffffff" font-family="sans-serif" font-size="25">Planted double-ended hammer / bubble — geometry proxy only</text>',
        f'<circle cx="{cx}" cy="{cy}" r="{sphere_px}" fill="#92ddf7" fill-opacity="0.13" stroke="#aeeeff" stroke-width="3"/>',
    ]
    for candidate in candidates:
        anchor = candidate.bubble_contact_anchor
        head_top = candidate.head_outer_cap_center
        handle_root = candidate.handle_root
        handle_end = candidate.handle_end
        ax, ay = project_point(anchor, cx, cy, sphere_px)
        tx, ty = project_point(head_top, cx, cy, sphere_px)
        hx, hy = project_point(handle_root, cx, cy, sphere_px)
        ex, ey = project_point(handle_end, cx, cy, sphere_px)
        selected = candidate.candidate_id == selected_id
        color = "#fff3a6" if selected else "#69efff"
        width_face = 4 if selected else 2.0
        # Planted head axis: base at sphere, outer cap outside; lateral handle leaves side-middle.
        elements.extend([
            f'<line x1="{ax:.2f}" y1="{ay:.2f}" x2="{tx:.2f}" y2="{ty:.2f}" stroke="#b8d0df" stroke-width="{HEAD_DIAMETER * scale:.2f}" stroke-linecap="round"/>',
            f'<circle cx="{ax:.2f}" cy="{ay:.2f}" r="{HEAD_DIAMETER * scale * 0.34:.2f}" fill="{color}" fill-opacity="0.45" stroke="#ffffff" stroke-width="{width_face}"/>',
            f'<circle cx="{tx:.2f}" cy="{ty:.2f}" r="{HEAD_DIAMETER * scale * 0.34:.2f}" fill="#b8d0df" stroke="#ffffff" stroke-width="1.5"/>',
            f'<line x1="{hx:.2f}" y1="{hy:.2f}" x2="{ex:.2f}" y2="{ey:.2f}" stroke="#d5e3ed" stroke-width="{HANDLE_DIAMETER * scale:.2f}" stroke-linecap="round"/>',
            f'<text x="{ex + 7:.2f}" y="{ey - 4:.2f}" fill="{color}" font-family="sans-serif" font-size="16" font-weight="bold">{escape(candidate.candidate_id)}</text>',
        ])
    if selected_id:
        elements.append(f'<text x="36" y="1160" fill="#fff3a6" font-family="sans-serif" font-size="20">Selected {escape(selected_id)} — use actual raster as authority</text>')
    else:
        elements.append('<text x="36" y="1160" fill="#ffffff" font-family="sans-serif" font-size="19">24 candidate proxies only; actual raster is required for pixel selection.</text>')
    elements.append("</svg>")
    return "\n".join(elements) + "\n"



def _raise_deprecated_person_bubble():
    raise ValueError(
        "--person-height-of-bubble 已廢止；Stage C 人:槌硬鎖 1:1，請用 --person-to-hammer-scale"
    )


def build_packet(
    outdir: Path,
    selected_id: str | None = None,
    bubble_scale: float = 1.0,
    hammer_scale: float = 1.0,
    person_to_hammer_scale: float = PERSON_TO_HAMMER_SCALE_DEFAULT,
    source_raster: Path | None = None,
    roi: tuple[int, int, int, int] | None = None,
) -> dict[str, object]:
    for name, value in (
        ("bubble_scale", bubble_scale),
        ("hammer_scale", hammer_scale),
        ("person_to_hammer_scale", person_to_hammer_scale),
    ):
        if not math.isfinite(value) or value <= 0:
            raise ValueError(f"{name} 必須是正的有限數值")
    if roi and not source_raster:
        raise ValueError("--roi 必須與 --source-raster 一起使用")
    if source_raster and not source_raster.is_file():
        raise ValueError(f"找不到來源 Stage-A 圖片：{source_raster}")

    candidates = make_candidates()
    selected = candidate_by_id(candidates, selected_id) if selected_id else None
    raster_sha = hashlib.sha256(source_raster.read_bytes()).hexdigest() if source_raster else None
    outdir.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, object] = {
        "schema_version": 2,
        "workflow": "double-ended-round-hammer-planted-on-bubble",
        "topology": {
            "head": "double-ended cylindrical round head, radial axis",
            "contact": "bubble-facing base cap with sphere-conforming full-seat interface",
            "handle": "single lateral handle attached at head side-middle, tangent to sphere",
            "stage_c_hard_locks": "NO_NEW_HANDLE; person_to_hammer_scale default 1:1",
            "stage_d_chain": "D0→D1→D2→D3→D4 no skip; D2 first-grip locks prev side-handle pixels; pixel gates block_next on FAIL",
        },
        "stage_a_candidate_count": len(candidates),
        "bubble_diameter_proxy_units": BUBBLE_DIAMETER,
        "hammer_proportions": {
            "head_diameter_over_bubble_diameter": HEAD_DIAMETER_RATIO,
            "head_axial_length_over_head_diameter": HEAD_LENGTH_TO_DIAMETER,
            "lateral_handle_length_over_head_axial_length": HANDLE_LENGTH_TO_HEAD_LENGTH,
            "handle_diameter_over_head_diameter": HANDLE_DIAMETER_TO_HEAD_DIAMETER,
        },
        "selected_candidate_id": selected.candidate_id if selected else None,
        "scale_changes": {
            "bubble_scale": bubble_scale,
            "hammer_scale": hammer_scale,
            "person_to_hammer_scale": person_to_hammer_scale,
            "person_height_over_bubble_diameter": None,
            "NO_NEW_HANDLE": True,
            "person_scale_rule": "MINI person: full-body visual area : hammer assembly visual area = person_to_hammer_scale : 1 (default 1:1; 人變迷你; NOT person>>hammer; NOT k*bubble)",
        },
        "source_stage_a_raster": str(source_raster) if source_raster else None,
        "source_stage_a_sha256": raster_sha,
        "selected_raster_roi_xywh": roi,
        "raster_selection_evidence": (
            "SOURCE_SHA256_AND_USER_ROI_RECORDED" if raster_sha and roi
            else "PENDING_REAL_RASTER_REFERENCE"
        ),
        "image_realization": "NOT_RUN",
        "pixel_audit": "NOT_RUN",
        "candidates": [asdict(candidate) for candidate in candidates],
    }
    (outdir / "candidate_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (outdir / "planted_round_hammer_proxy.svg").write_text(
        make_svg(candidates, selected.candidate_id if selected else None), encoding="utf-8"
    )
    (outdir / "stage_a_planted_round_hammer_atlas.md").write_text(
        make_stage_a_prompt(candidates), encoding="utf-8"
    )
    outputs = ["candidate_manifest.json", "planted_round_hammer_proxy.svg", "stage_a_planted_round_hammer_atlas.md"]
    if selected:
        (outdir / "stage_b_one_hammer_no_person.md").write_text(
            make_stage_b_prompt(selected, bubble_scale, hammer_scale, raster_sha, roi), encoding="utf-8"
        )
        (outdir / "stage_c_scale_and_add_person.md").write_text(
            make_stage_c_prompt(selected, person_to_hammer_scale), encoding="utf-8"
        )
        (outdir / "stage_d_action_refinement.md").write_text(
            make_stage_d_prompt(selected), encoding="utf-8"
        )
        # Emit D0–D4 with step-chain formula (no skip); SHA filled later by gate runner
        _prev = None
        for _dstep in ("D0", "D1", "D2", "D3", "D4"):
            _name = f"stage_d_step_{_dstep}.md"
            (outdir / _name).write_text(
                make_stage_d_step_prompt(selected, _dstep, prev_raster_sha256=None, from_step=_prev),
                encoding="utf-8",
            )
            _prev = _dstep
        (outdir / "stage_d_GATES.md").write_text(
            """# Stage D script gates (mandatory after each IMG→IMG)

## Formula error that must never recur
- Skipping D1/D2, or first grip (D2) without locking previous-frame side-handle pixels.

## After full program RUN + each step raster
1. validate_step_transition(prev, current) — no skip
2. prev_raster_sha256 required for D1+
3. Pixel gates: outer_end_empty + side_handle_present (ROIs)
4. overall_pass False → block_next; do not proceed; roll back

```bash
python -m bubble_break.stage_d_gates --step D2 --from D1 \\
  --image path/to/D2.jpg --prev-sha <D1_sha256> \\
  --outer-roi 0.58,0.38,0.78,0.72 --side-roi 0.38,0.45,0.58,0.62 \\
  --out path/to/D2_gate.json
```
""",
            encoding="utf-8",
        )
        (outdir / "stage_e_glow_bubble_break.md").write_text(
            make_stage_e_prompt(selected), encoding="utf-8"
        )
        outputs.extend([
            "stage_b_one_hammer_no_person.md",
            "stage_c_scale_and_add_person.md",
            "stage_d_action_refinement.md",
            "stage_d_step_D0.md",
            "stage_d_step_D1.md",
            "stage_d_step_D2.md",
            "stage_d_step_D3.md",
            "stage_d_step_D4.md",
            "stage_d_GATES.md",
            "stage_e_glow_bubble_break.md",
        ])
    result = {
        "outdir": str(outdir),
        "candidate_count": len(candidates),
        "selected_candidate_id": selected.candidate_id if selected else None,
        "raster_selection_evidence": manifest["raster_selection_evidence"],
        "outputs": outputs,
        "image_realization": "NOT_RUN",
        "pixel_audit": "NOT_RUN",
    }
    (outdir / "packet_summary.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return result


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=Path("out/dense_hammer_bubble"))
    parser.add_argument("--select", type=str, default=None, help="Selected visible raster ID, e.g. C17")
    parser.add_argument("--bubble-scale", type=float, default=1.0)
    parser.add_argument("--hammer-scale", type=float, default=1.0)
    parser.add_argument("--person-to-hammer-scale", type=float, default=PERSON_TO_HAMMER_SCALE_DEFAULT,
                        help="Stage C hard lock: mini person full-body area / hammer area (default 1.0 = 1:1, 人變迷你)")
    parser.add_argument("--person-height-of-bubble", type=float, default=None,
                        help=argparse.SUPPRESS)  # removed; kept only to error if used
    parser.add_argument("--source-raster", type=Path, default=None)
    parser.add_argument("--roi", type=parse_roi, default=None, help="user-checked raster region x,y,width,height")
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        result = build_packet(
            outdir=args.outdir,
            selected_id=args.select,
            bubble_scale=args.bubble_scale,
            hammer_scale=args.hammer_scale,
            person_to_hammer_scale=(
                args.person_to_hammer_scale if args.person_height_of_bubble is None
                else (_raise_deprecated_person_bubble())
            ),
            source_raster=args.source_raster,
            roi=args.roi,
        )
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
