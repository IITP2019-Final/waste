from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^chatbot', views.post_chatbot, name='chatbot'),
    re_path(r'^image', views.post_image, name='image'),
    path('', views.index, name='index')
]
