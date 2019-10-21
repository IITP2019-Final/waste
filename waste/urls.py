from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^chatbots', views.post, name='chatbots'),
    re_path(r'^images', views.upload_images, name='images'),
    path('', views.index, name='index')
]