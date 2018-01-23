try:
    from builtins import object
except ImportError:
    pass

#import warnings

#from unittest import TestCase  #, skipIf
import unittest
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
        self.assertEqual(self.test_range_bot.clip_distance, 5)

    def test_set_clip_distance(self):
        val = 6
        self.test_range_bot.set_clip_distance(val)
        self.assertEqual(self.test_range_bot.clip_distance, val)

    def test_scan(self):
        pass

    def test_find_target2(self):
        pass

    def test_execute(self):
        pass




if __name__ == "__main__":

    unittest.main()
