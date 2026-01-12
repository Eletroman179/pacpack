#!/usr/bin/env python

from colorama import Fore, init
from termcolor import colored, cprint
import json
import sys
import os

init()

if len(sys.argv) > 1:
    pac_file = sys.argv[1]
else:
    while True:
        pac_file = input("pac file: ")
        if os.path.isfile(pac_file) == False:
            break  
        else:
            print("Re-enter pac file")

with open(pac_file, 'r') as f:
    pac = json.load(f)

cols, rows = os.get_terminal_size()

divide_term = "=" * cols

print(json.dumps(pac, indent=4))

print(divide_term)
print(f"Pac made by {pac["info"]["creator"]} on {pac["info"]["website"]["type"]} @ {pac["info"]["website"]["site"]}")
print(divide_term)
print("Installing:")
for name in pac["packs"]:
    print(f"- {name["name"]}")
print(divide_term)

for i in pac["packs"]:
    if i["type"] in ("command"):
        has_commands = True
        break
else:
    has_commands = False

if has_commands:
    cprint("Warning", "red", attrs=["blink"])
    print(f"{Fore.RED}This pac contains commands this might be malware{Fore.RESET}")
    print(f"{Fore.RED}Make sure that you trust {pac["info"]["creator"]}{Fore.RESET}")
usr_inp = input("Confirm [Y/n]: ")

if usr_inp.lower() != "n":
    for data in pac["packs"]:
        if data["type"] == "pacman":
            os.system(f"sudo pacman -S {data["package"]}")
        elif data["type"] == "AUR":
            os.system(f"yay -S {data["package"]}")
        elif data["type"] == "command":
            for command in data["package"]:
                os.system(command)