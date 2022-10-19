import io
import json
import base64
import logging
import numpy as np
from PIL import Image

from django.core.files import File
# from django.core.files import ImageFile
from django.core.files.images import ImageFile
from django.conf import settings
from django.conf.urls.static import static

from gettingstarted.wsgi import *
from save_image.models import GeneratedImage

from flask import Flask, request, jsonify, abort

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)


@app.route("/test", methods=['POST'])
def test_method():

    request_id = request.json['id']
    num_images = request.json['imagenum']

    for i in range(num_images):
        if GeneratedImage.objects.filter(request_id=request_id).filter(img_idx=i).exists():
            continue
        im_b64 = request.json[str(i)]
        img_bytes = base64.b64decode(im_b64.encode('utf-8'))
        img = Image.open(io.BytesIO(img_bytes))
        
        # buffer = io.BytesIO()
        # img_bytes.save(fp=buffer, format="png")
        # generated_image.image.save(name="いい感じの名前", content=buffer)
        generated_image = GeneratedImage(request_id=0, img_idx=0, img_url='adf')
        generated_image.save()

        buffer = io.BytesIO(img_bytes)
        generated_image.image.save(name=f"hoge{i}.png", content=buffer)


        # img_url = f'{settings.MEDIA_ROOT}/{request_id}_{i}.png'
        # img.save(img_url)
        # breakpoint()
        # img_arr = np.asarray(img)
        # print('img shape', img_arr.shape)
        # generated_image = GeneratedImage(request_id=request_id, img_idx=i, img_bytes=img_bytes)

        # generated_image = GeneratedImage(request_id=request_id, img_idx=i, img_url=img_url)
        # generated_image.save()


    result_dict = {'output': 'output_key'}
    return result_dict


def run_server_api():
    app.run(host='0.0.0.0', port=8080)


if __name__ == "__main__":
    run_server_api()
