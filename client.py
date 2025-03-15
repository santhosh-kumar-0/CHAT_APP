import socket
import sqlite3
from PyQt5.QtWidgets import QMessageBox
from ui.login_window import LoginWindow
from ui.chat_window import ChatApp
from encryption import encrypt_message, decrypt_message

# Server Address and Port
HOST = '192.168.39.187'
PORT = 5000

class Client:
    def __init__(self, username):
        self.username = username
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_connected = False

    def connect_to_server(self):
        try:
            self.socket.connect((HOST, PORT))
            self.socket.sendall(self.username.encode())
            self.is_connected = True
        except Exception as e:
            QMessageBox.warning(None, "Connection Failed", str(e))

    def send_message(self, recipient, message):
        if self.is_connected:
            try:
                encrypted_message = encrypt_message(message)
                full_message = f"{self.username}|{recipient}|{encrypted_message}"
                self.socket.sendall(full_message.encode())
            except Exception as e:
                QMessageBox.warning(None, "Error", f"Failed to send message: {e}")

    def receive_messages(self):
        while self.is_connected:
            try:
                data = self.socket.recv(1024).decode()
                if data:
                    return data  # Decrypted message is handled in the UI
            except Exception as e:
                QMessageBox.warning(None, "Error", f"Connection lost: {e}")
                break