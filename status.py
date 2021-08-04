import psutil
import socket
import subprocess
import os
import platform
from gpiozero import CPUTemperature
import datetime
import time

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def loop():
    clear = lambda: os.system('clear')
    t = datetime.datetime.now()
    cpu = CPUTemperature()
    net_io = psutil.net_io_counters()
    disk = psutil.disk_usage('/')
    command = "ps aux | wc -l"
    ret = subprocess.run(command, capture_output=True, shell=True)

    clear()
    print(f"raspberrypi : {t.day:02d}-{t.month:02d}-{t.year} {t.hour:02d}:{t.minute:02d}:{t.second:02d}")
    print(f"")
    print(f"CPU Usage: {psutil.cpu_percent(percpu=False, interval=1)}% Temp: {cpu.temperature}")
    print(f"Memory Free: {get_size(psutil.virtual_memory().free)}  Used: {get_size(psutil.virtual_memory().used)}")
    print(f"IP Address: {get_ip()}")
    print(f"Bytes Sent: {get_size(net_io.bytes_sent)}  Recieved: {get_size(net_io.bytes_recv)}")
    print(f"Disk Used: {get_size(disk.used)}  Free: {get_size(disk.free)}")
    print(f"Processes Running: {ret.stdout.decode()}")

while True:
    loop()
    time.sleep(600)
