from django.http import HttpResponse
from django.shortcuts import render
from .models import City, Business, Waste
import json
import pickle
from waste.intent import predictions, get_final_output
from .forms import ImageUploadFileForm
from waste.image_checker import image_pred
import pathlib


def post_chatbot(request):
    if request.method == "POST":

        # Load pickle
        with open("data/unique_intent.pickle", "rb") as fr:
            unique_intent = pickle.load(fr)

        # type = QueryDic
        user_text = request.POST.get('text[value]')
        intent = get_final_output(predictions(user_text), unique_intent)
        data = create_final_answer_data(intent['intent'])

        return HttpResponse(json.dumps(data), content_type="application/json")


def upload_images(request):
    if request.method == 'POST':
        form = ImageUploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            file = request.FILES['file']
            print(file.name, file.content_type, file.size)

            handle_uploaded_file(file)

            prediction = image_pred(file.read())

            data = {'file_name': file.name, 'file_content_type': file.content_type, 'file_size': file.size, 'result': prediction}

            return HttpResponse(json.dumps(data), content_type="application/json")
        else :
            data = {'file': 'is_not_valid'}

            return HttpResponse(json.dumps(data), content_type="application/json")


def create_final_answer_data(intent):
    result = {}

    PRICE = '비용'
    BUSINESS = '업체'
    HOW = '방법'

    if intent == PRICE:
        CATEGORY = '카테고리'
        ITEM = '물품'
        SIZE = '규격'
        HEADER = [CATEGORY, ITEM, SIZE, PRICE]

        result['intent'] = PRICE
        result['contents'] = {'header': HEADER, 'content': []}
        # ORM 폐기물:카테고리, 물품, 규격, 가격
        for w in Waste.objects.filter(item__contains='침대', city_cityid=1):
            row = [w.category, w.item, w.size, w.price]
            result['contents']['content'].append(row)
    elif intent == BUSINESS:
        NAME = '업체명'
        TYPE = '처리분야'
        DONG = '세부지역'
        PHONE = '전화번호'
        HEADER = [NAME, TYPE, DONG, PHONE]

        result['intent'] = BUSINESS
        result['contents'] = {'header': HEADER, 'content': []}
        # ORM 업체:
        for business in Business.objects.filter(city_cityid=(10, 26), type__icontains='재활용'):
            row = [business.name, business.type, business.dong, business.phone]
            result['contents']['content'].append(row)
    elif intent == HOW:
        result['intent'] = HOW

    print(result)

    return result


def handle_uploaded_file(f):
    pathlib.Path('data/temp').mkdir(exist_ok=True)

    with open('data/temp/uploaded_image.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def index(request):
    return render(request, 'waste/index.html')
