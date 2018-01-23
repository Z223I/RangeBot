#!usr/bin/python

import sys
sys.path.append("/home/pi/pythondev/Lidar-Lite-3_Threaded")
# print(sys.path)
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

        self.servo = Servo(servo_channel)
        self.lidar = LidarLiteChild()
        init_ok = self.lidar.init()
        if not init_ok:
            print("ERROR: Lidar failed to initialize.")

        self.clip_distance = 5

    def scan(self, min_angle, max_angle, step):
        """ The scan method uses the servo and Lidar to
        return a list of angle and range pairs."""

        # Initialize the angle and range pairs list.
        angles = []
        ranges = []

        current_angle = min_angle
        while current_angle <= max_angle:
            # print("Angle: ", current_angle)

            # Position the servo
            self.servo.set_angle(current_angle)

            # Allow servo to finish its move
            if current_angle == min_angle:
                # Give the servo extra time to get to the first angle.
                time.sleep(1)
            else:
                time.sleep(.25)

            # Read the lidar
            range = self.lidar.read()
            range = int(range * 10)
            range = float(range) / 10.0

            # Place angle and range in respective lists
            angles.append(current_angle)
            ranges.append(range)

            # Increment current angle
            current_angle += step

        return angles, ranges

    def find_target(self, angles, ranges):
        """ The find_target method takes as input a list of
        angle and range pairs.  It searches the list for the 
        smallest range."""

        # Found the next line on StackOverflow.com.  But, xrange couldn't
        # be found.  Am using Python 3.  The page said xrange was built-in.
        # index_min = min(xrange(len(ranges)), key=ranges.__getitem__)

        # Method #1 Just use the minimum.
        minimum, index = min((ranges[i], i) for i in range(len(ranges)))

        # Method #2 Average three ranges and then take the minimum.
        range_averages = []
        range_count = len(ranges)
        assert(range_count >= 3) # If it isn't the following code will break.
        for i in range(range_count):
            if i == 0:
                # Use first three numbers of the list.
                mean_val = (ranges[i] + ranges[i + 1] + ranges[i + 2]) / 3
            elif i == range_count - 1:
                # Use last three numbers of the list.
                mean_val = (ranges[i - 2] + ranges[i - 1] + ranges[i]) / 3
            else:
                mean_val = (ranges[i - 1] + ranges[i] + ranges[i + 1]) / 3
            range_averages.append(mean_val)
        minimum, index = min((range_averages[i], i) 
            for i in range(len(range_averages)))

        minimum = int(minimum * 10) / 10.0

        location = [angles[index], minimum]

        return location

    def find_target2(self, angles, ranges):
        "find_target2"

        print
        print(ranges)
        
        minimum, index = min((ranges[i], i) for i in range(len(ranges)))

        print(minimum)

        clipped_ranges = []
        for i in range(len(ranges)):
            if ranges[i] < minimum + self.clip_distance:
               clipped_ranges.append(1)
            else:
               clipped_ranges.append(0)

        print(clipped_ranges)



#        self.clip_distance = 5
#        self.array[1]



    def execute(self, min_angle, max_angle, step):
        angles, ranges = self.scan(min_angle, max_angle, step)
        print("Angles: ", angles)
        print("Ranges: ", ranges)

        target_location = self.find_target(angles, ranges)
#        print("Target location: ", target_location

        self.find_target2(angles, ranges)

        return target_location


if __name__ == "__main__":
    range_bot = RangeBot(4)

    min_angle = -10
    max_angle = 10
    step = 1

    target_location = range_bot.execute(min_angle, max_angle, step)
    print(target_location)

    print("Bye!")
