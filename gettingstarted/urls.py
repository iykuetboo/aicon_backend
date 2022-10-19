from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

import hello.views
import aiconapi.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name='blog')
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path('', hello.views.index, name='index'),
    path('test/', hello.views.test, name='test'),
    path('db/', hello.views.db, name='db'),

    path('aiconapi/check_result',aiconapi.views.check_result, name='checkresult'),
    path('aiconapi/check_result_nodb',aiconapi.views.check_result_nodb, name='checkresultnodb'),
    
    path('save_image/', include('save_image.urls')),

    path('admin/', admin.site.urls),
]+static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

