#Importing libs
from tkinter import messagebox
import customtkinter
import socket
import os
import threading
import sys
import rsa
import cryptography
import hashlib
import json
import time
from requests import get
#Importing files
import server
import client
import register
import login
def create(IP, PORT, passwordSecurity, password, root):
    root.destroy()
    passwdCheck = open("etc/password/check.txt", "w+").write("true")
    if passwordSecurity == True:
        with open("etc/config/config.json", "r") as hashMode:
            hashMode = json.load(hashMode)

        hash = hashMode["Hash Algorithm"]
        if hash == "sha256":

            if not os.path.exists("password/password.key"):
                sha256 = hashlib.sha256()
                sha256.update(password.encode('utf-8'))
                with open("etc/password/password.key", "w+") as password_file:
                    password_file.write(sha256.hexdigest())
            else:
                pass
        else:
            if not os.path.exists("password/password.key"):
                sha512 = hashlib.sha512()
                sha512.update(password.encode('utf-8'))
                with open("etc/password/password.key", "w+") as password_file:
                    password_file.write(sha512.hexdigest())
            else:
                pass
    else:
        if os.path.exists("etc/password/check.txt"):

                os.system("rm etc/password/check.txt")
        else:
            pass
        pass
    server.server(IP, int(PORT))
def createFrame():
    root = customtkinter.CTk()
    root.title("BigCat - Create Session")
    root.minsize(400, 500)
    root.maxsize(400, 500)

    label = customtkinter.CTkLabel(root, text="Create your session!")
    label.pack(pady=10)

    ipLabel = customtkinter.CTkLabel(root, text="IP Address")
    ipLabel.pack()
    ipEntry = customtkinter.CTkEntry(root, placeholder_text="192.168.1.1")
    ipEntry.pack()

    portLabel = customtkinter.CTkLabel(root, text="Port")
    portLabel.pack()
    portEntry = customtkinter.CTkEntry(root, placeholder_text="1234")
    portEntry.pack()
    encryptButton = customtkinter.CTkSwitch(root, text="Encrypt connections")
    encryptButton.pack(pady=5)

    passwordVariable = customtkinter.StringVar(value="off")
    passwordEntry = customtkinter.CTkEntry(root, placeholder_text="Enter password", show="*")
    passwordSecurity = False

    def togglePassword(*args):
        nonlocal passwordSecurity
        if passwordVariable.get() == "on":
            passwordEntry.pack(pady=5)
            passwordSecurity = True
        else:
            passwordEntry.pack_forget()
            passwordSecurity = False

    passwordButton = customtkinter.CTkSwitch(
        root,
        text="Password Security",
        variable=passwordVariable,
        onvalue="on",
        offvalue="off"
    )
    passwordButton.pack(pady=5)

    passwordVariable.trace_add("write", togglePassword)
    createButton = customtkinter.CTkButton(root,text="Create", command=lambda: create(ipEntry.get(), portEntry.get(),passwordSecurity ,passwordEntry.get(), root))
    createButton.pack()

    root.mainloop()
def joinFrame():
    root = customtkinter.CTk()
    root.title("BigCat - Join Session")
    root.minsize(400, 500)
    root.maxsize(400, 500)
    ipLabel = customtkinter.CTkLabel(root, text="IP Address")
    ipLabel.pack()
    ipEntry = customtkinter.CTkEntry(root, placeholder_text="192.168.1.1")
    ipEntry.pack()

    portLabel = customtkinter.CTkLabel(root, text="Port")
    portLabel.pack()
    portEntry = customtkinter.CTkEntry(root, placeholder_text="1234")
    portEntry.pack()

    joinButton = customtkinter.CTkButton(root,text="Join", command=lambda: client.client(ipEntry.get(), int(portEntry.get())))
    joinButton.pack()
    root.mainloop()
