#!/usr/bin/env python3
"""Compile rigid T-hammer collision trials across 3D impact axes, swing paths and camera views.

This creates prompts and projected SVG geometry proxies only. It does not generate images
or claim pixel acceptance. Camera changes are view transforms; they never alter contact geometry.
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
def length(a: V)->float: return math.sqrt(dot(a,a))
def unit(a: V)->V:
    d=length(a)
    if d<1e-9: raise ValueError('zero vector')
    return mul(a,1.0/d)

def tangent_basis(n: V)->Tuple[V,V]:
    # A shared contact-plane frame; stable even when n is near vertical.
    ref: V=(0.0,0.0,1.0) if abs(n[2])<0.92 else (0.0,1.0,0.0)
    u=unit(sub(ref,mul(n,dot(ref,n))))
    return u,unit(cross(n,u))

def rolled_handle(axis: V, degrees: float)->V:
    u,v=tangent_basis(axis); a=math.radians(degrees)
    return unit(add(mul(u,math.cos(a)),mul(v,math.sin(a))))

@dataclass(frozen=True)
class StrikeAxis:
    axis_id: str; name_zh: str; name_en: str; normal: V; swing_id: str
@dataclass(frozen=True)
class CameraView:
    camera_id: str; name_zh: str; name_en: str; off_normal_deg: float; orbit_deg: float; roll_deg: float; focal_mm: int; visibility_note: str
@dataclass(frozen=True)
class SwingStyle:
    swing_id: str; name_zh: str; name_en: str; windup: str; impact: str
@dataclass(frozen=True)
class HammerPose:
    role: str; face_center: V; face_normal: V; head_center: V; rear_face_center: V
    handle_direction: V; face_u: V; face_v: V; handle_root: V; handle_end: V
    head_length: float=220.; face_width: float=64.; face_depth: float=64.; handle_length: float=320.; handle_radius: float=9.

AXES=(
 StrikeAxis('X_RIGHT','水平由左向右','Horizontal left-to-right',(1.,0.,0.),'SIDE_SWEEP'),
 StrikeAxis('X_LEFT','水平由右向左','Horizontal right-to-left',(-1.,0.,0.),'REVERSE_SWEEP'),
 StrikeAxis('Z_UP','由下而上垂直頂擊','Vertical rising uppercut',(0.,0.,1.),'RISING_UPPERCUT'),
 StrikeAxis('Z_DOWN','由上而下垂直斬擊','Vertical overhead downstroke',(0.,0.,-1.),'OVERHAND_DOWN'),
 StrikeAxis('XZ_RISE','左下至右上斜擊','Diagonal rising strike',unit((1.,0.,1.)),'DIAGONAL_RISE'),
 StrikeAxis('XZ_FALL','左上至右下斜擊','Diagonal falling strike',unit((1.,0.,-1.)),'DIAGONAL_FALL'),
 StrikeAxis('Y_DEPTH','沿場景縱深方向突擊','Depth-axis thrust',(0.,1.,0.),'DEPTH_THRUST'),
 StrikeAxis('OBLIQUE_3D','三維斜向重擊','Three-dimensional oblique power strike',unit((1.,1.,1.)),'OBLIQUE_POWER'),
)
# Off-normal=0 means looking down the collision normal; grazing offsets expose the seam.
CAMERAS=(
 CameraView('CAM01_GRAZING_FACE','端面掠射審計','Grazing end-face audit',18,0,0,85,'接縫可見，避免沿法線完全遮住端面'),
 CameraView('CAM02_FRONT_THREE_QUARTER','前側四分之三斜視','Front three-quarter',38,35,0,35,'同時顯示端面與長側壁深度'),
 CameraView('CAM03_SIDE_PROFILE','側面輪廓','Side profile',90,0,0,85,'完整呈現槌頭、中央接柄和碰撞軸'),
 CameraView('CAM04_LOW_HERO','低仰角英雄鏡位','Low-angle hero view',62,20,0,24,'由低位仰看並保持接觸切口可見'),
 CameraView('CAM05_HIGH_CRANE','高位鶴臂俯視','High crane view',62,200,0,35,'從碰撞軸另一側高位觀察'),
 CameraView('CAM06_DUTCH_ROLL','荷蘭斜角','Dutch angle',48,70,25,32,'只滾轉構圖，不改變剛體姿態'),
 CameraView('CAM07_REVERSE_THREE_QUARTER','反向三分之四鏡位','Reverse three-quarter',125,35,0,40,'從目標側反看並保留兩柄與接縫'),
 CameraView('CAM08_MACRO_SEAM','微距接縫特寫','Macro seam close-up',28,110,0,100,'近距離辨識端面邊界，火花不可遮縫'),
 CameraView('CAM09_OVER_SHOULDER','越肩追擊','Over-the-shoulder',72,145,-8,28,'從攻擊柄後方看向接觸面'),
 CameraView('CAM10_OVERHEAD_ORBIT','高空環繞視角','Overhead orbit',78,260,0,35,'從上方繞看但不改世界碰撞方向'),
 CameraView('CAM11_LOW_GRAZING','低位掠射鏡頭','Low grazing camera',78,310,-4,40,'用切線方向顯示端面厚度和零間隙'),
 CameraView('CAM12_DEPTH_DIAGONAL','縱深透視斜視','Depth diagonal view',52,225,0,50,'辨識前後深度、雙端面與兩柄'),
)
SWINGS={
 'SIDE_SWEEP':SwingStyle('SIDE_SWEEP','橫向弧形揮擊','Lateral arc swing','肩、軀幹與雙臂帶動寬弧蓄力；槌頭與柄作為完整剛體。','接觸前最後一段沿 X_RIGHT 法線直線推進；僅終端端面先接觸。'),
 'REVERSE_SWEEP':SwingStyle('REVERSE_SWEEP','反向橫掃','Reverse lateral sweep','從相反側蓄力並自然轉移重心，槌頭不獨立扭轉。','接觸前最後一段沿 X_LEFT 法線直線推進；兩端面法線反向。'),
 'RISING_UPPERCUT':SwingStyle('RISING_UPPERCUT','由下而上上勾揮擊','Rising uppercut','由膝腰屈伸帶動向上弧線，雙手位置符合人體工學。','接觸瞬間槌頭長軸與 Z_UP 法線共線；只有頂端終端端面接觸。'),
 'OVERHAND_DOWN':SwingStyle('OVERHAND_DOWN','高位下劈','Overhand downstroke','高位蓄力後向下揮動，肩肘帶動完整剛體槌身。','接觸瞬間槌頭長軸與 Z_DOWN 法線共線；只有下端終端面接觸。'),
 'DIAGONAL_RISE':SwingStyle('DIAGONAL_RISE','對角上斬','Diagonal rising strike','武器沿斜向弧線加速，頭柄接合保持剛性。','接觸瞬間端面法線沿 XZ_RISE；禁止側壁擦撞。'),
 'DIAGONAL_FALL':SwingStyle('DIAGONAL_FALL','對角下劈','Diagonal falling strike','由高側斜向落下，張力來自人物動作，不以彎柄表現。','接觸瞬間端面法線沿 XZ_FALL；禁止角或長側壁先碰。'),
 'DEPTH_THRUST':SwingStyle('DEPTH_THRUST','縱深突擊','Depth-axis thrust','沿鏡頭前後縱深短促揮擊，不將柄誤當槌頭軸。','槌頭長軸與 Y_DEPTH 法線共線；鏡頭偏離法線以顯示接縫。'),
 'OBLIQUE_POWER':SwingStyle('OBLIQUE_POWER','三維斜向重擊','3D oblique power swing','全身沿三維斜線旋轉蓄力，槌頭與柄始終為同一剛體。','接觸瞬間沿 OBLIQUE_3D 法線跟進；相機可繞行但接觸軸不變。'),
}
WINDUP_PROFILES=(
 {'profile_id':'WINDUP_WIDE_ARC','name':'wide rotational wind-up','text':'Use a broad shoulder-and-hip rotational wind-up. The arc may curve before contact, but the final approach segment is straight along the defined impact normal; lock the hammer orientation before the last 50 units.'},
 {'profile_id':'WINDUP_COMPACT_SNAP','name':'compact accelerating wind-up','text':'Use a compact recoil and fast accelerating swing with a different body pose from the wide-arc version. The final approach segment is straight along the same defined impact normal; lock the hammer orientation before the last 50 units.'},
)
ROLLS=(0.,90.,180.,270.)
H0_GAP=50.0; H3_ADVANCE=15.0; HEAD_LENGTH=220.0; CAP_SIZE=64.0; HANDLE_LENGTH=320.0

def make_pose(role: str, face: V, normal: V, roll: float)->HammerPose:
    n=unit(normal)
    # Canonicalize the unoriented head axis so opposing square caps share the same plane frame.
    flip=(n[0]<-1e-9 or (abs(n[0])<1e-9 and (n[1]<-1e-9 or (abs(n[1])<1e-9 and n[2]<0))))
    axis=mul(n,-1.) if flip else n
    h=rolled_handle(axis,roll); k=unit(cross(axis,h))
    center=sub(face,mul(n,HEAD_LENGTH/2)); rear=sub(face,mul(n,HEAD_LENGTH))
    root=add(center,mul(h,CAP_SIZE/2)); end=add(root,mul(h,HANDLE_LENGTH))
    return HammerPose(role,face,n,center,rear,h,h,k,root,end)

def make_variant(axis: StrikeAxis,camera: CameraView,motion_index: int)->Dict[str,object]:
    n=unit(axis.normal); p=(0.,0.,0.)
    # In the dual-hammer H0 proof, 50 is the TOTAL gap, 25 units per end face.
    a0=add(p,mul(n,-H0_GAP/2)); b0=add(p,mul(n,H0_GAP/2))
    roll_a=ROLLS[(AXES.index(axis)+motion_index)%4]
    roll_b=ROLLS[(ROLLS.index(roll_a)+motion_index+1)%4]
    poses={'H0_attacker':make_pose('attacker',a0,n,roll_a),
           'H0_target':make_pose('target',b0,mul(n,-1.),roll_b),
           'H2_attacker':make_pose('attacker',p,n,roll_a),
           'H2_target':make_pose('target',p,mul(n,-1.),roll_b)}
    swing=SWINGS[axis.swing_id]; vid=f'{axis.axis_id}__{camera.camera_id}__M{motion_index+1}'
    rigid_lock=("RIGID-BODY LOCK: one straight rectangular T-hammer head whose long axis is collinear with the active terminal-face normal; "
      "one straight, long handle joined at the midpoint of a long head side at exactly 90 degrees. Head and handle are one rigid body. "
      "Only the flat rectangular terminal end face may touch first; no cheek, upper/lower long surface, corner, joint or handle contact. "
      "Camera angle is a view transform and must not alter the world-space strike normal or rotate the head independently.")
    dual_contract=("STAGE A DUAL-HAMMER PROOF: exactly two independent complete T-hammers. " + rigid_lock + " "
      "Hammer A terminal face normal is n; hammer B terminal face normal is -n (dot=-1). Their terminal face planes meet at the same P, "
      "with zero gap and no interpenetration. Both long handles must remain individually traceable; do not merge the tools into one H weapon.")
    scene_contract=("STAGE B/C SINGLE-HAMMER SCENE: exactly one attacking T-hammer and one transparent containment sphere, not two hammers. " + rigid_lock + " "
      "At P, the hammer terminal-face normal is n and the sphere's outward surface normal is -n (dot=-1). The handle runs tangent to the sphere "
      "outside the impact zone; the hammer's flat terminal end face is the only part that touches the sphere first.")
    nstr=tuple(round(x,6) for x in n); neg=tuple(round(-x,6) for x in n)
    view=f"{camera.name_en}, focal {camera.focal_mm}mm, off impact normal {camera.off_normal_deg}°, orbit about impact axis {camera.orbit_deg}°, image roll {camera.roll_deg}°. {camera.visibility_note}."
    windup=WINDUP_PROFILES[motion_index]
    prompts={
      'stage_a_two_hammer_proof':f"{dual_contract}\nVARIANT={vid}. Impact axis={axis.name_en}, n={nstr}; opposing target normal={neg}. CAMERA={view} Handle-roll variant: A={roll_a}°, B={roll_b}°, rigid rolls only. One full-frame scene showing two complete heads, both long handles, and the terminal-face seam. Tiny restrained contact sparks must not obscure the seam. No labels or collage.",
      'H0_preimpact':f"{scene_contract}\nH0 PRE-IMPACT. Swing={swing.name_en}; wind-up profile={windup['profile_id']} ({windup['name']}). {swing.windup} {windup['text']} Same character, tool scale and camera as H2. The attacker's terminal face is 50 units from the sphere surface along -n={tuple(round(-x,6) for x in n)}. Sphere pristine and uncracked; no sparks or debris. Handle tangent to the local sphere and rigidly attached.",
      'H2_first_contact':f"{scene_contract}\nH2 MASTER ANCHOR. Swing={swing.name_en}; wind-up profile={windup['profile_id']}. {swing.impact} At P=(0,0,0), attacker face normal n={nstr}, sphere outward normal -n={neg}; dot=-1. Sphere center C=P+R*n so the outward pole at P has normal -n. The only first contact is the flat rectangular terminal end face. First fine radial micro-cracks start at P only; the rest of the transparent sphere and miniature city remain intact. CAMERA={view}.",
      'H3_followthrough':f"{scene_contract}\nH3 FOLLOW-THROUGH. Use accepted H2 as the strict image reference. Keep camera, character, background and proportions fixed. Advance the same rigid hammer 15 units along +n={nstr} past P, with head axis still collinear to n and handle still 90 degrees. Shatter the shell outward from P only; miniature city and people remain unharmed. No handle bend, twist or independent head rotation."
    }
    geom={'P':[0.,0.,0.],'attacker_normal':list(n),'target_normal':list(mul(n,-1.)),
          'normal_dot':round(dot(n,mul(n,-1.)),8),'attacker_handle_dot':round(dot(n,poses['H2_attacker'].handle_direction),8),
          'target_handle_dot':round(dot(mul(n,-1.),poses['H2_target'].handle_direction),8),
          'H0_total_gap':H0_GAP,'H2_gap':0.0,'H3_advance':H3_ADVANCE,'roll_A':roll_a,'roll_B':roll_b,
          'camera_view_only':True}
    return {'variant_id':vid,'axis':asdict(axis),'camera':asdict(camera),'swing':asdict(swing),'windup_profile':windup,'geometry':geom,
      'prompts':prompts,'poses':{k:asdict(v) for k,v in poses.items()},
      'audit_status':{'geometry_model':'COMPILED','prompt_compile':'COMPILED','image_realization':'NOT_RUN','pixel_audit':'NOT_RUN'}}

def camera_frame(n: V,camera: CameraView)->Tuple[V,V,V,V]:
    n=unit(n); t,b=tangent_basis(n); a=math.radians(camera.orbit_deg)
    around=add(mul(t,math.cos(a)),mul(b,math.sin(a))); off=math.radians(camera.off_normal_deg)
    pos=unit(add(mul(n,math.cos(off)),mul(around,math.sin(off))))
    forward=mul(pos,-1.); up_world=(0.,0.,1.); right=cross(forward,up_world)
    if length(right)<1e-8: right=cross(forward,(0.,1.,0.))
    right=unit(right); up=unit(cross(right,forward)); r=math.radians(camera.roll_deg)
    right2=add(mul(right,math.cos(r)),mul(up,math.sin(r)))
    up2=add(mul(up,math.cos(r)),mul(right,-math.sin(r)))
    return pos,forward,right2,up2

def project(p: V,camera: CameraView,n: V,width:int=960,height:int=540)->Tuple[float,float,float]:
    cp,forward,right,up=camera_frame(n,camera); cam=mul(cp,1100.); rel=sub(p,cam); depth=dot(rel,forward)
    if depth<=20: depth=20.
    f=camera.focal_mm*22.
    return width/2+f*dot(rel,right)/depth,height/2-f*dot(rel,up)/depth,depth

def pose_vertices(d:Dict[str,object])->Dict[str,List[V]]:
    face=tuple(d['face_center']); rear=tuple(d['rear_face_center']); u=tuple(d['face_u']); v=tuple(d['face_v'])
    w=float(d['face_width'])/2; dep=float(d['face_depth'])/2
    def corners(c:V)->List[V]: return [add(add(c,mul(u,-w)),mul(v,-dep)),add(add(c,mul(u,w)),mul(v,-dep)),add(add(c,mul(u,w)),mul(v,dep)),add(add(c,mul(u,-w)),mul(v,dep))]
    return {'front':corners(face),'rear':corners(rear),'handle':[tuple(d['handle_root']),tuple(d['handle_end'])]}

def render_proxy_svg(v:Dict[str,object],width:int=960,height:int=540)->str:
    cam=CameraView(**v['camera']); n=tuple(v['axis']['normal']); els=[]
    def point(p:V)->Tuple[float,float,float]: return project(p,cam,n,width,height)
    def poly(ps:Sequence[V])->str: return ' '.join(f'{point(p)[0]:.2f},{point(p)[1]:.2f}' for p in ps)
    for key,fill,edge in [('H2_target','#875629','#ffc078'),('H2_attacker','#234b72','#83e8ff')]:
        d=v['poses'][key]; verts=pose_vertices(d); f=verts['front']; r=verts['rear']
        faces=[([f[0],f[1],r[1],r[0]],'#172532'),([f[1],f[2],r[2],r[1]],fill),([f[2],f[3],r[3],r[2]],'#344b5c'),([f[3],f[0],r[0],r[3]],fill)]
        for q,c in faces: els.append(f'<polygon points="{poly(q)}" fill="{c}" stroke="{edge}" stroke-width="2"/>')
        els.append(f'<polygon points="{poly(f)}" fill="{fill}" fill-opacity=".92" stroke="{edge}" stroke-width="3"/>')
        (h0,h1)=verts['handle']; x0,y0,_=point(h0); x1,y1,_=point(h1)
        els.append(f'<line x1="{x0:.2f}" y1="{y0:.2f}" x2="{x1:.2f}" y2="{y1:.2f}" stroke="#111820" stroke-width="18" stroke-linecap="round"/>')
        els.append(f'<line x1="{x0:.2f}" y1="{y0:.2f}" x2="{x1:.2f}" y2="{y1:.2f}" stroke="{edge}" stroke-width="10" stroke-linecap="round"/>')
    els.append('<circle cx="480" cy="270" r="6" fill="#f8d66d" stroke="#ffffff" stroke-width="2"/>')
    vid=v['variant_id']
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" data-variant="{vid}" data-contact="H2" data-image-realization="NOT_RUN">'
      f'<rect width="100%" height="100%" fill="#0b1118"/><text x="24" y="30" fill="#e8eef5" font-size="17">{vid} — projected geometry proxy; NOT pixel proof</text>'
      +''.join(els)+'</svg>')

def build_matrix()->Dict[str,object]:
    variants=[make_variant(a,c,m) for a in AXES for c in CAMERAS for m in range(2)]
    return {'schema_version':'1.0.0-t-hammer-multiview-swing-engine',
      'principle_lock':{'only_first_contact':'TERMINAL_END_FACE_TO_TERMINAL_END_FACE','normal_dot':-1.0,
        'handle_dot_impact_normal':0.0,'camera_changes_geometry':False,'stage_a_H0_gap_total':H0_GAP,'H3_follow_through':H3_ADVANCE},
      'counts':{'strike_axes':len(AXES),'camera_views':len(CAMERAS),'windup_profiles_per_axis_camera':2,'total_variants':len(variants)},
      'variants':variants,'acceptance_gate':{'image_realization':'NOT_RUN','pixel_audit':'NOT_RUN','manual_review_pass_count':0}}

def export(outdir:Path)->Dict[str,object]:
    m=build_matrix(); proxies=outdir/'svg_proxies'; prompts=outdir/'prompts'; proxies.mkdir(parents=True,exist_ok=True); prompts.mkdir(parents=True,exist_ok=True)
    outdir.mkdir(parents=True,exist_ok=True)
    (outdir/'t_hammer_multiview_swing_matrix.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
    (outdir/'README.txt').write_text(f"T-Hammer camera/swing matrix\nVariants: {m['counts']['total_variants']} (8 axes x 12 cameras x 2 windups)\nOnly terminal-end-face first contact; 3D rigid body; camera is view-only.\nimage_realization=NOT_RUN\npixel_audit=NOT_RUN\n",encoding='utf-8')
    for v in m['variants']:
        vid=v['variant_id']; (prompts/f'{vid}.json').write_text(json.dumps({'variant_id':vid,'prompts':v['prompts'],'audit_status':v['audit_status']},ensure_ascii=False,indent=2),encoding='utf-8')
        (proxies/f'{vid}__H2.svg').write_text(render_proxy_svg(v),encoding='utf-8')
    return m

if __name__=='__main__':
    p=argparse.ArgumentParser(description='Compile geometry-locked T-hammer swing and camera trials.')
    p.add_argument('--outdir',type=Path,default=Path('out/t_hammer_multiview_swing')); a=p.parse_args()
    m=export(a.outdir); print(json.dumps({'status':'COMPILED','variants':m['counts']['total_variants'],'image_realization':'NOT_RUN','pixel_audit':'NOT_RUN','outdir':str(a.outdir)},ensure_ascii=False))
