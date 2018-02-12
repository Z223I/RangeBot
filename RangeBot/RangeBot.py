#!usr/bin/python

import sys
sys.path.append("/home/pi/pythondev/LidarLite3Ext/LidarLite3Ext")
# print(sys.path)

from LidarLite3Ext import LidarLite3Ext
from Servo import Servo
import time
import math

#import pdb
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RangeBot():

    """ RangeBot uses a servo and Lidar to find a target.
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

        # This is the default clip distance.
        self.clip_distance = 6

        # desired hits on target
        self.DESIRED_HITS = 7

        self.NARROW_SCAN_DISTANCE = 2
        self.NARROW_SCAN = 1.0
        self.NORMAL_SCAN = 3.0




    def set_clip_distance(self, distance):
        self.clip_distance = distance


    def scan(self, min_angle, max_angle, step):
        """ The scan2 method uses the servo and Lidar to return a list of
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

#        pdb.set_trace()
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

    def scan2(self, est_tgt_r, min_angle, max_angle, step):
        """ The scan2 method uses the servo and Lidar to return a list of
        angle and range pairs.

        Scan2 is different from scan in that it attempts to remove shorter
        distances that are spill over from the previous scan of the Lidar
        Lite v3.

        @type: float
        @param: est_tgt_r

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

#        pdb.set_trace()
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
                current_range = 0
                # This is dealing with the Lidar Lite spill over.
                while current_range < .90 * est_tgt_r:
                    current_range = self.lidar.read()

                ranges_1.append(current_range)



            ranges_2 = []
            max_range = max(ranges_1)

            for i in range(len(ranges_1)):
                # Having a problem of spill over from highly reflective targets.
                # They show up as short distances.
                # Keep values that are 90 percent of the expect range or
                # higher.
                if ranges_1[i] / max_range > .90:
                    ranges_2.append(ranges_1[i])

            range_avg = sum(ranges_2) / len(ranges_2)
            range_avg = '{:.2f}'.format(range_avg)
            range_avg = float(range_avg)

            # Place angle and range_avg in respective lists
            angles.append(current_angle)
            ranges.append(range_avg)

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

    def find_target2_helper(self, est_tgt_r, ranges):
        """find_target2_helper uses an estimated target range and a list of
        ranges to find the target.

        @type float
        @param est_tgt_r

        @type float list
        @param ranges

        @rtype float list
        @param clipped_ranges

        @rtype int
        @param hits"""

        minimum, index = min((ranges[i], i) for i in range(len(ranges)))

#        print(minimum)

        clipped_ranges = []
        target_marker = 1
        for i in range(len(ranges)):
            if ranges[i] < int(minimum) + int(self.clip_distance):
               clipped_ranges.append(target_marker)
            else:
               clipped_ranges.append(0)

        logger.debug('RangeBot.find_taget2_helper() Clipped ranges: ', \
            clipped_ranges)
        print(clipped_ranges)

        target_hits = clipped_ranges.count(target_marker)
#        print("Target hits: ", target_hits)

        return clipped_ranges, target_hits

    def find_target2(self, est_tgt_r, angles, ranges):
        """find_target2"""

#        print
#        print(ranges)

        clipped_ranges, target_hits = \
            self.find_target2_helper(est_tgt_r, ranges)



#
# TODO: Fix this algorithm.  It assumes consecutive 1's.
#


        target_center_index = None
        target_marker = 1
        if target_hits > 0:
            mid_target = int(target_hits / 2)

            # Find first target hit
            for i in range(len(ranges)):
                if clipped_ranges[i] == target_marker:
                    first_target_hit = i
                    break
            # end for
            # Calculate center of target
            target_center_index = first_target_hit + mid_target

        # end if





        if target_center_index > -1:
            return_angle = angles[target_center_index]
            return_range = ranges[target_center_index]
        else:
            return_angle = None
            return_range = None
        # end else

        print("Target angle and range: {:.2f}, {:.1f}".format(return_angle, return_range))
        return return_angle, return_range, target_hits


    def execute(self, min_angle, max_angle, step):
        """execute"""

        angles, ranges = self.scan(min_angle, max_angle, step)
#        print("Angles: ", angles)
#        print("Ranges: ", ranges)

        target_location = self.find_target(angles, ranges)
#        print("Target location: ", target_location

        target_angle, target_range, target_hits = self.find_target2(angles, ranges)

        return target_location

    def valid_hunt(self, est_tgt_r, target_width):
        """execute

        type: float
              est_tgt_r Estimated target range

        type: int
              target_width

        rtype: float list
               target_angle (deg)

        rtype: float list
               target_range (inches)

        rtype: int
               hits as a count
        """

#        print("RangeBot:execute_hunt(", est_tgt_r, ", ", target_width, ")")
        return False

    def scan_info(self, est_tgt_r, target_width):
        """scan_info uses target range and width to determine the scan angle
        to be used.

        @type: float
        @param: est_tgt_r Estimated target range

        @type: int
        @param: target_width

        @rtype: float
        @param: scan_half_angle (deg)

        @rtype: float
        @param: step_angle
        """

#        print("RangeBot:scan_info(", est_tgt_r, ", ", target_width, ")")


#        pdb.set_trace()
        if est_tgt_r < 2 * RangeBot.INCHES_PER_FOOT:
            # RangeBot is less than two feet from the target.  Cut the scan
            #angle down so the scan is faster and we are NOT manuevering at
            # this point anyways.  We only need to know when to stop.
            scan_width = self.NARROW_SCAN
        else:
            scan_width = self.NORMAL_SCAN

        angle_rads = math.atan(target_width / est_tgt_r)

        scan_rads = angle_rads * scan_width

        scan_angle = math.degrees(scan_rads)

        scan_half_angle = scan_angle / 2.0

        # Calculate the step angle.
        total_steps = self.DESIRED_HITS * scan_width
        step_angle = scan_angle / total_steps

        return scan_half_angle, step_angle






    def execute_hunt(self, est_tgt_r, target_width):
        """execute

        type: float
              est_tgt_r Estimated target range

        type: int
              target_width

        rtype: float list
               target_angle (deg)

        rtype: float list
               target_range (inches)

        rtype: int
               hits as a count
        """

#        print("RangeBot:execute_hunt(", est_tgt_r, ", ", target_width, ")")

        self.lidar.auto_configure(est_tgt_r)

        scan_half_angle, step_angle = \
            self.scan_info(est_tgt_r, target_width)

        angles, ranges = \
            self.scan2(est_tgt_r, -scan_half_angle, scan_half_angle, step_angle)








#        print(ranges)
        logger.debug('RangeBot.execute_hunt() ranges: ', ranges)

        target_angle, target_range, target_hits = \
            self.find_target2(est_tgt_r, angles, ranges)

        return target_angle, target_range, target_hits


if __name__ == "__main__":
    range_bot = RangeBot(3)

#    min_angle = -10
#    max_angle = 10
#    step = 1

#    target_location = range_bot.execute(min_angle, max_angle, step)
#    print(target_location)

    # The units of measurement do not matter.  We are getting a ratio to
    # calculate the atan.
    USE_INPUT = False

    if USE_INPUT:
        target_range = input("Target range: ")
        target_range = int(target_range)

        target_width = input("Target width: ")
        target_width = int(target_width)
    else:
        target_range = 30
        target_width = 3

    range_bot.execute_hunt(target_range, target_width)

    print("Bye!")
