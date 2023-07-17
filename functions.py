import os
import requests
from bs4 import BeautifulSoup
import re #регулярные выражения

def name_from_url(url):

    # Получаем имя файла из URL-адреса
    filename = os.path.basename(url)

    #Выбираем расширение
    extension = filename.split('.')[-1]

    # Удаляем расширение файла
    name_without_extension = os.path.splitext(filename)[0]

    # Разделяем имя на отдельные слова
    words = name_without_extension.split('-')

    # Удаляем 600x600
    words.pop()

    # Объединяем слова в строку с пробелами
    name = '-'.join(words)
    result = name + '.' + extension
    return  result
