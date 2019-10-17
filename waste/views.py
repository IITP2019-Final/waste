from django.http import HttpResponse
from django.shortcuts import render
from .models import City
import json
import pickle
from waste.intent import predictions, get_final_output


def post(request):
    if request.method == "POST":
        # get_value = request.body

        # Load pickle
        with open("data/unique_intent.pickle", "rb") as fr:
            unique_intent = pickle.load(fr)

        text = "방법"
        pred = predictions(text)
        get_final_output(pred, unique_intent)

        print(request.body)

        data = []

        for c in City.objects.all():
            print(c.sigungu)
            data.append(c.sigungu)

        data = {'sigungu': data}

        return HttpResponse(json.dumps(data), content_type="application/json")


def index(request):
    return render(request, 'waste/index.html')
