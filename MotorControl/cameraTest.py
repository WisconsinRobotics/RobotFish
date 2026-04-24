from gpiozero import Servo
from time import sleep

servo = Servo(13)

try:
    while True:
        servo.mid()
        sleep(10)

except:
    print("something went wrong")