from konlpy.tag import Kkma
kkma=Kkma() 




def read_file(msg):
    result=[]
    if msg == 'item':
        fileName='DB_ITEM.txt'
    if msg == 'place':
        fileName='DB_LOC.txt'
        
    fread_target = open(fileName, 'r', encoding="utf-8")

    while True:
        line=fread_target.readline()
        if not line: break #다읽으면 종료
        result.append(line.replace('\n',''))

    fread_target.close()
    
    return result




def proto_st_detector(question):# 코드 정리점 
    Q_token={}
    item_token={}
    loc_token={}
    
    tokenlist = kkma.pos(question) # 단어 토큰화
    
    item_token=read_file('item')
    loc_token=read_file('place')
    
    for item_word in tokenlist:        
        if item_word[1] in ["NNG"]:
            for item_tk in item_token :
                if item_tk in item_word[0]: #DB에서 품목있는 애만 저장
                    Q_token['item']=item_word[0]
                    break;
            
    
    for place_word in tokenlist:     
        if place_word[1] in ["NNP"]:
            for loc_tk in loc_token:
                if loc_tk in place_word[0]:
                    Q_token['location']= place_word[0]
                    break;
            
                
    return Q_token



print(proto_st_detector("서울시 관악구에서 장롱 버릴래"))


