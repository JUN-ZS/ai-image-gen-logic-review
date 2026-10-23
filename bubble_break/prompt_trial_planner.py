#!/usr/bin/env python3
"""Plan the next controlled image, teaching-board, or video-prompt experiment.

This is a deterministic experiment scheduler. It does not inspect images, generate
media, or infer which formula is best. A prior trial counts as reviewed only when
each arm has enough evidence items and every review receipt binds to that exact
artifact SHA-256.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


TRIALS: list[dict[str, Any]] = [
    {
        "trial_id": "IMG-FORMULA-01",
        "family": "image_formula",
        "title": "Explicit contact contract vs compact prose",
        "objective": "Test whether an explicit geometry/contact contract improves correct active-face contact without damaging topology.",
        "hypothesis": "Naming the active terminal face, point P, collision normal and forbidden first-contact surfaces will make contact more reliable than compact prose alone.",
        "control": {
            "label": "A — compact-prose baseline",
            "kind": "prompt_suffix",
            "payload": "Use the approved T-Hammer topology to strike the same translucent sphere with the intended flat terminal face. Keep the scene and character unchanged."
        },
        "treatment": {
            "label": "B — explicit geometry contract",
            "kind": "prompt_suffix",
            "payload": "CONTACT CONTRACT: active_surface=terminal_end_face; first contact occurs at the declared anchor P along the existing collision normal n. H0 keeps a positive air gap; H2 has zero gap and zero penetration; H3 advances along the same n. The broad sidewall, corner, handle and head-handle joint must not be the first-contact surface. Keep the approved rigid T-Hammer topology."
        },
        "vary_only": ["contact-contract wording block"],
        "freeze": ["topology_id", "character_identity", "target_geometry", "scene_landmarks", "camera_rig", "seed policy", "lighting", "effect budget"],
        "replicates_per_arm": 3,
        "metric": "Number of reviewed images passing all physical and topology hard gates, out of 3 per arm; separately count each failure code.",
        "success_rule": "Screening win only if treatment has at least 2 more full-gate passes than control and introduces no new topology or protected-resident safety failure. Otherwise repeat or call inconclusive; n=3 is not statistical proof.",
        "required_artifacts": ["exact control/treatment prompt text", "one real source raster per replicate", "raster SHA-256", "same-raster review receipt", "teaching board per raster", "failure-code tally"],
        "dependencies": [],
        "after_win": "Repeat with three new paired seeds before adopting the explicit contract as the preferred formula.",
        "after_tie_or_loss": "Inspect per-code counts; do not lengthen every prompt at once. Choose a new, separately registered factor only after this comparison is reviewed."
    },
    {
        "trial_id": "IMG-TEACH-01",
        "family": "image_teaching",
        "title": "Standard evidence board vs formula-first teaching board",
        "objective": "Test whether a formula-first teaching layout helps a reviewer explain the image without confusing prompt intent with pixel evidence.",
        "hypothesis": "Showing the formula sequence before variable details makes the relationship between prompt structure, expected geometry and the observed raster easier to teach.",
        "control": {
            "label": "A — standard evidence board",
            "kind": "render_mode",
            "payload": "Render the same manifest and exact same source raster with --teaching-layout standard."
        },
        "treatment": {
            "label": "B — formula-first teaching board",
            "kind": "render_mode",
            "payload": "Render the same manifest and exact same source raster with --teaching-layout formula-first. Display OUTPUT CONTRACT → TOPOLOGY → CONTACT → ACTION → CAMERA → LIGHT/FX → NEGATIVES before the changed-variable line."
        },
        "vary_only": ["teaching-board layout"],
        "freeze": ["source raster bytes and SHA-256", "manifest values", "review receipt", "all underlying image pixels", "review rubric"],
        "replicates_per_arm": 3,
        "metric": "Reviewer can correctly identify the selected topology, active face, single experimental variable, expected-vs-observed mismatch, and next experiment without guessing; compare blind rubric pass counts.",
        "success_rule": "Formula-first wins only if it improves the blind teaching-rubric result for at least 2 of the 3 paired source images, while all raster hashes remain identical between layouts.",
        "required_artifacts": ["three reviewed real source rasters", "standard board for each raster", "formula-first board for the same raster", "layout-only comparison receipts", "source raster hash shown on both boards"],
        "dependencies": [],
        "after_win": "Use formula-first as the default teaching layout only after the paired review; retain the standard layout for direct comparison.",
        "after_tie_or_loss": "Keep both layouts available and revise one teaching field at a time; do not alter or regenerate the source image during this test."
    },
    {
        "trial_id": "VIDEO-FORMULA-01",
        "family": "video_formula",
        "title": "Monolithic 10-second prompt vs five timed state contracts",
        "objective": "Compare a single prose timeline with a prompt organized around five explicit, auditable time states.",
        "hypothesis": "Per-state constraints will improve event order and state readability compared with one continuous prose description.",
        "control": {
            "label": "A — monolithic timeline prompt",
            "kind": "prompt_suffix",
            "payload": "Create one continuous 10-second cinematic 16:9 shot: the heroine winds up, strikes the sphere, cracks spread, and the outer shell breaks. Keep the scene coherent from beginning to end."
        },
        "treatment": {
            "label": "B — five-state prompt formula",
            "kind": "prompt_suffix",
            "payload": "TIMECODED STATE CONTRACT: 0.0–2.0 s PRE_FAR: intact sphere and positive gap; 2.0–4.5 s PRE_NEAR: same rigid weapon advances and gap stays positive; at 4.5 s CONTACT: declared terminal face meets the sphere at P with zero gap and no penetration, first glow/cracks begin at P; 4.5–7.0 s E_MID: cracks/ripples propagate outward from P; 7.0–10.0 s E_END: shell fragments move outward while the protected inner sanctuary remains intact. Preserve the same identity, topology, P, world axis, camera rig and scene landmarks throughout. If continuous motion cannot be guaranteed, create five separate keyframes and audit continuity rather than claiming a continuous-video pass."
        },
        "vary_only": ["temporal prompt structure"],
        "freeze": ["story meaning", "character identity/outfit", "weapon topology", "sphere geometry", "contact anchor P", "camera rig", "scene landmarks", "lighting direction", "protected-resident safety contract"],
        "replicates_per_arm": 3,
        "metric": "Full sequence pass count: ordered pre-contact gap, contact at the declared time, crack origin at P, outward propagation, stable identity/scene, and protected inner sanctuary.",
        "success_rule": "Treat the format as a screening win only if it yields at least 2 additional full-sequence passes out of 3 and has no safety or topology regression. If a real video backend is unavailable, five audited keyframes may test state compliance but cannot establish video continuity.",
        "required_artifacts": ["exact arm prompts", "actual clip or five individually generated keyframes", "clip/frame-set SHA-256", "timecoded review receipts", "teaching board per keyframe", "continuity scorecard"],
        "dependencies": [],
        "after_win": "Test parent-frame anchors and per-keyframe authorized deltas as the next isolated continuity factor.",
        "after_tie_or_loss": "Retain both prompt forms as unranked candidates; diagnose which timeline state failed before registering a new comparison."
    },
    {
        "trial_id": "VIDEO-CONTINUITY-02",
        "family": "video_continuity",
        "title": "Text-only continuity vs parent-frame and authorized-delta locks",
        "objective": "Test whether explicit parent-frame provenance and frozen/authorized fields reduce identity, scene and contact-point drift.",
        "hypothesis": "Binding each keyframe to a parent raster SHA, master anchor, scene ID and authorized delta list will reduce between-frame drift.",
        "control": {
            "label": "A — text-only continuity",
            "kind": "prompt_suffix",
            "payload": "Keep the heroine, weapon and location consistent across the five keyframes."
        },
        "treatment": {
            "label": "B — provenance and state locks",
            "kind": "prompt_suffix",
            "payload": "For every keyframe, record scene_id, parent_PASS_raster_sha256, master_anchor_sha256, frame_time, authorized_delta_fields and frozen_fields. Change only the fields authorized for that state. Keep character identity, weapon topology, camera rig, background landmarks, sphere geometry and contact anchor P frozen unless the state contract explicitly authorizes a change. A missing parent SHA or failed parent blocks later frames."
        },
        "vary_only": ["continuity state-lock block"],
        "freeze": ["keyframe times", "base composition", "scene and character designs", "motion intent", "review criteria"],
        "replicates_per_arm": 3,
        "metric": "Number of sequences whose identity, landmarks, topology, P and unauthorized pixels remain within the declared review limits.",
        "success_rule": "Treatment wins only with at least 2 more sequence-level continuity passes out of 3 and no missing provenance or safety gate.",
        "required_artifacts": ["five real keyframes or real clip per replicate", "parent/master raster hashes", "authorized and frozen field list", "per-frame receipts", "sequence continuity receipt"],
        "dependencies": ["VIDEO-FORMULA-01"],
        "after_win": "Carry the lock block into later video tests, while preserving the winning temporal format as a separate factor.",
        "after_tie_or_loss": "Check whether the parent raster was actually supplied and each delta was respected; do not declare continuity from prompt text alone."
    },
    {
        "trial_id": "VIDEO-CAUSALITY-03",
        "family": "video_causality",
        "title": "Generic smash language vs timed causal fracture chain",
        "objective": "Test whether causal ordering language improves the sequence from first contact to crack propagation and shell breakup.",
        "hypothesis": "An explicit contact → first crack at P → outward propagation → shell breakup chain will reduce premature cracks and unrelated fracture origins.",
        "control": {
            "label": "A — generic action wording",
            "kind": "prompt_suffix",
            "payload": "The hammer smashes the sphere dramatically and the sphere breaks into fragments."
        },
        "treatment": {
            "label": "B — causal event chain",
            "kind": "prompt_suffix",
            "payload": "Causal order is mandatory: before contact the shell remains intact; at first contact only the declared point P receives the first restrained glow and first micro-crack; cracks and shock ripples then propagate outward from P; only later does the outer shell fragment outward. Never show cracks before contact or a fracture originating away from P. Keep the protected inner sanctuary intact."
        },
        "vary_only": ["fracture-causality wording"],
        "freeze": ["time format", "keyframe schedule", "identity", "topology", "camera", "scene", "impact path"],
        "replicates_per_arm": 3,
        "metric": "Count sequences with correct event ordering, first-crack origin P, outward propagation, and no pre-contact effects.",
        "success_rule": "Treatment wins only if it gains at least 2 full causal-order passes out of 3 with no hard-gate regression; otherwise keep the result inconclusive.",
        "required_artifacts": ["exact prompts", "real video or five real keyframes per replicate", "artifact SHA-256", "timecoded review receipt", "teaching boards for reviewed states"],
        "dependencies": ["VIDEO-FORMULA-01"],
        "after_win": "Keep causal wording as an independently supported block; then test its interaction with continuity locks in a separately registered experiment.",
        "after_tie_or_loss": "Inspect the earliest causal violation and design a new single-factor test; do not pile on extra style adjectives."
    },
    {
        "trial_id": "IMG-CAMERA-02",
        "family": "image_formula",
        "title": "Readable three-quarter camera vs current camera",
        "objective": "Test whether a contact-legible three-quarter camera improves auditability without changing world-space geometry.",
        "hypothesis": "A modest camera move that exposes the active-face seam will improve reviewer agreement while preserving the exact collision geometry.",
        "control": {
            "label": "A — current approved camera",
            "kind": "prompt_suffix",
            "payload": "Use the currently approved camera rig and framing."
        },
        "treatment": {
            "label": "B — contact-legible three-quarter view",
            "kind": "prompt_suffix",
            "payload": "Change only the camera viewpoint to a three-quarter view that exposes the active-face/sphere seam and the handle joint. Do not move the weapon, target, contact point P or world-space collision axis."
        },
        "vary_only": ["camera viewpoint"],
        "freeze": ["weapon rigid pose", "world collision axis", "target geometry", "P", "character identity", "light direction", "style"],
        "replicates_per_arm": 3,
        "metric": "Blind reviewer can classify the actual first-contact surface and gap state; separately verify that world-space geometry is unchanged.",
        "success_rule": "Treatment wins only if at least 2 additional images are auditable out of 3 and there is no geometry drift.",
        "required_artifacts": ["paired real rasters", "camera settings", "contact ROI", "raster-bound review receipts", "standard and formula-first teaching boards"],
        "dependencies": ["IMG-FORMULA-01"],
        "after_win": "Use the better camera only for evidence capture; assess cinematic composition separately later.",
        "after_tie_or_loss": "Do not change pose and camera together. Keep the current camera pending a new isolated camera experiment."
    }
]


TRIAL_BY_ID = {item["trial_id"]: item for item in TRIALS}
SHA_RE = re.compile(r"^[a-fA-F0-9]{64}$")
FAMILY_ALIASES = {
    "all": None,
    "image": {"image_formula", "image_teaching"},
    "video": {"video_formula", "video_continuity", "video_causality"},
}


def _evidence_counts(entry: dict[str, Any], trial: dict[str, Any]) -> dict[str, Any] | None:
    evidence = entry.get("evidence")
    if not isinstance(evidence, list):
        return None
    accepted: dict[str, list[dict[str, Any]]] = {"control": [], "treatment": []}
    for item in evidence:
        if not isinstance(item, dict):
            continue
        arm = str(item.get("arm", "")).lower()
        digest = str(item.get("artifact_sha256", "")).lower()
        receipt = item.get("review_receipt")
        if arm not in accepted or not SHA_RE.fullmatch(digest) or not isinstance(receipt, dict):
            continue
        if str(receipt.get("artifact_sha256", "")).lower() != digest:
            continue
        verdict = str(receipt.get("verdict", "")).upper()
        if verdict not in {"PASS", "FAIL"}:
            continue
        accepted[arm].append({"artifact_sha256": digest, "verdict": verdict})
    minimum = int(trial["replicates_per_arm"])
    if any(len(accepted[arm]) < minimum for arm in accepted):
        return None
    return {
        "control_n": len(accepted["control"]),
        "treatment_n": len(accepted["treatment"]),
        "control_passes": sum(x["verdict"] == "PASS" for x in accepted["control"]),
        "treatment_passes": sum(x["verdict"] == "PASS" for x in accepted["treatment"]),
        "evidence_items": len(accepted["control"]) + len(accepted["treatment"]),
        "evidence_binding": "MATCHED_ARTIFACT_SHA256_PER_RECEIPT"
    }


def reviewed_results(history: dict[str, Any] | None) -> tuple[dict[str, dict[str, Any]], list[str]]:
    completed: dict[str, dict[str, Any]] = {}
    ignored: list[str] = []
    records = history.get("reviewed_trials", []) if isinstance(history, dict) else []
    if not isinstance(records, list):
        return completed, ["history.reviewed_trials is not a list"]
    for entry in records:
        if not isinstance(entry, dict):
            continue
        trial_id = str(entry.get("trial_id", ""))
        trial = TRIAL_BY_ID.get(trial_id)
        if trial is None:
            ignored.append(f"{trial_id or 'MISSING_TRIAL_ID'}: unknown trial")
            continue
        counts = _evidence_counts(entry, trial)
        if counts is None:
            ignored.append(f"{trial_id}: incomplete or SHA-mismatched arm evidence; not counted as reviewed")
            continue
        completed[trial_id] = counts
    return completed, ignored


def build_trial_plan(
    history: dict[str, Any] | None = None,
    family: str = "all",
    limit: int = 3
) -> dict[str, Any]:
    if limit < 1 or limit > 20:
        raise ValueError("limit must be between 1 and 20")
    if family not in {*FAMILY_ALIASES.keys(), *(t["family"] for t in TRIALS)}:
        raise ValueError(f"unknown family: {family}")
    completed, ignored = reviewed_results(history)
    allowed = FAMILY_ALIASES[family] if family in FAMILY_ALIASES else {family}
    candidates: list[dict[str, Any]] = []
    blocked: list[dict[str, Any]] = []
    for trial in TRIALS:
        if allowed is not None and trial["family"] not in allowed:
            continue
        if trial["trial_id"] in completed:
            continue
        missing = [dependency for dependency in trial["dependencies"] if dependency not in completed]
        if missing:
            blocked.append({"trial_id": trial["trial_id"], "blocked_by": missing})
            continue
        candidates.append(dict(trial))
        if len(candidates) >= limit:
            break
    return {
        "schema_version": 1,
        "planner": "DETERMINISTIC_PREREGISTERED_TRIAL_CATALOG",
        "plan_status": "PLAN_READY" if candidates else "NO_ELIGIBLE_TRIALS",
        "family_filter": family,
        "plan_only": True,
        "external_generation_called": False,
        "reviewed_trial_results": completed,
        "ignored_history": ignored,
        "blocked_candidates": blocked,
        "next_trials": candidates,
        "notes": [
            "This schedules what to try next; it does not tell you that a single prompt edit is the answer.",
            "A trial is complete only after each control/treatment arm has enough review receipts whose artifact SHA-256 matches the recorded artifact SHA-256.",
            "A PASS receipt is an external reviewer assertion; matching hashes bind the receipt to an artifact but do not authenticate the reviewer or make this planner a vision model.",
            "Three replicates per arm are a screening design, not statistical proof. Record every hard-gate failure and do not promote an unreviewed candidate."
        ]
    }


def trial_card(trial: dict[str, Any]) -> str:
    lines = [
        f"# {trial['trial_id']} — {trial['title']}",
        "",
        f"**Family:** {trial['family']}",
        f"**Objective:** {trial['objective']}",
        f"**Hypothesis (untested):** {trial['hypothesis']}",
        "",
        "## Arms",
        "",
        f"### {trial['control']['label']}",
        f"Kind: {trial['control']['kind']}",
        "",
        trial["control"]["payload"],
        "",
        f"### {trial['treatment']['label']}",
        f"Kind: {trial['treatment']['kind']}",
        "",
        trial["treatment"]["payload"],
        "",
        "## Experimental controls",
        "",
        "Vary only: " + ", ".join(trial["vary_only"]),
        "",
        "Freeze: " + ", ".join(trial["freeze"]),
        "",
        f"Replicates: {trial['replicates_per_arm']} per arm.",
        "",
        "## Score before looking at preference",
        "",
        trial["metric"],
        "",
        "Decision rule: " + trial["success_rule"],
        "",
        "## Required evidence",
        ""
    ]
    lines.extend(f"- {item}" for item in trial["required_artifacts"])
    lines.extend([
        "",
        "## After review",
        "",
        "If treatment wins: " + trial["after_win"],
        "",
        "If tie/loss: " + trial["after_tie_or_loss"],
        "",
        "Do not claim an image/video result until real generated media and the corresponding review receipts exist."
    ])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--history", help="JSON with reviewed_trials and per-artifact SHA-bound review receipts")
    parser.add_argument("--family", choices=["all", "image", "video", *(t["family"] for t in TRIALS)], default="all")
    parser.add_argument("--limit", type=int, default=3, help="maximum number of eligible trials to schedule")
    parser.add_argument("--outdir", required=True, help="where to write the plan, trial cards and per-arm text")
    args = parser.parse_args()
    try:
        history = json.loads(Path(args.history).read_text(encoding="utf-8")) if args.history else None
        plan = build_trial_plan(history, family=args.family, limit=args.limit)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "trial_plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    cards_dir = outdir / "trial_cards"
    cards_dir.mkdir(exist_ok=True)
    for trial in plan["next_trials"]:
        trial_id = trial["trial_id"]
        (cards_dir / f"{trial_id}.md").write_text(trial_card(trial), encoding="utf-8")
        (cards_dir / f"{trial_id}.control.txt").write_text(trial["control"]["payload"].rstrip() + "\n", encoding="utf-8")
        (cards_dir / f"{trial_id}.treatment.txt").write_text(trial["treatment"]["payload"].rstrip() + "\n", encoding="utf-8")
    print(json.dumps({
        "plan_status": plan["plan_status"],
        "family_filter": plan["family_filter"],
        "next_trial_ids": [item["trial_id"] for item in plan["next_trials"]],
        "trial_card_dir": str(cards_dir),
        "plan_file": str(outdir / "trial_plan.json"),
        "plan_only": True,
        "external_generation_called": False
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
