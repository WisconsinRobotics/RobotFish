from gpiozero import AngularServo
from gpiozero.pins.lgpio import LGPIOFactory # Reduces jitter
from .config import *
from time import sleep

factory = LGPIOFactory()

servo = AngularServo(
    SERVO_HEAD_PIN,
    min_angle=-90,
    max_angle=90,
    pin_factory=factory
)
servo.angle = CENTER_ANGLE

def camera_adjust(x_center, frame_width, target_x=None):
    """
    Move servo to point at the specified target x-coordinate. Called by facerecognitionCam.py.

    Args:
        x_center: X pixel location of the tracked face center, or -1 when no face.
        frame_width: Width of the video.
        target_x: Target x coordinate to point at. Defaults to center if None.

    Returns:
        The new servo value in range [-90, 90].
    """
    if x_center == -1 or frame_width <= 0:
        servo.angle = 0  # No face detected or invalid frame width. Return to neutral position.
        sleep(0.5)
        return 0.0

    if target_x is None:
        target_x = frame_width / 2.0
    
    # Calculate error and scale to servo range
    error = (x_center - target_x)  # Distance from target in pixels
    max_error = (frame_width / 2.0) / SERVO_SENSITIVITY  # Scale factor for full range
    
    # Map error to angle range [-90, 90]
    angle_offset = (error / max_error) * 90.0
    new_angle = angle_offset
    sleep(0.5)
    new_angle = max(-90, min(90, new_angle))
    servo.angle = new_angle
    sleep(0.5)
    return new_angle
