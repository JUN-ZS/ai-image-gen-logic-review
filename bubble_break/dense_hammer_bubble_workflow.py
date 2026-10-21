#!/usr/bin/env python3
"""Compile a dense hammer-around-one-bubble selection workflow.

This emits deterministic candidate metadata, an SVG geometry proxy, and staged
image prompts. It does not generate a raster image or claim pixel acceptance.
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
FACE_GAP_TO_HEAD_DIAMETER = 0.025
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
FACE_GAP = HEAD_DIAMETER * FACE_GAP_TO_HEAD_DIAMETER


@dataclass(frozen=True)
class HammerCandidate:
    candidate_id: str
    index: int
    radial_normal: V3
    front_face_normal: V3
    handle_direction: V3
    bubble_contact_anchor: V3
    glowing_face_center: V3
    handle_end: V3
    polar_deg_to_camera: float
    azimuth_deg: float
    projected_contact_x: float
    projected_contact_y: float
    projected_handle_x: float
    projected_handle_y: float
    head_diameter: float = HEAD_DIAMETER
    head_stub_length: float = HEAD_LENGTH
    handle_length: float = HANDLE_LENGTH
    handle_diameter: float = HANDLE_DIAMETER
    face_gap: float = FACE_GAP


def make_candidates(count: int = CANDIDATE_COUNT, seed: int = SEED) -> list[HammerCandidate]:
    """Sample distinct, irregular points on the visible spherical cap.

    Every candidate has an independent inward-facing circular end face; its
    handle runs outward from the rear of the head. These are proxy coordinates,
    not an image model's guaranteed pixel layout.
    """
    if count < 1:
        raise ValueError("候選數量必須至少為 1")
    rng = random.Random(seed)
    camera = CAMERA_DIRECTION
    right = CAMERA_RIGHT
    up = CAMERA_UP
    golden_angle = math.pi * (3.0 - math.sqrt(5.0))
    # Keep every shaft sufficiently oblique to the camera to remain readable.
    min_polar = math.radians(28.0)
    max_polar = math.radians(76.0)
    cos_min = math.cos(min_polar)
    cos_max = math.cos(max_polar)
    candidates: list[HammerCandidate] = []

    # Quasi-uniform but lightly jittered spherical-cap distribution. This is not
    # a rectangular grid; angle and azimuth are independently perturbed.
    for i in range(count):
        fraction = (i + 0.5) / count
        cos_polar = cos_min + fraction * (cos_max - cos_min)
        cos_polar = clamp(cos_polar + rng.uniform(-0.012, 0.012), cos_max, cos_min)
        polar = math.acos(cos_polar)
        azimuth = i * golden_angle + rng.uniform(-0.18, 0.18)
        tangent = add(mul(right, math.cos(azimuth)), mul(up, math.sin(azimuth)))
        radial = unit(add(mul(camera, math.cos(polar)), mul(tangent, math.sin(polar))))
        contact = mul(radial, BUBBLE_RADIUS)
        face_center = mul(radial, BUBBLE_RADIUS + FACE_GAP)
        # The front face points inward. The rear handle continues outward.
        front_face_normal = mul(radial, -1.0)
        handle_end = mul(radial, BUBBLE_RADIUS + FACE_GAP + HEAD_LENGTH + HANDLE_LENGTH)
        proxy_scale = 275.0 / BUBBLE_RADIUS
        projected_contact_x = 700.0 + proxy_scale * dot(contact, right)
        projected_contact_y = 600.0 - proxy_scale * dot(contact, up)
        projected_handle_x = 700.0 + proxy_scale * dot(handle_end, right)
        projected_handle_y = 600.0 - proxy_scale * dot(handle_end, up)
        candidates.append(
            HammerCandidate(
                candidate_id=f"C{i + 1:02d}",
                index=i,
                radial_normal=tuple(round(x, 8) for x in radial),
                front_face_normal=tuple(round(x, 8) for x in front_face_normal),
                handle_direction=tuple(round(x, 8) for x in radial),
                bubble_contact_anchor=tuple(round(x, 8) for x in contact),
                glowing_face_center=tuple(round(x, 8) for x in face_center),
                handle_end=tuple(round(x, 8) for x in handle_end),
                polar_deg_to_camera=round(math.degrees(polar), 4),
                azimuth_deg=round(math.degrees(azimuth) % 360.0, 4),
                projected_contact_x=round(projected_contact_x, 3),
                projected_contact_y=round(projected_contact_y, 3),
                projected_handle_x=round(projected_handle_x, 3),
                projected_handle_y=round(projected_handle_y, 3),
            )
        )
    return candidates


def candidate_by_id(candidates: Sequence[HammerCandidate], candidate_id: str) -> HammerCandidate:
    requested = candidate_id.strip().upper()
    for candidate in candidates:
        if candidate.candidate_id == requested:
            return candidate
    raise ValueError(
        f"未知候選編號 {candidate_id!r}；可用範圍為 C01–C{len(candidates):02d}"
    )


def fmt_vec(vector: Sequence[float]) -> str:
    return "(" + ", ".join(f"{value:.4f}" for value in vector) + ")"


def make_stage_a_prompt(candidates: Sequence[HammerCandidate]) -> str:
    ids = ", ".join(candidate.candidate_id for candidate in candidates)
    return f"""# STAGE A — DENSE HAMMER-TO-ONE-BUBBLE SELECTION ATLAS

