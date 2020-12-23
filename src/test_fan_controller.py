import unittest
from fan_controller import FanController


class TestFanController(unittest.TestCase):

    def test_fan_controller_sets_mode_to_manual_when_temp_is_below_70(self):
        fc = FanController()
        fc.exec(test_temp=69)
        self.assertEqual(fc.get_status(), 0)
        fc.exec(test_temp=75)
        fc.exec(test_temp=50)
        self.assertEqual(fc.get_status(), 0)

    def test_fan_controller_sets_mode_to_automatic_when_temp_is_above_or_equal_to_70(self):
        fc = FanController()
        fc.exec(test_temp=70)
        self.assertEqual(fc.get_status(), 1)
        fc.exec(test_temp=60)
        fc.exec(test_temp=71)
        self.assertEqual(fc.get_status(), 1)


if __name__ == '__main__':
    unittest.main()
