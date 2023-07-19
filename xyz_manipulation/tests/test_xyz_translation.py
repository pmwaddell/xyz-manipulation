import unittest
from xyz_operate import operate_on_lines
from xyz_translation import translate


class TestXYZTranslation(unittest.TestCase):
    """Tests functionality from xyz_translation.py"""

    def setUp(self) -> None:
        with open('test.xyz') as file_object:
            self.test_lines = file_object.read().split('\n')
        self.dv = [-0.221753, -6.076221, -4.034970]
        with open('test_translated_success.xyz') as file_object:
            self.success_lines = file_object.read().split('\n')

    def test_translation(self) -> None:
        """
        Tests the operate_on_lines function with translate on the file
        test.xyz, by comparing with the contents of test_translated_success.xyz.
        """
        translation_attempt_lines = operate_on_lines(
            self.test_lines, translate, self.dv).split('\n')
        for i in range(len(translation_attempt_lines)):
            self.assertEqual(translation_attempt_lines[i],
                             self.success_lines[i])
