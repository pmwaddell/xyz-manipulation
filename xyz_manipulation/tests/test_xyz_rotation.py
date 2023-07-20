#!/usr/bin/env python3
__author__ = "Peter Waddell"
__copyright__ = "Copyright 2023"
__credits__ = ["Peter Waddell"]
__version__ = "0.0.1"
__date__ = "2023/7/16"
__maintainer__ = "Peter Waddell"
__email__ = "pmwaddell9@gmail.com"
__status__ = "Prototype"

import unittest
from typing import List
from xyz_operate import transform_lines
from xyz_rotation import rotate, get_compound_rotation_matrices


class TestXYZRotation(unittest.TestCase):
    """Tests functionality from xyz_rotation.py"""

    def setUp(self):
        with open('test.xyz') as file_object:
            self.test_lines = file_object.read().split('\n')

    def do_rotation_test(self,
                         rotation_axis: List,
                         theta: float,
                         success_filename: str):
        """
        Tests the operate_on_lines function with rotate on the file
        test.xyz, by comparing with the contents of the corresponding file.

        Parameters
        ----------
        rotation_axis : List
            List of  floats: coordinates of the rotation axis (which is taken
            to be between the origin and this input point).
        theta : float
            Number of degrees for the rotation.
        success_filename : str
            Filename of the .xyz file after the successful rotation for
            each test, used for comparison.
        """
        rotation_attempt_lines = transform_lines(self.test_lines, rotate,
                                                 get_compound_rotation_matrices(
                                                     rotation_axis,
                                                     theta)).split('\n')
        with open(success_filename) as file_object:
            self.success_lines = file_object.read().split('\n')
        for i in range(len(rotation_attempt_lines)):
            self.assertEqual(rotation_attempt_lines[i],
                             self.success_lines[i])

    def test_rot_1_2_3_30d(self):
        """
        Tests rotation around the axis <1, 2, 3> by 30 degrees.
        """
        self.do_rotation_test([1, 2, 3], 30, 'test_rot_1_2_3_30d.xyz')

    def test_rot_1_2_3_neg30d(self):
        """
        Tests rotation around the axis <1, 2, 3> by -30 degrees.
        """
        self.do_rotation_test([1, 2, 3], -30, 'test_rot_1_2_3_neg30d.xyz')

    def test_rot_neg1_2_3_30d(self):
        """
        Tests rotation around the axis <-1, 2, 3> by 30 degrees.
        """
        self.do_rotation_test([-1, 2, 3], 30, 'test_rot_neg1_2_3_30d.xyz')

    def test_rot_1_neg2_3_30d(self):
        """
        Tests rotation around the axis <1, -2, 3> by 30 degrees.
        """
        self.do_rotation_test([1, -2, 3], 30, 'test_rot_1_neg2_3_30d.xyz')

    def test_rot_1_2_neg3_30d(self):
        """
        Tests rotation around the axis <1, 2, -3> by 30 degrees.
        """
        self.do_rotation_test([1, 2, -3], 30, 'test_rot_1_2_neg3_30d.xyz')

    def test_rot_neg1_neg2_3_30d(self):
        """
        Tests rotation around the axis <-1, -2, 3> by 30 degrees.
        """
        self.do_rotation_test([-1, -2, 3], 30, 'test_rot_neg1_neg2_3_30d.xyz')

    def test_rot_neg1_neg2_neg3_30d(self):
        """
        Tests rotation around the axis <-1, -2, -3> by 30 degrees.
        """
        self.do_rotation_test([-1, -2, -3], 30,
                              'test_rot_neg1_neg2_neg3_30d.xyz')

    def test_rot_1_0_0_63d(self):
        """
        Tests rotation around the axis <1, 0, 0> by 63 degrees.
        """
        self.do_rotation_test([1, 0, 0], 63, 'test_rot_1_0_0_63d.xyz')

    def test_rot_0_1_0_63d(self):
        """
        Tests rotation around the axis <0, 1, 0> by 63 degrees.
        """
        self.do_rotation_test([0, 1, 0], 63, 'test_rot_0_1_0_63d.xyz')

    def test_rot_0_0_1_63d(self):
        """
        Tests rotation around the axis <0, 0, 1> by 63 degrees.
        """
        self.do_rotation_test([0, 0, 1], 63, 'test_rot_0_0_1_63d.xyz')

    def test_rot_6_3_neg11_360d(self):
        """
        Tests rotation around the axis <6, 3, -11> by 360 degrees.
        """
        self.do_rotation_test([6, 3, -11], 360, 'test_rot_6_3_neg11_360d.xyz')

    def test_rot_6_3_neg11_234250d(self):
        """
        Tests rotation around the axis <6, 3, -11> by 234250 degrees.
        """
        self.do_rotation_test([6, 3, -11], 234250,
                              'test_rot_6_3_neg11_234250d.xyz')
