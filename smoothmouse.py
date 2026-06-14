import pyautogui
import math
import time

# Define the duration of the movement in seconds
duration = 2.0  # You can adjust this as needed

# Define custom easing functions (e.g., ease-in and ease-out)
def ease_in_out_quad(t):
    return t * t if t < 0.5 else 1 - (1 - t) * (1 - t)

# Get the screen dimensions
screen_width, screen_height = pyautogui.size()

# Calculate the number of steps based on the duration and desired smoothness
num_steps = int(duration * 60)  # 60 FPS

# Perform smooth mouse movement
for step in range(num_steps):
    t = step / num_steps
    ease_t = ease_in_out_quad(t)
    
    # Calculate the target position using smooth curves
    x = int(screen_width * ease_t)
    y = int(screen_height * ease_t)
    
    # Move the mouse to the target position
    pyautogui.moveTo(x, y, duration=0.0)  # Adjust the duration to control speed
    
    # Sleep briefly to control the frame rate
    time.sleep(1 / 60)  # 60 FPS

# Move the mouse to the final position (optional)
pyautogui.moveTo(screen_width, screen_height)

# You can add other actions or logic after the mouse movement
# For example, click or perform other tasks

# To test the script, run it in a terminal
