import mysql.connector
from mysql.connector import Error

# 1. Connect to MySQL server
def connect_to_server(host, user, password, database="music"):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            print("Connected to MySQL server")
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# 2. Create users table
def create_users_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE
            )
        """)
        print("Users table created or already exists")
    except Error as e:
        print(f"Error: {e}")

# 3. Add a user to the table
def add_user(connection, username, password, email=None):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO users (name, password, mail) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, password, email))
        connection.commit()
        print("User added successfully")
    except Error as e:
        if "Duplicate entry" in str(e):
            print("Error: User already exists")
        else:
            print(f"Error: {e}")

# 4. Check if user already exists
def check_user_exists(connection, username, password):
    """
    Check if a user exists in the database with the given username and password.
    """
    try:
        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM users WHERE mail = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        return result[0] > 0
    except Error as e:
        print(f"Error: {e}")
        return False

# returns list of playlists id for the user id
def get_user_playlists(connection, user_mail):
    try:
        cursor = connection.cursor()
        query = "SELECT id, name FROM playlists WHERE user_mail = %s"
        cursor.execute(query, (user_mail,))
        playlists = cursor.fetchall()

        if playlists:
            return playlists
        else:
            print(f"No playlists found for user with email: {user_mail}")
            return []
    except Error as e:
        print(f"Error: {e}")
        return []

def getsongs_by_playlist(connection, playlist_id):
    try:
        cursor = connection.cursor()

        # SQL query to get all songs in the playlist by joining song_in_playlist and songs tables
        query = """
            SELECT songs.id, songs.title, songs.album, songs.date_added, songs.duration
            FROM song_in_playlist
            JOIN songs ON song_in_playlist.Song_id = songs.id
            WHERE song_in_playlist.playlist_id = %s
        """

        # Execute the query with the playlist_id
        cursor.execute(query, (playlist_id,))
        songs = cursor.fetchall()

        if songs:
            return songs
        else:
            print(f"No songs found for playlist with ID: {playlist_id}")
            return []

    except Error as e:
        print(f"Error: {e}")
        return []


# Main Function to Test
if __name__ == "__main__":
    # Update these with your MySQL server credentials
    host = "localhost"
    user = "root"
    password = "root"
    database = "music"

    # 1. Connect to the MySQL server and create database if not exists
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

    # # 2. Create users table
    # create_users_table(connection)
    #
    # # 3. Add users
    username = "aviya"
    password = "securepassword"
    email = "aviya2@gmail.com"

    # if not check_user_exists(connection, email):
    #     add_user(connection, username, password, email)
    # else:
    #     print("User already exists")

    # # 4. Check if a user exists
    # if check_user_exists(connection, "johndoe"):
    #     print("User johndoe exists in the database")
    # else:
    #     print("User johndoe does not exist")

    # Close the connection
    user_mail = "aviya@gmail.com"
    playlists = get_user_playlists(connection, user_mail)

    if playlists:
        print(f"Playlists for {user_mail}:")
        for playlist in playlists:
            print(f"ID: {playlist[0]}, Name: {playlist[1]}")
    else:
        print("No playlists found for this user.")
    connection.close()
