import json
import socket

from PyQt5.QtWidgets import QListWidget
from PyQt6.QtWidgets import QMessageBox


class PlaylistsList(QListWidget):
    def __init__(self, song_table, client,  mail = None):
        super().__init__()
        self.song_table = song_table
        self.mail = "j@j.com"
        self.playlists = {}
        self.load_playlists(client)


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
        songs = self.get_songs(0)
        for song in songs:
            self.song_table.add_song( song,  "Album", "Date Added", "Duration")


    def add(self, list_name):
        self.addItem(list_name)

    def get_songs(self,row):
        # here get songs from server by list id
        temp_dic = {132:["song1.1", "song1.2"],36:["song2.1"],952:["song3.1", "song3.2"]}
        playlist_id = list(self.playlists.keys())[row]
        return temp_dic[int(playlist_id)]

    def on_playlist_click(self, item, rowindex):
        playlist_name = item.text()
        # playlist_row = item.row(item)
        print(f"Clicked playlist: {playlist_name}")
        songs = self.get_songs(rowindex)
        self.song_table.setRowCount(0)
        for song in songs:
            self.song_table.add_song( song,  "Album", "Date Added", "Duration")


