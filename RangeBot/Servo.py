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

    # Configure min and max servo pulse lengths
    SERVO_MIN = 130  # Min pulse length out of 4096
    SERVO_MAX = 630  # Max pulse length out of 4096

    # Establish constants for min and max angles.
    ANGLE_MIN = -90
    ANGLE_MAX = 90

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
        self.servo_max = Servo.SERVO_MAX
        self.angle_min = Servo.ANGLE_MIN
        self.angle_max = Servo.ANGLE_MAX
        self.angle = None

    def set_servo_pulse(self, pulse: int) -> None:
        """Set the pulse width for the servo motor.

        Args:
            pulse (int): The pulse width in microseconds.
        """
        pulse_length = 1000000  # 1,000,000 us per second
        pulse_length //= self.pwm.frequency  # 60 Hz
        pulse_length //= 4096  # 12 bits of resolution
        pulse = int(pulse * 1000 / pulse_length)
        self.pwm.channels[self.channel].duty_cycle = pulse

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

        total_degrees = self.angle_max - self.angle_min
        total_pulse = self.servo_max - self.servo_min
        pulse_per_degree = total_pulse / total_degrees
        pulse = int(self.servo_min + (pulse_per_degree * (angle - self.angle_min)))
        self.pwm.channels[self.channel].duty_cycle = pulse
        self.angle = angle
        return self.angle

    def test(self) -> None:
        """Test the servo by moving it between minimum and maximum pulse widths."""
        for _ in range(2):
            self.pwm.channels[self.channel].duty_cycle = self.servo_min
            time.sleep(1)
            self.pwm.channels[self.channel].duty_cycle = self.servo_max
            time.sleep(1)

    def test2(self) -> None:
        """Test the servo by moving it between minimum and maximum angles."""
        for _ in range(3):
            self.set_angle(self.angle_min)
            time.sleep(2)
            self.set_angle(self.angle_max)
            time.sleep(2)

    def center(self) -> None:
        """Center the servo to 0 degrees."""
        self.set_angle(0)

    def exec(self) -> None:
        """Execute servo tests in a loop until interrupted by the user."""
        print('Moving servo on channel 3, press Ctrl-C to quit...')
        self.center()

        try:
            while True:
                self.test()
                time.sleep(1.5)
                self.test2()
                time.sleep(3)
        except KeyboardInterrupt:
            print("Program terminated.")

if __name__ == "__main__":
    servo = Servo(channel=3, address=0x40)
    servo.exec()
