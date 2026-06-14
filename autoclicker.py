import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode

TOGGLE_KEY = KeyCode(char="s")
clicking = False
mouse = Controller()

def clicker():
    while True:
        if clicking:
            mouse.click(Button.left, 1)
        time.sleep(1.1)

def toggle_event(key):
    if key == TOGGLE_KEY:
        global clicking
        clicking = not clicking

click_thread = threading.Thread(target=clicker)
click_thread.start()

with Listener(on_press=toggle_event) as listener:
    listener.join()
