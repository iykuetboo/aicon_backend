from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    print(request)
    return HttpResponse("Hello, world. You're at the save_image index.")

def test(request):
    print(request)
    return HttpResponse("test")
