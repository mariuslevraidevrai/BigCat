import os
import hashlib
import customtkinter

def submit(username,password):
    with open("account/username.txt", "w+") as usernameFile:
        usernameFile.write(username)
    password = password.encode("utf8")
    passwordHash = hashlib.sha256(password)
    passwordHex = passwordHash.hexdigest()
    with open("account/password.key", "w+") as passwordFile:
        passwordFile.write(passwordHex)
    quit()    
def register():
    root = customtkinter.CTk()
    root.title("BigCat - Register")
    root.minsize(400, 500)
    label = customtkinter.CTkLabel(root, text="Register you on BigCat")
    label.pack()
    usernameLabel = customtkinter.CTkLabel(root, text="Username")
    usernameLabel.pack()
    username = customtkinter.CTkEntry(root)
    username.pack()
    passwordLabel = customtkinter.CTkLabel(root, text="Password")
    passwordLabel.pack()
    password = customtkinter.CTkEntry(root)
    password.pack()
    submitButton = customtkinter.CTkButton(
        root, 
        text="Submit", 
        command=lambda: submit(username.get(), password.get())
    )
    submitButton.pack()
    root.mainloop()