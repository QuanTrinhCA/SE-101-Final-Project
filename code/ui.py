import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests

class App:
    def __init__(self, root, conn_to_main):
        self.root = root
        self.root.title("Smert")
        self.root.geometry("800x480")
        self.root.overrideredirect(True)

        self.conn_to_main = conn_to_main

        image = Image.open(os.path.dirname(os.path.realpath(__file__)) + "\\not_loaded.gif")  # Replace "music_icon.png" with your image file
        image = image.resize((300, 300))
        self.photo = ImageTk.PhotoImage(image)

        self.create_widgets()

    def updateTitle(self, title):
        self.song_name_label.config(text=title)

    def updateProgress(self, progress):
        self.progressbar.config(value=progress * 100)

    def changeProgress(self, value):
        return
    
    def updateThumbnail(self, url):
        # Load the image
        image = Image.open(requests.get(url, stream=True).raw)  # Replace "music_icon.png" with your image file
        image = image.resize((300, 150))
        self.photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.photo)
    
    def updateVolume(self, volume):
        self.volume_slider.config(value=volume)

    def changeVolume(self, value):     
        volume = round(float(value))       
        self.conn_to_main.send({'action': 'set_volume',
                                'volume': volume})
        print(volume)

    def nextSong(self):
        self.conn_to_main.send({'action': 'next_song'})

    def pauseAudio(self):
        self.conn_to_main.send({'action': 'pause'})

    def unpauseAudio(self):
        self.conn_to_main.send({'action': 'unpause'})

    def create_widgets(self):
        # Display the image at the top
        self.image_label = tk.Label(self.root, image=self.photo)
        self.image_label.pack(pady=10)

        # Text label for song name
        self.song_name_label = tk.Label(self.root, text="YOUR MOM", font=("Arial", 25))
        self.song_name_label.pack(pady=30)

        self.progressbar = ttk.Progressbar(self.root,
                                           value=0,
                                           mode="determinate",
                                           orient="horizontal",
                                           length=700)
        self.progressbar.pack(padx=10, pady=10)

        # Create buttons
        self.play_button = tk.Button(self.root, text="Play", command=self.unpauseAudio, width=8, padx=5, pady=5)
        self.play_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = tk.Button(self.root, text="Pause", command=self.pauseAudio, width=8, padx=5, pady=5)
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.next_button = tk.Button(self.root, text="Next", command=self.nextSong, width=8, padx=5, pady=5)
        self.next_button.pack(side=tk.LEFT, padx=5)

        self.like_button = tk.Button(self.root, text="Like", width=8, padx=5, pady=5)
        self.like_button.pack(side=tk.LEFT, padx=5)

        self.dislike_button = tk.Button(self.root, text="Dislike", width=8, padx=5, pady=5)
        self.dislike_button.pack(side=tk.LEFT, padx=5)

        self.volume_slider = ttk.Scale(self.root, from_=100, to=0, value=100, command=self.changeVolume, orient="vertical", length=200)
        self.volume_slider.pack(side=tk.RIGHT, padx=10, pady=7)

        # Create status label
        self.status_label = tk.Label(self.root, text="No track loaded.")
        self.status_label.pack(side=tk.BOTTOM, pady=10)

def ui(conn_to_main):
    root = tk.Tk()
    mp = App(root=root, conn_to_main=conn_to_main)
    root.update()
    while True:
        if conn_to_main.poll():
            info = conn_to_main.recv()
            for key in info:
                if (key == 'position'):
                    mp.updateProgress(progress=info[key])
                if (key == 'title'):
                    mp.updateTitle(title=info[key])
                if (key == 'thumbnailurl'):
                    mp.updateThumbnail(url=info[key])
                if (key == 'length'):
                    print(info[key])
                if (key == 'artist'):
                    print(info[key])
                if (key == 'volume'):
                    mp.updateVolume(volume=info[key])
        root.update()