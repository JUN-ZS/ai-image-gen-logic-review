#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compile image-followable keyframe prompts; this program does not render images."""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path
from typing import Any, Dict, List

VERSION = "1.0.0"
FRAME_IDS = ("H0", "H2", "H3")
FRAME_NAMES = {"H0":"H0_pre_impact", "H2":"H2_first_contact_anchor", "H3":"H3_post_impact"}
NEGATIVE = (
    "collage, diptych, triptych, storyboard sheet, contact sheet, multi-panel layout, infographic, "
    "labels, captions, typography, watermark, logo, diagram, weapon turntable, duplicate heroine, extra limbs, "
    "spear through sphere center, shaft touching shell, broad cheek touching target, conventional rectangular hammer, "
    "spikes, studs, mace, flail, chain, separate hammers in a ring, four-headed cross hammer, premature cracks, "
    "cracks away from contact point, explosion replacing shell, shards piercing residents, injured residents, destroyed city"
)
COMMON = (
    "ONE standalone cinematic frame, 16:9 widescreen, photorealistic live-action fantasy still. "
    "One full-bleed image, not a page, not a storyboard, not a comparison, not a collage. No writing, letters, "
    "labels, panel borders, inset images, diagrams or watermark. FIXED SHOT: low three-quarter frontal wide shot, "
    "35mm cinema lens, fixed tripod, same horizon, vanishing lines, architecture landmarks, camera distance, "
    "sphere center and scale in every frame. A giant transparent iridescent bubble encloses a visible floating city "
    "and tiny residents; the lower pole is unobstructed. Heroine stays in the lower-left third, bubble occupies "
    "upper/central frame, P is the exact six-o'clock bottom pole. Keep negative space around P so the gap/contact "
    "can be judged from pixels. ONE realistic East Asian female warrior, long straight center-parted dark-brown hair, "
    "natural makeup, expressive eyes, black leather combat outfit with straps and gloves, consistent face/costume, "
    "both hands on the same handle. No second heroine. CANONICAL WEAPON: ONE long rigid handle + ONE compact "
    "near-spherical dense steel hammer head. The head looks spherical because many broad, flat polygonal sledgehammer "
    "striking faces tile its surface and point radially outward. These are flat faces, not spikes, studs, blades, "
    "a halo, chain, or separate hammers. Keep several flat faces readable. At impact, only the single upper-facing "
    "flat polygon contacts the shell; its outline is visible, while head side walls and other faces remain lateral. "
    "The handle runs diagonally down-left toward the heroine, not through the bubble center like a spear. POWER CUES: "
    "planted wide stance, legs driving from ground, visible hip and torso rotation, shoulders accelerating into late "
    "arm extension, hair/clothing trailing the swing. Do not substitute raised arms or blur for force. Keep contact "
    "geometry sharp. The target is the containment membrane, never the residents; city and residents remain intact."
)
STATE = {
"H0": (
    "PRE-IMPACT START FRAME. Bubble membrane perfectly intact: zero cracks, holes, fragments or explosion. Hammer "
    "is pulled back below and slightly left of P in a loaded diagonal backswing. Center of its upper-facing flat "
    "striking polygon aims at P, but a clearly visible continuous band of empty air separates that polygon from "
    "the bottom membrane. No contact, spark or pre-impact crack. Heroine's feet are grounded, knees flexed, hips "
    "and torso coiled, both hands gripping the handle at separated positions. The gap must not be hidden by glare, "
    "hair, ornament or the sphere."
),
"H2": (
    "EXACT FIRST-CONTACT ANCHOR. Show the single instant the upper-facing flat polygonal striking face on the "
    "spherical multi-face hammer head FIRST touches the exact six-o'clock bottom point P of the bubble. Center of "
    "this one flat face meets the shell; the face is square to the local tangent, its normal points upward into the "
    "bubble. Contact patch is unmistakable and unobstructed. Other flat faces and long side walls remain lateral "
    "and do not touch; shaft does not touch shell and stays diagonal down-left, not a spear through sphere center. "
    "Membrane was intact immediately before this instant. Only first tiny fractures now begin at P and radiate "
    "outward from that one contact center; no cracks elsewhere and sphere is not yet fully exploded. Show hip/torso "
    "rotation, both hands on handle, and lower-body response. No light effect may hide the striking face or P."
),
"H3": (
    "POST-IMPACT END FRAME, SAME CAMERA AND SCENE. No continuous unbroken membrane remains. Large iridescent film "
    "fragments and fine light-shards expand outward from the original six-o'clock point P along the original sphere "
    "envelope. Preserve sphere-center projection, P screen position, horizon, city landmarks, heroine identity, "
    "costume, weapon topology, handle length, head size and lighting. Same multi-face head has passed only slightly "
    "beyond P and visibly decelerated; handle, arms and torso continue in believable follow-through along the same "
    "swing path, feet/hips absorbing the reaction. Fragments flow away from residents, not through them. All residents "
    "remain alive and uninjured; city and supporting surfaces stay intact. No second explosion source, new crack "
    "origin, changed camera or text."
)}

