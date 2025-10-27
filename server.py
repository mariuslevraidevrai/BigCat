import socket
import threading
import rsa
from cryptography.fernet import Fernet
import hashlib
import os
import customtkinter
import json

def handleClient(client, address, root, chatBox, entry):
    try:
        if os.path.exists("etc/password/check.txt"):
            client.send("[*] Password Require [*]".encode("utf8"))
            with open("etc/config/config.json", "r") as hashMode:
                hashMode = json.load(hashMode)

            hash = hashMode["Hash Algorithm"]
            if hash == "sha256":
                client.send("[*] sha256 use [*]".encode("utf8"))
            else:
                client.send("[*] sha512 use [*]".encode("utf8"))
            hashedPass = client.recv(4096).decode("utf8")
            storedHash = open("etc/password/password.key", "r").read().strip()

            if hashedPass != storedHash:
                client.send("[!] Authentification incorrect! [!]".encode("utf8"))
                chatBox.configure(state="normal")
                chatBox.insert("end", f"[!] Authentification failed [!]{address[0]}\n")
                chatBox.configure(state="disabled")
                client.close()
                return

            client.send("[*] Authentification successful! [*]".encode("utf8"))
            chatBox.configure(state="normal")
            chatBox.insert("end", f"[*] {address[0]} authenticate succesfuly! [*]\n")
            chatBox.configure(state="disabled")
        else:
            client.send("[!] No Password require [!]".encode("utf8"))

        if os.path.exists("account/username.txt"):
            username = open("account/username.txt", "r").read().strip()
        else:
            username = "Server"
        client.send(username.encode("utf8"))

        publicKey, privateKey = rsa.newkeys(2048)
        client.send(publicKey.save_pkcs1())

        encryptedKey = client.recv(4096)
        decryptedKey = rsa.decrypt(encryptedKey, privateKey)
        f = Fernet(decryptedKey)

        def log(chatBox, msg):
            chatBox.configure(state="normal")
            chatBox.insert("end", msg + "\n")
            chatBox.configure(state="disabled")
            chatBox.see("end")
        def receiveMessage():
            try:
                while True:
                    data = client.recv(10_000_000)
                    if not data:
                        break
                    if data.startswith(b"[TEXT]"):
                        msg = f.decrypt(data[6:]).decode()
                        log(chatBox, f"{address[0]} → {msg}")
                    elif data.startswith(b"[FILE]"):
                        header, encryptedData = data.split(b"::", 1)
                        filename = header[6:].decode()
                        decryptedData = f.decrypt(encryptedData)
                        with open(f"etc/cache/{filename}", "wb") as out:
                            out.write(decryptedData)
                        log(chatBox, f"[*] {filename} received 📥 [*]")
            except Exception as e:
                log(chatBox, f"[!] Receive error from {address[0]}: {e} [!]")
            finally:
                client.close()
                log(chatBox, f"[!] {address[0]} disconnected [!]")
        def sendMessage(event=None):
            msg = entry.get().strip()
            if not msg:
                return
            entry.delete(0, "end")
            if msg.lower() == "bye":
                client.close()
                return
            try:
                client.send(b"[TEXT]" + f.encrypt(msg.encode("utf8")))
                chatBox.configure(state="normal")
                chatBox.insert("end", f"Vous → {msg}\n")
                chatBox.configure(state="disabled")
            except:
                chatBox.configure(state="normal")
                chatBox.insert("end", "[!] Erreur d’envoi. [!]\n")
                chatBox.configure(state="disabled")
        def sendFile():
            file = customtkinter.filedialog.askopenfilename(title="Select a file")
            if not file:
                return
            with open(file, "rb") as File:
                data = File.read()
            fileName = os.path.basename(file)
            header = f"[FILE]{fileName}".encode()
            encryptedData = f.encrypt(data)
            client.send(header + b"::" + encryptedData)
            chatBox.configure(state="normal")
            chatBox.insert("end", f"[*] {fileName} send 📤[*]\n")
            chatBox.configure(state="disabled")
        threading.Thread(target=receiveMessage, daemon=True).start()
        entry.bind("<Return>", sendMessage)

    except Exception as e:
        chatBox.configure(state="normal")
        chatBox.insert("end", f"[!] Error with {address[0]} : {e}\n")
        chatBox.configure(state="disabled")
        client.close()
        entry = customtkinter.CTkEntry(root, placeholder_text="Write Here")
        entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
    
    sendButton = customtkinter.CTkButton(root, text="⌲", command=sendMessage, width=28, height=28)
    sendButton.pack(side="left")
    def clearChat():
        chatBox.configure(state="normal")
        chatBox.delete("0.0", "end")
        chatBox.configure(state="disabled")

    clearButton = customtkinter.CTkButton(root, text="🧹", command=clearChat, width=30, height=28)
    clearButton.pack(side="right")

    fileButton = customtkinter.CTkButton(root, text="📑", width=28, height=28, command=sendFile)
    fileButton.pack(side="left")
    


def server(IP, PORT):
    root = customtkinter.CTk()
    root.title("BigCat - Server")
    root.geometry("400x500")

    chatBox = customtkinter.CTkTextbox(root, width=380, height=400)
    chatBox.pack(pady=10)
    chatBox.insert("end", "[*] Serveur started [*]\n")
    chatBox.configure(state="disabled")

    entry = customtkinter.CTkEntry(root, placeholder_text="Write Here")
    entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind((IP, PORT))
    serverSocket.listen(5)

    def acceptConnections():
        while True:
            try:
                client, address = serverSocket.accept()
                chatBox.configure(state="normal")
                chatBox.insert("end", f"[*] {address[0]} connected [*]\n")
                chatBox.configure(state="disabled")
                threading.Thread(
                    target=handleClient, 
                    args=(client, address, root, chatBox, entry), 
                    daemon=True
                ).start()
            except Exception as e:
                chatBox.configure(state="normal")
                chatBox.insert("end", f"[!] Server error : {e} [!]\n")
                chatBox.configure(state="disabled")
                break
            

    threading.Thread(target=acceptConnections, daemon=True).start()

    root.mainloop()