import unittest
from operate import operate_on_lines
from xyz_translation import translate


class TestXYZTranslation(unittest.TestCase):
    """Tests functionality from xyz_translation.py"""

    def setUp(self) -> None:
        with open('test.xyz') as file_object:
            self.test_lines = file_object.read().split('\n')
        self.dv = [-0.221753, -6.076221, -4.034970]
        with open('test translated success.xyz') as file_object:
            self.success_lines = file_object.read().split('\n')

    def test_translation(self) -> None:
        translation_attempt_lines = operate_on_lines(
            self.test_lines, translate, self.dv).split('\n')
        for i in range(len(translation_attempt_lines)):
            self.assertEqual(translation_attempt_lines[i],
                             self.success_lines[i])
