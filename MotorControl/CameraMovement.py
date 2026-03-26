from gpiozero import Servo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory
from config import *

# use GPIO pin 13 for the servo
servo_kwargs = {
    "min_pulse_width": 0.0005,
    "max_pulse_width": 0.0025,
}
if PiGPIOFactory is not None:
    servo_kwargs["pin_factory"] = PiGPIOFactory()
servo = Servo(SERVO_HEAD_PIN, **servo_kwargs)
servo.value = 0.0

# Proportional steering gain for smoother tracking.
TRACKING_GAIN = 0.25

def camera_adjust(x_center, frame_width, target_x=None):
    """
    Move servo to point at the specified target x-coordinate. Called by facerecognitionCam.py.

    Args:
        x_center: X pixel location of the tracked face center, or -1 when no face.
        frame_width: Width of the video.
        target_x: Target x coordinate to point at. Defaults to center if None.

    Returns:
        The new servo value in range [-1.0, 1.0].
    """
    if x_center == -1 or frame_width <= 0:
        return servo.value

    if target_x is None:
        target_x = frame_width / 2.0
    
    error = (x_center - target_x) / frame_width
    new_value = (servo.value or 0.0) + (error * TRACKING_GAIN)
    new_value = max(-1.0, min(1.0, new_value))
    servo.value = new_value
    return new_value
