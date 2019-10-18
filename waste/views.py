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

        for city in City.objects.all():
            print(city.sigungu)
            data.append(city.sigungu)

        data = {'sigungu': data}

        return HttpResponse(json.dumps(data), content_type="application/json")

def get(self, request):
    form = HomeForm()
    posts= Post.objects.all()

    args= {'form':form,}
    return render(request, self.template_name, args)

def post(self, request):
    form = HomeForm(request.POST)
    if form.is_valid():


        print(request.body)

        data = []

        for waste in Waste.objects.filter(item__contains='침대', city_cityid=1):
            temp=(waste.category, waste.item, waste.size,waste.price)
            data.append(temp)

        data = {'data': data}


        return HttpResponse(json.dumps(data), content_type="application/json")


def business(request):
    if request.method == "POST":
        # get_value = request.body

        print(request.body)

        data = []

        for business in Business.objects.filter(city_cityid=(10, 26), type__icontains='재활용'):
            temp=business.name, business.dong, business.type, business.phone
            data.append(temp)


        data = {'data': data}
        print(data)

        return HttpResponse(json.dumps(data), content_type="application/json")


def index(request):
    return render(request, 'waste/index.html')
