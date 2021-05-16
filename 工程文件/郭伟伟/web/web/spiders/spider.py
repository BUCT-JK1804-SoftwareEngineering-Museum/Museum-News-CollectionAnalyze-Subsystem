import json
import time
import urllib
import scrapy
import re
import urllib3

from ..items import WebItem

class webSpider(scrapy.Spider):
    name = 'spider'
    access_token = '';
    allowed_domains = ['baidu.com']  # 限制域名爬取
    #start_urls = ['https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&ie=utf-8&word=%E4%B8%AD%E5%9B%BD%E9%97%BD%E5%8F%B0%E7%BC%98%E5%8D%9A%E7%89%A9%E9%A6%86']# 起始网址
    def GetAccess(self):
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=ZGdgBze0j5NhLkmtYXRHUeFf&client_secret=5tkNIusKDfKFXFxpYg5T3qHGCi3RuvbM'
        request = urllib.request.Request(host)
        request.add_header('Content-Type', 'application/json; charset=UTF-8')
        response = urllib.request.urlopen(request)
        content = response.read()
        content = json.loads(content)
        if (content):
            self.access_token = content['access_token']

    def analyze(self, analyzetext):
        http = urllib3.PoolManager()
        url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?access_token=' + self.access_token
        time.sleep(0.32)
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
        if ('items' in res):
            senti = res['items'][0]
            if (senti['positive_prob'] < 0.5):
                return "负面"
            else:
                if (senti['positive_prob'] > 0.8):
                    return "正面"
        else:
            print("访问时间过短")
        return "中立"
    def start_requests(self):
        self.GetAccess()
        prim = 'https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&ie=utf-8&word='
        urls = []
        museum = ['自贡市盐业历史博物馆','遵义会议纪念馆','云南省博物馆','云南民族博物馆','重庆中国三峡博物馆','重庆红岩革命历史博物馆','重庆自然博物馆','西藏博物馆','陕西历史博物馆','秦始皇兵马俑博物馆','延安革命纪念馆','汉阳陵博物馆','西安碑林博物馆','西安半坡博物馆','西安博物院','宝鸡青铜器博物院','西安大唐西市博物馆','甘肃省博物馆','天水市博物馆','敦煌研究院','固原博物馆','宁夏博物馆','青海省博物馆','新疆维吾尔自治区博物馆','吐鲁番博物馆']
        for mname in museum:
            urls.append(prim+mname)
        i=0
        for url in urls:
            yield scrapy.Request(url=url,meta={'museumName':museum[i]},callback=self.parse)
            i+=1

    def parse(self, response):
        print([response.meta['museumName'],response])
        divs = response.xpath('//div[@class="result-op c-container xpath-log new-pmd"]')
        for div in divs:
            item = WebItem()
            item['museum'] = response.meta['museumName']
            title = div.xpath('.//h3[@class="news-title_1YtI1"]/a').extract()
            title1 = re.search(r'<!--s-text-->.*<!--/s-text-->', title[0], re.M | re.I)
            if title1:
                title = re.sub(r'<!--s-text-->|<!--/s-text-->|<em>|</em>', "", title1.group())
            else:
                title = ''
            item['title'] = title

            image = div.xpath('.//div[@class="c-span3 img-margin-bottom_BzjMI"]//img').extract()
            if len(image)>0:
                title1_photo = re.search(r'src=".*" alt', image[0], re.M | re.I)
                if title1_photo:
                    image = re.sub(r'src="|" alt', "", title1_photo.group())
                else:
                    image = ''
                image = re.sub(r'&amp;', '&', image)
                image = re.sub(r'&quot;', '"', image)
                image = re.sub(r'&lt;', '<', image)
                image = re.sub(r'&gt;', '>', image)
            else:
                image=''
            item['image'] = image

            content = div.xpath('.//span[@class="c-font-normal c-color-text"]').extract()
            if len(content) > 0:
                title1_introduction = re.search(r'<!--s-text-->.*<!--/s-text-->', content[0], re.M | re.I)
                if title1_introduction:
                    content = re.sub(r'<!--s-text-->|<!--/s-text-->|<em>|</em>', "", title1_introduction.group())
                else:
                    content = ''
            item['content'] = content

            time= div.xpath('.//span[@class="c-color-gray2 c-font-normal"]').extract()
            if len(time) > 0:
                title1_time = re.search(r'">.*</span>', time[0], re.M | re.I)
                if title1_time:
                    time = re.sub(r'">|</span>', "",title1_time.group())
                else:
                    time = ''
            item['time'] = time

            title_poster= div.xpath('.//span[@class="c-color-gray c-font-normal c-gap-right"]/text()').extract()
            item['poster'] = title_poster[0]

            title_source = div.xpath('@mu').extract()
            item['source'] = title_source[0]

            item['sentiment'] = self.analyze(item['title'])
            yield item


        '''pageNum=100
        for page in range(0,pageNum,10):
            page='https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&ie=utf-8&word=%E4%B8%AD%E5%9B%BD%E9%97%BD%E5%8F%B0%E7%BC%98%E5%8D%9A%E7%89%A9%E9%A6%86&x_bfe_rqs=03E80&x_bfe_tjscore=0.100000&tngroupname=organic_news&newVideo=12&rsv_dl=news_b_pn&pn={}'.format(page)
            yield scrapy.Request(page,callback=self.parse)'''

        x = response.xpath('//div[@class="page-inner"]//a[@class="n"]').extract()
        for page in x:
            page1 = re.search(r'a href=".*" class="n">下一页', page, re.M | re.I)
            if page1:
                page = re.sub(r'a href="|" class="n">下一页', "", page1.group())
            else:
                page = ''
            page = re.sub(r'&amp;', '&', page)
            page = re.sub(r'&quot;', '"', page)
            page = re.sub(r'&lt;', '<', page)
            page = re.sub(r'&gt;', '>', page)
            total_title="https://www.baidu.com"
            page=total_title+page
            yield scrapy.Request(page, callback=self.parse, meta={'museumName':response.meta['museumName']},dont_filter=False)