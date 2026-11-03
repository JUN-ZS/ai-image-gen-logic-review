#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T-Hammer vs T-Hammer ((H) vs (H)) terminal striking-face contact matrix."""
from __future__ import annotations
import argparse, json, math, unittest
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

@dataclass(frozen=True)
class Vec2:
    x: float
    y: float
    def __add__(self, o): return Vec2(self.x+o.x, self.y+o.y)
    def __sub__(self, o): return Vec2(self.x-o.x, self.y-o.y)
    def scale(self, s): return Vec2(self.x*s, self.y*s)
    def dot(self, o): return self.x*o.x + self.y*o.y
    def norm(self): return math.hypot(self.x, self.y)
    def normalized(self):
        n=self.norm()
        if n==0: raise ValueError("zero")
        return Vec2(self.x/n, self.y/n)
    def to_tuple(self): return (round(self.x,4), round(self.y,4))

@dataclass(frozen=True)
class CollisionAxisSpec:
    axis_id: str; name_zh: str; name_en: str; impact_angle_deg: float
    target_pole_clock: str; shaft_handedness: int; kinetic_description_zh: str

@dataclass(frozen=True)
class CameraAngleSpec:
    camera_id: str; name_zh: str; name_en: str; focal_mm: int
    pitch_deg: float; yaw_deg: float; roll_deg: float
    framing_directive_zh: str; optical_cue_zh: str

COLLISION_AXES = (
 CollisionAxisSpec("AXIS_01_UPWARD_6OCLOCK","由下而上垂直頂擊（6點鐘底極點 P）","Upward Vertical",-90.0,"6:00 (Bottom Pole P)",-1,"攻擊方 T 槌剛體旋轉使橫樑沿垂直撞擊軸立起，頂端終端打擊面法線朝正上方 (0,-1) 對準 6 點鐘底極點 P；中央長柄嚴格保持 90 度垂直於橫樑中點向左下方延伸，雙手由下而上爆發揮擊"),
 CollisionAxisSpec("AXIS_02_DIAG_UP_RIGHT_730","左下往右上 45° 對角重擊（7:30 斜下極點 P）","Diag Up-Right",-45.0,"7:30 (Lower-Left Oblique Pole P)",-1,"攻擊方 T 槌沿 -45° 對角線剛體旋轉，橫樑前側終端打擊面法線朝右上方 (+0.707,-0.707) 正對 7:30 接觸點 P；中央長柄以 90 度正交鎖定於橫樑中點並延伸至左下方蓄力軌跡外側"),
 CollisionAxisSpec("AXIS_03_HORIZ_H_VS_H_9OCLOCK","水平正面對撞 ((H) vs (H) / 9點鐘側極點 P)","Horiz (H) vs (H)",0.0,"9:00 (Left Lateral Pole P)",1,"兩把 T 槌呈 ((H) vs (H))／橫向對稱剛體構型，攻擊方橫樑沿水平撞擊軸指向右方 (+1,0)，前端終端打擊面與目標方終端打擊面在 P 點正面平齊對撞，長柄以 90 度正交向外側延伸"),
 CollisionAxisSpec("AXIS_04_HIGH_ARC_1030","高角度斜劈對撞（10:30 左上極點 P）","High Arc 10:30",35.0,"10:30 (Upper-Left Oblique Pole P)",-1,"攻擊方 T 槌沿 +35° 高位斜弧剛體旋轉，橫樑前端終端打擊面法線朝右下方 (+0.819,+0.574) 對準 10:30 接觸點 P；長柄嚴格保持 90 度正交延伸於揮擊弧線外側，禁止長側壁或柄身提前擦碰"),
)

