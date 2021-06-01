# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class LmparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.leroymerlinru


    def process_item(self, item, spider):

        item['_id'] = item['_id'][0]
        item['link'] = item['link'][0]
        item['price'] = item['price'][0]
        item['currency'] = item['currency'][0]
        del item['price']
        collection = self.mongobase[spider.name]
        collection.insert_one(item)


        return item


class LmparsePhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for image in item['photos']:
                try:
                    yield scrapy.Request(image.replace('_82', '_2000'))
                except TypeError as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if [itm[0]]]
        return item
