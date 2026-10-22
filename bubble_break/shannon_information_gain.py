"""Shannon-inspired information-gain planner for the image-generation feedback loop.

The calculations are mathematically exact for the likelihood assumptions supplied here, but the
likelihood values are engineering priors—not empirically calibrated model performance. This module
chooses diagnostic experiments; it never declares a picture visually correct.
"""
from __future__ import annotations

import math
from collections import Counter
from dataclasses import asdict, dataclass
from typing import Any, Iterable, Mapping, Sequence

HYPOTHESES = (
    "TOPOLOGY_DRIFT",
    "WRONG_CONTACT_SURFACE",
    "ANCHOR_OR_SCALE_DRIFT",
    "PARENT_OR_IDENTITY_DRIFT",
    "FRACTURE_CAUSALITY_FAILURE",
    "SANCTUARY_PROTECTION_FAILURE",
)

ERROR_TERMS = {
    "TOPOLOGY_DRIFT": (
        "handle", "hammer", "head axis", "joint", "t-shape", "stub", "orthogonal",
        "instance", "head_bbox", "handle_axis",
    ),
    "WRONG_CONTACT_SURFACE": (
        "contact surface", "end-face", "end face", "cheek", "striking face", "face center",
        "signed gap", "zero gap", "first contact", "active surface",
    ),
    "ANCHOR_OR_SCALE_DRIFT": (
        "pole", "anchor", "drift", "bubble radius", "sphere center", "scale mismatch",
        "contact point p", "locked p",
    ),
    "PARENT_OR_IDENTITY_DRIFT": (
        "sha256", "parent", "identity", "stage slot", "no-op", "identical to parent",
        "camera lock", "scene lock", "provenance",
    ),
    "FRACTURE_CAUSALITY_FAILURE": (
        "crack", "fracture", "shell state", "crack front", "propagat", "shatter",
    ),
    "SANCTUARY_PROTECTION_FAILURE": (
        "inhabitant", "sanctuary", "warmth", "resident", "shell-only breach",
        "shell only", "city damaged",
    ),
}

