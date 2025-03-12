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
        # HERE RECEIVE PLAYLISTS OF CURRENT USER FROM SERVER
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
        elif response_json['status'] == 'error':
            QMessageBox.critical(self, "Loading Playlists Failed", response_json['message'])

        # add and display playlists name to playlists list
        self.playlists = response_json['message']
        for playlist_name in self.playlists.values():
            self.addItem(playlist_name)


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
        elif response_json['status'] == 'error':
            QMessageBox.critical(self, "Failed", response_json['message'])


        return response_json["message"]


    # def on_song_click(self, row):
    #     """
    #     This function is called when a song is clicked.
    #     It gets the songs row, the get the id of the song, then requests the song file from the server,
    #     and then plays the song.
    #     """
    #     song_id = self.songs_id[row]
    #     self.song_table.play(song_id)
