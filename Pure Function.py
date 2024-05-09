import requests
import numpy as np
import face_recognition
from PIL import Image
from io import BytesIO
from pymongo import MongoClient
import time

match_set = set()


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
        # print(f"Error: {e}")
        return False

    # Compare the face encodings
    result = face_recognition.compare_faces([face_encoding1], face_encoding2)
    return result[0]


def compare(image_list1, image_list2):
    for image_set2 in image_list2:
        for image_set1 in image_list1:
            match_count = 0
            for image1_url in image_set1[1]:
                if compare_faces(image1_url, image_set2[1]):
                    match_count += 1
                if match_count > (len(image_set1[1]) - 1) / 2:
                    print(f"Match found between {image_set2[0]} and {image_set1[0]}")
                    match_set.add((image_set2[0], image_set1[0]))
                    break
            # else:
            # print(f"No Match Between {image_set2[0]} and {image_set1[0]}")


def fetch_data_from_mongo(collection, field_name):
    cursor_lost = collection.find({}, {'_id': 1, f'{field_name}': 1})
    data_list = []

    for doc in cursor_lost:
        data_list.append([doc['_id'], doc[f'{field_name}']])

    return data_list


if __name__ == "__main__":
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['People']
    collection_lost = db['Personal Information']
    collection_found = db['Found']

    while True:
        lost_list = fetch_data_from_mongo(collection_lost, "Images")
        found_list = fetch_data_from_mongo(collection_found, "Image")

        print("Lost List:", lost_list)
        print("Found List:", found_list)

        compare(lost_list, found_list)

        print(match_set)
        print(
            "done\n ####################################################################################################################")
        time.sleep(5)
