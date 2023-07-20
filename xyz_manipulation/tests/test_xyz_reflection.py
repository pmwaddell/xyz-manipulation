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
from xyz_operate import transform_lines
from xyz_reflection import reflect, Plane


class TestXYZReflection(unittest.TestCase):
    """Tests functionality from xyz_reflection.py"""

    def setUp(self):
        with open('test.xyz') as file_object:
            self.test_lines = file_object.read().split('\n')

    def do_reflection_test(self, plane: Plane, success_filename: str):
        """
        Tests the operate_on_lines function with reflect on the file
        test.xyz, by comparing with the contents of the corresponding file.

        Parameters
        ----------
        plane : Plane
            Plane used for the reflection test.
        success_filename : str
            Filename of the .xyz file after the successful reflection for
            each test, used for comparison.
        """
        reflection_attempt_lines = transform_lines(
            self.test_lines, reflect, plane).split('\n')
        with open(success_filename) as file_object:
            self.success_lines = file_object.read().split('\n')
        for i in range(len(reflection_attempt_lines)):
            self.assertEqual(reflection_attempt_lines[i],
                             self.success_lines[i])

    def test_refl_origin_0_0_1(self):
        """
        Tests reflection through the plane defined by the origin and normal
        vector <0, 0, 1>.
        """
        test_plane = Plane(point=[0, 0, 0], normal_vector=[0, 0, 1])
        self.do_reflection_test(test_plane, 'test_refl_origin_0_0_1.xyz')

    def test_refl_origin_0_1_0(self):
        """
        Tests reflection through the plane defined by the origin and normal
        vector <0, 1, 0>.
        """
        test_plane = Plane(point=[0, 0, 0], normal_vector=[0, 1, 0])
        self.do_reflection_test(test_plane, 'test_refl_origin_0_1_0.xyz')

    def test_refl_origin_1_0_0(self):
        """
        Tests reflection through the plane defined by the origin and normal
        vector <1, 0, 0>.
        """
        test_plane = Plane(point=[0, 0, 0], normal_vector=[1, 0, 0])
        self.do_reflection_test(test_plane, 'test_refl_origin_1_0_0.xyz')
