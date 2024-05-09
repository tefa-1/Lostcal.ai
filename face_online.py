import face_recognition
import cv2
import os
import numpy as np
import requests
from io import BytesIO

class SimpleFacerec:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []

        # Resize frame for a faster speed
        self.frame_resizing = 0.25

    def load_encoding_images(self, images_dict):
        """
        Load encoding images from URLs
        :param images_dict: Dictionary containing names as keys and URLs as values
        """
        print("{} encoding images found.".format(len(images_dict)))

        for name, url in images_dict.items():
            try:
                response = requests.get(url)
                img = cv2.imdecode(np.frombuffer(response.content, np.uint8), -1)
                rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                # Get encoding
                img_encoding = face_recognition.face_encodings(rgb_img)[0]

                # Store name and encoding
                self.known_face_encodings.append(img_encoding)
                self.known_face_names.append(name)
                print(f"Encoding for {name} loaded.")
            except Exception as e:
                print(f"Error loading {name}: {e}")

        print("Encoding images loaded")

    def detect_known_faces(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        # Find all the faces and face encodings in the current frame of video
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            face_names.append(name)

        # Convert to numpy array to adjust coordinates with frame resizing quickly
        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing
        return face_locations.astype(int), face_names
