# face_app/train.py
import os
import cv2
import face_recognition
import numpy as np
import pickle

def train_faces(image_folder, output_model):
    encodings = []
    names = []

    for filename in os.listdir(image_folder):
        img_path = os.path.join(image_folder, filename)
        img = face_recognition.load_image_file(img_path)
        encoding = face_recognition.face_encodings(img)[0]
        name = os.path.splitext(filename)[0]
        encodings.append(encoding)
        names.append(name)

    data = {"encodings": encodings, "names": names}
    with open(output_model, "wb") as f:
        pickle.dump(data, f)

train_faces("media/dataset/user_images/", "trained_model/encodings.pickle")
