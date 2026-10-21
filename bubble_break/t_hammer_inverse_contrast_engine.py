#!/usr/bin/env python3
"""Compile paired correct-vs-inverse-wrong T-hammer attack trials.

The scene pairs an airborne attacker using the correct terminal end face with a
grounded low attacker deliberately using the wrong broad cheek. The wrong pose is
a labeled negative control in metadata and must never count as an accepted strike.
This compiler emits prompts, geometry manifests and camera-projected SVG proxies.
It does NOT generate raster images or claim pixel-level acceptance.
"""
from __future__ import annotations
import argparse, json, math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

V = Tuple[float, float, float]
def add(a: V,b: V)->V: return (a[0]+b[0],a[1]+b[1],a[2]+b[2])
def sub(a: V,b: V)->V: return (a[0]-b[0],a[1]-b[1],a[2]-b[2])
def mul(a: V,s: float)->V: return (a[0]*s,a[1]*s,a[2]*s)
def dot(a: V,b: V)->float: return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]
def cross(a: V,b: V)->V: return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def norm(a: V)->float: return math.sqrt(dot(a,a))
def unit(a: V)->V:
    d=norm(a)
    if d<1e-10: raise ValueError("zero vector")
    return mul(a,1./d)
def tangent_basis(n: V)->Tuple[V,V]:
    n=unit(n); ref=(0.,1.,0.) if abs(n[1])<0.9 else (1.,0.,0.)
    u=unit(cross(ref,n)); v=unit(cross(n,u))
    return u,v

SPHERE_R=210.0
HEAD_LENGTH=150.0
HEAD_WIDTH=58.0
HEAD_DEPTH=46.0
HANDLE_LENGTH=205.0
H0_GAP=50.0
H3_ADVANCE=15.0

# Outward normals point from sphere center to each contact location.
AIR_OUTWARD=unit((0.56,-0.08,0.825))
GROUND_OUTWARD=unit((-0.67,-0.10,-0.736))

@dataclass(frozen=True)
class Camera:
    camera_id:str; name:str; azimuth_deg:float; elevation_deg:float; roll_deg:float; focal_mm:int; note:str
@dataclass(frozen=True)
class AirMove:
    move_id:str; name:str; body_action:str
@dataclass(frozen=True)
class GroundMove:
    move_id:str; name:str; body_action:str

CAMERAS=(
 Camera("CAM01_GRAZING","端面掠射審計",25,8,0,85,"偏離接觸法線以看清打擊面邊界"),
 Camera("CAM02_LOW_HERO","貼地低仰角",35,-18,0,24,"從低處仰望飛身者與低位攻擊者"),
 Camera("CAM03_HIGH_CRANE","高空鶴臂俯視",140,48,0,35,"由高處看兩個不同球面接觸點"),
 Camera("CAM04_SIDE_PROFILE","側面輪廓",90,3,0,85,"清楚展示槌頭長軸與柄的正交關係"),
 Camera("CAM05_FRONT_THREE_QUARTER","前側三分之四",48,15,0,35,"同時保留圓球曲面、端面及槌頭厚度"),
 Camera("CAM06_REVERSE_THREE_QUARTER","反向三分之四",225,18,0,40,"從攻擊對側回看兩種接觸方式"),
 Camera("CAM07_DUTCH_25","25度荷蘭斜角",55,12,25,32,"只滾轉畫面，不改變世界接觸法線"),
 Camera("CAM08_OVER_SHOULDER_A","飛身者越肩",155,10,-5,28,"沿空中攻擊者的運動方向觀察"),
 Camera("CAM09_OVER_SHOULDER_G","低位者越肩",320,5,4,28,"從低位攻擊者後方看錯面接觸"),
 Camera("CAM10_MACRO_SPLIT_DEPTH","微距深度角",80,25,0,100,"保留兩端面/側面接縫與前後深度"),
 Camera("CAM11_ORBIT_LEFT","左側環繞",275,22,-7,40,"沿球殼環繞以改變可見輪廓"),
 Camera("CAM12_ORBIT_RIGHT","右側環繞",105,32,6,50,"反向環繞但保持接觸類型不變"),
)
AIR_MOVES=(
 AirMove("AIR_DIVE_DIAGONAL","騰空斜向俯擊","The airborne fighter is above the floor, knees tucked and torso rotated through a diagonal diving attack; the final 50 units of the tool path are straight toward the contact normal."),
 AirMove("AIR_LEAP_SIDE_SWEEP","飛身橫掃","The airborne fighter crosses the frame in a powerful lateral leap, hips and shoulders rotating; the hammer stays rigid and locks to the correct face orientation before contact."),
 AirMove("AIR_SPIN_FINISH","旋身收勢後擊中","The airborne fighter completes a whole-body spin and then aligns the rigid hammer for contact; do not spin the head independently from its handle."),
 AirMove("AIR_INVERTED_DROP","倒掛下墜式攻擊","The airborne fighter is briefly inverted in a controlled acrobatic drop, both hands retain the handle, and the hammer head remains a rigid body with the terminal cap leading."),
)
GROUND_MOVES=(
 GroundMove("GROUND_DEEP_UPPERCUT","深蹲上勾","The grounded fighter stays very low in a deep crouch, driving a rising swing from legs and hips; the deliberately wrong broad cheek reaches the sphere before the terminal cap."),
 GroundMove("GROUND_KNEEL_SWEEP","單膝低位橫掃","The grounded fighter attacks from one knee with a lateral sweep; the wrong crossbar side wall, not either end cap, is the first-contact surface."),
 GroundMove("GROUND_LOW_REVERSE","低位反向橫掃","The grounded fighter shifts weight backward in a reverse low sweep; keep the deliberate wrong-face contact unmistakable and keep the handle straight."),
 GroundMove("GROUND_CROUCH_THRUST","貼地短促突擊","The grounded fighter lunges from a compact crouch; the head is intentionally presented broadside so the cheek makes the wrong first contact."),
)

