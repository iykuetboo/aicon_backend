import base64
import json   
import glob                 
import sys

import requests
import time
# {id:10, imagenum:5, 0:<byte>, ... , 4: <byte>}

def send_image(id):
    api = 'http://localhost:8000/aiconapi/save_generated_images'
    images = {}
    images["id"] = id
    image_paths = glob.glob("static/dummyImage/*")
    images["imagenum"] = len(image_paths)
    for i, f in enumerate(image_paths):
        with open(f, "rb") as f:
            images[str(i)] = base64.b64encode(f.read()).decode("utf8")
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    payload = json.dumps(images)
    while True:
        try:
            response = requests.post(api, data=payload, headers=headers)
            print(response.json())
            break
        except:
            time.sleep(0.5)

if __name__=="__main__":
    send_image(sys.argv[-1])
