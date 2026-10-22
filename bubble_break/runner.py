#!/usr/bin/env python3
"""Executable command-line entry point for the calibrated dual-T -> Bubble-Break pipeline.

This runner never fabricates rasters or annotations. With no provider command it only validates
candidate files already present and reports BLOCKED when the evidence is incomplete. A configured
provider is an external command that must return actual raster paths plus raster-bound evidence.
"""
from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any, Sequence

from bubble_break.dual_t_hammer_collision import compile_dual_hammer_prompt
from bubble_break.frame_pipeline import BUBBLE_BREAK_STAGES, sha256_file
from bubble_break.proxy_edit_pipeline import (
    CandidateBatchEntry,
    RerunProviderFn,
    run_calibrated_bubble_break_closed_loop,
)
from bubble_break.shannon_information_gain import recommend_next_experiment
from bubble_break.closed_loop_evidence_guard import CALIBRATION_SEQUENCE


BUBBLE_STAGE_PROMPTS = {
    "H0_PRE_IMPACT": (
        "Generate ONE full-frame Bubble-Break image. One calibrated rigid T-hammer approaches ONE intact "
        "transparent containment bubble. No contact, glow at P, cracks, holes, or shell fragments. Keep one "
        "camera, one bubble identity, one attacker identity, the existing transverse handle, and a clear positive gap."
    ),
    "H1_PRE_NEAR": (
        "Generate ONE full-frame continuation from the parent raster. Keep the camera, scene, bubble center/radius, "
        "attacking hammer topology, handle joint, character and lighting locked. Reduce the positive gap toward P; "
        "still no contact, impact flash, or cracks."
    ),
    "H2_FIRST_CONTACT": (
        "Generate the exact first-contact instant. Only the calibrated thick terminal striking end-face touches the "
        "bubble at the locked six-o'clock point P; measured gap is zero. No cheek, side head, shaft or handle contact. "
        "The membrane was intact immediately before this instant and only tiny initial cracks begin at P."
    ),
    "H2B_CRACK_PROPAGATION": (
        "Continue from the accepted H2 parent. Keep P and all scene identities fixed. Show the same cracks expanding "
        "radially outward from P; the crack-front radius must increase. Damage the containment membrane only; do not "
        "let shards enter the sanctuary or injure inhabitants."
    ),
    "H3_FOLLOWTHROUGH_SHELL_SHATTER": (
        "Continue from the accepted H2B parent. The containment shell is now shattered outward from the same P; the "
        "crack/front extent increases, while the attacking hammer remains the same rigid object and the inner sanctuary "
        "and all residents remain alive and uninjured. Do not add another impact source or change the camera."
    ),
}


def _resolve_candidate_path(raw_path: str, base_dir: Path) -> Path:
    path = Path(raw_path)
    return path.resolve() if path.is_absolute() else (base_dir / path).resolve()


def _load_candidate_map(raw: Any, base_dir: Path) -> dict[str, list[CandidateBatchEntry]]:
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        raise ValueError("candidate map must be a JSON object keyed by stage")
    result: dict[str, list[CandidateBatchEntry]] = {}
    for stage, candidates in raw.items():
        if not isinstance(candidates, list):
            raise ValueError(f"candidate list for {stage} must be a JSON array")
        batch: list[CandidateBatchEntry] = []
        for index, item in enumerate(candidates):
            if not isinstance(item, dict) or not isinstance(item.get("path"), str):
                raise ValueError(f"{stage}[{index}] must contain a raster 'path'")
            evidence = item.get("evidence")
            if evidence is not None and not isinstance(evidence, dict):
                raise ValueError(f"{stage}[{index}].evidence must be an object or null")
            batch.append((_resolve_candidate_path(item["path"], base_dir), evidence))
        result[str(stage)] = batch
    return result


def _stage_prompt(stage_or_frame_id: str) -> tuple[str, str, str]:
    if stage_or_frame_id.startswith("CAL_"):
        stage = stage_or_frame_id.removeprefix("CAL_")
        return "CALIBRATION", stage, compile_dual_hammer_prompt(stage)
    stage = stage_or_frame_id
    if stage not in BUBBLE_STAGE_PROMPTS:
        raise ValueError(f"unsupported rerun stage: {stage_or_frame_id}")
    return "BUBBLE_BREAK", stage, BUBBLE_STAGE_PROMPTS[stage]


