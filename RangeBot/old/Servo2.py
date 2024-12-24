import time
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio

class Servo:
    """Servo class for controlling a servo motor using Adafruit PCA9685 library.

    Attributes:
        channel (int): PCA9685 channel for the servo.
        pwm (PCA9685): Instance of the PCA9685 class to control the servo.
    """

    SERVO_MIN = 1000  # Minimum pulse width in microseconds
    SERVO_MAX = 2000  # Maximum pulse width in microseconds
    ANGLE_MIN = -90   # Minimum angle in degrees
    ANGLE_MAX = 90    # Maximum angle in degrees

    def __init__(self, channel: int, address: int = 0x40):
        """Initialize the Servo class with a specified PCA9685 channel and I2C address.

        Args:
            channel (int): The channel number (0-15) on the PCA9685.
            address (int, optional): I2C address of the PCA9685. Defaults to 0x40.
        """
        i2c = busio.I2C(SCL, SDA)
        self.pwm = PCA9685(i2c, address=address)
        self.pwm.frequency = 60  # Set frequency to 60 Hz, suitable for servos.

        self.channel = channel
        self.servo_min = Servo.SERVO_MIN
        print(self.servo_min)
        self.servo_max = Servo.SERVO_MAX
        print(self.servo_max)
        self.angle_min = Servo.ANGLE_MIN
        print(self.angle_min)
        self.angle_max = Servo.ANGLE_MAX
        print(self.angle_max)
        self.angle = None

    def get_angle(self) -> int:
        """Retrieve the current angle of the servo.

        Returns:
            int: The current angle of the servo in degrees.
        """
        return self.angle

    def set_angle(self, angle: int) -> int:
        """Set the servo to the specified angle.

        Args:
            angle (int): Desired angle in degrees (-90 to 90).

        Returns:
            int: The angle set after clamping.
        """
        if angle < self.angle_min:
            angle = self.angle_min
        if angle > self.angle_max:
            angle = self.angle_max

        # Calculate pulse width based on angle
        pulse_width = int((angle - self.angle_min) * (self.servo_max - self.servo_min) / (self.angle_max - self.angle_min) + self.servo_min)

        # Set the pulse width on the PCA9685
        self.pwm.channels[self.channel].duty_cycle = pulse_width #* 16  # Convert to 16-bit value

        self.angle = angle
        return angle

    def exec(self):
        # Example usage: Set the servo to 45 degrees
        #self.set_angle(-90)
        #self.set_angle(-45)
        self.set_angle(0)
        #self.set_angle(45)
        #self.set_angle(90)
        pass

if __name__ == "__main__":
    servo = Servo(channel=3, address=0x40)
    servo.exec()
