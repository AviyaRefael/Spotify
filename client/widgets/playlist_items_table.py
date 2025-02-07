from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem


class PlaylistItemsTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["Title", "Album", "Date Added", "Duration"])

    def add_song(self, title, album, date_added, duration):
        row_position = self.rowCount()  # Get the current number of rows
        self.insertRow(row_position)  # Add a new row at the end

        # Add items to each column
        self.setItem(row_position, 0, QTableWidgetItem(title))  # Title
        self.setItem(row_position, 1, QTableWidgetItem(album))  # Album
        self.setItem(row_position, 2, QTableWidgetItem(date_added))  # Date Added
        self.setItem(row_position, 3, QTableWidgetItem(duration))  # Duration

    # def load_playlist(self, playlist_id):

