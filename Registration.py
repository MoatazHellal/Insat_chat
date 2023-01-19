import re
import secrets
import sqlite3
import hashlib
import string
import tkinter as tk
from User import User
from getpass import getpass


class Registration:
    def __init__(self):
        self.connection = sqlite3.connect("ChatroomDB.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='User';")
        if (self.cursor.fetchall() == []):
            self.cursor.execute(
                "CREATE TABLE User(FirstName VARCHAR2, LastName VARCHAR2 , Pseudo VARCHAR2, NCard INT, Password VARCHAR2, token VARCHAR2)")

    def register(self):

        user = User()
        firstName_input = first_name_entry.get()
        lastName_input = last_name_entry.get()
        pseudo_input = pseudo_entry.get()
        nCard_input = nCard_entry.get()
        pwd_input = pwd_entry.get()
        if (self.verify_name(firstName_input) and self.verify_pwd(pwd_input) and not self.verify_user(pseudo_input, nCard_input)):
            user.setFirstName(firstName_input)
            user.setLastName(lastName_input)
            user.setPseudo(pseudo_input)
            user.setNCard(nCard_input)
            user.setPassword(hashlib.sha256(pwd_input.encode()).hexdigest())
            token = self.generate_token()
            user.setToken(token)
            with open("token.txt", 'a') as f:
                f.write(''+user.firstName+' ' +
                        user.lastName+': '+user.token+"\n")
            self.saveBD(user)
            root.destroy()
            return user
        if (not self.verify_name(firstName_input) and not firstName_input == ""):
            invalid_first_name_label = tk.Label(root, text="Invalid Name")
            invalid_first_name_label.grid(row=0, column=5)
            return None
        if (not self.verify_pwd(pwd_input)):
            invalid_pwd_label = tk.Label(
                root, text="Weak Password" and not pwd_input == "")
            invalid_pwd_label.grid(row=3, column=5)
            return None
        if (self.verify_user(pseudo_input, nCard_input)):
            invalid_pseudo_label = tk.Label(root, text="User Already exists")
            invalid_pseudo_label.grid(row=2, column=5)
            return None
        else:
            invalid_inputs = tk.Label(root, text="Please fill all fields")
            invalid_inputs.grid(row=6, column=1)
            return None

        # user_exists = self.verify_user(pseudo_input)

        # # while (user_exists):
        # #     print("Pseudo already exists.")
        # #     pseudo_input = input("Reenter your pseudo:\n> ")
        # #     user_exists = self.verify_user(
        # #         pseudo_input)
        # user.setPseudo(pseudo_input)
        # firstName_input = first_name_entry.get()
        # while (not self.verify_name(firstName_input)):
        #     invalid_first_name_label.grid()
        #     firstName_input = input("Reenter your first name:\n> ")
        # user.setFirstName(firstName_input)
        # lastName_input = last_name_entry.get()
        # while (not self.verify_name(lastName_input)):
        #     print("Invalid last name.")
        #     lastName_input = input("Entrer votre nom de nouveau:\n> ")
        # user.setLastName(lastName_input)
        # pwd_input = 'none'
        # pwdVerif_input = 'noneVerif'
        # # while (pwd_input != pwdVerif_input):
        # #     pwd_input = pwd_entry.get()
        # #     while (not self.verify_pwd(pwd_input)):
        # #         invalid_pwd_label.grid(row=3, column=3)
        # #         pwd_input = pwd_entry.get()
        # #     pwdVerif_input = pwd_entry.get()
        # #     if (pwd_input != pwdVerif_input):
        # #         print("Verification eronnee.")

        # password = hashlib.sha256(pwd_input.encode()).hexdigest()
        # user.setPassword(password)
        # token = self.generate_token()
        # user.setToken(token)
        # print()
        # print("Le token associé à ce compte est: ", user.token)
        # token_path = input(
        #     "Donner le path du fichier pour sauvegarder le token:\n> ")
        # with open(token_path, 'a') as f:
        #     f.write(''+user.firstName+' ' +
        #             user.lastName+': '+user.token+"\n")
        # self.saveBD(user)
        # root.destroy()
        # return True, user

    def verify_name(self, name):
        regex = re.compile(r'^[a-zA-Z]+$')
        return re.fullmatch(regex, name)

    def verify_pwd(self, pwd):
        regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$')
        return re.fullmatch(regex, pwd)

    def verify_user(self, pseudo, nCard):
        self.cursor.execute(
            'SELECT * FROM user WHERE pseudo=? AND nCard=?', (pseudo, nCard,))
        return self.cursor.fetchall() != []

    def saveBD(self, user: User):
        sql_query = 'INSERT INTO user VALUES(?,?,?,?,?,?);'
        user_insertion = (
            user.firstName,
            user.lastName,
            user.pseudo,
            user.nCard,
            user.password,
            user.token
        )
        self.cursor.execute(sql_query, user_insertion)
        self.connection.commit()

    def generate_token(self):
        num = 8
        token = ''.join(secrets.choice(string.ascii_letters +
                                       string.digits) for x in range(num))
        return token

    def on_click(self):
        global result
        result = self.register()

    def registerForm(self):
        global root
        root = tk.Tk()
        root.geometry("600x450")
        root.title("My Form")

        first_name_label = tk.Label(root, text="First Name:")
        first_name_label.grid(row=0, column=0)

        global first_name_entry
        first_name_entry = tk.Entry(root)
        first_name_entry.grid(row=0, column=1)

        last_name_label = tk.Label(root, text="Last Name:")
        last_name_label.grid(row=1, column=0)

        global last_name_entry
        last_name_entry = tk.Entry(root)
        last_name_entry.grid(row=1, column=1)

        pseudo_label = tk.Label(root, text="Pseudo:")
        pseudo_label.grid(row=2, column=0)

        global pseudo_entry
        pseudo_entry = tk.Entry(root)
        pseudo_entry.grid(row=2, column=1)

        nCard_label = tk.Label(root, text="Card Number:")
        nCard_label.grid(row=3, column=0)

        global nCard_entry
        nCard_entry = tk.Entry(root)
        nCard_entry.grid(row=3, column=1)

        pwd_label = tk.Label(root, text="Password:")
        pwd_label.grid(row=4, column=0)

        global pwd_entry
        pwd_entry = tk.Entry(root, show="*")
        pwd_entry.grid(row=4, column=1)

        submit_button = tk.Button(root, text="Submit", command=self.on_click)
        submit_button.grid(row=7, column=1)
        root.mainloop()
        return result
