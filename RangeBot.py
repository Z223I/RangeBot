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
        """ Create the Servo and LidarLiteChild objects."""

        self.servo = Servo( servo_channel )
        self.lidar = LidarLiteChild()
        init_ok = self.lidar.init()
        if not init_ok:
            print( "ERROR: Lidar failed to initialize." )


    def scan(self, min_angle, max_angle, step):
        """ The scan method uses the servo and Lidar to
        return a list of angle and range pairs."""

        # Initialize the angle and range pairs list.
        angles = []
        ranges = []

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
            range = self.lidar.read()
            range = int( range * 10 )
            range = float( range ) / 10.0 

            # Place angle and range in respective lists
            angles.append( current_angle )
            ranges.append( range )

            # Increment current angle
            current_angle += step

        return angles, ranges


    def find_target(self, angles, ranges):
        """ The find_target method takes as input a list of
        angle and range pairs.  It searches the list for the 
        smallest range."""

        # Found the next line on StackOverflow.com.  But, xrange couldn't
        # be found.  Am using Python 3.  The page said xrange was built-in.
        #index_min = min( xrange(len(ranges)), key=ranges.__getitem__ )

        minimum, index = min( (ranges[i], i) for i in range( len(ranges) ) )

        location = [ angles[index], minimum ]

        return location

    def execute(self, min_angle, max_angle, step):
        angles, ranges = self.scan(min_angle, max_angle, step)
        print( "Angles: ", angles )
        print( "Ranges: ", ranges )

        target_location = self.find_target(angles, ranges)
#        print( "Target location: ", target_location
        return target_location


if __name__ == "__main__":
    range_bot = RangeBot(4)

    min_angle = -60
    max_angle = 60
    step = 10

    target_location = range_bot.execute( min_angle, max_angle, step )
    print ( target_location )

    print ( "Bye!" )
