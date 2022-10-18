from datetime import datetime
from unicodedata import name
from urllib import response
from uuid import uuid4
from django.shortcuts import render
from django.http import HttpResponse, Http404
import json
from django.http.response import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.sites.shortcuts import get_current_site
import re
from .models import Reservation, Tag

# Create your views here.

@ensure_csrf_cookie
def check_result(request):

    # 最初のGETでアクセスしてCSRF情報を返す
    if request.method == 'GET':
        return JsonResponse({})

    # JSON文字列
    datas = json.loads(request.body)

    id = str(datas["id"])
    print("id",id)

    print("Reservation.objects",Reservation.objects)
    print("Reservation.objects",Reservation.objects.count())
    print("Reservation.objects",Reservation.objects.first())
    print("Reservation.objects",Reservation.objects.first().reservation_id)
    print("Reservation.objects",id)

    reservation = Reservation.objects.filter(reservation_id=id)
    
    print("reservation",reservation)
    print("reservation",reservation.count())

    if reservation.count() == 0:
        raise Http404("reservation does not exist")

    reservation = reservation[0]

    if reservation.state==1: # completed
        respath = []
        print(reservation.result_image)
        print(reservation.result_image.all())
        domain = get_current_site(request).domain
        for img in reservation.result_image.all():
            
            respath.append(domain+img.image.url)

        ret = {
            "id": id,
            "completed":True,
            "result":respath
            }

    elif reservation.state==0: # inprogress
        queue_length = Reservation.objects.filter(state=0,created_at__lt=reservation.created_at).count()
        ret = {
            "id": id,
            "completed":True,
            "queue_length":queue_length
            }
    else:
        raise Http404("reservation disabled")

    response = JsonResponse(ret)

    return response

@ensure_csrf_cookie
def check_result_nodb(request):

    # 最初のGETでアクセスしてCSRF情報を返す
    if request.method == 'GET':
        return JsonResponse({})

    # JSON文字列
    datas = json.loads(request.body)

    id = str(datas["id"])

    id_num = re.sub(r"\D", "", id)

    if "finish" in id: # completed
        domain = get_current_site(request).domain

        respath = [
            domain + "/static/dummyImage/icon_of_owl_kawaii_hi-resolusion_oil-painting_autumn_concept-art_00.png",
            domain + "/static/dummyImage/icon_of_owl_kawaii_hi-resolusion_oil-painting_autumn_concept-art_01.png",
            domain + "/static/dummyImage/icon_of_owl_kawaii_hi-resolusion_oil-painting_autumn_concept-art_02.png",
            domain + "/static/dummyImage/icon_of_owl_kawaii_hi-resolusion_oil-painting_autumn_concept-art_03.png",
            domain + "/static/dummyImage/icon_of_owl_kawaii_hi-resolusion_oil-painting_autumn_concept-art_04.png",
            domain + "/static/dummyImage/icon_of_owl_kawaii_hi-resolusion_oil-painting_autumn_concept-art_05.png",
            ]
        ret = {
            "id": id,
            "completed":True,
            "result":respath
            }

    elif id_num != "": # inprogress
        ret = {
            "id": id,
            "completed":True,
            "queue_length":int(id_num)
            }
    else:
        raise Http404("reservation disabled")


    response = JsonResponse(ret)

    return response



@ensure_csrf_cookie
def reserve(request):

    # 最初のGETでアクセスしてCSRF情報を返す
    if request.method == 'GET':
        return JsonResponse({})

    # JSON文字列
    datas = json.loads(request.body)

    tags = datas["tags"]

    # create reservation with id
    reservation = Reservation(id=str(uuid4()))
    for tag in tags:
        t,new = Tag.get_or_create(name=tag)
        reservation.input_tags.add(t)

    reservation.save()

    id = reservation.pk
    

    ret = {"id":id, "queue_length": 5}
    response = JsonResponse(ret)

    return response