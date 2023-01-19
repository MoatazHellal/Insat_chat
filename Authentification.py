from getpass import getpass
import hashlib
import sqlite3
from tabnanny import check
from User import User
import tkinter as tk


class Authentification:
    def __init__(self):
        self.connection = sqlite3.connect("ChatroomDB.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='User';")
        if (self.cursor.fetchone()[0] != 'User'):
            print("Cannot find account !")
            exit()

    def authentify(self):
        user = User()
        pseudo_input = pseudo_entry.get()
        pwd_input = pwd_entry.get()
        user.setPseudo(pseudo_input)
        user.setPassword(hashlib.sha256(pwd_input.encode()).hexdigest())
        user = self.find_user(user)
        if (not user == None):
            root.destroy()
            return user

        # tests = 0
        # pseudo_input = ''
        # pwd_input = ''
        # credentials_valid = False
        # while (not credentials_valid and tests < 3):
        #     pseudo_input = input("Enter your pseudo:\n> ")
        #     while (not (pseudo_input)):
        #         print("Invalid pseudo.")
        #         pseudo_input = input("Retry entering your pseudo:\n> ")
        #     # user.setEmail(pseudo_input)
        #     user.setPseudo(pseudo_input)
        #     pwd_input = getpass("Entrer votre mot de passe:\n> ")
        #     password = hashlib.sha256(pwd_input.encode()).hexdigest()
        #     user.setPassword(password)
        #     tests += 1
        #     credentials_valid, user = self.find_user(
        #         user)
        # return credentials_valid or tests == 3, user

    def find_user(self, user: User):
        sql_query = 'SELECT * FROM User WHERE pseudo=? and password=?;'
        user_search = (
            user.pseudo,
            user.password
        )
        self.cursor.execute(sql_query, user_search)
        if (self.cursor.fetchall() == []):
            invalid_label = tk.Label(root, text="Invalid Credentials")
            invalid_label.grid(row=3, column=1)
            return None
        token = token_entry.get()
        if (not self.verify_token(token, user.pseudo)):
            invalid_label = tk.Label(root, text="Invalid Credentials")
            invalid_label.grid(row=3, column=1)
            return None

        self.cursor.execute(sql_query, user_search)
        user_found = self.cursor.fetchone()
        user.setFirstName(user_found[0])
        user.setLastName(user_found[1])
        return user

    def verify_token(self, token, pseudo):
        sql_query = 'SELECT * FROM User WHERE token=? and pseudo=?'
        self.cursor.execute(sql_query, (token, pseudo,))
        return self.cursor.fetchall() != []

    def on_click(self):
        global result
        result = self.authentify()

    def loginForm(self):
        global root
        root = tk.Tk()
        root.geometry("600x450")
        root.title("My Form")

        pseudo_label = tk.Label(root, text="Pseudo:")
        pseudo_label.grid(row=0, column=0)

        global pseudo_entry
        pseudo_entry = tk.Entry(root)
        pseudo_entry.grid(row=0, column=1)

        pwd_label = tk.Label(root, text="Password:")
        pwd_label.grid(row=1, column=0)

        global pwd_entry
        pwd_entry = tk.Entry(root, show="*")
        pwd_entry.grid(row=1, column=1)

        token_label = tk.Label(root, text="Token:")
        token_label.grid(row=2, column=0)

        global token_entry
        token_entry = tk.Entry(root)
        token_entry.grid(row=2, column=1)

        submit_button = tk.Button(root, text="Submit", command=self.on_click)
        submit_button.grid(row=4, column=1)
        root.mainloop()
        return result
