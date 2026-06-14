import time
import threading
import random
from pynput.keyboard import Listener, KeyCode
from pynput.mouse import Controller, Button

TOGGLE_KEY = KeyCode(char="x")

scrolling = False
mouse = Controller()

def scroller():
    while True:
        if scrolling:
            mouse.scroll(0, -3)
        time.sleep(0.016)

def toggle_event(key):
    if key == TOGGLE_KEY:
        global scrolling
        scrolling = not scrolling

scroll_thread = threading.Thread(target=scroller)
scroll_thread.start()

with Listener(on_press=toggle_event) as listener:
    listener.join()
