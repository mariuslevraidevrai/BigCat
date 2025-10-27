import os
import hashlib
import customtkinter

def submit(password):
    sha256 = hashlib.sha256()
    password_bytes = password.encode("utf8")
    passwordHex = hashlib.sha256(password_bytes).hexdigest()
    if passwordHex == open("account/password.key", "r").read():
        os.system("touch account/valid")
    else:
        quit()
def login():
    if os.path.exists("account/valid"):
        pass
    else:
        root = customtkinter.CTk()
        root.title("BigCat - login")
        root.minsize(400, 500)
        label = customtkinter.CTkLabel(root, text="Login you on BigCat")
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
            command=lambda: submit(password.get())
        )
        submitButton.pack()
        root.mainloop()