#!/usr/bin/env python3
"""Rigid-body contract for two T-hammers colliding strike-face to strike-face.

This module deliberately separates:
1. prompt compilation (what an image model is asked to depict),
2. geometric evidence validation (what an estimator/annotator measured), and
3. raster approval (which remains NOT_VERIFIED unless evidence is attached).

It never treats text similarity, background NCC, or a bright pixel as proof of contact.
"""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable


Vec3 = tuple[float, float, float]

CAMERA_VIEWS: tuple[str, ...] = (
    "three-quarter side view, both strike faces and their gap clearly visible",
    "near-profile view along the collision axis, show the two end-face planes rather than the head cheeks",
    "low three-quarter angle, camera below the two heads, preserve visible separation/contact point P",
    "high three-quarter angle, both head axes and both handle attachments readable",
    "reverse-side three-quarter view, maintain the same left/right tool identities and collision axis",
    "tight macro view of the opposed end faces at P, include enough head material to distinguish face from cheek",
    "wide environmental view with both full T-shaped tools, both operators/hands if present, and clear collision geometry",
    "telephoto side view compressing depth while keeping the end-face plane and no-gap state legible",
    "over-shoulder view from tool A's operator toward tool B; do not hide either strike face",
    "over-shoulder view from tool B's operator toward tool A; do not hide either strike face",
    "slightly canted cinematic angle with the contact normal still visually recoverable",
    "orthographic-like technical cinema view, minimal perspective ambiguity around P",
)


@dataclass(frozen=True)
class HammerRigidBody:
    tool_id: str
    head_shape: str
    strike_face: str
    strike_face_normal: Vec3
    head_axis: Vec3
    handle_axis: Vec3
    handle_joint: str
    locked_material_identity: str


@dataclass(frozen=True)
class DualHammerCollisionContract:
    contract_id: str
    interaction: str
    tool_a: HammerRigidBody
    tool_b: HammerRigidBody
    approach_axis: Vec3
    first_contact_point_name: str
    allowed_contact_surfaces: tuple[str, ...]
    forbidden_contact_surfaces: tuple[str, ...]
    pre_far_gap_min: float
    pre_near_gap_min: float
    pre_near_gap_max: float
    contact_gap_abs_max: float
    max_face_center_lateral_offset: float
    max_normal_error_degrees: float
    max_handle_head_axis_dot_abs: float

    def validate_definition(self) -> list[str]:
        errors: list[str] = []
        if self.tool_a.tool_id == self.tool_b.tool_id:
            errors.append("tool IDs must be different")
        if self.allowed_contact_surfaces != ("END_FACE_TO_END_FACE",):
            errors.append("only END_FACE_TO_END_FACE is allowed as first contact")
        if "CHEEK" not in self.forbidden_contact_surfaces:
            errors.append("CHEEK contact must be explicitly forbidden")
        for tool in (self.tool_a, self.tool_b):
            if _norm(tool.strike_face_normal) == 0 or _norm(tool.head_axis) == 0 or _norm(tool.handle_axis) == 0:
                errors.append(f"{tool.tool_id}: axis/normal vectors must be nonzero")
            if abs(_dot(_unit(tool.head_axis), _unit(tool.handle_axis))) > self.max_handle_head_axis_dot_abs:
                errors.append(f"{tool.tool_id}: handle must be transverse to the hammer head axis")
            if abs(_dot(_unit(tool.strike_face_normal), _unit(tool.head_axis))) < math.cos(math.radians(15)):
                errors.append(f"{tool.tool_id}: strike-face normal must align with the head's end-face axis")
        n_dot = _dot(_unit(self.tool_a.strike_face_normal), _unit(self.tool_b.strike_face_normal))
        max_dot = -math.cos(math.radians(self.max_normal_error_degrees))
        if n_dot > max_dot:
            errors.append("default strike-face normals must oppose each other")
        return errors


