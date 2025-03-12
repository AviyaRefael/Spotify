import json
import socket

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import sys

from register_gui import RegistrationWindow
from main_gui import MusicPlayer


class SpotifyLogin(QWidget):
    def __init__(self):
        super().__init__()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(("localhost", 12345))
        self.simple_window = None

        self.init_ui()

    def init_ui(self):
        # Window setup
        self.setWindowTitle("Spotify Login")
        self.setFixedSize(400, 500)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Logo or Title
        logo_label = QLabel("Spotify")
        logo_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Username input
        self.username_input = QLineEdit()  # Define as instance variable
        self.username_input.setPlaceholderText("Email address")
        self.username_input.setFixedHeight(40)
        self.username_input.setText("aviya@gmail.com")


        # Password input
        self.password_input = QLineEdit()  # Define as instance variable
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(40)
        self.password_input.setText("securepassword")

        # Login button
        login_button = QPushButton("LOG IN")
        login_button.setFixedHeight(40)
        login_button.setStyleSheet("""
            background-color: #1DB954;
            color: white;
            border: none;
            border-radius: 20px;
            font-size: 16px;
        """)
        login_button.clicked.connect(self.handle_login)  # Connect button click to the handler

        # Registration button
        register_button = QPushButton("REGISTER")
        register_button.setFixedHeight(40)
        register_button.setStyleSheet("""
            background-color: #535353;
            color: white;
            border: none;
            border-radius: 20px;
            font-size: 16px;
        """)
        register_button.clicked.connect(self.open_registration_window)  # Open registration window

        # Link for forgotten password
        forgot_password_label = QLabel('<a href="#">Forgot your password?</a>')
        forgot_password_label.setOpenExternalLinks(True)
        forgot_password_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add widgets to the layout
        main_layout.addWidget(logo_label)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.username_input)  # Use instance variable
        main_layout.addWidget(self.password_input)  # Use instance variable
        main_layout.addSpacing(20)
        main_layout.addWidget(login_button)
        main_layout.addWidget(register_button)  # Add registration button
        main_layout.addSpacing(10)
        main_layout.addWidget(forgot_password_label)

        # Set layout to the window
        self.setLayout(main_layout)

    def handle_login(self):
        # Retrieve user input
        mail = self.username_input.text().strip()  # Access instance variable
        password = self.password_input.text().strip()  # Access instance variable

        # Check if fields are not empty
        if not mail or not password:
            QMessageBox.warning(self, "Input Error", "Email and Password cannot be empty!")
            return

        # Create a JSON object for the login request
        login_request = {
            "type": "login",
            "mail": mail,
            "password": password
        }

        try:
            # Convert the JSON object to a string and send it to the server
            self.client.send((json.dumps(login_request)+"END_OF_MSG").encode())
        except Exception as e:
            QMessageBox.critical(self, "Connection Error", f"Failed to send data to server: {e}")

        response = self.client.recv(1024).decode()
        response = response.replace("END_OF_MSG", "")
        print("Response from server", response)
        response_json = json.loads(response)

        if response_json['status'] == 'success':
            print(response_json['message'])
            # self.client.close()  # Close the socket
            # self.close()  # Close the login window
            window_new = MusicPlayer(self.client,mail, response_json['name'])
            window_new.show()


        elif response_json['status'] == 'error':
            QMessageBox.critical(self, "Login Failed", response_json['message'])

    def open_registration_window(self):
        # Open the registration window
        self.registration_window = RegistrationWindow()
        self.registration_window.show()



##############################################################


# Run the application
if __name__ == "__main__":
    # Replace None with an actual database connection
    connection = None
    app = QApplication(sys.argv)
    # window = RegistrationWindow()
    window = SpotifyLogin()
    window.show()
    # window_new = SpotifyLogin()
    # window_new.show()
    sys.exit(app.exec())
    # app.exec()



