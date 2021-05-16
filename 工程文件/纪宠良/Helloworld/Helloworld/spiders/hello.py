import scrapy
import re
import pymysql
from Helloworld.items import HelloworldItem
class HelloSpider(scrapy.Spider):
    name = 'hello'
    # 填写爬取地址
    allowed_domains = ["baidu.com"]
    #start_urls = ['https://www.baidu.com/s?ie=utf-8&medium=0&rtt=1&bsst=1&rsv_dl=news_t_sk&cl=2&wd=%E6%95%A6%E7%85%8C%E7%A0%94%E7%A9%B6%E9%99%A2&tn=news&rsv_bp=1&rsv_n=2&oq=&rsv_sug3=1&rsv_sug1=1&rsv_sug7=100&rsv_sug2=0&rsv_btype=t&f=8&inputT=483&rsv_sug4=483&rsv_sug=1']
    base_url = "https://www.baidu.com"
    def start_requests(self):
        prim='https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&ie=utf-8&word='
        urls=[]
        museum=['抗美援朝纪念馆','旅顺博物馆','沈阳故宫博物院','大连现代博物馆','吉林省自然博物馆','吉林省博物院','伪满皇宫博物院','东北烈士纪念馆','铁人王进喜纪念馆','瑷珲历史陈列馆','黑龙江省博物馆','大庆博物馆','上海博物馆','上海鲁迅纪念馆','中共一大会址纪念馆','上海科技馆','陈云纪念馆','南京博物院','侵华日军南京大屠杀遇难同胞纪念馆','南通博物苑','苏州博物馆','扬州博物馆','常州博物馆','南京市博物总馆','浙江省博物馆','浙江自然博物馆','中国丝绸博物馆']
        for mname in museum:
            urls.append(prim+mname)
        i=0
        for url in urls:
            conn = pymysql.Connect(
                host='127.0.0.1',  # 连接IP地址，如果是本地就是localhost
                user='root',  # 数据库用户名
                passwd='jclgogogo.',  # 据库密码
                db='test',  # 要查询的数据库名
                charset='utf8'  # 码
            )
            #mus_id
            c = conn.cursor()  # 标，上一行数据查完后，游标移至下一行继续查询
            c.execute('SELECT mus_id FROM `text_museum` where mus_name="'+museum[i]+'"')  # 行这条查询语句
            row = c.fetchone()  # etchone查询一行
            mid = row[0]
            yield scrapy.Request(url=url,meta={'museumName':museum[i],'museumId':mid},callback=self.parse)
            i+=1
    # 编写爬取方法

    def parse(self, response):
        print(response)
        for box in response.xpath('//div[@class="result-op c-container xpath-log new-pmd"]'):
            item = HelloworldItem()
            ###标题
            bbbb = box.xpath('.//h3[@class="news-title_1YtI1"]/a').extract()
            ab = bbbb[0]
            aaaaa = re.search(r'<!--s-text-->.*<!--/s-text-->', ab, re.M | re.I)
            if aaaaa:
                title = re.sub(r'<!--s-text-->|<!--/s-text-->|<em>|</em>', "", aaaaa.group())
            else:
                title = ''
            item['title'] = title
            # new_id
            conn = pymysql.Connect(
                host='127.0.0.1',  # 连接IP地址，如果是本地就是localhost
                user='root',  # 数据库用户名
                passwd='jclgogogo.',  # 据库密码
                db='test',  # 要查询的数据库名
                charset='utf8'  # 码
            )

            b=conn.cursor()
            b.execute('select new_id from test_m where title="' + item['title'] + '"')
            flag = b.fetchone()
            if(flag):
                continue
            b.execute('select MAX(new_id) from test_m ')
            row1 = b.fetchone()
            maxsize = row1[0]
            if (maxsize == None):
                maxsize = 0

            #博物馆
            item['mus_id'] = response.meta['museumId']
            item['id']=maxsize+1
            item['museum']=response.meta['museumName']
            #源地址
            father_url=box.xpath('@mu').extract()[0]
            item['source']=father_url

            # 获取图片地址
            cccc = box.xpath('.//div[@class="c-row c-gap-top-small"]//div[@class="c-img c-img3 c-img-radius-large"]').extract()
            if len(cccc) > 0:
                cb = cccc[0]
                ccccc = re.search(r'https.*alt', cb, re.M | re.I)
                if (ccccc):
                    image = re.sub(r' alt|"', "", ccccc.group())
                    image = re.sub(r'&amp;', '&', image)
                    image = re.sub(r'&quot;', '"', image)
                    image = re.sub(r'&lt;', '<', image)
                    image = re.sub(r'&gt;', '>', image)
            else:
                image=""
            item['image'] = image
            ###获取作者
            author=box.xpath('.//div[@class="news-source"]//span[@class="c-color-gray c-font-normal c-gap-right"]/text()').extract()
            item['poster']=author[0]

            time = box.xpath('.//div[@class="news-source"]//span[@class="c-color-gray2 c-font-normal"]/text()').extract()
            tim = ''
            if len(time)>0:
                tim = time[0]
            item['time'] = tim
            eeee=box.xpath('.//div[@class="c-row c-gap-top-small"]//span[@class="c-font-normal c-color-text"]').extract()
            content = ''
            if len(eeee)>0:
                eb = eeee[0]
                eeeee = re.search(r'<!--s-text-->.*<!--/s-text-->', eb, re.M | re.I)
                if eeeee:
                    content = re.sub(r'<!--s-text-->|<!--/s-text-->|<em>|</em>', "", eeeee.group())
            item['content']=content
            yield item
        next_url = response.xpath('//div[@id="page"]/div[@class="page-inner"]//a[contains(text(),"下一页")]').extract()
        if len(next_url) > 0:
            next = re.search(r'href=".*" class="n"', next_url[0], re.M | re.I)
            next = re.sub(r'href="|" class="n"', '', next.group())
            next = re.sub(r'&amp;', '&', next)
            next = re.sub(r'&quot;', '"', next)
            next = re.sub(r'&lt;', '<', next)
            next = re.sub(r'&gt;', '>', next)
            yield scrapy.Request(self.base_url + next, callback=self.parse, meta={'museumName':response.meta['museumName'],'museumId':response.meta['museumId']},dont_filter=False)