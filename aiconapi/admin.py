from django.contrib import admin
from .models import *

from django.db.models.functions import Lower

# Register your models here.


class ReservationAdmin(admin.ModelAdmin):
    def disable_action(self,request,queryset):
        queryset.update(state=-1)
    actions=['disable_action']

admin.site.register(Reservation,ReservationAdmin)
admin.site.register(Tag)
admin.site.register(GeneratedImage)

