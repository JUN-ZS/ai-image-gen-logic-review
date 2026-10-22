#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H9 — Grok Imagine planted-cylinder Bubble-Break closed loop (no GEMINI_API_KEY).

Design
------
- Same contract as ``planted_bubble_closed_loop``:
  ``PLANTED_DOUBLE_ENDED_CYLINDER_BUBBLE_CONTACT_V1``
  stages B → C → D1 → D2 → D3 → E_MID → E_END
- Image generation is **not** done by Google. The provider is:
  1. **agent-driven**: a Grok Imagine session produces each serial full-frame
     from the compiled stage packet (recommended live path), or
  2. **file-ingest**: you drop pre-generated PNGs/JPGs into the stage spool
     and H9 hashes + manifests them.

This module never invents synthetic PASS pixels, never upgrades FAIL reviews,
and always leaves ``code_visual_acceptance_status=NOT_VERIFIED_BY_CODE``.

CLI
---
Compile stage packets (for the Imagine agent)::

    python -m bubble_break.imagine_planted_bubble_h9 compile \\
      --master-b3 path/to/B3.jpg \\
      --person-ref path/to/her.jpg \\
      --outdir out/h9_packet

Ingest a finished serial run (agent already generated files)::

    python -m bubble_break.imagine_planted_bubble_h9 ingest \\
      --packet-dir out/h9_packet \\
      --rasters-dir out/h9_rasters \\
      --outdir out/h9_run

``rasters-dir`` must contain one file per stage name, e.g.::

    B_LOCKED_TOOL_MASTER.jpg
    C_PERSON_SCALE_NO_GRIP.jpg
    ...
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

from PIL import Image

from bubble_break.planted_bubble_closed_loop import (
    CONTRACT_ID,
    GLOBAL_LOCKS,
    STAGE_ORDER,
    STAGE_SPECS,
    contract_fingerprint,
    sha256_file,
)

H9_ID = "H9_IMAGINE_PLANTED_BUBBLE_CLOSED_LOOP_V1"
H9_PROVIDER = "grok_imagine_serial_fullframe"
VISUAL = "NOT_VERIFIED_BY_CODE"


@dataclass
class StageArtifact:
    stage: str
    label_zh: str
    prompt_path: str
    parent_stage: str | None
    authorized_delta_fields: list[str]
    must_preserve: list[str]


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _locks_block() -> str:
    return "\n".join(f"- {item}" for item in GLOBAL_LOCKS)


def compile_stage_prompt(stage: str, *, master_note: str, person_note: str) -> str:
    if stage not in STAGE_SPECS:
        raise KeyError(stage)
    spec = STAGE_SPECS[stage]
    return f"""# H9 / {H9_ID}
# CONTRACT {CONTRACT_ID}
# STAGE {stage} — {spec['label_zh']}
# provider={H9_PROVIDER}  (NO GEMINI_API_KEY required)

## Master
{master_note}

## Person (when stage requires actor)
{person_note}

## GLOBAL LOCKS
{_locks_block()}

## AUTHORIZED DELTA ONLY
{json.dumps(spec['authorized_delta_fields'], ensure_ascii=False)}

## MUST PRESERVE
{json.dumps(spec['must_preserve'], ensure_ascii=False)}

## STAGE PROMPT
{spec['prompt']}

## HARD OUTPUT RULES
- One serial full-frame photoreal image (16:9 preferred). NEVER a multi-cell control sheet.
- NO_NEW_HANDLE: outer circular end cap EMPTY; only the pre-existing side-middle lateral handle.
- Planted at P; cylinder axis = local bubble normal; glow only at conformal base seat.
- When person present: MINIATURE scale (full-body area ≈ hammer area); identity locked.
- D2 first grip: hands move to the existing side handle pixels — never invent a rod.
- E stages: cracks/shatter originate at the same P; shell only; sanctuary safe if present.
- code_visual_acceptance_status remains {VISUAL} until human pixel review.
"""


