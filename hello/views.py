from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    response = HttpResponse('Hello from Python!')
    return response

    
def test(request):
    # return HttpResponse('Hello from Python!')
    response = HttpResponse('Test Response!')
    return response


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
