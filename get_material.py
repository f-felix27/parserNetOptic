
from bs4 import BeautifulSoup
import re 

def material():
    # Чтение файла
    with open('index.xml', 'r', encoding='utf-8') as f:
        content = f.read()
        
    soup = BeautifulSoup(content, 'xml') #парсим, создаем объект супа, туда прочитанную страницу, указывает парсер

    offers = soup.find_all('offer') #находим все офферы
    materials = [] #массив для офферов с очками и оправами
    check = []
    
    #находим офферы с оправами
    for offer in offers:
        name = offer.find('name', string = re.compile("([Оо]права|[Оо]чки)"))
    
        if name: #если в оффере есть тэг name со словами "Оправа", "Очки"
            materials.append(offer) #добавляем этот оффер в frame
            
    for material in materials:
        
        material_type = material.find('param', {'name': re.compile('[Мм]атериал')}) #строение оправы
        
        if material_type is not None and material_type.string.strip() in check:    
            pass
        else: 
            
            if material_type is not None:
                check.append(material_type.string.strip())
                print(material_type.string)
        
    return 
        
material()