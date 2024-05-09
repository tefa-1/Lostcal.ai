from flask import Flask, jsonify
import requests
import numpy as np
import face_recognition
from PIL import Image
from io import BytesIO
from pymongo import MongoClient
import threading
import time

app = Flask(__name__)

match_set = set()
lock = threading.Lock()


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
    client = MongoClient('mongodb://localhost:27017/')
    db = client['People']
    collection_lost = db['Personal Information']
    collection_found = db['Found']
    while True:
        lost_list = fetch_data_from_mongo(collection_lost, "Images")
        found_list = fetch_data_from_mongo(collection_found, "Image")
        compare(lost_list, found_list)
        time.sleep(60)  # Adjust the time interval as needed


@app.route('/matches', methods=['GET'])
def get_matches():
    global match_set
    with lock:
        return jsonify(list(match_set))


if __name__ == "__main__":
    comparison_thread = threading.Thread(target=compare_images)
    comparison_thread.daemon = True
    comparison_thread.start()

    app.run(debug=True)
