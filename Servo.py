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
    def __init__(self):
        # Initialise the PCA9685 using the default address (0x40).
        self.pwm = Adafruit_PCA9685.PCA9685()

        # Alternatively specify a different address and/or bus:
        #self.pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)
        
        # Configure min and max servo pulse lengths

        self.servo_MIN = 130  # Min pulse length out of 4096
        self.servo_MAX = 630  # Max pulse length out of 4096
        
        # Configure min and max servo pulse lengths
        self.servo_min = self.servo_MIN
        self.servo_max = self.servo_MAX

        # Establish constants for min and max angles.
        self.ANGLE_MIN = -90
        self.ANGLE_MAX = 90

        # Angles can be used to control the servo instead of using frequency.
        self.angle_min = self.ANGLE_MIN
        self.angle_max = self.ANGLE_MAX

        # Set frequency to 60hz, good for servos.
        self.pwm.set_pwm_freq(60)

    # Helper function to make setting a servo pulse width simpler.
    def set_servo_pulse(self, channel, pulse):
            pulse_length = 1000000    # 1,000,000 us per second
            pulse_length //= 60       # 60 Hz
            print('{0}us per period'.format(pulse_length))
            pulse_length //= 4096     # 12 bits of resolution
            print('{0}us per bit'.format(pulse_length))
            pulse *= 1000
            pulse //= pulse_length
            self.pwm.set_pwm(channel, 0, pulse)


    def test(self):
        print "test"
#        try:
        while True:
            print "test while loop"

      	    # Move servo on channel O between extremes.
      	    self.pwm.set_pwm(4, 0, self.servo_min)
       	    time.sleep(1)
            self.pwm.set_pwm(4, 0, self.servo_max)
            time.sleep(1)
	
#	except:
    	pass
	
	pulse_start = 0
	pulse_stop  = 0
	self.pwm.set_pwm(4, pulse_start, pulse_stop)
	







if __name__ == "__main__":

    print('Moving servo on channel 4, press Ctrl-C to quit...')

    servo = Servo()
    servo.test()
