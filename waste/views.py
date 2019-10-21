from django.http import HttpResponse
from django.shortcuts import render
from .models import City, Business, Waste
import json
import pickle
from waste.intent import predictions, get_final_output
from .forms import ImageUploadFileForm
from waste.image_checker import image_pred


def post(request):
    if request.method == "POST":

        # data = []
        #
        # for c in Waste.objects.filter(item__contains='침대', city_cityid=1):
        #     print(c.item)
        #     data.append(c.item)
        #
        # data = {'item': data}

        # QueryDic
        data = request.POST
        print('post text:', data)
        print(data.get('text[value]'))

        # Load pickle
        with open("data/unique_intent.pickle", "rb") as fr:
            unique_intent = pickle.load(fr)

        prediction = predictions(data.get('text[value]'))
        data = get_final_output(prediction, unique_intent)

        if data['result'] == '비용':
            data['result'] = 0
        elif data['result'] == '업체':
            data['result'] = 1
        elif data['result'] == '방법':
            data['result'] = 2

        print(data)

        return HttpResponse(json.dumps(data), content_type="application/json")


def upload_images(request):
    if request.method == 'POST':
        form = ImageUploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            file = request.FILES['file']
            print(file.name, file.content_type, file.size)

            prediction = image_pred(file.read())

            data = {'file_name': file.name, 'file_content_type': file.content_type, 'file_size': file.size, 'result': prediction}

            return HttpResponse(json.dumps(data), content_type="application/json")
        else :
            data = {'file': 'is_not_valid'}

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
