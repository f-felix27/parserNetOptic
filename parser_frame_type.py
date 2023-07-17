import requests
from bs4 import BeautifulSoup
import re #регулярные выражения
import os
import functions

#Ссылка на сайт
# url = 'https://www.netoptik.ru/yandexmarket.yml'


# req = requests.get(url)
# src = req.text #получаем код страницы

#Сохраняем в файл с обработкой ошибки
# try:
#     with open("index.xml", "w", encoding='utf-8') as file:
#         file.write(src)
# except UnicodeEncodeError:
#     with open("index.xml", "w", encoding='utf-16') as file:
#         file.write(src)


# Чтение файла
with open('index.xml', 'r', encoding='utf-8') as f:
    content = f.read()
    
soup = BeautifulSoup(content, 'xml') #парсим, создаем объект супа, туда прочитанную страницу, указывает парсер

#находим все офферы
offers = soup.find_all('offer')
frames = [] #массив для офферов с очками и оправами

#это счетчики, чтобы проверить все ли спарсено
frame_count = 0 #счетчик оправ
bezel_count = 0 #счетчик фотографий ободковых оправ
nonframe_count = 0 #счетчик фотографий безободковых оправ
line_count = 0 #счетчик фотографий оправ на леске
nonsorted_count = 0 #счетчик фотографий ресортированных видов дужек

#находим офферы с оправами
for offer in offers:
    name = offer.find('name', string = re.compile("([Оо]права|[Оо]чки)"))
    
    if name: #если в оффере есть тэг name
        frames.append(offer) 
        frame_count += 1
print('Всего очков: ', frame_count)
print(len(frames))

# складываем фотографии в папки по виду оправ
for frame in frames:
    
    frame_type = frame.find('param', {'name': re.compile('[Сс]троение оправы')}) #строение оправы
    
    pictures = frame.find_all('picture') #собираем картинки
    
    if frame_type is not None and frame_type.string.strip()  in ['Ободковая']:
        folder = 'img/Ободковые'
        bezel_count += 1
    elif frame_type is not None and frame_type.string.strip() in ['Безободковая']:
        folder = 'img/Безободковые'
        nonframe_count += 1
    # elif material.string == re.compile('[Кк]омбинированны'): #почему-то не работает
    # Как сделать строку короче?
    elif frame_type is not None and frame_type.string.strip() in ['Леска','леска']:
        folder = 'img/Леска'
        line_count += 1
    else:
        folder = 'img/Несортированные (виды дужек)'
        nonsorted_count += 1
    
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
        
print('Ободковые: ', bezel_count)
print('Безободковые: ', nonframe_count)
print('Леска: ', line_count)
print('Несортированных очков: ', nonsorted_count)
    