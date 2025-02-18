from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem


class PlaylistItemsTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["Title", "Artist", "Category", "Duration"])

    def add_song(self, title, artist, category, duration):
        row_position = self.rowCount()  # Get the current number of rows
        self.insertRow(row_position)  # Add a new row at the end

        # Add items to each column
        self.setItem(row_position, 0, QTableWidgetItem(title))  # Title
        self.setItem(row_position, 1, QTableWidgetItem(artist))  # Album
        self.setItem(row_position, 2, QTableWidgetItem(category))  # Date Added
        self.setItem(row_position, 3, QTableWidgetItem(duration))  # Duration

    # def load_playlist(self, playlist_id):

