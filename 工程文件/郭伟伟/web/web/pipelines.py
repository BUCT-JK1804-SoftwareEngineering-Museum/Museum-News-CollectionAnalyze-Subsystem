import os
from scrapy.exporters import JsonLinesItemExporter

class WebPipeline:
    def __init__(self):
        path = 'result\\'
        self.files = os.listdir(path)
        self.fp = []
        self.exporter = []
        for str in self.files:
            f = open(path+str, 'wb')
            self.fp.append(f)
            self.exporter.append(JsonLinesItemExporter(f, ensure_ascii=False, encoding='utf-8'))
        '''self.file = open('web.json', 'wb')  # 必须二进制写入
        self.exporter = JsonLinesItemExporter(self.file, ensure_ascii=False, encoding='utf-8')'''

    def open_spider(self, spider):
        print('爬虫开始')

    def process_item(self, item, spider):
        museumName = item['museum']
        index = self.files.index(museumName+'.json')
        self.exporter[index].export_item(item)
        return item

    def close_spider(self, spider):
        for f in self.fp:
            f.close()
        print("爬虫结束")