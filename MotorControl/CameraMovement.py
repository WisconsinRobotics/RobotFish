from gpiozero import Servo
#from gpiozero.pins.pigpio import PiGPIOFactory
#import RPi.GPIO as GPIO
from time import sleep

import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
# ensure project root is importable and preferred
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import importlib.util
try:
    import Camera.non_usbcam as non_usbcam
except Exception:
    # fallback: load module directly from file path
    spec = importlib.util.spec_from_file_location(
        "non_usbcam", os.path.join(root_dir, "Camera", "non_usbcam.py")
    )
    non_usbcam = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(non_usbcam)
    except (ModuleNotFoundError, ImportError) as e:
        print(f"Warning: failed to import Camera.non_usbcam ({e}). using fallback stub.")
        import types
        non_usbcam = types.ModuleType("non_usbcam")
        def get_center():
            return -1
        non_usbcam.get_center = get_center


#this code controls the servo motor for the pi camera

# servo for camera motor
servo = Servo(13) #, pin_factory=PiGPIOFactory()) # use GPIO pin 13 for the servo
servo.value = 0  # motor range from -1 to 1
xcam_center = 4608/2  # this is an arbitrary number we will probably change later
total_pixel = 900


def camera_adjust(x):
    # face not found in the screen, reset the motor to zero
    if x == -1:
        servo.value = 0
    
    adjustment = x - xcam_center
    amount_move = adjustment / total_pixel
    servomove = servo.value + amount_move
    
    if servomove > 1.0:
        servomove = 1.0
    if servomove < 0.0:
        servomove = 0.0
    
    servo.value = servomove
    
camera_adjust(non_usbcam.get_centerx())