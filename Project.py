import tkinter as tk
from Chatroom import chatroom_menu
from Registration import Registration
from Authentification import Authentification
from tkinter import *


def register():
    r.destroy()
    registration = Registration()
    user = registration.registerForm()
    chatroom_menu(user)


def login():
    r.destroy()
    authentification = Authentification()
    user = authentification.loginForm()
    chatroom_menu(user)


def main():
    global r
    r = tk.Tk()
    r.geometry("600x450")
    bgimg = tk.PhotoImage(file="chat-box.png")
    limg = Label(r, i=bgimg)
    limg.pack()
    r.title("chatroom")
    RegisterButton = tk.Button(
        r, text='register', width=25, command=register)
    RegisterButton.pack()
    LoginButton = tk.Button(r, text='Login', width=25, command=login)
    LoginButton.pack()
    r.mainloop()


if __name__ == "__main__":
    main()
