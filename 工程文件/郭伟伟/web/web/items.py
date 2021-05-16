# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    image = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()
    poster=scrapy.Field()
    source=scrapy.Field()
    museum=scrapy.Field()
    sentiment=scrapy.Field()
    #scrapy 框架数据结构是一个类字典对象