def camera_frame(cam:Camera)->Tuple[V,V,V,V]:
    az=math.radians(cam.azimuth_deg); el=math.radians(cam.elevation_deg)
    pos=unit((math.cos(el)*math.cos(az),math.cos(el)*math.sin(az),math.sin(el)))
    forward=mul(pos,-1.); up0=(0.,0.,1.); right=cross(forward,up0)
    if norm(right)<1e-8: right=cross(forward,(0.,1.,0.))
    right=unit(right); up=unit(cross(right,forward))
    r=math.radians(cam.roll_deg)
    right2=add(mul(right,math.cos(r)),mul(up,math.sin(r)))
    up2=add(mul(up,math.cos(r)),mul(right,-math.sin(r)))
    return pos,forward,unit(right2),unit(up2)

def project(p:V,cam:Camera,w:int=960,h:int=540)->Tuple[float,float,float]:
    cp,fw,right,up=camera_frame(cam); camera=mul(cp,850.); rel=sub(p,camera); dep=dot(rel,fw)
    if dep<5: dep=5.
    f=cam.focal_mm*3.2
    return w/2+f*dot(rel,right)/dep,h/2-f*dot(rel,up)/dep,dep

def build_contacts()->Dict[str,Dict[str,object]]:
    # One airborne correct strike, one low grounded intentional wrong-face control.
    result={}
    for role,outward in (("AIRBORNE_CORRECT",AIR_OUTWARD),("GROUND_LOW_WRONG",GROUND_OUTWARD)):
        s=unit(outward); p=mul(s,SPHERE_R); u,v=tangent_basis(s)
        if role=="AIRBORNE_CORRECT":
            # Head runs radially; front terminal cap faces inward toward sphere center.
            head_axis=s; active_normal=mul(s,-1.); face="TERMINAL_END_FACE"
            handle=v; first_contact="CORRECT_TERMINAL_FACE"
            center=add(p,mul(s,HEAD_LENGTH/2))
            cheek_normal=None
        else:
            # Head runs along the tangent plane; the inward-facing broad cheek is the
            # deliberately wrong contact surface. Handle extends outward, rigidly 90° to head.
            head_axis=u; active_normal=mul(s,-1.); face="BROAD_CHEEK_SIDEWALL"
            handle=s; first_contact="INTENTIONAL_WRONG_FACE_FIRST"
            center=add(p,mul(s,HEAD_DEPTH/2))
            cheek_normal=mul(s,-1.)
        result[role]={
          "role":role,"sphere_outward_normal":list(s),"contact_point":list(p),
          "head_long_axis":list(head_axis),"contact_surface":face,
          "contact_surface_normal":list(active_normal),"handle_direction":list(handle),
          "head_center":list(center),"face_plane_u":list(u),"face_plane_v":list(v),
          "cheek_normal":list(cheek_normal) if cheek_normal else None,
          "normal_dot_sphere":round(dot(active_normal,s),8),
          "head_axis_dot_inward_normal":round(dot(head_axis,mul(s,-1.)),8),
          "handle_dot_head_axis":round(dot(handle,head_axis),8),
          "first_contact_class":first_contact
        }
    return result

