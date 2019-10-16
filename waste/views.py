from django.http import HttpResponse
from django.shortcuts import render
from .models import City
import json


def post(request):
    if request.method == "POST":
        # get_value = request.body

        print(request.body)

        data = []

        for c in City.objects.all():
            print(c.sigungu)
            data.append(c.sigungu)

        data = {'sigungu': data}

        return HttpResponse(json.dumps(data), content_type="application/json")


def index(request):
    return render(request, 'waste/index.html')
