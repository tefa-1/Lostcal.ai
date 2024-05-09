from flask import Flask, request, jsonify
import requests
import numpy as np
import face_recognition
from PIL import Image
from io import BytesIO

app = Flask(__name__)


# Function to compare faces
def compare_faces(image1_url, image2_url):
    response1 = requests.get(image1_url)
    image1 = Image.open(BytesIO(response1.content))
    image1 = np.array(image1)

    response2 = requests.get(image2_url)
    image2 = Image.open(BytesIO(response2.content))
    image2 = np.array(image2)

    # Find face locations and encodings in each image
    face_locations1 = face_recognition.face_locations(image1)
    face_encodings1 = face_recognition.face_encodings(image1, face_locations1)

    face_locations2 = face_recognition.face_locations(image2)
    face_encodings2 = face_recognition.face_encodings(image2, face_locations2)

    # Compare faces
    for encoding1 in face_encodings1:
        for encoding2 in face_encodings2:
            # Compare faces
            result = face_recognition.compare_faces([encoding1], encoding2)
            if result[0] == True:
                return True  # Faces match
    return False  # Faces do not match


# Route to handle the face comparison request
@app.route('/compare_faces', methods=['POST'])
def handle_compare_faces():
    # Get image URLs from the request
    data = request.json
    image1_url = data.get('image1_url')
    image2_url = data.get('image2_url')

    # Perform face comparison
    result = compare_faces(image1_url, image2_url)

    # Return the result
    return jsonify({'result': result})


if __name__ == '__main__':
    app.run(debug=True)

























