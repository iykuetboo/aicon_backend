from distutils.command.upload import upload
from email.policy import default
from enum import unique
from http import server
from importlib.metadata import requires
from random import choices
from unicodedata import name
from unittest import result
from django.db import models
import uuid

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=128,primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Reservation(models.Model):
    reservation_id = models.CharField(max_length=128,unique=True)
    input_tags = models.ManyToManyField(Tag)
    prompt = models.TextField(blank=True,default="")

    state_chioces = (
        (0,'inprocessing'), (1,'completed'), (-1,'desabled')
    )
    state = models.IntegerField(choices=state_chioces,blank=False,default=0)
    last_checked = models.DateTimeField(blank=True,null=True)
    queue_length = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "reservation_" + self.reservation_id

class Result(models.Model):
    name = models.CharField(max_length=256)
    image = models.ImageField(upload_to='images/result')
    reservation = models.ForeignKey(Reservation,on_delete=models.DO_NOTHING,related_name='result_image')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
