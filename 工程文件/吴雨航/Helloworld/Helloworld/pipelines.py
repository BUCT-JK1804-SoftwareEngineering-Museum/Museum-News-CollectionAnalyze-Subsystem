
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from scrapy.exporters import JsonLinesItemExporter
import os


class HelloworldPipeline:
    def __init__(self):
        path = 'result\\'
        self.files = os.listdir(path)
        self.fp = []
        self.exporter = []
        for str in self.files:
            f = open(path+str, 'wb')
            self.fp.append(f)
            self.exporter.append(JsonLinesItemExporter(f, ensure_ascii=False, encoding='utf-8'))
        #self.exporter = JsonLinesItemExporter(self.fp, ensure_ascii=False, encoding='utf-8')

    def open_spider(self, spider):
        print("爬虫开始了...")

    def process_item(self, item, spider):
        index = self.files.index(item['museum']+'.json')
        self.exporter[index].export_item(item)
        return item

    def close_spider(self, spider):
        for f in self.fp:
            f.close()
        print("爬虫结束了...")

    #def process_item(self, item, spider):
        #print('Success')
        #today = time.strftime('%y%m%d', time.localtime())  # 获取本地时间
        #fileName = today + 'tit.txt'
        #fileNamecon = today + 'con.txt'  # 对标题和内容分别保存
        #with open(fileName, 'a', encoding='utf-8') as f:
        #    f.write(item["title"])
        #with open(fileNamecon, 'a', encoding='utf-8') as f:
        #    f.write(item["content"])
        #print('Success')