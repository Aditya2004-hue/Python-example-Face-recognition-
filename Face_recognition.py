import requests
import numpy as np
import os
import cv2
import pickle
import json

url="http://localhost:9900/v1/face2embedding"
api_url = "http://localhost:9900/v1/compareface"
image_path = os.path.join("brainypi-ai-api-examples", "sample_inputs", "images", "face.jpg")

image = cv2.imread(image_path)
retval,image_file = cv2.imencode('.jpg', image)
if retval:
    encoded_image = image_file.tobytes()
    print("encoded")
else:
    print("Image encoding failed.")

response = requests.post(url, encoded_image)

if response.status_code == 200:
    response_data = response.json()
    embeddings=response_data["result"]["faces"][0]["embeddings"]
    with open("/home/pi/face2_encoding.pkl", "wb") as f:
        pickle.dump(embeddings, f)
    with open("/home/pi/face2_encoding.pkl", 'rb') as file:
        face2_embeddings = pickle.load(file)

    with open("/home/pi/face_encoding.pkl", "rb") as file:
         face1_embeddings = pickle.load(file)

    data = {
                "face1": {
                    "embeddings": face1_embeddings
                 },
                "face2": {
                    "embeddings": face2_embeddings
                 }
           }

    js1=json.dumps(data)
    print("Request Body created.")

    response1 = requests.post(api_url, js1)

    if response1.status_code == 200:
        response_data1 = response1.json()
        print(response_data1)
        confidence=response_data1["result"]["confidence"]
        if(confidence>0.1):
           print("face verified successfully")
        else:
           print("face not matched")

    else:
        print("error in verification")
        print("Error: Response received from the server {}".format(response1.status_code))



else:
    print("Error: Response received from the server {}".format(response.status_code))
print("Code execution completed.")
