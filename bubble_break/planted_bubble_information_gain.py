"""Shannon-style information-gain planner for the planted-cylinder Bubble-Break workflow.

The likelihoods below are transparent engineering priors, not measured Gemini accuracy.
Information gain chooses a diagnostic/edit emphasis; it never overrides a geometry gate or
sets visual acceptance. Replace priors with measured image-matched review outcomes over time.
"""
from __future__ import annotations

import math
from collections import Counter
from typing import Any, Iterable, Mapping, Sequence

HYPOTHESES = (
    "MASTER_ROI_OR_SOURCE_FAILURE",
    "CYLINDER_SEAT_OR_POLE_DRIFT",
    "HANDLE_INSTANCE_OR_AXIS_DRIFT",
    "PERSON_GRIP_STATE_FAILURE",
    "SHELL_FRACTURE_CAUSALITY_FAILURE",
    "SANCTUARY_SAFETY_FAILURE",
    "RASTER_LINEAGE_FAILURE",
)

ERROR_TERMS = {
    "MASTER_ROI_OR_SOURCE_FAILURE": ("MASTER_SELECTION", "SOURCE_ATLAS", "ROI", "SINGLE_TOOL", "TOOL_MASTER"),
    "CYLINDER_SEAT_OR_POLE_DRIFT": ("P_NOT_ON_BUBBLE", "CONTACT_POINT", "BASE_SEAT", "BUBBLE_CENTER", "CYLINDER_AXIS", "OUTER_END_CAP"),
    "HANDLE_INSTANCE_OR_AXIS_DRIFT": ("HANDLE", "STUB", "ROD", "SIDE_HANDLE", "TRANSVERSE", "TANGENT"),
    "PERSON_GRIP_STATE_FAILURE": ("HEROINE", "GRIP", "BOTH_HANDS", "ACTOR_PRESENCE", "MINIATURE"),
    "SHELL_FRACTURE_CAUSALITY_FAILURE": ("CRACK", "SHELL_STATE", "BASE_GLOW", "FRACTURE", "SHATTER"),
    "SANCTUARY_SAFETY_FAILURE": ("SANCTUARY", "INHABITANT", "RESIDENT", "SHELL_ONLY", "CITY"),
    "RASTER_LINEAGE_FAILURE": ("SHA256", "PARENT", "ANCHOR", "RASTER", "STAGE", "IDENTITY", "NO_OP"),
}