def compile_h9_packet(
    *,
    outdir: str | Path,
    master_b3: str | Path,
    person_ref: str | Path | None = None,
    aspect: str = "16:9",
) -> dict[str, Any]:
    """Write prompt packets + source copies for an agent-driven Imagine run."""
    root = Path(outdir).resolve()
    root.mkdir(parents=True, exist_ok=True)
    prompts = root / "prompts"
    sources = root / "sources"
    prompts.mkdir(exist_ok=True)
    sources.mkdir(exist_ok=True)

    master = Path(master_b3).resolve()
    if not master.is_file():
        raise FileNotFoundError(f"master B3 missing: {master}")
    master_dst = sources / f"B3_MASTER{master.suffix.lower() or '.jpg'}"
    shutil.copy2(master, master_dst)
    master_sha = sha256_file(master_dst)

    person_sha = None
    person_dst = None
    if person_ref:
        pref = Path(person_ref).resolve()
        if not pref.is_file():
            raise FileNotFoundError(f"person ref missing: {pref}")
        person_dst = sources / f"PERSON_REF{pref.suffix.lower() or '.jpg'}"
        shutil.copy2(pref, person_dst)
        person_sha = sha256_file(person_dst)

    master_note = f"B3 geometry master file={master_dst.name} sha256={master_sha}"
    person_note = (
        f"Heroine identity file={person_dst.name} sha256={person_sha}"
        if person_dst
        else "No person ref supplied — stages C+ must still use a fixed mini identity."
    )

    artifacts: list[dict[str, Any]] = []
    parent: str | None = None
    for stage in STAGE_ORDER:
        text = compile_stage_prompt(stage, master_note=master_note, person_note=person_note)
        path = prompts / f"{stage}.md"
        path.write_text(text, encoding="utf-8")
        spec = STAGE_SPECS[stage]
        artifacts.append(
            asdict(
                StageArtifact(
                    stage=stage,
                    label_zh=str(spec["label_zh"]),
                    prompt_path=str(path.relative_to(root)),
                    parent_stage=parent,
                    authorized_delta_fields=list(spec["authorized_delta_fields"]),
                    must_preserve=list(spec["must_preserve"]),
                )
            )
        )
        parent = stage

    agent_playbook = root / "AGENT_PLAYBOOK.md"
    agent_playbook.write_text(
        f"""# H9 Imagine agent playbook

1. Start from `sources/B3_MASTER…` as the Stage-B parent (or isolate to B if atlas was denser).
2. For each stage in order, open `prompts/<STAGE>.md` and run **one** full-frame Imagine
   image-to-image (or reference-to-image when person is introduced) edit.
3. Never skip D1/D2. First grip must lock existing side-handle pixels.
4. Save outputs as `rasters/<STAGE>.jpg` (or `.png`) with exact STAGE_ORDER names.
5. Run `python -m bubble_break.imagine_planted_bubble_h9 ingest …` to hash + filmstrip.

Aspect target: **{aspect}**
Contract: `{CONTRACT_ID}` / fingerprint `{contract_fingerprint()}`
No `GEMINI_API_KEY` is used in H9.
""",
        encoding="utf-8",
    )

    packet = {
        "h9_id": H9_ID,
        "contract_id": CONTRACT_ID,
        "contract_sha256": contract_fingerprint(),
        "provider": H9_PROVIDER,
        "compiled_at_utc": _utc_now(),
        "aspect": aspect,
        "master_b3_sha256": master_sha,
        "person_ref_sha256": person_sha,
        "stage_order": list(STAGE_ORDER),
        "stages": artifacts,
        "code_visual_acceptance_status": VISUAL,
        "paths": {
            "prompts": "prompts/",
            "sources": "sources/",
            "playbook": "AGENT_PLAYBOOK.md",
        },
    }
    (root / "H9_PACKET.json").write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return packet


def _find_raster(rasters_dir: Path, stage: str) -> Path:
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        candidate = rasters_dir / f"{stage}{ext}"
        if candidate.is_file() and candidate.stat().st_size > 0:
            return candidate
        locked = rasters_dir / f"LOCKED_{stage}{ext}"
        if locked.is_file() and locked.stat().st_size > 0:
            return locked
    raise FileNotFoundError(f"missing raster for stage {stage} under {rasters_dir}")


