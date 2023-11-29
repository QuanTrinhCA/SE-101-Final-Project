from multiprocessing import Process, Pipe
from backend import audio_backend
from emotiondection import emotion_detect
from ui import ui

if __name__ == '__main__':
    conn_to_ui,conn_to_main = Pipe()
    backend_process = Process(target=ui, args=(conn_to_main,))
    backend_process.start()
    conn_to_audio_backend,conn_to_main = Pipe()
    backend_process = Process(target=audio_backend, args=(conn_to_main,))
    backend_process.start()
    conn_to_emotion_detection,conn_to_main = Pipe()
    backend_process = Process(target=emotion_detect, args=(conn_to_main,))
    backend_process.start()
    conn_to_emotion_detection.send({'action': 'get_emotion'})
    emotion = ''
    position = -1
    while True:
        if (emotion != ''):
            if (position == -1):
                conn_to_audio_backend.send({'action': 'set_new_mood', 'mood': emotion})
                emotion = ''
                continue

        # Receiving info
        if conn_to_audio_backend.poll():
            info = conn_to_audio_backend.recv()
            sending_info = {}
            for key in info:
                if (key == 'position'):
                    position = info[key]
                    if (position > 0.9):
                        conn_to_emotion_detection.send({'action': 'get_emotion'})
                    sending_info['position'] = position
                if (key == 'title'):
                    sending_info['title'] = info[key]
                if (key == 'thumbnailurl'):
                    sending_info['thumbnailurl'] = info[key]
                if (key == 'length'):
                    sending_info['length'] = info[key]
                if (key == 'artist'):
                    sending_info['artist'] = info[key]
                conn_to_ui.send(sending_info)
        if conn_to_emotion_detection.poll():
            info = conn_to_emotion_detection.recv()
            for key in info:
                if (key == 'emotion'):
                    emotion = info[key]
        if conn_to_ui.poll():
            order = conn_to_ui.recv()
            sending_info = {'action': order['action']}
            if (order['action'] == 'set_volume'):
                sending_info['volume'] = order['volume']
            conn_to_audio_backend.send(sending_info)