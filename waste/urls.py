from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^chatbot', views.post_chatbot, name='chatbot'),
    re_path(r'^image', views.post_image, name='image'),
    re_path(r'^output', views.get_image_output, name='image_output'),
    path('', views.index, name='index')
]
