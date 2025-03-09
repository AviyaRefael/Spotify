import json
import socket
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class RegistrationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(("localhost", 12345))

        self.init_ui()

    def init_ui(self):
        # Window setup
        self.setWindowTitle("Spotify Register")
        self.setFixedSize(400, 500)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Logo or Title
        logo_label = QLabel("Spotify")
        logo_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Name input
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Full Name")
        self.name_input.setFixedHeight(40)

        # Email input
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email address")
        self.email_input.setFixedHeight(40)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(40)

        # Re-enter password input
        self.re_password_input = QLineEdit()
        self.re_password_input.setPlaceholderText("Re-enter Password")
        self.re_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.re_password_input.setFixedHeight(40)

        # Register button
        register_button = QPushButton("REGISTER")
        register_button.setFixedHeight(40)
        register_button.setStyleSheet("""
            background-color: #1DB954;
            color: white;
            border: none;
            border-radius: 20px;
            font-size: 16px;
        """)
        register_button.clicked.connect(self.handle_register)

        # Add widgets to the layout
        main_layout.addWidget(logo_label)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.name_input)
        main_layout.addWidget(self.email_input)
        main_layout.addWidget(self.password_input)
        main_layout.addWidget(self.re_password_input)
        main_layout.addSpacing(20)
        main_layout.addWidget(register_button)

        # Set layout to the window
        self.setLayout(main_layout)

    def handle_register(self):
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        re_password = self.re_password_input.text().strip()

        if not name or not email or not password or not re_password:
            QMessageBox.warning(self, "Input Error", "All fields must be filled!")
            return

        if password != re_password:
            QMessageBox.warning(self, "Input Error", "Passwords do not match!")
            return

        # Create JSON request
        register_request = {
            "type": "register",
            "name": name,
            "mail": email,
            "password": password
        }

        try:
            self.client.send((json.dumps(register_request) + "END_OF_MSG").encode())
            response = self.client.recv(1024).decode().replace("END_OF_MSG", "")
            response_json = json.loads(response)

            if response_json["status"] == "success":
                QMessageBox.information(self, "Success", "Registration Successful!")
                self.close()
            else:
                QMessageBox.critical(self, "Registration Failed", response_json["message"])

        except Exception as e:
            QMessageBox.critical(self, "Connection Error", f"Failed to send data to server: {e}")
