from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QTextEdit, QLineEdit, QPushButton, QWidget, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import requests

class GeminiAIChatbotWindow(QMainWindow):
    API_URL = "https://api.gemini.com/v1/chat/completions"
    API_KEY = "AIzaSyBCF_nLHaBPmGDJh5HfoQ-2ypRDvyXzAIU"  # Replace with your actual API key

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gemini AI Chatbot")
        self.setGeometry(200, 200, 700, 600)
        self.init_ui()

    def init_ui(self):
        # Main layout
        layout = QVBoxLayout()

        # Header
        header = QLabel("🤖 Gemini AI Chatbot")
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont("Arial", 18, QFont.Bold))
        header.setStyleSheet("color: #0078D7; margin: 10px;")
        layout.addWidget(header)

        # Chat Display
        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Arial", 12))
        self.chat_display.setStyleSheet("background-color: #f4f4f4; padding: 10px;")
        layout.addWidget(self.chat_display)

        # Input Layout
        input_layout = QHBoxLayout()
        self.msg_input = QLineEdit(self)
        self.msg_input.setPlaceholderText("Ask something to Gemini AI...")
        self.msg_input.setFont(QFont("Arial", 12))
        self.msg_input.setStyleSheet("padding: 10px; border-radius: 5px;")
        input_layout.addWidget(self.msg_input)

        self.send_button = QPushButton("Send", self)
        self.send_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #0078D7;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
        """)
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)

        layout.addLayout(input_layout)

        # Footer
        footer = QLabel("Powered by Gemini AI API")
        footer.setAlignment(Qt.AlignCenter)
        footer.setFont(QFont("Arial", 10))
        footer.setStyleSheet("color: gray; margin: 10px;")
        layout.addWidget(footer)

        # Set central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def send_message(self):
        """Send a message to the AI and get a response."""
        user_message = self.msg_input.text().strip()
        if user_message:
            # Display user's message
            self.chat_display.append(f"You: {user_message}")
            self.msg_input.clear()

            # Get AI response
            ai_response = self.get_ai_response(user_message)
            if ai_response:
                self.chat_display.append(f"Gemini AI: {ai_response}")
            else:
                self.chat_display.append("Gemini AI: Sorry, I couldn't understand that.")

    def get_ai_response(self, user_message):
        """Make a request to the AI API and return its response."""
        headers = {
            "Authorization": f"Bearer {self.API_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "model": "gpt-3.5-turbo",  # Ensure you have access to this model or use another available model
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": user_message},
            ],
        }

        try:
            response = requests.post(self.API_URL, headers=headers, json=data)
            if response.status_code == 200:
                response_json = response.json()
                return response_json["choices"][0]["message"]["content"].strip()
            else:
                self.chat_display.append(f"Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            self.chat_display.append(f"Error: {e}")
            return None