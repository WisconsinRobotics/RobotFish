from config import BUTTON_PIN
from gpiozero import Button

button = Button(BUTTON_PIN)

def button_changed(button):
    if button.is_pressed:
        print("Button pressed.")

try:
    while True:
        button_changed(button)
finally:
    button.close()