CAMERA_ANGLES = (
 CameraAngleSpec('CAM_01_ORTHO_PROFILE','正交側面幾何審計鏡位','Ortho',85,0,0,0,'85mm 長焦正側面平視，零透視吞沒，完整呈現兩把 T 槌剛體 90° 結構與終端打擊面法線共線對齊','cue'),
 CameraAngleSpec('CAM_02_LOW_HEROIC_WORMS_EYE','極低仰角英雄破界鏡位','Low Heroic',24,-38,15,0,'24mm 廣角貼地極低仰拍，由下往上直視終端打擊面迎頭撞入 P 點的壓迫感，保留可見接觸縫隙與邊界','cue'),
 CameraAngleSpec('CAM_03_THREE_QUARTER_FRONT_45','前側 45° 立體斜角鏡位','3/4',35,-12,45,0,'35mm 前側 45° 斜角，同時交代終端矩形打擊面厚度、橫樑長側壁與中央長柄的 3D 剛體正交關係','cue'),
 CameraAngleSpec('CAM_04_MACRO_GRAZING_CONTACT','微距掠射接觸面特寫鏡位','Macro',100,-5,12,0,'100mm 微距以 12° 掠射角貼近接觸切面 P，放大量度兩個終端打擊面的平行度與零穿模','cue'),
 CameraAngleSpec('CAM_05_OVER_SHOULDER_KINETIC','越肩動力鏈跟隨鏡位','OTS',28,-10,-30,-6,'28mm 從揮擊者後側越肩前望，完整串聯雙手握柄、長柄力臂與前端橫樑終端打擊面命中 P 點','cue'),
 CameraAngleSpec('CAM_06_HIGH_OVERWATCH_CRANE','高空俯瞰戰術鶴臂鏡位','High',35,42,25,0,'35mm 高角度俯拍，俯視球體內部與 T 槌終端打擊面精準切入 P 點','cue'),
 CameraAngleSpec('CAM_07_DUTCH_TENSION_ROLL_25','25° 荷蘭斜角高張力鏡位','Dutch',32,-15,30,25,'32mm 鏡頭滾轉 25° 強化張力，但兩把 T 槌剛體 90° 結構與終端面接觸法線嚴格不變形','cue'),
 CameraAngleSpec('CAM_08_REVERSE_THROUGH_BUBBLE','180° 穿泡逆向反打鏡位','Reverse',24,18,165,0,'24mm 從目標內側往外逆向反打，直視攻擊方終端打擊面衝向 P','cue'),
 CameraAngleSpec('CAM_09_VERTIGO_DOLLY_CORRIDOR','希區考克變焦縱深走廊鏡位','Vertigo',50,-8,20,0,'50mm 變焦壓縮背景，焦點鎖死在接觸點 P 與終端打擊面','cue'),
 CameraAngleSpec('CAM_10_ORBIT_TANGENTIAL_60','60° 環繞切線動勢鏡位','Orbit',40,-6,60,-4,'40mm 環繞至 60° 切線，長柄弧線與終端打擊面法線匯聚於 P','cue'),
 CameraAngleSpec('CAM_11_EXTREME_WIDE_MONUMENTAL','極遠景巨構尺度對比鏡位','Wide',18,-14,10,0,'18mm 超廣角全景，P 點接觸幾何仍清晰可辨','cue'),
 CameraAngleSpec('CAM_12_SNORRICAM_SHAFT_LOCKED','柄身綁定軸向衝擊鏡位','Snorri',28,-4,-18,0,'28mm 沿長柄外側斜向鎖定槌頭橫樑，長柄 90° 接入橫樑中點，終端打擊面撞擊 P','cue'),
)

@dataclass(frozen=True)
class RigidTHammerPose:
    role: str; face_center: Vec2; head_center: Vec2; rear_face_center: Vec2
    n_active: Vec2; v_shaft: Vec2; shaft_root: Vec2; shaft_end: Vec2
    head_corners: Tuple[Vec2, Vec2, Vec2, Vec2]
    active_face_segment: Tuple[Vec2, Vec2]
    head_length: float = 220.0; head_thickness: float = 64.0
    shaft_length: float = 320.0; shaft_width: float = 24.0

def compute_rigid_t_hammer_pose(role, contact_point_p, n_active, signed_gap_px, shaft_handedness=-1, head_length=220.0, head_thickness=64.0, shaft_length=320.0):
    u = n_active.normalized()
    v = Vec2(-u.y, u.x) if shaft_handedness >= 0 else Vec2(u.y, -u.x)
    face_center = contact_point_p - u.scale(signed_gap_px)
    head_center = face_center - u.scale(head_length * 0.5)
    rear_face_center = face_center - u.scale(head_length)
    half_w = head_thickness * 0.5
    c0 = face_center + v.scale(half_w); c1 = face_center - v.scale(half_w)
    c2 = rear_face_center - v.scale(half_w); c3 = rear_face_center + v.scale(half_w)
    shaft_root = head_center + v.scale(half_w)
    shaft_end = shaft_root + v.scale(shaft_length)
    return RigidTHammerPose(role, face_center, head_center, rear_face_center, u, v, shaft_root, shaft_end, (c0,c1,c2,c3), (c0,c1), head_length, head_thickness, shaft_length)