image_list1 = [["Will Smith",
                "https://media.npr.org/assets/img/2021/11/10/will-smith-new-headshot-credit-lorenzo-agius_wide-fce30e30fbf83a2c586848fa991d1d61ab768cd2-s1100-c50.jpg",
                "https://media-cldnry.s-nbcnews.com/image/upload/t_focal-360x700,f_auto,q_auto:best/newscms/2016_01/921591/ss-160104-will-smith-tease.jpg",
                "https://www.famousbirthdays.com/headshots/will-smith-8.jpg"
                ],
               ["Robert Downey Jr",
                "https://static.wikia.nocookie.net/ironman/images/7/79/Photo%28906%29.jpg/revision/latest?cb=20141019122536",
                "https://cdn.shopify.com/s/files/1/0523/8521/8751/files/c5c11ebc-954e-4d9c-abf9-d4f47d88fea4.jpg",
                "https://www.koimoi.com/wp-content/new-galleries/2023/05/when-robert-downey-jr-revealed-that-he-jrked-off-compulsively-said-rode-it-for-everything-it-was-worth.jpg"
                ],
               ["Tom Hardy",
                "https://media.gq.com/photos/56d4902a9acdcf20275ef34c/16:9/w_2560%2Cc_limit/tom-hardy-lead-840.jpg",
                "https://www.indiewire.com/wp-content/uploads/2014/06/tom-hardy.jpg?w=350",
                "https://townsquare.media/site/442/files/2014/09/tom-hardy-tag-page.jpg?w=780&q=75"
                ],
               ["Tom Holland",
                "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Tom_Holland_by_Gage_Skidmore.jpg/800px-Tom_Holland_by_Gage_Skidmore.jpg",
                "https://static1.srcdn.com/wordpress/wp-content/uploads/2023/06/tom-holland-as-peter-parker-in-spider-man-no-way-home.jpg",
                "https://ew.com/thmb/jxSyI2WFhHeFEtD_92G6J4fkRII=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/gettyimages-1158532533-2000-ef76aa55f7ac4b948ffb7e2f08a01f00.jpg"
                ],
               ["Tom Cruise",
                "https://m.media-amazon.com/images/M/MV5BYTFlOTdjMjgtNmY0ZC00MDgxLThjNmEtZGIxZTQyZDdkMTRjXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_.jpg",
                "https://www.theglobeandmail.com/resizer/v2/HYQ5ZVERUVDJXPIYPNK2EMFUVI.JPG?auth=2cdf0f83bb56a6ab2232d1cd2a92f44574b4a788175aef2e08c6962806f4a43b&width=1500&quality=80",
                "https://hips.hearstapps.com/hmg-prod/images/tom-cruise-attends-the-european-premiere-of-rock-of-ages-at-news-photo-1674570476.jpg"
                ],
               ["Morgan Freeman",
                "https://upload.wikimedia.org/wikipedia/commons/4/42/Morgan_Freeman_at_The_Pentagon_on_2_August_2023_-_230802-D-PM193-3363_%28cropped%29.jpg",
                "https://goldenglobes.com/wp-content/uploads/2023/10/Morgan-Freeman-by-Vera-Anderson.jpg",
                "https://static.wikia.nocookie.net/batman/images/c/cc/Morgan_Freeman.jpg/revision/latest?cb=20150911163015"
                ],
               ["Scarlet Johansson",
                "https://image-cdn.hypb.st/https%3A%2F%2Fhypebeast.com%2Fimage%2F2023%2F04%2Fscarlett-johansson-done-with-marvel-black-widow-001.jpg?cbr=1&q=90",
                "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Scarlett_Johansson_2%2C_2012.jpg/640px-Scarlett_Johansson_2%2C_2012.jpg",
                "https://static.wikia.nocookie.net/ideas/images/0/06/Scarlett-Johansson-635.jpg/revision/latest?cb=20181031004406"
                ],
               ["Megan Fox",
                "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Megan_Fox_2014.jpg/1200px-Megan_Fox_2014.jpg",
                "https://cdn.britannica.com/75/191075-050-DC41EAFD/Megan-Fox-2012.jpg",
                "https://phantom-marca.unidadeditorial.es/ee97b3f6b71aa9f358c2270152766784/crop/0x0/2044x1363/resize/828/f/jpg/assets/multimedia/imagenes/2023/11/09/16995614796313.jpg"
                ],
               ["Jacky Chan",
                "https://media.themoviedb.org/t/p/w500/nraZoTzwJQPHspAVsKfgl3RXKKa.jpg",
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSnTLr2cNdiNWdgS3gON3TBkeB35K8aKddPuw&usqp=CAU",
                "https://imageio.forbes.com/specials-images/imageserve/5ed66ef9d1db3e000665f5da/0x0.jpg?format=jpg&crop=1080,1080,x0,y0,safe&height=416&width=416&fit=bounds"
                ],
               ["Brad Pitt",
                "https://resizing.flixster.com/-XZAfHZM39UwaGJIFWKAE8fS0ak=/v3/t/assets/1366_v9_bc.jpg",
                "https://media.architecturaldigest.com/photos/64249dbb5b98a5c5b21bc25d/16:9/w_2560%2Cc_limit/GettyImages-1469289926.jpg",
                "https://i0.wp.com/culturacolectiva.com/wp-content/uploads/2023/07/brad-pitt-por-que-aparece-actor-internet.jpg"
                ]
               ]

image_list2 = [["Scarlet", "https://img.brut.media/thumbnail/the-life-of-scarlett-johansson-af9953f9-07db-48a7-93be-ff25144c820c.230426_FR_CANNES_SCARLETT_JOHANSSON_UPDATE_2023_US_VERT_V2.00_10_33_00.Still015-274b8975-5213-4b24-8f51-f151eb9830c9-portrait.jpg"],
               ["Jack", "https://variety.com/wp-content/uploads/2022/12/Jackie_Chan_v4.png"],
               ["Tom", "https://img.asmedia.epimg.net/resizer/v2/Y6AOLVC6EAR6KPEZAHEJXUVRE4.jpg?auth=ec64f53456a7fe0e7ed56fc885882028f449aba4da6c9921aa0868a719c25ec4&width=1200&height=1200&focal=2252%2C1084"]]
