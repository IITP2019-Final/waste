from django.http import HttpResponse
from django.shortcuts import render
from .models import City, Business, Waste
import json
import pickle
from waste.intent import predictions, get_final_output
from .forms import ImageUploadFileForm
from waste.image_checker import image_pred
from waste.pos_tagging import proto_st_detector
import pathlib


context_stack = [{'intents': [], 'entities': [], 'input': {}, 'output': {}, 'context': {}}]


def post_chatbot(request):
    if request.method == "POST":

        # # Load pickle
        # with open("data/unique_intent.pickle", "rb") as fr:
        #     unique_intent = pickle.load(fr)

        # type = QueryDic
        user_text = request.POST.get('text[value]')

        # user_input = {'input': {'text': user_text}, 'context': {'dialog_stack': []}}

        user_input = {'input': {'text': user_text}}

        if len(context_stack) > 0:
            context = create_context(user_input, context_stack.pop())

            context_stack.append(context)

            data = context

            print(data['context'])

            if 'state' not in data['context']:
                data = create_final_answer_data(data)

            return HttpResponse(json.dumps(data), content_type="application/json")

        # data = create_final_answer_data(intent['intent'])


def post_image(request):
    if request.method == 'POST':
        form = ImageUploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            file = request.FILES['file']
            print(file.name, file.content_type, file.size)

            handle_uploaded_file(file)

            item = image_pred(file.read())

            data = {'item': item}

            return HttpResponse(json.dumps(data), content_type="application/json")


def create_context(user_input, context):
    with open('data/waste_context.json', 'rb') as jf:
        waste_context = json.load(jf)

    if 'state' in context['context'] and context['context']['state'] == 'in_progress':  # 대화 진행중
        result = context

        detector = proto_st_detector(user_input['input']['text'])

        for entity in detector:
            result['entities'].append(entity)  # entity = {'entity': '', 'value': ''}

        result['input']['text'] = user_input['input']['text']

        event_handler = result['context']['dialog_stack']

        parent_node = {}

        # event_handler의 인텐트 부모 찾기 오류 event_handler가 없을 수 있다......
        for i in waste_context['dialog_nodes']:
            if i['dialog_node'] == event_handler[len(event_handler) - 1]['parent']:
                slot = i
                for k in waste_context['dialog_nodes']:
                    if k['dialog_node'] == slot['parent']:
                        parent_node = k

        # if detector ok: #  개체가 찾아지면
        for d in detector:
            for i in waste_context['dialog_nodes']:
                if len(event_handler) > 0:
                    if i['dialog_node'] == event_handler[len(event_handler) - 1]['parent']:
                        if d['entity'] == i['variable'][1:]:
                            result['context']['dialog_stack'].pop()

        # if detector ok: #  개체가 찾아지면
        # if len(detector) > 0:
        #     result['context']['dialog_stack'].pop()
        # else detector not: #  개체를 못찾으면 Fallback 수행
        # if len(result['context']['dialog_stack']) > 0:  # 조건을 고쳐야함...

        # detector로 발견한 개체를 문맥에 저장
        for i in result['entities']:
            result['context'][i['entity']] = i['value']

        if len(event_handler) > 0:  # 대화가 남음
            result['output']['text'] = event_handler[len(event_handler) - 1]['output']['text']
            result['context']['dialog_stack'] = event_handler
            result['context']['state'] = 'in_progress'
        else:  # 대화 끝, 조건 더 추가 필요! state, 문맥 데이터를 꺼내오는 것도 필요
            for i in waste_context['dialog_nodes']:
                if 'parent' in i and i['parent'] == parent_node['dialog_node'] and i['type'] == 'response_condition':
                    print('result_node:', i)
                    result['output']['text'] = i['output']['text']['values'][0]
                    del result['context']['dialog_stack']
                    del result['context']['state']

        print("event_handler~", event_handler)

        print("result~", result)

    else:  # 초기 대화(Welcome)
        result = {'intents': [], 'entities': [], 'input': {}, 'output': {}, 'context': {}}

        # Load pickle
        with open("data/unique_intent.pickle", "rb") as fr:
            unique_intent = pickle.load(fr)

        intent = get_final_output(predictions(user_input['input']['text']), unique_intent)

        intent = intent  # {'intent': '', 'confidence': 0}

        if intent['intent'] == '비용':
            intent['intent'] = 'price'
        elif intent['intent'] == '업체':
            intent['intent'] = 'business'
        elif intent['intent'] == '방법':
            intent['intent'] = 'how'

        result['intents'].append(intent)

        detector = proto_st_detector(user_input['input']['text'])

        for entity in detector:
            result['entities'].append(entity)  # entity = {'entity': '', 'value': ''}

        result['input']['text'] = user_input['input']['text']

        parent_node = {}

        # ?? 인텐트 dialog 찾기
        for i in waste_context['dialog_nodes']:
            if 'conditions' in i and i['conditions'] == '#' + intent['intent']:
                parent_node = i

        slot = []

        # ?? 인텐트 dialog 자식 찾기
        for i in waste_context['dialog_nodes']:
            if 'parent' in i and i['parent'] == parent_node['dialog_node'] and i['type'] == 'slot':
                slot.append(i)

        # detector로 발견한 개체를 문맥에 저장
        for i in result['entities']:
            result['context'][i['entity']] = i['value']

        event_handler = []

        # 필요한 개체 슬롯과 현재 문맥에 저장된 개체를 비교해 남은 이벤트 저장
        for i in slot:
            if i['variable'][1:] not in result['context']:
                for k in waste_context['dialog_nodes']:
                    if 'parent' in k and k['parent'] == i['dialog_node'] and k['type'] == 'event_handler' and k['dialog_node'][-5:] == '_text':
                        event_handler.append(k)

        result['output']['text'] = []
        result['context']['dialog_stack'] = []
        result['context']['state'] = ''

        if len(event_handler) > 0:  # 대화가 남음
            result['output']['text'] = event_handler[len(event_handler) - 1]['output']['text']
            result['context']['dialog_stack'] = event_handler
            result['context']['state'] = 'in_progress'
        else:  # 대화 끝, 조건 더 추가 필요! state, 문맥 데이터를 꺼내오는 것도 필요
            for i in waste_context['dialog_nodes']:
                if 'parent' in i and i['parent'] == parent_node['dialog_node'] and i['type'] == 'response_condition':
                    print('result_node:', i)
                    result['output']['text'] = i['output']['text']['values'][0]
                    del result['context']['dialog_stack']
                    del result['context']['state']

        print("event_handler~", event_handler)

        print("result~", result)

    return result


