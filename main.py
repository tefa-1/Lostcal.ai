from flask import Flask, jsonify
import requests
import numpy as np
import face_recognition
from PIL import Image
from io import BytesIO
from pymongo import MongoClient
import threading
import os
import time

app = Flask(__name__)

match_set = set()
lock = threading.Lock()

MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://newUser:TXk.ch28bNCds5c@cluster0.ir11p5g.mongodb.net/lostcal")
CLEAR_INTERVAL = 3600


def compare_faces(image1_url, image2_url):
    try:
        response = requests.get(image1_url)
        image = Image.open(BytesIO(response.content))
        image1 = np.array(image)
        face_encoding1 = face_recognition.face_encodings(image1)[0]

        response = requests.get(image2_url)
        image = Image.open(BytesIO(response.content))
        image2 = np.array(image)
        face_encoding2 = face_recognition.face_encodings(image2)[0]
    except Exception as e:
        return False

    result = face_recognition.compare_faces([face_encoding1], face_encoding2)
    return result[0]


def compare(lost_list, found_list):
    global match_set
    for image_set2 in found_list:
        for image_set1 in lost_list:
            match_count = 0
            for image1_url in image_set1[1]:
                if compare_faces(image1_url, image_set2[1]):
                    match_count += 1
                if match_count > (len(image_set1[1]) - 1) / 2:
                    with lock:
                        print(f"match found between {image_set2[0]} and {image_set1[0]}")
                        match_set.add((str(image_set2[0]), str(image_set1[0])))
                    break


def fetch_data_from_mongo(collection, field_name):
    cursor = collection.find({}, {'_id': 1, f'{field_name}': 1})
    data_list = []
    for doc in cursor:
        data_list.append([doc['_id'], doc[f'{field_name}']])
    return data_list


def compare_images():
    client = MongoClient(MONGO_URI)
    db = client['lostcal']
    collection_lost = db['missingpepoles']
    collection_found = db['lostpepoles']
    while True:
        lost_list = fetch_data_from_mongo(collection_lost, "img")
        found_list = fetch_data_from_mongo(collection_found, "img")
        compare(lost_list, found_list)


def clear_match_set():
    global match_set
    while True:
        time.sleep(CLEAR_INTERVAL)
        with lock:
            match_set.clear()
            print("Match set cleared!")


@app.get("/")
def home():
    return {"health_check": "OK", "model_version": "1.0"}


@app.route('/matches', methods=['GET'])
def get_matches():
    global match_set
    with lock:
        return jsonify(list(match_set))


if __name__ == "__main__":
    comparison_thread = threading.Thread(target=compare_images)
    comparison_thread.daemon = True
    comparison_thread.start()

    clear_match_set_thread = threading.Thread(target=clear_match_set)
    clear_match_set_thread.daemon = True
    clear_match_set_thread.start()

    app.run(host="0.0.0.0", port=8080, debug=False)