def build_variant_geometry(axis, sphere_center=Vec2(1090.0,330.0), sphere_radius=280.0):
    rad = math.radians(axis.impact_angle_deg)
    n_attacker = Vec2(math.cos(rad), math.sin(rad)).normalized()
    n_target = n_attacker.scale(-1.0)
    contact_p = sphere_center + n_target.scale(sphere_radius)
    att_h0 = compute_rigid_t_hammer_pose("attacker", contact_p, n_attacker, 50.0, axis.shaft_handedness)
    att_h2 = compute_rigid_t_hammer_pose("attacker", contact_p, n_attacker, 0.0, axis.shaft_handedness)
    att_h3 = compute_rigid_t_hammer_pose("attacker", contact_p, n_attacker, -15.0, axis.shaft_handedness)
    tgt_h0 = compute_rigid_t_hammer_pose("target_proxy", contact_p, n_target, 50.0, -axis.shaft_handedness)
    tgt_h2 = compute_rigid_t_hammer_pose("target_proxy", contact_p, n_target, 0.0, -axis.shaft_handedness)
    return {
      "axis_id": axis.axis_id, "impact_angle_deg": axis.impact_angle_deg, "target_pole_clock": axis.target_pole_clock,
      "sphere_center": sphere_center.to_tuple(), "sphere_radius": sphere_radius,
      "contact_point_p": contact_p.to_tuple(), "n_attacker": n_attacker.to_tuple(), "n_target": n_target.to_tuple(),
      "normal_dot_product": round(n_attacker.dot(n_target), 6),
      "orthogonality_attacker_dot": round(att_h2.n_active.dot(att_h2.v_shaft), 6),
      "orthogonality_target_dot": round(tgt_h2.n_active.dot(tgt_h2.v_shaft), 6),
      "h2_terminal_face_gap_px": round((att_h2.face_center - tgt_h2.face_center).norm(), 6),
      "h0_attacker_to_p_gap_px": round((contact_p - att_h0.face_center).dot(n_attacker), 6),
      "h2_attacker_to_p_gap_px": round((contact_p - att_h2.face_center).dot(n_attacker), 6),
      "h3_attacker_follow_through_px": round((att_h3.face_center - contact_p).dot(n_attacker), 6),
      "poses": {"attacker_h0": att_h0, "attacker_h2": att_h2, "attacker_h3": att_h3, "target_h0": tgt_h0, "target_h2": tgt_h2},
    }

def render_t_to_t_clash_svg(geom, stage="H2"):
    poses = geom["poses"]
    att = poses["attacker_h2" if stage=="H2" else "attacker_h0"]
    tgt = poses["target_h2" if stage=="H2" else "target_h0"]
    px, py = geom["contact_point_p"]; cx, cy = geom["sphere_center"]; r = geom["sphere_radius"]
    def poly(corners): return " ".join(f"{p.x:.1f},{p.y:.1f}" for p in corners)
    af0, af1 = att.active_face_segment; tf0, tf1 = tgt.active_face_segment
    mark = f'<circle cx="{px:.1f}" cy="{py:.1f}" r="14" fill="#ffcf56" stroke="#ff595e" stroke-width="4"/>' if stage=="H2" else ""
    return (
      f'<?xml version="1.0" encoding="UTF-8"?>\n'
      f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080" data-stage="{stage}" data-axis="{geom["axis_id"]}" data-contact-p="{px:.1f},{py:.1f}" data-normal-dot="{geom["normal_dot_product"]}">\n'
      f'<rect width="1920" height="1080" fill="#0d131a"/>\n'
      f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" stroke="#3a506b" stroke-width="2" stroke-dasharray="10 8"/>\n'
      f'<line x1="{tgt.shaft_root.x:.1f}" y1="{tgt.shaft_root.y:.1f}" x2="{tgt.shaft_end.x:.1f}" y2="{tgt.shaft_end.y:.1f}" stroke="#8d6e63" stroke-width="{tgt.shaft_width:.1f}"/>\n'
      f'<polygon points="{poly(tgt.head_corners)}" fill="#bc6c25" stroke="#dda15e" stroke-width="4"/>\n'
      f'<line x1="{tf0.x:.1f}" y1="{tf0.y:.1f}" x2="{tf1.x:.1f}" y2="{tf1.y:.1f}" stroke="#ff9f1c" stroke-width="8"/>\n'
      f'<line x1="{att.shaft_root.x:.1f}" y1="{att.shaft_root.y:.1f}" x2="{att.shaft_end.x:.1f}" y2="{att.shaft_end.y:.1f}" stroke="#90a4ae" stroke-width="{att.shaft_width:.1f}"/>\n'
      f'<polygon points="{poly(att.head_corners)}" fill="#1d3557" stroke="#457b9d" stroke-width="4"/>\n'
      f'<line x1="{af0.x:.1f}" y1="{af0.y:.1f}" x2="{af1.x:.1f}" y2="{af1.y:.1f}" stroke="#00f5d4" stroke-width="8"/>\n'
      f'{mark}\n</svg>\n'
    )