# P(diagnostic observation | fault hypothesis). These initial values are explicit engineering
# assumptions for deciding what to inspect next. Replace with empirically measured rates when
# enough reviewed runs exist; the report labels them uncalibrated until then.
DEFAULT_ACTIONS: tuple[dict[str, Any], ...] = (
    {
        "action_id": "TOPOLOGY_WIDE_RIGID_BODY_AUDIT",
        "target_hypothesis": "TOPOLOGY_DRIFT",
        "cost_units": 1.4,
        "likelihoods": {
            "TOPOLOGY_DRIFT": 0.94, "WRONG_CONTACT_SURFACE": 0.18,
            "ANCHOR_OR_SCALE_DRIFT": 0.12, "PARENT_OR_IDENTITY_DRIFT": 0.10,
            "FRACTURE_CAUSALITY_FAILURE": 0.09, "SANCTUARY_PROTECTION_FAILURE": 0.08,
        },
        "instruction": "Create a diagnostic full-frame view that exposes the entire rigid head, its actual handle joint, and the handle axis. Do not change the canonical scene frame or relax any lock.",
    },
    {
        "action_id": "CONTACT_PLANE_GRAZING_MACRO",
        "target_hypothesis": "WRONG_CONTACT_SURFACE",
        "cost_units": 1.0,
        "likelihoods": {
            "TOPOLOGY_DRIFT": 0.15, "WRONG_CONTACT_SURFACE": 0.96,
            "ANCHOR_OR_SCALE_DRIFT": 0.18, "PARENT_OR_IDENTITY_DRIFT": 0.10,
            "FRACTURE_CAUSALITY_FAILURE": 0.30, "SANCTUARY_PROTECTION_FAILURE": 0.05,
        },
        "instruction": "Create a separate contact-diagnostic macro from a grazing three-quarter angle. Show the terminal-face perimeter, local bubble normal, gap and point P; glow may not cover the actual interface. This diagnostic view is not itself the final continuity frame.",
    },
    {
        "action_id": "PARENT_PAIR_LOCK_AUDIT",
        "target_hypothesis": "PARENT_OR_IDENTITY_DRIFT",
        "cost_units": 0.55,
        "likelihoods": {
            "TOPOLOGY_DRIFT": 0.10, "WRONG_CONTACT_SURFACE": 0.12,
            "ANCHOR_OR_SCALE_DRIFT": 0.24, "PARENT_OR_IDENTITY_DRIFT": 0.97,
            "FRACTURE_CAUSALITY_FAILURE": 0.08, "SANCTUARY_PROTECTION_FAILURE": 0.08,
        },
        "instruction": "Before spending another image attempt, compare parent/candidate SHA-256, expected-stage binding, same-camera and scene-lock IDs, object identity IDs, dimensions, and unchanged protected regions. Reject stale or copied candidates.",
    },
    {
        "action_id": "POLE_AND_SCALE_CALIBRATION_VIEW",
        "target_hypothesis": "ANCHOR_OR_SCALE_DRIFT",
        "cost_units": 1.0,
        "likelihoods": {
            "TOPOLOGY_DRIFT": 0.12, "WRONG_CONTACT_SURFACE": 0.24,
            "ANCHOR_OR_SCALE_DRIFT": 0.95, "PARENT_OR_IDENTITY_DRIFT": 0.16,
            "FRACTURE_CAUSALITY_FAILURE": 0.15, "SANCTUARY_PROTECTION_FAILURE": 0.06,
        },
        "instruction": "Inspect a separate calibrated view with bubble center/radius and six-o'clock pole P annotated. Measure the face-to-P offset and positive gap without moving the canonical camera or silently changing sphere scale.",
    },
    {
        "action_id": "FRACTURE_ORIGIN_AND_FRONT_AUDIT",
        "target_hypothesis": "FRACTURE_CAUSALITY_FAILURE",
        "cost_units": 0.9,
        "likelihoods": {
            "TOPOLOGY_DRIFT": 0.08, "WRONG_CONTACT_SURFACE": 0.23,
            "ANCHOR_OR_SCALE_DRIFT": 0.18, "PARENT_OR_IDENTITY_DRIFT": 0.08,
            "FRACTURE_CAUSALITY_FAILURE": 0.96, "SANCTUARY_PROTECTION_FAILURE": 0.12,
        },
        "instruction": "Inspect P and the crack front in separate native-resolution crops. Record the crack-origin distance from P and normalized crack-front radius for H2, H2B and H3; require monotonic outward growth.",
    },
    {
        "action_id": "SANCTUARY_SHELL_ONLY_AUDIT",
        "target_hypothesis": "SANCTUARY_PROTECTION_FAILURE",
        "cost_units": 0.75,
        "likelihoods": {
            "TOPOLOGY_DRIFT": 0.04, "WRONG_CONTACT_SURFACE": 0.05,
            "ANCHOR_OR_SCALE_DRIFT": 0.06, "PARENT_OR_IDENTITY_DRIFT": 0.05,
            "FRACTURE_CAUSALITY_FAILURE": 0.22, "SANCTUARY_PROTECTION_FAILURE": 0.97,
        },
        "instruction": "Inspect shell shards, resident silhouettes, and the enclosed sanctuary separately from the contact FX. Confirm the containment shell is the only damaged target and residents remain intact.",
    },
)


def normalize_distribution(values: Mapping[str, float]) -> dict[str, float]:
    if not values:
        raise ValueError("probability distribution must not be empty")
    clean: dict[str, float] = {}
    for key, value in values.items():
        p = float(value)
        if not math.isfinite(p) or p < 0:
            raise ValueError(f"invalid probability for {key}: {value!r}")
        clean[str(key)] = p
    total = sum(clean.values())
    if total <= 0:
        raise ValueError("probability distribution must have positive mass")
    return {key: value / total for key, value in clean.items()}


def shannon_entropy_bits(distribution: Mapping[str, float]) -> float:
    """H(X) = -sum p(x) log2(p(x)); zero-probability terms contribute zero."""
    p = normalize_distribution(distribution)
    return -sum(value * math.log2(value) for value in p.values() if value > 0)


def _binary_entropy(p: float) -> float:
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -(p * math.log2(p) + (1.0 - p) * math.log2(1.0 - p))


@dataclass(frozen=True)
class ExperimentScore:
    action_id: str
    target_hypothesis: str
    cost_units: float
    expected_information_gain_bits: float
    information_gain_per_cost: float
    prior_entropy_bits: float
    expected_remaining_entropy_bits: float
    diagnostic_instruction: str
    assumptions_status: str = "ENGINEERING_PRIORS_NOT_EMPIRICALLY_CALIBRATED"


