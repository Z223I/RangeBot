#!usr/bin/python

from LidarLiteChild import LidarLiteChild
from Servo import Servo
import time



class RangeBot():

    """ RangeBot uses a servo and Lidar to find a target.
    The software looks for an object that is at closer
    distance and also in the middle of the scan.

    Ultimately, this class has the azimuth and range of
    the target."""

    def __init__(self, servo_channel):
        self.servo = Servo( servo_channel )
        self.lidar = LidarLiteChild()
        init_ok = self.lidar.init()
        if not init_ok:
            print( "ERROR: Lidar failed to initialize." )


    def scan(self, min_angle, max_angle, step):
        """ The scan method uses the servo and Lidar to
        return a list of angle and range pairs."""

        current_angle = min_angle
        while current_angle <= max_angle:
            print( "Angle: ", current_angle )

            # Position the servo
            self.servo.set_angle( current_angle )

            # Allow servo to finish its move
            if current_angle == min_angle:
                # Give the servo extra time to get to the first angle.
                time.sleep(1)
            else:
                time.sleep(.25)

            # Read the lidar
            self.lidar.read()

            # Place [angle, range] in list

            # Increment current angle
            current_angle += step

        return [ [-20, 5.], [0, 3.], [20, 5] ]

    def find_target(self, range_list):
        """ The find_target method takes as input a list of
        angle and range pairs.  It searches the list for the 
        smallest range."""

        return [0.0, 20.0]

    def execute(self, min_angle, max_angle, step):
        list = self.scan(min_angle, max_angle, step)
        targetLocation = self.find_target(list)
        return targetLocation


if __name__ == "__main__":
    range_bot = RangeBot(4)

    min_angle = -5
    max_angle = 5
    step = 1

    target_location = range_bot.execute( min_angle, max_angle, step )
    print ( target_location )

    print ( "Bye!" )
