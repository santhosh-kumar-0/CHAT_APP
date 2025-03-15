from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QMessageBox, QHBoxLayout, QFileDialog, 
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

import sqlite3
from ui.chat_window import ChatApp  # Import the ChatApp class

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("CHAT APPLICATION")
        self.setGeometry(100, 100, 400, 300)

        self.setWindowIcon(QIcon("logo.ico"))

        layout = QVBoxLayout()

        # Application Logo
        self.logo_label = QLabel(self)
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.load_logo("logo.png")  # Try to load the default logo
        layout.addWidget(self.logo_label)

       
        # Header
        header = QLabel("Welcome to Chat App", self)
        header.setFont(QFont('Arial', 16, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # Username
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Enter Username")
        self.username_input.setFixedHeight(40)
        layout.addWidget(self.username_input)

        # Password
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setFixedHeight(40)
        layout.addWidget(self.password_input)

        # Buttons
        btn_layout = QHBoxLayout()

        # Login Button
        self.login_button = QPushButton("Login", self)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;  /* Green */
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.login_button.clicked.connect(self.login_user)  # Connect to login_user method
        btn_layout.addWidget(self.login_button)

        # Register Button
        self.register_button = QPushButton("Register", self)
        self.register_button.setStyleSheet("""
            QPushButton {
                background-color: #008CBA;  /* Blue */
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #007bb5;
            }
        """)
        self.register_button.clicked.connect(self.register_user)  # Connect to register_user method
        btn_layout.addWidget(self.register_button)

        layout.addLayout(btn_layout)

        # Set central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_logo(self, logo_path):
        """Load the logo from the specified path."""
        try:
            pixmap = QPixmap(logo_path)
            if pixmap.isNull():
                raise FileNotFoundError
            pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio)
            self.logo_label.setPixmap(pixmap)
        except Exception as e:
            print(f"Warning: Could not load logo. Error: {e}")
            # Set a default text if the logo is missing
            self.logo_label.setText("Logo Not Found")
            self.logo_label.setFont(QFont('Arial', 12))

    
    def login_user(self):
        """Handle user login."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Login Failed", "Username and password cannot be empty.")
            return

        conn = sqlite3.connect("chat_app.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.open_chat_window(username)  # Open the chat window
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

    def register_user(self):
        """Handle user registration."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Registration Failed", "Username and password cannot be empty.")
            return

        conn = sqlite3.connect("chat_app.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            QMessageBox.information(self, "Registration Successful", "You can now log in.")
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Registration Failed", "Username already exists.")
        conn.close()

    def open_chat_window(self, username):
        """Open the chat window and close the login window."""
        self.chat_window = ChatApp(username)  # Create the chat window
        self.chat_window.show()  # Show the chat window
        self.close()  # Close the login window