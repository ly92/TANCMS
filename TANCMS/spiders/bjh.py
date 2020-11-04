import scrapy
import time
import re
from ..libs.ES import isExitByUrl
import json

from TANCMS.libs.redisHelper import cacheGet

class BjhSpider(scrapy.Spider):
    name = 'bjh'

    # base_url = 'https://www.baidu.com/s?q1={}&q2=&q3=&q4=&gpc=stf={},{}|stftype=1&ft=&q5=&q6=baijiahao.baidu.com&tn=baiduadv&pn={}'
    end = int(time.time())
    begin = int(time.time()) - 86400 * 1
    base_url = cacheGet('bjh_url')
    word = cacheGet('bjh_keyWord')
    pn = 0

    def start_requests(self):
        print('-------------')
        print(self.word, self.base_url, self.begin, self.end)
        print('-------------23')
        url = self.base_url.format(self.word, self.begin, self.end, self.pn)
        print(url)
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # divs = response.xpath('//*[@class="result c-container "]')
        # for div in divs:
        #     time.sleep(3)
        #     url = div.xpath('./h3/a/@href').extract_first()
        #     title_str = div.xpath('./h3/a').get()
        #     title_str = title_str.replace('<em>', '').replace('</em>', '')
        #     title = re.findall('target="_blank">(.*?)</a>', title_str, re.S)[0]
        #
        #     item = ArticleItem()
        #     item['title'] = title
        #     item['url'] = url
        #     item['htmlContent'] = ''
        #     item['content'] = ''
        #     item['source'] = '百家号'
        #     yield scrapy.Request(url=url, callback=self.parse_content, meta={'item': item})
        page_inner = response.xpath('//*[@class="page-inner"]/a')
        if len(page_inner) > 0 & self.pn < 50:
            time.sleep(3)
            last_a = page_inner[-1]
            if last_a.xpath('./text()').extract_first() == '下一页 >':
                self.pn = self.pn + 10
                url = self.base_url.format(self.word, self.begin, self.end, self.pn)
                print(url)
                yield scrapy.Request(url=url, callback=self.parse)

    def parse_content(self, response):
        s_advert = re.findall('var s_advert = (.*?);', response.text, re.S)[0]
        s_advert = json.loads(s_advert)
        url = s_advert['contentUrl']
        if not isExitByUrl(url):
            time_source = response.xpath('//*[@class="author-txt"]')
            t1 = time_source.xpath('./div/span[1]/text()').extract_first()
            t2 = time_source.xpath('./div/span[2]/text()').extract_first()
            time_str = '2020-' + t1.replace('发布时间：', '') + ' ' + t2
            timeArray = time.strptime(time_str, "%Y-%m-%d %H:%M")
            timeStamp = int(time.mktime(timeArray))
            author = time_source.xpath('./p/text()').extract_first()
            content_p = response.xpath('//*[@class="article-content"]/p')
            content = ''
            try:
                for p in content_p:
                    spans = p.xpath('./span')
                    p_str = ''
                    for span in spans:
                        s = span.xpath('./text()').extract_first()
                        if s:
                            p_str = p_str + s
                    content = content + p_str + "\n"
            except:
                content = ''
            item = response.meta['item']
            item['content'] = content
            item['htmlContent'] = response.xpath('//*[@class="article-content"]').get()
            item['time'] = timeStamp
            item['author'] = author
            item['url'] = url
            yield item




