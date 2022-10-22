from django.contrib import admin
from .models import *

from django.db.models.functions import Lower

# Register your models here.


# class ReservationAdmin(admin.ModelAdmin):
#     def get_ordering(self, request):
#         return [Lower('created_at')] 

admin.site.register(Reservation)
admin.site.register(Tag)
admin.site.register(GeneratedImage)

