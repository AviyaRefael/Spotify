import mysql.connector
from mysql.connector import Error


class Db:
    def __init__(self,db_host = "localhost",db_username = "root",db_password = "root",db_name = "music"):
        try:
            connection = mysql.connector.connect(
                host=db_host,
                user=db_username,
                password=db_password,
                database=db_name
            )
            if connection.is_connected():
                self.db_connection = connection
                self.cursor = self.db_connection.cursor()
                print(f"successfully connected to db {db_name} on {db_host}")
            else:
                raise Error
        except Error as e:
            print(f"Error connection to DB: {e}")


    def exceute_query(self,query):
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error executing query: {query}, Error: {e}")
            return None
        


    # 2. Create users table
    # connection אובייקט החיבור ל SQL
    def create_users_table(self):
        try:
            # ה-cursor מתפקד כ"מתווך" בין קוד ה-Python לבין מסד הנתונים
            cursor = self.db_connection.cursor()
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
    def add_user(self,username, password, email):
        # username: שם המשתמש שיתווסף לטבלה.
        # password: סיסמת המשתמש.
        try:
            cursor = self.db_connection.cursor()
            query = "INSERT INTO users (name, password, mail) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, password, email))
            self.db_connection.commit()
            return True, "User added successfully"
        except Error as e:
            if "Duplicate entry" in str(e):
                return False, "User already exists"
            else:
                return False, e

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
            query = f"""SELECT songs.id, songs.name
                    FROM songs
                    INNER JOIN playlist_songs ON playlist_songs.song_id = songs.id WHERE playlist_id={playlist_id};"""
            cursor.execute(query)
            playlist_songs = cursor.fetchall()
            print(playlist_songs)
            return {"status": "success", "message": playlist_songs}
        except Error as e:
            print(f"Error: {e}")

