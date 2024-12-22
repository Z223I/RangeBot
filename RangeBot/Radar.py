#!usr/bin/python

# DreamPie
# J
# Komodo Edit
# SPE <-- **


import sys
sys.path.append("/home/pi/pythondev/LidarLite3Ext/LidarLite3Ext")
# print(sys.path)

from LidarLite3Ext import LidarLite3Ext
from Servo import Servo
import time
import math

import pdb
import logging
logger = logging.getLogger(__name__)
hdlr = logging.FileHandler('Radar.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)



class Radar():

    """ Radar uses a servo and Lidar to find a target.
    The software looks for an object that is at closer
    distance and also in the middle of the scan.

    Ultimately, this class has the azimuth and range of
    the target."""

    INCHES_PER_FOOT = 12

    def __init__(self, servo_channel):
        """ Create the Servo and LidarLite3Ext objects."""

        self.servo = Servo(servo_channel)
        self.lidar = LidarLite3Ext()
        init_ok = self.lidar.init()
        if not init_ok:
            print("ERROR: Lidar failed to initialize.")


    def scan(self, min_angle=-90.0, max_angle=90.0, step=10.0):
        """
        The scan method uses the servo and Lidar to return a list of
        angle and range pairs.

        @type: float
        @param: min_angle

        @type: float
        @param: max_angle

        @type: float
        @param: step (size of step.  not step count)

        @rtype: float list
        @param: angles

        @rtype: float list
        @param: ranges
        """

        # pdb.set_trace()
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
                time.sleep(.10)

            # Read the lidar
            ranges_1 = []
            for i in range(3):
                ranges_1.append(self.lidar.read())

            ranges_2 = []
            max_range = max(ranges_1)

            for i in range(len(ranges_1)):
                # Having a problem of spill over from highly reflective targets.
                # They show up as short distances.
                # Keep values that are close to each other.
                if ranges_1[i] / max_range > .90:
                    ranges_2.append(ranges_1[i])

            range_avg = sum(ranges_2) / len(ranges_2)

            range_avg = int(range_avg * 10)
            range_avg = float(range_avg) / 10.0

            # Place angle and range_avg in respective lists
            angles.append(current_angle)
            ranges.append(range_avg)

            # Increment current angle
            current_angle += step

        return angles, ranges


if __name__ == "__main__":
    range_bot = Radar(3)
    logger.info('Radar main initialized Radar')

    # while True:
    #     pdb.set_trace()
    #     range_bot.execute_hunt(target_range, target_width)

    print("Bye!")
