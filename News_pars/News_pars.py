from lxml import html
from pprint import pprint
import requests

def __init__(self):
    global item
    client = MongoClient('localhost', 27017)
    self.mongobase = client.yandex

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}

    response = requests.get('https://yandex.ru/news/')
    dom = html.fromstring(response.text)
    yandex_News = []
    all_news = []

    items = dom.xpath("//div[contains(@class, 'rubric')]")

    for item in items:
        news = {'link_sourse_title_time': item.xpath(
            "//a[contains(@class,'mg-card__source-link')]/text() | //a[contains(@class,'mg-card__source-link')]/@href | //h2[contains(@class ,'mg-card__title')]/text() | //span[contains(@class,'mg-card-source__time')]/text()")}
        # news['headers'] = item.xpath(")
        # news['link'] = item.xpath("//a[contains(@class,'mg-card__source-link')]/text()")
        # news['sourse'] = item.xpath("//a[contains(@class,'mg-card__source-link')]/@href")
        # news['title'] = item.xpath("//h2[contains(@class ,'mg-card__title')]/text()")
        # news['time'] = item.xpath("//span[contains(@class,'mg-card-source__time')]/text()")
        all_news.append(news)

        strings = []
        for key, item in news.items():
            strings.append("{}: {}".format(key.capitalize(), item))
        result = "; ".join(strings)
        new_result = result.replace(u"\\xa0", u" ").replace(u", 'Отменить'", u"")
        yandex_News.append(new_result)
    # Обработав данные мы видим дубли новостей, уберём лишнее
    all_yandex_News = []
    for x in yandex_News:
        if x not in all_yandex_News:
            all_yandex_News.append(x)

    # Выведем все новости сайта https://yandex.ru/news/
    print(all_yandex_News, end="______________________________________________________")

    collection.insert_one(item)
    return item