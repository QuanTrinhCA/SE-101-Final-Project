import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import cv2
from deepface import DeepFace
from time import sleep

def emotion_detect(conn_to_main):
    # Classifier gives (x,y), width and height
    face_classifier = cv2.CascadeClassifier()
    face_classifier.load(cv2.samples.findFile("haarcascade_frontalface_default.xml"))

    # Capture video source (laptop webcam, external webcam, etc)
    cap = cv2.VideoCapture(1)

    while True:
        order = conn_to_main.recv()
        if (order['action'] == 'get_emotion'):
            frame = cv2.VideoCapture(1).read()

            # Give deepface an image so that it returns an emotion
            response = DeepFace.analyze(frame, actions=("emotion",), enforce_detection=False)

            conn_to_main.send({'emotion': response[0]['dominant_emotion']})

            continue
        elif (order['action'] == 'terminate'):
            cap.release()
            cv2.destroyAllWindows()
            
            conn_to_main.send({'result': 'ok'})