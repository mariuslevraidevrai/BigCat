import os
import hashlib

def login():
    os.system("clear")
    if os.path.exists("account/valid"):
        pass
    else:
        print("Connect you to BigCat")
        username = input("Username → ")
        password = input("Password → ").encode("utf8")
        sha256 = hashlib.sha256()
        passwordHash = hashlib.sha256(password)
        passwordHex = passwordHash.hexdigest()
        if passwordHex == open("account/password.key", "r").read():
            os.system("touch account/valid")
        else:
            print("[!] Sorry the password is incorect [!]")