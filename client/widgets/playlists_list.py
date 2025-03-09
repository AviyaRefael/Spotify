import base64
import json
import socket

import pygame
from PyQt6.QtWidgets import QListWidget
from PyQt6.QtWidgets import QMessageBox


class PlaylistsList(QListWidget):
    def __init__(self, song_table, client,  mail = None):
        super().__init__()
        self.song_table = song_table
        # self.song_table.itemClicked.connect(self.on_song_click)
        self.mail = mail
        self.playlists = {}
        self.load_playlists(client)
        self.client = client


    def load_playlists(self, client):
        # HERE RECEIVE PLAYLISTS FROM SERVER
        # Create a JSON object for the login request
        playlists_request = {
            "type": "playlists",
            "mail": self.mail
        }
        try:
            # Convert the JSON object to a string and send it to the server
            client.send((json.dumps(playlists_request)+"END_OF_MSG").encode())
        except Exception as e:
            print(f"Failed to send data to server: {e}")

        response = client.recv(4096).decode()
        response = response.replace("END_OF_MSG", "")
        print("Response from server", response)
        response_json = json.loads(response)

        if response_json['status'] == 'success':
            print(response_json['message'])
            # window_new = MusicPlayer("mail", "John")
            # window_new.show()


        elif response_json['status'] == 'error':
            QMessageBox.critical(self, "Login Failed", response_json['message'])

        self.playlists = response_json['message']
        for playlist_name in self.playlists.values():
            self.add(playlist_name)
        print("added user's playlists to ui successfully")


    def add(self, list_name):
        self.addItem(list_name)


    # def get_songs(self,row):
    #     # here get songs from server by list id
    #     for playlist in self.playlists:
    #         self.get_playlist_songs(playlist)
    #     # temp_dic = {1:["song1.1", "song1.2"],2:["song2.1"]}
    #     playlist_id = list(self.playlists.keys())[row]
    #     return temp_dic[int(playlist_id)]

    def on_playlist_click(self, item, rowindex):
        playlist_name = item.text()
        playlist_id = 0
        for key, value in self.playlists.items():
            if value==playlist_name:
                playlist_id = key
                break

        # Clear previous songs before adding new ones
        self.song_table.setRowCount(0)
        playlist_songs = self.get_playlist_songs_id(playlist_id)
        self.songs_id=[]
        for song in playlist_songs:
            self.song_table.display_songs(song[1],song[4],song[3],song[2], song[0])
            # add song id to list of songs id
            self.songs_id.append(song[0])

    def get_playlist_songs(self,playlist):
        return

    def get_playlist_songs_id(self,playlist_id):
        playlists_request = {
            "type": "get_playlist_songs_id",
            "playlist_id": playlist_id
        }
        try:
            # Convert the JSON object to a string and send it to the server
            self.client.send((json.dumps(playlists_request) + "END_OF_MSG").encode())
        except Exception as e:
            print(f"Failed to send data to server: {e}")

        response = self.client.recv(1024).decode()
        response = response.replace("END_OF_MSG", "")
        print("Response from server", response)
        response_json = json.loads(response)

        if response_json['status'] == 'success':
            print(response_json['message'])
            # window_new = MusicPlayer("mail", "John")
            # window_new.show()


        elif response_json['status'] == 'error':
            QMessageBox.critical(self, "Login Failed", response_json['message'])


        return response_json["message"]

    # def on_song_click(self, item):
    #     """
    #     This function is called when a song is clicked.
    #     It gets the song's ID, requests the song file from the server,
    #     and then plays the song.
    #     """
    #     row = item.row()
    #
    #     song_id = self.songs_id[row]
    #
    #     print(f"Selected song ID: {song_id}")
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


    def on_song_click(self, row):
        """
        This function is called when a song is clicked.
        It gets the songs row, the get the id of the song, then requests the song file from the server,
        and then plays the song.
        """
        song_id = self.songs_id[row]

        print(f"Selected song ID: {song_id}")

        # Request the song data from the server
        song_request = {
            "type": "get_song",
            "song_id": str(song_id)
        }
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

        # Check if the song was successfully received
        if response_json['status'] == 'success':
            print("Song received successfully")

            # Get the song data (Base64 encoded) and decode it
            song_data = response_json['file_data'].encode('utf-8')
            song_bytes = base64.b64decode(song_data)

            # Save the song temporarily
            temp_song_path = "temp_song.mp3"
            with open(temp_song_path, "wb") as song_file:
                song_file.write(song_bytes)

            song_file.close()
            # return temp_song_path
            # Initialize Pygame mixer
            pygame.mixer.init()

            # Play the song using pygame
            pygame.mixer.music.load(temp_song_path)
            pygame.mixer.music.play()

        elif response_json['status'] == 'error':
            print(f"Error: {response_json['message']}")
            QMessageBox.critical(self, "Error", response_json['message'])