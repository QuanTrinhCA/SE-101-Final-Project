import vlc, ytmusicapi, yt_dlp, random

def find_song_based_on_mood(mood):
    mood_index = 0
    with ytmusicapi.YTMusic() as ytmusic:
        if mood == 'happy':
            mood_index = 5
        elif mood == 'ur mom':
            mood_index = 69
        playlistlist = ytmusic.get_mood_playlists(params=ytmusic.get_mood_categories()["Moods & moments"][mood_index]['params'])
        luckyplaylist = ytmusic.get_playlist(playlistId=playlistlist[random.randint(0,len(playlistlist) - 1)]['playlistId'])
        luckysong = luckyplaylist['tracks'][random.randint(0, len(luckyplaylist['tracks']) - 1)]
    return luckysong

def get_song_info(name):
    with ytmusicapi.YTMusic() as ytmusic:
        return ytmusic.get_song(ytmusic.search(query=name, filter="songs")[0]['videoId'])

def get_audio_stream(videoId):
    ydl_opts = {
        'extractor_args': {
            'youtube': {
                'skip': ['hls,dash,translated_subs'],
                'player_client': ['android_music']
                }
        }
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for format in ydl.sanitize_info(ydl.extract_info(f"https://music.youtube.com/watch?v=" + videoId, download=False, process=False, ie_key="Youtube"))['formats']:
            if format['format_id'] == '251':
                return format['url']

def init_vlc_player():
    return vlc.MediaPlayer()

def play_audio_stream(player, url):
    player.set_mrl(url)
    player.play()

def pause_audio_stream(player):
    player.pause()

def unpause_audio_stream(player):
    player.play()

def set_audio_stream_volume(player, volume):
    player.audio_set_volume(volume)

def audio_backend(conn_to_main):
    player = init_vlc_player()
    while True:
        order = conn_to_main.recv()
        if (order['action'] == 'unpause'):
            unpause_audio_stream(player=player)
            continue
        elif (order['action'] == 'pause'):
            pause_audio_stream(player=player)
            continue
        elif (order['action'] == 'set_new_mood'):
            song = find_song_based_on_mood(order['mood'])
            play_audio_stream(player=player, url=get_audio_stream(song['videoId']))
            continue
        elif (order['action'] == 'set_volume'):
            set_audio_stream_volume(player=player, volume=order['volume'])
            continue