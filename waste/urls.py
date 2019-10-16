from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^chatbots', views.post, name='chatbots'),
    path('', views.index, name='index')
]