Create ONE cinematic 16:9 image: a single large, pristine, translucent spherical
bubble dominates a dark, controlled background. Around it, densely crowd exactly
{len(candidates)} independent complete compact cylindrical-headed hammers, all
aimed inward toward this same bubble from varied 3D positions and directions.
This is a dense spatial swarm around one sphere, NOT a grid, tiled atlas, contact
sheet, or repeated product-stamp pattern.

EACH HAMMER MUST BE A COMPLETE, SEPARATE TOOL:
- One short solid cylindrical head, with a clean flat circular front striking
  face aimed toward a distinct point on the bubble.
- One thin, straight, long-enough handle attached concentrically to the REAR
  cap of that head. It extends outward, away from the sphere. Head and handle
  are one rigid axial assembly; no T-head, crossbar, extra arm, or side handle.
- Every shaft is independently traceable from the rear head joint to its own end.
  Never collapse several handles into one central post or hide them behind the
  same diagonal motif.
- The glowing surface is the front circular terminal face aimed at the bubble,
  not the rear cap, not the shaft joint, and not a luminous ring that makes the
  hammer appear grown out of the shell.

LOCKED STARTING PROPORTION GRAMMAR:
head diameter ≈ 8% of bubble diameter; head axial stub length ≈ 1.5 × head
diameter; handle length ≈ 3 × head stub length; handle diameter ≈ 1/10 of head
diameter. Keep this ratio consistent across all {len(candidates)} candidates.

All {len(candidates)} front faces glow with distinct readable white-hot or
cyan-white circular face emission and a restrained coloured rim. Aim every face
inward at the bubble surface from outside the shell. Faces may be just short of
contact or at first touch, but their round boundaries must remain legible. Each
hammer approaches the sphere; NO hammer grows out of the sphere and no handle
points through the bubble. The bubble remains intact.

DENSE BUT READABLE SPATIAL DESIGN:
- Irregular 3D distribution around the visible spherical volume, with varied
  depth, near/far perspective, radial angle, azimuth, projected shaft slope and
  small handle-roll/material variation. Use overlapping depth layers, but not
  2D overlaps that make a head or shaft ambiguous.
- No identical isometric copies; no uniform orientation; no regular rings,
  rows, columns, eight-by-six layout, tile grid, or cloned silhouettes.
- Every candidate has a unique visible ID: {ids}. Place a small high-contrast
  ID label beside its OUTER HANDLE END, never on the glowing face or head joint.
  Labels are navigation aids; prioritize clear object identity over typography.
- Fill the frame densely with the one sphere and its 24 tools, while leaving
  enough margin to distinguish complete head/handle assemblies.

STRICT EXCLUSIONS: no humans, no hands, no bodies, no extra bubbles, no bubble
cracks, no shards, no explosion, no huge spark spray, no motion blur hiding the
face, no hammer-to-hammer collision, no T-shaped hammers, no tiny centre pegs,
no detached or bent handles, no duplicate ID tags intentionally assigned to
different tools.

This image is only a candidate discovery atlas. Do not claim precise model-world
coordinates from text or from the accompanying SVG proxy. The actual generated
raster and its visible candidate are the authority for later selection.
"""


def selected_geometry_note(candidate: HammerCandidate, bubble_scale: float, hammer_scale: float) -> str:
    return f"""SELECTED ID: {candidate.candidate_id}
