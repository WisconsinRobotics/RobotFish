from gpiozero import Servo
#from gpiozero.pins.pigpio import PiGPIOFactory
import RPi.GPIO as GPIO
from time import sleep
#this code controls the servo motor for the pi camera

# servo for camera motor
servo = Servo(17)
servo.value = 0  # motor range from -1 to 1
xcam_center = 450  # this is an arbitrary number we will probably change later
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