import socket
import threading
import rsa
from cryptography.fernet import Fernet
import hashlib
import os


def serverSend(client, address, f):
    try:
        while True:
            prompt = input(f"You → ")
            msg = f.encrypt(prompt.encode())
            client.send(msg)
    except Exception as e:
        print(f"[!] Error : {e} [!]")

def server(IP, PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((IP, PORT))
    s.listen(5)
    print(f"[*] Your BigCat session started on port {PORT} [*]")

    try:
        while True:
            client, address = s.accept()
            print(f"[*] {address[0]} connected! [*]")
            if os.path.exists("etc/password/check.txt"):
                passwordFind = client.send("[*] Password Require [*]".encode("utf8"))
                passwd = client.recv(4096).decode("utf8")
                if passwd == open("etc/password/password.key", "r").read():
                    resultOk = client.send("[*] Authentification successful! [*]".encode("utf8"))
                    print("[*] Authentification successful! [*]")
                    #Send the username
                    userName = open("account/username.txt", "r").read().encode("utf8")
                    client.send(userName)

                    publicKey, privateKey = rsa.newkeys(2048)
                    client.send(publicKey.save_pkcs1())
                    key = client.recv(4096)
                    decryptKey = rsa.decrypt(key, privateKey)
                    f = Fernet(decryptKey)
                    threading.Thread(target=serverSend, args=(client, address, f), daemon=True).start()
                    try:
                        while True:
                            msg = client.recv(4096)
                            if not msg:
                                break
                            msg = f.decrypt(msg).decode()
                            print(f"\n{address[0]} → {msg}")
                            print("You → ", end="", flush=True)
                    except Exception as e:
                        print(f"[!] Error : {e} [!]")
                        client.close()
                        s.close()
                    finally:
                        print(f"[!] {address[0]} left the chat ˙◠˙ [!]")
                        client.close()
                        s.close()
                    
                else:
                    resultNotOk = client.send("[!] Authentification incorrect! [!]".encode("utf8"))
                    client.close()
                    continue
            else:
                client.send("[!] No Password require [!]".encode("utf8"))
                userName = open("account/username.txt", "r").read().encode("utf8")
                client.send(userName)
                publicKey, privateKey = rsa.newkeys(2048)
                client.send(publicKey.save_pkcs1())
                key = client.recv(4096)
                decryptKey = rsa.decrypt(key, privateKey)
                f = Fernet(decryptKey)

                threading.Thread(target=serverSend, args=(client, address, f), daemon=True).start()
                try:
                    while True:
                        msg = client.recv(4096)
                        if not msg:
                            break
                        msg = f.decrypt(msg).decode()
                        print(f"\n{address[0]} → {msg}")
                        print("You → ", end="", flush=True)
                except Exception as e:
                    print(f"[!] Error : {e} [!]")
                finally:
                    print(f"[!] {address[0]} left the chat ˙◠˙ [!]")
                    client.close()
    except KeyboardInterrupt:
        print("\n[!] Server shutting down [!]")
    finally:
        s.close()