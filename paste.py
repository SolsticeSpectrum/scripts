from pynput import keyboard as kbd
from pynput.keyboard import Key, Controller
import pyperclip

keyboard = Controller()

def paste_string():
    # Get the string from the clipboard
    #clipboard_string = pyperclip.paste()

    # Create a keyboard listener
    with kbd.Listener(on_press=on_press) as listener:
        listener.join()

def on_press(key):
    # Press F10 to trigger the paste
    clipboard_string = "Nu5QjjcnPisHawENYkfQjb42HW2VFRTvsWuNroxyx3iJo7kqsgztt33arQE5yV4J"
    if key == Key.f11:
        for char in clipboard_string:
            keyboard.press(char)
            keyboard.release(char)

if __name__ == "__main__":
    paste_string()
