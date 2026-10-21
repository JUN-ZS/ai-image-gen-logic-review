import unittest
from bubble_break.t_hammer_multiview_swing_engine import (
    AXES, CAMERAS, build_matrix, camera_frame, dot, length, make_variant,
    pose_vertices, render_proxy_svg, mul, unit,
)


class TestTHammerMultiViewSwingEngine(unittest.TestCase):
    def test_full_matrix_and_unique_variant_ids(self):
        matrix = build_matrix()
        self.assertEqual(len(AXES), 8)
        self.assertEqual(len(CAMERAS), 12)
        self.assertEqual(matrix['counts']['total_variants'], 192)
        ids = [x['variant_id'] for x in matrix['variants']]
        self.assertEqual(len(ids), len(set(ids)))

    def test_opposed_terminal_face_normals_and_orthogonal_handles(self):
        for axis in AXES:
            n = unit(axis.normal)
            self.assertAlmostEqual(dot(n, mul(n, -1.0)), -1.0, places=7)
            variant = make_variant(axis, CAMERAS[1], 0)
            g = variant['geometry']
            self.assertAlmostEqual(g['normal_dot'], -1.0, places=7)
            self.assertAlmostEqual(g['attacker_handle_dot'], 0.0, places=7)
            self.assertAlmostEqual(g['target_handle_dot'], 0.0, places=7)

    def test_stage_gap_definition_and_followthrough(self):
        for axis in AXES:
            g = make_variant(axis, CAMERAS[0], 0)['geometry']
            self.assertAlmostEqual(g['H0_total_gap'], 50.0, places=7)
            self.assertAlmostEqual(g['H2_gap'], 0.0, places=7)
            self.assertAlmostEqual(g['H3_advance'], 15.0, places=7)

    def test_end_caps_share_plane_and_square_contact_patch(self):
        for axis in AXES:
            v = make_variant(axis, CAMERAS[2], 0)
            a = pose_vertices(v['poses']['H2_attacker'])['front']
            b = pose_vertices(v['poses']['H2_target'])['front']
            self.assertTrue(all(abs(x-y) < 1e-6 for x,y in zip(v['poses']['H2_attacker']['face_center'], v['poses']['H2_target']['face_center'])))
            sa = sorted(tuple(round(c, 6) for c in p) for p in a)
            sb = sorted(tuple(round(c, 6) for c in p) for p in b)
            self.assertEqual(sa, sb)

    def test_camera_change_does_not_change_contact_geometry(self):
        axis = AXES[4]
        first = make_variant(axis, CAMERAS[0], 0)['geometry']
        other = make_variant(axis, CAMERAS[8], 0)['geometry']
        for key in ('P', 'attacker_normal', 'target_normal', 'normal_dot', 'H0_total_gap', 'H2_gap'):
            self.assertEqual(first[key], other[key])
        self.assertTrue(first['camera_view_only'] and other['camera_view_only'])

    def test_camera_frames_are_orthonormal_and_varied(self):
        frames = [camera_frame(AXES[4].normal, c) for c in CAMERAS]
        for pos, forward, right, up in frames:
            for vec in (pos, forward, right, up):
                self.assertAlmostEqual(length(vec), 1.0, places=6)
            self.assertAlmostEqual(dot(forward, right), 0.0, places=6)
            self.assertAlmostEqual(dot(forward, up), 0.0, places=6)
            self.assertAlmostEqual(dot(right, up), 0.0, places=6)
        self.assertGreaterEqual(len({tuple(round(x, 4) for x in f[0]) for f in frames}), 10)

    def test_prompt_contract_and_honest_image_gate(self):
        for v in build_matrix()['variants']:
            self.assertIn('terminal', v['prompts']['H2_first_contact'].lower())
            self.assertIn('handle', v['prompts']['H2_first_contact'].lower())
            self.assertIn('camera', v['prompts']['H2_first_contact'].lower())
            self.assertEqual(v['audit_status']['image_realization'], 'NOT_RUN')
            self.assertEqual(v['audit_status']['pixel_audit'], 'NOT_RUN')

    def test_single_hammer_sphere_scene_is_not_confused_with_dual_hammer_proof(self):
        first = make_variant(AXES[0], CAMERAS[0], 0)
        stage_a = first['prompts']['stage_a_two_hammer_proof'].lower()
        scene_h2 = first['prompts']['H2_first_contact'].lower()
        self.assertIn('exactly two', stage_a)
        self.assertIn('exactly one attacking t-hammer', scene_h2)
        self.assertIn('sphere outward normal', scene_h2)

    def test_windup_profiles_are_different_but_share_impact_axis(self):
        a = make_variant(AXES[4], CAMERAS[1], 0)
        b = make_variant(AXES[4], CAMERAS[1], 1)
        self.assertNotEqual(a['windup_profile']['profile_id'], b['windup_profile']['profile_id'])
        self.assertNotEqual(a['prompts']['H0_preimpact'], b['prompts']['H0_preimpact'])
        self.assertEqual(a['geometry']['attacker_normal'], b['geometry']['attacker_normal'])
        self.assertEqual(a['geometry']['target_normal'], b['geometry']['target_normal'])

    def test_svg_proxy_is_not_pixel_proof_and_cameras_change_projection(self):
        a = make_variant(AXES[0], CAMERAS[0], 0)
        b = make_variant(AXES[0], CAMERAS[2], 0)
        svg_a = render_proxy_svg(a)
        svg_b = render_proxy_svg(b)
        self.assertIn('data-image-realization="NOT_RUN"', svg_a)
        self.assertIn('NOT pixel proof', svg_a)
        self.assertNotEqual(svg_a, svg_b)


if __name__ == '__main__':
    unittest.main(verbosity=2)
