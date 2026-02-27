#!/usr/bin/env python3

from concurrent.futures import ThreadPoolExecutor
import argparse
import random
import signal
import os
import sys

try:
    from pwn import *
    from termcolor import colored
    import requests
    from rich.panel import Panel
    from rich.console import Console
    from scapy.all import ARP, Ether, srp
except:
    print("\n[-] Libraries cant't be imported\n")
    sys.exit(1)

console = Console()

NAME = f"""
 ▄   ▄▄▄▄                     ▄▄▄▄▄▄                                  
 ▀██████▀                    █▀██▀▀▀█▄                                
   ██   ▄ ▄    ▀▀ ▄            ██▄▄▄█▀                          ▄     
   ██  ██ ████▄██ ███▄███▄     ██▀▀█▄   ▄█▀█▄ ▄▀▀█▄ ████▄ ▄█▀█▄ ████▄ 
   ██  ██ ██   ██ ██ ██ ██   ▄ ██  ██   ██▄█▀ ▄█▀██ ██ ██ ██▄█▀ ██    
   ▀█████▄█▀  ▄██▄██ ██ ▀█   ▀██▀  ▀██▀▄▀█▄▄▄▄▀█▄██▄████▀▄▀█▄▄▄▄█▀    
   ▄   ██                                           ██                
   ▀████▀                                           ▀                 
                                                                      
"""

