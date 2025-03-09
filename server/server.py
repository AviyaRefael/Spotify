import base64
import socket
import threading
import json
import os
from mysql.connector import Error

# Configuration
from db_functions import add_user, connect_to_server, get_playlist, get_playlist_songs_id, check_user_exists

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345
FILES_DIR = "files"  # Directory to save uploaded files
END_MARKER = "END_OF_MSG"
# Ensure the directory for uploaded files exists
os.makedirs(FILES_DIR, exist_ok=True)

connection = None

# Helper Functions
def register_user(mail, name, password):
    """Register a new user."""
    try:
        result, message = add_user(connection, name, password, mail)
        if result:
            return {"status": "success", "message": message}
        else:
            return {"status": "error", "message": message}
    except Error as e:
        return {"status": "error", "message": str(e)}

def login_user(name, password):
    """Authenticate user."""
    ###################################################
    ###################################################

      # REPLACE THIS CODE BY DB_FUNCTION CHECK USER

    try:
        resp, name = check_user_exists(connection, name, password)
        if resp:
            return {"status": "success", "message": "Login successful.", "name":name}
        else:
            return {"status": "error", "message": "Invalid credentials."}
    except Error as e:
        return {"status": "error", "message": str(e)}
    ###################################################
    ###################################################
def save_file(file_name, file_data):
    """Save uploaded file."""
    try:
        file_path = os.path.join(FILES_DIR, file_name)
        with open(file_path, "wb") as f:
            f.write(file_data)
        return {"status": "success", "message": f"File '{file_name}' uploaded successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_file(song_id):
    """Retrieve a file."""
    try:
        file_path = os.path.join(FILES_DIR, song_id+".mp3")
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                return {"status": "success", "file_name": song_id, "file_data": base64.b64encode(f.read()).decode('utf-8')}
        return {"status": "error", "message": "File not found."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Client Handler
def handle_client(client_socket, address):
    print(f"New connection from {address}")
    try:
        while True:
            data = b""
            while True:
                packet = client_socket.recv(1024)
                print("Receive from client:",packet)
                if not packet:
                    print(f"Client {address} disconnected.")
                    return
                data += packet
                if b"END_OF_MSG" in data:
                    break

            data = data.replace(b"END_OF_MSG", b"")

            try:
                request = json.loads(data.decode('utf-8'))
                response = {}

                if request['type'] == 'register':
                    # add user to db
                    response = register_user(request['mail'], request['name'], request['password'])
                elif request['type'] == 'login':
                    # check in db if user exists
                    response = login_user(request['mail'], request['password'])
                elif request['type'] == 'upload':
                    # 1. add song file to server
                    file_name = request['file_name']
                    file_data = base64.b64decode(request['file_data'])
                    # 2. add song data to db
                    response = save_file(file_name, file_data)
                elif request['type'] == 'get_song':
                    # get one song data from server
                    response = get_file(request['song_id'])
                elif request['type'] == 'playlists':
                    # get from DB all playlists of specific user (by mail address as identifier)
                    response = get_playlist(connection,request["mail"])
                elif request['type'] == 'get_playlist_songs_id':
                    # get from DB all songs info. of specific playlist
                    response = get_playlist_songs_id(connection,request['playlist_id'])

                client_socket.sendall((json.dumps(response) + "END_OF_MSG").encode('utf-8'))

            except Exception as e:
                print(f"Error processing request from {address}: {e}")
                error_response = {"status": "error", "message": str(e)}
                client_socket.sendall((json.dumps(error_response) + "END_OF_MSG").encode('utf-8'))

    except Exception as e:
        print(f"Error handling client {address}: {e}")
    finally:
        print(f"Closing connection with {address}")
        client_socket.close()

# Server Function
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen(5)
        print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")

        host = "localhost"
        user = "root"
        password = "root"
        database = "music"

        global connection
        connection = connect_to_server(host, user, password)
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
                print(f"Database '{database}' is ready")
                connection.database = database
            except Error as e:
                print(f"Error while creating database: {e}")
                connection.close()
                exit()

        while True:
            client_socket, address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
            client_thread.start()

    except Exception as e:
        print(f"Error starting server: {e}")
    finally:
        server_socket.close()

# Run the Server
if __name__ == "__main__":
    start_server()

