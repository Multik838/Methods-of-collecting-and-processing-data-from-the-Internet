from pprint import pprint
from typing import List, Any, Dict
from lxml import html
import requests


# Настраиваем соединение
header = {'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/90.0.4430.212 Safari/537.36'}
responce = requests.get('https://news.mail.ru/')
dom = html.fromstring(responce.text)

# Создадим итератор для обработки всех новостей с сайта
mail_News = []
mail_ru_News = dom.xpath("//div[contains(@class, 'layout')]")
for news in mail_ru_News:
    # Соберём данные в словарь
    NMR = {'center': news.xpath("//a[@class= 'list__text']//text()"),
           'News_MMO': news.xpath("//span[@class= 'newsitem__title-inner']//text()"),
           'society': news.xpath("//span[@class = 'link__text']//text()")}
    # В нашем словаре обнаружены пропуски \\xa0" и также мы скачали (, 'Отменить')
    # Переведём словарь в строку
    strings = []
    for key, item in NMR.items():
        strings.append("{}: {}".format(key.capitalize(), item))
    result = "; ".join(strings)
    new_result = result.replace(u"\\xa0", u" ").replace(u", 'Отменить'", u"")
    mail_News.append(new_result)
# Обработав данные мы видим дубли новостей, уберём лишнее
all_mail_News = []
for x in mail_News:
    if x not in all_mail_News:
        all_mail_News.append(x)

# Выведем все новости сайта https://news.mail.ru/
print(all_mail_News)