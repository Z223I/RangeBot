try:
    from builtins import object
except ImportError:
    pass

#import warnings
#import sys

#from unittest import TestCase  #, skipIf
import unittest
import time

from RangeBot import RangeBot

class TestRangeBot(unittest.TestCase):
    CHANNEL = 4

    def setUp(self):
        self.testrangebot = RangeBot()

    def tearDown(self):
        pass

    def test___init___(self):
        self.assertEqual(True, True)

#    def test_listify(self):



if __name__ == "__main__":

    unittest.main()
