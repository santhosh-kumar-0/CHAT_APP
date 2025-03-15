import socket
import threading
import sqlite3
from encryption import encrypt_message, decrypt_message

class ChatServer:
    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        print(f"Server started on {host}:{port}")
        self.clients = {}  # Map client sockets to usernames

    def can_send_message(self, sender, recipient):
        conn = sqlite3.connect("chat_app.db")
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM followers WHERE follower = ? AND followed = ?", (sender, recipient))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    def broadcast(self, message, sender_username, recipient_username):
        if not self.can_send_message(sender_username, recipient_username):
            print(f"Message blocked: {sender_username} does not follow {recipient_username}.")
            return

        recipient_socket = None
        for client_socket, username in self.clients.items():
            if username == recipient_username:
                recipient_socket = client_socket
                break

        if recipient_socket:
            try:
                recipient_socket.sendall(f"{sender_username}: {message}".encode())
            except Exception as e:
                print(f"Error sending message to {recipient_username}: {e}")
        else:
            print(f"Recipient {recipient_username} is not online.")

    def handle_client(self, client_socket):
        try:
            username = client_socket.recv(1024).decode()
            self.clients[client_socket] = username
            print(f"New connection: {username}")

            for sock, uname in self.clients.items():
                if sock != client_socket:
                    try:
                        sock.sendall(f"SERVER: {username} has joined the chat.".encode())
                    except Exception as e:
                        print(f"Error notifying user {uname}: {e}")

            while True:
                data = client_socket.recv(1024).decode()
                if not data:
                    break

                if data.startswith("FILE|"):
                    parts = data.split("|", 4)
                    sender, recipient, file_name = parts[1], parts[2], parts[3]
                    if self.can_send_message(sender, recipient):
                        file_data = client_socket.recv(4096)
                        with open(f"received_{file_name}", "wb") as file:
                            file.write(file_data)
                        print(f"File {file_name} received from {sender}.")
                else:
                    sender, recipient, message = data.split('|', 2)
                    decrypted_message = decrypt_message(message)
                    self.save_message(sender, recipient, decrypted_message)
                    self.broadcast(decrypted_message, sender, recipient)
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            username = self.clients.get(client_socket, "Unknown")
            del self.clients[client_socket]
            client_socket.close()
            print(f"{username} disconnected.")

    def save_message(self, sender, recipient, message):
        conn = sqlite3.connect("chat_app.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (sender, recipient, message) VALUES (?, ?, ?)", (sender, recipient, message))
        conn.commit()
        conn.close()

    def start(self):
        while True:
            client_socket, _ = self.server.accept()
            threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()