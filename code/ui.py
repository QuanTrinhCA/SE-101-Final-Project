import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
#from PIL import Image, ImageTk
from pygame import mixer

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("400x250")

        self.current_track = None
        self.tracks = []
        self.track_index = 0

        # Load the image
        #image = Image.open("music_icon.png")  # Replace "music_icon.png" with your image file
        #image = image.resize((300, 150), Image.ANTIALIAS)
        #self.photo = ImageTk.PhotoImage(image)

        self.create_widgets()

    def create_widgets(self):
        # Display the image at the top
        #image_label = tk.Label(self.root, image=self.photo)
        #image_label.pack(pady=10)

        # Text label for song name
        self.song_name_label = tk.Label(self.root, text="YOUR MOM", font=("Arial", 25))
        self.song_name_label.pack(pady=30)

        # Create buttons
        self.play_button = tk.Button(self.root, text="Play", command=self.play_track,width=8, padx=5, pady=5)
        self.play_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause_track, width=8, padx=5, pady=5)
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.next_button = tk.Button(self.root, text="Next", command=self.next_track, width=8, padx=5, pady=5)
        self.next_button.pack(side=tk.LEFT, padx=5)

        self.like_button = tk.Button(self.root, text="Like", command=self.like_track, width=8, padx=5, pady=5)
        self.like_button.pack(side=tk.LEFT, padx=5)

        self.dislike_button = tk.Button(self.root, text="Dislike", command=self.dislike_track, width=8, padx=5, pady=5)
        self.dislike_button.pack(side=tk.LEFT, padx=5)

        self.volume_slider = ttk.Scale(self.root, from_=0, to=1, orient="vertical", command=self.set_volume,length=200)
        self.volume_slider.set(0.5)
        self.volume_slider.pack(side=tk.RIGHT, padx=10, pady=7)

        # Create status label
        self.status_label = tk.Label(self.root, text="No track loaded.")
        self.status_label.pack(side=tk.BOTTOM, pady=10)