CONTACTS=build_contacts()

def make_variant(air:AirMove,ground:GroundMove,cam:Camera)->Dict[str,object]:
    vid=f"{air.move_id}__{ground.move_id}__{cam.camera_id}"
    a=CONTACTS["AIRBORNE_CORRECT"]; g=CONTACTS["GROUND_LOW_WRONG"]
    invariant=("NON-NEGOTIABLE RIGID-BODY CONTACT RULE. Each hammer is one rigid T-shaped tool: one straight crossbar/head plus one straight handle attached at its defined midpoint joint, with no bending, twisting, telescoping or independent head rotation. The camera may change only the view; it must not change the contact surfaces or world-space contact rules.")
    correct=("CORRECT POSITIVE CONTROL — AIRBORNE FIGHTER: the hammer head's long axis points radially at the sphere pole. ONLY the narrow flat terminal end cap touches first. Its contact-face normal points from the attacker into the sphere and is exactly opposite the sphere outward normal (dot=-1). The head body extends away from the sphere; the handle attaches to the midpoint of a long side at 90 degrees and extends tangentially outside the collision zone. No cheek, corner, broad top/bottom face or handle may touch first.")
    wrong=("INTENTIONAL INVERSE / NEGATIVE CONTROL — GROUNDED LOW FIGHTER: this is deliberately WRONG and must never be scored as a successful strike. The crossbar is turned broadside with its long axis tangent to the sphere; its broad cheek/sidewall is presented toward the sphere and touches first. The designated terminal end face is NOT the contacting face. This demonstrates sidewall-first failure; do not secretly correct it into a proper terminal-cap strike. Keep the head and handle rigid and the handle attached at 90 degrees.")
    view=f"{cam.name}, camera azimuth {cam.azimuth_deg}°, elevation {cam.elevation_deg}°, frame roll {cam.roll_deg}°, {cam.focal_mm}mm lens. {cam.note}. The contact seams on both sides of the sphere must remain visible."
    combined=(
      "ONE single full-frame live-action cinematic scene, not a collage or split screen. A huge transparent iridescent glass containment sphere enclosing a miniature city stands in a ruined industrial hall. EXACTLY TWO adult fighters attack two distinct contact points on the same sphere, one on each separated side. "
      f"FIGHTER A, AIRBORNE AND CLEARLY OFF THE GROUND: {air.body_action} {correct} "
      f"FIGHTER B, FEET/KNEE ON THE FLOOR IN A DEEP LOW STANCE: {ground.body_action} {wrong} "
      f"{invariant} CAMERA: {view} "
      "Make the contrast immediately readable through physical geometry and contact location, not text: one small green-tinted glint at A's terminal-cap contact; one restrained red-tinted glint at B's cheek-first contact. These are subtle lighting cues only, not labels or overlays. Keep the sphere and miniature city intact in this contact-comparison frame. No flying glass shards yet. No text, watermark, arrows, drawn labels, borders, grids, duplicate heads or extra handles."
    )
    prompt_correct=(
      "POSITIVE-ONLY REFERENCE CROP. One adult fighter airborne, performing "+air.name+". "+
      invariant+" Correct T-hammer end-face strike only: "+correct+
      f" Sphere pole normal={a['sphere_outward_normal']}, contact point={a['contact_point']}. CAMERA: {view} "
      "Single scene, intact sphere with only tiny first microcracks from the terminal-cap contact. No wrong-face example in this crop."
    )
    prompt_wrong=(
      "NEGATIVE-CONTROL REFERENCE CROP — INTENTIONAL FAILURE, DO NOT MARK PASS. One adult fighter in a deep grounded crouch, performing "+ground.name+". "+
      invariant+" Deliberately use the wrong broad cheek/sidewall first: "+wrong+
      f" Sphere pole normal={g['sphere_outward_normal']}, contact point={g['contact_point']}. CAMERA: {view} "
      "The wrong contact must be unmistakable, with the designated terminal cap visibly not touching first. No airborne correct attacker in this crop."
    )
    return {
      "variant_id":vid,"air_move":asdict(air),"ground_move":asdict(ground),"camera":asdict(cam),
      "contact_geometry":{"sphere_radius":SPHERE_R,"airborne_positive_control":a,"grounded_negative_control":g,
                          "positive_surface_normal_dot_sphere":a["normal_dot_sphere"],
                          "negative_surface_normal_dot_sphere":g["normal_dot_sphere"],
                          "negative_head_axis_dot_inward_normal":g["head_axis_dot_inward_normal"],
                          "camera_changes_contact_geometry":False},
      "prompts":{"paired_contrast_scene":combined,"positive_correct_face_crop":prompt_correct,"negative_wrong_face_crop":prompt_wrong},
      "expected_acceptance":{"airborne_correct_contact":"REVIEW_FOR_PASS","grounded_wrong_contact":"EXPECTED_FAIL_NEGATIVE_CONTROL",
                             "paired_scene_as_a_whole":"CONTRAST_EXPERIMENT_NOT_A_SINGLE_PASS"},
      "audit_status":{"geometry_compile":"COMPILED","prompt_compile":"COMPILED","image_realization":"NOT_RUN","pixel_audit":"NOT_RUN"}
    }