def build_contact_matrix_prompts(axis, camera, geom):
    px, py = geom["contact_point_p"]; cx, cy = geom["sphere_center"]
    nx, ny = geom["n_attacker"]; tx, ty = geom["n_target"]
    lock = (
      f"【T字槌剛體與終端打擊面契約｜{axis.axis_id} × {camera.camera_id}】"
      f"每把T字槌皆為『一條筆直橫樑槌頭＋中央正交90度單一長柄』的剛體（u_crossbar ⊥ v_shaft）。"
      f"唯一合法的打擊接觸面是橫樑前端的『矩形終端打擊面（Terminal Striking Face）』，"
      f"其外法線 n_active=({nx:+.3f},{ny:+.3f}) 嚴格對準接觸點 P=({px:.1f},{py:.1f})；"
      f"絕對禁止把橫樑上下寬面疊在一起（禁止 ⊤ 對 ⊥ 平推），"
      f"絕對禁止橫樑長側壁（cheek）、斜角或長柄（錘柄／桿身）先碰到目標。"
      f"鏡頭採用 {camera.name_zh}（{camera.focal_mm}mm, pitch={camera.pitch_deg}°, yaw={camera.yaw_deg}°, roll={camera.roll_deg}°）："
      f"{camera.framing_directive_zh}。純單張電影畫面，禁止多格拼貼、禁止文字水印與座標標籤。"
    )
    stage_a = (
      f"【Stage A｜T字槌對T字槌 終端打擊面互撞錨點 ((H) vs (H))】"
      f"兩把巨型重工業鋼鐵T字槌在 {axis.name_zh} 軸向上正面交鋒。"
      f"攻擊方T字槌橫樑沿 ({nx:+.3f},{ny:+.3f}) 指向接觸點 P=({px:.1f},{py:.1f})，"
      f"目標方T字槌橫樑沿相反法線 ({tx:+.3f},{ty:+.3f}) 指向同一個 P 點；"
      f"兩把T字槌各自的『橫樑前端矩形終端打擊面』在 P 點平齊正對（法線內積 = -1.0），"
      f"各自的單一長柄（錘柄／桿身）均以 90 度垂直鎖定於橫樑中點並延伸在碰撞區外側，構成 ((H) vs (H)) 剛體對撞幾何。" + lock
    )
    stage_b = (
      f"【Stage B｜局部遮罩編輯：僅將目標方T字槌替換為透明封存球體】"
      f"保留攻擊方T字槌的完整剛體姿態、橫樑終端打擊面位置 P=({px:.1f},{py:.1f})、長柄角度與 {camera.name_zh} 鏡位不動；"
      f"僅將目標方T字槌區域替換為以球心 C=({cx:.1f},{cy:.1f})、半徑 R={geom['sphere_radius']:.0f}px 定義的巨型透明虹彩玻璃泡殼，"
      f"使泡殼在 {axis.target_pole_clock} 的極點切面恰好落在同一接觸點 P=({px:.1f},{py:.1f})，球殼外法線與攻擊方終端打擊面法線完全相反。"
    )
    h0 = f"【H0 前幀｜終端打擊面逼近・50px 可見空隙・泡殼完整無裂】{axis.kinetic_description_zh}。攻擊方T字槌的橫樑前端『指定打擊端面（終端打擊面）』正對巨型透明泡殼的 {axis.target_pole_clock} 接觸點 P=({px:.1f},{py:.1f})，但終端打擊面與泡殼表面之間仍保持清晰可見的 50px 空氣間隙；整顆透明泡殼 100% 完整光滑、零預裂紋、零提前碎片，泡內受困居民與微型城市清晰可見。" + lock
    h2 = f"【H2 接觸錨點幀｜終端打擊面零間隙首次接觸 P 點・裂紋自 P 點初生】同一鏡位（{camera.name_zh}）與同一角色動作延續。攻擊方T字槌作為剛體高速揮至頂點，僅以橫樑前端唯一的『指定打擊端面（矩形終端打擊面）』在 P=({px:.1f},{py:.1f})（{axis.target_pole_clock}）與透明泡殼表面達成 0px 首次平齊接觸；橫樑長側壁、後端面與錘柄／桿身均與泡殼保持安全淨空。第一道高折射放射狀裂紋嚴格只從接觸點 P 向外初生擴散，泡殼其餘區域尚未解體，泡內居民安全無傷。" + lock
    h3 = f"【H3 後幀｜終端打擊面越過 P 點 15px 跟進・泡殼自 P 點崩解・居民全數生還】同一鏡位（{camera.name_zh}）下撞擊後的真實物理跟進（Follow-through）。攻擊方T字槌保持 90 度剛體結構不變形，橫樑前端終端打擊面沿 ({nx:+.3f},{ny:+.3f}) 慣性越過原接觸點 P=({px:.1f},{py:.1f}) 約 15px；透明泡殼由 P 點向外全面爆裂成大片折射玻璃碎片與虹彩薄膜殘片，泡內居民毫髮無傷、重獲呼吸與自主選擇。" + lock
    neg = "禁止把T字槌橫樑上下寬面疊在一起平推（禁止 ⊤ 對 ⊥ 寬面貼合）；禁止用橫樑長側壁（cheek）或錘柄／桿身側面敲擊；禁止橫樑保持水平卻用側端面硬蹭球底造成法線垂直矛盾；禁止T字槌退化成多面圓球頭、十字加號錘、L形歪頭錘、雙柄或彎曲軟柄；禁止H0提前出現裂紋或接觸閃光；禁止H2全泡提前粉碎；禁止多格漫畫拼貼、文字標籤、座標線與水印。"
    return {
      "variant_id": f"{axis.axis_id}__{camera.camera_id}", "axis_id": axis.axis_id, "axis_name_zh": axis.name_zh,
      "camera_id": camera.camera_id, "camera_name_zh": camera.name_zh,
      "camera_params": {"focal_mm": camera.focal_mm, "pitch_deg": camera.pitch_deg, "yaw_deg": camera.yaw_deg, "roll_deg": camera.roll_deg},
      "contact_geometry": {
        "sphere_center": geom["sphere_center"], "sphere_radius": geom["sphere_radius"], "contact_point_p": geom["contact_point_p"],
        "target_pole_clock": axis.target_pole_clock, "n_attacker": geom["n_attacker"], "n_target": geom["n_target"],
        "normal_dot_product": geom["normal_dot_product"], "orthogonality_attacker_dot": geom["orthogonality_attacker_dot"],
        "orthogonality_target_dot": geom["orthogonality_target_dot"], "h0_gap_px": geom["h0_attacker_to_p_gap_px"],
        "h2_gap_px": geom["h2_attacker_to_p_gap_px"], "h3_follow_through_px": geom["h3_attacker_follow_through_px"],
      },
      "prompts": {"Stage_A_T_to_T_clash": stage_a, "Stage_B_target_T_to_bubble_edit": stage_b, "H0_pre_impact": h0, "H2_first_contact": h2, "H3_post_impact": h3, "negative_prompt": neg},
      "audit_status": {"prompt_contract": "PASS", "geometry_proxy_contract": "PASS", "image_realization": "NOT_RUN", "pixel_audit": "NOT_RUN"},
    }