def default_dual_t_hammer_contract() -> DualHammerCollisionContract:
    return DualHammerCollisionContract(
        contract_id="DUAL_T_HAMMER_END_FACE_IMPACT_V1",
        interaction="two distinct T-shaped hammers approach one another and collide on their actual opposing strike end-faces",
        tool_a=HammerRigidBody(
            tool_id="HAMMER_A",
            head_shape="one transverse T-hammer head/bar with two identifiable end faces",
            strike_face="HAMMER_A inward-facing end face (not the cylindrical cheek or handle joint)",
            strike_face_normal=(1.0, 0.0, 0.0),
            head_axis=(1.0, 0.0, 0.0),
            handle_axis=(0.0, 1.0, 0.0),
            handle_joint="single handle fixed at the center of the head, transverse to head axis",
            locked_material_identity="matte dark steel, stable head length/diameter and one fixed handle",
        ),
        tool_b=HammerRigidBody(
            tool_id="HAMMER_B",
            head_shape="one transverse T-hammer head/bar with two identifiable end faces",
            strike_face="HAMMER_B inward-facing end face (not the cylindrical cheek or handle joint)",
            strike_face_normal=(-1.0, 0.0, 0.0),
            head_axis=(-1.0, 0.0, 0.0),
            handle_axis=(0.0, -1.0, 0.0),
            handle_joint="single handle fixed at the center of the head, transverse to head axis",
            locked_material_identity="contrasting but consistent steel finish; stable head length/diameter and one fixed handle",
        ),
        approach_axis=(1.0, 0.0, 0.0),
        first_contact_point_name="P",
        allowed_contact_surfaces=("END_FACE_TO_END_FACE",),
        forbidden_contact_surfaces=("CHEEK", "HANDLE", "SHAFT", "HANDLE_JOINT", "OTHER"),
        pre_far_gap_min=80.0,
        pre_near_gap_min=8.0,
        pre_near_gap_max=60.0,
        contact_gap_abs_max=2.0,
        max_face_center_lateral_offset=0.18,
        max_normal_error_degrees=15.0,
        max_handle_head_axis_dot_abs=0.25,
    )


def _dot(a: Vec3, b: Vec3) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _norm(v: Vec3) -> float:
    return math.sqrt(_dot(v, v))


def _unit(v: Vec3) -> Vec3:
    n = _norm(v)
    if n < 1e-9:
        return (0.0, 0.0, 0.0)
    return (v[0] / n, v[1] / n, v[2] / n)


def _vec(raw: Any, key: str) -> Vec3:
    if not isinstance(raw, (list, tuple)) or len(raw) != 3:
        raise ValueError(f"{key} must be a 3-vector [x,y,z]")
    v = tuple(float(x) for x in raw)
    if not all(math.isfinite(x) for x in v):
        raise ValueError(f"{key} must contain finite numbers")
    return v  # type: ignore[return-value]


