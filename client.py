import os
import datetime
import json
import socket
import threading

from termcolor import colored
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64encode, b64decode
import tkinter as tk
from tkinter import *


class Client:
    def __init__(self, server, port, username):
        self.server = server
        self.port = port
        self.username = username
        self.isStopped = False

    def create_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.server, self.port))
        except Exception as e:
            print(colored('[!] ' + e.__str__(), 'red'))

        self.s.send(self.username.encode())
        global connection_label
        connection_label = tk.Label(
            r, text="Connected Successfully")
        connection_label.grid(row=0, column=1)
        global exchange_label
        exchange_label = tk.Label(
            r, text="Keys exchange")
        exchange_label.grid(row=1, column=1)
        # print(colored('[+] Connected successfully!', 'green'))
        # print(colored('[+] Keys exchange', 'yellow'))

        self.create_key_pairs()
        self.exchange_public_keys()
        global secret_key
        secret_key = self.handle_secret()
        global initiation_label
        initiation_label = tk.Label(
            r, text="Initiation complete")
        initiation_label.grid(row=2, column=1)
        message_label = tk.Label(
            r, text="Message exchanged successfully")
        message_label.grid(row=3, column=1)
        # print(colored('[+] Initiation complete', 'green'))
        # print(colored('[+] Messages exchanged successfully', 'green'))
        message_handler = threading.Thread(
            target=self.handle_messages, args=())
        message_handler.start()
        # input_handler = threading.Thread(target=self.input_handler, args=())
        # input_handler.start()
        send_button = tk.Button(
            r, text="Send", command=self.input_handler)
        send_button.place(x=260, y=406)
        while not self.isStopped:
            continue

    def handle_messages(self):
        while not self.isStopped:
            message = self.s.recv(1024).decode()
            if message:
                key = secret_key
                decrypt_message = json.loads(message)
                iv = b64decode(decrypt_message['iv'])
                cipherText = b64decode(decrypt_message['ciphertext'])
                cipher = AES.new(key, AES.MODE_CFB, iv=iv)
                msg = cipher.decrypt(cipherText)
                # current_time = datetime.datetime.now()
                # print(colored(current_time.strftime(
                #     '%Y-%m-%d %H:%M:%S ') + msg.decode(), 'green'))
                # message_label = tk.Label(
                #     r, text=msg.decode())
                # message_label.grid(row=4, column=1)
                # message_label.update()
                label.config(text=msg)
                label.update()
            else:
                print(colored('[!] Connection to server failed', 'red'))
                print(colored('[!] Connection closed', 'red'))
                self.s.shutdown(socket.SHUT_RDWR)
                self.isStopped = True

    def input_handler(self):
        # while True:
        #     message = chat_entry.get()
        #     if message == "EXIT":
        #         break
        #     else:
        message = chat_entry.get()
        key = secret_key
        cipher = AES.new(key, AES.MODE_CFB)
        message_to_encrypt = self.username + ": " + message
        msgBytes = message_to_encrypt.encode()
        encrypted_message = cipher.encrypt(msgBytes)
        iv = b64encode(cipher.iv).decode('utf-8')
        message = b64encode(encrypted_message).decode('utf-8')
        result = json.dumps({'iv': iv, 'ciphertext': message})
        self.s.send(result.encode())

        # self.s.shutdown(socket.SHUT_RDWR)
        # self.isStopped = True

    def handle_secret(self):
        secret_key = self.s.recv(1024)
        private_key = RSA.importKey(
            open(f'chatroom_keys/{self.username}_private_key.pem', 'r').read())
        cipher = PKCS1_OAEP.new(private_key)
        return cipher.decrypt(secret_key)

    def exchange_public_keys(self):
        try:
            global rcvPubK_label
            rcvPubK_label = tk.Label(
                r, text="Receive server public key")
            rcvPubK_label.grid(row=4, column=1)
            server_public_key = self.s.recv(1024).decode()
            server_public_key = RSA.importKey(server_public_key)

            global sndPubK_label
            sndPubK_label = tk.Label(
                r, text="sending public key to server")
            sndPubK_label.grid(row=5, column=1)
            public_pem_key = RSA.importKey(
                open(f'chatroom_keys/{self.username}_public_key.pem', 'r').read())
            self.s.send(public_pem_key.exportKey())
            global complete_label
            complete_label = tk.Label(
                r, text="Exchange completed successfully")
            complete_label.grid(row=6, column=1)
            label1 = tk.Label(
                r, text="amani : hello")
            label1.grid(row=7, column=1)
            label2 = tk.Label(
                r, text="marco : hi")
            label2.grid(row=8, column=1)

        except Exception as e:
            print(str(e))

    def create_key_pairs(self):
        try:
            private_key = RSA.generate(2048)
            public_key = private_key.publickey()
            private_pem = private_key.exportKey().decode()
            public_pem = public_key.exportKey().decode()
            with open(f'chatroom_keys/{self.username}_private_key.pem', 'w') as priv:
                priv.write(private_pem)
            with open(f'chatroom_keys/{self.username}_public_key.pem', 'w') as pub:
                pub.write(public_pem)

        except Exception as e:
            print(str(e))


def start_UI():
    global r
    r = tk.Tk()
    r.geometry("600x450")
    global chat_entry
    chat_entry = tk.Entry(r)
    chat_entry.place(x=5, y=410)
    chat_entry.config(width=40)
    global label
    label = tk.Label(r)
    r.mainloop()


def initialize_and_start_client(username):
    gui_thread = threading.Thread(target=start_UI)
    gui_thread.start()
    client = Client('127.0.0.1', 8081, username)
    client.create_connection()
