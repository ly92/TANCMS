import scrapy
import json
from ..libs.ES import isExitByUrl
from ..libs.timeHelper import strToTimeStamp
from ..items import BlogItem
import time
from TANCMS.libs.redisHelper import cacheGet

class WeiboSpider(scrapy.Spider):
    name = 'weibo'

    page = 1
    base_url = cacheGet('weibo_url')
    word = cacheGet('weibo_keyWord')


    def start_requests(self):
        url = self.base_url.format(self.word, self.page)
        yield scrapy.Request(url=url, meta={
                 'dont_redirect': True,
                 'handle_httpstatus_list': [302]
                }, callback=self.parse)
        pass

    def parse(self, response):

        res = json.loads(response.text)
        data = res['data']['cards']
        for item in data:
            url = 'https://m.weibo.cn/status/' + item['mblog']['id']
            if isExitByUrl(url):
                continue
            blog = BlogItem()
            blog['url'] = url
            blog['blog_id'] = item['mblog']['id']
            text = item['mblog']['text']
            blog['title'] = text[0:30]
            blog['content'] = text
            blog['time'] = strToTimeStamp(item['mblog']['created_at'])
            blog['source'] = '新浪微博'

            blog['author'] = item['mblog']['user']['screen_name']
            blog['author_url'] = 'https://m.weibo.cn/u/' + item['mblog']['user']['id']
            blog['auth_id'] = item['mblog']['user']['id']
            if text.endswith('全文</a>') > 0:
                url2 = 'https://m.weibo.cn/statuses/extend?id=' + item['mblog']['id']
                yield scrapy.Request(url=url2, callback=self.content_parse, meta={'item': blog})
            else:
                yield blog

        if len(data) == 10 & self.page < 20:
            time.sleep(5)  # 获取下一页文章前停留一会
            self.page = self.page + 1
            url = self.base_url.format(self.word, self.page)
            yield scrapy.Request(url=url, callback=self.parse)

    def content_parse(self, response):
        res = json.loads(response.text)
        blog = response.meta['item']
        if res['ok'] == 1 & res['data']['ok'] == 1:
            htmlContent = res['data']['longTextContent']
            blog['content'] = htmlContent

        yield blog

