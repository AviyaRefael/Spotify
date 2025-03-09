import mysql.connector
from mysql.connector import Error

# 1. Connect to MySQL server
# פונקציה התחברות  ל SQL
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
# connection אובייקט החיבור ל SQL
def create_users_table(connection):
    try:
        # ה-cursor מתפקד כ"מתווך" בין קוד ה-Python לבין מסד הנתונים
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
    # connection: אובייקט החיבור למסד הנתונים.
    # username: שם המשתמש שיתווסף לטבלה.
    # password: סיסמת המשתמש.
    # email: כתובת האימייל של המשתמש (לא חובה, ערך ברירת מחדל הוא None).
    try:
        cursor = connection.cursor()
        query = "INSERT INTO users (name, password, mail) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, password, email))
        connection.commit()
        return True, "User added successfully"
    except Error as e:
        if "Duplicate entry" in str(e):
            return False, "User already exists"
        else:
            return False, e

# 4. Check if user already exists
def check_user_exists(connection, mail, password):
    """
    Check if a user exists in the database and return their name if found.
    """
    try:
        cursor = connection.cursor()
        query = "SELECT name FROM users WHERE mail = %s AND password = %s"
        cursor.execute(query, (mail, password))
        result = cursor.fetchone()

        if result:  # If a user is found, return True and the name
            return True, result[0]
        else:
            return False, None  # No user found

    except Exception as e:
        print(f"Error: {e}")
        return False, None  # Return failure in case of an error


def get_playlist(connection,email):
    try:
        # ה-cursor מתפקד כ"מתווך" בין קוד ה-Python לבין מסד הנתונים
        cursor = connection.cursor()
        query = f"SELECT * FROM playlists WHERE user_mail='{email}'"
        cursor.execute(query)
        resp = cursor.fetchall()
        print(resp)
        playlists={}
        for row in resp:
            playlists[row[0]] = row[1]
        return {"status": "success","message": playlists}
    except Error as e:
        print(f"Error: {e}")

def get_playlist_songs_id(connection,playlist_id):
    try:
        # ה-cursor מתפקד כ"מתווך" בין קוד ה-Python לבין מסד הנתונים
        cursor = connection.cursor()
        # query = f"""SELECT songs.id, songs.name
        #         FROM songs
        #         INNER JOIN playlist_songs ON playlist_songs.song_id = songs.id WHERE playlist_id={playlist_id};"""

        query = f"""
        SELECT 
            songs.id, 
            songs.name, 
            songs.length, 
            categories.name AS category_name, 
            artists.name AS artist_name
        FROM songs
        INNER JOIN playlist_songs ON playlist_songs.song_id = songs.id
        LEFT JOIN categories ON songs.category_code = categories.id
        LEFT JOIN artists ON songs.artist_id = artists.id
        WHERE playlist_songs.playlist_id = {playlist_id};
        """
        # use ? for security (avoiding sql injection)
        cursor.execute(query)
        playlist_songs = cursor.fetchall()
        print(playlist_songs)
        return {"status": "success", "message": playlist_songs}
    except Error as e:
        print(f"Error: {e}")



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
#
    # # 2. Create users table
    # create_users_table(connection)
    #
    # # 3. Add users
    username = "aviya"
    password = "securepassword"
    mail = "aviya2@gmail.com"

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
    # connection.close()
