import sys
import threading
from PyQt5.QtWidgets import QApplication
from database import initialize_database
from server import ChatServer
from ui.login_window import LoginWindow

# Server Address and Port
HOST = '192.168.14.190'  # Use 'localhost' for local testing or your machine's IP address
PORT = 1234

def start_server():
    """Start the chat server in a separate thread."""
    try:
        server = ChatServer(HOST, PORT)
        print(f"Server started on {HOST}:{PORT}")
        server.start()
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == '__main__':
    # Initialize the database
    initialize_database()

    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Create the PyQt application
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Use Fusion style for a modern look

    # Create and show the login window
    login_window = LoginWindow()
    login_window.show()

    # Run the application event loop
    sys.exit(app.exec_())