import requests
import face_recognition
from io import BytesIO
import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("localhost", 27017)
db = client["People"]
collection1 = db["Personal Information"]
collection2 = db["Found"]

def compare_faces(image1_url, image2_url):
    try:
        response1 = requests.get(image1_url)
        image1 = face_recognition.load_image_file(BytesIO(response1.content))

        response2 = requests.get(image2_url)
        image2 = face_recognition.load_image_file(BytesIO(response2.content))

        face_locations1 = face_recognition.face_locations(image1)
        face_encodings1 = face_recognition.face_encodings(image1, face_locations1)

        face_locations2 = face_recognition.face_locations(image2)
        face_encodings2 = face_recognition.face_encodings(image2, face_locations2)

        match_count = 0
        for encoding1 in face_encodings1:
            for encoding2 in face_encodings2:
                result = face_recognition.compare_faces([encoding1], encoding2)
                if result[0] == True:
                    match_count += 1

        if match_count > len(face_encodings1) / 2:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def process_comparison(image_set1, image_set2):
    match_count = 0
    for image1_url in image_set1:
        if compare_faces(image1_url, image_set2['urls'][0]):
            match_count += 1
            if match_count > (len(image_set1['urls']) - 1) / 2:
                print(f"Match found with more than half of the photos in {image_set2['name']} and {image_set1['name']}")
                return True
    print(f"No match found between {image_set2['name']} and {image_set1['name']}")

def compare_images(image_list1, image_list2):
    for image_set2 in image_list2:
        for image_set1 in image_list1:
             if process_comparison(image_set1, image_set2):
                 break

def fetch_data_from_mongo(collection, field_name):
    cursor_lost = collection.find({}, {'_id': 1, f'{field_name}': 1})

    list = []

    for doc in cursor_lost:
        list.append([doc['_id'], doc[f'{field_name}']])

    return list

# Fetching data from MongoDB
image_list1 = fetch_data_from_mongo(collection1, 'Images')
image_list2 = fetch_data_from_mongo(collection2, 'Image')


print(image_list1)
print(image_list2)
# Example usage
#compare_images(image_list1, image_list2)
