from django.http import HttpResponse
from django.shortcuts import render
import json


def post(request):
    if request.method == "POST":
        # get_value = request.body

        data = {'result': '서버입니다. 반갑습니다.'}
        return HttpResponse(json.dumps(data), content_type="application/json")


def index(request):
    return render(request, 'waste/index.html')
