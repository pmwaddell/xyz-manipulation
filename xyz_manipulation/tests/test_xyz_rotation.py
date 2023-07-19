import unittest
from xyz_operate import operate_on_lines
from xyz_rotation import rotate


class TestXYZRotation(unittest.TestCase):
    """Tests functionality from xyz_rotation.py"""

    def setUp(self) -> None:
        with open('test.xyz') as file_object:
            self.test_lines = file_object.read().split('\n')
        #self.rotation_matrices =
        with open('test_rotated_success.xyz') as file_object:
            self.success_lines = file_object.read().split('\n')

    # x, y, z axes w letters and manual
    # arbitrary rotation axes: all positive, all negative, one negative, two negative
    # large angles, very large angles
    # negative angles
