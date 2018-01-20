#!usr/bin/python

from LidarLiteChild import LidarLiteChild


class RangeBot():

    """ RangeBot uses a servo and Lidar to find a target.
    The software looks for an object that is at closer
    distance and also in the middle of the scan.

    Ultimately, this class has the azimuth and range of
    the target."""

    def __init__(self):
        pass

    def scan(self, _minAngle, _maxAngle, _step):
        """ The scan method uses the servo and Lidar to
        return a list of angle and range pairs."""

        return [ [-20, 5.], [0, 3.], [20, 5] ]

    def find_target(self, _range_list):
        """ The find_target method takes as input a list of
        angle and range pairs.  It searches the list for the 
        smallest range."""

        return [0.0, 20.0]

    def exec(self, _minAngle, _maxAngle, _step):
        list = scan(self, _minAngle, _maxAngle, _step)
        targetLocation = find_target(list)
        return targetLocation
