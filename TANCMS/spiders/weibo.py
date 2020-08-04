import scrapy
import json
from ..libs.ES import isExitByUrl
from ..items import ArticleItem
import time
import re


class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    base_url = 'http://sinanews.sina.cn/interface/type_of_search.d.html?keyword={}&page={}&type=siftWb&size=20&newpage=0&chwm=&imei=&token=&did=&from=&oldchwm='
    page = 1
    word = '核酸检测'

    def start_requests(self):
        url = self.base_url.format(self.word, self.page)
        url = 'http://www.weibo.com/1715196611/JdlA1qDdR'
        yield scrapy.Request(url=url, meta={
                 'dont_redirect': True,
                 'handle_httpstatus_list': [302]
                }, callback=self.parse)
        pass

    def parse(self, response):
        print(response.text)


        # res = json.loads(response.text)
        # data = res['data']['feed1']
        # for item in data:
        #     url = item['url']
        #     # if isExitByUrl(url):
        #     #     continue
        #     acticle = ArticleItem()
        #     acticle['url'] = url
        #     acticle['author'] = item['user']['name']
        #     acticle['title'] = item['title'][0:30]
        #     acticle['content'] = item['title']
        #     acticle['htmlContent'] = ''
        #     # time_str = '2020年' + item['time']
        #     # timeArray = time.strptime(time_str, "%Y年%m月%d日 %H:%M")
        #     # timeStamp = int(time.mktime(timeArray))
        #     # acticle['creationTime'] = timeStamp
        #     url2 = url + '?type=comment#_rnd' + str(int(time.time()))
        #     yield scrapy.Request(url=url2, callback=self.content_parse, meta={'item': acticle})

        # if len(data) == 20:
        #     time.sleep(3)
        #     self.page = self.page + 1
        #     url = self.base_url.format(self.word, self.page)
        #     yield scrapy.Request(url=url, callback=self.parse)


    def content_parse(self, response):

        print('-------------------------')
        print(response.text)
        print('-------------------------')


        content = response.xpath('//*[@class="WB_text W_f14"]').get()

        print('-------------------------')
        print(content)
        print('-------------------------')

        item = response.meta['item']
        item['htmlContent'] = content

        aaa = re.findall('<a(.*?)>', content, re.S)
        for s in aaa:
            content = content.replace(s, '')
        content = content.replace('<a>', '').replace('</a>', '')
        item['content'] = content

        print(item)