def settingFrame():
    root = customtkinter.CTk()
    root.title("BigCat - Settings")
    root.minsize(400, 500)
    root.maxsize(400, 500)
    darkModeVariable = customtkinter.StringVar(value="off")
    passwordEntry = customtkinter.CTkEntry(root, placeholder_text="Enter password", show="*")
    passwordSecurity = False

    def darkMode(*args):
        nonlocal passwordSecurity
        if darkModeVariable.get() == "on":
            with open("etc/config/theme.json", "w+") as themeFile:
                themeFile.write('{\n"DarkMode" : "True"\n}')
        else:
            with open("etc/config/theme.json", "w+") as themeFile:
                themeFile.write('{\n"DarkMode" : "False"\n}')

    darkModeSwitch = customtkinter.CTkSwitch(
        root,
        text="Dark Mode",
        variable=darkModeVariable,
        onvalue="on",
        offvalue="off"
    )
    darkModeSwitch.pack(pady=5)

    darkModeVariable.trace_add("write", darkMode)

    def about():
            about_frame = customtkinter.CTk()
            about_frame.title("BigCat - About")
            about_frame.minsize(500, 100)
            about_frame.maxsize(500, 100)

            explain = customtkinter.CTkLabel(about_frame, 
                text="BigCat is a secure messaging app in python that protect your privacy!.\n"
                     "It's a small project just for fun. I am a beginner in coding\n"
                     "so there are may be bugs and security issues.\n"
                     "Thanks using my project :3")
            explain.pack(padx=20, pady=20)
            about_frame.mainloop()


    def hash(hashChoice):
        path = "etc/config/config.json"

        if not os.path.exists(path):
            data = {"Hash Algorithm": ""}
        else:
            with open(path, "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {"Hash Algorithm": ""}

        data["Hash Algorithm"] = hashChoice

        with open(path, "w") as f:
            json.dump(data, f, indent=4)


    hashChoice = ["sha256", "sha512"]
    hashMenu = customtkinter.CTkOptionMenu(root, values=hashChoice, command=hash)
    hashMenu.pack()

    aboutButton = customtkinter.CTkButton(root, text="About BigCat", command=about)
    aboutButton.place(relx=0.325, rely=0.2)


    root.mainloop()
def getPrivateIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    privateIP = s.getsockname()[0]
    s.close()
    return privateIP
def getPublicIP():
    ip = get('https://api.ipify.org').content.decode('utf8')
    return ip

def main():
    ascii_art = r"""
                      /^--^\     /^--^\     /^--^\
                      \____/     \____/     \____/
                     /      \   /      \   /      \
                    |        | |        | |        |
                     \__  __/   \__  __/   \__  __/
|^|^|^|^|^|^|^|^|^|^|^|^\ \^|^|^|^/ /^|^|^|^|^\ \^|^|^|^|^|^|^|^|^|^|^|^|
| | | | | | | | | | | | |\ \| | |/ /| | | | | | \ \ | | | | | | | | | | |
########################/ /######\ \###########/ /#######################
| | | | | | | | | | | | \/| | | | \/| | | | | |\/ | | | | | | | | | | | |
|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|
"""
    username = open("account/username.txt", "r").read()
    privateIP = getPrivateIP()
    publicIP = getPublicIP()

    root = customtkinter.CTk()
    root.title("BigCat - Gui")
    root.minsize(900, 500)
    root.maxsize(900, 500)
    if os.path.exists("account/valid"):

        with open("etc/config/theme.json", "r") as themeFile:
            themeFile = json.load(themeFile)

        darkMode = themeFile["DarkMode"]
        if darkMode == "True":
            root._set_appearance_mode("dark")
        else:
            root._set_appearance_mode("light")

    usernameLabel = customtkinter.CTkLabel(root, text=f"{username}")
    usernameLabel.place(anchor="center", relx=0.9, rely=0.05)

    publicIPLabel = customtkinter.CTkLabel(root, text=f"Public IP : {publicIP}", text_color="green")
    publicIPLabel.place(anchor="center", relx=0.28, rely=0.95)

    privateIPLabel = customtkinter.CTkLabel(root, text=f"Private IP : {privateIP}", text_color="green")
    privateIPLabel.place(anchor="center", relx=0.1, rely=0.95)

    settingButton = customtkinter.CTkButton(root, text="⚙", width=25, height=28,command=settingFrame)
    settingButton.place(anchor="center", relx=0.95, rely=0.95)

    createButton = customtkinter.CTkButton(root, text="Create", command=createFrame)
    createButton.place(anchor="center", relx=0.085, rely=0.05)

    joinButton = customtkinter.CTkButton(root, text="Join", command=joinFrame)
    joinButton.place(anchor="center", relx=0.25, rely=0.05)

    iconLabel = customtkinter.CTkLabel(
        root,
        text=ascii_art,
        font=("Courier", 12),
        justify="left"
    )
    iconLabel.place(anchor="center", relx=0.5, rely=0.5)

    root.mainloop()
if os.path.exists("account/password.key"):
    login.login()
    if os.path.exists("account/valid"):
        main()
else:
    update = customtkinter.CTk()
    update.title("BigCat - News")
    update.minsize(400, 400)
    update.maxsize(400, 400)
    news = customtkinter.CTkLabel(update, text="-⛉sha512 available\n-🖳Full gui interface\n-🗎File sending\n-✎New design\n-🗲Simple Optimization\n-🖧Bug correction\n-</>New code structure", font=("font", 30))
    news.pack()
    okButton = customtkinter.CTkButton(update, text="Ok", command=(
        register.register
    ))
    okButton.pack()
    update.mainloop()