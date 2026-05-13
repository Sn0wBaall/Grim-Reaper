#!/usr/bin/env python3

from concurrent.futures import ThreadPoolExecutor
import argparse, random, signal, os, sys

try:
    from pwn import *
    from termcolor import colored
    import requests
    from rich.panel import Panel
    from rich.console import Console
    from rich.table import Table
    from rich import box
    from scapy.all import ARP, Ether, srp
except ImportError as e:
    print(f"\n[-] Libraries cant't be imported\n[i] {e}\n")
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

base_url = "https://api.macvendors.com/v1/lookup/"

api = "[API]"

def get_random_banner():

    return random.choice(BANNERS)

def signal_handler(key, frame):
    log.failure(f"{colored('Exit...', 'white')}")
    os._exit(1)

signal.signal(signal.SIGINT, signal_handler)

def help_panel():
    print(f"{colored('Usage:', 'white')} {colored(sys.argv[0], 'magenta', attrs=['bold'])}")
    
    print()
    
    print(f"{colored('MAC Checker:', 'yellow', attrs=['bold'])}")
    print(f"\t{colored('-m', 'blue', attrs=['bold'])} \t\t\t{colored('Uniq MAC', 'white')}")
    print(f"\t{colored('-M', 'blue', attrs=['bold'])} \t\t\t{colored('MAC file', 'white')}")
    print(f"\t{colored('-t, --threads', 'blue', attrs=['bold'])} \t\t{colored('Threads number', 'white')}")
    print(f"{colored('ARP scanner', 'yellow', attrs=['bold'])} {colored('(', 'white', attrs=['bold'])}{colored('EXECUTE IT AS ROOT', 'white', 'on_red', attrs=['bold'])}{colored(')', 'white', attrs=['bold'])}{colored(':', 'yellow', attrs=['bold'])}")
    print(f"\t{colored('-r, --range', 'blue', attrs=['bold'])} \t\t{colored('IP range', 'white')}")
    print(f"\t{colored('-i, --interface', 'blue', attrs=['bold'])} \t{colored('Netowork interface', 'white')}")
    print(f"\t{colored('-c, --complete', 'blue', attrs=['bold'])} \t\t{colored('ARP scan and check MAC\'S', 'white')}")
    print(f"{colored('General:', 'yellow', attrs=['bold'])}")
    print(f"\t{colored('-h, --help', 'blue', attrs=['bold'])} \t\t{colored('Show this help panel', 'white')}")

def setup_args():

    parser = argparse.ArgumentParser(description="Grim Reaper", add_help=False)

    parser.add_argument('-m', dest="mac", help="Uniq MAC")
    parser.add_argument('-M', dest="file", help="MAC File")
    parser.add_argument('-t', '--threads', dest="threads", type=int, help="Threads num")
    parser.add_argument('-r', '--range', dest="ip_range", help="IP range")
    parser.add_argument('-i', '--interface', dest="interface", help="Network interface")
    parser.add_argument('-c', '--complete', dest="complete", action="store_true",help="ARP scan and d check MAC\'s")
    parser.add_argument('-h', '--help', help="Help panel")

    return parser.parse_args()

