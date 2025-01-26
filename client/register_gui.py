import json
import socket

from PyQt5.QtWidgets import QMainWindow
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import sys


class RegistrationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(("localhost", 12345))
        self.init_ui()

    def init_ui(self):
        # Window setup
        self.setWindowTitle("Register")
        self.setFixedSize(400, 400)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Username input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter Username")
        self.username_input.setFixedHeight(40)

        # Email input
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter Email")
        self.email_input.setFixedHeight(40)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(40)
        self.password_input.setText("123456")

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
        register_button.clicked.connect(self.handle_register)  # Connect button click to the handler

        # Add widgets to the layout
        main_layout.addWidget(self.username_input)
        main_layout.addWidget(self.email_input)
        main_layout.addWidget(self.password_input)
        main_layout.addWidget(register_button)

        # Set layout to the window
        self.setLayout(main_layout)

    def handle_register(self):
        # Retrieve user input
        name = self.username_input.text().strip()
        mail = self.email_input.text().strip()
        password = self.password_input.text().strip()

        # Check if fields are not empty
        if not name or not mail or not password:
            QMessageBox.warning(self, "Input Error", "All fields are required!")
            return

        # Create a JSON object for the login request
        register_request = {
            "type": "register",
            "name":name,
            "mail": mail,
            "password": password
        }

        try:
            # Convert the JSON object to a string and send it to the server
            self.client.send((json.dumps(register_request) + "END_OF_MSG").encode())
        except Exception as e:
            QMessageBox.critical(self, "Connection Error", f"Failed to send data to server: {e}")

        response = self.client.recv(1024).decode()
        response = response.replace("END_OF_MSG", "")
        print("Response from server", response)
        response_json = json.loads(response)

        if response_json['status'] == 'success':
            print(response_json['message'])
            # window_new = MusicPlayer("mail", "John")
            # window_new.show()
            # משתנה לשמירת מופע החלון
            self.client.close()
            self.close()
            # יצירת מופע של
        elif response_json['status'] == 'error':
            QMessageBox.critical(self, "Register Failed", response_json['message'])


##############################################################


# Run the application
if __name__ == "__main__":
    # Replace None with an actual database connection
    connection = None
    app = QApplication(sys.argv)
    window = RegistrationWindow()
    window.show()
    sys.exit(app.exec())



