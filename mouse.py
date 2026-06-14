import os

ENABLED_FILE = "enabled_m"

def remap_tab_to_mouse():
    os.system("xkbset m")
    os.system("xmodmap -e 'keycode 23 = Pointer_Button1'")
    print("Enabled")
    with open(ENABLED_FILE, 'w'):
        pass

def revert_tab_to_default():
    os.system("xmodmap -e 'keycode 23 = Tab'")
    os.system("xkbset -m")
    print("Disabled")
    if os.path.exists(ENABLED_FILE):
        os.remove(ENABLED_FILE)

def main():
    if not os.path.exists(ENABLED_FILE):
        remap_tab_to_mouse()
    else:
        revert_tab_to_default()

if __name__ == "__main__":
    main()