def uniq_mac(mac):

    url = base_url + mac

    headers = {
        "Authorization": f"Bearer {api}",
        "Accept": "text/plain"
    }
    
    request = requests.get(url, headers=headers, timeout=5)

    if "Not Found" in request.text:
        sys.exit(1)

    if "Too Many Requests" in request.text:
        console.print(Panel(
        f"[white] Too Many Requests[/]\n[white] Recommended action: adjust the threads using[/][blue] -t[/]",
        title="[bold yellow]Grim Reaper[/]",
        border_style="red",
        expand=False
        ))
        sys.exit(1)

    console.print(Panel(
        f"[white]Mac:[/][bold blue] {mac}[/]\n[white]Vendor:[/][bold blue] {request.text}[/]",
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
    arp_request = ARP(pdst=ip_range, psrc="1.1.1.1")
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast / arp_request
    
    try:

        answered_list = srp(packet, timeout=3, iface=interface, verbose=False)[0]
        
        if not answered_list:
            log.warning(f"{colored('No devices found. Verify that the range is correct', 'white')}")
            return

        for sent, received in answered_list:

            console.print(Panel(
                f"[white]IP:[/][bold blue] {received.psrc}[/]\n[white]MAC:[/][bold blue] {received.hwsrc}[/]",
                title="[bold yellow]Grim Reaper[/]",
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

    if option not in ['M', 'I', 'A']:
        log.failure(f"{colored('Invalid optino', 'white')}")
        return

    filename = input(f"{colored('File name (default: info.txt)', 'white')} {colored('==>', 'blue')} ") or "info.txt"

    try:
        with open(filename, "w") as f:
            for _, received in answered_list:
                ip, mac = received.psrc.strip(), received.hwsrc.strip()

                formats = {
                    "M": f"{mac}\n",
                    "I": f"{ip}\n",
                    "A": f"{ip},{mac}\n"
                }
                f.write(formats[option])

        log.success(f"{colored('Data saved to', 'white')} {colored(filename, 'magenta', attrs=['bold'])}")
    except Exeption as e:
        log.error(f"{colored('Error saving file: {e}')}")

def consult(ip, mac):      

    url = base_url + mac
    
    headers = {
        "Authorization": f"Bearer {api}",
       "Accept": "text/plain"
    }

    request = requests.get(url, headers=headers)

    if "Not Found" in request.text:
        return

    if "Too Many Requests" in request.text:
        console.print(Panel(
        f"[white] Too Many Requests[/]\n[white] Recommended action: adjust the threads using[/][blue] -t[/]",
        title="[bold yellow]Grim Reaper[/]",
        border_style="red",
        expand=False
    ))

    console.print(Panel(
        f"[white]IP:[/][bold blue] {ip}[/]\n[white]MAC:[/][bold blue] {mac}[/]\n[white]Vendor:[/][bold blue] {request.text}[/]",
        title="[bold yellow]Grim Reaper[/]",
        border_style="green",
        expand=False
    ))


def complete_scan(ip_range, interface, num_threads):
    
    p1 = log.progress(f"{colored('Getting MAC\'s', 'white')}")

    arp_request = ARP(pdst=ip_range, psrc="1.1.1.1")
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast / arp_request
    
    try:

        answered_list = srp(packet, timeout=3, iface=interface, verbose=False)[0]
        
        if not answered_list:
            log.warning(f"{colored('No devices found. Verify that the range is correct', 'white')}")
            return

    except Exception as e:
        log.error(f"{colored('Scan errot', 'white')} {colored(e, 'magenta', attrs=['bold'])}")
        sys.exit(1)

    network_map = {received.psrc: received.hwsrc for sent, received in answered_list}
    
    p1.success(f"{colored('Done', 'green')}")
    p1 = log.progress(f"{colored('Cheking MAC\'s', 'white')}")

    with ThreadPoolExecutor(max_workers=num_threads) as executor:

        for ip, mac in network_map.items():

            executor.submit(consult, ip, mac)

    p1.success(f"{colored('Done', 'green')}")

if __name__ == '__main__':

    os.system("clear")
    
    print(f"{colored(NAME, 'white', attrs=['reverse',])}")
    print(f"{colored(get_random_banner(), 'white')}")

    info = Table(border_style="white", box=box.ROUNDED, show_header=False, width=50)
    
    info.add_column("Key", style="bold red", width=12)
    info.add_column("Value", style="bold cyan")

    info.add_row('Author', 'Sn0wBaall')
    info.add_row('Github', 'https://github.com/Sn0wBaall')

    console.print(info)

    print()
    args = setup_args()

    if len(sys.argv) == 1:
        help_panel()
        sys.exit(1)

    if args.complete:
        if not args.ip_range:
            log.failure(f"{colored('The parameter', 'white')} {colored('-c', 'blue')} {colored('need a IP range', 'white')}")
            sys.exit(1)
        complete_scan(args.ip_range, args.interface, args.threads)
        sys.exit(0)

    if args.mac:
        uniq_mac(args.mac)
        sys.exit(1)

    if args.file:
        process_file(args.file, args.threads)
        sys.exit(1)

    if args.ip_range:
        arp_scan(args.ip_range, args.interface)
        sys.exit(1)
