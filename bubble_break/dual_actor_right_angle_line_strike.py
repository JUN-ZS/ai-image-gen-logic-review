"""Geometry gate for a right-angle, line-shaped striker collision.

This checks world-space direction vectors only. It cannot prove that an image
actually shows the facets touching; rendered images still need a pixel audit.
Run directly with: python dual_actor_right_angle_line_strike.py
"""
from __future__ import annotations

import math
from typing import Dict, Sequence

Vector3 = Sequence[float]


def unit(v: Vector3) -> tuple[float, float, float]:
    if len(v) != 3:
        raise ValueError("方向向量必須是 3D 向量")
    length = math.sqrt(sum(float(x) * float(x) for x in v))
    if length == 0:
        raise ValueError("方向向量不可為零向量")
    return tuple(float(x) / length for x in v)  # type: ignore[return-value]


def dot(a: Vector3, b: Vector3) -> float:
    return sum(a[i] * b[i] for i in range(3))


def angle_deg(cosine: float) -> float:
    return math.degrees(math.acos(max(-1.0, min(1.0, cosine))))


def check_crossed_face_contact(
    axis_a: Vector3,
    axis_b: Vector3,
    face_normal_a: Vector3,
    face_normal_b: Vector3,
    axis_tolerance_deg: float = 5.0,
    face_tolerance_deg: float = 8.0,
) -> Dict[str, float | bool]:
    """Pass only if striker axes cross at 90° and planar faces oppose.

    The striker axes are undirected: parallel and anti-parallel both represent
    a coaxial 0° relationship. Face normals are outward normals; face-to-face
    contact requires them to oppose (180° apart).
    """
    if not 0 <= axis_tolerance_deg < 90:
        raise ValueError("axis_tolerance_deg 必須介於 [0, 90)")
    if not 0 <= face_tolerance_deg < 90:
        raise ValueError("face_tolerance_deg 必須介於 [0, 90)")

    a = unit(axis_a)
    b = unit(axis_b)
    f1 = unit(face_normal_a)
    f2 = unit(face_normal_b)

    axis_angle = angle_deg(abs(dot(a, b)))
    axis_error = abs(axis_angle - 90.0)
    face_opposition_error = angle_deg(-dot(f1, f2))

    axis_pass = axis_error <= axis_tolerance_deg
    face_pass = face_opposition_error <= face_tolerance_deg
    return {
        "axis_angle_deg": round(axis_angle, 6),
        "axis_error_from_90_deg": round(axis_error, 6),
        "face_opposition_error_deg": round(face_opposition_error, 6),
        "axis_90_pass": axis_pass,
        "face_opposition_pass": face_pass,
        "geometry_pass": axis_pass and face_pass,
    }


def self_test() -> None:
    correct = check_crossed_face_contact(
        axis_a=(1, 0, 0),
        axis_b=(0, 1, 0),
        face_normal_a=(0, 0, 1),
        face_normal_b=(0, 0, -1),
    )
    assert correct["geometry_pass"] is True, correct

    # Same 90° axes, but face normals point the same way: reject.
    inverse_face = check_crossed_face_contact(
        axis_a=(1, 0, 0),
        axis_b=(0, 1, 0),
        face_normal_a=(0, 0, 1),
        face_normal_b=(0, 0, 1),
    )
    assert inverse_face["axis_90_pass"] is True, inverse_face
    assert inverse_face["face_opposition_pass"] is False, inverse_face
    assert inverse_face["geometry_pass"] is False, inverse_face

    # Correctly opposed facets do not rescue coaxial rods.
    coaxial = check_crossed_face_contact(
        axis_a=(1, 0, 0),
        axis_b=(-1, 0, 0),
        face_normal_a=(0, 0, 1),
        face_normal_b=(0, 0, -1),
    )
    assert coaxial["axis_90_pass"] is False, coaxial
    assert coaxial["geometry_pass"] is False, coaxial

    # A 45° axis crossing must fail the 90° gate.
    oblique = check_crossed_face_contact(
        axis_a=(1, 0, 0),
        axis_b=(1, 1, 0),
        face_normal_a=(0, 0, 1),
        face_normal_b=(0, 0, -1),
    )
    assert oblique["axis_90_pass"] is False, oblique
    assert oblique["geometry_pass"] is False, oblique

    print("PASS correct right-angle face contact:", correct)
    print("PASS rejected inverse-face control:", inverse_face)
    print("PASS rejected coaxial control:", coaxial)
    print("PASS rejected 45-degree-axis control:", oblique)


if __name__ == "__main__":
    self_test()
