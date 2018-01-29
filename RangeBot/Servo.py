#!usr/bin/python

"""Servo class
Author: Bruce Wilson
License: GNU 3

Based on...
Simple demo of of the PCA9685 PWM servo/LED controller library.
This will move channel 0 from min to max position repeatedly.
Author: Tony DiCola
License: Public Domain
"""

# from __future__ import division
import time

import sys

# Import the PCA9685 module.
sys.path.append("/home/pi/pythondev/Adafruit_Python_PCA9685/Adafruit_PCA9685")
#print( sys.path )
import PCA9685


# Uncomment to enable debug output.
# import logging
# logging.basicConfig(level=logging.DEBUG)

class Servo:

    """ Class: Servo
    This class provides a mechanism to control a servo based on angles.
    The is a method for using pulse duration."""

    # Configure min and max servo pulse lengths
    SERVO_MIN = 130  # Min pulse length out of 4096
    SERVO_MAX = 630  # Max pulse length out of 4096

    # Establish constants for min and max angles.
    ANGLE_MIN = -90
    ANGLE_MAX = 90

    def __init__(self, _channel):
        """ Method: __init__
        Provides set up necessary to control a servo using
        Adafruit's PCA9685 PWM board."""

        # Initialise the PCA9685 using the default address (0x40).
#        self.pwm = PCA9685.PCA9685()
        self.pwm = PCA9685.PCA9685(address=0x41)

        # Alternatively specify a different address and/or bus:
        # self.pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

        # Configure min and max servo pulse lengths
        self.servo_min = Servo.SERVO_MIN
        self.servo_max = Servo.SERVO_MAX

        # Angles can be used to control the servo instead of using frequency.
        self.angle_min = Servo.ANGLE_MIN
        self.angle_max = Servo.ANGLE_MAX

        self.channel = _channel

        # Set frequency to 60hz, good for servos.
        self.pwm.set_pwm_freq(60)

        self.angle = None

    # Helper function to make setting a servo pulse width simpler.
    def set_servo_pulse(self, channel, pulse):

        """ set_servo_pulse method
        Author: Tony DiCola"""
        pulse_length = 1000000    # 1,000,000 us per second
        pulse_length //= 60       # 60 Hz
        print('{0}us per period'.format(pulse_length))
        pulse_length //= 4096     # 12 bits of resolution
        print('{0}us per bit'.format(pulse_length))
        pulse *= 1000
        pulse //= pulse_length
        self.pwm.set_pwm(channel, 0, pulse)

    def get_angle(self):

        """ Method: angle
        Returns the approximate angle of the servo."""

        return self.angle

    def set_angle(self, _angle):
        """ Move the servo to the desired angle.
        Set the attribule angle.
        """
        # Adjust for slight error in servo.
        _angle += 6

        if _angle < self.ANGLE_MIN:
            _angle = self.ANGLE_MIN

        if _angle > self.ANGLE_MAX:
            _angle = self.ANGLE_MAX

        # Calculate the usable azimuth range in degrees.
        total_degrees = self.ANGLE_MAX - self.ANGLE_MIN

        # Calculate the range of pulse durations.
        total_pulse = self.SERVO_MAX - self.SERVO_MIN

        pulse_per_degree = float(total_pulse) / float(total_degrees)

#        print "Total usable pulse duration: ", total_pulse
#        print "Pulse duration per degree: ", pulse_per_degree
#        print "Adjusted angle: ", (_angle - self.ANGLE_MIN)

        pulse = self.SERVO_MIN + (pulse_per_degree * (_angle - self.ANGLE_MIN))
        pulse = int(pulse)
        if pulse < self.SERVO_MIN:
            pulse = self.SERVO_MIN
        if pulse > self.SERVO_MAX:
            pulse = self.SERVO_MAX

        START_PULSE = 0

#        print "Angle: ", _angle
#        print "Pulse: ", pulse

        self.pwm.set_pwm(self.channel, START_PULSE, pulse)

        # TODO: Calculate the current angle based on the pulse duration.

        self.angle = _angle
        return self.angle

    def test(self):
        """ method test uses the pulse duration to exercise the servo between
        min and max."""

        for i in range(2):
            START_PULSE = 0
            self.pwm.set_pwm(self.channel, START_PULSE, self.servo_min)
            time.sleep(1)
            self.pwm.set_pwm(self.channel, START_PULSE, self.servo_max)
            time.sleep(1)

    def test2(self):
        """ method test2 uses angles to exercise the servo between min
        and max."""
        for i in range(3):
            self.set_angle(-90)
            time.sleep(2)
            self.set_angle(90)
            time.sleep(2)

    def center(self):
        self.set_angle(0)

if __name__ == "__main__":

    print('Moving servo on channel 3, press Ctrl-C to quit...')

    SERVO = Servo(3)

    SERVO.center()

#    while True:
#        SERVO.test()
#        time.sleep(1.5)

#        SERVO.test2()
#        time.sleep(3)
