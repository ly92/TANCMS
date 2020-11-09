import scrapy
import re
import time
from ..items import BlogItem
from ..libs.ES import isExitByUrl
from TANCMS.libs.redisHelper import cacheGet
from ..libs.timeHelper import strToTimeStamp

class TianyaSpider(scrapy.Spider):
    name = 'tianya'

    page = 1
    base_url = cacheGet('tianya_url')
    word = cacheGet('tianya_keyWord')

    def start_requests(self):

        url = self.base_url.format(self.word, self.page)
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        ul = response.xpath('//*[@class="searchListOne"]/ul/li')
        for li in ul:
            try:
                url = li.xpath('./div/h3/a/@href').extract_first()
                if isExitByUrl(url):
                    continue
                title = li.xpath('./div/h3/a').get()
                title = title.replace('<span class="kwcolor">', '').replace('</span>', '')
                title = re.findall('target="_blank">(.*?)</a>', title, re.S)[0]
                author = li.xpath('./p/a[2]/text()').extract_first()
                time_str = li.xpath('./p/span[1]/text()').extract_first()

                blog = BlogItem()
                blog['title'] = title
                blog['url'] = url
                blog['blog_id'] = ''
                blog['content'] = ''
                blog['source'] = '天涯论坛'
                blog['author'] = author
                blog['author_url'] = 'https://m.weibo.cn/u/' + item['mblog']['user']['id']
                blog['author_id'] = item['mblog']['user']['id']
                blog['time'] = strToTimeStamp(time_str)
                time.sleep(2)
                yield scrapy.Request(url=url, callback=self.parse_content, meta={'item': blog})
            except:
                pass

        if len(ul) > 0 and self.page < 40:
            self.page = self.page + 1
            url = self.base_url.format(self.word, self.page)
            time.sleep(3)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_content(self, response):
        contents = response.xpath('//*[@class="bbs-content clearfix"]/text()').extract()
        content = "\\n".join(contents)
        content = content.replace('\\u3000', ' ').replace('\\n', '').replace('\\t', '')
        item = response.meta['item']
        item['content'] = content
        yield item
