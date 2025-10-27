import socket
import threading
import rsa
from cryptography.fernet import Fernet
import hashlib
import customtkinter
import os


def client(IP, PORT):
    root = customtkinter.CTk()
    root.title(f"BigCat - Client")
    root.geometry("400x500")

    chatBox = customtkinter.CTkTextbox(root, width=380, height=400)
    chatBox.pack(pady=10)
    chatBox.insert("end", f"[*] Connection to {IP}! [*]\n")
    chatBox.configure(state="disabled")

    entry = customtkinter.CTkEntry(root, placeholder_text="Write Here")
    entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

    def clearChat():
        chatBox.configure(state="normal")
        chatBox.delete("0.0", "end")
        chatBox.configure(state="disabled")

    clearButton = customtkinter.CTkButton(root, text="🧹", command=clearChat, width=30, height=28)
    clearButton.pack(side="right")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    f = None
    connected = False

    def log(msg):
        chatBox.configure(state="normal")
        chatBox.insert("end", msg + "\n")
        chatBox.configure(state="disabled")
        chatBox.see("end")

    def connectToServer():
        nonlocal f, connected
        try:
            s.connect((IP, PORT))
            log("[*] Connected to server! [*]")

            msg = s.recv(4096).decode("utf8")
            if msg == "[*] Password Require [*]":
                log("[*] Password required [*]")
                pwWindow = customtkinter.CTkToplevel(root)
                pwWindow.title("Authentification")
                pwWindow.minsize(400,200)

                pwEntry = customtkinter.CTkEntry(pwWindow, show="*")
                pwEntry.pack(pady=10)

                def sendPassword():
                    hashMode= s.recv(4096).decode("utf8")
                    if hashMode == "[*] sha256 use [*]":

                        hashed = hashlib.sha256(pwEntry.get().encode("utf8")).hexdigest()
                        s.send(hashed.encode("utf8"))
                    else:
                        hashed = hashlib.sha512(pwEntry.get().encode("utf8")).hexdigest()
                        s.send(hashed.encode("utf8"))

                    def waitForResult():
                        nonlocal f, connected
                        try:
                            result = s.recv(4096).decode("utf8")
                            if result != "[*] Authentification successful! [*]":
                                log("[!] Incorrect password [!]")
                                s.close()
                            else:
                                log("[*] Authentification successful [*]")
                                setupEncryption()
                        except Exception as e:
                            log(f"[!] Connection error: {e} [!]")
                        finally:
                            pwWindow.destroy()

                    threading.Thread(target=waitForResult, daemon=True).start()

                btn = customtkinter.CTkButton(pwWindow, text="Connect", command=sendPassword)
                btn.pack(pady=5)

            elif msg == "[!] No Password require [!]":
                log("[!] No password required [!]")
                setupEncryption()

        except Exception as e:
            log(f"[!] Connection error : {e} [!]")
            s.close()

    def setupEncryption():
        nonlocal f, connected
        try:
            username = s.recv(4096).decode("utf8")
            log(f"[*] Connected to {username} [*]")

            publicKey = rsa.PublicKey.load_pkcs1(s.recv(4096))
            key = Fernet.generate_key()
            encryptedKey = rsa.encrypt(key, publicKey)
            s.send(encryptedKey)
            f = Fernet(key)
            connected = True
            log("[*] Encryption Initialized 🔐 [*]")

            threading.Thread(target=receiveLoop, daemon=True).start()

        except Exception as e:
            log(f"[!] Encryption setup error : {e} [!]")

    def receiveLoop():
        nonlocal connected
        try:
            while connected:
                data = s.recv(10_000_000)
                if not data:
                    break
                if data.startswith(b"[FILE]"):
                    
                    header, encryptedData = data.split(b"::", 1)
                    filename = header[6:].decode()
                    decryptedData = f.decrypt(encryptedData)
                    with open(f"etc/cache/{filename}", "wb") as out:
                        out.write(decryptedData)

                elif data.startswith(b"[TEXT]"):
                    msg = f.decrypt(data[6:]).decode("utf8")
                    log(f"Server → {msg}")
                else:
                    msg = f.decrypt(data).decode("utf8")
                    log(f"Server → {msg}")
        except Exception as e:
            log(f"[!] Receive error: {e} [!]")
        finally:
            connected = False
            s.close()
            log("[!] Disconnected from server [!]")

    def sendMessage(event=None):
        nonlocal connected
        if not connected or not f:
            return log("[!] Not connected [!]")
        msg = entry.get().strip()
        if not msg:
            return
        entry.delete(0, "end")
        try:
            s.send(b"[TEXT]" + f.encrypt(msg.encode("utf8")))
            log(f"Vous → {msg}")
        except Exception as e:
            log(f"[!] Send error: {e} [!]")

    def sendFile():
        nonlocal connected
        if not connected or not f:
            return log("[!] Not connected [!]")
        filePath = customtkinter.filedialog.askopenfilename(title="Select a file")
        if not filePath:
            return
        with open(filePath, "rb") as file:
            data = file.read()
        fileName = os.path.basename(filePath)
        header = f"[FILE]{fileName}".encode()
        encryptedData = f.encrypt(data)
        try:
            s.sendall(header + b"::" + encryptedData)
            log(f"[*] {fileName} sent 📤 [*]")
        except Exception as e:
            log(f"[!] File send error: {e} [!]")

    entry.bind("<Return>", sendMessage)
    sendButton = customtkinter.CTkButton(root, text="⌲", command=sendMessage, width=28, height=28)
    sendButton.pack(side="left")
    fileButton = customtkinter.CTkButton(root, text="📑", width=28, height=28, command=sendFile)
    fileButton.pack(side="left")

    threading.Thread(target=connectToServer, daemon=True).start()

    root.mainloop()