def axis_text(record: Dict[str, Any], key: str, fallback: str) -> str:
    axes = record.get("axes", {})
    value = axes.get(key, {}) if isinstance(axes, dict) else {}
    if isinstance(value, dict):
        desc, ident = value.get("description"), value.get("id")
        if desc and ident: return f"{ident}: {desc}"
        if desc: return str(desc)
    return fallback

def safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("._")[:100] or "story"

def compile_frame_set(record: Dict[str, Any]) -> Dict[str, Any]:
    story_id = str(record.get("story_id") or "STORY-UNKNOWN")
    scene = axis_text(record, "environment", "a monumental surreal city plaza")
    scale = axis_text(record, "scale", "a giant bubble enclosing a floating city")
    shell = axis_text(record, "shell", "transparent iridescent membrane")
    palette = axis_text(record, "palette", "cold silver, electric cyan, restrained amber")
    lock = {
        "version": VERSION, "story_id": story_id, "scene": scene, "scale": scale, "shell": shell,
        "palette": palette, "weapon": "WEAPON_C_RADIAL_SPHERE", "camera": "locked low 3/4 35mm",
        "contact": "exact six-o'clock bottom pole P"
    }
    shot_id = "SHOT-" + hashlib.sha256(json.dumps(lock,sort_keys=True,ensure_ascii=False).encode()).hexdigest()[:12].upper()
    narrative = (
        f"Story kernel shown only through visible objects, never printed text: {record.get('root_sin','unassigned')}. "
        f"Mechanism: {record.get('root_mechanism','coercive containment')}. "
        f"Human cost: {record.get('human_cost','loss of meaningful choice')}. "
        f"Scene: {scene}. Scale: {scale}. Shell: {shell}. Palette: {palette}. "
    )
    prompts = {fid: COMMON + "\n\nSHOT LOCK ID (metadata only; do not render as text): " + shot_id + ".\n"
               + narrative + STATE[fid] + "\nUse visible silhouette, position, overlap, gap/contact and fragment direction; "
               "no labels, arrows, formulas or diagrams.\nNEGATIVE PROMPT: " + NEGATIVE for fid in FRAME_IDS}
    errors=[]
    checks = [
        ("H0","clearly visible continuous band of empty air"),
        ("H2","FIRST touches the exact six-o'clock bottom point P"),
        ("H2","radiate outward from that one contact center"),
        ("H3","No continuous unbroken membrane remains"),
        ("H3","All residents remain alive and uninjured"),
    ]
    for fid,token in checks:
        if token not in prompts[fid]: errors.append(f"{fid}: missing {token}")
    visual_checks=[
        ("V01","每張都是單張成片，不是拼貼／分格／資訊圖"),
        ("V02","H0/H2/H3 鏡位、地平線、地標、球心及 P 投影位置一致"),
        ("V03","女主臉、服裝一致，且只有一位女主"),
        ("V04","一柄一頭；球頭由多向寬扁平槌面構成，不是刺球或普通長方槌"),
        ("V05","H0 球膜完整無裂，指定扁平面與 P 之間有空隙"),
        ("V06","H2 只有一塊扁平槌面首次接觸六點鐘 P；柄與側壁均未先碰球"),
        ("V07","首裂只從 P 起始向外傳播"),
        ("V08","H3 球膜已解體，碎片對應原球面並從 P 向外分佈"),
        ("V09","雙手、寬站、腿、髖、軀幹、肩臂形成可讀動力鏈與跟進"),
        ("V10","居民與承載面無傷；碎片遠離居民"),
    ]
    return {
        "pipeline_version":VERSION,"story_id":story_id,"shot_lock_id":shot_id,
        "canonical_weapon":"WEAPON_C_RADIAL_SPHERE","frame_order":list(FRAME_IDS),
        "workflow":{"endpoint_frames":["H0","H3"],"contact_validation_anchor":"H2",
          "generation_policy":"Generate each frame as a separate single image; never request all frames on one canvas.",
          "continuity_warning":"Shared prompts do not guarantee identical pixels; independently generated endpoints can drift. Review actual images before interpolation."},
        "prompts":prompts,"prompt_contract_status":"PROMPT_CONTRACT_PASS" if not errors else "BLOCK",
        "prompt_contract_errors":errors,"image_realization":"NOT_RUN","pixel_audit_status":"NOT_RUN",
        "pixel_audit_checks":[{"id":i,"criterion":c,"result":"UNASSESSED"} for i,c in visual_checks]
    }

