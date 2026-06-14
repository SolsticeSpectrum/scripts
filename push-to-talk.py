#push to talk pro Firefox
from pynput import keyboard
import subprocess

AMIXER = "amixer"
MUTE = ["set", "Capture", "nocap"]
UNMUTE = ["set", "Capture", "cap"]

def on_press(key):
    global caps_lock_pressed
    if key == keyboard.Key.caps_lock:
        subprocess.run([AMIXER] + UNMUTE)

def on_release(key):
    global caps_lock_pressed
    if key == keyboard.Key.caps_lock:
        subprocess.run([AMIXER] + MUTE)

try:
    subprocess.run([AMIXER] + MUTE)
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
except KeyboardInterrupt:
    subprocess.run([AMIXER] + UNMUTE)
    print("Exiting nicely...")