# P(observation is diagnostically positive | fault hypothesis), uncalibrated.
DEFAULT_ACTIONS: tuple[dict[str, Any], ...] = (
    {
        "action_id": "MASTER_ROI_AND_SOURCE_PROOF",
        "target_hypothesis": "MASTER_ROI_OR_SOURCE_FAILURE",
        "cost_units": 0.7,
        "likelihoods": {"MASTER_ROI_OR_SOURCE_FAILURE": 0.97, "CYLINDER_SEAT_OR_POLE_DRIFT": 0.12, "HANDLE_INSTANCE_OR_AXIS_DRIFT": 0.10, "PERSON_GRIP_STATE_FAILURE": 0.04, "SHELL_FRACTURE_CAUSALITY_FAILURE": 0.05, "SANCTUARY_SAFETY_FAILURE": 0.03, "RASTER_LINEAGE_FAILURE": 0.14},
        "instruction": "Audit the human-selected source-atlas ROI by pixel position, source SHA, dimensions, and crop SHA. Inspect only one candidate tool; do not infer correctness from printed labels."
    },
    {
        "action_id": "BASE_SEAT_AND_POLE_MACRO",
        "target_hypothesis": "CYLINDER_SEAT_OR_POLE_DRIFT",
        "cost_units": 0.9,
        "likelihoods": {"MASTER_ROI_OR_SOURCE_FAILURE": 0.12, "CYLINDER_SEAT_OR_POLE_DRIFT": 0.97, "HANDLE_INSTANCE_OR_AXIS_DRIFT": 0.20, "PERSON_GRIP_STATE_FAILURE": 0.04, "SHELL_FRACTURE_CAUSALITY_FAILURE": 0.26, "SANCTUARY_SAFETY_FAILURE": 0.05, "RASTER_LINEAGE_FAILURE": 0.08},
        "instruction": "Inspect a native-resolution macro of P and the conformal curved base seat. Measure bubble center/radius, base-seat center, surface normal and any gap; never replace a planted seat with a flying strike."
    },
    {
        "action_id": "EXISTING_HANDLE_TRACK_AUDIT",
        "target_hypothesis": "HANDLE_INSTANCE_OR_AXIS_DRIFT",
        "cost_units": 0.8,
        "likelihoods": {"MASTER_ROI_OR_SOURCE_FAILURE": 0.08, "CYLINDER_SEAT_OR_POLE_DRIFT": 0.16, "HANDLE_INSTANCE_OR_AXIS_DRIFT": 0.97, "PERSON_GRIP_STATE_FAILURE": 0.34, "SHELL_FRACTURE_CAUSALITY_FAILURE": 0.04, "SANCTUARY_SAFETY_FAILURE": 0.03, "RASTER_LINEAGE_FAILURE": 0.16},
        "instruction": "Audit the same side-middle tangent handle instance and track across parent/candidate. Confirm its attachment, axis and length are invariant; D2 moves hands to the existing rod and must not invent an axial handle or lower stub."
    },
    {
        "action_id": "GRIP_AND_BODY_POSE_AUDIT",
        "target_hypothesis": "PERSON_GRIP_STATE_FAILURE",
        "cost_units": 0.8,
        "likelihoods": {"MASTER_ROI_OR_SOURCE_FAILURE": 0.05, "CYLINDER_SEAT_OR_POLE_DRIFT": 0.05, "HANDLE_INSTANCE_OR_AXIS_DRIFT": 0.28, "PERSON_GRIP_STATE_FAILURE": 0.96, "SHELL_FRACTURE_CAUSALITY_FAILURE": 0.05, "SANCTUARY_SAFETY_FAILURE": 0.02, "RASTER_LINEAGE_FAILURE": 0.08},
        "instruction": "Review the heroine/handle relationship. C and D1 must not grip; D2/D3 must grip the same existing handle with both hands. Keep the planted cylinder and contact seat unchanged."
    },
    {
        "action_id": "CRACK_ORIGIN_AND_OUTWARD_FRONT_AUDIT",
        "target_hypothesis": "SHELL_FRACTURE_CAUSALITY_FAILURE",
        "cost_units": 1.0,
        "likelihoods": {"MASTER_ROI_OR_SOURCE_FAILURE": 0.03, "CYLINDER_SEAT_OR_POLE_DRIFT": 0.24, "HANDLE_INSTANCE_OR_AXIS_DRIFT": 0.04, "PERSON_GRIP_STATE_FAILURE": 0.04, "SHELL_FRACTURE_CAUSALITY_FAILURE": 0.98, "SANCTUARY_SAFETY_FAILURE": 0.18, "RASTER_LINEAGE_FAILURE": 0.04},
        "instruction": "Compare E-mid with D3 and E-end with E-mid. Verify crack origin coincides with the same P, fracture extent grows outward, E-mid is not yet fully shattered, and no second origin is introduced."
    },
    {
        "action_id": "SANCTUARY_AND_SHELL_ONLY_AUDIT",
        "target_hypothesis": "SANCTUARY_SAFETY_FAILURE",
        "cost_units": 0.75,
        "likelihoods": {"MASTER_ROI_OR_SOURCE_FAILURE": 0.02, "CYLINDER_SEAT_OR_POLE_DRIFT": 0.05, "HANDLE_INSTANCE_OR_AXIS_DRIFT": 0.02, "PERSON_GRIP_STATE_FAILURE": 0.03, "SHELL_FRACTURE_CAUSALITY_FAILURE": 0.22, "SANCTUARY_SAFETY_FAILURE": 0.98, "RASTER_LINEAGE_FAILURE": 0.03},
        "instruction": "Inspect shell shards, city structures and residents separately from glow/impact effects. Reject if the sanctuary or residents appear damaged, if shards pass through them, or if the target changes from shell to city."
    },
    {
        "action_id": "PARENT_AND_MASTER_HASH_AUDIT",
        "target_hypothesis": "RASTER_LINEAGE_FAILURE",
        "cost_units": 0.45,
        "likelihoods": {"MASTER_ROI_OR_SOURCE_FAILURE": 0.12, "CYLINDER_SEAT_OR_POLE_DRIFT": 0.07, "HANDLE_INSTANCE_OR_AXIS_DRIFT": 0.12, "PERSON_GRIP_STATE_FAILURE": 0.05, "SHELL_FRACTURE_CAUSALITY_FAILURE": 0.05, "SANCTUARY_SAFETY_FAILURE": 0.04, "RASTER_LINEAGE_FAILURE": 0.99},
        "instruction": "Before spending another image request, verify exact candidate/parent/master SHA-256, stage binding, canvas dimensions, and scene/cylinder/handle IDs. Reject stale reviews and no-op copies."
    },
)

def normalize_distribution(values: Mapping[str, float]) -> dict[str, float]:
    if not values:
        raise ValueError("probability distribution must not be empty")
    clean: dict[str, float] = {}
    for key, raw in values.items():
        value = float(raw)
        if not math.isfinite(value) or value < 0:
            raise ValueError(f"invalid probability for {key}: {raw!r}")
        clean[str(key)] = value
    total = sum(clean.values())
    if total <= 0:
        raise ValueError("probability distribution must have positive mass")
    return {key: value / total for key, value in clean.items()}

