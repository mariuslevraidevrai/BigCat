#Importing libs
from tkinter import messagebox
import socket
import os
import threading
import sys
import rsa
import cryptography
import hashlib
import json
import time
from termcolor import colored
from requests import get
#Importing files
import server
import client
import register
import login
import friends
def getPrivateIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    privateIP = s.getsockname()[0]
    s.close()
    return privateIP
def getPublicIP():
    ip = get('https://api.ipify.org').content.decode('utf8')
    return ip

def main(menuPrompt):
    privateIP = getPrivateIP()
    publicIP = getPublicIP()
    os.system("clear")
    animation = "|/-\\"
    for i in range(10):
        time.sleep(0.1)
        sys.stdout.write(f"\rBigCat is loading... {animation[i % len(animation)]}")
        sys.stdout.flush()
    sys.stdout.write("\n")
    os.system("clear")
    print(colored("Version > BigCat 0.0.2 x86_64","blue"))
    print(colored(f"privateIP > {privateIP}", "red"))
    print(colored(f"publicIP > {publicIP}", "green"))
    print(colored("Encryption : RSA, Fernet, sha256", "blue"))
    print(colored("Licence : GPL 3.0", "blue"))
    username = open("account/username.txt", "r").read()
    print(f"Welcome {username}, lets go to chat with your friend safely!")
    while True:
        
        mPrompt = {
            "Default" : "BigCat → ",
            "Bash" : "BigCat:~$ " ,
            "Arch" : "root@BigCat ~ #",
            "Custom" : f"{menuPrompt}"
        }
        cmd = ["bye", "clear"]
        if menuPrompt not in mPrompt:
            prompt = input(f"{menuPrompt}")
        else:
            prompt = input(f"{mPrompt[f"{menuPrompt}"]}")
        if prompt in cmd:
            if prompt == "bye":
                print("""  
                         ^~^  ,
                        ('Y') )
                        /   \/ 
                        (\|||/) Bye
                        """)
                return
            if prompt == "clear":
                os.system("clear" if os.name != "nt" else "cls")
        elif prompt == "help":
            with open("etc/commands/cmds.txt", "r") as helpFile:
                print(colored(helpFile.read(), "blue"))
        elif prompt.startswith("create "):
            parts = prompt.split()
            if len(parts) == 3:
                IP = parts[1]
                PORT = int(parts[2])
                passwordDialog = input("Do you want a password (Y/n) : ")
                if passwordDialog in ["y", "Y"]:
                    passwdCheck = open("etc/password/check.txt", "w+").write("true")
                    if not os.path.exists("password/password.key"):
                        sha256 = hashlib.sha256()
                        password = input("Password → ")
                        sha256.update(password.encode('utf-8'))
                        with open("etc/password/password.key", "w+") as password_file:
                            password_file.write(sha256.hexdigest())
                    else:
                        pass
                else:
                    if os.path.exists("etc/password/check.txt"):

                        os.system("rm etc/password/check.txt")
                    else:
                        pass
                    pass
                server.server(IP, PORT)
            if parts[3] == "code":
                IP = parts[1]
                PORT = int(parts[2])
                #Generate Code
                ip = parts[1].split(".")
                port = int(parts[2])
                part1 = int(ip[0]) + 256
                part2 = int(ip[1]) + 256
                part3 = int(ip[2]) + 256
                part4 = int(ip[3]) + 256

                code = f"{int(part1)}-{part2}-{part3}-{part4}:{str(port)}"
                print(f"[*] Your session code is {code} [*]")

                passwordDialog = input("Do you want a password (Y/n) : ")
                if passwordDialog in ["y", "Y"]:
                    passwdCheck = open("etc/password/check.txt", "w+").write("true")
                    if not os.path.exists("password/password.key"):
                        sha256 = hashlib.sha256()
                        password = input("Password → ")
                        sha256.update(password.encode('utf-8'))
                        with open("etc/password/password.key", "w+") as password_file:
                            password_file.write(sha256.hexdigest())
                    else:
                        pass
                else:
                    if os.path.exists("etc/password/check.txt"):

                        os.system("rm etc/password/check.txt")
                    else:
                        pass
                    pass
                server.server(IP, PORT)
        elif prompt.startswith("join "):
            parts = prompt.split()
            if len(parts) == 3:
                IP = parts[1]
                PORT = int(parts[2])
                client.loader(IP, PORT)
            if len(parts) == 2:
                code = parts[1].split(":")
                IP = code[0]
                PORT = code[1]
                IPSplit = IP.split("-")
                IPPart1 = int(IPSplit[0])-256
                IPPart2 = int(IPSplit[1])-256
                IPPart3 = int(IPSplit[2])-256
                IPPart4 = int(IPSplit[3])-256
                IPFinal = f"{IPPart1}.{IPPart2}.{IPPart3}.{IPPart4}"
                warningDialog = input(f"Do you want join {IPFinal} (Y/n) : ")
                client.loader(IPFinal, int(PORT))

        else:
            print("[!] Sorry, this command is not recognized [!]")
if os.path.exists("account/password.key"):
    login.login()
    if os.path.exists("account/valid"):

        with open("etc/config/config.json", "r") as config:
            config = json.load(config)

        menuPrompt = config["menuPrompt"]
        main(menuPrompt)
    else:
        raise SystemExit
else:
    update = messagebox.showinfo("BigCat 0.0.2", "BigCat 0.0.2 is available!")
    register.register()