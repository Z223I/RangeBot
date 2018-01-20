# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
import time

# Import the PCA9685 module.
import Adafruit_PCA9685


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)



class Servo:
    def __init__(self, _channel):
        # Initialise the PCA9685 using the default address (0x40).
        self.pwm = Adafruit_PCA9685.PCA9685()

        # Alternatively specify a different address and/or bus:
        #self.pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)
        
        # Configure min and max servo pulse lengths

        self.SERVO_MIN = 130  # Min pulse length out of 4096
        self.SERVO_MAX = 630  # Max pulse length out of 4096
        
        # Configure min and max servo pulse lengths
        self.servo_min = self.SERVO_MIN
        self.servo_max = self.SERVO_MAX

        # Establish constants for min and max angles.
        self.ANGLE_MIN = -90
        self.ANGLE_MAX = 90

        # Angles can be used to control the servo instead of using frequency.
        self.angle_min = self.ANGLE_MIN
        self.angle_max = self.ANGLE_MAX

        self.channel = _channel

        # Set frequency to 60hz, good for servos.
        self.pwm.set_pwm_freq(60)

        self.angle = None

    # Helper function to make setting a servo pulse width simpler.
    def set_servo_pulse(self, channel, pulse):
            pulse_length = 1000000    # 1,000,000 us per second
            pulse_length //= 60       # 60 Hz
            print('{0}us per period'.format(pulse_length))
            pulse_length //= 4096     # 12 bits of resolution
            print('{0}us per bit'.format(pulse_length))
            pulse *= 1000
            pulse //= pulse_length
            startPulse = 0
            # pulse is now a duration.
            self.pwm.set_pwm(channel, startPulse, pulse)


    def angle(self):
        return self.angle

    def set_angle(self, _angle):



        # TODO: Error checking



        total_degrees = self.ANGLE_MAX - self.ANGLE_MIN
        total_pulse = self.SERVO_MAX - self.SERVO_MIN

        pulse_per_degree = total_pulse / total_degrees

        pulse = self.SERVO_MIN + (pulse_per_degree * (_angle - self.ANGLE_MIN))
        pulse = int(pulse)

        START_PULSE = 0
        
        self.pwm.set_pwm(self.channel, START_PULSE, pulse)
        self.angle = _angle
        return self.angle


    def test(self):
        print "test"

        for i in range(2):
            START_PULSE = 0
      	    self.pwm.set_pwm(self.channel, START_PULSE, self.servo_min)
       	    time.sleep(1)
            self.pwm.set_pwm(self.channel, START_PULSE, self.servo_max)
            time.sleep(1)
	
	

    def test2(self):
        for i in range(3):
            self.set_angle(-90)
            time.sleep(1)
            self.set_angle(90)
            time.sleep(1)





if __name__ == "__main__":

    print('Moving servo on channel 4, press Ctrl-C to quit...')

    servo = Servo(4)
    servo.test()
    time.sleep(1.5)

    servo.test2()