def generate_full_48_matrix():
    variants=[]; axis_geometries={}
    for axis in COLLISION_AXES:
        geom=build_variant_geometry(axis); axis_geometries[axis.axis_id]=geom
        for camera in CAMERA_ANGLES: variants.append(build_contact_matrix_prompts(axis, camera, geom))
    return {"schema_version":"2.0.0-rigid-T-terminal-clash-matrix","total_collision_axes":len(COLLISION_AXES),"total_camera_angles":len(CAMERA_ANGLES),"total_variants":len(variants),"total_keyframe_prompts":len(variants)*3,"contact_face_contract":"T_CROSSBAR_TERMINAL_END_FACE_VS_TERMINAL_END_FACE ((H) vs (H))","image_realization":"NOT_RUN","pixel_audit":"NOT_RUN","variants":variants,"axis_geometries":axis_geometries}

def render_patched_master_geometry_svg():
    return '<?xml version="1.0"?><svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" data-active-faces="LEFT_AND_RIGHT_TERMINAL_END_FACES"><rect width="100%" height="100%" fill="#e9edf0"/><rect x="788" y="216" width="345" height="91" fill="#647f95"/><rect x="919" y="307" width="82" height="578" fill="#334f65"/><rect x="788" y="216" width="10" height="91" fill="#00f5d4"/><rect x="1123" y="216" width="10" height="91" fill="#00f5d4"/></svg>\n'

