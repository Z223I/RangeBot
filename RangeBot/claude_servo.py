#!/usr/bin/env python3

import time
import board
import busio
from adafruit_pca9685 import PCA9685

class Servo:
    """
    A class to control a Hitec HS-422 servo motor using PCA9685 PWM controller.

    The HS-422 servo uses:
    - Pulse width range: 500-2500 microseconds
    - Operating speed: 0.21 sec/60° at 4.8V, 0.16 sec/60° at 6.0V
    - Operating angle: 180 degrees
    """

    # For HS-422:
    # 500µs = 0° = 125 (500µs / 4096 * 1000000µs/s / (1/50Hz))
    # 2500µs = 180° = 625 (2500µs / 4096 * 1000000µs/s / (1/50Hz))
    MIN_PULSE = 115  # Corresponds to 500µs
    MAX_PULSE = 542  # Corresponds to 2500µs
    FREQUENCY = 50   # Standard servo frequency of 50Hz

    def __init__(self, pca: PCA9685, channel: int):
        """
        Initialize the servo on a specific channel.

        Args:
            pca: PCA9685 instance
            channel: PWM channel number (0-15)
        """
        self.pca = pca
        self.channel = channel
        self.pca.frequency = self.FREQUENCY
        self.current_angle = 0

    def set_angle(self, angle: float):
        """
        Set the servo to a specific angle.

        Args:
            angle: Desired angle in degrees (0-180)
        """
        # Ensure angle is within bounds
        angle = max(0, min(180, angle))

        # Convert angle to pulse length
        pulse_length = int(
            self.MIN_PULSE + (self.MAX_PULSE - self.MIN_PULSE) * (angle / 180)
        )

        # Set PWM pulse
        self.pca.channels[self.channel].duty_cycle = pulse_length << 4
        self.current_angle = angle

    def exec(self, cycles: int = 1, delay: float = 0.02):
        """
        Exercise the servo through its full range of motion.

        Args:
            cycles: Number of full cycles to perform
            delay: Delay in seconds between angle adjustments
                  Default of 0.02s matches the HS-422's speed capabilities
        """
        for _ in range(cycles):
            # Sweep from 0 to 180
            for angle in range(0, 181, 1):
                self.set_angle(angle)
                time.sleep(delay)

            # Sweep from 180 to 0
            for angle in range(180, -1, -1):
                self.set_angle(angle)
                time.sleep(delay)

def main():
    """
    Main function to demonstrate servo control.
    """
    try:
        # Initialize I2C bus and PCA9685
        i2c = busio.I2C(board.SCL, board.SDA)
        pca = PCA9685(i2c)

        # Create a servo on channel 3
        servo = Servo(pca, 3)

        print("Starting servo demonstration...")

        # Center the servo
        print("Centering servo...")
        servo.set_angle(0)
        time.sleep(2)
        servo.set_angle(90)
        time.sleep(2)
        servo.set_angle(180)
        time.sleep(2)

        # Move to extremes
        print("Testing range of motion...")
        servo.set_angle(0)
        time.sleep(1)
        servo.set_angle(180)
        time.sleep(1)

        # Exercise the servo
        print("Exercising servo (2 cycles)...")
        #servo.exec(cycles=2)

        # Return to center position
        print("Returning to center...")
        servo.set_angle(90)
        time.sleep(1)

    except KeyboardInterrupt:
        print("\nProgram stopped by user")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up
        print("Cleaning up...")
        try:
            pca.deinit()
        except:
            pass

if __name__ == "__main__":
    main()
