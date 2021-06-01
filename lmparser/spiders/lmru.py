import scrapy
from scrapy.http import HtmlResponse
from lmparser.items import LmparserItem
from scrapy.loader import ItemLoader


class LmruSpider(scrapy.Spider):
    name = 'lmru'
    allowed_domains = ['leroymerlin.ru']
    # start_urls = ['http://leroymerlin.ru/']

    def __init__(self, search):
        super(LmruSpider, self).__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response: HtmlResponse):
        goods_links = response.xpath("//a[contains(@href, 'product')]")
        for link in goods_links:
            yield response.follow(link, callback=self.parse_good)

        next_page = response.xpath("//a[@data-qa-pagination-item = 'right']/@href").extract_first()
        print('Переход на следующую страницу')
        if next_page == None:
            print("That's all folks")
        yield response.follow(next_page, callback=self.parse)

    def parse_good(self, response: HtmlResponse):
        loader = ItemLoader(item=LmparserItem(), response=response)
        loader.add_value('_id', str(response))
        loader.add_xpath('name', "//h1[contains(text(),'')]/text()")
        loader.add_value('link', response.url)
        loader.add_xpath('price', "//meta[@itemprop='price']/@content")
        loader.add_xpath('currency', "//span[@slot='currency']/text()")
        loader.add_xpath('photos', "//img[contains(@slot, 'thumbs')]/@src")
        loader.add_xpath('description', "//p[contains(text(),'Габариты')]/text()")
        yield loader.load_item()

# //dl[@class = 'def-list']
#