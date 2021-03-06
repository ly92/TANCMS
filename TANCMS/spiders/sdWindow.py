import scrapy
import json
from ..items import ArticleItem
from ..libs.ES import isExitByUrl
from urllib.parse import urlparse
import time
from TANCMS.libs.redisHelper import cacheGet

class SdWindowSpider(scrapy.Spider):
    name = 'sdWindow'
    word = '核酸检测'
    page = 1
    max_page = 1

    num1 = 0
    num2 = 0
    num3 = 0

    # json列表推荐
    # base_url = 'http://www.beijing.gov.cn/so/interest?sort=dateDesc&timeOption=1&days=30&qt={}&tab=all&siteCode=1100000088&keyPlace=0&toolsStatus=1&mode=1&pageSize=20&page={}'

    base_url = cacheGet('sdWindow_url')
    word = cacheGet('sdWindow_keyWord')

    def start_requests(self):
        url = self.base_url.format(self.word, self.page)
        print(url)
        yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        response = json.loads(response.text)
        totalHits = response['totalHits']
        resultList = response['resultList']

        self.max_page = totalHits // 20 + 1

        for result in resultList:
            url = result['url']
            parse = urlparse(url)
            if parse.path.startswith('/shipin/'):
                self.num1 = self.num1 + 1
                continue
            if isExitByUrl(url):
                self.num2 = self.num2 + 1
                continue
            time.sleep(2)
            self.num3 = self.num3 + 1
            item = ArticleItem()
            item['title'] = result['title']
            item['url'] = url
            item['htmlContent'] = ''
            item['content'] = ''
            item['source'] = '首都之窗'
            item['author'] = ''
            item['time'] = result['myValues']['DREDATE']
            print(item)
            # yield scrapy.Request(url=url, callback=self.parse_content, dont_filter=True, meta={'item': item})
        if self.page < self.max_page:
            self.page = self.page + 1
            url = self.base_url.format(self.word, self.page)
            time.sleep(3)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
        # print('-----------------')
        # print(self.num1)
        # print(self.num2)
        # print(self.num3)
        # print(self.max_page)
        # print(self.page)
        # print('-----------------')


    def parse_content(self, response):
        item = response.meta['item']
        author = response.xpath('//*[@id="othermessage"]/p/span[2]/text()').extract_first()
        item['author'] = author.replace('来源：', '')
        content_html = response.xpath('//*[@class="view TRS_UEDITOR trs_paper_default trs_web"]//p')
        content = ''
        htmlContent = ''
        for p in content_html:
            htmlContent = htmlContent + p.get()
            content = content + p.xpath('text()').extract_first() + "\n"
        item['content'] = content.replace('\\u3000', ' ')
        item['htmlContent'] = htmlContent.replace('\\u3000', ' ')
        yield item








    # 网页版
    # base_url = 'http://www.beijing.gov.cn/so/s?sort=dateDesc&timeOption=1&days=30&toolsStatus=1&qt={}&tab=all&siteCode=1100000088&page={}'
    # divs = response.xpath('//*[@class="news clearfix"]')
    # for div in divs:
    #     title_str = div.xpath('./*[@class="title"]/a/text()').extract_first()
    #     title_href = div.xpath('./*[@class="title"]/a/@href').extract_first()
    #     author = div.xpath('./div[2]/div[2]/a/text()').extract_first()

    # 网页内获取列表 post请求 返回 json
    # base_url = 'http://www.beijing.gov.cn/so/news?siteCode=1100000088&qt=核酸检测&tab=all&pageSize=20&redTitleLength=28&combine=MD5TITLE&mode=1'

