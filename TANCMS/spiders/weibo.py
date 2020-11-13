import scrapy
import json
from ..libs.ES import isExitBlogByUrl
from ..libs.timeHelper import formatTime
from ..items import BlogItem
import time
from TANCMS.libs.redisHelper import cacheGet
import urllib
import re

class WeiboSpider(scrapy.Spider):
    name = 'weibo'

    page = 1
    # base_url = cacheGet('weibo_url')
    base_url = ''
    word = cacheGet('weibo_keyWord')


    def start_requests(self):
        # url中的一段需要编码
        s1 = 'https://m.weibo.cn/api/container/getIndex?containerid=100103'
        s2 = 'type=60&q=' + self.word + '&t=0'
        s3 = '&page_type=searchall&page={}'
        self.base_url = s1 + urllib.parse.quote(s2, 'utf-8') + s3

        url = self.base_url.format(self.page)
        yield scrapy.Request(url=url, meta={
                 'dont_redirect': True,
                 'handle_httpstatus_list': [302]
                }, callback=self.parse)
        pass

    def parse(self, response):

        res = json.loads(response.text)

        data = res['data']
        if 'cards' in data.keys():
            cards = data['cards']
        else:
            cards = []
        for item in cards:
            url = 'https://m.weibo.cn/status/' + item['mblog']['id']
            if isExitBlogByUrl(url):
                continue
            blog = BlogItem()
            blog['url'] = url
            blog['blog_id'] = item['mblog']['id']
            text = item['mblog']['text']
            text = self.getContent(text)
            blog['title'] = text[0:30]
            blog['content'] = text
            blog['time'] = formatTime(item['mblog']['created_at'])
            blog['source'] = '新浪微博'

            blog['author'] = item['mblog']['user']['screen_name']
            blog['author_id'] = str(item['mblog']['user']['id'])
            blog['author_url'] = 'https://m.weibo.cn/u/' + blog['author_id']
            blog['bar'] = ''
            blog['bar_url'] = ''
            if text.endswith('全文') > 0:
                url2 = 'https://m.weibo.cn/statuses/extend?id=' + item['mblog']['id']
                yield scrapy.Request(url=url2, callback=self.content_parse, meta={'item': blog})
            else:
                yield blog

        if len(data) > 0 and self.page < 40:
            time.sleep(5)  # 获取下一页文章前停留一会
            self.page = self.page + 1
            url = self.base_url.format(self.page)
            yield scrapy.Request(url=url, callback=self.parse)

    def content_parse(self, response):
        res = json.loads(response.text)
        blog = response.meta['item']
        if res['ok'] == 1 & res['data']['ok'] == 1:
            htmlContent = res['data']['longTextContent']
            blog['content'] = self.getContent(htmlContent)

        yield blog


    def getContent(self, content):
        a_s = re.findall('<a(.*?)>', content, re.S)
        for a in a_s:
            content = content.replace(a, '')
        span_s = re.findall('<span(.*?)>', content, re.S)
        for span in span_s:
            content = content.replace(span, '')
        img_s = re.findall('<img(.*?)>', content, re.S)
        for img in img_s:
            content = content.replace(img, '')
        content = content.replace('<a>', '').replace('<span>', '').replace('</a>', '').replace('</span>', '').replace(
            '<img>', '').replace('<br />', '')
        return content