def expected_information_gain_bits(
    priors: Mapping[str, float],
    likelihood_positive_given_hypothesis: Mapping[str, float],
) -> float:
    """Mutual information I(H;O) for a binary diagnostic outcome O.

    Each likelihood is P(O=positive | H=h). A score of zero means the experiment is not expected
    to distinguish the current hypotheses under the supplied model.
    """
    p_h = normalize_distribution(priors)
    if set(p_h) - set(likelihood_positive_given_hypothesis):
        raise ValueError("likelihood matrix is missing one or more hypotheses")
    likelihoods: dict[str, float] = {}
    for hypothesis in p_h:
        q = float(likelihood_positive_given_hypothesis[hypothesis])
        if not math.isfinite(q) or q < 0 or q > 1:
            raise ValueError(f"likelihood for {hypothesis} must be in [0,1]")
        likelihoods[hypothesis] = q
    p_positive = sum(p_h[h] * likelihoods[h] for h in p_h)
    outcome_entropy = _binary_entropy(p_positive)
    conditional_entropy = sum(p_h[h] * _binary_entropy(likelihoods[h]) for h in p_h)
    return max(0.0, outcome_entropy - conditional_entropy)


def classify_failure_hypotheses(errors: Iterable[str]) -> list[str]:
    text = " ".join(str(error).lower() for error in errors)
    matched = [
        hypothesis for hypothesis, terms in ERROR_TERMS.items()
        if any(term in text for term in terms)
    ]
    return matched or list(HYPOTHESES)


def _priors_from_attempt_history(
    attempt_history: Sequence[Mapping[str, Any]] | None,
) -> dict[str, float]:
    counts = Counter({hypothesis: 1.0 for hypothesis in HYPOTHESES})  # Laplace smoothing
    if attempt_history:
        for record in attempt_history:
            if record.get("accepted") is True:
                continue
            errors = record.get("errors", [])
            if isinstance(errors, str):
                errors = [errors]
            for hypothesis in classify_failure_hypotheses(errors):
                counts[hypothesis] += 1.0
    return normalize_distribution(counts)


def rank_diagnostic_experiments(
    priors: Mapping[str, float],
    actions: Sequence[Mapping[str, Any]] = DEFAULT_ACTIONS,
) -> list[ExperimentScore]:
    p_h = normalize_distribution(priors)
    entropy_before = shannon_entropy_bits(p_h)
    scores: list[ExperimentScore] = []
    for action in actions:
        cost = float(action.get("cost_units", 1.0))
        if not math.isfinite(cost) or cost <= 0:
            raise ValueError(f"experiment {action.get('action_id')} must have positive finite cost")
        likelihoods = action.get("likelihoods", {})
        information_gain = expected_information_gain_bits(p_h, likelihoods)
        conditional_entropy = max(0.0, entropy_before - information_gain)
        scores.append(
            ExperimentScore(
                action_id=str(action["action_id"]),
                target_hypothesis=str(action["target_hypothesis"]),
                cost_units=cost,
                expected_information_gain_bits=round(information_gain, 6),
                information_gain_per_cost=round(information_gain / cost, 6),
                prior_entropy_bits=round(entropy_before, 6),
                expected_remaining_entropy_bits=round(conditional_entropy, 6),
                diagnostic_instruction=str(action["instruction"]),
            )
        )
    scores.sort(key=lambda score: (-score.information_gain_per_cost, -score.expected_information_gain_bits, score.action_id))
    return scores


def recommend_next_experiment(
    errors: Iterable[str],
    attempt_history: Sequence[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Choose the highest expected information-gain/cost diagnostic after a failed gate."""
    error_list = [str(error) for error in errors]
    identified = classify_failure_hypotheses(error_list)
    base = _priors_from_attempt_history(attempt_history)
    # Current observed error codes are evidence about the fault hypothesis. This uses a transparent
    # heuristic update (not a learned/calibrated model): reweight matched classes, then normalize.
    weights = {hypothesis: base[hypothesis] * (8.0 if hypothesis in identified else 1.0) for hypothesis in HYPOTHESES}
    posterior = normalize_distribution(weights)
    ranked = rank_diagnostic_experiments(posterior)
    best = ranked[0]
    return {
        "controller": "SHANNON_EXPECTED_INFORMATION_GAIN",
        "identified_failure_hypotheses": identified,
        "posterior_hypotheses": posterior,
        "uncertainty_entropy_bits": round(shannon_entropy_bits(posterior), 6),
        "selected_experiment": asdict(best),
        "ranked_experiments": [asdict(item) for item in ranked],
        "calibration_status": "UNVALIDATED_ENGINEERING_PRIORS",
        "hard_rule": "Information gain selects the next diagnostic only; it cannot override any geometric gate or turn missing visual evidence into PASS.",
    }