def validate_collision_evidence(
    evidence: dict[str, Any],
    contract: DualHammerCollisionContract | None = None,
) -> dict[str, Any]:
    """Validate structured geometry evidence from a calibrated vision model or human annotator.

    Evidence schema:
      stage: PRE_FAR | PRE_NEAR | FIRST_CONTACT | REACTION | RECOIL
      contact_surface: END_FACE_TO_END_FACE | CHEEK | HANDLE | SHAFT | OTHER | NONE
      signed_gap: signed head-to-head face gap in normalized units (positive=apart)
      face_normal_a / face_normal_b: face outward unit normals
      face_center_a / face_center_b: end-face centers, normalized image/world coordinates
      contact_point: detected intersection/contact location (required for FIRST_CONTACT)
      contact_point_on_face_a / contact_point_on_face_b: booleans from segmenter/annotator
      tool_a_present / tool_b_present / separate_handles: booleans from instance segmentation
      evidence_source: named detector/model or HUMAN_REVIEW
    """
    c = contract or default_dual_t_hammer_contract()
    errors = c.validate_definition()
    required = (
        "stage", "contact_surface", "signed_gap",
        "face_normal_a", "face_normal_b",
        "face_center_a", "face_center_b",
        "tool_a_present", "tool_b_present", "separate_handles",
        "evidence_source",
    )
    missing = [k for k in required if k not in evidence]
    errors.extend(f"missing evidence field: {k}" for k in missing)
    if missing:
        return {
            "contract_id": c.contract_id,
            "accepted": False,
            "status": "BLOCKED_MISSING_GEOMETRY_EVIDENCE",
            "errors": errors,
            "visual_acceptance_status": "NOT_VERIFIED",
        }

    try:
        stage = str(evidence["stage"]).upper()
        surface = str(evidence["contact_surface"]).upper()
        gap = float(evidence["signed_gap"])
        na = _unit(_vec(evidence["face_normal_a"], "face_normal_a"))
        nb = _unit(_vec(evidence["face_normal_b"], "face_normal_b"))
        ca = _vec(evidence["face_center_a"], "face_center_a")
        cb = _vec(evidence["face_center_b"], "face_center_b")
        if not math.isfinite(gap):
            raise ValueError("signed_gap must be finite")
    except (TypeError, ValueError) as exc:
        return {
            "contract_id": c.contract_id,
            "accepted": False,
            "status": "BLOCKED_INVALID_GEOMETRY_EVIDENCE",
            "errors": errors + [str(exc)],
            "visual_acceptance_status": "NOT_VERIFIED",
        }

    if not evidence["tool_a_present"] or not evidence["tool_b_present"]:
        errors.append("both distinct hammer instances must be visibly present")
    if not evidence["separate_handles"]:
        errors.append("each hammer must retain its own distinct handle")
    if surface not in c.allowed_contact_surfaces:
        if stage in ("FIRST_CONTACT", "REACTION"):
            errors.append(f"forbidden first-contact surface: {surface}")
    if stage in ("PRE_FAR", "PRE_NEAR", "RECOIL") and surface not in ("NONE", "NO_CONTACT"):
        errors.append(f"{stage} must remain visibly separated; detected contact surface={surface}")

    normal_dot = max(-1.0, min(1.0, _dot(na, nb)))
    normal_error = math.degrees(math.acos(max(-1.0, min(1.0, -normal_dot))))
    lateral_delta = tuple(cb[i] - ca[i] for i in range(3))
    signed_along_axis = abs(_dot(lateral_delta, _unit(c.approach_axis)))
    lateral_vec = tuple(lateral_delta[i] - _dot(lateral_delta, _unit(c.approach_axis)) * _unit(c.approach_axis)[i] for i in range(3))
    lateral_offset = _norm(lateral_vec)

    if stage in ("PRE_FAR", "PRE_NEAR", "FIRST_CONTACT", "REACTION", "RECOIL"):
        # Normals must face one another before considering any raster a physically valid collision.
        if normal_error > c.max_normal_error_degrees:
            errors.append(f"end-face normals are not opposing (error={normal_error:.2f}° > {c.max_normal_error_degrees:.2f}°)")
        if lateral_offset > c.max_face_center_lateral_offset:
            errors.append(f"end-face centers miss laterally (offset={lateral_offset:.4f} > {c.max_face_center_lateral_offset:.4f})")

    if stage == "PRE_FAR" and gap < c.pre_far_gap_min:
        errors.append(f"PRE_FAR requires a large positive gap >= {c.pre_far_gap_min}; got {gap:.4f}")
    elif stage == "PRE_NEAR" and not (c.pre_near_gap_min <= gap <= c.pre_near_gap_max):
        errors.append(f"PRE_NEAR requires positive shrinking gap [{c.pre_near_gap_min},{c.pre_near_gap_max}]; got {gap:.4f}")
    elif stage == "FIRST_CONTACT":
        if abs(gap) > c.contact_gap_abs_max:
            errors.append(f"FIRST_CONTACT requires zero gap within ±{c.contact_gap_abs_max}; got {gap:.4f}")
        if surface != "END_FACE_TO_END_FACE":
            errors.append("FIRST_CONTACT must be end-face to end-face; end-face/cheek does NOT count")
        for key in ("contact_point", "contact_point_on_face_a", "contact_point_on_face_b"):
            if key not in evidence:
                errors.append(f"FIRST_CONTACT missing {key}")
        if not evidence.get("contact_point_on_face_a", False) or not evidence.get("contact_point_on_face_b", False):
            errors.append("point P must lie on both strike faces")
    elif stage == "REACTION" and surface not in ("END_FACE_TO_END_FACE", "NONE", "NO_CONTACT"):
        errors.append(f"REACTION contains forbidden contact surface={surface}")
    elif stage == "RECOIL" and gap <= 0:
        errors.append(f"RECOIL must show the tools separating again; gap must be positive, got {gap:.4f}")

    accepted = not errors
    return {
        "contract_id": c.contract_id,
        "accepted": accepted,
        "status": "GEOMETRY_EVIDENCE_PASS" if accepted else "BLOCKED_GEOMETRY_CONTRACT_FAIL",
        "visual_acceptance_status": "GEOMETRY_EVIDENCE_VERIFIED" if accepted else "NOT_VERIFIED",
        "evidence_source": evidence.get("evidence_source"),
        "metrics": {
            "normal_dot": round(normal_dot, 6),
            "normal_error_degrees": round(normal_error, 4),
            "signed_gap": gap,
            "face_center_lateral_offset": round(lateral_offset, 6),
            "face_center_distance_along_approach": round(signed_along_axis, 6),
        },
        "errors": errors,
    }


