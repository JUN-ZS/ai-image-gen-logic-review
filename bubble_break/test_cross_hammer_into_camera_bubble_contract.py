#!/usr/bin/env python3
"""Unit tests for cross_hammer_into_camera_bubble_contract (L1–L5)."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

from bubble_break.cross_hammer_into_camera_bubble_contract import (
    BubbleBarrageSpec,
    CrossHammerGeometry,
    CrossHammerPanelCandidateSpec,
    run_cumulative_cross_hammer_full_reaudit,
    sha256_file,
)


class CrossHammerIntoCameraContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _asymmetric(self, name: str, variant: int) -> tuple[Path, str]:
        p = self.root / name
        im = Image.new("RGB", (640, 360), (10, 12, 18))
        d = ImageDraw.Draw(im)
        if variant == 1:
            d.rectangle([20, 30, 260, 300], fill=(220, 160, 80))
            d.ellipse([380, 40, 620, 200], fill=(40, 160, 220))
        else:
            d.rectangle([340, 160, 620, 340], fill=(240, 90, 160))
            d.polygon([(30, 40), (280, 50), (140, 200)], fill=(90, 220, 140))
        im.save(p, format="PNG")
        return p, sha256_file(p)

    def _mirror(self, name: str) -> tuple[Path, str]:
        p = self.root / name
        im = Image.new("RGB", (640, 360), (16, 18, 22))
        d = ImageDraw.Draw(im)
        d.rectangle([80, 100, 290, 260], fill=(200, 150, 90))
        d.rectangle([640 - 290, 100, 640 - 80, 260], fill=(200, 150, 90))
        d.ellipse([280, 120, 360, 240], fill=(255, 240, 180))
        im.save(p, format="PNG")
        return p, sha256_file(p)

    def test_rejects_cylinder_spear_and_cleared_stream(self) -> None:
        p1, sha1 = self._mirror("bad1.png")
        # Pseudo "cross" that is really a horizontal bar (E/W only) + handle along camera
        # Actually make plain cylinder: N/S long, E/W missing
        bad = CrossHammerGeometry(
            instance_id="CX1",
            arm_tip_n_px=(320.0, 80.0),
            arm_tip_s_px=(320.0, 280.0),
            arm_tip_e_px=(325.0, 180.0),  # almost no E arm
            arm_tip_w_px=(315.0, 180.0),  # almost no W arm
            boss_center_px=(320.0, 180.0),
            handle_axis_px=((100.0, 180.0), (320.0, 180.0)),  # handle along 0 deg = into-cam axis
            grip_point_px=(140.0, 180.0),
            pull_force_vec=(1.0, 0.0),  # axial
            declared_strike_face_id="CX_ARM_END_E",
            active_face_center_px=(400.0, 180.0),  # claim E but arms short
            active_face_radius_px=20.0,
        )
        c1 = CrossHammerPanelCandidateSpec(
            panel_id="BAD_01",
            panel_index=1,
            raster_path=p1,
            raster_sha256=sha1,
            skill_move_id="SK_THRUST_INTO_LENS",
            camera_rig_id="CAM_INTO_LENS_EYE",
            camera_elevation_deg=0.0,
            camera_azimuth_deg=0.0,
            into_camera_axis_angle_deg=0.0,
            hammer=bad,
            barrage=BubbleBarrageSpec(
                bubble_count_visible=2,
                into_camera_fraction=0.2,
                exploding_near_lens_count=0,
                stream_never_clears=False,
                primary_impact_p_px=(400.0, 180.0),
            ),
        )
        rep = run_cumulative_cross_hammer_full_reaudit([c1], up_to_layer=5)
        self.assertFalse(rep.passed)
        blob = " | ".join(rep.blocking_errors)
        self.assertTrue(
            any(
                k in blob
                for k in (
                    "PLAIN_CYLINDER_NOT_CROSS",
                    "CROSS arm",
                    "STREAM_CLEARED",
                    "INTO_CAMERA_FRACTION",
                    "SPEAR_HANDLE",
                    "AXIAL_PUSH",
                    "too few bubbles",
                )
            ),
            msg=blob,
        )

    def test_approves_true_cross_and_into_camera_barrage_across_layers(self) -> None:
        p1, sha1 = self._asymmetric("g1.png", 1)
        p2, sha2 = self._asymmetric("g2.png", 4)

        # True cross: N/S vertical, E/W horizontal, handle down from boss, strike E into +X cam
        good_h1 = CrossHammerGeometry(
            instance_id="CX_A",
            arm_tip_n_px=(320.0, 100.0),
            arm_tip_s_px=(320.0, 260.0),
            arm_tip_e_px=(400.0, 180.0),
            arm_tip_w_px=(240.0, 180.0),
            boss_center_px=(320.0, 180.0),
            handle_axis_px=((320.0, 180.0), (320.0, 320.0)),  # vertical handle
            grip_point_px=(320.0, 300.0),
            pull_force_vec=(1.0, 0.15),  # torque for horizontal smash
            declared_strike_face_id="CX_ARM_END_E",
            active_face_center_px=(395.0, 180.0),
            active_face_radius_px=24.0,
        )
        c1 = CrossHammerPanelCandidateSpec(
            panel_id="GOOD_01",
            panel_index=1,
            raster_path=p1,
            raster_sha256=sha1,
            skill_move_id="SK_SIDE_SWEEP",
            camera_rig_id="CAM_INTO_LENS_EYE",
            camera_elevation_deg=-10.0,
            camera_azimuth_deg=20.0,
            into_camera_axis_angle_deg=0.0,
            hammer=good_h1,
            barrage=BubbleBarrageSpec(
                bubble_count_visible=12,
                into_camera_fraction=0.85,
                exploding_near_lens_count=3,
                stream_never_clears=True,
                primary_impact_p_px=(400.0, 180.0),
            ),
        )

        # Panel 2: into-cam axis vertical, strike N, different skill/camera
        good_h2 = CrossHammerGeometry(
            instance_id="CX_A",
            arm_tip_n_px=(320.0, 90.0),
            arm_tip_s_px=(320.0, 270.0),
            arm_tip_e_px=(410.0, 180.0),
            arm_tip_w_px=(230.0, 180.0),
            boss_center_px=(320.0, 180.0),
            handle_axis_px=((320.0, 180.0), (200.0, 180.0)),
            grip_point_px=(220.0, 180.0),
            pull_force_vec=(0.1, 1.0),
            declared_strike_face_id="CX_ARM_END_N",
            active_face_center_px=(320.0, 100.0),
            active_face_radius_px=24.0,
        )
        c2 = CrossHammerPanelCandidateSpec(
            panel_id="GOOD_02",
            panel_index=2,
            raster_path=p2,
            raster_sha256=sha2,
            skill_move_id="SK_OVERHEAD_SMASH",
            camera_rig_id="CAM_INTO_LENS_LOW",
            camera_elevation_deg=-35.0,
            camera_azimuth_deg=-30.0,
            into_camera_axis_angle_deg=90.0,
            hammer=good_h2,
            barrage=BubbleBarrageSpec(
                bubble_count_visible=15,
                into_camera_fraction=0.9,
                exploding_near_lens_count=4,
                stream_never_clears=True,
                primary_impact_p_px=(320.0, 100.0),
            ),
        )

        for layer in range(1, 6):
            rep = run_cumulative_cross_hammer_full_reaudit([c1, c2], up_to_layer=layer)
            self.assertTrue(rep.passed, f"L{layer}: {rep.blocking_errors}")
            self.assertEqual(
                rep.status, "PASSED_CUMULATIVE_CROSS_HAMMER_REAUDIT_ADVANCE_APPROVED"
            )
            self.assertEqual(rep.visual_acceptance_status, "NOT_VERIFIED_BY_CODE")
            self.assertEqual(rep.contract_id, "CROSS_HAMMER_INTO_CAMERA_BUBBLE_L1_L5")


if __name__ == "__main__":
    unittest.main()
