from django.urls import path

from . import views



urlpatterns = [
path('reserve',views.reserve, name='reserve'),
path('reserve_from_question',views.reserve_from_question, name='reservefromquestion'),
path('check_result',views.check_result, name='checkresult'),
path('check_result_nodb',views.check_result_nodb, name='checkresultnodb'),
path('save_generated_images',views.save_generated_images, name='savegeneratedimages'),
]
