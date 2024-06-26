Face Recognition Web Service Documentation
Overview
This project provides a Flask-based web service for face recognition, capable of comparing faces from URLs and identifying matches between two MongoDB collections: one for missing people and one for found people. It also offers an API endpoint to retrieve the current set of matches.
Prerequisites
Before running the project, ensure you have the following installed:
•	Python 3.6 or later
•	Flask
•	Requests
•	NumPy
•	face_recognition
•	Pillow
•	PyMongo
You can install the required libraries using pip:
pip install Flask requests numpy face_recognition Pillow pymongo
Environment Setup
Set up the required MongoDB URI as an environment variable:
export MONGO_URI="your_mongo_url"
If the environment variable is not set, the script will use a default MongoDB URI.

Main Application Script (app.py)
Description
The main script sets up a Flask web server with endpoints to check the health status and retrieve face match results. It also includes background threads to continuously compare faces and clear the match set at regular intervals.
Endpoints
•	GET /: Health check endpoint to ensure the server is running.
•	GET /matches: Endpoint to retrieve the current set of face matches.
Functions
1.	compare_faces(image1_url, image2_url):
o	Downloads images from the provided URLs and compares the faces.
o	Returns True if the faces match, otherwise False.
2.	compare(lost_list, found_list):
o	Compares faces from two lists of images and updates the global match set if matches are found.
3.	fetch_data_from_mongo(collection, field_name):
o	Fetches data from the specified MongoDB collection and returns it as a list of IDs and image URLs.
4.	compare_images():
o	Continuously fetches data from MongoDB collections and compares faces.
5.	clear_match_set():
o	Clears the global match set at regular intervals (every hour).
Running the Project
1.	Set the MONGO_URI environment variable to your MongoDB connection string.
2.	Run the main script:
python main.py
3.	Access the health check endpoint:
curl http://localhost:8080/
4.	Retrieve face match results:
curl http://localhost:8080/matches
Conclusion
This project provides a web service for face recognition, continuously comparing faces from MongoDB collections and exposing match results through a REST API. It can be extended and customized further based on specific requirements
