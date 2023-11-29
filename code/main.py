from multiprocessing import Process, Pipe
from backend import audio_backend
from emotiondection import emotion_detect

if __name__ == '__main__':
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
            for key in info:
                if (key == 'position'):
                    position = info[key]
                    if (position > 0.9):
                        conn_to_emotion_detection.send({'action': 'get_emotion'})
                    # Send to UI
                if (key == 'title'):
                    print(info[key])
                    # Send to UI
                if (key == 'thumbnailurl'):
                    print(info[key])
                    # Send to UI
                if (key == 'length'):
                    print(info[key])
                    # Send to UI
                if (key == 'artist'):
                    print(info[key])
                    # Send to UI
        if conn_to_emotion_detection.poll():
            info = conn_to_emotion_detection.recv()
            for key in info:
                if (key == 'emotion'):
                    emotion = info[key]