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

    def test___init___(self):
        self.assertEqual(self.test_range_bot.clip_distance, 6)

    def test_set_clip_distance(self):
        val = 6
        self.test_range_bot.set_clip_distance(val)
        self.assertEqual(self.test_range_bot.clip_distance, val)

    def test_scan(self):
        pass

    @patch('LidarLite3Ext.LidarLite3Ext.read')
    def test_scan2(self):
        est_tgt_r = 30
        half_angle = 5
        min_angle = -half_angle
        max_angle = half_angle
        step = 2 * half_angle / 10
        self.test_range_bot.scan2(est_tgt_r, min_angle, max_angle, step)

    def test_find_target2_helper_A(self):
        # Estimated target range.
        est_tgt_r = 60
        ranges = [99, 99, 99, 99, 99, 99, 99, \
                  60, 60, 60, 60, 60, 60, 60, \
                  99, 99, 99, 99, 99, 99, 99]

        clipped_ranges, tgt_hits = \
            self.test_range_bot.find_target2_helper(est_tgt_r, ranges)

        clipped_ranges_check = [0, 0, 0, 0, 0, 0, 0, \
                                1, 1, 1, 1, 1, 1, 1, \
                                0, 0, 0, 0, 0, 0, 0]

        tgt_hits_check = 7

        self.assertEqual(clipped_ranges, clipped_ranges_check)
        self.assertEqual(tgt_hits, tgt_hits_check)


    def test_find_target2_helper_B(self):
        """test_find_target2_helper_B verifies that a small variation in the
        target range is ok."""

        # Estimated target range.
        est_tgt_r = 60
        ranges = [99, 99, 99, 99, 99, 99, 99, \
                  60, 61, 62, 63, 62, 61, 61, \
                  99, 99, 99, 99, 99, 99, 99]

        clipped_ranges, tgt_hits = \
            self.test_range_bot.find_target2_helper(est_tgt_r, ranges)

        clipped_ranges_check = [0, 0, 0, 0, 0, 0, 0, \
                                1, 1, 1, 1, 1, 1, 1, \
                                0, 0, 0, 0, 0, 0, 0]

        tgt_hits_check = 7

        self.assertEqual(clipped_ranges, clipped_ranges_check)
        self.assertEqual(tgt_hits, tgt_hits_check)

    def test_find_target2_helper_C(self):
        """test_find_target2_helper_C checks to see if close range targets
        properly get ignored."""

        # Estimated target range.
        est_tgt_r = 60
        ranges = [33, 33, 99, 99, 99, 99, 99, \
                  60, 60, 60, 60, 60, 60, 60, \
                  99, 99, 99, 99, 99, 99, 99]

        clipped_ranges, tgt_hits = \
            self.test_range_bot.find_target2_helper(est_tgt_r, ranges)

        clipped_ranges_check = [0, 0, 0, 0, 0, 0, 0, \
                                1, 1, 1, 1, 1, 1, 1, \
                                0, 0, 0, 0, 0, 0, 0]

        tgt_hits_check = 7

        self.assertEqual(clipped_ranges, clipped_ranges_check)
        self.assertEqual(tgt_hits, tgt_hits_check)

    def test_find_target2_helper_C(self):
        # Estimated target range.
        est_tgt_r = 60
        ranges = [99, 99, 99, 99, 99, 99, 99, \
                  60, 60, 60, 60, 60, 60, 60, \
                  99, 99, 99, 99, 99, 99, 99]

        clipped_ranges, tgt_hits = \
            self.test_range_bot.find_target2_helper(est_tgt_r, ranges)

        clipped_ranges_check = [0, 0, 0, 0, 0, 0, 0, \
                                1, 1, 1, 1, 1, 1, 1, \
                                0, 0, 0, 0, 0, 0, 0]

        tgt_hits_check = 7

        self.assertEqual(clipped_ranges, clipped_ranges_check)
        self.assertEqual(tgt_hits, tgt_hits_check)

    def test_find_target2(self):
        pass

    def test_execute(self):
        pass

    def test_valid_hunt_A(self):
        hits = 7
        ranges = [100,100,100,100,100,100,100, \
            24, 24, 24, 24, 24, 24, 24, \
            100,100,100,100,100,100,100]

        valid = self.test_range_bot.valid_hunt(ranges, hits)
        self.assertTrue(valid)

    def test_valid_hunt_B(self):
        # Four hits is below the threshold for a valid hunt.
        hits = 4

        # The values of ranges is irrelavent.
        ranges = [100,100,100,100,100,100,100, \
            24, 24, 24, 24, 24, 24, 24, \
            100,100,100,100,100,100,100]

        valid = self.test_range_bot.valid_hunt(ranges, hits)
        self.assertFalse(valid)

    def test_scan_info(self):
        # Use a 3, 4, 5 (36.87 degrees) right angle for testing.
        est_tgt_r = 4 * RangeBot.INCHES_PER_FOOT
        target_width = 3 * RangeBot.INCHES_PER_FOOT

        total_hits = self.test_range_bot.NORMAL_SCAN * \
                     self.test_range_bot.DESIRED_HITS

        total_scan_angle = 36.87 * self.test_range_bot.NORMAL_SCAN
        HALF_ANGLE = total_scan_angle / 2.0

        STEP_ANGLE = total_scan_angle / total_hits

        scan_half_angle, step_angle = \
            self.test_range_bot.scan_info(est_tgt_r, target_width)
        
        scan_half_angle = "[:.3f]".format(scan_half_angle)
        HALF_ANGLE = "[:.3f]".format(HALF_ANGLE)
        self.assertEqual(scan_half_angle, HALF_ANGLE)


        step_angle = "[:.3f]".format(step_angle)
        STEP_ANGLE = "[:.3f]".format(STEP_ANGLE)
        self.assertEqual(step_angle, STEP_ANGLE)

    def test_execute_hunt(self):
        pass




if __name__ == "__main__":

    unittest.main()
