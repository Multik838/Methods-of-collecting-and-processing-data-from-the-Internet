import scrapy
# Для более удобного использования переменных указываем класс через :
# Например x:dict
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
# Здесь указывает ссылки для входа на сайт
# [https: // hh.ru / vacancies / analitik],
#     start_urls = ['http://hh.ru/']
    start_urls = ['https://hh.ru/vacancies/analitik']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        vacancies_links = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href")
        for link in vacancies_links:
            yield response.follow(link, callback=self.vacancy_parse)
# Yield это ключевое слово, которое используется примерно как return — отличие в том, что функция вернёт генератор.



    def vacancy_parse(self, response: HtmlResponse):
        item_name = response.xpath("//h1/text()").extract_first()
        item_salary = response.xpath("//p/span[@data-qa='bloko-header-2']/text()").extract()
        item_link = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").extract_first()
        item = JobparserItem(vacancy_name=item_name, salary=item_salary, vacancy_link=item_link)
        yield item