def get_image_output(request):
    if request.method == "GET":
        item = request.GET.get('item')
        location = request.GET.get('location')

        print(item, location)

        data = {'business': {}, 'price': {}}

        location_id = City.objects.get(sigungu=location).cityid
        print(location_id)

        # 업체
        NAME = '업체명'
        TYPE = '처리분야'
        DONG = '세부지역'
        PHONE = '전화번호'
        HEADER = [NAME, TYPE, DONG, PHONE]

        data['business']['contents'] = {'header': HEADER, 'content': []}
        # ORM 업체:
        for business in Business.objects.filter(city_cityid=location_id):
            row = [business.name, business.type, business.dong, business.phone]
            data['business']['contents']['content'].append(row)

        # 비용
        CATEGORY = '카테고리'
        ITEM = '물품'
        SIZE = '규격'
        PRICE = '비용'
        HEADER = [CATEGORY, ITEM, SIZE, PRICE]

        data['price']['contents'] = {'header': HEADER, 'content': []}
        # ORM 폐기물:카테고리, 물품, 규격, 가격
        for w in Waste.objects.filter(item__contains=item, city_cityid=location_id):
            row = [w.category, w.item, w.size, w.price]
            data['price']['contents']['content'].append(row)

        return HttpResponse(json.dumps(data), content_type="application/json")


# def create_final_answer_data(intent):
#     result = {}
#
#     PRICE = '비용'
#     BUSINESS = '업체'
#     HOW = '방법'
#
#     if intent == PRICE:
#         CATEGORY = '카테고리'
#         ITEM = '물품'
#         SIZE = '규격'
#         HEADER = [CATEGORY, ITEM, SIZE, PRICE]
#
#         result['intent'] = PRICE
#         result['contents'] = {'header': HEADER, 'content': []}
#         # ORM 폐기물:카테고리, 물품, 규격, 가격
#         for w in Waste.objects.filter(item__contains='침대', city_cityid=1):
#             row = [w.category, w.item, w.size, w.price]
#             result['contents']['content'].append(row)
#     elif intent == BUSINESS:
#         NAME = '업체명'
#         TYPE = '처리분야'
#         DONG = '세부지역'
#         PHONE = '전화번호'
#         HEADER = [NAME, TYPE, DONG, PHONE]
#
#         result['intent'] = BUSINESS
#         result['contents'] = {'header': HEADER, 'content': []}
#         # ORM 업체:
#         for business in Business.objects.filter(city_cityid=(10, 26), type__icontains='재활용'):
#             row = [business.name, business.type, business.dong, business.phone]
#             result['contents']['content'].append(row)
#     elif intent == HOW:
#         result['intent'] = HOW
#
#     print(result)
#
#     return result

def create_final_answer_data(data):
    result = {}

    PRICE = 'price'
    BUSINESS = 'business'
    HOW = 'how'

    if data['intents'][0]['intent'] == PRICE:
        CATEGORY = '카테고리'
        ITEM = '물품'
        SIZE = '규격'
        HEADER = [CATEGORY, ITEM, SIZE, PRICE]

        result['intent'] = PRICE
        result['contents'] = {'header': HEADER, 'content': []}

        item = data['context']['item']
        location_id = City.objects.get(sigungu=data['context']['location']).cityid

        # ORM 폐기물:카테고리, 물품, 규격, 가격
        for w in Waste.objects.filter(item__contains=item, city_cityid=location_id):
            row = [w.category, w.item, w.size, w.price]
            result['contents']['content'].append(row)

        result['title'] = '서울시 ' + data['context']['location'] + ' ' + item + ' 처리 비용이에요.'
    elif data['intents'][0]['intent'] == BUSINESS:
        NAME = '업체명'
        TYPE = '처리분야'
        DONG = '세부지역'
        PHONE = '전화번호'
        HEADER = [NAME, TYPE, DONG, PHONE]

        result['intent'] = BUSINESS
        result['contents'] = {'header': HEADER, 'content': []}

        location_id = City.objects.get(sigungu=data['context']['location']).cityid
        # ORM 업체:
        for business in Business.objects.filter(city_cityid=location_id):
            row = [business.name, business.type, business.dong, business.phone]
            result['contents']['content'].append(row)

        result['title'] = '서울시 ' + data['context']['location'] + ' 처리 업체에요!'
    elif data['intents'][0]['intent'] == HOW:
        result['intent'] = HOW
        result['title'] = '폐기물 처리 방법이에요!'

    print(result)

    return result


def handle_uploaded_file(file):
    UPLOAD_FILE_PATH = 'data/temp'
    pathlib.Path(UPLOAD_FILE_PATH).mkdir(exist_ok=True)

    with open(UPLOAD_FILE_PATH + '/uploaded_image.jpg', 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def index(request):
    return render(request, 'waste/index.html')
