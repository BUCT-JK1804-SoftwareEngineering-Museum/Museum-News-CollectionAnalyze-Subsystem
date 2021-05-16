# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from gevent.libev.corecext import os
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import json
import pymysql
from scrapy.exporters import JsonLinesItemExporter

class HelloworldPipeline(object):
    def __init__(self):
        #打开文件
        path='result\\'
        self.files=os.listdir(path)
        self.fp=[]
        self.exporter=[]
        for str in self.files:
            f=open(path+str,'wb')
            self.fp.append(f)
            self.exporter.append(JsonLinesItemExporter(f,ensure_ascii=False,encoding='utf-*'))
    #该方法用于处理数据
    def process_item(self, item, spider):
        museumName=item['museum']
        index=self.files.index(museumName+'.json')
        self.exporter[index].export_item(item)
        return item
    #该方法在spider被开启时被调用。
    def open_spider(self, spider):
        print("start_program")
    #该方法在spider被关闭时被调用。
    def close_spider(self, spider):
        for f in self.fp:
            f.close()
        print("end_program")


# 将数据存储到mysql数据库

from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
''''''
class MySQLStorePipeline(object):
    # 数据库参数
    def __init__(self):
        dbargs = dict(
            host='127.0.0.1',
            db='test',
            user='root',
            passwd='jclgogogo.',
            cursorclass=MySQLdb.cursors.DictCursor,
            charset='utf8',
            use_unicode=True
        )
        self.dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)

    '''
    The default pipeline invoke function
    '''

    def process_item(self, item, spider):
        res = self.dbpool.runInteraction(self.insert_into_table, item)
        return item

    # 插入的表，此表需要事先建好
    def insert_into_table(self, conn, item):
        conn.execute('insert into test_m(new_id,mus_id,museum,source,title,image,poster,time,content) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)', (
            item['id'],
            item['mus_id'],
            item['museum'],
            item['source'],
            item['title'],
            item['image'],
            item['poster'],
            item['time'],
            item['content'])
                     )