BANNERS = [
f"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢤⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⡾⠿⢿⡀⠀⠀⠀⠀⣠⣶⣿⣷⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣦⣴⣿⡋⠀⠀⠈⢳⡄⠀⢠⣾⣿⠁⠈⣿⡆⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⠿⠛⠉⠉⠁⠀⠀⠀⠹⡄⣿⣿⣿⠀⠀⢹⡇⠀⠀⠀
⠀⠀⠀⠀⠀⣠⣾⡿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⣰⣏⢻⣿⣿⡆⠀⠸⣿⠀⠀⠀
⠀⠀⠀⢀⣴⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣆⠹⣿⣷⠀⢘⣿⠀⠀⠀
  ⢀⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⠋⠉⠛⠂⠹⠿⣲⣿⣿⣧⠀⠀
⠀⢠⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣿⣿⣿⣷⣾⣿⡇⢀⠀⣼⣿⣿⣿⣧⠀
⠰⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⡘⢿⣿⣿⣿⠀
⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣷⡈⠿⢿⣿⡆
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠁⢙⠛⣿⣿⣿⣿⡟⠀⡿⠀⠀⢀⣿⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣶⣤⣉⣛⠻⠇⢠⣿⣾⣿⡄⢻⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣦⣤⣾⣿⣿⣿⣿⣆⠁

⠀⠀⠀⠀YOUR TIME HAS COME
""",

f"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⣤⣤⠴⠶⠶⠶⠶⠶⠶⠶⢤⣤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣴⠶⠞⠛⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠻⢶⣦⡤⢤⣤⣀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡴⠟⠋⣁⡤⠴⠶⠶⢦⣄⣀⣀⣀⣀⡀⠀⠀⢀⣀⡀⠀⠀⠀⠀⠀⠀⠀⢰⡟⠀⠀⠈⢻⡆⠀
⠀⠀⠀⠀⠀⠀⠀⣠⡶⢋⡥⠒⠛⠉⠙⠛⠓⠲⠦⢤⣀⠉⠻⢿⡟⢿⡛⠛⠛⠛⠿⠶⣦⣤⣀⡀⠀⢠⡿⠁⠀⡀⢠⣼⠇⠀
⠀⠀⠀⠀⠀⣠⠞⠁⣠⠎⢠⣶⣶⣶⠦⢤⣀⠀⠀⠀⠀⢭⡀⡀⠙⠂⠙⢄⠀⠀⠀⠀⠀⠀⠉⠙⠻⢿⣁⣀⣴⣷⣿⡏⠀⠀
⠀⠀⠀⣠⠞⢡⣿⡾⣿⠀⣾⠟⡋⠀⠀⠀⠙⢷⣦⣄⠀⠀⠙⢾⣆⠀⠀⠈⠳⡄⠀⠀⠀⠀⠀⠀⠀⢨⠋⠛⣿⣿⡟⠀⠀⠀
⠀⠀⡔⢁⣴⠟⠁⠀⡏⢸⣏⡎⠀⠀⠀⠀⠀⠀⢹⣻⣷⣦⣄⠀⠙⢧⠀⠀⠀⠙⣦⡀⠀⠀⠀⠀⢀⠇⠀⢠⣿⡏⠀⠀⠀⠀
⠀⠌⡠⠊⠀⠀⠀⠀⡇⣾⢻⠀⠀⠀⠀⠀⠀⣸⡿⠋⢁⣀⠈⠳⣄⠀⠑⡀⠀⠀⢸⣷⡀⠀⠀⠀⡎⠀⢀⣾⡟⠀⠀⠀⠀⠀
⡴⠊⠀⠀⠀⠀⠀⠀⠇⢹⢸⣷⣤⣤⣀⢀⣴⠏⢀⣴⠿⣿⣿⠀⣹⣦⠀⠈⢂⠀⠀⠙⣿⡄⠀⡜⠀⢠⣿⡿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢠⠘⡞⠁⠀⣀⢉⣹⣧⡤⠾⠿⠶⣿⡯⠞⢻⡟⣧⠀⢸⡄⠀⠀⡘⣿⡴⠁⢀⣾⡿⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢸⢨⣷⣼⣿⣿⡟⠉⣿⣷⡄⠀⢀⣀⡤⢤⡿⢁⣿⣇⢸⣧⠀⠃⢸⣿⠃⠀⣾⣿⠃⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢸⡀⣿⣾⡙⠛⠋⠠⣿⡟⠻⠓⠀⠈⣠⣾⡇⢸⣿⣿⠀⣿⠀⡏⢸⠇⠀⣼⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢸⣷⠸⣿⣿⣶⣆⡀⢀⣀⣀⣤⠴⢋⣟⡿⠁⢸⣿⣿⣾⡟⢀⣿⡞⢀⣼⣿⣧⣄⣀⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣧⠙⣿⣿⣿⣿⣭⡬⡤⣟⣿⢷⡿⢁⣴⣿⠟⣽⠋⠀⣸⡟⠀⢨⣿⣿⣿⣿⠟⠿⣦⡀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⡜⢷⣌⢻⣿⣏⠙⣿⠿⠛⠛⡿⠀⣾⡿⢋⡼⠇⠀⠀⡿⠁⢀⣾⣿⣿⠀⠘⡄⠀⠀⠙⢦⡀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣮⣙⠷⣝⠻⣿⣁⣠⣗⣒⣱⣾⡟⢡⠎⠀⡇⠀⢠⠁⢀⣾⡟⠾⡇⠀⠀⠈⠀⠀⠀⠀⠹⣆⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣩⣿⣿⣿⣯⡻⣿⣿⣿⣿⡟⢠⡿⠀⠀⣇⢀⠆⢀⣼⡿⠁⠀⠇⠀⠀⡀⠀⢰⠀⠀⠀⢻⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠟⠋⣿⢿⣿⣿⣿⣿⣍⠻⡿⢀⣿⡇⠀⢀⣿⡏⠀⢸⣿⠁⠀⠀⢀⠀⠀⢡⠀⠈⣆⠀⠀⢸⠀
⠀⠀⠀⠀⠀⠀⠀⣠⣾⠋⠁⠀⠀⡟⢸⠹⣏⣿⣘⣿⣶⡇⣸⣿⡅⠀⢸⡟⠀⢠⣿⠃⠀⡇⠀⠘⣇⠀⠈⡆⠀⣿⣆⣸⣿⡀
⠀⠀⠀⠀⠀⠀⣾⡿⢁⠀⡇⠀⠀⠇⠀⢀⣿⡿⠋⠙⠉⣷⣿⣿⣇⠀⡸⠀⣠⣿⢣⡇⠀⣷⠀⢀⣿⡀⠀⣿⡀⣿⣿⣿⡏⠀
⠀⠀⠀⠀⠀⢸⡿⠃⢸⠀⣧⠀⣠⠴⠺⠋⡽⠁⢀⡾⣟⠛⠭⠉⢯⣴⣇⣼⣿⣿⣿⣷⣼⣿⣦⣾⣿⣷⣠⣿⣷⣿⡷⢿⣷⠀
⠀⠀⠀⠀⠀⢸⠁⠀⡿⢰⣯⡴⠃⠀⠀⡼⠀⠀⣿⠁⠈⢧⡀⢶⣤⡿⢿⣿⣿⣿⣿⣿⢿⣿⣿⡏⣸⣿⣿⡟⠸⣿⡇⠀⠙⠀
⠀⠀⠀⠀⠀⣬⡄⣸⣷⠋⢹⠃⠀⡄⠀⡀⠀⣠⣿⣀⠀⣘⣽⡞⠉⣷⣄⣹⣿⣿⣿⡇⠈⢻⣿⡀⠙⣿⣿⣷⠀⢿⣿⢠⡆⠀
⠀⠀⠀⠀⠀⣿⢰⠟⠃⠀⡎⠀⢰⡇⠀⣄⢰⣿⣿⣿⠛⢻⣄⠱⣄⠈⢻⡟⢹⣿⣿⠿⡆⢈⣿⠃⢸⣿⣟⠁⢀⠀⠀⠈⠁⠀
⠀⠀⠀⠀⢰⣿⠏⢰⠁⢸⡀⠀⣾⣧⣴⣿⣿⡙⣿⣿⣆⠀⠙⢆⣨⣶⣫⠗⠻⣿⡏⠀⠃⠘⢻⡆⠀⢻⠏⠀⠘⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠸⠿⣦⣿⣄⣼⣷⣾⡏⠹⣿⢿⣯⢁⣹⣿⣿⣧⡠⢾⠧⠚⠀⠀⠀⠙⠃⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣄⢻⡏⠙⠹⠛⠿⠗⠀⠁⠈⠛⠀⠉⠉⠈⠉⠙⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
""",

f"""
⠀⠀⣿⠲⠤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣸⡏⠀⠀⠀⠉⠳⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣿⠀⠀⠀⠀⠀⠀⠀⠉⠲⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢰⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠲⣄⠀⠀⠀⡰⠋⢙⣿⣦⡀⠀⠀⠀⠀⠀
⠸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣙⣦⣮⣤⡀⣸⣿⣿⣿⣆⠀⠀⠀⠀
⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⠀⣿⢟⣫⠟⠋⠀⠀⠀⠀
⠀⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣷⣷⣿⡁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⢸⣿⣿⣧⣿⣿⣆⠙⢆⡀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢾⣿⣤⣿⣿⣿⡟⠹⣿⣿⣿⣿⣷⡀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣧⣴⣿⣿⣿⣿⠏⢧⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠈⢳⡀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡏⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⢳
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠸⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡇⢠⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠃⢸⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣼⢸⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠛⠻⠿⣿⣿⣿⡿⠿⠿⠿⠿⠿⢿⣿⣿⠏⠀⠀⠀⠀⠀⠀
"""
]

