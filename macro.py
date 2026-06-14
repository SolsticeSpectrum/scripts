from pynput import keyboard, mouse
import time
import threading

# Global variables to track the state and recorded inputs
record_inputs = False
replay_inputs = False
input_events = []
output_file = "recorded_inputs.txt"
replay_thread = None

# Function to record input events
def record_input(event):
    global record_inputs, input_events
    if record_inputs:
        input_events.append(event)

# Function to replay input events
def replay_input():
    global replay_inputs, input_events
    if replay_inputs:
        with open(output_file, "w") as file:
            for event in input_events:
                if isinstance(event, keyboard.KeyboardEvent):
                    file.write(f"Keyboard: {event.name}\n")
                elif isinstance(event, mouse.MouseEvent):
                    file.write(f"Mouse: {event}\n")

# Function to start recording
def start_recording():
    global record_inputs
    record_inputs = True

# Function to stop recording
def stop_recording():
    global record_inputs
    record_inputs = False

# Function to start replaying
def start_replay():
    global replay_inputs, replay_thread
    if replay_thread is None or not replay_thread.is_alive():
        replay_inputs = True
        replay_thread = threading.Thread(target=replay_input)
        replay_thread.start()

# Function to stop replaying
def stop_replay():
    global replay_inputs
    replay_inputs = False

# Function to clear recorded inputs
def clear_recorded_inputs():
    global input_events
    input_events = []

# Function to handle key presses
def on_key_press(key):
    if key == keyboard.Key.esc:
        return False
    elif key == keyboard.Key.f1:
        start_recording()
    elif key == keyboard.Key.f2:
        stop_recording()
    elif key == keyboard.Key.f3:
        start_replay()
    elif key == keyboard.Key.f4:
        stop_replay()
    elif key == keyboard.Key.f5:
        clear_recorded_inputs()

# Function to listen for keyboard events
def keyboard_listener():
    with keyboard.Listener(on_press=on_key_press) as listener:
        listener.join()

# Function to listen for mouse events
def mouse_listener():
    with mouse.Listener(on_click=record_input) as listener:
        listener.join()

# Start the listeners in separate threads
keyboard_thread = threading.Thread(target=keyboard_listener)
mouse_thread = threading.Thread(target=mouse_listener)

keyboard_thread.start()
mouse_thread.start()

keyboard_thread.join()
mouse_thread.join()
