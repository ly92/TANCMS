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

    def start_requests(self):
        for blog in self.blogs:
            url = blog['url']
            self.blog_id = blog['blog_id']
            self.base_url = url + '?&pn={}'
            yield scrapy.Request(url=url, callback=self.parse_content)

