import base64
import socket
import threading
import json
import os
from db import Db

FILES_DIR = "files"  # Directory to save uploaded files
# Ensure the directory for uploaded files exists
os.makedirs(FILES_DIR, exist_ok=True)


class Server:
    def __init__(self, host = '127.0.0.1',port = 12345):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        
    
    def start_server(self):
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print(f"Server listening on {self.host}:{self.port}")
        except Exception as e:
            print(f"Error starting server: {e}")

        self.db = Db('127.0.0.1', 'root', '1234',"music")

        while True:
            client_socket, address = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
            client_thread.start()


    
    def handle_client(self, client_socket: socket, address):
        print(f"New connection from {address}")
        try:
            while True:
                data = client_socket.recv(1024)
                print(f"new request from {address}: {data}")
                try:
                    request = json.loads(data.decode())
                    response = {}

                    if request['type'] == 'register':
                        response = self.register_user(request['mail'], request['name'], request['password'])
                    elif request['type'] == 'login':
                        response = self.login_user(request['mail'], request['password'])
                    elif request['type'] == 'upload':
                        file_name = request['file_name']
                        file_data = base64.b64decode(request['file_data'])
                        response = save_file(file_name, file_data)
                    elif request['type'] == 'get_song':
                        response = get_file(request['file_name'])
                    elif request['type'] == 'playlists':
                        response = self.get_playlists(request["mail"])
                    elif request['type'] == 'get_playlist_songs_by_id':
                        response = self.get_playlist_songs_by_id(request['playlist_id'])

                    client_socket.sendall((json.dumps(response)).encode())

                except Exception as e:
                    print(f"Error processing request from {address}: {e}")
                    error_response = {"status": "error", "message": str(e)}
                    client_socket.sendall((json.dumps(error_response)).encode())

        except Exception as e:
            print(f"Error handling client {address}: {e}")
        finally:
            print(f"Closing connection with {address}")
            client_socket.close()
        
        

# Helper Functions
    def register_user(self, mail, name, password):
        """Register a new user."""
        query = f"INSERT INTO users (name, password, mail) VALUES ('{mail}','{name}', '%{password}')"
        try:
            result = self.db.exceute_query(query)
            if result:
                return {"status": "success", "message": result}
            else:
                return {"status": "error", "message": result}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def login_user(self, mail, password):
        """Authenticate user."""

        query = f"SELECT mail,name FROM users WHERE mail='{mail}' AND password='{password}'"
        try:
            result = self.db.exceute_query(query)
            if result:
                return {"status": "success", "message": result}
            else:
                return {"status": "error", "message": result}
        except Exception as e:
            return {"status": "error", "message": str(e)}
        
    def get_playlists(self, mail):
        """Authenticate user."""

        query = f"SELECT id,name FROM playlists WHERE user_mail='{mail}'"
        try:
            result = self.db.exceute_query(query)
            print(result)
            if result:
                return {"status": "success", "message": result}
            else:
                return {"status": "error", "message": result}
        except Exception as e:
            return {"status": "error", "message": str(e)}
        
    def get_playlist_songs_by_id(self,playlist_id):
        query = f"""SELECT songs.id, songs.name
                    FROM songs
                    INNER JOIN playlist_songs ON playlist_songs.song_id = songs.id WHERE playlist_id={playlist_id};"""
        try:
            result = self.db.exceute_query(query)
            print(result)
            if result:
                return {"status": "success", "message": result}
            else:
                return {"status": "error", "message": result}
        except Exception as e:
            return {"status": "error", "message": str(e)}
        

def save_file(file_name, file_data):
    """Save uploaded file."""
    try:
        file_path = os.path.join(FILES_DIR, file_name)
        with open(file_path, "wb") as f:
            f.write(file_data)
        return {"status": "success", "message": f"File '{file_name}' uploaded successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_file(file_name):
    """Retrieve a file."""
    try:
        file_path = os.path.join(FILES_DIR, file_name)
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                return {"status": "success", "file_name": file_name, "file_data": base64.b64encode(f.read()).decode('utf-8')}
        return {"status": "error", "message": "File not found."}
    except Exception as e:
        return {"status": "error", "message": str(e)}



# Run the Server
if __name__ == "__main__":
    server = Server()
    server.start_server()

