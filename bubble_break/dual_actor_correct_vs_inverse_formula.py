#!/usr/bin/env python3
"""Dual-actor correct vs inverse-face strike formula (geometry only).

Does not generate images. IMAGE_REALIZATION and PIXEL_AUDIT stay NOT_RUN until
raster review. Camera is a free parameter; contact PASS depends only on f·(-n).
"""
from __future__ import annotations
import argparse, json, math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

V = Tuple[float, float, float]
DEFAULT_TOL_DEG = 8.0

def _dot(a: V, b: V) -> float:
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def _len(a: V) -> float:
    return math.sqrt(_dot(a, a))

def unit(a: V) -> V:
    d = _len(a)
    if d < 1e-12:
        raise ValueError("zero vector")
    return (a[0]/d, a[1]/d, a[2]/d)

def check_contact(
    n: Sequence[float],
    f: Sequence[float],
    tolerance_deg: float = DEFAULT_TOL_DEG,
) -> Dict[str, object]:
    """PASS iff f · (-n) >= cos(theta_tol) after unit-normalization."""
    nu = unit(tuple(float(x) for x in n))  # type: ignore[arg-type]
    fu = unit(tuple(float(x) for x in f))  # type: ignore[arg-type]
    alignment = _dot(fu, (-nu[0], -nu[1], -nu[2]))
    threshold = math.cos(math.radians(tolerance_deg))
    return {
        "n": [round(x, 6) for x in nu],
        "f": [round(x, 6) for x in fu],
        "alignment": round(alignment, 6),
        "threshold": round(threshold, 6),
        "tolerance_deg": tolerance_deg,
        "pass": alignment >= threshold,
    }

@dataclass(frozen=True)
class ActorRole:
    actor_id: str
    height: str  # airborne | ground_low
    swing: str
    face_mode: str  # CORRECT | INVERSE_NEGATIVE_CONTROL
    must_pass: bool

@dataclass(frozen=True)
class Trial:
    trial_id: str
    n: V
    correct_actor: str
    inverse_actor: str
    camera: str
    actors: Tuple[ActorRole, ActorRole]
    checks: Dict[str, Dict[str, object]]
    prompt_lock: str
    audit: Dict[str, str]

# Variable axes for a real test set (not one repeated stamp)
HEIGHTS = ("airborne", "ground_low")
SWINGS_AIR = ("dive_overhead", "spin_slash", "falling_chop")
SWINGS_GROUND = ("low_rising_pick", "ground_sweep", "kneel_thrust")
CAMERAS = (
    "low_hero_24mm",
    "high_crane_35mm",
    "side_profile_85mm",
    "three_quarter_35mm",
    "dutch_roll_32mm",
    "ots_28mm",
)
# Unit impact normals to sample
NORMALS: Tuple[V, ...] = (
    (1.0, 0.0, 0.0),
    (-1.0, 0.0, 0.0),
    (0.0, 0.0, 1.0),
    (0.0, 0.0, -1.0),
    unit((1.0, 0.0, 1.0)),
    unit((1.0, 1.0, 0.0)),
)

def face_for_mode(n: V, mode: str) -> V:
    nu = unit(n)
    if mode == "CORRECT":
        return (-nu[0], -nu[1], -nu[2])  # f = -n
    if mode == "INVERSE_NEGATIVE_CONTROL":
        return nu  # f = n  (deliberate wrong / reverse face)
    raise ValueError(mode)

def make_trial(
    n: V,
    correct_is_airborne: bool,
    camera: str,
    air_swing: str,
    ground_swing: str,
    index: int,
) -> Trial:
    n = unit(n)
    if correct_is_airborne:
        a = ActorRole("A_AIR", "airborne", air_swing, "CORRECT", True)
        b = ActorRole("B_GROUND", "ground_low", ground_swing, "INVERSE_NEGATIVE_CONTROL", False)
        correct_actor, inverse_actor = a.actor_id, b.actor_id
    else:
        a = ActorRole("A_AIR", "airborne", air_swing, "INVERSE_NEGATIVE_CONTROL", False)
        b = ActorRole("B_GROUND", "ground_low", ground_swing, "CORRECT", True)
        correct_actor, inverse_actor = b.actor_id, a.actor_id

    checks = {
        a.actor_id: check_contact(n, face_for_mode(n, a.face_mode)),
        b.actor_id: check_contact(n, face_for_mode(n, b.face_mode)),
    }
    # Formula contract: correct actor must PASS, inverse must FAIL
    assert checks[correct_actor]["pass"] is True
    assert checks[inverse_actor]["pass"] is False

    tid = f"DACVI__n{index:02d}__{'AIR_OK' if correct_is_airborne else 'GND_OK'}__{camera}"
    prompt_lock = (
        "DUAL-ACTOR CORRECT-VS-INVERSE LOCK. Two independent T-hammers, full heads and long handles visible. "
        f"Target contact outward normal n={tuple(round(x,6) for x in n)}. "
        f"Actor {correct_actor}: face_mode=CORRECT, f=-n, must PASS face-on. "
        f"Actor {inverse_actor}: face_mode=INVERSE_NEGATIVE_CONTROL, f=n, deliberate reverse/wrong wide face, must FAIL as control. "
        f"Heights: A airborne ({air_swing}), B ground_low ({ground_swing}) — poses must not mirror-copy. "
        f"CAMERA={camera} is view-only; camera must not reclassify inverse as correct. "
        "contact_PASS_claimed=false for the paired scene as a whole (contains intentional FAIL control). "
        "Sparks must not hide the seam. Do not merge into one H-weapon."
    )
    return Trial(
        trial_id=tid,
        n=n,
        correct_actor=correct_actor,
        inverse_actor=inverse_actor,
        camera=camera,
        actors=(a, b),
        checks=checks,
        prompt_lock=prompt_lock,
        audit={
            "geometry_formula": "COMPILED",
            "image_realization": "NOT_RUN",
            "pixel_audit": "NOT_RUN",
            "contact_PASS_claimed": "false",
            "wrong_face": "intentional",
        },
    )

