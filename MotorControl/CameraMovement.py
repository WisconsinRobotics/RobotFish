try:
    from gpiozero import Servo
except Exception:
    Servo = None

from time import sleep

try:
    from gpiozero.pins.pigpio import PiGPIOFactory
except Exception:
    PiGPIOFactory = None


class _DummyServo:
    """Fallback servo used on non-RPi/dev machines."""

    def __init__(self):
        self.value = 0.0


# This code controls the servo motor for the pi camera.
if Servo is None:
    servo = _DummyServo()
else:
    # use GPIO pin 13 for the servo
    servo_kwargs = {
        "min_pulse_width": 0.0005,
        "max_pulse_width": 0.0025,
    }
    if PiGPIOFactory is not None:
        servo_kwargs["pin_factory"] = PiGPIOFactory()
    servo = Servo(13, **servo_kwargs)
    servo.value = 0.0

# Proportional steering gain for smoother tracking.
TRACKING_GAIN = 0.25


def camera_adjust(x_center, frame_width):
    """Adjust pan servo from a detected face x-coordinate.

    Args:
        x_center: X pixel location of the tracked face center, or -1 when no face.
        frame_width: Width of the current video frame in pixels.

    Returns:
        The new servo value in range [-1.0, 1.0].
    """
    if x_center == -1 or frame_width <= 0:
        return servo.value

    frame_center = frame_width / 2.0
    error = (x_center - frame_center) / frame_center
    new_value = (servo.value or 0.0) + (error * TRACKING_GAIN)
    new_value = max(-1.0, min(1.0, new_value))
    servo.value = new_value
    return new_value

if __name__ == "__main__":
    servo_sweep_test()