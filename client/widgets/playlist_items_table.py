import base64
import json

import pygame
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox


class PlaylistItemsTable(QTableWidget):
    def __init__(self, client, media_player):
        super().__init__()
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels(["Title", "Artist", "Category", "Duration","Id"])
        self.client = client
        self.media_player = media_player  # Reference to QMediaPlayer

    # display in songs list all the song from the selected playlist
    # the function is called from on_playlist_click function in playlist_list.py
    def display_songs(self, title, artist, category, duration, id):
        row_position = self.rowCount()  # Get the current number of rows
        self.insertRow(row_position)  # Add a new row at the end

        # Add items to each column
        self.setItem(row_position, 0, QTableWidgetItem(title))  # Title
        self.setItem(row_position, 1, QTableWidgetItem(artist))  # Album
        self.setItem(row_position, 2, QTableWidgetItem(category))  # Date Added
        self.setItem(row_position, 3, QTableWidgetItem(str(duration)))  # Duration
        self.setItem(row_position, 4, QTableWidgetItem(str(id)) ) # Id


    def play(self, song_id):
        """
        Request song from server and play it using QMediaPlayer.
        """
        # Request the song data from the server
        song_request = {"type": "get_song", "song_id": str(song_id)}
        try:
            self.client.send((json.dumps(song_request) + "END_OF_MSG").encode())
        except Exception as e:
            print(f"Failed to send data to server: {e}")
            return

        # Receive the song data from the server
        response = b""
        while True:
            chunk = self.client.recv(4096)
            if b"END_OF_MSG" in chunk:
                response += chunk.split(b"END_OF_MSG")[0]
                break
            response += chunk

        # Decode the response
        response_json = json.loads(response.decode('utf-8'))

        if response_json['status'] == 'success':
            print("Song received successfully")
            song_data = base64.b64decode(response_json['file_data'])

            # Save the song temporarily
            temp_song_path = "temp_song.mp3"
            with open(temp_song_path, "wb") as song_file:
                song_file.write(song_data)

            # Play with QMediaPlayer
            # todo: check while player doesnt play music
            self.media_player.setSource(QUrl.fromLocalFile(temp_song_path))
            self.media_player.play()

        elif response_json['status'] == 'error':
            print(f"Error: {response_json['message']}")
            QMessageBox.critical(self, "Error", response_json['message'])

    # def play(self, song_id):
    #     """
    #     This function is called when a song is clicked.
    #     It gets the songs row, the get the id of the song, then requests the song file from the server,
    #     and then plays the song.
    #     """
    #
    #     # Request the song data from the server
    #     song_request = {
    #         "type": "get_song",
    #         "song_id": str(song_id)
    #     }
    #     try:
    #         self.client.send((json.dumps(song_request) + "END_OF_MSG").encode())
    #     except Exception as e:
    #         print(f"Failed to send data to server: {e}")
    #         return
    #
    #     # Receive the song data from the server
    #     response = b""
    #     while True:
    #         chunk = self.client.recv(4096)
    #         if b"END_OF_MSG" in chunk:
    #             response += chunk.split(b"END_OF_MSG")[0]
    #             break
    #         response += chunk
    #
    #     # Decode the response
    #     response_json = json.loads(response.decode('utf-8'))
    #
    #     # Check if the song was successfully received
    #     if response_json['status'] == 'success':
    #         print("Song received successfully")
    #
    #         # Get the song data (Base64 encoded) and decode it
    #         song_data = response_json['file_data'].encode('utf-8')
    #         song_bytes = base64.b64decode(song_data)
    #
    #         # Save the song temporarily
    #         temp_song_path = "temp_song.mp3"
    #         with open(temp_song_path, "wb") as song_file:
    #             song_file.write(song_bytes)
    #
    #         song_file.close()
    #         # return temp_song_path
    #         # Initialize Pygame mixer
    #         pygame.mixer.init()
    #
    #         # Play the song using pygame
    #         pygame.mixer.music.load(temp_song_path)
    #         pygame.mixer.music.play()
    #
    #     elif response_json['status'] == 'error':
    #         print(f"Error: {response_json['message']}")
    #         QMessageBox.critical(self, "Error", response_json['message'])
