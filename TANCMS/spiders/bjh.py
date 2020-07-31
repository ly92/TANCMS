import scrapy
import time
import re
from ..libs.ES import isExitByUrl
from ..items import ArticleItem

class BjhSpider(scrapy.Spider):
    name = 'bjh'

    base_url = 'https://www.baidu.com/s?q1={}&q2=&q3=&q4=&gpc=stf={},{}|stftype=1&ft=&q5=&q6=baijiahao.baidu.com&tn=baiduadv&pn={}'
    end = time.time()
    begin = int(time.time()) - 86400 * 30
    word = '核酸检测'
    page = 3

    def start_requests(self):
        url = self.base_url.format(self.word, self.begin, self.end, self.page)
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        divs = response.xpath('//*[@class="result c-container "]')
        for div in divs:
            url = div.xpath('./h3/a/@href').extract_first()
            # if isExitByUrl(url):
            #     continue
            title_str = div.xpath('./h3/a').get()
            title_str = title_str.replace('<em>', '').replace('</em>', '')
            title = re.findall('target="_blank">(.*?)</a>', title_str, re.S)[0]

            item = ArticleItem()
            item['title'] = title
            item['url'] = url
            item['htmlContent'] = ''
            item['content'] = ''
            item['source'] = '百家号'

            yield scrapy.Request(url=url, callback=self.parse_content, meta={'item': item})

    def parse_content(self, response):

        time_source = response.xpath('//*[@class="author-txt"]')
        t1 = time_source.xpath('./div/span[1]/text()').extract_first()
        t2 = time_source.xpath('./div/span[2]/text()').extract_first()
        time_str = '2020-' + t1.replace('发布时间：', '') + ' ' + t2
        timeArray = time.strptime(time_str, "%Y-%m-%d %H:%M")
        timeStamp = int(time.mktime(timeArray))

        author = time_source.xpath('./p/text()').extract_first()

        content_p = response.xpath('//*[@class="article-content"]/p')
        content = ''
        for p in content_p:
            spans = p.xpath('./span')
            p_str = ''
            for span in spans:
                p_str = p_str + span.xpath('./text()').extract_first()
            content = content + p_str + "\n"
        item = response.meta['item']
        item['content'] = content
        item['htmlContent'] = response.xpath('//*[@class="article-content"]').get()
        item['time'] = timeStamp
        item['author'] = author

        # yield item

