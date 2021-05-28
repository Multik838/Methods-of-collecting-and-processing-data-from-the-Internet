import scrapy
# Для более удобного использования переменных указываем класс через :
# Например x:dict
# scrapy genspider superjobru superjob.ru
from scrapy.http import HtmlResponse
from jobparser.items import SuperjobruItem

class SuperjobruSpider(scrapy.Spider):
    name = 'superjobru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://korolev.superjob.ru/vakansii/analitik.html']

    def parse(self, response: HtmlResponse, **kwargs):
        next_page = response.xpath("//span[text() = 'Дальше']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        vacancy_links = response.xpath("//div[@class='_1h3Zg _2rfUm _2hCDz _21a7u']/a/@href")
        for link in vacancy_links:
            yield response.follow(link, callback=self.vacancy_parse)

# Yield это ключевое слово, которое используется примерно как return — отличие в том, что функция вернёт генератор.



    def vacancy_parse(self, response: HtmlResponse):
        item_name = response.xpath("//h1/text()").extract_first()
        item_salary = response.xpath('//span[@class="_1OuF_ ZON4b"]//text()').extract()
        # item_link = response.xpath("//div[@class='_1h3Zg _2rfUm _2hCDz _21a7u']/a/@href").extract()
        item_link = response.url


        item = SuperjobruItem(name=item_name, salary=item_salary, link=item_link)
        yield item