def build_matrix(limit: int | None = None) -> Dict[str, object]:
    trials: List[Trial] = []
    i = 0
    for ni, n in enumerate(NORMALS):
        for correct_air in (True, False):
            for cam in CAMERAS:
                for sa, sg in zip(SWINGS_AIR, SWINGS_GROUND):
                    trials.append(
                        make_trial(n, correct_air, cam, sa, sg, index=ni)
                    )
                    i += 1
                    if limit is not None and i >= limit:
                        break
                if limit is not None and i >= limit:
                    break
            if limit is not None and i >= limit:
                break
        if limit is not None and i >= limit:
            break
    # demo asserts from spec
    n_demo = (1.0, 0.0, 0.0)
    correct = check_contact(n_demo, (-1.0, 0.0, 0.0))
    inverse = check_contact(n_demo, (1.0, 0.0, 0.0))
    return {
        "schema_version": "1.0.0-dual-actor-correct-vs-inverse",
        "branch_intent": "feat/dual-actor-correct-vs-inverse-strike",
        "invariant": "PASS iff unit(f)·unit(-n) >= cos(tolerance_deg)",
        "default_tolerance_deg": DEFAULT_TOL_DEG,
        "demo": {
            "CORRECT": correct,
            "INVERSE_NEGATIVE_CONTROL": inverse,
        },
        "counts": {
            "trials": len(trials),
            "normals": len(NORMALS),
            "cameras": len(CAMERAS),
            "height_pair": "airborne_vs_ground_low",
            "face_modes": ["CORRECT", "INVERSE_NEGATIVE_CONTROL"],
        },
        "acceptance_gate": {
            "image_realization": "NOT_RUN",
            "pixel_audit": "NOT_RUN",
            "formula_tests": "RUN_LOCALLY",
        },
        "trials": [
            {
                "trial_id": t.trial_id,
                "n": list(t.n),
                "correct_actor": t.correct_actor,
                "inverse_actor": t.inverse_actor,
                "camera": t.camera,
                "actors": [asdict(a) for a in t.actors],
                "checks": t.checks,
                "prompt_lock": t.prompt_lock,
                "audit": t.audit,
            }
            for t in trials
        ],
        "linked_realized_package": "out/dual_t_correct_vs_wrong (H0/H2/H3 candidate frames; not formal PASS)",
    }

def export(outdir: Path, limit: int | None = None) -> Dict[str, object]:
    outdir.mkdir(parents=True, exist_ok=True)
    m = build_matrix(limit=limit)
    (outdir / "dual_actor_correct_vs_inverse_matrix.json").write_text(
        json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    prompts = outdir / "prompts"
    prompts.mkdir(exist_ok=True)
    for t in m["trials"]:
        (prompts / f"{t['trial_id']}.json").write_text(
            json.dumps(
                {
                    "trial_id": t["trial_id"],
                    "prompt_lock": t["prompt_lock"],
                    "checks": t["checks"],
                    "audit": t["audit"],
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
    (outdir / "README.md").write_text(
        "# Dual-actor correct vs inverse-face formula package\n\n"
        "Geometry-only. Camera varies; contact rule does not.\n\n"
        f"Trials: {m['counts']['trials']}\n"
        "IMAGE_REALIZATION=NOT_RUN\nPIXEL_AUDIT=NOT_RUN\n"
        "contact_PASS_claimed=false (paired scene always contains intentional FAIL control)\n",
        encoding="utf-8",
    )
    return m

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", type=Path, default=Path("out/dual_actor_correct_vs_inverse"))
    ap.add_argument("--limit", type=int, default=None, help="optional cap on trial count")
    args = ap.parse_args()
    m = export(args.outdir, limit=args.limit)
    print(
        json.dumps(
            {
                "status": "COMPILED",
                "trials": m["counts"]["trials"],
                "demo": m["demo"],
                "image_realization": "NOT_RUN",
                "pixel_audit": "NOT_RUN",
            },
            ensure_ascii=False,
        )
    )