def shannon_entropy_bits(distribution: Mapping[str, float]) -> float:
    p = normalize_distribution(distribution)
    return -sum(value * math.log2(value) for value in p.values() if value > 0)

def _binary_entropy(p: float) -> float:
    if p <= 0 or p >= 1:
        return 0.0
    return -(p * math.log2(p) + (1-p) * math.log2(1-p))

def expected_information_gain_bits(
    priors: Mapping[str, float],
    likelihood_positive_given_hypothesis: Mapping[str, float],
) -> float:
    p_h = normalize_distribution(priors)
    if set(p_h) - set(likelihood_positive_given_hypothesis):
        raise ValueError("likelihood matrix is missing one or more hypotheses")
    likelihoods: dict[str, float] = {}
    for hypothesis in p_h:
        q = float(likelihood_positive_given_hypothesis[hypothesis])
        if not math.isfinite(q) or not 0 <= q <= 1:
            raise ValueError(f"likelihood for {hypothesis} must be in [0,1]")
        likelihoods[hypothesis] = q
    p_positive = sum(p_h[h] * likelihoods[h] for h in p_h)
    return max(0.0, _binary_entropy(p_positive) - sum(p_h[h] * _binary_entropy(likelihoods[h]) for h in p_h))

def classify_failure_hypotheses(errors: Iterable[str]) -> list[str]:
    text = " ".join(str(error).lower() for error in errors)
    found = [hypothesis for hypothesis, terms in ERROR_TERMS.items() if any(term.lower() in text for term in terms)]
    return found or list(HYPOTHESES)

def _priors_from_history(history: Sequence[Mapping[str, Any]] | None) -> dict[str, float]:
    counts = Counter({hypothesis: 1.0 for hypothesis in HYPOTHESES})
    for record in history or ():
        if record.get("contract_valid") is True or record.get("eligible_for_next_stage") is True:
            continue
        errors = record.get("errors", [])
        if isinstance(errors, str):
            errors = [errors]
        for hypothesis in classify_failure_hypotheses(errors):
            counts[hypothesis] += 1
    return normalize_distribution(counts)

def rank_diagnostic_experiments(
    priors: Mapping[str, float],
    actions: Sequence[Mapping[str, Any]] = DEFAULT_ACTIONS,
) -> list[dict[str, Any]]:
    p_h = normalize_distribution(priors)
    h_before = shannon_entropy_bits(p_h)
    scores = []
    for action in actions:
        cost = float(action.get("cost_units", 1.0))
        if not math.isfinite(cost) or cost <= 0:
            raise ValueError(f"diagnostic action {action.get('action_id')} needs positive finite cost")
        info = expected_information_gain_bits(p_h, action["likelihoods"])
        scores.append({
            "action_id": str(action["action_id"]),
            "target_hypothesis": str(action["target_hypothesis"]),
            "cost_units": cost,
            "expected_information_gain_bits": round(info, 6),
            "information_gain_per_cost": round(info / cost, 6),
            "prior_entropy_bits": round(h_before, 6),
            "expected_remaining_entropy_bits": round(max(0.0, h_before - info), 6),
            "diagnostic_instruction": str(action["instruction"]),
            "assumptions_status": "UNVALIDATED_ENGINEERING_PRIORS",
        })
    scores.sort(key=lambda item: (-item["information_gain_per_cost"], -item["expected_information_gain_bits"], item["action_id"]))
    return scores

def recommend_next_experiment(
    errors: Iterable[str],
    attempt_history: Sequence[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    error_list = [str(error) for error in errors]
    identified = classify_failure_hypotheses(error_list)
    base = _priors_from_history(attempt_history)
    posterior = normalize_distribution({
        hypothesis: base[hypothesis] * (8.0 if hypothesis in identified else 1.0)
        for hypothesis in HYPOTHESES
    })
    ranked = rank_diagnostic_experiments(posterior)
    return {
        "controller": "SHANNON_EXPECTED_INFORMATION_GAIN",
        "identified_failure_hypotheses": identified,
        "posterior_hypotheses": posterior,
        "uncertainty_entropy_bits": round(shannon_entropy_bits(posterior), 6),
        "selected_experiment": ranked[0],
        "ranked_experiments": ranked,
        "calibration_status": "UNVALIDATED_ENGINEERING_PRIORS",
        "hard_rule": "Information gain selects a diagnostic emphasis only; it cannot override a hard gate, fabricate evidence, or set PASS.",
    }
