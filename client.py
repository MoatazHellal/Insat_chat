import os
import datetime
import socket
import json
import threading
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


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
            print(e.__str__())

        self.s.send(self.username.encode())
        print(' Successfully Connected')

        self.create_key_pairs()
        self.exchange_public_keys()
        global secret_key
        secret_key = self.handle_secret()

        print(' Start chatting !')

        message_handler = threading.Thread(
            target=self.handle_messages, args=())
        message_handler.start()
        input_handler = threading.Thread(target=self.input_handler, args=())
        input_handler.start()
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
                current_time = datetime.datetime.now()
                print(msg.decode())
            else:
                print('lost connection', 'red')
                self.s.shutdown(socket.SHUT_RDWR)
                self.isStopped = True

    def input_handler(self):
        while True:
            message = input('> ')
            if message == "Quit":
                break
            else:
                key = secret_key
                cipher = AES.new(key, AES.MODE_CFB)
                message_to_encrypt = self.username + ": " + message
                msgBytes = message_to_encrypt.encode()
                encrypted_message = cipher.encrypt(msgBytes)
                iv = b64encode(cipher.iv).decode('utf-8')
                message = b64encode(encrypted_message).decode('utf-8')
                result = json.dumps({'iv': iv, 'ciphertext': message})
                self.s.send(result.encode())

        self.s.shutdown(socket.SHUT_RDWR)
        self.isStopped = True

    def handle_secret(self):
        secret_key = self.s.recv(1024)
        private_key = RSA.importKey(
            open(f'chatroom_keys/{self.username}_private_key.pem', 'r').read())
        cipher = PKCS1_OAEP.new(private_key)
        return cipher.decrypt(secret_key)

    def exchange_public_keys(self):
        try:
            print(' public key received ')
            server_public_key = self.s.recv(1024).decode()
            server_public_key = RSA.importKey(server_public_key)

            print(' public key sent ... ')
            public_pem_key = RSA.importKey(
                open(f'chatroom_keys/{self.username}_public_key.pem', 'r').read())
            self.s.send(public_pem_key.exportKey())
            print((' exchange done !'))

        except Exception as e:
            print(
                ('there was an issue ...  ' + str(e)))

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
            print(
                'there was an issue  ' + e.__str__())


def initialize_and_start_client(username):
    client = Client('127.0.0.1', 8081, username)
    client.create_connection()
