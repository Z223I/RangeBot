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
        channel = 4
        self.testservo = Servo(4)

    def tearDown(self):
        pass

    def test___init___(self):
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
        self.testservo.set_angle(0)
        self.assertEqual(self.testservo.angle, 0)

        self.testservo.set_angle(90)
        self.assertEqual(self.testservo.angle, 90)

        self.testservo.set_angle(-90)
        self.assertEqual(self.testservo.angle, -90)

        self.testservo.set_angle(-45)
        self.assertEqual(self.testservo.angle, -45)

#    def test_listify(self):



if __name__ == "__main__":

    unittest.main()
