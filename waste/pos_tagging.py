from konlpy.tag import Kkma
kkma=Kkma()


def read_file(msg):
    result=[]
    if msg == 'item':
        fileName='data/DB_ITEM.txt'
    if msg == 'place':
        fileName='data/DB_PLACE.txt'
        
    fread_target = open(fileName, 'r', encoding="utf-8")

    while True:
        line=fread_target.readline()
        if not line: break #다읽으면 종료
        result.append(line.replace('\n',''))

    fread_target.close()
    
    return result


def proto_st_detector(question):
    Q_token = []
    i_token = {}
    l_token = {}

    tokenlist = kkma.pos(question)
    print(tokenlist)

    item_token = read_file('item')
    loc_token = read_file('place')

    for token in tokenlist:
        if token[0] in item_token:
            i_token['entity'] = 'item'
            i_token['value'] = token[0]

        if token[0] in loc_token:
            l_token['entity'] = 'location'
            l_token['value'] = token[0]

        if len(i_token) > 0:
            Q_token.append(i_token)

        if len(l_token) > 0:
            Q_token.append(l_token)

    return Q_token




# def proto_st_detector(question):# 코드 정리점
#     Q_token={}
#     item_token={}
#     loc_token={}
#
#     tokenlist = kkma.pos(question) # 단어 토큰화
#
#     item_token=read_file('item')
#     loc_token=read_file('place')
#
#     for item_word in tokenlist:
#         if item_word[1] in ["NNG"]:
#             for item_tk in item_token :
#                 if item_tk in item_word[0]: #DB에서 품목있는 애만 저장
#                     Q_token['item']=item_word[0]
#                     break;
#
#
#     for place_word in tokenlist:
#         if place_word[1] in ["NNP"]:
#             for loc_tk in loc_token:
#                 if loc_tk in place_word[0]:
#                     Q_token['location']= place_word[0]
#                     break;
#
#
#     return Q_token


