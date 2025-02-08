import json
from PyQt6.QtWidgets import QListWidget



class PlaylistsList(QListWidget):
    def __init__(self, song_table, client,  mail = None):
        super().__init__()
        self.song_table = song_table
        self.mail = mail
        self.playlists = {}
        self.client = client
        self.itemClicked.connect(self.on_playlist_click)
        self.load_playlists()
        print("finished loading Playlists Widget")


    def load_playlists(self):
        self.playlists = self.get_user_playlists(self.mail)
        for _,playlist_name in self.playlists:
            self.add(playlist_name)
        print("Added user's playlists to ui successfully")
        

    def get_user_playlists(self,user_email):
        playlists_request = {
            "type": "playlists",
            "mail": user_email
        }
        return self.handle_server_request(playlists_request)

    def add(self, playlist_name):
        self.addItem(playlist_name)

    def on_playlist_click(self, item):
        playlist_name = item.text()
        playlist_id = 0
        for key,value in self.playlists:
            if value==playlist_name:
                playlist_id = key
                break
        print(f"Clicked playlist: {playlist_name}")
        for id,name in self.get_playlist_songs_by_id(playlist_id):
            self.song_table.add_song(name,"album","date added","duration")
        


    def get_playlist_songs_by_id(self,playlist_id):
        playlist_songs_request = {
            "type": "get_playlist_songs_by_id",
            "playlist_id": playlist_id
        }
        return self.handle_server_request(playlist_songs_request)

    def handle_server_request(self,request):
        # Try sending data to server
        try:
            print(f"sending request to server: {request}")
            self.client.send(json.dumps(request).encode())
        except Exception as e:
            print(f"Failed to send data to server: {e}")
            # Return None if Error raised
            return None

        # Try receiving the response
        try:
            # Receive response
            response = self.client.recv(1024)
            response_json = json.loads(response.decode())
            print("Response from server:", response_json)
            # Return response if no error raised
            return response_json['message']
        except Exception as e:
            print(f"Error decoding data from server: {response_json} error: {e}")
            # Return None if error raised
            return None
        



