import email
from email.policy import default
from importlib.metadata import requires
from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)
    name = models.TextField("name",default="hoge")

# class User(models.Model):
#     name = models.TextField(requires=True)
#     email = models.TextField()

