import os

ENABLED_FILE = "enabled_k"

def remap_tab_to_mouse():
    os.system("setxkbmap -layout us,cz -option grp:alt_shift_toggle")
    print("Enabled")
    with open(ENABLED_FILE, 'w'):
        pass

def revert_tab_to_default():
    os.system("setxkbmap -layout cz,us -option grp:alt_shift_toggle")
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
