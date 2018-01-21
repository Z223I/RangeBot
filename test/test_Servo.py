try:
    from builtins import object
except ImportError:
    pass

#import warnings
#import sys

#from unittest import TestCase  #, skipIf
import unittest
import time

from Servo import Servo

class TestServo(unittest.TestCase):
    CHANNEL = 4

    def setUp(self):
        self.testservo = Servo(TestServo.CHANNEL)

    def tearDown(self):
        pass

    def test___init___(self):
        self.assertEqual(self.testservo.channel, TestServo.CHANNEL)

        self.assertEqual(130, self.testservo.SERVO_MIN)
        self.assertEqual(630, self.testservo.SERVO_MAX)

        self.assertEqual(self.testservo.SERVO_MIN, self.testservo.servo_min)
        self.assertEqual(self.testservo.SERVO_MAX, self.testservo.servo_max)

        self.assertEqual(-90, self.testservo.ANGLE_MIN)
        self.assertEqual(+90, self.testservo.ANGLE_MAX)

        self.assertEqual(self.testservo.ANGLE_MIN, self.testservo.angle_min)
        self.assertEqual(self.testservo.ANGLE_MAX, self.testservo.angle_max)

        self.assertEqual(self.testservo.angle, None)

    def test_set_angle_valid_input(self):
        self.testservo.set_angle(90)
        self.assertEqual(self.testservo.angle, 90)
        time.sleep(1)

        self.testservo.set_angle(0)
        self.assertEqual(self.testservo.angle, 0)
        time.sleep(1)

        self.testservo.set_angle(-90)
        self.assertEqual(self.testservo.angle, -90)
        time.sleep(1)

        self.testservo.set_angle(-45)
        self.assertEqual(self.testservo.angle, -45)
        time.sleep(1)

    def test_set_angle_invalid_input(self):
        # This number is too high.  It should be reduced
        # to the maximum allowed.
        self.testservo.set_angle(90.5)
        self.assertEqual(self.testservo.angle, 90)
        time.sleep(1)

        # This number is too low.  It should be increased
        # to the minimum allowed.
        self.testservo.set_angle(-90.1)
        self.assertEqual(self.testservo.angle, -90)
        time.sleep(1)

#    def test_listify(self):



if __name__ == "__main__":

    unittest.main()
