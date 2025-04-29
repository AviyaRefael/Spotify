from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton, QFileDialog, QLineEdit,
    QLabel, QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt
import os
import base64
import json
from mutagen.mp3 import MP3


class UploadWindow(QDialog):
    def __init__(self, client):
        super().__init__()
        self.setWindowTitle("Upload New Song")
        self.setFixedSize(400, 300)
        self.client = client
        self.file_path = None
        self.length = 0

        # Layout
        layout = QVBoxLayout()

        # File chooser
        self.browse_btn = QPushButton("Browse MP3 File")
        self.browse_btn.clicked.connect(self.browse_file)
        layout.addWidget(self.browse_btn)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Song Name")
        layout.addWidget(self.name_input)

        self.artist_box = QComboBox()
        layout.addWidget(QLabel("Select Artist"))
        layout.addWidget(self.artist_box)

        self.category_box = QComboBox()
        layout.addWidget(QLabel("Select Category"))
        layout.addWidget(self.category_box)

        self.upload_btn = QPushButton("Upload")
        self.upload_btn.clicked.connect(self.upload_song)
        layout.addWidget(self.upload_btn)

        self.setLayout(layout)

        # Fetch data from server
        self.load_artists()
        self.load_categories()

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose MP3", "", "MP3 Files (*.mp3)")
        if file_path:
            self.file_path = file_path
            self.name_input.setText(os.path.basename(file_path).replace(".mp3", ""))
            audio = MP3(file_path)
            self.length = int(audio.info.length)

    def load_artists(self):
        request = {"type": "get_artists"}
        self.send_request(request)
        response = self.receive_response()
        if response['status'] == 'success':
            self.artists = response['message']
            for name in self.artists.values():
                self.artist_box.addItem(name)

    def load_categories(self):
        request = {"type": "get_categories"}
        self.send_request(request)
        response = self.receive_response()
        if response['status'] == 'success':
            self.categories = response['message']
            for name in self.categories.values():
                self.category_box.addItem(name)

    def upload_song(self):
        if not self.file_path:
            QMessageBox.warning(self, "No file", "Choose an MP3 file first.")
            return

        with open(self.file_path, "rb") as f:
            file_data = base64.b64encode(f.read()).decode('utf-8')

        song_name = self.name_input.text().strip()
        artist_name = self.artist_box.currentText()
        category_name = self.category_box.currentText()

        request = {
            "type": "upload_song",
            "song_name": song_name,
            "artist_name": artist_name,
            "category_name": category_name,
            "length": self.length,
            "file_data": file_data
        }
        self.send_request(request)
        response = self.receive_response()
        if response['status'] == 'success':
            QMessageBox.information(self, "Success", response['message'])
            self.accept()
        else:
            QMessageBox.critical(self, "Failed", response['message'])

    def send_request(self, request):
        self.client.send((json.dumps(request) + "END_OF_MSG").encode())

    def receive_response(self):
        data = b""
        while True:
            chunk = self.client.recv(4096)
            if b"END_OF_MSG" in chunk:
                data += chunk.split(b"END_OF_MSG")[0]
                break
            data += chunk
        return json.loads(data.decode("utf-8"))
