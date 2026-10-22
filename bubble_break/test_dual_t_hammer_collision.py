from __future__ import annotations

import unittest

from bubble_break.dual_t_hammer_collision import (
    CAMERA_VIEWS,
    compile_camera_matrix,
    compile_dual_hammer_prompt,
    default_dual_t_hammer_contract,
    validate_collision_evidence,
)


def evidence(**overrides):
    data = {
        "stage": "FIRST_CONTACT",
        "contact_surface": "END_FACE_TO_END_FACE",
        "signed_gap": 0.0,
        "face_normal_a": [1.0, 0.0, 0.0],
        "face_normal_b": [-1.0, 0.0, 0.0],
        "face_center_a": [0.0, 0.0, 0.0],
        "face_center_b": [0.0, 0.0, 0.0],
        "contact_point": [0.0, 0.0, 0.0],
        "contact_point_on_face_a": True,
        "contact_point_on_face_b": True,
        "tool_a_present": True,
        "tool_b_present": True,
        "separate_handles": True,
        "evidence_source": "test_geometry_fixture",
    }
    data.update(overrides)
    return data


class DualTHammerCollisionTests(unittest.TestCase):
    def test_contract_defines_two_distinct_t_hammers_with_opposed_end_faces(self):
        contract = default_dual_t_hammer_contract()
        self.assertEqual(contract.tool_a.tool_id, "HAMMER_A")
        self.assertEqual(contract.tool_b.tool_id, "HAMMER_B")
        self.assertNotEqual(contract.tool_a.tool_id, contract.tool_b.tool_id)
        self.assertEqual(contract.allowed_contact_surfaces, ("END_FACE_TO_END_FACE",))
        self.assertEqual(contract.validate_definition(), [])

    def test_true_end_face_to_end_face_contact_passes(self):
        result = validate_collision_evidence(evidence())
        self.assertTrue(result["accepted"], result["errors"])
        self.assertEqual(result["status"], "GEOMETRY_EVIDENCE_PASS")
        self.assertEqual(result["metrics"]["normal_error_degrees"], 0.0)

    def test_cheek_collision_is_not_misclassified_as_a_strike(self):
        result = validate_collision_evidence(evidence(contact_surface="CHEEK"))
        self.assertFalse(result["accepted"])
        self.assertTrue(any("forbidden first-contact surface" in e for e in result["errors"]))

    def test_wrong_plane_or_parallel_normals_fail(self):
        result = validate_collision_evidence(evidence(face_normal_b=[1.0, 0.0, 0.0]))
        self.assertFalse(result["accepted"])
        self.assertTrue(any("normals are not opposing" in e for e in result["errors"]))

    def test_first_contact_with_a_gap_fails_even_if_glow_might_be_visible(self):
        result = validate_collision_evidence(evidence(signed_gap=0.12))
        self.assertFalse(result["accepted"])
        self.assertTrue(any("zero gap" in e for e in result["errors"]))

    def test_first_contact_point_must_belong_to_both_faces(self):
        result = validate_collision_evidence(evidence(contact_point_on_face_b=False))
        self.assertFalse(result["accepted"])
        self.assertTrue(any("point P must lie on both strike faces" in e for e in result["errors"]))

    def test_both_tools_and_separate_handles_are_required(self):
        result = validate_collision_evidence(evidence(tool_b_present=False, separate_handles=False))
        self.assertFalse(result["accepted"])
        self.assertTrue(any("both distinct hammer instances" in e for e in result["errors"]))
        self.assertTrue(any("each hammer must retain its own distinct handle" in e for e in result["errors"]))

    def test_precontact_gap_windows_are_not_interchangeable_with_contact(self):
        far = validate_collision_evidence(evidence(stage="PRE_FAR", contact_surface="NONE", signed_gap=100))
        near = validate_collision_evidence(evidence(stage="PRE_NEAR", contact_surface="NONE", signed_gap=20))
        touching_too_early = validate_collision_evidence(evidence(stage="PRE_NEAR", contact_surface="END_FACE_TO_END_FACE", signed_gap=0))
        self.assertTrue(far["accepted"], far["errors"])
        self.assertTrue(near["accepted"], near["errors"])
        self.assertFalse(touching_too_early["accepted"])

    def test_prompt_says_dual_tools_and_forbids_bubble_and_cheek_contact(self):
        prompt = compile_dual_hammer_prompt("FIRST_CONTACT")
        self.assertIn("HAMMER_A", prompt)
        self.assertIn("HAMMER_B", prompt)
        self.assertIn("FLAT END FACES", prompt)
        self.assertIn("CHEEK", prompt)
        self.assertIn("no bubble as target", prompt)
        self.assertNotIn("Create one cinematic 16:9 image with exactly ONE large, intact", prompt)

    def test_camera_matrix_generates_independent_single_frame_variants(self):
        result = compile_camera_matrix("FIRST_CONTACT", CAMERA_VIEWS[:5])
        self.assertEqual(len(result), 5)
        self.assertEqual(len({r["variant_id"] for r in result}), 5)
        self.assertEqual(len({r["camera_view"] for r in result}), 5)
        self.assertTrue(all("not a grid" in r["prompt"] for r in result))


if __name__ == "__main__":
    unittest.main()
