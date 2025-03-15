from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QLineEdit,
    QPushButton, QLabel, QListWidget, QMessageBox, QFileDialog, QColorDialog, QInputDialog, QMenu, QApplication
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt
from googletrans import Translator  # For translation
import google.generativeai as genai  # For Gemini AI API

class ChatApp(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.dark_mode = False  # Initialize dark_mode attribute
        self.translator = Translator()  # Initialize translator
        self.gemini_model = None  # Initialize Gemini model as None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"Chat Application - {self.username}")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Toggle Light/Dark Mode
        toggle_layout = QHBoxLayout()
        self.toggle_button = QPushButton("Toggle Dark Mode", self)
        self.toggle_button.clicked.connect(self.toggle_theme)
        toggle_layout.addWidget(self.toggle_button)
        layout.addLayout(toggle_layout)

        # Header
        header = QLabel(f"Welcome, {self.username}")
        header.setFont(QFont('Arial', 16, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # Main Content Layout
        main_layout = QHBoxLayout()

        # User List
        self.user_list = QListWidget(self)
        self.user_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.user_list.customContextMenuRequested.connect(self.show_user_context_menu)
        main_layout.addWidget(self.user_list, 1)

        # Chat Layout
        chat_layout = QVBoxLayout()

        # AI Chatbot Button
        self.ai_chatbot_button = QPushButton("Open AI Chatbot", self)
        self.ai_chatbot_button.setStyleSheet("""
            QPushButton {
                background-color: #0078D7;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
        """)
        self.ai_chatbot_button.clicked.connect(self.open_ai_chatbot)
        chat_layout.addWidget(self.ai_chatbot_button)

        # Chat Display
        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
        chat_layout.addWidget(self.chat_display)

        # Message Input Layout
        message_layout = QHBoxLayout()

        self.msg_input = QLineEdit(self)
        self.msg_input.setPlaceholderText("Type your message...")
        message_layout.addWidget(self.msg_input)

        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(self.send_message)
        message_layout.addWidget(self.send_button)

        # Translate Button
        self.translate_button = QPushButton("Translate", self)
        self.translate_button.clicked.connect(self.translate_selected_message)
        self.translate_button.setStyleSheet("""
            QPushButton {
                background-color: #FF6347; /* Tomato Red */
                color: #FFFFFF; /* White text */
                font-weight: bold;
                border-radius: 8px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #FF4500; /* Orange Red */
            }
        """)
        chat_layout.addWidget(self.translate_button)
        chat_layout.addLayout(message_layout)

        # Dropdown Actions Button
        self.actions_button = QPushButton("MORE OPTIONS", self)
        self.actions_menu = QMenu(self)
        self.actions_menu.addAction("Share File", self.share_file)
        self.actions_menu.addAction("Export Chat", self.export_chat)
        self.actions_menu.addAction("Change Chat Background", self.change_chat_display_background)
        self.actions_button.setMenu(self.actions_menu)
        chat_layout.addWidget(self.actions_button)

        main_layout.addLayout(chat_layout, 3)
        layout.addLayout(main_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Apply colorful button styles
        self.apply_button_styles()

        # Configure Gemini AI
        self.configure_gemini_ai()

    def configure_gemini_ai(self):
        """Allow the user to configure the Gemini AI API key and model."""
        api_key, ok = QInputDialog.getText(
            self,
            "Gemini AI Configuration",
            "Enter your Gemini API key:"
        )
        if ok and api_key:
            try:
                genai.configure(api_key=api_key)
                model_type, ok = QInputDialog.getItem(
                    self,
                    "Gemini AI Configuration",
                    "Select the model type:",
                    ["gemini-pro", "gemini-ultra"],  # Add more models if available
                    0,
                    editable=False
                )
                if ok and model_type:
                    self.gemini_model = genai.GenerativeModel(model_type)
                    QMessageBox.information(self, "Success", "Gemini AI configured successfully!")
                else:
                    QMessageBox.warning(self, "Error", "Model type not selected.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to configure Gemini AI: {str(e)}")
        else:
            QMessageBox.warning(self, "Error", "API key not provided.")

    def send_message(self):
        """Handle sending a message."""
        message = self.msg_input.text().strip()
        if message:
            self.chat_display.append(f"{self.username}: {message}")
            self.msg_input.clear()

    def show_user_context_menu(self, position):
        """Show context menu for user actions."""
        menu = QMenu(self)
        menu.addAction("Follow", self.follow_user)
        menu.addAction("Unfollow", self.unfollow_user)
        menu.exec_(self.user_list.viewport().mapToGlobal(position))

    def follow_user(self):
        """Handle following a user."""
        selected_user = self.user_list.currentItem()
        if selected_user:
            username = selected_user.text()
            self.chat_display.append(f"You are now following {username}.")

    def unfollow_user(self):
        """Handle unfollowing a user."""
        selected_user = self.user_list.currentItem()
        if selected_user:
            username = selected_user.text()
            self.chat_display.append(f"You unfollowed {username}.")

    def translate_selected_message(self):
        """Translate the selected message."""
        selected_text = self.chat_display.textCursor().selectedText()
        if selected_text:
            # Provide a list of common languages
            language_options = {
                "English": "en",
                "Spanish": "es",
                "French": "fr",
                "German": "de",
                "Chinese (Simplified)": "zh-cn",
                "Hindi": "hi",
                "Arabic": "ar",
                "Japanese": "ja",
                "Tamil": "ta"
            }
            items = list(language_options.keys())
            choice, ok = QInputDialog.getItem(
                self,
                "Translate",
                "Choose target language:",
                items,
                0,
                editable=False
            )
            if ok and choice:
                target_language = language_options[choice]
                try:
                    translated = self.translator.translate(selected_text, dest=target_language)
                    self.chat_display.append(f"Translated ({choice}): {translated.text}")
                except Exception as e:
                    QMessageBox.critical(self, "Translation Error", f"Error translating message: {str(e)}")
        else:
            QMessageBox.warning(self, "Error", "Please select a message to translate.")

    def open_ai_chatbot(self):
        """Open the AI Chatbot and interact with Gemini AI."""
        if not self.gemini_model:
            QMessageBox.warning(self, "Error", "Gemini AI is not configured. Please configure it first.")
            return

        user_message, ok = QInputDialog.getText(
            self,
            "AI Chatbot",
            "Ask something to the AI Chatbot:"
        )
        if ok and user_message:
            try:
                # Send the user's message to Gemini AI
                response = self.gemini_model.generate_content(user_message)
                self.chat_display.append(f"AI Chatbot: {response.text}")
            except Exception as e:
                QMessageBox.critical(self, "AI Chatbot Error", f"Error communicating with AI Chatbot: {str(e)}")

    def share_file(self):
        """Handle sharing a file."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_path:
            self.chat_display.append(f"File shared: {file_path}")

    def export_chat(self):
        """Handle exporting the chat."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Chat", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.chat_display.toPlainText())
            QMessageBox.information(self, "Export Successful", f"Chat saved to {file_path}")

    def change_chat_display_background(self):
        """Allow the user to select and change the chat display background color or set a single image."""
        try:
            items = ["Color", "Image"]
            choice, ok = QInputDialog.getItem(
                self,
                "Change Chat Background",
                "Choose background type:",
                items,
                0,
                editable=False
            )
            if ok:
                if choice == "Color":
                    color = QColorDialog.getColor()
                    if color.isValid():
                        self.chat_display.setStyleSheet(f"background-color: {color.name()}; color: #000000;")
                elif choice == "Image":
                    file_path, _ = QFileDialog.getOpenFileName(
                        self,
                        "Select Background Image",
                        "",
                        "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.svg *.webp)"
                    )
                    if file_path:
                        self.chat_display.setStyleSheet(
                            f"background-image: url('{file_path}'); background-repeat: no-repeat; "
                            f"background-position: center; background-size: cover; color: #000000;"
                        )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def toggle_theme(self):
        """Toggle between light and dark modes."""
        if self.dark_mode:
            self.set_light_mode()
        else:
            self.set_dark_mode()
        self.dark_mode = not self.dark_mode

    def set_light_mode(self):
        """Set light theme."""
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(255, 255, 255))
        palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
        QApplication.setPalette(palette)

    def set_dark_mode(self):
        """Set dark theme."""
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        QApplication.setPalette(palette)

    def apply_button_styles(self):
        """Apply colorful styles to buttons."""
        button_style = """
        QPushButton {
            background-color: #4682B4;
            border-radius: 8px;
            padding: 5px;
            font-weight: bold;
            color: #FFFFFF;
        }
        QPushButton:hover {
            background-color: #5A9BD4;
        }
        """
        self.actions_button.setStyleSheet(button_style)
        self.send_button.setStyleSheet(button_style)
        self.toggle_button.setStyleSheet(button_style)