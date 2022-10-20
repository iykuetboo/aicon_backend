from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

import hello.views

urlpatterns = [
    path('', hello.views.index, name='index'),
    path('test/', hello.views.test, name='test'),
    path('db/', hello.views.db, name='db'),

    path('aiconapi/', include('aiconapi.urls')),
    path('save_image/', include('save_image.urls')),

    path('admin/', admin.site.urls),
]+static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

