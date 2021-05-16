# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class HelloworldItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    museum = scrapy.Field()
    content = scrapy.Field()  # 获取内容
    title = scrapy.Field()
    image = scrapy.Field()
    poster = scrapy.Field()
    time = scrapy.Field()
    source = scrapy.Field()
    sentiment = scrapy.Field()