def compile_dual_hammer_prompt(
    stage: str,
    *,
    camera_view: str = CAMERA_VIEWS[0],
    variant_index: int = 0,
    contract: DualHammerCollisionContract | None = None,
) -> str:
    """One full-frame prompt. Different calls/variants produce separate images, never a grid/contact-sheet."""
    c = contract or default_dual_t_hammer_contract()
    errors = c.validate_definition()
    if errors:
        raise ValueError("Invalid collision contract: " + "; ".join(errors))
    phase = stage.strip().upper()
    states = {
        "PRE_FAR": (
            "Both T-hammers are clearly separated by a large empty air gap. Their actual flat striking end faces "
            "are visible and already aimed toward one another. Neither tool touches the other."
        ),
        "PRE_NEAR": (
            "The same two T-hammers have moved closer on the same collision axis. Keep a clearly positive, smaller "
            "air gap between the two flat end faces. No cheek/shaft/handle contact and no impact glow yet."
        ),
        "FIRST_CONTACT": (
            "The two inward-facing flat STRIKING END FACES meet for the first time at one small marked physical "
            "point P. The face planes oppose one another, the gap is exactly zero, and P lies on BOTH flat end-face "
            "disks. The cylindrical head cheeks remain separate from each other; handles and shafts do not collide. "
            "Make the actual end-face-to-end-face interface legible from the chosen camera view; no fake glow-only contact."
        ),
        "REACTION": (
            "Impact energy and a restrained contact flash originate ONLY at the already established point P on "
            "the face-to-face interface. Preserve both head identities and their opposing end-face planes; do not "
            "move the contact to a cheek, shaft, handle, or handle joint."
        ),
        "RECOIL": (
            "Both T-hammers recoil apart after the strike. The gap becomes positive again. Preserve the same two "
            "tools, head dimensions, individual handles and collision axis; the impact trace remains localized to P."
        ),
    }
    if phase not in states:
        raise ValueError(f"Unknown stage {stage!r}; use {tuple(states)}")
    tool_a = c.tool_a
    tool_b = c.tool_b
    return f"""# DUAL T-HAMMER RIGID-BODY COLLISION — {phase} — VIEW {variant_index:02d}

Create ONE independent cinematic 16:9 full-frame image, not a grid, collage, storyboard sheet, or product layout.
This is a two-tool physical interaction, NOT a single hammer planted into a bubble.

## LOCKED TOOL INSTANCES
- {tool_a.tool_id}: {tool_a.head_shape}; strike face = {tool_a.strike_face}; outward strike-face normal = {tool_a.strike_face_normal}.
- {tool_b.tool_id}: {tool_b.head_shape}; strike face = {tool_b.strike_face}; outward strike-face normal = {tool_b.strike_face_normal}.
- Each tool has its OWN head and exactly one attached handle. The handles attach at the head center and are transverse to the head's strike axis.
- Keep tool A and tool B independently identifiable. Never merge them into one H-shape, one long shaft, a planted tool, or two aligned handle shafts.
- The only intended first collision is FLAT END FACE A against FLAT END FACE B. An end face is the planar terminal striking surface, not the cylindrical side/cheek of the head.
- At FIRST_CONTACT, face normals are opposing (within {c.max_normal_error_degrees} degrees), lateral face-center offset is at most {c.max_face_center_lateral_offset}, gap is zero within ±{c.contact_gap_abs_max}, and point P belongs to both end faces.
- Explicitly reject head-cheek-to-cheek, face-to-cheek, shaft-to-shaft, handle-to-handle, handle-to-head, or any contact between non-striking surfaces.
- Do not add a protective bubble or a third object as the collision target. No extra hammer, duplicate tool, floating detached head, or new handle.

## FRAME PHYSICS
{states[phase]}

## CAMERA VIEW
{camera_view}. Change composition/camera view only; never change the contact-surface contract, either tool's geometry, the head/handle joint, or the physical stage state. Keep both end-face planes and point P readable, not occluded by hands, bloom, sparks, or motion blur.

## CREATIVITY WITHIN THE CONTRACT
Make this variant visually distinct through camera placement, lens perspective, lighting, background, operator pose, material micro-detail, and controlled motion cues—not by changing the rigid-body contact geometry. Variant index {variant_index}. The selected view must remain a single coherent physical instant with consistent shadows, scale and perspective.

## NEGATIVE CONSTRAINTS
no single planted hammer; no bubble as target; no H-vs-H visual shorthand that hides which surfaces meet; no contact at the cheeks; no side-swipe; no handle/shaft contact; no false zero-gap caused by glow; no intersecting solids; no impossible bent head; no topology replacement; no mirrored duplicate; no text labels covering P.
"""


