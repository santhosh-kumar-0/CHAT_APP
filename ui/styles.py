def apply_button_styles(button):
    button.setStyleSheet("""
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
    """)