PROXY METADATA ONLY — NOT A CLAIM OF PIXEL-EXACT ALIGNMENT:
- approximate radial direction: {fmt_vec(candidate.radial_normal)}
- approximate inward striking-face normal: {fmt_vec(candidate.front_face_normal)}
- approximate outward handle direction: {fmt_vec(candidate.handle_direction)}
- proxy face center: {fmt_vec(candidate.glowing_face_center)}
Use the actual Stage-A raster's visible selected hammer as the geometric source,
not these proxy values. Do not move/flip the raster-visible face to agree with a
proxy vector. Only apply these user-authorized scale factors:
- bubble scale relative to Stage A: {bubble_scale:.3f}x
- selected hammer scale relative to Stage A: {hammer_scale:.3f}x
If either scale is not 1.0, preserve the selected contact's normalized location on
the spherical surface and document the intentional scale transform. Keep the
hammer's head and handle scale locked together.
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
        raster_info += f"User-confirmed raster ROI (x,y,width,height): {roi}.\n"
    raster_info += (
        "If this source raster/reference is not actually supplied to the image-editing "
        "model, STOP and request it; never make a fresh text-only reconstruction.\n"
    )
    return f"""# STAGE B — ISOLATE ONE REAL RASTER HAMMER, NO PERSON

Use the exact accepted Stage-A image as the image-to-image / inpainting reference.
Do not create a new bubble composition from text. Do not rebuild the selected
hammer from a 3D coordinate guess.

{raster_info}
{selected_geometry_note(candidate, bubble_scale, hammer_scale)}
Select the actual visible hammer labelled {candidate.candidate_id} in the source
raster. Keep its visible glowing FRONT CIRCULAR STRIKING FACE, head silhouette,
head-to-handle joint, handle direction, perspective and contact location as seen
in that raster. The raster wins over the proxy coordinate if they differ.

Remove every other hammer completely: all 23 non-selected heads, handles, glows,
labels, reflected ghosts and detached fragments disappear. Retain one bubble and
exactly one selected hammer. No person, hands, action pose, extra prop, cracks,
shards, or large explosion.

The short cylinder's flat glowing front face aims toward the sphere; the handle
attaches concentrically to the REAR cap and extends away from the sphere. No
flipping the hammer end-for-end, no handle pointing into/through the bubble, no
sideways handle, no detached ghost rod. Keep the face outline clear. Preserve the
starting proportions unless the stated scale factors require a deliberate change:
head stub Hs ≈ 1.5 × head diameter; handle L ≈ 3 × Hs; handle diameter ≈ 1/10
head diameter. With both scale factors 1.0, do not change scale at all.

Acceptance is judged against the source raster, not the SVG. If the chosen ID,
visible face position, handle direction, or contact location is uncertain, mark
the stage BLOCKED and ask for selection evidence; do not silently choose another.
"""


def make_stage_c_prompt(candidate: HammerCandidate, person_height_of_bubble: float) -> str:
    return f"""# STAGE C — ADD ONE PERSON AFTER THE TOOL IS LOCKED

Use the accepted Stage-B raster as the only image reference. The selected
{candidate.candidate_id} hammer and bubble already exist and must not be rebuilt.
Preserve the real raster-visible glowing face center, face direction, rear-cap
handle joint, handle length/diameter, and normalized bubble-contact location.

Add exactly one full human figure behind the rear end of the selected handle.
Default human height ≈ {person_height_of_bubble:.3f} × bubble diameter (adjustable).
Size the person's hands and body to the existing handle and bubble; do not enlarge
the tool just to make it easier to grip. The person stands/leans naturally on the
outside of the bubble, both hands visibly wrapping around the same existing
handle with plausible wrist, elbow and shoulder alignment. Do not let the body,
arms or hands hide the glowing face or replace any part of the handle.

All other 23 hammers stay absent. Keep the bubble intact and keep effects minimal:
no explosion, no shards, no major shell cracks yet. This is an attachment/scale
proof, not a spectacle frame.
"""


def make_stage_d_prompt(candidate: HammerCandidate) -> str:
    return f"""# STAGE D — ACTION REFINEMENT WITH RASTER GEOMETRY LOCK

Start from the accepted Stage-C image. Improve the person's action only:
weight transfer, foot placement, shoulder/hip rotation, grip tension, controlled
wind-up and believable follow-through. Make the pose dynamic and readable rather
than a static stand.

LOCK the selected {candidate.candidate_id} hammer as one rigid axial assembly.
Do not move or flip the glowing front circular face, do not move its spherical
contact point except for approved action travel, and do not break or bend the
rear-cap handle joint. The handle remains behind the head and points away from
the bubble; the face remains directed toward the bubble. Keep the person gripping
that same handle. No other hammers return. Keep at least one clean readable frame
with the full glowing face boundary and head-handle joint visible.
"""


