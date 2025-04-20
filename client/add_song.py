from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QListWidget, QApplication, QHBoxLayout, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import os
import sys

class PlaylistCreator(QDialog):
    def __init__(self, songs_data=None):
        super().__init__()
        self.setWindowTitle("Music Search and Playlist")
        self.setGeometry(100, 100, 400, 500)

        # Song and playlist storage
        self.songs = []
        self.song_ids = {}  # Map song name to ID
        self.playlist = []
        self.selected_song_id = None  # Store the selected song ID

        # Load songs from argument or folder
        if songs_data:
            self.load_songs_from_data(songs_data)
        else:
            self.load_songs()

        # UI Components
        self.init_ui()

        # Apply style
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: white;
                font-family: Arial;
            }
            QLineEdit, QListWidget, QPushButton {
                background-color: #1e1e1e;
                color: white;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1DB954;
            }
        """)

    def init_ui(self):
        layout = QVBoxLayout()

        # Search label and input
        search_label = QLabel("Search Song:")
        search_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.search_input = QLineEdit()

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_song)

        layout.addWidget(search_label)
        layout.addWidget(self.search_input)
        layout.addWidget(search_button)

        # Song results
        layout.addWidget(QLabel("Search Results:"))
        self.song_list = QListWidget()
        self.song_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        layout.addWidget(self.song_list)


        # Select Song button
        select_button = QPushButton("Select Song and Return ID")
        select_button.clicked.connect(self.return_selected_song_id)
        layout.addWidget(select_button)

        self.setLayout(layout)

    def load_songs_from_data(self, songs_data):
        for song in songs_data:
            song_id, name, duration, category, artist = song
            display_name = f"{name} | {artist} | {category} | {duration}s"
            self.songs.append(display_name)
            self.song_ids[display_name] = song_id

    def search_song(self):
        query = self.search_input.text().lower()
        self.song_list.clear()
        for song in self.songs:
            if query in song.lower():
                self.song_list.addItem(song)

    def return_selected_song_id(self):
        selected_items = self.song_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a song first.")
            return
        song_name = selected_items[0].text()
        song_id = self.song_ids.get(song_name, None)
        if song_id:
            self.selected_song_id = song_id  # Set the value before closing
            self.accept()
        else:
            QMessageBox.warning(self, "Song Not Found", "Unable to find song ID.")
            return None