class CommandRerunProvider:
    """Adapter contract for any external image-generation command.

    The external command receives BUBBLE_BREAK_REQUEST_JSON and BUBBLE_BREAK_RESPONSE_JSON environment
    variables. It must generate real image files and write response JSON:
        {"candidates":[{"path":"actual-image.png","evidence":{...}}]}
    Relative candidate paths are resolved against the response JSON's directory. An adapter may call
    Gemini, another image model, or a user-controlled service, but this repository does not claim that
    a provider is connected until the user supplies that command.
    """

    def __init__(self, command: Sequence[str], timeout_seconds: int = 900):
        if not command:
            raise ValueError("provider command must not be empty")
        self.command = list(command)
        self.timeout_seconds = timeout_seconds
        self.attempt_requests: list[dict[str, Any]] = []

    def __call__(
        self,
        stage_or_frame_id: str,
        attempt_index: int,
        parent_image_path: Path | None,
        errors: list[str],
        outdir: Path,
    ) -> list[CandidateBatchEntry]:
        outdir.mkdir(parents=True, exist_ok=True)
        domain, stage, stage_prompt = _stage_prompt(stage_or_frame_id)
        diagnosis = recommend_next_experiment(errors, self.attempt_requests)
        parent_sha = sha256_file(parent_image_path) if parent_image_path and parent_image_path.is_file() else None
        request = {
            "protocol": "BUBBLE_BREAK_IMAGE_PROVIDER_REQUEST_V1",
            "domain": domain,
            "stage": stage,
            "attempt_index": attempt_index,
            "parent_raster_path": str(parent_image_path) if parent_image_path else None,
            "parent_raster_sha256": parent_sha,
            "previous_gate_errors": list(errors),
            "stage_prompt": stage_prompt,
            "diagnostic_experiment": diagnosis["selected_experiment"],
            "entropy_bits_before_diagnostic": diagnosis["uncertainty_entropy_bits"],
            "diagnostic_calibration_status": diagnosis["calibration_status"],
            "hard_rule": (
                "Return actual raster files and annotations for those exact file bytes. Do not set PASS, "
                "do not reuse the parent image as a no-op, do not invent geometry evidence, and do not omit "
                "parent/calibration SHA bindings or stable identity lock IDs."
            ),
        }
        request_path = outdir / f"request_{domain}_{stage}_attempt_{attempt_index:02d}.json"
        response_path = outdir / f"response_{domain}_{stage}_attempt_{attempt_index:02d}.json"
        request_path.write_text(json.dumps(request, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        self.attempt_requests.append({
            "accepted": False,
            "errors": list(errors),
            "stage": stage,
            "diagnostic_experiment_id": diagnosis["selected_experiment"]["action_id"],
        })

        env = os.environ.copy()
        env["BUBBLE_BREAK_REQUEST_JSON"] = str(request_path.resolve())
        env["BUBBLE_BREAK_RESPONSE_JSON"] = str(response_path.resolve())
        completed = subprocess.run(
            self.command,
            env=env,
            timeout=self.timeout_seconds,
            check=False,
            capture_output=True,
            text=True,
        )
        (outdir / f"stdout_{domain}_{stage}_{attempt_index:02d}.txt").write_text(completed.stdout, encoding="utf-8")
        (outdir / f"stderr_{domain}_{stage}_{attempt_index:02d}.txt").write_text(completed.stderr, encoding="utf-8")
        if completed.returncode != 0:
            raise RuntimeError(
                f"provider command failed ({completed.returncode}) for {stage_or_frame_id}; see {request_path.name} stderr receipt"
            )
        if not response_path.is_file():
            raise RuntimeError(
                f"provider command did not write BUBBLE_BREAK_RESPONSE_JSON={response_path}"
            )
        payload = json.loads(response_path.read_text(encoding="utf-8"))
        candidates = payload.get("candidates") if isinstance(payload, dict) else None
        if not isinstance(candidates, list):
            raise ValueError("provider response must contain a 'candidates' array")
        batch: list[CandidateBatchEntry] = []
        for index, item in enumerate(candidates):
            if not isinstance(item, dict) or not isinstance(item.get("path"), str):
                raise ValueError(f"provider candidate {index} must include actual raster path")
            evidence = item.get("evidence")
            if not isinstance(evidence, dict):
                raise ValueError(f"provider candidate {index} must include raster-bound evidence object")
            batch.append((_resolve_candidate_path(item["path"], response_path.parent), evidence))
        return batch


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-manifest", type=Path, required=True, help="JSON manifest containing initial calibration_candidates and bubble_break_candidates")
    parser.add_argument("--outdir", type=Path, default=Path("out/calibrated_bubble_break_closed_loop"))
    parser.add_argument("--provider-command", default=None, help="external command receiving BUBBLE_BREAK_REQUEST_JSON and BUBBLE_BREAK_RESPONSE_JSON")
    parser.add_argument("--provider-timeout-seconds", type=int, default=900)
    parser.add_argument("--max-retries", type=int, default=2)
    parser.add_argument("--locked-pole", type=float, nargs=2, default=(755.0, 384.0), metavar=("X", "Y"))
    args = parser.parse_args(list(argv) if argv is not None else None)

    try:
        manifest_path = args.candidate_manifest.resolve()
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        base_dir = manifest_path.parent
        calibration = _load_candidate_map(manifest.get("calibration_candidates"), base_dir)
        bubble = _load_candidate_map(manifest.get("bubble_break_candidates"), base_dir)
        provider: RerunProviderFn | None = None
        if args.provider_command:
            provider = CommandRerunProvider(shlex.split(args.provider_command), args.provider_timeout_seconds)
        report = run_calibrated_bubble_break_closed_loop(
            args.outdir,
            calibration_candidates=calibration,
            bubble_break_candidates=bubble,
            rerun_provider=provider,
            locked_pole_p_px=(float(args.locked_pole[0]), float(args.locked_pole[1])),
            max_retries=args.max_retries,
        )
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
        if report.status.startswith("BLOCKED"):
            return 2
        if report.code_visual_acceptance_status != "NOT_VERIFIED_BY_CODE":
            return 3
        return 0
    except (OSError, ValueError, json.JSONDecodeError, subprocess.TimeoutExpired, RuntimeError) as exc:
        print(f"BLOCK: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
