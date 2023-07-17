import requests
from bs4 import BeautifulSoup
import re #регулярные выражения

import os
import functions

#Скачиваем страницу, чтобы не обращаться на сервер
url = 'https://www.netoptik.ru/yandexmarket.yml' #ссылка на сайт


req = requests.get(url)
src = req.text #получаем код страницы

#Сохраняем в файл с обработкой ошибки
try:
    with open("index.xml", "w", encoding='utf-8') as file:
        file.write(src)
except UnicodeEncodeError:
    with open("index.xml", "w", encoding='utf-16') as file:
        file.write(src)


# Чтение файла
with open('index.xml', 'r', encoding='utf-8') as f:
    content = f.read()
    
soup = BeautifulSoup(content, 'xml') #парсим, создаем объект супа, туда прочитанную страницу, указывает парсер

#находим все офферы
offers = soup.find_all('offer')
frames = [] #массив для офферов с очками и оправами
#это счетчики, чтобы проверить все ли спарсено
frame_count = 0 #счетчик оправ
metall_count = 0 #счетчик фотографий металлических оправ
plactic_count = 0 #счетчик фотографий пластиковых оправ
comb_count = 0 #счетчик фотографий комбинированных оправ
nonsorted_material = 0 #счетчик фотографий несортированных оправ

#находим офферы с оправами
for offer in offers:
    name = offer.find('name', string = re.compile("([Оо]права|[Оо]чки)"))
    
    if name: #если в оффере есть тэг name
        frames.append(offer) 
        frame_count += 1
print('Всего очков: ', frame_count)
print(len(frames))

# складываем фотографии в папки по материалам и по виду оправ
for frame in frames:
    material = frame.find('param', {'name': re.compile('[Мм]атериал')}) #материал оправы
    
    pictures = frame.find_all('picture') #собираем картинки
    
    if material is not None and material.string.strip()  in ['Металл', 'металл', 'Титан', 'титан']:
        folder = 'img/Металл'
        metall_count += 1
    elif material is not None and material.string.strip() in ['Silflex', 'Пластик','пластик', 'силикон', 'Силикон', 'Пластик, ударопрочный']:
        folder = 'img/Пластик'
        plactic_count += 1
    # elif material.string == re.compile('[Кк]омбинированны'): #почему-то не работает
    # Как сделать строку короче?
    elif material is not None and material.string.strip() in ['Комбинированный','Комбинированная','комбинированный', 'комбинированная', 'Комбинированные']:
        folder = 'img/Комбинированный'
        comb_count += 1
    else:
        folder = 'img/Несортированные (материалы)'
        nonsorted_material += 1
    
    if not os.path.exists(folder): #если такая папка не существует,
        os.makedirs(folder)         #создать ее
            
    for picture in pictures:
        img_url = picture.string #получаем ссылки на картинки
        
        if img_url:
            filename = functions.name_from_url(img_url) #формируем имя картинок из адреса
            
            filepath = os.path.join(folder, filename) #полное имя картинки (с папкой)
        
            #сохраняем изображение в файл
            response = requests.get(img_url)
            with open(filepath, 'wb') as out_file:
                out_file.write(response.content)
        
print('Металлических очков: ', metall_count)
print('Пластиковых очков: ', plactic_count)
print('Комбинированных очков: ', comb_count)
print('Несортированных очков: ', nonsorted_material)
