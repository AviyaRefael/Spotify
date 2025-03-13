import pygame
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QPushButton, QWidget, QFileDialog
)
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

from client.playlist_items_table import PlaylistItemsTable
from client.playlists_list import PlaylistsList


class MusicPlayer(QMainWindow):
    def __init__(self,client,mail,name):
        super().__init__()
        self.client = client
        self.mail = mail
        self.setWindowTitle(name)
        self.setGeometry(100, 100, 800, 600)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Media player
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)

        # Song list (table)
        self.song_table = PlaylistItemsTable(self.client,self.media_player)
        self.song_table.cellClicked.connect(self.song_selected)


        pygame.mixer.init()

        # Playlist list
        # 3 parameters:
        # a. the song table (right side). each time you will click on playlist song table will be updated
        # b. client to send requests to server (get songs of clicked playlist)
        # c. user mail to retrieve the user data
        self.playlist_list = PlaylistsList(self.song_table,self.client,self.mail)
        self.playlist_list.itemClicked.connect(
            lambda item: self.playlist_list.on_playlist_click(item, self.playlist_list.row(item)))


        # Control buttons
        self.prev_button = QPushButton("Previous")
        self.play_button = QPushButton("Play")
        self.pause_button = QPushButton("Pause")
        self.stop_button = QPushButton("Stop")
        self.next_button = QPushButton("Next")
        self.add_button = QPushButton("Add")

        # Connect buttons to functions
        self.play_button.clicked.connect(self.play_audio)
        self.pause_button.clicked.connect(self.pause_audio)
        self.stop_button.clicked.connect(self.stop_audio)
        self.add_button.clicked.connect(self.add_song)

        # Horizontal layout for playlists and song table
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.playlist_list, 1)  # Add playlist list
        top_layout.addWidget(self.song_table, 3)    # Add song table

        # Horizontal layout for control buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.next_button)
        button_layout.addWidget(self.add_button)

        # Main vertical layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.addLayout(top_layout)    # Add top layout (playlists + song table)
        main_layout.addLayout(button_layout)  # Add button layout

        self.setStyleSheet("""
                QMainWindow {
                    background-color: #121212;
                }
                QListWidget {
                    color: white;
                    background-color: #1e1e1e;
                }
                QTableWidget {
                    color: white;
                    background-color: #1e1e1e;  
                    gridline-color: #333333;
                }
                QPushButton {
                    color: white;
                    background-color: #333333;
                    border: none;
                    padding: 10px;
                    font-size: 14px;
                    border-radius: 10px;  /* Makes the button round */
                    min-width: 60px;     /* Ensures button size */
                    min-height: 40px;
                }
                QPushButton:hover {
                    background-color: #444444;
                }
            """)

    def song_selected(self, row, column):
        self.stop_audio()
        pygame.mixer.music.unload()
        print("unload")
        song_id = self.song_table.item(row, 4).text()  # Get the song ID
        self.song_table.get_song_data(song_id)



    def play_audio(self):
        # todo: playing after pause play from beginning
        # # Play the loaded MP3 file
        pygame.mixer.music.load("temp_song.mp3")
        pygame.mixer.music.play()

    def pause_audio(self):
        # Pause the currently playing audio
        print("Audio paused.")
        pygame.mixer.music.pause()

    def stop_audio(self):
        # Stop the currently playing audio
        print("Audio stopped.")
        pygame.mixer.music.stop()

    def add_song(self):
        return






# Run the application
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MusicPlayer("mail", "John")
    window.show()
    sys.exit(app.exec_())
