import scrapy
import json
from ..libs.ES import isExitBlogByUrl
from ..libs.timeHelper import formatTime
from ..items import BlogItem
import time
from TANCMS.libs.redisHelper import cacheGet


class WeibobloggerSpider(scrapy.Spider):
    name = 'weiboBlogger'

    bloggers = cacheGet('bloggers')
    if bloggers:
        bloggers = json.loads(bloggers)

    stepOne = ''
    stepTwo = ''
    containerid = ''
    since_id = ''

    def start_requests(self):
        for blogger in self.bloggers:
            self.stepOne = blogger['stepOne']
            self.stepTwo = blogger['stepTwo']

            yield scrapy.Request(url=self.stepOne, meta={
                'dont_redirect': True,
                'handle_httpstatus_list': [302]
            }, callback=self.parse)
            pass

    def parse(self, response):
        res = json.loads(response.text)
        if res['ok']:
            for tab in res['data']['tabsInfo']['tabs']:
                if tab['type'] == 'weibo':
                    self.containerid = tab['containerid']
                    url = self.stepTwo.format(self.containerid, '')
                    time.sleep(5)  # 获取下一页文章前停留一会
                    yield scrapy.Request(url=url, meta={
                        'dont_redirect': True,
                        'handle_httpstatus_list': [302]
                    }, callback=self.parse_list())

    def parse_list(self, response):

        res = json.loads(response.text)
        if res['ok']:
            self.since_id = res['data']['cardlistInfo']['4567181164025859']
            data = res['data']['cards']
            for item in data:
                url = 'https://m.weibo.cn/status/' + item['mblog']['id']
                if not isExitBlogByUrl(url):
                    blog = BlogItem()
                    blog['url'] = url
                    blog['blog_id'] = item['mblog']['id']
                    text = item['mblog']['text']
                    blog['title'] = text[0:30]
                    blog['content'] = text
                    blog['time'] = formatTime(item['mblog']['created_at'])
                    blog['source'] = '新浪微博'

                    blog['author'] = item['mblog']['user']['screen_name']
                    blog['author_url'] = 'https://m.weibo.cn/u/' + item['mblog']['user']['id']
                    blog['author_id'] = item['mblog']['user']['id']
                    if text.endswith('全文</a>') > 0:
                        url2 = 'https://m.weibo.cn/statuses/extend?id=' + item['mblog']['id']
                        time.sleep(2)  # 获取下一页文章前停留一会
                        yield scrapy.Request(url=url2, callback=self.content_parse, meta={'item': blog})
                    else:
                        yield blog

                    url = self.stepTwo.format(self.containerid, self.since_id)
                    time.sleep(5)  # 获取下一页文章前停留一会
                    yield scrapy.Request(url=url, meta={
                        'dont_redirect': True,
                        'handle_httpstatus_list': [302]
                    }, callback=self.parse_list())

    def content_parse(self, response):
        res = json.loads(response.text)
        blog = response.meta['item']
        if res['ok'] == 1 & res['data']['ok'] == 1:
            htmlContent = res['data']['longTextContent']
            blog['content'] = htmlContent

        yield blog