def get_random_banner():

    return random.choice(BANNERS)

def signal_handler(key, frame):
    log.failure(f"{colored('Exit...', 'white')}")
    os._exit(1)

singal = signal.signal(signal.SIGINT, signal_handler)


def help_panel():
    print(f"{colored('Usage:', 'white')} {colored(sys.argv[0], 'magenta', attrs=['bold'])}")
    
    print()
    
    print(f"{colored('MAC Checker:', 'yellow', attrs=['bold'])}")
    print(f"\t{colored('-m', 'blue', attrs=['bold'])} \t\t\t{colored('Uniq MAC', 'white')}")
    print(f"\t{colored('-M', 'blue', attrs=['bold'])} \t\t\t{colored('MAC file', 'white')}")
    print(f"\t{colored('-t, --threads', 'blue', attrs=['bold'])} \t\t{colored('Threads number', 'white')}")
    print(f"{colored('ARP scanner:', 'yellow', attrs=['bold'])}")
    print(f"\t{colored('-r, --range', 'blue', attrs=['bold'])} \t\t{colored('IP range', 'white')}")
    print(f"\t{colored('-i, --interface', 'blue', attrs=['bold'])} \t{colored('Netowork interface', 'white')}")
    print(f"{colored('General:', 'yellow', attrs=['bold'])}")
    print(f"\t{colored('-h, --help', 'blue', attrs=['bold'])} \t\t{colored('Show this help panel', 'white')}")

def setup_args():

    parser = argparse.ArgumentParser(description="Grim Reaper", add_help=False)

    parser.add_argument('-m', dest="mac", help="Uniq MAC")
    parser.add_argument('-M', dest="file", help="MAC File")
    parser.add_argument('-t', '--threads', dest="threads", type=int, help="Threads num")
    parser.add_argument('-r', '--range', dest="ip_range", help="IP range")
    parser.add_argument('-i', '--interface', dest="interface", help="Network interface")
    parser.add_argument('-h', '--help', help="Help panel")

    return parser.parse_args()

