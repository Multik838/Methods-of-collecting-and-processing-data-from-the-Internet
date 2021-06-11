from pprint import pprint
from lxml import html
import requests



def __init__(self):
    global item
    client = MongoClient('localhost', 27017)
    self.mongobase = client.mail


    # Настраиваем соединение
    header = {'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/90.0.4430.212 Safari/537.36'}
    responce = requests.get('https://news.mail.ru/')
    dom = html.fromstring(responce.text)

    # Создадим итератор для обработки всех новостей с сайта
    mail_News = []
    mail_ru_News = dom.xpath("//div[contains(@class, 'layout')]//text()")

    for news in mail_ru_News:
        # Соберём данные в словарь
        NMR = {}
        NMR['source'] = news.xpath("//span[@class= 'newsitem__param']//text()|//div/span[@class = 'newsitem__param js-ago']/text()")
        NMR['name_link'] = news.xpath("//li[@class= 'list__item']//@href|//span[@class= 'link__text']//text() | //div/span[@class = 'newsitem__param js-ago']/text()")
        NMR['day_news_link'] = news.xpath("//a[@class= 'newsitem__title link-holder']//@href|//a[@class= 'newsitem__title link-holder']//text()|//div/span[@class = 'newsitem__param js-ago']/text()")
        all_NMR.append(NMR)
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

    collection.insert_one(item)
    return item