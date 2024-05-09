import requests

# Make a GET request to the API endpoint
response = requests.get('http://127.0.0.1:5000/matches')

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Get the match_set data from the response
    match_set = response.json()
    print("Match Set:", match_set)
else:
    print("Error:", response.text)
