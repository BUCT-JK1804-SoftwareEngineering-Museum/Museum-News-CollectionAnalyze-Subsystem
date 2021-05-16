# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HelloworldItem(scrapy.Item):
    # define the fields for your item here like:
    # 博物馆
    mus_id=scrapy.Field()
    id=scrapy.Field()
    museum=scrapy.Field()
    # 源地址
    source = scrapy.Field()
    #课程标题
    title = scrapy.Field()
    #图片地址
    image=scrapy.Field()
    #作者
    poster=scrapy.Field()
    #时间
    time=scrapy.Field()
    #内容
    content=scrapy.Field()