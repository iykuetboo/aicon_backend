from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

from . import views



urlpatterns = [
path('reserve',views.reserve, name='reserve'),
path('check_result',views.check_result, name='checkresult'),
path('check_result_nodb',views.check_result_nodb, name='checkresultnodb'),
path('save_generated_images',views.save_generated_images, name='savegeneratedimages'),
]
