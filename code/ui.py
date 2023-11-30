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

    def updateArtist(self, artist):
        self.song_artist_label.config(text=artist)

    def updateProgress(self, progress):
        self.progressbar.config(value=progress * 100)

    def changeProgress(self, value):
        self.conn_to_main.send({'action': 'set_position',
                           'position': value})
    
    def _fast_forward(self):
        position = self.progressbar['value']
        if position < 95:
            position += 5
        else:
            position = 99.8
        self.changeProgress(position / 100)
    
    def _fast_backward(self):
        position = self.progressbar['value']
        if position > 5:
            position -= 5
        else:
            position = 0
        self.changeProgress(position / 100)
    
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

    def updateEmo(self, emo):
        self.emo_label.config(text="Detected emotion: " + emo)

    def create_widgets(self):

        self.volume_slider = ttk.Scale(self.root, from_=100, to=0, value=100, command=self.changeVolume, orient="vertical", length=400)
        self.volume_slider.pack(side=tk.RIGHT, padx=15, pady=10)

        # Display the image at the top
        self.image_label = tk.Label(self.root, image=self.photo)
        self.image_label.pack(pady=10)

        # Text label for song name
        self.song_name_label = tk.Label(self.root, text="YOUR MOM", font=("Arial", 25))
        self.song_name_label.pack(pady=5)

        self.song_artist_label = tk.Label(self.root, text="Test", font=("Arial", 20))
        self.song_artist_label.pack(pady=5)  # Adjusting vertical padding and anchoring to the left

        self.progressbar = ttk.Progressbar(self.root,
                                           value=0,
                                           mode="determinate",
                                           orient="horizontal",
                                           length=700)
        self.progressbar.pack(padx=10, pady=10)

        # Create buttons
        button_row_1 = tk.Frame(self.root)
        button_row_1.pack(padx=10, pady=10)

        button_row_2 = tk.Frame(self.root)
        button_row_2.pack(padx=10, pady=10)

        self.backward_button = tk.Button(button_row_1, text="Fast backward", command=self._fast_backward, width=10, padx=5, pady=5, font=("Arial", 14))
        self.backward_button.pack(side=tk.LEFT, padx=5)

        self.play_button = tk.Button(button_row_1, text="Play", command=self.unpauseAudio, width=10, padx=5, pady=5, font=("Arial", 14))
        self.play_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = tk.Button(button_row_1, text="Pause", command=self.pauseAudio, width=10, padx=5, pady=5, font=("Arial", 14))
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.forward_button = tk.Button(button_row_1, text="Fast forward", command=self._fast_forward, width=10, padx=5, pady=5, font=("Arial", 14))
        self.forward_button.pack(side=tk.LEFT, padx=5)

        self.next_button = tk.Button(button_row_2, text="Next", command=self.nextSong, width=8, padx=5, pady=5, font=("Arial", 12))
        self.next_button.pack(side=tk.LEFT, padx=5)

        self.like_button = tk.Button(button_row_2, text="Like", width=8, padx=5, pady=5, font=("Arial", 12))
        self.like_button.pack(side=tk.LEFT, padx=5)

        self.dislike_button = tk.Button(button_row_2, text="Dislike", width=8, padx=5, pady=5, font=("Arial", 12))
        self.dislike_button.pack(side=tk.LEFT, padx=5)

        # Create status label
        self.emo_label = tk.Label(self.root, text="Detected emotion:")
        self.emo_label.pack(side=tk.BOTTOM, pady=10)

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
                    mp.updateArtist(artist=info[key])
                if (key == 'volume'):
                    mp.updateVolume(volume=info[key])
                if (key == 'emotion'):
                    mp.updateEmo(emo=info[key])
        root.update()