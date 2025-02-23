import base64
import socket
import json
import os

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345
MY_FILES_FOLDER = "my_files"
END_MARKER = "END_OF_MSG"

# Ensure the client files directory exists
os.makedirs(MY_FILES_FOLDER, exist_ok=True)


class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((SERVER_HOST, SERVER_PORT))

    def send_request(self, request_data):
        # Convert request to JSON, encode, and append end marker
        # ממיר את הנתונים בפורמט של Python (למשל, מילון) למחרוזת בפורמט JSON.
        # פורמט JSON -מחרוזת
        json_data = json.dumps(request_data).encode('utf-8') + END_MARKER.encode('utf-8')
        self.client_socket.sendall(json_data)
        # Receive the response from the server
        # ממיר את התשובה שקיבלנו מהשרת (שהיא בפורמט JSON) בחזרה למבנה נתונים של Python, כמו מילון או רשימה.
        response_data = self.receive_response()
        return json.loads(response_data)

    def receive_response(self):
        data = b""# משתנה לאחסון הנתונים שנקלטו
        while True:
            chunk = self.client_socket.recv(1024)
            if END_MARKER.encode('utf-8') in chunk:
                data += chunk.split(END_MARKER.encode('utf-8'))[0]
                break
            data += chunk
        return data.decode('utf-8') # פענוח הנתונים ממבנה בינארי למחרוזת

    def register(self, mail, name, password):
        # הפונקציה בונה מילון (dictionary) שמכיל את פרטי הבקשה:
        request = {"type": "register", "mail": mail, "name": name, "password": password}
        return self.send_request(request)

    def login(self, mail, password):
        # הפונקציה בונה מילון (dictionary) שמכיל את פרטי הבקשה:
        request = {"type": "login", "mail": mail, "password": password}
        return self.send_request(request)

    def upload_song(self, file_path):
        file_name = os.path.basename(file_path)
        with open(file_path, "rb") as f:
            file_data = f.read()

        # Encode the file data in Base64
        file_data_base64 = base64.b64encode(file_data).decode('utf-8')
        request = {
            "type": "upload",
            "file_name": file_name,
            "file_data": file_data_base64
        }
        return self.send_request(request)

    def get_song(self, song_name):
        request = {"type": "get_song", "song_name": song_name}
        response = self.send_request(request)

        if response["status"] == "success":
            file_path = os.path.join(MY_FILES_FOLDER, response["file_name"])
            with open(file_path, "wb") as f:
                f.write(base64.b64decode(response["file_data"]))
            return {"status": "success", "message": f"File saved at {file_path}"}
        else:
            return response


# Example usage
if __name__ == "__main__":
    client = Client()

    # Register
    # response = client.register("test@mail.com", "Test User", "password123")
    # print("Register Response:", response)
    #
    # Login
    response = client.login("test2@mail.com", "password123")
    print("Login Response:", response)
    #
    # # Upload a song
    # response = client.upload_song("128.mp3")
    # print("Upload Response:", response)
    #
    # # Get a song

    # response = client.get_song("128.mp3")
    # print("Get Song Response:", response)
