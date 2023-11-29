import tkinter as tk
from tkinter import ttk
#from PIL import Image, ImageTk

class App:
    def __init__(self, root, conn_to_main):
        self.root = root
        self.root.title("Smert")
        self.root.geometry("800x480")

        self.conn_to_main = conn_to_main

        # Load the image
        #image = Image.open("music_icon.png")  # Replace "music_icon.png" with your image file
        #image = image.resize((300, 150), Image.ANTIALIAS)
        #self.photo = ImageTk.PhotoImage(image)

        self.create_widgets()

    def updateTitle(self, title):
        self.song_name_label.config(text=title)

    def updateProgress(self, progress):
        return
    
    def updateVolume(self, volume):
        self.volume_slider.config(value=volume)

    def pauseAudio(self):
        self.conn_to_main.send({'action': 'pause'})

    def unpauseAudio(self):
        self.conn_to_main.send({'action': 'unpause'})

    def create_widgets(self):
        # Display the image at the top
        #image_label = tk.Label(self.root, image=self.photo)
        #image_label.pack(pady=10)

        # Text label for song name
        self.song_name_label = tk.Label(self.root, text="YOUR MOM", font=("Arial", 25))
        self.song_name_label.pack(pady=30)

        # Create buttons
        self.play_button = tk.Button(self.root, text="Play", command=self.unpauseAudio, width=8, padx=5, pady=5)
        self.play_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = tk.Button(self.root, text="Pause", command=self.pauseAudio, width=8, padx=5, pady=5)
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.next_button = tk.Button(self.root, text="Next", width=8, padx=5, pady=5)
        self.next_button.pack(side=tk.LEFT, padx=5)

        self.like_button = tk.Button(self.root, text="Like", width=8, padx=5, pady=5)
        self.like_button.pack(side=tk.LEFT, padx=5)

        self.dislike_button = tk.Button(self.root, text="Dislike", width=8, padx=5, pady=5)
        self.dislike_button.pack(side=tk.LEFT, padx=5)

        self.volume_slider = ttk.Scale(self.root, from_=0, to=100, orient="vertical", length=200)
        self.volume_slider.set(0.5)
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
                    print(info[key])
                if (key == 'length'):
                    print(info[key])
                if (key == 'artist'):
                    print(info[key])
                if (key == 'volume'):
                    mp.updateVolume(volume=info[key])
        root.update()