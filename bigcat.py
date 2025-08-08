import socket
import os
import threading
import sys
import server
import client
import rsa
import cryptography
import hashlib
import json

def main(menuPrompt):
    while True:
        
        mPrompt = {
            "Default" : "BigCat → ",
            "Bash" : "BigCat:~$ " 
        }
        cmd = ["bye", "clear"]
        prompt = input(f"{mPrompt[f"{menuPrompt}"]}")
        if prompt in cmd:
            if prompt == "bye":
                quit()
            if prompt == "clear":
                os.system("clear" if os.name != "nt" else "cls")
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
        elif prompt.startswith("join "):
            parts = prompt.split()
            if len(parts) == 3:
                IP = parts[1]
                PORT = int(parts[2])
                client.loader(IP, PORT)
        else:
            print("[!] Sorry, this command is not recognized [!]")
with open("etc/config/config.json", "r") as config:
    config = json.load(config)

menuPrompt = config["menuPrompt"]
main(menuPrompt)
