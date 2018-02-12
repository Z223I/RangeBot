try:
    from builtins import object
except ImportError:
    pass

import unittest
from unittest.mock import patch

import time

import sys
sys.path.append('/home/pi/pythondev/RangeBot/RangeBot')
from RangeBot import RangeBot

class TestRangeBot(unittest.TestCase):
    CHANNEL = 4

    def setUp(self):
        self.test_range_bot = RangeBot(TestRangeBot.CHANNEL)

    def tearDown(self):
        pass

    @patch('RangeBot.LidarLite3Ext.read')
    def test_scan2(self, mock_read):
        mock_read.return_value = 80

        est_tgt_r = 30
        half_angle = 5
        min_angle = -half_angle
        max_angle = half_angle
        step = 2 * half_angle / 10
        angles, ranges = \
            self.test_range_bot.scan2(est_tgt_r, min_angle, max_angle, step)
        print(ranges)



if __name__ == "__main__":

    unittest.main()
