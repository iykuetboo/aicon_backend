from datetime import datetime
from unicodedata import name
from urllib import response
from uuid import uuid4
from django.shortcuts import render
from django.http import HttpResponse, Http404
import json
import base64
import io
from django.http.response import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_exempt
from django.contrib.sites.shortcuts import get_current_site
import re
from .models import Reservation, Tag, GeneratedImage

# Create your views here.

@csrf_exempt
def check_result(request):

    # 最初のGETでアクセスしてCSRF情報を返す
    if request.method == 'GET':
        return JsonResponse({})

    # JSON文字列
    datas = json.loads(request.body)

    id = str(datas['id'])
    print('id',id)

    reservation = Reservation.objects.filter(reservation_id=id)

    if reservation.count() == 0:
        raise Http404('reservation does not exist')

    reservation = reservation.first()
    print('reservation',reservation, reservation.state)

    if reservation.is_completed(): # completed
        respath = []
        print(reservation.generated_image)
        print(reservation.generated_image.all())
        domain = 'https://' + get_current_site(request).domain
        for img in reservation.generated_image.all():
            
            respath.append(domain+img.image.url)

        ret = {
            'id': id,
            'completed':True,
            'result':respath
            }
        if 'aicon_reservation' in request.session:
            del request.session['aicon_reservation']
        else:
            print("no session data")


    elif reservation.is_inprogress(): # inprogress
        queue_length = reservation.get_queue_length()
        ret = {
            'id': id,
            'completed':False,
            'queue_length':queue_length
            }
    else:
        raise Http404('reservation disabled')

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
        domain = 'https://' + get_current_site(request).domain

        respath = [
            domain + '/static/dummyImage/icon_of_owl_kawaii_hi-resolusion_oil-painting_autumn_concept-art_00.png',
            domain + '/static/dummyImage/icon_of_owl_kawaii_hi-resolusion_oil-painting_autumn_concept-art_01.png',
            domain + '/static/dummyImage/icon_of_owl_kawaii_hi-resolusion_oil-painting_autumn_concept-art_02.png',
            domain + '/static/dummyImage/icon_of_owl_kawaii_hi-resolusion_oil-painting_autumn_concept-art_03.png',
            domain + '/static/dummyImage/icon_of_owl_kawaii_hi-resolusion_oil-painting_autumn_concept-art_04.png',
            domain + '/static/dummyImage/icon_of_owl_kawaii_hi-resolusion_oil-painting_autumn_concept-art_05.png',
            ]
        ret = {
            'id': id,
            'completed':True,
            'result':respath
            }

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
    # 最初のGETでアクセスしてCSRF情報を返す
    if request.method == 'GET':
        return JsonResponse({})

    # JSON文字列
    datas = json.loads(request.body)

    tags = datas['tags']

    # create reservation with id
    reservation = Reservation(reservation_id=str(uuid4()))
    for tag in tags:
        t,new = Tag.objects.get_or_create(name=tag)
        reservation.input_tags.add(t)

    reservation.save()

    id = reservation.pk

    if 'aicon_reservation' in request.session:
        print("same user !!", request.session)
    else:
        request.session['aicon_reservation'] = id
    
    queue_length = reservation.get_queue_length()
    
    ret = {'id':id, 'queue_length': queue_length}
    response = JsonResponse(ret)

    return response

@csrf_exempt
def save_generated_images(request):
    datas = json.loads(request.body)

    request_id = datas['id']
    num_images = datas['imagenum']

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

