from django.http import HttpResponse
from django.shortcuts import render
from .models import City, Business, Waste
import json
import pickle
from waste.intent import predictions, get_final_output


def post1(request):
    if request.method == "POST":
        # get_value = request.body

        # Load pickle
        with open("data/unique_intent.pickle", "rb") as fr:
            unique_intent = pickle.load(fr)

        data = request.POST
        print('type: ', type(data))
        print('post text:', data)

        # QueryDic
        print(data.get('text[value]'))

        pred = predictions(data.get('text[value]'))
        get_final_output(pred, unique_intent)

        data = []

        for c in City.objects.all():
            print(c.sigungu)
            data.append(c.sigungu)

        data = {'sigungu': data}

        return HttpResponse(json.dumps(data), content_type="application/json")


def post(request):
    if request.method == "POST":
        # get_value = request.body

        print(request.body)

        data = []

        for c in Waste.objects.filter(item__contains='침대', city_cityid=1):
            print(c.item)
            data.append(c.item)

        data = {'item': data}

        return HttpResponse(json.dumps(data), content_type="application/json")


def business(request):
    if request.method == "POST":
        # get_value = request.body

        print(request.body)

        data = []

        for c in Business.objects.filter(city_cityid=(10, 26), type__icontains='재활용'):
            print(c.name)
            data.append(c.name)

        data = {'name': data}

        return HttpResponse(json.dumps(data), content_type="application/json")


def index(request):
    return render(request, 'waste/index.html')
