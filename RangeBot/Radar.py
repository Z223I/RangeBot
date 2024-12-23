#!/usr/bin/env python3

import sys
import time
import math
import logging
import random
import matplotlib.pyplot as plt
from typing import List, Tuple

# Attempt to import required modules
try:
    from LidarLite3Ext import LidarLite3Ext
except ImportError:
    LidarLite3Ext = None

try:
    from Servo import Servo
except ImportError:
    Servo = None

# Configure logging
logger = logging.getLogger(__name__)
hdlr = logging.FileHandler('Radar.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)

class Radar:
    """
    Radar class combines a servo and LidarLite sensor to perform a scanning operation.
    It detects objects by measuring distances at different angles.

    Attributes:
        INCHES_PER_FOOT (int): Constant for unit conversion.
        servo (Servo): Servo object to control angular movement.
        lidar (LidarLite3Ext): Lidar object for distance measurement.
        lidar_initialized (bool): Indicates if the LidarLite sensor was initialized successfully.
    """

    INCHES_PER_FOOT = 12

    def __init__(self, servo_channel: int):
        """
        Initialize the Radar object with a servo and LidarLite sensor.

        Args:
            servo_channel (int): The servo channel to control the servo motor.
        """
        if Servo:
            self.servo = Servo(servo_channel)
        else:
            self.servo = None
            logger.warning("Servo module not available. Servo functionality will be disabled.")

        if LidarLite3Ext:
            self.lidar = LidarLite3Ext()
            self.lidar_initialized = self.lidar.init()
            if not self.lidar_initialized:
                logger.error("Lidar failed to initialize.")
                print("ERROR: Lidar failed to initialize.")
        else:
            self.lidar = None
            self.lidar_initialized = False
            logger.warning("LidarLite3Ext module not available. Lidar functionality will be disabled.")

    def scan(self, min_angle: float = -90.0, max_angle: float = 90.0, step: float = 10.0) -> Tuple[List[float], List[float]]:
        """
        Perform a scan by sweeping the servo through a range of angles and measuring distances.

        Args:
            min_angle (float): The starting angle of the scan in degrees. Defaults to -90.0.
            max_angle (float): The ending angle of the scan in degrees. Defaults to 90.0.
            step (float): The step size for the angle increments. Defaults to 10.0.

        Returns:
            Tuple[List[float], List[float]]: A tuple containing two lists - angles and their corresponding distances.
        """
        angles = []
        ranges = []
        current_angle = min_angle

        while current_angle <= max_angle:
            if self.servo:
                self.servo.set_angle(current_angle)
            else:
                logger.warning("Servo functionality is disabled. Skipping angle movement.")

            # Allow servo to finish moving
            time.sleep(1 if current_angle == min_angle else 0.1)

            if self.lidar_initialized:
                # Take multiple lidar readings to improve reliability
                readings = [self.lidar.read() for _ in range(3)]
                valid_readings = [r for r in readings if r / max(readings) > 0.9]

                if valid_readings:
                    range_avg = sum(valid_readings) / len(valid_readings)
                    range_avg = round(range_avg, 1)
                else:
                    range_avg = float('inf')  # Assign infinity if no valid readings
            else:
                range_avg = random.uniform(1, 10)  # Generate random distances if lidar is not initialized
                time.sleep(1)  # Sleep for 1 second when generating random distances

            angles.append(math.radians(current_angle))  # Convert angles to radians for polar plot
            ranges.append(range_avg)

            current_angle += step

        return angles, ranges

    def plot_scan(self, angles: List[float], ranges: List[float]):
        """
        Plot the scan results as a polar plot.

        Args:
            angles (List[float]): List of angles in radians.
            ranges (List[float]): List of corresponding distances.
        """
        plt.figure()
        ax = plt.subplot(111, polar=True)
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)

        ax.plot(angles, ranges, marker='o')
        ax.set_title("Radar Scan", va='bottom')

        plt.show()
        plt.close()

    def exec(self):
        """
        Execute the radar scanning process, continuously scanning and displaying results.
        """
        try:
            logger.info('Radar initialized successfully.')

            while True:
                angles, ranges = self.scan()
                for angle, distance in zip(angles, ranges):
                    print(f"Angle: {math.degrees(angle):.1f}°, Distance: {distance:.1f} units")

                print("--- Scan Complete ---")

                # Plot the scan results
                self.plot_scan(angles, ranges)

        except KeyboardInterrupt:
            print("\nScanning interrupted by user. Exiting...")
            logger.info('Radar scanning interrupted by user.')

if __name__ == "__main__":
    radar = Radar(servo_channel=3)
    radar.exec()
