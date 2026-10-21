#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bridge bulk story JSONL to one shared T-weapon master and story-specific scene prompt packets. Does not render images."""
from __future__ import annotations
import argparse, json, re, sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List

from frame_pipeline import CAMERA_VARIANTS, compile_frame_set, write_packet as write_frame_packet
from proxy_edit_pipeline import write_packet as write_proxy_packet
from t_contact_matrix import build_matrix, validate_matrix, validate_master_review
from cylinder_cross_contact_matrix import build_matrix as build_cylinder_matrix, validate_matrix as validate_cylinder_matrix

def safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+","_",value).strip("._")[:100] or "story"

def select_records(input_path: Path, per_kernel: int=1, limit: int=20) -> List[Dict[str,Any]]:
    if per_kernel < 1: raise ValueError("--per-kernel must be >= 1")
    if limit < 1: raise ValueError("--limit must be >= 1")
    selected=[]; counts=Counter()
    with input_path.open("r",encoding="utf-8") as handle:
        for line in handle:
            if not line.strip(): continue
            row=json.loads(line)
            kernel=str(row.get("causal_kernel_id") or row.get("root_sin") or "UNASSIGNED")
            if counts[kernel] >= per_kernel: continue
            selected.append(row); counts[kernel]+=1
            if len(selected)>=limit: break
    if not selected: raise ValueError("no records selected from input JSONL")
    return selected

