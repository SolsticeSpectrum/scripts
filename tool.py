from itertools import cycle
from colorama import init, Fore, Style
from concurrent.futures import ThreadPoolExecutor
import os
import pyfiglet
import datetime
import string
import random
import time
from pystyle import *
from pystyle import Add, Center, Anime, Colors, Colorate, Write, System
import urllib.request
import json
import pypresence
from discord_webhook import DiscordWebhook, DiscordEmbed
import win32console as wc
from pypresence import Presence
import requests
import threading
import ctypes
import sys
import discord
from discord.ext import commands


with open('config.json') as f:
    config = json.load(f)
username = config.get('user')
key = config.get('key')


def Spinner():
    l = ['|', '/', '-', '\\', ' ']
    for i in l+l+l:
        sys.stdout.write(f"""\r {i}""")
        sys.stdout.flush()
        time.sleep(0.1)


intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix="l", intents=intents)
client.remove_command("help")
i = 0
membercount = 0
version = 1


def log_msg(message):
    try:
        requests.post('http://127.0.0.1:25575/log', json={'log': message})
    except:
        pass


def log(message):
    threading.Thread(target=log_msg, args=(message,)).start()


client_id = '1122608936646881430'
RPC = Presence(client_id)
RPC.connect()
start_time = time.time()

banner_ch = """


                                        __    _  _  ___  ____  __          ___   ___ 
                                       /__\  ( \( )/ __)( ___)(  )        / __) / __)
                                      /(__)\  )  (( (_-. )__)  )(__      ( (_-.( (_-.
                                     (__)(__)(_)\_)\___/(____)(____)  ()  \___/ \___/
                                         

                                                       1. Mass Ban




"""

banner = """


                                        __    _  _  ___  ____  __          ___   ___ 
                                       /__\  ( \( )/ __)( ___)(  )        / __) / __)
                                      /(__)\  )  (( (_-. )__)  )(__      ( (_-.( (_-.
                                     (__)(__)(_)\_)\___/(____)(____)  ()  \___/ \___/


                                                  Made by ~ Kwertzyy


                                           

"""


def txt():

    login = f"Angel Multi Tool ~ Version: v{version} ~ Made by ! Kwertzyy"

    text = ""

    for character in login:

        ctypes.windll.kernel32.SetConsoleTitleW(text)

        text += character

        time.sleep(0.050)

    ctypes.windll.kernel32.SetConsoleTitleW(login)


cls = os.system("cls")


def txt_print(login):

    text = ""

    for character in login:

        sys.stdout.write(character)

        time.sleep(0.025)


def Menu():
    os.system("cls")


txt()
RPC.update(state=f"Logged as: {username}", details=f"In menu...", large_image="big", large_text=".gg/angelgg",
           start=start_time, buttons=[{"label": "Join on our support", "url": "https://discord.gg/3VbnYQkzEj"}])
Write.Print(f"{banner_ch}", Colors.blue_to_white, interval=0.000)
choice = Write.Input(f"root@{username}: ",
                     Colors.blue_to_white, interval=0.000)

if choice == "1" or "01":
    Spinner()
    os.system("cls")
    RPC.update(state=f"Logged as: {username}", details=f"Preparing for mass ban...", large_image="big", large_text=".gg/angelgg",
               start=start_time, buttons=[{"label": "Join on our support", "url": "https://discord.gg/3VbnYQkzEj"}])
    Write.Print(f"{banner}", Colors.blue_to_white, interval=0.000)
    token = Write.Input("> Token: ", Colors.blue_to_white, interval=0.000)
    os.system("cls")
    os.system("cls")
    os.system("cls")
    Spinner()
    os.system("cls")
    os.system("cls")
    os.system("cls")
    headers = {'Authorization': f'Bot {token}'}


@client.event
async def on_ready():
    await guild()


async def menuban():
    guild = guildid
    txt = open('member_id.txt')
    for member in txt:
        threading.Thread(target=massban, args=(guild, member,)).start()
    txt.close()
    time.sleep(4)


def massban(guild, member):
    global i, membercount
    while True:
        ban_time = time.time()
        r = requests.put(
            f"https://discord.com/api/v8/guilds/{guild}/bans/{member}", headers=headers)
        if 'retry_after' in r.text:
            time.sleep(r.json()['retry_after'])
        else:
            if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                log(f"[ {Fore.GREEN}✔  {Fore.RESET}] User was banned")
                print(f"All users were banned in {ban_time}ms")
                break
            else:
                break


async def main():
    if len(sys.argv) < 2:
        sys.stdout.write(f'''
    
    [ {Fore.RED}❗ {Fore.RESET}] Connected as ~ {client.user} (BOT)
    [ {Fore.RED}❗ {Fore.RESET}] Guild ~ {guildid}
    [ {Fore.RED}❗ {Fore.RESET}] Connection ~ Logitech Gamepad for Submarine Titan

    ''')

    option = input("[ > ] Start (y/n): ")
    if option == 'y':
        os.system("cls")
        await menuban()

    if option == 'n':
        Menu()

    elif option is None:
        await main()


async def guild():
    global membercount, guildid
    os.system("cls")
    Write.Print(f"{banner}", Colors.blue_to_white, interval=0.000)
    guildid = int(input(''' 
 > Server ID: '''))
    os.system("cls")
    await client.wait_until_ready()
    ob = client.get_guild(guildid)
    members = await ob.chunk()
    os.remove("member_id.txt")

    with open('member_id.txt', 'a') as txt:
        for member in members:
            txt.write(str(member.id) + "\n")
            membercount += 1
        if membercount == 1:
            print(f''' 
 [ {Fore.GREEN}✔  {Fore.RESET}] ~ Scraped {membercount} members!''')
        else:
            print(f''' 
 [ {Fore.GREEN}✔  {Fore.RESET}] ~ Scraped {membercount} members!''')
        txt.close()
        time.sleep(1)
        await main()


def check():
    try:
        client.run(token)
    except:
        print('''
 [ ✖️ ] Invalid Token''')
        time.sleep(2)
        Menu()


check()
