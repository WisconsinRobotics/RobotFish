from gpiozero import Servo
import RPi.GPIO as GPIO
from time import sleep

servo = Servo(2)
servoa = Servo(3)

try:
        while True:
            servo.mid()
            servoa.mid()
            
            sleep(0.5)
            
            servo.max()
            servoa.max()
            
            sleep(0.5)
except KeyboardInterrupt:
    print("Program stopped")