def write_packet(packet: Dict[str, Any], outdir: Path) -> Dict[str, Any]:
    story_dir=outdir/safe_name(packet["story_id"]); story_dir.mkdir(parents=True,exist_ok=True)
    names={}
    for fid in FRAME_IDS:
        name=FRAME_NAMES[fid]+".txt"; (story_dir/name).write_text(packet["prompts"][fid]+"\n",encoding="utf-8"); names[fid]=name
    manifest=dict(packet); manifest["prompt_files"]=names
    (story_dir/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    lines=[f"# Pixel audit — {packet['story_id']}","",f"Shot lock: {packet['shot_lock_id']}",
           f"Prompt contract: {packet['prompt_contract_status']}","Image realization: NOT_RUN","Pixel audit: NOT_RUN","",
           "Only mark PASS/FAIL after reviewing actual H0/H2/H3 images side by side. Prompt text is not pixel evidence.","",
           "| ID | Visual criterion | Result |","|---|---|---|"]
    lines.extend(f"| {x['id']} | {x['criterion']} | UNASSESSED |" for x in packet["pixel_audit_checks"])
    (story_dir/"pixel_audit.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    return {"story_id":packet["story_id"],"shot_lock_id":packet["shot_lock_id"],
            "prompt_contract_status":packet["prompt_contract_status"],"image_realization":"NOT_RUN",
            "pixel_audit_status":"NOT_RUN","directory":str(story_dir)}

def build_packets(input_path: Path, outdir: Path, limit: int=1, story_id_filter: str|None=None) -> Dict[str, Any]:
    if limit < 1: raise ValueError("--limit must be >= 1")
    summaries=[]
    with input_path.open("r",encoding="utf-8") as handle:
        for line in handle:
            if not line.strip(): continue
            record=json.loads(line)
            if story_id_filter and record.get("story_id") != story_id_filter: continue
            summaries.append(write_packet(compile_frame_set(record),outdir))
            if len(summaries)>=limit: break
    if not summaries: raise ValueError("no story records selected from input JSONL")
    batch={"pipeline_version":VERSION,"input":str(input_path),"requested_limit":limit,
           "written_story_packets":len(summaries),"image_realization":"NOT_RUN",
           "pixel_audit_status":"NOT_RUN","packets":summaries}
    outdir.mkdir(parents=True,exist_ok=True)
    (outdir/"batch_manifest.json").write_text(json.dumps(batch,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return batch

def main(argv: List[str]|None=None) -> int:
    parser=argparse.ArgumentParser(description="Compile separate H0/H2/H3 prompts; does not render images.")
    parser.add_argument("--input",required=True,help="story JSONL from bubble_break/generate.py")
    parser.add_argument("--outdir",required=True,help="directory for prompts and pixel-audit packet")
    parser.add_argument("--limit",type=int,default=1,help="maximum story packets; default 1")
    parser.add_argument("--story-id",default=None,help="select one exact story_id")
    args=parser.parse_args(argv)
    try: batch=build_packets(Path(args.input),Path(args.outdir),args.limit,args.story_id)
    except (OSError,ValueError,json.JSONDecodeError) as exc:
        print(f"BLOCK: {exc}",file=sys.stderr); return 2
    print(json.dumps({"written_story_packets":batch["written_story_packets"],
      "image_realization":batch["image_realization"],"pixel_audit_status":batch["pixel_audit_status"],
      "manifest":str(Path(args.outdir)/"batch_manifest.json")},ensure_ascii=False,indent=2),file=sys.stderr)
    return 0

if __name__=="__main__": raise SystemExit(main())
