from datetime import datetime
from multiprocessing import dummy
from random import sample
import time
from unicodedata import name
import PIL
import urllib.response
import urllib.parse
import urllib.request
from uuid import uuid4
from django.shortcuts import render
from django.http import HttpResponse, Http404
import asyncio
import json
import base64
import io
import threading
from django.http.response import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_exempt
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
import re
from .models import Reservation, Tag, GeneratedImage
from .prompt import make_prompt
from .gpuapi import send_to_gpu

# Create your views here.

@csrf_exempt
def check_result(request):

    # 最初のGETでアクセスしてCSRF情報を返す
    if request.method == 'GET':
        return JsonResponse({})

    # JSON文字列
    datas = json.loads(request.body)

    id = str(datas['id'])

    reservation = Reservation.objects.filter(reservation_id=id)

    if reservation.count() == 0:
        raise Http404('reservation does not exist')

    reservation = reservation.first()

    if reservation.state==1: # completed
        respath = []
        domain = 'https://' + get_current_site(request).domain
        for img in reservation.generated_image.all():
            respath.append(domain+img.image.url)
        ret = {
            'id': id,
            'completed':True,
          # 'prompt': reservation.prompt,
            'result':respath,
            }
    elif reservation.state==0: # inprogress
        queue_length = reservation.get_queue_length()
        ret = {
            'id': id,
            'completed':False,
          # 'prompt': reservation.prompt,
            'queue_length':queue_length
            }
    elif reservation.state == -1: # disabled by gpu missing
        gpu_is_active = send_to_gpu(reservation.prompt,id)
        if gpu_is_active:
            reservation.state = 0
            queue_length = reservation.get_queue_length()
            ret = {
                'id': id,
                'completed':False,
              # 'prompt': reservation.prompt,
                'queue_length':queue_length
                }
        else:
            ret = ret_sample(id,request)
    else:
        raise Http404('irregular reservation')

    response = JsonResponse(ret)

    return response

# @ensure_csrf_cookie
@csrf_exempt
def check_result_nodb(request):

    # 最初のGETでアクセスしてCSRF情報を返す
    if request.method == 'GET':
        return JsonResponse({})

    print(request.body)

    # JSON文字列
    datas = json.loads(request.body)

    id = str(datas['id'])

    id_num = re.sub(r'\D', '', id)

    if 'finish' in id: # completed
        ret = ret_sample(id,request)
        if 'aicon_reservation' in request.session:
            del request.session['aicon_reservation']
        else:
            print("no session data")

    elif id_num != '': # inprogress
        ret = {
            'id': id,
            'completed':False,
            'queue_length':int(id_num)
            }
    else:
        raise Http404('reservation disabled')


    response = JsonResponse(ret)

    return response



@csrf_exempt
def reserve(request):
    datas = json.loads(request.body)
    tags = datas['tags']

    if len(tags) == 0:
        return HttpResponse("invalid tags")

    id = str(uuid4())
    reservation = Reservation(reservation_id=id)
    reservation.save()
    for tag in tags:
        t,new = Tag.objects.get_or_create(name=tag)
        t.save()
        reservation.input_tags.add(t)
    reservation.save()

    threading.Thread(target=reserve_process,args=(id, tags, reservation)).start()

    ret = {'id':id}    
    response = JsonResponse(ret)
    return response


def reserve_process(id,tags,reservation):
    prompt = make_prompt(tags)
    reservation.prompt = prompt

    gpu_is_active = send_to_gpu(prompt,id)

    if gpu_is_active:
        print(f'{id} succeed to send gpu')
    else:
        print(f'{id} failed to send gpu')
        reservation.state = -1 # set disabled
    reservation.save()


@csrf_exempt
def save_generated_images(request):
    datas = json.loads(request.body)

    # print(datas)

    request_id = datas['id']
    num_images = int(datas['num_images'])

    reservations = Reservation.objects.filter(reservation_id=request_id)
    if reservations.count() > 0:
        reservation = reservations.first()
    else:
        reservation = None

    for i in range(num_images):
        if GeneratedImage.objects.filter(request_id=request_id,img_idx=i).exists():
            continue

        im_b64 = datas[str(i)]
        img_bytes = base64.b64decode(im_b64.encode('utf-8'))
        
        generated_image = GeneratedImage(request_id=request_id, img_idx=i)
        
        if reservation:
            generated_image.reservation = reservation

        buffer = io.BytesIO(img_bytes)
        generated_image.image.save(name=f"{request_id}_{i}.png", content=buffer)

    if reservation:
        reservation.state = 1
        reservation.save()
    ret = {'output': 'output_key'}
    response = JsonResponse(ret)
    return response

def ret_sample(id,request):
    domain = 'https://' + get_current_site(request).domain

    respath = [
        domain + '/static/dummy/dummy_0.png',
        domain + '/static/dummy/dummy_1.png',
        domain + '/static/dummy/dummy_2.png',
        domain + '/static/dummy/dummy_3.png',
        domain + '/static/dummy/dummy_4.png',
        domain + '/static/dummy/dummy_5.png',
        ]

    ret = {
        'id': id,
        'completed':True,
        'prompt': 'dummy prompt',
        'result':respath
        }
    return ret









        # if True:
        #     ss = [
        #     '/dummyImage/dummy_0.png',
        #     '/dummyImage/dummy_1.png',
        #     '/dummyImage/dummy_2.png',
        #     '/dummyImage/dummy_3.png',
        #     '/dummyImage/dummy_4.png',
        #     '/dummyImage/dummy_5.png',
        #     ]
        #     for i,s in enumerate(ss):
        #         if GeneratedImage.objects.filter(request_id=dummy_id,img_idx=i).exists():
        #             continue
        #         print(get_current_site(request))
        #         print(settings.STATIC_ROOT /settings.STATIC_ / s)
        #         img = PIL.Image.open(settings.STATIC_ROOT / s)
        #         print(img)
        #         buffer = io.BytesIO()
        #         img.save(fp=buffer, format='png')

        #         generated_image = GeneratedImage(request_id=dummy_id, img_idx=i)
        #         generated_image.reservation = reservation
        #         generated_image.save()

        #         generated_image.image.save(name=f'{dummy_id}_{i}', content=buffer)
        #         # generated_image.save()