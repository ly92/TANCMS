import scrapy
import re
from ..libs.timeHelper import strToTimeStamp
import time
from TANCMS.libs.redisHelper import cacheGet
from ..items import BlogItem
from ..libs.ES import isExitByUrl
from urllib import parse
import json

class TiebabloggerSpider(scrapy.Spider):
    name = 'tiebaBlogger'

    bars = cacheGet('bars')
    if bars:
        bars = json.loads(bars)

    base_url = ''
    word = ''
    page = 1

    def start_requests(self):
        for bar in self.bars:
            self.page = 1
            self.base_url = bar['url']
            self.word = bar['word']
            url = self.base_url.format(self.word, self.page)
            yield scrapy.Request(url=url, callback=self.parse_tie)


    # 解析贴吧内容列表
    def parse_tie(self, response):
        divs = response.xpath('//*[@class="s_post_list"]/div')
        for div in divs:
            title = div.xpath('./span/a').get()
            a_s = re.findall('<a(.*?)>', title, re.S)
            for a in a_s:
                title = title.replace('<a' + a + '>', '')
            title = title.replace('<em>', '').replace('</em>', '').replace('</a>', '')
            ba = div.xpath('./a[1]/font/text()').extract_first()
            author = div.xpath('./a[2]/font/text()').extract_first()
            time = div.xpath('./font/text()').extract_first()
            time_str = strToTimeStamp(time)
            url = div.xpath('./span/a/@href').extract_first()
            url = 'https://tieba.baidu.com' + re.findall('(.*?)\?', url, re.S)[0]
            url_arr = url.split('?')
            if len(url_arr) > 0:
                url = url_arr[0]
            if not isExitByUrl(url):
                blog = BlogItem()
                blog['url'] = url
                blog['blog_id'] = div.xpath('./span/a/@data-tid').extract_first()
                blog['title'] = title
                blog['content'] = ''
                blog['time'] = time_str
                blog['source'] = '百度贴吧'

                blog['ba'] = ba
                blog['ba_url'] = 'https://tieba.baidu.com/f?kw=' + ba

                blog['author'] = author
                author_url = div.xpath('./a[2]/@href').extract_first()
                blog['author_url'] = parse.unquote(author_url, encoding='GBK')
                yield blog

            page_inner = response.xpath('//*[@class="pager pager-search"]/a')
            if len(page_inner) > 0 & self.page < 40:
                last_a = page_inner[-2]
                if last_a.xpath('./text()').extract_first() == '下一页>':
                    self.page = self.page + 1
                    url = self.base_url.format(self.word, self.begin, self.end, self.pn)
                    print(url)
                    time.sleep(3)  # 获取下一页文章前停留一会
                    yield scrapy.Request(url=url, callback=self.parse)
                yield scrapy.Request(url=url, callback=self.parse_content)




