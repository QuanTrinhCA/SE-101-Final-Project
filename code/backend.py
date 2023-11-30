import vlc, ytmusicapi, yt_dlp, random

# with ytmusicapi.YTMusic() as ytmusic:
#     test = ytmusic.get_mood_categories()
#     print(test)

class AudioBackend:
    def __init__(self, conn_to_main):
        self.player = vlc.MediaPlayer()
        self.prevposition = 0
        self.ispause = True
        self.song = ''
        self.songinfo = ''
        self.audiourl = ''

    def find_song_based_on_mood(self, mood):
        mood_index = 0
        with ytmusicapi.YTMusic() as ytmusic:
            if mood == 'happy':
                mood_index = 8
            elif mood == 'sad':
                mood_index = 11
            elif mood == 'surprise':
                mood_index = 1
            elif mood == 'neutral':
                mood_index = 4
            elif mood == 'angry':
                mood_index = 1
            elif mood == 'disgust':
                mood_index = 5
            elif mood == 'fear':
                mood_index = 7
            playlistlist = ytmusic.get_mood_playlists(params=ytmusic.get_mood_categories()["Moods & moments"][mood_index]['params'])
            luckyplaylist = ytmusic.get_playlist(playlistId=playlistlist[random.randint(0,len(playlistlist) - 1)]['playlistId'])
            luckysong = luckyplaylist['tracks'][random.randint(0, len(luckyplaylist['tracks']) - 1)]
        self.song = luckysong
    
    # def get_song_info(self, name):
    #     with ytmusicapi.YTMusic() as ytmusic:
    #         self.songinfo = ytmusic.get_song(ytmusic.search(query=name, filter="songs")[0])

    def get_audio_stream(self):
        ydl_opts = {
            'extractor_args': {
                'youtube': {
                    'skip': ['hls,dash,translated_subs'],
                    'player_client': ['android_music']
                    }
            }
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for format in ydl.sanitize_info(ydl.extract_info(f"https://music.youtube.com/watch?v=" + self.song['videoId'], download=False, process=False, ie_key="Youtube"))['formats']:
                if format['format_id'] == '251':
                    self.audiourl = format['url']

    def play_audio_stream(self):
        self.player.set_mrl(self.audiourl)
        self.player.play()
        self.ispause = False

    def pause_audio_stream(self):
        if not self.ispause:
            self.player.pause()
            self.ispause = True

    def unpause_audio_stream(self):
        if self.ispause:
            self.player.pause()
            self.ispause = False

    def set_audio_stream_volume(self, volume):
        self.player.audio_set_volume(volume)

    def get_stream_position(self):
        return self.player.get_position()
    
    def set_stream_position(self, position):
        self.player.set_position(position)

def audio_backend(conn_to_main):
    backend = AudioBackend(conn_to_main=conn_to_main)
    while True:
        # Sending info
        currentposition = backend.get_stream_position()
        if (currentposition - backend.prevposition > 0.001):
            backend.prevposition = currentposition
            conn_to_main.send({'position': currentposition})

        # Receiving info
        if conn_to_main.poll():
            order = conn_to_main.recv()
            if (order['action'] == 'unpause'):
                backend.unpause_audio_stream()
            elif (order['action'] == 'pause'):
                backend.pause_audio_stream()
            elif (order['action'] == 'set_new_mood'):
                backend.find_song_based_on_mood(order['mood'])
                backend.get_audio_stream()
                backend.play_audio_stream()

                backend.prevposition = 0

                # Send to main song info
                conn_to_main.send({'title': backend.song['title'], 
                                   'thumbnailurl': backend.song['thumbnails'][0]['url'], 
                                   'length': backend.song['duration_seconds'], 
                                   'artist': backend.song['artists'][0]['name'], 
                                   'position': backend.get_stream_position()})
            elif (order['action'] == 'set_volume'):
                backend.set_audio_stream_volume(volume=order['volume'])
            elif (order['action'] == 'set_position'):
                backend.set_stream_position(order['position'])