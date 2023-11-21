from multiprocessing import Process, Pipe
from backend import audio_backend
from time import sleep

if __name__ == '__main__':
    parent_conn,child_conn = Pipe()
    backend_process = Process(target=audio_backend, args=(child_conn,))
    backend_process.start()
    parent_conn.send({'action': 'set_new_mood', 'mood': 'happy'})
    sleep(20)
    parent_conn.send({'action': 'pause'})
    sleep(5)
    parent_conn.send({'action': 'unpause'})
    sleep(5)
    parent_conn.send({'action': 'set_volume', 'volume': 50})
    sleep(5)
    parent_conn.send({'action': 'set_volume', 'volume': 0})
    sleep(5)
    parent_conn.send({'action': 'set_volume', 'volume': 100})
    sleep(100000)