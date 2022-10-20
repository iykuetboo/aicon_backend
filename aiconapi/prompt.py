from ast import While
import requests
import json
import translators as ts
import time

app_id = "edca785dbae630a5989545cd0548dc197faecb06603e2826c18439a9c3fd8784"

art_styles = ["fantasy", "science fiction", "adventure", "drama", "steampank", "Ghibli", "Marvel", "Disney"]
national_styles = ["pixiv light novel","artstation deviantart"]
genarals = ["cinematic lighting", "beautiful composition", "detailed", "digital painting"]

materials = ["a ball-point pen art",
            "a pencil sketch",
            "a crayon painting",
            "an acrylic painting",
            "a watercolor painting",
            "an oil painting",
            "an ukiyo-e painting",
            "airbrush caricature",
            "a low poly illustration",
            "japanese anime",
            "pixel art",
            "3D"]

headers = {'Content-Type':'application/x-www-form-urlencoded'}

def make_prompt(tags):
    object = ts.google(tags[0])

    tag = " ".join(tags)
    print(tag)

    # select material
    score = []
    for text in materials:
            parameters = {
                        "app_id": app_id,
                        "text1": tag,
                        "text2": text
                        }
            cnt = 0
            while cnt < 4:
                cnt += 1
                try:
                    res = requests.post('https://labs.goo.ne.jp/api/textpair', headers=headers, json=parameters)
                    response = json.loads(res.text)
                    score.append(response["score"])
                    break
                except:
                    # time.sleep(0.5)
                    print('goo api try again.')
    material = materials[score.index(max(score))]

    # select art_style
    score = []
    for text in art_styles:
            parameters = {
                        "app_id": app_id,  
                        "text1": tag,
                        "text2": text
                        }
            cnt = 0
            while cnt < 4:
                cnt += 1
                try:
                    res = requests.post('https://labs.goo.ne.jp/api/textpair', headers=headers, json=parameters)
                    response = json.loads(res.text)
                    score.append(response["score"])
                    break
                except:
                    # time.sleep(0.5)
                    print('goo api try again.')
    art_style = art_styles[score.index(max(score))]

    # select national_style
    score = []
    for text in national_styles:
            parameters = {
                        "app_id": app_id,  
                        "text1": tag,
                        "text2": text
                        }
            cnt = 0
            while cnt < 4:
                cnt += 1
                try:
                    res = requests.post('https://labs.goo.ne.jp/api/textpair', headers=headers, json=parameters)
                    response = json.loads(res.text)
                    score.append(response["score"])
                    break
                except:
                    # time.sleep(0.5)
                    print('goo api try again.')
    national_style = national_styles[score.index(max(score))]
    prompt = "a SNS icon of " + object.lower()+ " " + material + " " + art_style + " " + national_style + " " + " ".join(genarals) + " " + ts.google(" ".join(tags[1:])).lower()
    # print("tags: ", tags)
    # print("prompt: ", prompt)
    return prompt

import sys

if __name__=="__main__":
    print(sys.argv[1:])
    print(make_prompt(sys.argv[1:]))