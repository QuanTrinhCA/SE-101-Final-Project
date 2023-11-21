from multiprocessing import Process, Pipe
from backend import audio_backend
from emotiondection import emotion_detect
from time import sleep

if __name__ == '__main__':
    conn_to_audio_backend,conn_to_main = Pipe()
    backend_process = Process(target=audio_backend, args=(conn_to_main,))
    backend_process.start()
    conn_to_emotion_detection,conn_to_main = Pipe()
    backend_process = Process(target=emotion_detect, args=(conn_to_main,))
    backend_process.start()
    conn_to_audio_backend.send({'action': 'set_new_mood', 'mood': 'happy'})
    sleep(20)
    conn_to_audio_backend.send({'action': 'pause'})
    sleep(5)
    conn_to_audio_backend.send({'action': 'unpause'})
    sleep(5)
    conn_to_audio_backend.send({'action': 'set_volume', 'volume': 50})
    sleep(5)
    conn_to_audio_backend.send({'action': 'set_volume', 'volume': 0})
    sleep(5)
    conn_to_audio_backend.send({'action': 'set_volume', 'volume': 100})
    sleep(100000)