def uniq_mac(mac):

    url = "https://api.macvendors.com/v1/lookup/" + mac

    headers = {
        "Authorization": "[API]",
        "Accept": "text/plain"
}
    
    request = requests.get(url, headers=headers, timeout=5)

    if "Not Found" in request.text:
        sys.exit(1)

    if "Too Many Requests" in request.text:
        console.print(Panel(
        f"[white] Too Many Requests[/]",
        title="[bold yellow] Grim Reaper[/]",
        border_style="red",
        expand=False
        ))
        sys.exit(1)

    console.print(Panel(
        f"[white]Mac:[/] [bold blue]{mac}[/]\n[white]Vendor:[/] [bold blue]{request.text}[/]",
        title="[bold yellow] Grim Reaper[/]",
        border_style="green",
        expand=False
        ))

def process_file(file_path, num_threads):
    try:
        with open(file_path, 'r') as f:
            macs = [line.strip() for line in f if line.strip()]

        if not macs:
            log.failure(f"Empty file")
            sys.exit(1)

        total = len(macs)
        p1 = log.progress(f"{colored('Checking MAC\'s', 'white')}")
        
        completed = [0]

        def threaded_lookup(mac):
            uniq_mac(mac)
            completed[0] += 1
            p1.status(f"{colored('Found', 'white')} {colored(completed[0], 'green')}{colored('/', 'white')}{colored(total, 'red')} {colored('[', 'white')} {colored(mac, 'magenta', attrs=['bold'])} {colored(']', 'white')}")
        
        
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            executor.map(threaded_lookup, macs)
            
        p1.success(f"{colored(completed[0], 'green', attrs=['bold'])} {colored('MAC\'s found', 'white')}")

    except FileNotFoundError:
        log.failure(f"{colored('File not found:', 'white')} {colored(file_path, 'blue')}")


def arp_scan(ip_range, interface=None):
    arp_request = ARP(pdst=ip_range)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast / arp_request
    
    try:

        answered_list = srp(packet, timeout=3, iface=interface, verbose=False)[0]
        
        if not answered_list:
            log.warning("No devices found. Verify that the range is correct")
            return

        for sent, received in answered_list:

            console.print(Panel(
                f"[white]IP:[/] [bold blue]{received.psrc}[/]\n[white]MAC:[/] [bold blue]{received.hwsrc}[/]",
                title="[bold yellow] Grim Reaper[/]",
                border_style="green",
                expand=False
            ))
        
    except Exception as e:
        log.error(f"Scan error: {e}")
    
    console.print(Panel(
        f"[bold green]\\[M][/][green]ac[/]\n[bold cyan]\\[I][/][cyan]P[/]\n[bold red]\\[A][/][red]ll[/]",
        title="[bold yellow] Options[/]",
        border_style="green",
        expand=False
    ))
    option = input(f"{colored('What do you want to save? ', 'white')} ")
    if option == "":
        print()
        log.failure(f"{colored('Invalid option', 'white')}")
        sys.exit(1)
    file = input(f"{colored('File name', 'white')} {colored('==>', 'blue')} ")
    
    if file == "":
        file = "info.txt"

    if option == "M":
        with open (file, "w") as f:
            for sent, received in answered_list:
                info = received.hwsrc.strip()
                f.write(f"{info}\n")
        print()
        log.success(f"{colored('MAC\'s saved to:', 'white')} {colored(file, 'magenta', attrs=['bold'])}")

    elif option == "I":
        with open(file, "w") as f:
            for sent, received in answered_list:
                info = received.psrc.strip()
                f.write(f"{info}\n")
        print()
        log.success(f"{colored('IP\'s saved to:', 'white')} {colored(file, 'magenta', attrs=['bold'])}")

    elif option == "A":
        with open(file, "w") as f:
            for sent, received in answered_list:
                MAC = received.hwsrc.strip()
                IP = received.psrc.strip()
                f.write(f"{IP} {MAC}\n")
        print()
        log.success(f"{colored('IP\'s and MAC\'s saved to:', 'white')} {colored(file, 'magenta', attrs=['bold'])}")


if __name__ == '__main__':

    os.system("clear")
    
    print(f"{colored(NAME, 'white', attrs=['reverse',])}")
    print(f"{colored(get_random_banner(), 'white')}")

    console.print(Panel(
        f"[bold white]Author:[/][blue] Sn0wBaall[/]\n[bold white]My github:[/][blue] https://github.com/Sn0wBaall[/]",
        title="Info",
        expand=False
    ))
    print()

    args = setup_args()

    if len(sys.argv) == 1:
        help_panel()
        sys.exit(1)
    
    if args.mac:
        uniq_mac(args.mac)
        sys.exit(1)

    if args.file:
        process_file(args.file, args.threads)
        sys.exit(1)

    if args.ip_range:
        arp_scan(args.ip_range, args.interface)
        sys.exit(1)