def render_patched_silhouette_reference_svg():
    return '<?xml version="1.0"?><svg xmlns="http://www.w3.org/2000/svg" width="1000" height="900" data-active-faces="LEFT_AND_RIGHT_TERMINAL_END_FACES"><rect width="1000" height="900" fill="#f3f5f7"/><rect x="300" y="150" width="400" height="105" fill="#263746"/><rect x="465" y="255" width="70" height="520" fill="#334f65"/><rect x="300" y="150" width="12" height="105" fill="#00f5d4"/><rect x="688" y="150" width="12" height="105" fill="#00f5d4"/></svg>\n'

class TestRigidTHammerContactMatrix(unittest.TestCase):
    def test_48_variants_completeness(self):
        m=generate_full_48_matrix()
        self.assertEqual(m["total_collision_axes"],4); self.assertEqual(m["total_camera_angles"],12)
        self.assertEqual(m["total_variants"],48); self.assertEqual(m["total_keyframe_prompts"],144)
        self.assertEqual(len({v["variant_id"] for v in m["variants"]}),48)
    def test_rigid_body_orthogonality_and_anti_parallel_normals(self):
        for axis in COLLISION_AXES:
            g=build_variant_geometry(axis)
            self.assertAlmostEqual(g["normal_dot_product"],-1.0,places=6)
            self.assertAlmostEqual(g["orthogonality_attacker_dot"],0.0,places=6)
            self.assertAlmostEqual(g["orthogonality_target_dot"],0.0,places=6)
            self.assertAlmostEqual(g["h0_attacker_to_p_gap_px"],50.0,places=5)
            self.assertAlmostEqual(g["h2_attacker_to_p_gap_px"],0.0,places=5)
            self.assertAlmostEqual(g["h3_attacker_follow_through_px"],15.0,places=5)
            self.assertAlmostEqual(g["h2_terminal_face_gap_px"],0.0,places=5)
    def test_6_oclock_bottom_pole_has_upward_terminal_face_normal(self):
        g=build_variant_geometry(COLLISION_AXES[0])
        self.assertEqual(g["contact_point_p"],(1090.0,610.0))
        self.assertEqual(g["n_attacker"],(0.0,-1.0)); self.assertEqual(g["n_target"],(0.0,1.0))
        att=g["poses"]["attacker_h2"]; c0,c1=att.active_face_segment
        self.assertAlmostEqual(c0.y,610.0,places=4); self.assertAlmostEqual(c1.y,610.0,places=4)
        self.assertGreater(att.head_center.y,610.0); self.assertAlmostEqual(att.shaft_root.y,720.0,places=4)
    def test_prompts_enforce_terminal_face_and_forbid_broad_top_stacking(self):
        m=generate_full_48_matrix()
        for v in m["variants"]:
            for key in ("Stage_A_T_to_T_clash","H0_pre_impact","H2_first_contact","H3_post_impact"):
                t=v["prompts"][key]
                self.assertIn("終端打擊面",t); self.assertIn("錘柄／桿身",t); self.assertIn("禁止把橫樑上下寬面疊在一起",t)
            self.assertIn("指定打擊端面",v["prompts"]["H0_pre_impact"])
        self.assertEqual(m["image_realization"],"NOT_RUN")
    def test_patched_master_highlights_terminal_faces_only(self):
        self.assertIn("LEFT_AND_RIGHT_TERMINAL_END_FACES", render_patched_master_geometry_svg())
        self.assertNotIn("M796 224 H1125", render_patched_master_geometry_svg())

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--outdir",type=Path,default=Path("out/contact_matrix_48")); ap.add_argument("--run-tests",action="store_true"); args=ap.parse_args()
    if args.run_tests:
        r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(TestRigidTHammerContactMatrix))
        if not r.wasSuccessful(): raise SystemExit(1)
    args.outdir.mkdir(parents=True,exist_ok=True)
    m=generate_full_48_matrix()
    svg=args.outdir/"svg_proxies"; svg.mkdir(parents=True,exist_ok=True)
    for aid,g in m["axis_geometries"].items():
        (svg/f"{aid}__H0_T_to_T_gap.svg").write_text(render_t_to_t_clash_svg(g,"H0"),encoding="utf-8")
        (svg/f"{aid}__H2_T_to_T_contact.svg").write_text(render_t_to_t_clash_svg(g,"H2"),encoding="utf-8")
    (args.outdir/"00_T_weapon_master_geometry_patched.svg").write_text(render_patched_master_geometry_svg(),encoding="utf-8")
    (args.outdir/"05_T_silhouette_reference_patched.svg").write_text(render_patched_silhouette_reference_svg(),encoding="utf-8")
    vdir=args.outdir/"variants"; vdir.mkdir(parents=True,exist_ok=True)
    for v in m["variants"]:
        d=vdir/v["variant_id"]; d.mkdir(parents=True,exist_ok=True)
        for k,t in v["prompts"].items(): (d/f"{k}.txt").write_text(t+"\n",encoding="utf-8")
        rev={"variant_id":v["variant_id"],"status":"UNASSESSED","manual_pixel_review":False,"image_realization":"NOT_RUN","pixel_audit":"NOT_RUN","checks":{"two_distinct_T_hammers":False,"terminal_end_faces_coincident_at_P":False,"normals_dot_minus_one":False,"no_broad_top_stacking":False,"no_cheek_first":False,"no_handle_first":False,"rigid_shaft_orthogonal":False},"notes":"","warning":"PROMPT/SVG PASS != image PASS"}
        (d/"H2_review.template.json").write_text(json.dumps(rev,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    export={k:v for k,v in m.items() if k!="axis_geometries"}
    (args.outdir/"contact_matrix_48_variants.json").write_text(json.dumps(export,ensure_ascii=False,indent=2),encoding="utf-8")
    summary=[{"axis_id":a,"contact_point_p":g["contact_point_p"],"n_attacker":g["n_attacker"],"n_target":g["n_target"],"normal_dot_product":g["normal_dot_product"],"orthogonality_attacker_dot":g["orthogonality_attacker_dot"],"h0_gap_px":g["h0_attacker_to_p_gap_px"],"h2_gap_px":g["h2_attacker_to_p_gap_px"],"h3_follow_through_px":g["h3_attacker_follow_through_px"]} for a,g in m["axis_geometries"].items()]
    (args.outdir/"axis_geometry_summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    man={"schema_version":m["schema_version"],"total_variants":m["total_variants"],"total_keyframe_prompts":m["total_keyframe_prompts"],"contact_face_contract":m["contact_face_contract"],"image_realization":"NOT_RUN","pixel_audit":"NOT_RUN","svg_proxy_count":8,"gate":"BLOCKED_UNTIL_H2_PIXEL_REVIEW","note":"PROMPT_PASS and SVG_PASS do not equal image PASS."}
    (args.outdir/"manifest.json").write_text(json.dumps(man,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(man,ensure_ascii=False,indent=2)); print("Exported", args.outdir)

if __name__ == "__main__":
    main()
