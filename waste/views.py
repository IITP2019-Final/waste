from django.http import HttpResponse
from django.shortcuts import render
from .models import City
import json


def post(request):
    if request.method == "POST":
        # get_value = request.body

        print(request.body)

        q = City.objects.all()
        data = {'result': '서버입니다.' + q.sido[10]}
        return HttpResponse(json.dumps(data), content_type="application/json")


def index(request):
    return render(request, 'waste/index.html')
