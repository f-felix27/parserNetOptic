from bs4 import BeautifulSoup
import re 

def get_frame_types():
    # Чтение файла
    with open('index.xml', 'r', encoding='utf-8') as f:
        content = f.read()
        
    soup = BeautifulSoup(content, 'xml') #парсим, создаем объект супа, туда прочитанную страницу, указывает парсер

    offers = soup.find_all('offer') #находим все офферы
    frames = [] #массив для офферов с очками и оправами
    check = []
    
    #находим офферы с оправами
    for offer in offers:
        name = offer.find('name', string = re.compile("([Оо]права|[Оо]чки)"))
    
        if name: #если в оффере есть тэг name со словами "Оправа", "Очки"
            frames.append(offer) #добавляем этот оффер в frame
            
    for frame in frames:
        
        frame_type = frame.find('param', {'name': re.compile('[Сс]троение оправы')}) #строение оправы
        
        if frame_type is not None and frame_type.string.strip() in check:    
            pass
        else: 
            
            if frame_type is not None:
                check.append(frame_type.string.strip())
                print(frame_type.string)
        
    return 
        
get_frame_types()
