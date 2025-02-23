import tkinter as tk
from tkinter import Listbox, Entry, Button, Scrollbar
import socket

def fetch_songs_from_server():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("127.0.0.1", 12345))  # כתובת ופורט השרת
        client.sendall(b"GET_SONGS")
        data = client.recv(4096).decode("utf-8")
        client.close()
        return data.split("\n")
    except Exception as e:
        print(f"Error fetching songs: {e}")
        return []

def search_song():
    query = search_entry.get().lower()
    filtered_songs = [song for song in all_songs if query in song.lower()]
    song_listbox.delete(0, tk.END)
    for song in filtered_songs:
        song_listbox.insert(tk.END, song)

# יצירת חלון
root = tk.Tk()
root.title("חיפוש שירים")
root.geometry("400x400")

# שדה חיפוש
search_entry = Entry(root, width=40)
search_entry.pack(pady=10)

# כפתור חיפוש
search_button = Button(root, text="חפש", command=search_song)
search_button.pack()

# תיבת תצוגת רשימת השירים
scrollbar = Scrollbar(root)
song_listbox = Listbox(root, width=50, height=15, yscrollcommand=scrollbar.set)
scrollbar.config(command=song_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
song_listbox.pack(pady=10)

# טעינת השירים מהשרת
all_songs = fetch_songs_from_server()
for song in all_songs:
    song_listbox.insert(tk.END, song)

# הפעלת הלולאה הראשית
root.mainloop()