def make_stage_e_prompt(candidate: HammerCandidate) -> str:
    return f"""# STAGE E — GLOWING FACE → BUBBLE BREAK EFFECT

Use the accepted Stage-D frame as the reference. Do not recompose or replace the
chosen {candidate.candidate_id} hammer, person, or bubble. Preserve their actual
raster geometry and relative proportions.

Build the effect from the selected hammer's glowing FRONT CIRCULAR FACE and its
specific bubble contact point: bright coherent face-core emission, a tight rim
halo, localized energy transfer, concentric ripples along the translucent shell,
then radial fractures that visibly originate at that point. For the peak spectacle
frame, the bubble shell ruptures outward into curved luminous shards and a large
shock ring, with cinematic depth and directional debris.

Provide at least one clean contact frame before maximum bloom. In the clean frame,
the circular face edge, bubble contact point, intact rear-handle connection and
the person's grip remain inspectable. Sparks and bloom must never obscure the
contact seam in every frame. The shell must visibly break; sparks around an intact
bubble alone are not enough. Remove every unselected hammer and every ghost copy.
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
        '<text x="36" y="42" fill="#ffffff" font-family="sans-serif" font-size="25">Dense hammer / one-bubble candidate proxy — NOT raster evidence</text>',
        f'<circle cx="{cx}" cy="{cy}" r="{sphere_px}" fill="#92ddf7" fill-opacity="0.13" stroke="#aeeeff" stroke-width="3"/>',
    ]
    for candidate in candidates:
        radial = candidate.radial_normal
        anchor = candidate.bubble_contact_anchor
        face = candidate.glowing_face_center
        end = candidate.handle_end
        px, py = project_point(anchor, cx, cy, sphere_px)
        fx, fy = project_point(face, cx, cy, sphere_px)
        ex, ey = project_point(end, cx, cy, sphere_px)
        # Head axial segment connects face to its rear cap; handle leaves its rear.
        face_to_rear = mul(radial, HEAD_LENGTH)
        rear = add(face, face_to_rear)
        rx, ry = project_point(rear, cx, cy, sphere_px)
        selected = candidate.candidate_id == selected_id
        color = "#fff6ad" if selected else "#6df5ff"
        width_face = 4 if selected else 2.2
        # Distinct components: thin shaft first, short head second, face marker last.
        elements.extend([
            f'<line x1="{rx:.2f}" y1="{ry:.2f}" x2="{ex:.2f}" y2="{ey:.2f}" stroke="#d5e3ed" stroke-width="{HANDLE_DIAMETER * scale:.2f}" stroke-linecap="round"/>',
            f'<line x1="{fx:.2f}" y1="{fy:.2f}" x2="{rx:.2f}" y2="{ry:.2f}" stroke="#afc4d3" stroke-width="{HEAD_DIAMETER * scale:.2f}" stroke-linecap="round"/>',
            f'<circle cx="{fx:.2f}" cy="{fy:.2f}" r="{HEAD_DIAMETER * scale * 0.28:.2f}" fill="{color}" fill-opacity="0.30"/>',
            f'<circle cx="{fx:.2f}" cy="{fy:.2f}" r="{HEAD_DIAMETER * scale * 0.18:.2f}" fill="{color}" stroke="#ffffff" stroke-width="{width_face}"/>',
            f'<text x="{ex + 7:.2f}" y="{ey - 3:.2f}" fill="{color}" font-family="sans-serif" font-size="16" font-weight="bold">{escape(candidate.candidate_id)}</text>',
        ])
    if selected_id:
        elements.append(f'<text x="36" y="1160" fill="#fff6ad" font-family="sans-serif" font-size="20">Selected {escape(selected_id)} — selected image raster remains authoritative</text>')
    else:
        elements.append('<text x="36" y="1160" fill="#ffffff" font-family="sans-serif" font-size="19">24 candidates — proxy only. Confirm selection from a real generated raster.</text>')
    elements.append("</svg>")
    return "\n".join(elements) + "\n"


def build_packet(
    outdir: Path,
    selected_id: str | None = None,
    bubble_scale: float = 1.0,
    hammer_scale: float = 1.0,
    person_height_of_bubble: float = 0.65,
    source_raster: Path | None = None,
    roi: tuple[int, int, int, int] | None = None,
) -> dict[str, object]:
    for name, value in (
        ("bubble_scale", bubble_scale),
        ("hammer_scale", hammer_scale),
        ("person_height_of_bubble", person_height_of_bubble),
    ):
        if not math.isfinite(value) or value <= 0:
            raise ValueError(f"{name} 必須是正的有限數值")
    if roi and not source_raster:
        raise ValueError("--roi 必須與 --source-raster 一起使用")
    if source_raster and not source_raster.is_file():
        raise ValueError(f"找不到來源 Stage-A 圖片：{source_raster}")
    candidates = make_candidates()
    selected = candidate_by_id(candidates, selected_id) if selected_id else None
    raster_sha = None
    if source_raster:
        raster_sha = hashlib.sha256(source_raster.read_bytes()).hexdigest()

    outdir.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, object] = {
        "schema_version": 1,
        "workflow": "dense-hammer-bubble-pick",
        "stage_a_candidate_count": len(candidates),
        "bubble_diameter_proxy_units": BUBBLE_DIAMETER,
        "hammer_proportions": {
            "head_diameter_over_bubble_diameter": HEAD_DIAMETER_RATIO,
            "head_stub_length_over_head_diameter": HEAD_LENGTH_TO_DIAMETER,
            "handle_length_over_head_stub_length": HANDLE_LENGTH_TO_HEAD_LENGTH,
            "handle_diameter_over_head_diameter": HANDLE_DIAMETER_TO_HEAD_DIAMETER,
            "glowing_face_gap_over_head_diameter": FACE_GAP_TO_HEAD_DIAMETER,
        },
        "selected_candidate_id": selected.candidate_id if selected else None,
        "scale_changes": {
            "bubble_scale": bubble_scale,
            "hammer_scale": hammer_scale,
            "person_height_over_bubble_diameter": person_height_of_bubble,
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
    (outdir / "dense_hammer_candidate_proxy.svg").write_text(
        make_svg(candidates, selected.candidate_id if selected else None), encoding="utf-8"
    )
    (outdir / "stage_a_dense_hammer_atlas.md").write_text(
        make_stage_a_prompt(candidates), encoding="utf-8"
    )
    outputs = [
        "candidate_manifest.json",
        "dense_hammer_candidate_proxy.svg",
        "stage_a_dense_hammer_atlas.md",
    ]
    if selected:
        (outdir / "stage_b_one_hammer_no_person.md").write_text(
            make_stage_b_prompt(selected, bubble_scale, hammer_scale, raster_sha, roi),
            encoding="utf-8",
        )
        (outdir / "stage_c_add_person.md").write_text(
            make_stage_c_prompt(selected, person_height_of_bubble), encoding="utf-8"
        )
        (outdir / "stage_d_action_refinement.md").write_text(
            make_stage_d_prompt(selected), encoding="utf-8"
        )
        (outdir / "stage_e_glow_bubble_break.md").write_text(
            make_stage_e_prompt(selected), encoding="utf-8"
        )
        outputs.extend([
            "stage_b_one_hammer_no_person.md",
            "stage_c_add_person.md",
            "stage_d_action_refinement.md",
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
    parser.add_argument("--select", type=str, default=None, help="Selected raster candidate, e.g. C17")
    parser.add_argument("--bubble-scale", type=float, default=1.0, help="Bubble scale relative to Stage A")
    parser.add_argument("--hammer-scale", type=float, default=1.0, help="Selected hammer scale relative to Stage A")
    parser.add_argument("--person-height-of-bubble", type=float, default=0.65, help="Person height / bubble diameter")
    parser.add_argument("--source-raster", type=Path, default=None, help="Actual Stage-A raster file used as reference")
    parser.add_argument("--roi", type=parse_roi, default=None, help="User-checked selected hammer region: x,y,width,height")
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        result = build_packet(
            outdir=args.outdir,
            selected_id=args.select,
            bubble_scale=args.bubble_scale,
            hammer_scale=args.hammer_scale,
            person_height_of_bubble=args.person_height_of_bubble,
            source_raster=args.source_raster,
            roi=args.roi,
        )
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
