import json

import scrapy
import re
import requests
import urllib3
import time

from Helloworld.items import HelloworldItem
import urllib.request
import urllib.parse
import urllib.request

class HelloSpider(scrapy.Spider):
    name = 'hello'
    allowed_domains = ['www.baidu.com']
    base_url = 'https://www.baidu.com'
    access_token = ''

    def GetAccess(self):
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=ZGdgBze0j5NhLkmtYXRHUeFf&client_secret=5tkNIusKDfKFXFxpYg5T3qHGCi3RuvbM'
        request = urllib.request.Request(host)
        request.add_header('Content-Type', 'application/json; charset=UTF-8')
        response = urllib.request.urlopen(request)
        content = response.read()
        content = json.loads(content)
        if (content):
            self.access_token = content['access_token']

    def analyze(self,analyzetext):
        http = urllib3.PoolManager()
        url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?access_token=' + self.access_token
        time.sleep(0.3)
        params = {'text': analyzetext}
        # 进行json转换的时候，encode编码格式不指定也不会出错
        encoded_data = json.dumps(params).encode('GBK')
        request = http.request('POST',
                               url,
                               body=encoded_data,
                               headers={'Content-Type': 'application/json'})
        # 对返回的byte字节进行处理。Python3输出位串，而不是可读的字符串，需要进行转换
        # 注意编码格式
        result = str(request.data, 'GBK')
        res = json.loads(result)
        if('items' in res):
            senti = res['items'][0]
            if(senti['positive_prob']<0.4):
                return "负面"
            else:
                if(senti['positive_prob']>0.8):
                    return "正面"
        else:
            print("访问时间过短")
        return "中立"

    def start_requests(self):
        self.GetAccess()
        prim = 'https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&ie=utf-8&word='
        urls = []
        museum = ['开封市博物馆','鄂豫皖苏区首府革命博物馆','湖北省博物馆','荆州博物馆','武汉博物馆','辛亥革命武昌起义纪念馆','武汉市中山舰博物馆','湖南省博物馆','韶山毛泽东故居纪念馆','刘少奇故居纪念馆','长沙简牍博物馆','广东省博物馆','西汉南越王博物馆','孙中山故居纪念馆','深圳博物馆','广州博物馆','广东民间工艺博物馆','广西壮族自治区博物馆','广西民族博物馆','海南省博物馆','自贡恐龙博物馆','三星堆博物馆','成都武侯祠博物馆','成都杜甫草堂博物馆','四川博物院','成都金沙遗址博物馆']
        for mname in museum:
            urls.append(prim+mname)
        i = 0
        for url in urls:
            yield scrapy.Request(url=url, meta={'museumName': museum[i]}, callback=self.parse)
            i+=1

    def parse(self, response):
        print([response.meta['museumName'],response])
        main_list = response.xpath('//div[@class="result-op c-container xpath-log new-pmd"]')
        for box in main_list:
            item = HelloworldItem()
            item['museum'] = response.meta['museumName']
            #title_list = response.xpath(main1+'['+str(i+1)+']'+'//h3[@class="news-title_1YtI1"]/a').extract()
            title_list = box.xpath('.//h3[@class="news-title_1YtI1"]/a').extract()
            title = ''
            if len(title_list)>0:
                title = title_list[0]
                searchObj = re.search(r'<!--s-text-->.*<!--/s-text-->', title, re.M | re.I)
                if searchObj:
                    title = re.sub(r'<!--s-text-->|<!--/s-text-->|<em>|</em>', "", searchObj.group())
            item['title'] = title

            #content_list = response.xpath(main1+'['+str(i+1)+']'+'//span[@class="c-font-normal c-color-text"]').extract()
            content_list = box.xpath('.//span[@class="c-font-normal c-color-text"]').extract()
            content = ''
            if len(content_list)>0:
                content = content_list[0]
                searchObj = re.search(r'<!--s-text-->.*<!--/s-text-->', content, re.M | re.I)
                if searchObj:
                    content = re.sub(r'<!--s-text-->|<!--/s-text-->|<em>|</em>', "", searchObj.group())
            item['content'] = content

            #image_list = response.xpath(main1+'['+str(i+1)+']'+'//div[@class="c-img c-img3 c-img-radius-large"]/img').extract()
            image_list = box.xpath('.//div[@class="c-img c-img3 c-img-radius-large"]/img').extract()
            image = ''
            if len(image_list)>0:
                image = image_list[0]
                searchObj = re.search(r'src=".*" ', image, re.M | re.I)
                if searchObj:
                    image = re.sub(r'src="|" ', "", searchObj.group())
                    #把&amp;改为&
                    image = re.sub(r'&amp;', '&', image)
                    image = re.sub(r'&quot;', '"', image)
                    image = re.sub(r'&lt;', '<', image)
                    image = re.sub(r'&gt;', '>', image)
            item['image'] = image

            item['poster'] = box.xpath('.//div[@class="news-source"]/span[@class="c-color-gray c-font-normal c-gap-right"]/text()').extract()[0]
            times = box.xpath('.//div[@class="news-source"]/span[@class="c-color-gray2 c-font-normal"]/text()').extract()
            if len(times)>0:
                item['time'] = times[0]
            else:
                item['time'] = ''
            item['source'] = box.xpath('@mu').extract()[0]

            item['sentiment'] = self.analyze(item['title'])
            #item['sentiment'] = self.analyze(item['title']+" "+item['content'])

            yield item

        urllist = response.xpath('//div[@class="page-inner"]/a[@class="n"]').extract()
        for u in urllist:
            newurl = re.search(r'href=".*" class="n">下一页', u, re.M | re.I)
            if newurl:
                url = re.sub(r'href="|" class="n">下一页', "", newurl.group())
                url = re.sub(r'&amp;', '&', url)
                url = re.sub(r'&quot;', '"', url)
                url = re.sub(r'&lt;', '<', url)
                url = re.sub(r'&gt;', '>', url)
                yield scrapy.Request(self.base_url+url, callback=self.parse, meta={'museumName': response.meta['museumName']}, dont_filter=False)