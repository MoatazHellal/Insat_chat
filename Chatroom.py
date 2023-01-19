from server import initialize_and_start_server
from client import initialize_and_start_client
from User import User
import tkinter as tk
from tkinter import *


def start_client():
    r.destroy()
    initialize_and_start_client(username)


def start_server():
    r.destroy()
    initialize_and_start_server()


def chatroom_menu(user: User):
    global r
    r = tk.Tk()
    r.geometry("600x450")
    bgimg = tk.PhotoImage(file="chat-box.png")
    limg = Label(r, i=bgimg)
    limg.pack()
    r.title("chatroom")
    RegisterButton = tk.Button(
        r, text='Execute As Server', width=25, command=start_server)
    RegisterButton.pack()
    global username
    username = ''+user.firstName + ' '+user.lastName
    LoginButton = tk.Button(r, text='Execute As Client',
                            width=25, command=start_client)
    LoginButton.pack()
    r.mainloop()
    # choice = ''
    # while (choice != '3'):
    #     print("---------------Menu Chatroom--------------")
    #     print("1- Executer autant que server")
    #     print("2- Executer autant que client")
    #     print("3- Revenir au menu principal")
    #     print("-------------------------------------------")
    #     choix = input("Donner le numero du choix:\n> ")
    #     if (choix == '1'):
    #         initialize_and_start_server()
    #     if (choix == '2'):
    #         userPseudo = user.pseudo
    #         initialize_and_start_client(userPseudo)
    #     if (choix == '3'):
    #         break
