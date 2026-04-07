from config import BUTTON_PIN
from gpiozero import Button

button = Button(BUTTON_PIN)

def button_pressed(button):
  """
  Returns true if the button is pressed.
  """
  if button.is_pressed:
      return True
  else:
      return False

# For testing
# try:
#     while True:
#         print(button_pressed(button))
# finally:
#     button.close()