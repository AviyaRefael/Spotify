import json
import socket

from PyQt6.QtWidgets import QListWidget
from PyQt6.QtWidgets import QMessageBox


class PlaylistsList(QListWidget):
    def __init__(self, song_table, client,  mail = None):
        super().__init__()
        self.song_table = song_table
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

        response = client.recv(1024).decode()
        response = response.replace("END_OF_MSG", "")
        print("Response from server", response)
        response_json = json.loads(response)

        if response_json['status'] == 'success':
            print(response_json['message'])
            # window_new = MusicPlayer("mail", "John")
            # window_new.show()


        elif response_json['status'] == 'error':
            QMessageBox.critical(self, "Login Failed", response_json['message'])

        # self.playlists = {132:"playlist1",36:"playlist2",952:"playlist3"}
        self.playlists = response_json['message']
        for playlist_name in self.playlists.values():
            self.add(playlist_name)
        print("added user's playlists to ui successfully")


    def add(self, list_name):
        self.addItem(list_name)

    def get_songs(self,row):
        # here get songs from server by list id
        for playlist in self.playlists:
            self.get_playlist_songs(playlist)
        temp_dic = {1:["song1.1", "song1.2"],2:["song2.1"]}
        playlist_id = list(self.playlists.keys())[row]
        return temp_dic[int(playlist_id)]

    def on_playlist_click(self, item, rowindex):
        playlist_name = item.text()
        playlist_id = 0
        for key,value in self.playlists:
            if value==playlist_name:
                playlist_id = key
                break
        # playlist_row = item.row(item)
        print(f"Clicked playlist: {playlist_name}")

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