def build_matrix()->Dict[str,object]:
    vs=[make_variant(a,g,c) for a in AIR_MOVES for g in GROUND_MOVES for c in CAMERAS]
    return {"schema_version":"1.0.0-t-hammer-inverse-contrast","principle_lock":{
      "positive":"TERMINAL_END_FACE_FIRST","negative_control":"BROAD_CHEEK_SIDEWALL_FIRST",
      "positive_face_normal_dot_sphere_outward":-1.0,"wrong_face_is_never_pass":True,
      "camera_is_view_only":True,"two_attackers_distinct_body_actions":True},
      "counts":{"airborne_moves":len(AIR_MOVES),"ground_low_moves":len(GROUND_MOVES),"camera_views":len(CAMERAS),"total_variants":len(vs)},
      "variants":vs,"acceptance_gate":{"image_realization":"NOT_RUN","pixel_audit":"NOT_RUN","positive_review_pass_count":0,"negative_control_reviewed_count":0}}

def render_proxy_svg(v:Dict[str,object],w:int=960,h:int=540)->str:
    cam=Camera(**v["camera"]); points=v["contact_geometry"]
    cp,fw,right,up=camera_frame(cam)
    def xy(p:V)->Tuple[float,float]:
        x,y,_=project(p,cam,w,h); return x,y
    def fmt(p:V)->str:
        x,y=xy(p); return f"{x:.1f},{y:.1f}"
    # Project sphere silhouette in the camera plane.
    center=(0.,0.,0.); outline=[]
    for i in range(73):
        t=2*math.pi*i/72
        p=add(center,add(mul(right,SPHERE_R*math.cos(t)),mul(up,SPHERE_R*math.sin(t))))
        outline.append(fmt(p))
    def line(p1:V,p2:V,color:str,sw:int,dash:str="")->str:
        x1,y1=xy(p1); x2,y2=xy(p2); extra=f' stroke-dasharray="{dash}"' if dash else ""
        return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"{extra}/>'
    els=[f'<polyline points="{" ".join(outline)}" fill="#15232c" fill-opacity=".55" stroke="#77d9e8" stroke-width="3"/>']
    for role,color in (("AIRBORNE_CORRECT","#62f0a6"),("GROUND_LOW_WRONG","#ff646e")):
        d=points[ "airborne_positive_control" if role=="AIRBORNE_CORRECT" else "grounded_negative_control"]
        s=tuple(d["sphere_outward_normal"]); p=tuple(d["contact_point"]); u=tuple(d["face_plane_u"]); vv=tuple(d["face_plane_v"])
        axis=tuple(d["head_long_axis"]); hd=tuple(d["handle_direction"])
        if role=="AIRBORNE_CORRECT":
            # Cap at P; the head extends outward along sphere normal, while handle runs tangent.
            back=add(p,mul(s,HEAD_LENGTH))
            cap=[add(add(p,mul(u,su*HEAD_WIDTH/2)),mul(vv,sv*HEAD_DEPTH/2)) for su,sv in ((-1,-1),(1,-1),(1,1),(-1,1))]
            backc=[add(add(back,mul(u,su*HEAD_WIDTH/2)),mul(vv,sv*HEAD_DEPTH/2)) for su,sv in ((-1,-1),(1,-1),(1,1),(-1,1))]
            mid=add(p,mul(s,HEAD_LENGTH/2)); root=add(mid,mul(hd,HEAD_DEPTH/2)); end=add(root,mul(hd,HANDLE_LENGTH))
        else:
            # Broad cheek plane is tangent at P; the head extends outward from that plane.
            back=add(p,mul(s,HEAD_DEPTH))
            cap=[add(add(p,mul(axis,sa*HEAD_LENGTH/2)),mul(vv,sb*HEAD_WIDTH/2)) for sa,sb in ((-1,-1),(1,-1),(1,1),(-1,1))]
            backc=[add(add(back,mul(axis,sa*HEAD_LENGTH/2)),mul(vv,sb*HEAD_WIDTH/2)) for sa,sb in ((-1,-1),(1,-1),(1,1),(-1,1))]
            mid=add(p,mul(s,HEAD_DEPTH/2)); root=mid; end=add(root,mul(hd,HANDLE_LENGTH))
        els.append(f'<polygon points="{" ".join(fmt(q) for q in cap)}" fill="{color}" fill-opacity=".65" stroke="{color}" stroke-width="3"/>')
        els.append(f'<polygon points="{" ".join(fmt(q) for q in backc)}" fill="{color}" fill-opacity=".25" stroke="{color}" stroke-width="2"/>')
        for k in range(4): els.append(line(cap[k],backc[k],color,2))
        els.append(line(root,end,color,9))
        x,y=xy(p); els.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{color}" stroke="#ffffff" stroke-width="2"/>')
        lab="AIRBORNE · CORRECT END CAP" if role=="AIRBORNE_CORRECT" else "GROUND LOW · WRONG CHEEK"
        els.append(f'<text x="{x+10:.1f}" y="{y-12:.1f}" fill="{color}" font-size="14">{lab}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
      f'data-variant="{v["variant_id"]}" data-image-realization="NOT_RUN"><rect width="100%" height="100%" fill="#0b1118"/>'
      f'<text x="18" y="24" font-size="15" fill="#f1f5f9">{v["variant_id"]} · schematic only, NOT pixel proof</text>'
      +''.join(els)+'</svg>')