def build_batch(input_path: Path, outdir: Path, per_kernel: int=1, limit: int=20,
                final_weapon: str="T") -> Dict[str,Any]:
    final_weapon=final_weapon.upper()
    if final_weapon not in ("CROSS","T","RADIAL","CYLINDER_CROSS"):
        raise ValueError("--final-weapon must be CROSS, T, RADIAL, or CYLINDER_CROSS")
    records=select_records(input_path,per_kernel,limit)
    outdir.mkdir(parents=True,exist_ok=True)
    packages=[]
    for record in records:
        story_id=str(record.get("story_id") or "STORY-UNKNOWN")
        story_dir=outdir/safe_name(story_id)
        frame_out=story_dir/"frames"
        frame_summaries=[]
        # For T mode, emit a distinct H0/H2/H3 trio for every camera variant.
        camera_ids=list(CAMERA_VARIANTS) if final_weapon in ("T","CYLINDER_CROSS") else ["LOW_3Q_FRONTAL"]
        for camera_id in camera_ids:
            packet=compile_frame_set(record,weapon_topology=final_weapon,camera_variant=camera_id)
            frame_summary=write_frame_packet(packet,frame_out/camera_id)
            frame_summaries.append(frame_summary)
        layout_path=Path(frame_summaries[0]["directory"])/"layout.json"
        proxy_dir=story_dir/"proxy_edit"
        proxy_summary=write_proxy_packet(layout_path,proxy_dir,final_weapon=final_weapon)
        edit_plan=json.loads((proxy_dir/"edit_plan.json").read_text(encoding="utf-8"))
        packages.append({
            "story_id":story_id,
            "causal_kernel_id":record.get("causal_kernel_id") or record.get("root_sin") or "UNASSIGNED",
            "causal_signature":record.get("causal_signature"),
            "final_weapon":final_weapon,
            "frame_directory":str(frame_out),
            "camera_variants":camera_ids,
            "frame_directories":[x["directory"] for x in frame_summaries],
            "proxy_directory":proxy_summary["outdir"],
            "proxy_status":proxy_summary["status"],
            "stage_gate_status":edit_plan.get("stage_gate_status","NO_T_TO_T_GATE"),
            "required_first_stage_artifact":edit_plan.get("required_artifacts",{}).get("stage_a_image"),
            "selected_edit_prompt":edit_plan.get("selected_edit_prompt"),
            "terminal_face_gap_px":proxy_summary["terminal_face_gap_px"],
            "camera_packet_count":len(frame_summaries),
            "frame_prompt_count":len(frame_summaries)*3,
            "image_realization":"NOT_RUN",
            "edited_pixel_audit":"NOT_RUN",
        })
    shared_master_dir=None
    contact_gate_status="NO_T_TO_T_GATE"
    contact_audit=None
    master_audit=None
    if final_weapon=="T":
        # One shape master is shared across the whole batch; do not redraw an identical master per story.
        shared_master_dir=outdir/"_shared_T_weapon_master"
        shared_master_dir.mkdir(parents=True,exist_ok=True)
        first_proxy=Path(packages[0]["proxy_directory"])
        shared_names=("00_T_weapon_master_geometry.svg","00_generate_T_weapon_master.txt",
                      "05_T_silhouette_reference.svg","A_T_weapon_master_review.template.json","stage_gate.json")
        for name in shared_names:
            src=first_proxy/name
            if not src.exists():
                raise ValueError(f"shared T master source missing: {src}")
            (shared_master_dir/name).write_text(src.read_text(encoding="utf-8"),encoding="utf-8")
        contact_dir=shared_master_dir/"contact_matrix"
        contact_manifest=build_matrix(contact_dir)
        contact_audit=validate_matrix(contact_dir)
        master_audit=validate_master_review(
            shared_master_dir/"A_T_weapon_master.png",
            shared_master_dir/"A_T_weapon_master_review.json",
        )
        matrix_and_master_approved=(
            contact_audit["overall_status"]=="PASS_MANUAL_REVIEW_RECORDED"
            and master_audit["status"]=="PASS_MANUAL_REVIEW_RECORDED"
        )
        contact_gate_status="T_CONTACT_MATRIX_APPROVED" if matrix_and_master_approved else "BLOCKED_UNTIL_T_CONTACT_MATRIX_APPROVED"
        shared_gate_path=shared_master_dir/"stage_gate.json"
        shared_gate=json.loads(shared_gate_path.read_text(encoding="utf-8"))
        shared_gate["status"]=contact_gate_status
        shared_gate["required_order"]=["A_T_WEAPON_MASTER","B_T_TO_T_END_FACE_CONTACT_MATRIX","C_STORY_SPECIFIC_SCENE_CAMERA_SWEEPS"]
        shared_gate["required_stage_a_artifact"]="A_T_weapon_master.png"
        shared_gate["required_stage_a_review"]="A_T_weapon_master_review.json"
        shared_gate["required_contact_matrix_manifest"]=str(contact_dir/"contact_matrix_manifest.json")
        shared_gate["required_contact_matrix_h2_images"]=contact_manifest["required_H2_contact_proof_images"]
        shared_gate["required_contact_matrix_h2_reviews"]="one manual review JSON per variant, all face-plane checks true"
        shared_gate["contact_matrix_audit_report"]=str(contact_dir/"contact_matrix_audit_report.json")
        shared_gate["contact_matrix_audit_status"]=contact_audit["overall_status"]
        shared_gate["master_review_status"]=master_audit["status"]
        shared_gate["master_review_issues"]=master_audit["issues"]
        shared_gate["scope"]="SHARED_ACROSS_BATCH"
        shared_gate["note"]="CI compiles 144 prompts; only generated and visually approved H2 images can pass the matrix."
        shared_gate_path.write_text(json.dumps(shared_gate,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        for package in packages:
            proxy=Path(package["proxy_directory"])
            plan_path=proxy/"edit_plan.json"
            plan=json.loads(plan_path.read_text(encoding="utf-8"))
            plan["master_scope"]="SHARED_ACROSS_BATCH"
            plan["shared_weapon_master_directory"]=str(shared_master_dir)
            plan["required_artifacts"]["stage_a_image"]=str(shared_master_dir/"A_T_weapon_master.png")
            plan["required_artifacts"]["stage_a_review"]=str(shared_master_dir/"A_T_weapon_master_review.json")
            plan["required_artifacts"]["stage_a_review_template"]=str(shared_master_dir/"A_T_weapon_master_review.template.json")
            plan["required_artifacts"]["contact_matrix_manifest"]=str(contact_dir/"contact_matrix_manifest.json")
            plan["required_artifacts"]["contact_matrix_h2_images"]=contact_manifest["required_H2_contact_proof_images"]
            plan["required_artifacts"]["contact_matrix_h2_reviews"]="one manual review JSON per variant"
            plan["status"]=contact_gate_status
            plan["stage_gate_status"]=contact_gate_status
            plan["contact_matrix_audit_status"]=contact_audit["overall_status"]
            plan["master_review_status"]=master_audit["status"]
            plan["stage_gate_file"]=str(shared_master_dir/"stage_gate.json")
            plan["files"]["proxy"]=str(shared_master_dir/"00_T_weapon_master_geometry.svg")
            plan["files"]["t_shape_reference"]=str(shared_master_dir/"05_T_silhouette_reference.svg")
            plan["files"]["t_weapon_master_generation_prompt"]=str(shared_master_dir/"00_generate_T_weapon_master.txt")
            plan_path.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
            local_gate=proxy/"stage_gate.json"
            gate=json.loads(local_gate.read_text(encoding="utf-8"))
            gate["required_stage_a_artifact"]=str(shared_master_dir/"A_T_weapon_master.png")
            gate["required_stage_a_review"]=str(shared_master_dir/"A_T_weapon_master_review.json")
            gate["status"]=contact_gate_status
            gate["contact_matrix_audit_status"]=contact_audit["overall_status"]
            gate["master_review_status"]=master_audit["status"]
            gate["required_contact_matrix_manifest"]=str(contact_dir/"contact_matrix_manifest.json")
            gate["required_contact_matrix_h2_images"]=contact_manifest["required_H2_contact_proof_images"]
            gate["shared_master_directory"]=str(shared_master_dir)
            local_gate.write_text(json.dumps(gate,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
            # Promote the per-camera scene packet only when both real-image review gates pass.
            for frame_dir in package["frame_directories"]:
                frame_path=Path(frame_dir)
                frame_manifest_path=frame_path/"manifest.json"
                frame_manifest=json.loads(frame_manifest_path.read_text(encoding="utf-8"))
                frame_gate=frame_manifest.get("realization_stage_gate",{})
                frame_gate["status"]=contact_gate_status
                frame_gate["contact_matrix_audit_status"]=contact_audit["overall_status"]
                frame_gate["master_review_status"]=master_audit["status"]
                frame_manifest["realization_stage_gate"]=frame_gate
                frame_manifest.setdefault("workflow",{})["realization_stage_gate"]=contact_gate_status
                frame_manifest_path.write_text(json.dumps(frame_manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
                frame_gate_path=frame_path/"stage_gate.json"
                frame_gate_path.write_text(json.dumps(frame_gate,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
            for name in ("00_T_weapon_master_geometry.svg","00_generate_T_weapon_master.txt","05_T_silhouette_reference.svg","A_T_weapon_master_review.template.json"):
                candidate=proxy/name
                if candidate.exists():
                    candidate.unlink()
            package["required_first_stage_artifact"]=str(shared_master_dir/"A_T_weapon_master.png")
            package["stage_gate_status"]=contact_gate_status
            package["contact_matrix_audit_status"]=contact_audit["overall_status"]
            package["master_review_status"]=master_audit["status"]
            package["shared_weapon_master_directory"]=str(shared_master_dir)
            package["contact_matrix_manifest"]=str(contact_dir/"contact_matrix_manifest.json")
            package["required_contact_matrix_h2_images"]=contact_manifest["required_H2_contact_proof_images"]
            package["selected_edit_prompt"]=str(proxy/"generate_scene_with_T_master.txt")

    elif final_weapon=="CYLINDER_CROSS":
        # A clean, independent 48-variant end-cap matrix. Old T evidence is never read or copied.
        shared_master_dir=outdir/"_shared_CYLINDER_CROSS_contact"
        shared_master_dir.mkdir(parents=True,exist_ok=True)
        contact_dir=shared_master_dir/"contact_matrix"
        contact_manifest=build_cylinder_matrix(contact_dir)
        contact_audit=validate_cylinder_matrix(contact_dir)
        contact_gate_status=(
            "CYLINDER_CROSS_CONTACT_MATRIX_APPROVED"
            if contact_audit["overall_status"]=="PASS_MANUAL_REVIEW_RECORDED"
            else "BLOCKED_UNTIL_CYLINDER_CROSS_CONTACT_MATRIX_APPROVED"
        )
        shared_gate={
            "status":contact_gate_status,
            "required_order":["A_CYLINDER_CROSS_END_CAP_CONTACT_MATRIX","B_STORY_SPECIFIC_SCENE_CAMERA_SWEEPS_H0_H2_H3"],
            "topology":"CYLINDER_CROSS",
            "required_contact_matrix_manifest":str(contact_dir/"contact_matrix_manifest.json"),
            "required_contact_matrix_h2_images":48,
            "required_contact_matrix_h2_reviews":"one explicit manual pixel-review JSON per variant; all checks true",
            "contact_matrix_audit_report":str(contact_dir/"contact_matrix_audit_report.json"),
            "contact_matrix_audit_status":contact_audit["overall_status"],
            "image_realization":"NOT_RUN",
            "pixel_audit":"NOT_RUN",
            "do_not_transfer_old_T_evidence":True,
            "note":"A prompt/SVG or the legacy T batch is not evidence. All 48 actual H2 images must be independently generated and manually reviewed."
        }
        (shared_master_dir/"stage_gate.json").write_text(json.dumps(shared_gate,ensure_ascii=False,indent=2)+"\\n",encoding="utf-8")
        for package in packages:
            proxy=Path(package["proxy_directory"])
            plan_path=proxy/"edit_plan.json"
            plan=json.loads(plan_path.read_text(encoding="utf-8"))
            plan["status"]=contact_gate_status
            plan["stage_gate_status"]=contact_gate_status
            plan["shared_contact_matrix_directory"]=str(contact_dir)
            plan.setdefault("required_artifacts",{})["contact_matrix_manifest"]=str(contact_dir/"contact_matrix_manifest.json")
            plan["required_artifacts"]["contact_matrix_h2_image_count"]=48
            plan["required_artifacts"]["contact_matrix_h2_reviews"]="one manually reviewed JSON per variant"
            plan["contact_matrix_audit_status"]=contact_audit["overall_status"]
            plan["stage_gate_file"]=str(shared_master_dir/"stage_gate.json")
            plan.setdefault("pixel_truth",{})["contact_matrix_images"]="NOT_RUN"
            plan["pixel_truth"]["edited_images"]="NOT_RUN"
            plan["pixel_truth"]["warning"]="All 48 fresh cylinder-cross H2 images require human pixel review; legacy T images are explicitly excluded."
            plan_path.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+"\\n",encoding="utf-8")
            local_gate=proxy/"stage_gate.json"
            gate={
                "status":contact_gate_status,
                "topology":"CYLINDER_CROSS",
                "required_contact_matrix_manifest":str(contact_dir/"contact_matrix_manifest.json"),
                "required_contact_matrix_h2_images":48,
                "contact_matrix_audit_status":contact_audit["overall_status"],
                "shared_contact_matrix_directory":str(contact_dir),
                "do_not_transfer_old_T_evidence":True,
                "manual_visual_approval_required":True
            }
            local_gate.write_text(json.dumps(gate,ensure_ascii=False,indent=2)+"\\n",encoding="utf-8")
            for frame_dir in package["frame_directories"]:
                frame_path=Path(frame_dir)
                manifest_path=frame_path/"manifest.json"
                fm=json.loads(manifest_path.read_text(encoding="utf-8"))
                fg=fm.setdefault("realization_stage_gate",{})
                fg.update({"status":contact_gate_status,
                           "required_contact_matrix_manifest":str(contact_dir/"contact_matrix_manifest.json"),
                           "required_contact_matrix_h2_images":48,
                           "contact_matrix_audit_status":contact_audit["overall_status"],
                           "do_not_transfer_old_T_evidence":True})
                fm["workflow"]["realization_stage_gate"]=contact_gate_status
                manifest_path.write_text(json.dumps(fm,ensure_ascii=False,indent=2)+"\\n",encoding="utf-8")
                (frame_path/"stage_gate.json").write_text(json.dumps(fg,ensure_ascii=False,indent=2)+"\\n",encoding="utf-8")
            package["stage_gate_status"]=contact_gate_status
            package["contact_matrix_audit_status"]=contact_audit["overall_status"]
            package["shared_contact_matrix_directory"]=str(contact_dir)
            package["contact_matrix_manifest"]=str(contact_dir/"contact_matrix_manifest.json")
            package["required_contact_matrix_h2_images"]=48
            package["selected_edit_prompt"]=str(proxy/"edit_attacker_cylinder_cross.txt")

    batch={
        "pipeline_version":"1.2.0",
        "input":str(input_path),
        "requested_per_kernel":per_kernel,
        "requested_limit":limit,
        "selected_stories":len(packages),
        "distinct_causal_kernels":len({p["causal_kernel_id"] for p in packages}),
        "final_weapon":final_weapon,
        "method":("bulk JSONL -> one shared T-weapon master -> stratified 48-variant T-to-T terminal-end-face matrix -> story-specific 12-camera sweeps" if final_weapon=="T"
                  else "bulk JSONL -> fresh CYLINDER_CROSS 48-variant flat-end-cap matrix -> fail-closed approval gate -> story-specific 12-camera sweeps" if final_weapon=="CYLINDER_CROSS"
                  else "bulk JSONL -> per-story frame packet -> cross proxy -> target-only sphere edit plan -> final weapon edit plan"),
        "stage_gate_status":(contact_gate_status if final_weapon in ("T","CYLINDER_CROSS") else "NO_T_TO_T_GATE"),
        "required_first_stage":("A_T_WEAPON_MASTER_AND_CONTACT_MATRIX" if final_weapon=="T" else "A_CYLINDER_CROSS_END_CAP_CONTACT_MATRIX" if final_weapon=="CYLINDER_CROSS" else None),
        "shared_weapon_master_directory":(str(shared_master_dir) if shared_master_dir else None),
        "contact_matrix_manifest":(str(shared_master_dir/"contact_matrix"/"contact_matrix_manifest.json") if shared_master_dir else None),
        "contact_matrix_audit_report":(str(shared_master_dir/"contact_matrix"/"contact_matrix_audit_report.json") if shared_master_dir else None),
        "contact_matrix_audit_status":(contact_audit["overall_status"] if contact_audit else "NOT_APPLICABLE"),
        "master_review_status":(master_audit["status"] if master_audit else "NOT_APPLICABLE"),
        "contact_matrix_variants":(48 if final_weapon in ("T","CYLINDER_CROSS") else 0),
        "contact_matrix_prompt_count":(144 if final_weapon in ("T","CYLINDER_CROSS") else 0),
        "scene_camera_variants_per_story":(len(CAMERA_VARIANTS) if final_weapon in ("T","CYLINDER_CROSS") else 1),
        "scene_frame_prompt_count":sum(p["frame_prompt_count"] for p in packages),
        "image_realization":"NOT_RUN",
        "pixel_audit_status":"NOT_RUN",
        "packages":packages,
    }
    (outdir/"realize_batch_manifest.json").write_text(json.dumps(batch,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return batch

def main(argv=None):
    parser=argparse.ArgumentParser(description="Select a small per-kernel sample from bulk JSONL and compile edit packets; no AI render is run.")
    parser.add_argument("--input",required=True)
    parser.add_argument("--outdir",required=True)
    parser.add_argument("--per-kernel",type=int,default=1)
    parser.add_argument("--limit",type=int,default=20)
    parser.add_argument("--final-weapon",choices=("CROSS","T","RADIAL","CYLINDER_CROSS"),default="T")
    args=parser.parse_args(argv)
    try: result=build_batch(Path(args.input),Path(args.outdir),args.per_kernel,args.limit,args.final_weapon)
    except (OSError,ValueError,json.JSONDecodeError) as exc:
        print("BLOCK: "+str(exc),file=sys.stderr); return 2
    print(json.dumps({k:result[k] for k in ("selected_stories","distinct_causal_kernels","final_weapon","image_realization","pixel_audit_status")},
                     ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__": raise SystemExit(main())
