from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QLineEdit,
    QPushButton, QLabel, QListWidget, QMessageBox, QFileDialog, QColorDialog, QInputDialog, QMenu, QApplication, 
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QSize
from googletrans import Translator  # For translation
import google.generativeai as genai

class ChatApp(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.dark_mode = False
        self.translator = Translator()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"Chat Application - {self.username}")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("logo.ico"))

        layout = QVBoxLayout()

        # Toggle Light/Dark Mode
        self.toggle_button = QPushButton(self)
        self.toggle_button.setIcon(QIcon("shutter_light_mode.png"))  # Replace with the shutter light mode icon
        self.toggle_button.setIconSize(QSize(100,100))
        self.toggle_button.setFixedSize(100,35)  # Small square button
        self.toggle_button.setStyleSheet("border: none;")  # Remove background and border
        self.toggle_button.clicked.connect(self.toggle_theme)

        header_layout = QHBoxLayout()
        header_layout.addStretch()  # Push the toggle button to the far right
        header_layout.addWidget(self.toggle_button)  # Add the toggle button
        layout.addLayout(header_layout)  # Add the header layout to the main layout

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

        # Logout Button
        self.logout_button = QPushButton("Logout", self)
        self.logout_button.setStyleSheet(self.get_colorful_button_style("#FF4500", "#FF6347"))
        self.logout_button.clicked.connect(self.logout)
        chat_layout.addWidget(self.logout_button)

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
        self.translate_button.setStyleSheet(self.get_colorful_button_style("#4682B4", "#5A9BD4"))
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

        # Apply colorful styles
        self.apply_button_styles()

    def get_colorful_button_style(self, base_color, hover_color):
        """Return a dynamic colorful style for buttons."""
        return f"""
        QPushButton {{
            background-color: {base_color};
            border-radius: 8px;
            padding: 5px;
            font-weight: bold;
            color: #FFFFFF;
        }}
        QPushButton:hover {{
            background-color: {hover_color};
        }}
        """

    def apply_button_styles(self):
        """Apply colorful styles to buttons."""
        colorful_style = self.get_colorful_button_style("#4682B4", "#5A9BD4")
        self.send_button.setStyleSheet(colorful_style)
        self.toggle_button.setStyleSheet(colorful_style)

    def logout(self):
        QMessageBox.information(self, "Logout", "You have been logged out.")
        self.close()

    def send_message(self):
        message = self.msg_input.text().strip()
        if message:
            self.chat_display.append(f"{self.username}: {message}")
            self.msg_input.clear()

    def show_user_context_menu(self, position):
        menu = QMenu(self)
        menu.addAction("Follow", self.follow_user)
        menu.addAction("Unfollow", self.unfollow_user)
        menu.exec_(self.user_list.viewport().mapToGlobal(position))

    def follow_user(self):
        selected_user = self.user_list.currentItem()
        if selected_user:
            username = selected_user.text()
            self.chat_display.append(f"You are now following {username}.")

    def unfollow_user(self):
        selected_user = self.user_list.currentItem()
        if selected_user:
            username = selected_user.text()
            self.chat_display.append(f"You unfollowed {username}.")

    def translate_selected_message(self):
        selected_text = self.chat_display.textCursor().selectedText()
        if selected_text:
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
            choice, ok = QInputDialog.getItem(self, "Translate", "Choose target language:", items, 0, editable=False)
            if ok and choice:
                target_language = language_options[choice]
                try:
                    translated = self.translator.translate(selected_text, dest=target_language)
                    self.chat_display.append(f"Translated ({choice}): {translated.text}")
                except Exception as e:
                    QMessageBox.critical(self, "Translation Error", f"Error translating message: {str(e)}")
        else:
            QMessageBox.warning(self, "Error", "Please select a message to translate.")

    def share_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_path:
            self.chat_display.append(f"File shared: {file_path}")

    def export_chat(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Chat", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.chat_display.toPlainText())
            QMessageBox.information(self, "Export Successful", f"Chat saved to {file_path}")

    def change_chat_display_background(self):
        items = ["Color", "Image"]
        choice, ok = QInputDialog.getItem(self, "Change Chat Background", "Choose background type:", items, 0, editable=False)
        if ok:
            if choice == "Color":
                color = QColorDialog.getColor()
                if color.isValid():
                    self.chat_display.setStyleSheet(f"background-color: {color.name()}; color: #000000;")
            elif choice == "Image":
                file_path, _ = QFileDialog.getOpenFileName(self, "Select Background Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.svg *.webp)")
                if file_path:
                    self.chat_display.setStyleSheet(f"background-image: url('{file_path}'); background-repeat: no-repeat; background-position: center; background-size: cover; color: #000000;")

    def toggle_theme(self):
        """Toggle between light and dark themes with shutter-style icons."""
        if self.dark_mode:
            self.set_light_mode()
            self.toggle_button.setIcon(QIcon("shutter_light_mode.png"))  # Replace with the light mode shutter icon
        else:
            self.set_dark_mode()
            self.toggle_button.setIcon(QIcon("shutter_dark_mode.png"))  # Replace with the dark mode shutter icon
        self.dark_mode = not self.dark_mode

    def set_light_mode(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(255, 255, 255))
        palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
        QApplication.setPalette(palette)

    def set_dark_mode(self):
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