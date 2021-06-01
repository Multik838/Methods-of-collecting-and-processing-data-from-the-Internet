# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from typing import Any
import re
import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from scrapy import Field

#
# class LmparserItem(scrapy.Item):
#     # define the fields for your item here like:
#     name = scrapy.Field()
#     link = scrapy.Field()
#     price = scrapy.Field()

def get_id(values):
    pattern = re.compile('(\d+)\/')
    values = int(re.findall(pattern, values)[0])
    return values

def change_url(value):
    try:
        result = value.replace(' ', '')
        return result
    except Exception:
        return value


def change_photo(value):
    try:
        result = value.replace('_82', '_2000')
        return result
    except Exception:
        return value


def change_price(value):
    try:
        result = value.replace(' ', '')
        return result
    except Exception:
        return value

def change_currency(value):
    try:
        result = value.replace('₽', 'Руб')
        return result
    except Exception:
        return value

def change_description(value):
    try:
        result = value.replace("\u202f", "")
        return result
    except Exception:
        return value



class LmparserItem(scrapy.Item):
    name = scrapy.Field(input_processor=MapCompose(), output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(change_photo))
    link = scrapy.Field()
    price = scrapy.Field(input_processor=MapCompose(change_price))
    currency = scrapy.Field(input_processor=MapCompose(change_currency))
    description = scrapy.Field(input_processor=MapCompose(change_description), output_processor=TakeFirst())
    _id = scrapy.Field(input_processor=MapCompose(get_id))

# https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_2000,h_2000,c_pad,b_white,d_photoiscoming.png/LMCode/81866599.jpg БОЛЬШАЯ КАРТИНКА
# https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_82,h_82,c_pad,b_white,d_photoiscoming.png/LMCode/81866599.jpg МАЛЕНЬКАЯ КАРТИНКА
