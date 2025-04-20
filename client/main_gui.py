import json

import pygame
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QPushButton, QWidget, QFileDialog, QMessageBox, QInputDialog
)
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

from client.add_song import PlaylistCreator
from client.playlist_items_table import PlaylistItemsTable
from client.playlists_list import PlaylistsList


class MusicPlayer(QMainWindow):
    def __init__(self,client,mail,name):
        super().__init__()
        self.client = client
        self.mail = mail
        self.setWindowTitle(name)
        self.setGeometry(100, 100, 800, 600)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Media player
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)

        # Song list (table)
        self.song_table = PlaylistItemsTable(self.client,self.media_player)
        self.song_table.cellClicked.connect(self.song_selected)

        pygame.mixer.init()

        # Playlist list
        self.playlist_list = PlaylistsList(self.song_table,self.client,self.mail)
        self.playlist_list.itemClicked.connect(
            lambda item: self.playlist_list.on_playlist_click(item, self.playlist_list.row(item)))

        # Control buttons
        # self.prev_button = QPushButton("Previous")
        self.play_button = QPushButton("Play")
        # self.pause_button = QPushButton("Pause")
        self.stop_button = QPushButton("Stop")
        # self.next_button = QPushButton("Next")
        self.add_button = QPushButton("Add")
        self.create_playlist_button = QPushButton("New Playlist")  # New playlist button

        # Connect buttons to functions
        self.play_button.clicked.connect(self.play_audio)
        # self.pause_button.clicked.connect(self.pause_audio)
        self.stop_button.clicked.connect(self.stop_audio)
        self.add_button.clicked.connect(self.add_song)
        self.create_playlist_button.clicked.connect(self.create_playlist)  # Connect to function

        # Horizontal layout for playlists and song table
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.playlist_list, 1)
        top_layout.addWidget(self.song_table, 3)

        # Horizontal layout for control buttons
        button_layout = QHBoxLayout()
        # button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.play_button)
        # button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.stop_button)
        # button_layout.addWidget(self.next_button)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.create_playlist_button)

        # Main vertical layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.addLayout(top_layout)
        main_layout.addLayout(button_layout)

        self.setStyleSheet("""
                QMainWindow {
                    background-color: #121212;
                }
                QListWidget {
                    color: white;
                    background-color: #1e1e1e;
                }
                QTableWidget {
                    color: white;
                    background-color: #1e1e1e;  
                    gridline-color: #333333;
                }
                QPushButton {
                    color: white;
                    background-color: #333333;
                    border: none;
                    padding: 10px;
                    font-size: 14px;
                    border-radius: 10px;
                    min-width: 60px;
                    min-height: 40px;
                }
                QPushButton:hover {
                    background-color: #444444;
                }
            """)

    def song_selected(self, row, column):
        self.stop_audio()
        pygame.mixer.music.unload()
        print("unload")
        song_id = self.song_table.item(row, 4).text()
        self.song_table.get_song_data(song_id)

    def play_audio(self):
        pygame.mixer.music.load("temp_song.mp3")
        pygame.mixer.music.play()

    def stop_audio(self):
        print("Audio stopped.")
        pygame.mixer.music.stop()

    def receive_full_response(self):
        data = b""
        while True:
            chunk = self.client.recv(4096)
            if b"END_OF_MSG" in chunk:
                data += chunk.split(b"END_OF_MSG")[0]
                break
            data += chunk
        return data.decode('utf-8')

    def add_song(self):
        selected_playlist_id = self.playlist_list.get_selected_playlist_id()

        not_in_playlist_songs_request ={
            "type": "get_not_in_playlist_songs_id",
            "playlist_id": selected_playlist_id,
        }

        try:
            self.client.send((json.dumps(not_in_playlist_songs_request) + "END_OF_MSG").encode())
        except Exception as e:
            QMessageBox.critical(self, "Connection Error", f"Failed to send data to server: {e}")

        response = self.receive_full_response()
        print("Response from server", response)
        response_json = json.loads(response)

        if response_json['status'] == 'success':
            song_id = None
            songs_data = response_json["message"]
            window = PlaylistCreator(songs_data)
            if window.exec():
                song_id = window.selected_song_id
                print("Selected song ID:", song_id)
        elif response_json['status'] == 'error':
            QMessageBox.critical(self, "Login Failed", response_json['message'])
            return

        add_song_to_selected_playlist = {
            "type": "add_to_playlist",
            "playlist_id": selected_playlist_id,
            "song_id": song_id
        }

        try:
            self.client.send((json.dumps(add_song_to_selected_playlist) + "END_OF_MSG").encode())
        except Exception as e:
            QMessageBox.critical(self, "Connection Error", f"Failed to send data to server: {e}")

        response = self.client.recv(1024).decode()
        response = response.replace("END_OF_MSG", "")
        print("Response from server", response)
        response_json = json.loads(response)

        if response_json['status'] == 'success':
            print(response_json['message'])
        elif response_json['status'] == 'error':
            QMessageBox.critical(self, "Login Failed", response_json['message'])

        return

    def create_playlist(self):
        playlist_name, ok = QInputDialog.getText(self, "New Playlist", "Enter playlist name:")
        if ok and playlist_name.strip():
            create_playlist_request = {
                "type": "new_playlist",
                "playlist_name": playlist_name.strip(),
                "mail": self.mail
            }

            try:
                self.client.send((json.dumps(create_playlist_request) + "END_OF_MSG").encode())
            except Exception as e:
                QMessageBox.critical(self, "Connection Error", f"Failed to send request: {e}")
                return

            response = self.client.recv(1024).decode().replace("END_OF_MSG", "")
            print("Response from server:", response)
            response_json = json.loads(response)

            if response_json["status"] == "success":
                QMessageBox.information(self, "Playlist Created", response_json["message"])
                self.playlist_list.load_playlists(self.client)  # Refresh playlists
            else:
                QMessageBox.critical(self, "Error", response_json["message"])

        return
