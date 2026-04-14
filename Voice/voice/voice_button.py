from .config import BUTTON_PIN
from gpiozero import Button
import threading

button = Button(BUTTON_PIN)
input_ready = threading.Event()
user_input = ""

def on_button_pressed():
    """Simulate Enter key press"""
    global user_input
    user_input = ""  # Empty string signals button was pressed
    input_ready.set()

button.when_pressed = on_button_pressed

def get_input_or_button():
    """
    Wait for either user typed input OR button press
    
    Returns:
        str: User input, or empty string if button pressed
    """
    def input_thread():
        global user_input
        user_input = input("\nPress button to record, or type a command: ").strip().lower()
        input_ready.set()
    
    thread = threading.Thread(target=input_thread, daemon=True)
    thread.start()
    
    input_ready.wait()  # Block until either input or button
    input_ready.clear()
    return user_input

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