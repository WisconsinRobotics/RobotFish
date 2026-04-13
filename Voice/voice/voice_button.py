from .config import BUTTON_PIN
from gpiozero import Button

button = Button(BUTTON_PIN)

def button_pressed():
  """
  Returns true if the button is pressed.
  """
  if button.is_pressed:
      #start recording for voice
      
    
      return True
  else:
      return False
  
def on_button_press(recording):
    """called when the button is pressed"""
    if(button.is_pressed):
        recording = not recording
        if recording:
            print("started recording")
        else:
            print("stopped recording")

# For testing
# try:
#     while True:
#         print(button_pressed(button))
# finally:
#     button.close()