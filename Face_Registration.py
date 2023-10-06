import requests
import numpy as np
import os
import cv2
import pickle

api_url = "http://localhost:9900/v1/face2embedding"
image_path = os.path.join("brainypi-ai-api-examples", "sample_inputs", "images", "face.jpg")

image = cv2.imread(image_path)
retval,image_file = cv2.imencode('.jpg', image)
if retval:
    encoded_image = image_file.tobytes()
    print("encoded")
else:
    print("Image encoding failed.")

response = requests.post(api_url, encoded_image)

if response.status_code == 200:
    response_data = response.json()
    embeddings=response_data["result"]["faces"][0]["embeddings"]
    encoding_file = "/home/pi/face_encoding.pkl"
    with open(encoding_file, "wb") as f:
        pickle.dump(embeddings, f)
    with open("/home/pi/face_encoding.pkl", 'rb') as file:
        data = pickle.load(file)
    print(data)
    print("Face registered successfully.")

else:
    print("Error: Response received from the server {}".format(response.status_code))
print("Code execution completed.")