def compile_camera_matrix(stage: str, views: Iterable[str] = CAMERA_VIEWS) -> list[dict[str, str]]:
    """Generate a non-repeating prompt set of independent images with a shared physical contract."""
    return [
        {"variant_id": f"{stage.strip().upper()}_V{i:02d}", "camera_view": view,
         "prompt": compile_dual_hammer_prompt(stage, camera_view=view, variant_index=i)}
        for i, view in enumerate(views, start=1)
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=Path("out/dual_t_hammer_collision"))
    parser.add_argument("--stage", choices=("PRE_FAR", "PRE_NEAR", "FIRST_CONTACT", "REACTION", "RECOIL"), default=None)
    parser.add_argument("--camera-count", type=int, default=12)
    args = parser.parse_args(argv)
    if not 1 <= args.camera_count <= len(CAMERA_VIEWS):
        parser.error(f"--camera-count must be 1..{len(CAMERA_VIEWS)}")
    args.outdir.mkdir(parents=True, exist_ok=True)
    c = default_dual_t_hammer_contract()
    (args.outdir / "DUAL_T_HAMMER_COLLISION_CONTRACT.json").write_text(
        json.dumps(asdict(c), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    manifest: dict[str, Any] = {
        "contract_id": c.contract_id,
        "stage_prompts": {},
        "camera_variants_per_stage": args.camera_count,
        "visual_acceptance_status": "NOT_VERIFIED",
        "generation_backend_status": "NOT_CONNECTED_BY_THIS_MODULE",
        "note": "Prompts/geometry contract only; a raster is not approved without geometry evidence + visual review.",
    }
    stages = (args.stage,) if args.stage else ("PRE_FAR", "PRE_NEAR", "FIRST_CONTACT", "REACTION", "RECOIL")
    for stage in stages:
        records = compile_camera_matrix(stage, CAMERA_VIEWS[:args.camera_count])
        target = args.outdir / f"{stage}_camera_matrix.json"
        target.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        manifest["stage_prompts"][stage] = {"path": str(target), "count": len(records)}
    (args.outdir / "DUAL_T_HAMMER_PROMPT_MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"outdir": str(args.outdir), **manifest}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