def export(outdir:Path)->Dict[str,object]:
    m=build_matrix(); outdir.mkdir(parents=True,exist_ok=True); pp=outdir/"prompts"; ss=outdir/"svg_proxies"; pp.mkdir(exist_ok=True); ss.mkdir(exist_ok=True)
    (outdir/"t_hammer_inverse_contrast_matrix.json").write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding="utf-8")
    readme=("T-Hammer inverse contrast matrix\n"
      "192 trials = 4 airborne moves x 4 ground-low moves x 12 camera angles.\n"
      "Airborne fighter: correct terminal end face first (candidate for positive review).\n"
      "Ground-low fighter: deliberately wrong broad cheek/sidewall first (negative control; never PASS).\n"
      "Each scene has different action roles, two different contact points, and view-only camera variants.\n"
      "image_realization=NOT_RUN; pixel_audit=NOT_RUN.\n")
    (outdir/"README.txt").write_text(readme,encoding="utf-8")
    for v in m["variants"]:
        (pp/f'{v["variant_id"]}.json').write_text(json.dumps({"variant_id":v["variant_id"],"prompts":v["prompts"],"expected_acceptance":v["expected_acceptance"]},ensure_ascii=False,indent=2),encoding="utf-8")
        (ss/f'{v["variant_id"]}.svg').write_text(render_proxy_svg(v),encoding="utf-8")
    return m

if __name__=="__main__":
    p=argparse.ArgumentParser(description="Compile T-hammer correct-vs-wrong surface contrast trials")
    p.add_argument("--outdir",type=Path,default=Path("out/t_hammer_inverse_contrast"))
    a=p.parse_args(); m=export(a.outdir)
    print(json.dumps({"status":"COMPILED","variants":m["counts"]["total_variants"],"image_realization":"NOT_RUN","pixel_audit":"NOT_RUN","outdir":str(a.outdir)},ensure_ascii=False))
