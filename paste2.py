import time
import pyautogui

def paste_string():
    # Wait for 5 seconds before typing the string
    time.sleep(5)

    # The string to type out
    clipboard_string2 = 'Z2QOGiCtxe7qaSpBmz3VD0Bt1gzXPRcaAs1aDtAN2UycQJujAdrXO8TXWSYQcSBq'
    clipboard_string = 'Nu5QjjcnPisHawENYkfQjb42HW2VFRTvsWuNroxyx3iJo7kqsgztt33arQE5yV4J'
    # Swap 'y' and 'z' in the string
    clipboard_string = clipboard_string.replace('y', 'temp').replace('z', 'y').replace('temp', 'z')
    clipboard_string = clipboard_string.replace('Y', 'temp').replace('Z', 'Y').replace('temp', 'Z')

    # Type out the string automatically
    pyautogui.typewrite(clipboard_string)

if __name__ == "__main__":
    print("Switch to the VMware window. The script will type the string automatically in 5 seconds.")
    paste_string()
