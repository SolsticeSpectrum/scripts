import random
from pystray import Icon, Menu, MenuItem, WindowsBackend

# Function to generate a random number and update the icon
def update_icon(icon, item):
    random_number = str(random.randint(1, 100))
    icon.update_menu(create_menu(random_number))
    icon.update_icon(data=create_icon_data())

# Function to create the icon data with a white background
def create_icon_data():
    icon_size = 16
    icon_data = b'\x00' * (icon_size * icon_size * 4)
    return icon_data

# Function to create the menu with a single item
def create_menu(number):
    return Menu(MenuItem(f'Number: {number}', update_icon))

# Create the icon using the Windows backend (Polybar often uses the XEmbed protocol on Linux)
icon = Icon("name", create_icon_data(), menu=create_menu(""))

# Run the icon in the system tray
icon.run(backend=WindowsBackend())
