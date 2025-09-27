import socket
import threading
import sys
import rsa
from cryptography.fernet import Fernet
import hashlib
import time
import friends

def loader(IP, PORT):
    animation = "|/-\\"
    for i in range(10):
        time.sleep(0.1)
        sys.stdout.write(f"\rLoading... {animation[i % len(animation)]}")
        sys.stdout.flush()
    sys.stdout.write("\n")
    client(IP, PORT)

def client(IP, PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))

    f = None

    passwordFind = s.recv(4096).decode("utf8")
    if passwordFind == "[*] Password Require [*]":
        print(passwordFind)
        password = input("Password → ")
        hashed_password = hashlib.sha256(password.encode("utf8")).hexdigest()
        s.send(hashed_password.encode("utf8"))
        result = s.recv(4096).decode("utf8")
        if result != "[*] Authentification successful! [*]":
            print("[*] Authentification incorrect! [*]")
            s.close()
            return
        print(result)

    elif passwordFind == "[!] No Password require [!]":
        print("[*] No password require [*]")

    userName = s.recv(4096)
    userName = userName.decode("utf8")
    friendDialog = input(f"Do you want to add {userName} to your friends ? (Y/n) → ")
    if friendDialog in ["y", "Y"]:
        friends.add(userName, IP)

    publicKey = s.recv(4096)
    publicKey = rsa.PublicKey.load_pkcs1(publicKey)
    key = Fernet.generate_key()
    encryptKey = rsa.encrypt(key, publicKey)
    s.send(encryptKey)

    f = Fernet(key)


    def clientSend():
        try:
            while True:
                msg = input("You → ")
                if msg.lower() in ["bye"]:
                    s.close()
                    break
                msg = f.encrypt(msg.encode())
                s.send(msg)
        except Exception as e:
            print(f"[!] Error : {e} [!]")
            s.close()

    threading.Thread(target=clientSend, daemon=True).start()

    try:
        while True:
            data = s.recv(4096)
            if not data:
                break
            data = f.decrypt(data).decode()
            print(f"\n{IP} → {data}")
            print("You → ", end="", flush=True)
    except Exception as e:
        print(f"[!] Error : {e} [!]")
    finally:
        s.close()
