import scrapy
import re
from ..libs.timeHelper import strToTimeStamp
import time
from TANCMS.libs.redisHelper import cacheGet
from ..items import CommentItem
from urllib import parse
from ..libs.ES import isOldComment


class TianyacommentSpider(scrapy.Spider):
    name = 'tianyaComment'

    base_url = ''
    blogs = cacheGet('tianyaComment_blogs')
    blog_id = ''
    page = 1
    start_urls = [
        # 'https://www.toutiao.com/a6841348279796498958',
        # 'https://www.toutiao.com/a6844326277470487048',
        # 'https://www.toutiao.com/a6882623302062309902',
        'https://www.toutiao.com/a6830715574046163464'
    ]

    def start_requests2(self):
        for blog in self.blogs:
            url = blog['url']
            self.blog_id = blog['blog_id']
            self.base_url = url + '?&pn={}'
            yield scrapy.Request(url=url, callback=self.parse_content)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_content)

    def parse_content(self, response):
        print(response.text())
        # spans = response.xpath('//*[@class="article-meta"]/span')
        # for span in spans:
        #     print(span.xpath('./text()'))

        pass
