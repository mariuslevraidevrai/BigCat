import os
import hashlib

def register():
    os.system("clear")
    print("Register you on BigCat")
    username = input("Username → ")
    with open("account/username.txt", "w+") as usernameFile:
        usernameFile.write(username)
    password = input("Password → ")
    password = password.encode("utf8")
    passwordHash = hashlib.sha256(password)
    passwordHex = passwordHash.hexdigest()
    with open("account/password.key", "w+") as passwordFile:
        passwordFile.write(passwordHex)