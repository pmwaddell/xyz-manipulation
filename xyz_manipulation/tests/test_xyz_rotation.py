import unittest
from typing import List
from xyz_operate import operate_on_lines
from xyz_rotation import rotate, get_compound_rotation_matrices


class TestXYZRotation(unittest.TestCase):
    """Tests functionality from xyz_rotation.py"""

    def setUp(self):
        with open('test.xyz') as file_object:
            self.test_lines = file_object.read().split('\n')
        with open('test_rot_1_2_3_30d.xyz') as file_object:
            self.success_lines = file_object.read().split('\n')

    def do_rotation_test(self,
                 rotation_axis: List,
                 theta: float,
                 success_filename: str):
        rotation_attempt_lines = operate_on_lines(
            self.test_lines, rotate,
            get_compound_rotation_matrices(rotation_axis, theta)).split('\n')
        with open(success_filename) as file_object:
            self.success_lines = file_object.read().split('\n')
        for i in range(len(rotation_attempt_lines)):
            self.assertEqual(rotation_attempt_lines[i],
                             self.success_lines[i])

    def test_rot_1_2_3_30d(self):
        self.do_rotation_test([1, 2, 3], 30, 'test_rot_1_2_3_30d.xyz')

    def test_rot_1_2_3_neg30d(self):
        self.do_rotation_test([1, 2, 3], -30, 'test_rot_1_2_3_neg30d.xyz')

    def test_rot_neg1_2_3_30d(self):
        self.do_rotation_test([-1, 2, 3], 30, 'test_rot_neg1_2_3_30d.xyz')

    def test_rot_1_neg2_3_30d(self):
        self.do_rotation_test([1, -2, 3], 30, 'test_rot_1_neg2_3_30d.xyz')

    def test_rot_1_2_neg3_30d(self):
        self.do_rotation_test([1, 2, -3], 30, 'test_rot_1_2_neg3_30d.xyz')

    # x, y, z axes w letters and manual
    # arbitrary rotation axes: all positive, all negative, one negative, two negative
    # large angles, very large angles
    # negative angles
