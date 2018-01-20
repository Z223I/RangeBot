try:
    from builtins import object
except ImportError:
    pass

#import warnings
#import sys

#from unittest import TestCase  #, skipIf
import unittest


from Servo import Servo

class TestServo(unittest.TestCase):

    def setUp(self):
        pass
#        self.stuff = Stuff()

    def tearDown(self):
        pass

    def test___init___(self):
        self.assertTrue(True, True)

#    def test_listify(self):



if __name__ == "__main__":

    unittest.main()
