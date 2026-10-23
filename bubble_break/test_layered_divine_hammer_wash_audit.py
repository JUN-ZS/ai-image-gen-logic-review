#!/usr/bin/env python3
"""Unit tests for `layered_divine_hammer_wash_audit.py` (5-Layer Progressive Lock & Cumulative Full Re-Audit)."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

from bubble_break.layered_divine_hammer_wash_audit import (
    HammerInstanceGeometry,
    WashPanelCandidateSpec,
    run_cumulative_layered_full_reaudit,
    sha256_file,
)


class LayeredDivineHammerWashAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _make_asymmetric_raster(self, name: str, variant: int) -> tuple[Path, str]:
        p = self.root / name
        im = Image.new("RGB", (640, 360), (14, 18, 24))
        draw = ImageDraw.Draw(im)
        # Draw asymmetric layout so LR_symmetry_ncc is low and pairwise layout_ncc is distinct
        if variant == 1:
            draw.rectangle([30, 40, 280, 320], fill=(230, 180, 90))
            draw.ellipse([360, 20, 600, 150], fill=(70, 140, 210))
        else:
            draw.rectangle([350, 180, 610, 340], fill=(240, 110, 190))
            draw.polygon([(40, 20), (310, 30), (160, 170)], fill=(120, 230, 150))
        im.save(p, format="PNG")
        return p, sha256_file(p)

    def _make_mirror_clone_raster(self, name: str) -> tuple[Path, str]:
        p = self.root / name
        im = Image.new("RGB", (640, 360), (16, 18, 22))
        draw = ImageDraw.Draw(im)
        # Highly symmetric left-right mirror image
        draw.rectangle([80, 100, 290, 260], fill=(200, 150, 90))
        draw.rectangle([640 - 290, 100, 640 - 80, 260], fill=(200, 150, 90))
        draw.ellipse([280, 120, 360, 240], fill=(255, 240, 180))
        im.save(p, format="PNG")
        return p, sha256_file(p)

    def test_rejects_spear_handle_side_cheek_trap_and_mirror_clones(self) -> None:
        p1, sha1 = self._make_mirror_clone_raster("bad_panel1.png")
        p2, sha2 = self._make_mirror_clone_raster("bad_panel2.png")

        # Spear-Handle Trap: handle is horizontal along collision axis (0 deg), head is vertical!
        bad_hammer_a = HammerInstanceGeometry(
            instance_id="HAMMER_A",
            head_axis_px=((300.0, 110.0), (300.0, 250.0)),      # vertical head!
            handle_axis_px=((120.0, 180.0), (300.0, 180.0)),    # horizontal handle aimed at P!
            active_face_center_px=(315.0, 180.0),
            active_face_radius_px=30.0,
            declared_face_id="F1_FRONT_STRIKE_END_FACE",
            grip_point_px=(160.0, 180.0),
            pull_force_vec=(1.0, 0.0),                          # axial push along handle!
        )
        bad_hammer_b = HammerInstanceGeometry(
            instance_id="HAMMER_B",
            head_axis_px=((340.0, 110.0), (340.0, 250.0)),      # vertical head!
            handle_axis_px=((520.0, 180.0), (340.0, 180.0)),    # horizontal handle aimed at P!
            active_face_center_px=(325.0, 180.0),
            active_face_radius_px=30.0,
            declared_face_id="F1_FRONT_STRIKE_END_FACE",
            grip_point_px=(480.0, 180.0),
            pull_force_vec=(-1.0, 0.0),
        )
        c1 = WashPanelCandidateSpec(
            panel_id="PANEL_01",
            panel_index=1,
            raster_path=p1,
            raster_sha256=sha1,
            strike_method_id="M1_HORIZONTAL",
            camera_rig_id="CAM_EYE",
            camera_elevation_deg=0.0,
            camera_azimuth_deg=0.0,
            collision_axis_angle_deg=0.0,
            contact_point_p_px=(320.0, 180.0),
            hammer_a=bad_hammer_a,
            hammer_b=bad_hammer_b,
        )
        c2 = WashPanelCandidateSpec(
            panel_id="PANEL_02_CLONE",
            panel_index=2,
            raster_path=p2,
            raster_sha256=sha2,
            strike_method_id="M1_HORIZONTAL",
            camera_rig_id="CAM_EYE",
            camera_elevation_deg=2.0,
            camera_azimuth_deg=3.0,
            collision_axis_angle_deg=4.0,
            contact_point_p_px=(320.0, 180.0),
            hammer_a=bad_hammer_a,
            hammer_b=bad_hammer_b,
        )

        rep = run_cumulative_layered_full_reaudit([c1, c2], up_to_layer=5)
        self.assertFalse(rep.passed)
        self.assertEqual(rep.status, "BLOCKED_LAYER_ADVANCE_DENIED_BY_FULL_REAUDIT")
        err_blob = " | ".join(rep.blocking_errors)
        self.assertIn("SPEAR_HANDLE_SIDE_CHEEK_TRAP", err_blob)
        self.assertIn("EXCESSIVE_MIRROR_SYMMETRY_CLONE", err_blob)
        self.assertIn("AXIAL_PUSH_NO_LEVER_TORQUE", err_blob)
        self.assertIn("LAYOUT_NCC_CLONE_DETECTED", err_blob)

    def test_approves_true_orthogonal_t_handle_and_diverse_faces_across_layers(self) -> None:
        p1, sha1 = self._make_asymmetric_raster("good_p1.png", 1)
        p2, sha2 = self._make_asymmetric_raster("good_p2.png", 4)

        # Panel 1: Horizontal collision axis (0 deg) -> Head is HORIZONTAL, Handle is VERTICAL (orthogonal!)
        ha_1 = HammerInstanceGeometry(
            instance_id="HAMMER_A",
            head_axis_px=((210.0, 180.0), (315.0, 180.0)),      # horizontal head aligned with 0-deg impact normal
            handle_axis_px=((262.0, 180.0), (262.0, 60.0)),     # vertical lateral handle (90 deg to head)
            active_face_center_px=(315.0, 180.0),
            active_face_radius_px=28.0,
            declared_face_id="F1_FRONT_STRIKE_END_FACE",
            grip_point_px=(262.0, 80.0),
            pull_force_vec=(1.0, 0.2),                          # tangential lever pull perpendicular to handle!
        )
        hb_1 = HammerInstanceGeometry(
            instance_id="HAMMER_B",
            head_axis_px=((430.0, 180.0), (325.0, 180.0)),
            handle_axis_px=((378.0, 180.0), (378.0, 300.0)),
            active_face_center_px=(325.0, 180.0),
            active_face_radius_px=28.0,
            declared_face_id="F1_FRONT_STRIKE_END_FACE",
            grip_point_px=(378.0, 280.0),
            pull_force_vec=(-1.0, -0.2),
        )
        c1 = WashPanelCandidateSpec(
            panel_id="GOOD_01",
            panel_index=1,
            raster_path=p1,
            raster_sha256=sha1,
            strike_method_id="M1_HORIZONTAL_END_FACE_TORQUE",
            camera_rig_id="CAM_LOW_OBLIQUE",
            camera_elevation_deg=-15.0,
            camera_azimuth_deg=25.0,
            collision_axis_angle_deg=0.0,
            contact_point_p_px=(320.0, 180.0),
            hammer_a=ha_1,
            hammer_b=hb_1,
        )

        # Panel 2: Vertical collision axis (90 deg) with F2_REAR_COUNTER_END_FACE -> Head is VERTICAL, Handle is HORIZONTAL!
        ha_2 = HammerInstanceGeometry(
            instance_id="HAMMER_A",
            head_axis_px=((320.0, 70.0), (320.0, 175.0)),       # vertical head aligned with 90-deg impact normal
            handle_axis_px=((320.0, 122.0), (190.0, 122.0)),    # horizontal lateral handle (90 deg to head)
            active_face_center_px=(320.0, 175.0),
            active_face_radius_px=28.0,
            declared_face_id="F2_REAR_COUNTER_END_FACE",
            grip_point_px=(210.0, 122.0),
            pull_force_vec=(0.1, 1.0),                          # downward lever pull perpendicular to horizontal handle!
        )
        hb_2 = HammerInstanceGeometry(
            instance_id="HAMMER_B",
            head_axis_px=((320.0, 290.0), (320.0, 185.0)),
            handle_axis_px=((320.0, 238.0), (450.0, 238.0)),
            active_face_center_px=(320.0, 185.0),
            active_face_radius_px=28.0,
            declared_face_id="F2_REAR_COUNTER_END_FACE",
            grip_point_px=(430.0, 238.0),
            pull_force_vec=(-0.1, -1.0),
        )
        c2 = WashPanelCandidateSpec(
            panel_id="GOOD_02",
            panel_index=2,
            raster_path=p2,
            raster_sha256=sha2,
            strike_method_id="M2_VERTICAL_REAR_END_COUNTER",
            camera_rig_id="CAM_HIGH_ZENITH",
            camera_elevation_deg=55.0,
            camera_azimuth_deg=-35.0,
            collision_axis_angle_deg=90.0,
            contact_point_p_px=(320.0, 180.0),
            hammer_a=ha_2,
            hammer_b=hb_2,
        )

        for layer_step in range(1, 6):
            rep = run_cumulative_layered_full_reaudit([c1, c2], up_to_layer=layer_step)
            self.assertTrue(rep.passed, f"Failed at layer {layer_step}: {rep.blocking_errors}")
            self.assertEqual(rep.status, "PASSED_CUMULATIVE_LAYER_REAUDIT_ADVANCE_APPROVED")


if __name__ == "__main__":
    unittest.main()