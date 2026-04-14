from gpiozero import AngularServo
from gpiozero.pins.lgpio import LGPIOFactory # Reduces jitter
import asyncio

# BAD BAD FIX THIS BAD

from config import CENTER_ANGLE, SERVO_MOUTH_PIN

factory = LGPIOFactory()

servo = AngularServo(
    SERVO_MOUTH_PIN,
    min_angle=-90,
    max_angle=90,
    pin_factory=factory
)
servo.angle = CENTER_ANGLE

MOUTH_CLOSED_ANGLE = -90
MOUTH_OPEN_ANGLE = 90
MOUTH_STEP_SECONDS = 5

async def main():
    try:
        while True:
            servo.angle = MOUTH_CLOSED_ANGLE
            await asyncio.sleep(MOUTH_STEP_SECONDS)

            servo.angle = MOUTH_OPEN_ANGLE
            await asyncio.sleep(MOUTH_STEP_SECONDS)
    finally:
        # Return to center and release servo on shutdown.
        servo.angle = CENTER_ANGLE
        servo.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass