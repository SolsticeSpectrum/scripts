##########################################################################################
#  This script helps to get access token for Minecraft directly from Mojang auth server  #
#      It's helpful when you want to develop mods and have runClient in online mode      #
##########################################################################################

import requests
import json
import os

# Cross-platform clear solution to get rid of text in terminal or command line
os.system('cls' if os.name == 'nt' else 'clear')

# Asks for Minecraft credentials
email = input("Please enter your Minecraft email: ")
password = input("Please enter your Minecraft password: ")

os.system('cls' if os.name == 'nt' else 'clear')

# If email and password is not entered, returns with an error
if email !="" and password !="":

    # Gets the response from mojang auth server and converts it into json dictionary
    post_data = '{"agent":{"name":"Minecraft","version":1},"username":"' + email + '","password":"' + password + '"}'
    response = requests.post('https://authserver.mojang.com/authenticate', data=post_data)
    dict_json = response.json()
    
    # Checks if there is accessToken in the response, else returns with an error
    if "accessToken" in dict_json:
        print("This is your access token for today:\n\n" + dict_json["accessToken"])
    else:
        print("There was an error when trying to get the access token...")
        print("Please check if your credentials are correct or contact me on github!")
        print("https://github.com/DarkReaper231")
    
else:
    print("The credentials cannot be empty!")