def ingest_h9_run(
    *,
    packet_dir: str | Path,
    rasters_dir: str | Path,
    outdir: str | Path,
) -> dict[str, Any]:
    """Hash serial rasters into a run manifest + filmstrip. No network."""
    packet_path = Path(packet_dir).resolve()
    rasters_path = Path(rasters_dir).resolve()
    out = Path(outdir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    locked_dir = out / "rasters"
    locked_dir.mkdir(exist_ok=True)

    packet_file = packet_path / "H9_PACKET.json"
    packet = json.loads(packet_file.read_text(encoding="utf-8")) if packet_file.is_file() else {}

    stage_rows: list[dict[str, Any]] = []
    images: list[Image.Image] = []
    parent_sha: str | None = None
    for stage in STAGE_ORDER:
        src = _find_raster(rasters_path, stage)
        dst = locked_dir / f"LOCKED_{stage}{src.suffix.lower()}"
        shutil.copy2(src, dst)
        digest = sha256_file(dst)
        with Image.open(dst) as im:
            size = list(im.size)
            images.append(im.convert("RGB").copy())
        stage_rows.append(
            {
                "stage": stage,
                "label_zh": STAGE_SPECS[stage]["label_zh"],
                "raster_path": str(dst.relative_to(out)),
                "raster_sha256": digest,
                "parent_raster_sha256": parent_sha,
                "size_px": size,
                "no_op_from_parent": bool(parent_sha and digest == parent_sha),
            }
        )
        parent_sha = digest

    # filmstrip
    h = 280
    scaled = [im.resize((max(1, int(im.width * h / im.height)), h)) for im in images]
    total_w = sum(s.width for s in scaled) + 4 * (len(scaled) - 1)
    strip = Image.new("RGB", (total_w, h), (0, 0, 0))
    x = 0
    for tile in scaled:
        strip.paste(tile, (x, 0))
        x += tile.width + 4
    strip_path = out / "H9_7STAGE_STRIP.jpg"
    strip.save(strip_path, quality=92)

    manifest = {
        "h9_id": H9_ID,
        "workflow": H9_ID,
        "contract_id": CONTRACT_ID,
        "contract_sha256": packet.get("contract_sha256") or contract_fingerprint(),
        "provider": H9_PROVIDER,
        "ingested_at_utc": _utc_now(),
        "packet_master_b3_sha256": packet.get("master_b3_sha256"),
        "total_stages": len(STAGE_ORDER),
        "stages_present": len(stage_rows),
        "all_stages_ingested": len(stage_rows) == len(STAGE_ORDER),
        "any_no_op_child": any(row["no_op_from_parent"] for row in stage_rows if row["parent_raster_sha256"]),
        "code_visual_acceptance_status": VISUAL,
        "limitation": (
            "H9 hashes and orders agent-generated rasters under the planted-cylinder contract. "
            "It does not call Gemini, does not claim human visual PASS, and does not invent pixels."
        ),
        "stages": stage_rows,
        "filmstrip_path": str(strip_path.relative_to(out)),
        "filmstrip_sha256": sha256_file(strip_path),
    }
    (out / "H9_RUN_MANIFEST.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_compile = sub.add_parser("compile", help="Compile H9 stage prompt packet from B3 + optional person ref")
    p_compile.add_argument("--master-b3", required=True, type=Path)
    p_compile.add_argument("--person-ref", type=Path, default=None)
    p_compile.add_argument("--outdir", required=True, type=Path)
    p_compile.add_argument("--aspect", default="16:9")

    p_ingest = sub.add_parser("ingest", help="Ingest serial Imagine rasters into H9 run manifest")
    p_ingest.add_argument("--packet-dir", required=True, type=Path)
    p_ingest.add_argument("--rasters-dir", required=True, type=Path)
    p_ingest.add_argument("--outdir", required=True, type=Path)

    p_show = sub.add_parser("show-contract", help="Print contract id + stage order")
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.cmd == "compile":
        packet = compile_h9_packet(
            outdir=args.outdir,
            master_b3=args.master_b3,
            person_ref=args.person_ref,
            aspect=args.aspect,
        )
        print(json.dumps({"ok": True, "h9_id": packet["h9_id"], "stages": len(packet["stage_order"]), "outdir": str(args.outdir)}, ensure_ascii=False))
        return 0
    if args.cmd == "ingest":
        manifest = ingest_h9_run(packet_dir=args.packet_dir, rasters_dir=args.rasters_dir, outdir=args.outdir)
        print(json.dumps({"ok": True, "all_stages_ingested": manifest["all_stages_ingested"], "outdir": str(args.outdir), "visual": VISUAL}, ensure_ascii=False))
        return 0
    if args.cmd == "show-contract":
        print(json.dumps({"h9_id": H9_ID, "contract_id": CONTRACT_ID, "stages": list(STAGE_ORDER), "provider": H9_PROVIDER}, indent=2))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
