from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^chatbots', views.post, name='chatbots'),
    path('home', views.index, name='index'),
    path('result', views.imageResult, name='result')
]